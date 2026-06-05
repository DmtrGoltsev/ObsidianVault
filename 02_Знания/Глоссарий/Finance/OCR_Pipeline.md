---
id: "term-ocr-pipeline"
тип: "термин"
проект: "Finance"
термин: "OCR Pipeline"
термин_en: "OCR Pipeline"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance", "ocr", "backend"]
источник: "apps/backend/src/app/capture_drafts/aggregate_parser.py"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Capture_Draft]]"
---

# OCR Pipeline (Конвейер распознавания)

## Определение

Конвейер преобразования скриншота банковского приложения в структурированные данные о расходах по категориям. Полный цикл: **raw image → Tesseract OCR → layout-aware parsing → `CategoryAggregateCandidate`**. Реализован в модуле `capture_drafts`.

## Архитектура pipeline

### 1. TesseractScreenshotOcrEngine

`apps/backend/src/app/capture_drafts/ocr_engine.py` — word-level extraction через pytesseract.

- Возвращает `ScreenshotOcrResult` с текстом и кортежем `ScreenshotOcrWord` (bounding boxes + confidence)
- **Препроцессинг изображения**: конвертация в grayscale (`L`), autocontrast, upscale ×2 если ширина < 1400px
- Поддерживаемые форматы: PNG, JPEG, WEBP
- Конфигурируется через `Settings`: язык, таймаут, путь к tesseract binary

### 2. ScreenshotOcrService

`apps/backend/src/app/capture_drafts/screenshot_ocr_service.py` — адаптер-оркестратор.

- Валидирует загрузку (`validate_screenshot_upload`)
- Вызывает engine через `_extract_ocr_result` — поддерживает как `extract_result` (word-level), так и fallback на `extract_text` (text-only)
- Передаёт результат в `parse_category_aggregate_screenshot_ocr`
- Маппит кандидатов через `CaptureCategoryMappingService`
- Формирует `ScreenshotOcrResponseDto` с предупреждениями

### 3. aggregate_parser (Layout-aware парсер)

`apps/backend/src/app/capture_drafts/aggregate_parser.py` — двухколоночный парсер с пространственным анализом.

- **Кластеризация слов в строки**: слова сортируются по Y-координате центра, группируются с tolerance = `max(8, median_height * 0.75)`
- **Разделение колонок**: порог 58% ширины страницы — слова левее порога = label, правее = amount
- **Извлечение label**: сбор label-частей из предыдущих строк с ограничением по вертикали (72px gap)
- **Поиск operation count**: lookahead до 4 строк, lookbehind до 4 строк
- **Дедупликация** кандидатов по ключу (normalized label, amount, operation_count)

## Ключевые сущности

| Сущность | Тип | Файл | Назначение |
|---|---|---|---|
| `OcrWordLike` | Protocol | `aggregate_parser.py` | Интерфейс word-level данных: `text`, `left`, `top`, `width`, `height`, `confidence` |
| `_LayoutLine` | dataclass | `aggregate_parser.py` | Группировка слов в строку по Y-координате |
| `_OperationCountLine` | dataclass | `aggregate_parser.py` | Связка `(index, count)` для split operation counts |
| `ScreenshotOcrWord` | dataclass | `ocr_engine.py` | Реализация word-level данных из Tesseract |
| `ScreenshotOcrResult` | dataclass | `ocr_engine.py` | Результат OCR: текст + кортеж слов |
| `CategoryAggregateCandidate` | dataclass | `aggregate_parser.py` | Итоговый структурированный кандидат с idempotency key |
| `ParsedAmount` | dataclass | `aggregate_parser.py` | Разобранная сумма: `amount` (Decimal) + `currency` |

## Модель confidence

| Режим | Confidence | Условие |
|---|---|---|
| Layout-aware | **0.9** | Используются bounding boxes, двухколоночный разбор |
| Text-only | **0.82** | Fallback на обычный текст без пространственных данных |

### Порог фильтрации слов

Слова с `confidence < 15` отбрасываются, **кроме** слов содержащих цифры — они сохраняются всегда. Это предотвращает потерю сумм при низком качестве распознавания.

## Edge cases

Реализовано 5 семантических кейсов:

1. **Шумовые слова (noisy aggregates)** — фильтрация кириллических символов в `_is_edge_label_noise`: короткие не-кириллические токены (≤4 символа) и односимвольные кириллические удаляются с краёв label
2. **Right-only rows** — строки, где amount виден только в правой колонке без label слева; парсер ищет operation count в предыдущих строках (`_previous_operation_count_line`)
3. **Split operation counts** — число операций разбито OCR на 2 строки: цифры на одной, слово «операций» на следующей (`_split_operation_count`)
4. **Standalone operation labels** — строка только со словом «операций» без числа; распознаётся через `_OPERATION_WORD_ONLY_RE` и не считается label-строкой
5. **Low-confidence amounts** — токены с цифрами сохраняются при `confidence < 15` через проверку `_contains_digit` в фильтрации слов

## Idempotency

Формат ключа:

```
capture-v1:screenshot:category-aggregate:{time_bucket}:{amount}:{currency}:{label_hash}:{evidence_hash}
```

- `time_bucket` — timestamp, округлённый до минуты
- `label_hash` — первые 16 символов SHA-256 от normalized label
- `evidence_hash` — SHA-256 от конкатенации `source|version|label|amount|currency|count|bucket`, обрезанный до 16 символов
- `amount` в ключе — Decimal с `_` вместо `.`

## PARSE_VERSION

`category-aggregate-v1` — версия формата парсинга, используется в idempotency key и evidence hash.

## Связанные термины

- [[Capture_Draft]] — контейнер распознанных данных
- [[Transaction]] — целевая сущность, создаваемая из распознанных кандидатов
- [[MOC_Finance]] — карта модуля Finance

## Источник

- `apps/backend/src/app/capture_drafts/aggregate_parser.py` — layout-aware парсер, модели данных
- `apps/backend/src/app/capture_drafts/ocr_engine.py` — Tesseract wrapper, word-level extraction
- `apps/backend/src/app/capture_drafts/screenshot_ocr_service.py` — сервис-адаптер
