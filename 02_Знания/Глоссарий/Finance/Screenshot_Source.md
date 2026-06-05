---
id: "term-screenshot-source"
тип: "термин"
проект: "Finance"
термин: "Screenshot Source"
термин_en: "Screenshot Source"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "db/migrations/versions/20260528_0008_restrict_capture_drafts_screenshot_source.py, apps/backend/src/app/db/model_enums.py"
ссылки:
  - "[[MOC_Finance]]"
---

Единственный разрешённый источник capture drafts в MVP — скриншот. CHECK-ограничение в БД гарантирует, что `capture_source` может быть только `'screenshot'`.

## Ключевые аспекты

- **CHECK constraint**: `ck_capture_drafts_capture_source_valid` — `capture_source IN ('screenshot')`
- **Миграция `0008`**: tightened constraint с `('sms', 'notification', 'screenshot')` до `('screenshot')` только
- **Безопасный upgrade**: миграция проверяет наличие legacy-записей с удалёнными source и падает, требуя ручного решения
- **Enum в коде**: `CAPTURE_SOURCES = ("screenshot",)` в `model_enums.py`
- **Post-MVP**: другие источники (sms, notification) зарезервированы, но не реализованы

## Связанные термины

- [[OCR_Layout_Parser]] — парсинг содержимого скриншотов
- [[Capture_Category_Mapping]] — маппинг распознанных категорий
