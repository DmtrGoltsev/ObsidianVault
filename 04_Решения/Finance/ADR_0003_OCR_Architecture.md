---
id: "adr-finance-0003"
тип: "решение"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["ADR", "finance", "архитектура", "OCR", "capture"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[ADR_0001_Stack_Repo_Layout]]"
  - "[[ADR_0004_Capture_Drafts_Lifecycle]]"
---

# ADR-0003: Разделённая OCR-архитектура

## Статус

Утверждено. Реализовано в backend и Android.

## Контекст

Finance позволяет пользователям создавать транзакции из скриншотов банковских приложений. OCR-распознавание должно работать на двух платформах:

- **Android** — нативное приложение с доступом к ML Kit (on-device). Может распознавать текст без отправки изображения на сервер (privacy, скорость, offline capability).
- **PWA / iOS** — браузерный клиент без доступа к on-device OCR. Требуется серверная обработка.

Скриншоты банковских приложений имеют специфическую структуру: двухколоночный layout с категориями слева, суммами справа, и количеством операций под/над суммой. Стандартный линейный OCR не справляется с таким layout.

## Решение

### Двухуровневая OCR-стратегия

**Android: on-device OCR (ML Kit)**
- Распознавание текста выполняется локально через Google ML Kit.
- Результат (текст + bounding boxes) передаётся в `CaptureParser.parseScreenshotOcrResult()`.
- Изображение не покидает устройство — нет серверной загрузки, нет privacy-рисков.
- Парсинг текста выполняется на устройстве: извлечение суммы, валюты, merchant, confidence scoring.

**PWA / iOS: server-side OCR (Tesseract)**
- Изображение загружается на backend как temporary upload.
- `TesseractScreenshotOcrEngine` обрабатывает изображение: grayscale + autocontrast + upscaling для изображений < 1400px.
- Возвращает `ScreenshotOcrResult` с текстом и positional words (bounding boxes).
- После обработки изображение не хранится постоянно (temporary only).

### Layout-aware двухколоночный парсер

Обе платформы используют концептуально идентичную логику парсинга агрегированных скриншотов:

- **Word clustering** — OCR-слова группируются в строки по Y-координате с tolerance на основе median height.
- **Right column detection** — граница колонок вычисляется как 58% ширины (`min_left + (max_right - min_left) * 0.58`).
- **Label extraction** — текст слева от границы распознаётся как название категории.
- **Amount matching** — текст справа от границы парсится через regex с поддержкой ₽, RUB, USD, EUR, разделителей (пробел, запятая, точка).
- **Operation count** — число операций ищется на той же или следующей строке (regex `\d+ операций`).
- **Evidence hash** — SHA-256 от нормализованных данных (label + amount + currency + operation_count + time_bucket) для idempotency и дедупликации.

### Confidence scoring

- Layout-based parsing: confidence `0.90` (позиционные данные надёжнее).
- Text-only parsing: confidence `0.82` (fallback без positional data).
- Android single-capture: base `0.45` + бонусы за expense signals (`+0.25`), merchant (`+0.20`), broker signals (`+0.15`), card signals (`+0.05`), capped at `0.95`.

## Альтернативы

1. **Полностью серверный OCR** — отклонено для Android. Нарушает privacy (загрузка скриншотов), добавляет latency, создаёт зависимость от сети.
2. **Полностью on-device** — отклонено. PWA/iOS не имеют доступа к надёжному on-device OCR. ML Kit не работает в браузере.
3. **ML Kit для всех через WebView bridge** — отклонено. Неприемлемая сложность интеграции для PWA, ненадёжность в iOS WebView.

## Последствия

### Положительные

- Android: полная privacy — изображения не покидают устройство.
- PWA: серверный fallback обеспечивает функциональность.
- Layout-aware парсер обрабатывает сложные двухколоночные скриншоты, а не только однострочные уведомления.
- Evidence hash + idempotency key предотвращают дубли при повторных распознаваниях одного скриншота.

### Издержки

- Две реализации парсера (Kotlin `CaptureParser` + Python `aggregate_parser`) — необходимо поддерживать синхронность regex и логики нормализации.
- Серверная загрузка изображений для PWA/iOS — temporary storage, TTL, cleanup.
- `TesseractScreenshotOcrEngine` зависит от system-installed Tesseract binary — deployment complexity.

## Ссылки

- `apps/backend/src/app/capture_drafts/ocr_engine.py` — `TesseractScreenshotOcrEngine`, validation, `ScreenshotOcrWord`/`ScreenshotOcrResult`
- `apps/backend/src/app/capture_drafts/aggregate_parser.py` — layout-aware двухколоночный парсер, `CategoryAggregateCandidate`, evidence hash
- `apps/backend/src/app/capture_drafts/screenshot_ocr_service.py` — координация OCR и парсинга
- `apps/android/app/src/main/java/com/finance/mvp/capture/CaptureParser.kt` — Android on-device парсинг, confidence scoring
- `apps/android/app/src/main/java/com/finance/mvp/capture/CaptureCandidate.kt` — DTO результата парсинга
