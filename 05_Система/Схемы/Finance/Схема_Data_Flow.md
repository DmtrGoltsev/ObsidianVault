---
id: "scheme-finance-data-flow"
тип: "схема"
проект: "Finance"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["схема", "finance", "data-flow", "ocr"]
ссылки:
  - "[[MOC_Finance]]"
---

# Finance — Data Flow: Capture Drafts OCR

## Общий поток

```
Пользователь ──► скриншот чека (финансовый отчет из банка)
    │
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│              Ветвление по платформе                     │
│                                                         │
│  ┌──────────────────┐    ┌───────────────────────────┐ │
│  │  Android          │    │  PWA / iOS                 │ │
│  │                   │    │                            │ │
│  │  ML Kit OCR       │    │  Загрузка скриншота        │ │
│  │  (on-device)      │    │  на сервер                 │ │
│  │       │           │    │       │                    │ │
│  │       ▼           │    │       ▼                    │ │
│  │  CaptureParser    │    │  POST /capture-drafts/     │ │
│  │  → кандидаты      │    │       screenshot-ocr       │ │
│  │       │           │    │       (PNG/JPEG/WebP,      │ │
│  │       ▼           │    │        max 8MB, 16Mpx)     │ │
│  │  POST /capture-   │    │                            │ │
│  │  drafts           │    │                            │ │
│  │  (candidates)     │    │                            │ │
│  └───────┬───────────┘    └──────────┬─────────────────┘ │
│          │                           │                    │
└──────────┼───────────────────────────┼────────────────────┘
           │                           │
           ▼                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend Pipeline                      │
│                                                         │
│  PWA/iOS path:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ScreenshotOcrService                              │  │
│  │  ├── validate_screenshot_upload (формат, размер)   │  │
│  │  ├── TesseractScreenshotOcrEngine                  │  │
│  │  │   └── word-level extraction                     │  │
│  │  │       (bounding boxes + confidence)             │  │
│  │  └── parse_category_aggregate_screenshot_ocr       │  │
│  │       └── aggregate_parser.py                      │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  Общий парсинг (обе ветки сходятся):                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  aggregate_parser.py                               │  │
│  │  ├── Двухколоночная эвристика (58% ширины)         │  │
│  │  ├── _LayoutLine кластеризация слов                │  │
│  │  ├── Сумма → ParsedAmount (₽/руб/$)               │  │
│  │  ├── Количество операций (операции N)              │  │
│  │  ├── deduplicate_candidates                        │  │
│  │  └── → list[CategoryAggregateCandidate]            │  │
│  │       ├── external_label                           │  │
│  │       ├── amount, currency                         │  │
│  │       ├── operation_count                          │  │
│  │       ├── confidence                               │  │
│  │       ├── idempotency_key                          │  │
│  │       └── evidence_hash                            │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  CaptureCategoryMappingService                     │  │
│  │  ├── lookup_suggested_category_id                  │  │
│  │  │   └── external_label_hash → внутренняя категория│  │
│  │  └── Хранит только хеш метки, не raw-текст         │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  CaptureDraft (PostgreSQL)                         │  │
│  │  ├── status: pending → confirmed / discarded       │  │
│  │  ├── idempotency_key (дедупликация)                │  │
│  │  └── evidence_hash (связь с OCR-результатом)       │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼ (user confirm)                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Transaction (sourceType = manual)                 │  │
│  │  ├── accountId                                     │  │
│  │  ├── categoryId                                    │  │
│  │  ├── amount, currency, occurredAt                  │  │
│  │  └── createdByUserId                               │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Lifecycle Capture Draft

```
pending ────► confirmed ────► Transaction (создана)
   │
   └────────► discarded     (отклонён пользователем)
```

## Privacy-инварианты OCR

```
✗ Скриншоты и raw OCR-текст НЕ сохраняются в:
    ├── логи
    ├── audit
    ├── backups
    ├── object storage
    └── debug dumps

✓ Сохраняется только:
    ├── normalized label hash (в category_mapping)
    └── draft metadata (pending / confirmed / discarded)
```

## Парсеры — детали

```
aggregate_parser.py:
│
├── parse_category_aggregate_screenshot_ocr()
│   ├── Вход: OCR text + ocr_words (word-level data)
│   ├── Фильтр header-строк ("расходы", "доходы", "операции")
│   ├── Фильтр summary-строк ("ещё N категорий")
│   ├── Двухколоночная эвристика:
│   │   └── правая колонка ≥ 58% ширины → amount-колонка
│   ├── _LayoutLine кластеризация (Y-близость слов)
│   ├── extract_layout_amount() из правой колонки
│   └── → CategoryAggregateCandidate[]
│
├── deduplicate_candidates()
│   └── Удаление дубликатов по (label + amount + count)
│
└── normalize_aggregate_label()
    └── Нормализация для external_label_hash
```
