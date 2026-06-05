---
id: "term-capture-category-mapping"
тип: "термин"
проект: "Finance"
термин: "Маппинг OCR-категорий"
термин_en: "Capture Category Mapping"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/capture_drafts/category_mapping_service.py"
ссылки:
  - "[[MOC_Finance]]"
---

Связь внешней текстовой метки (из OCR-распознавания) с внутренней категорией расходов. Позволяет автоматически предлагать категорию при повторном распознавании скриншота с той же меткой.

## Ключевые аспекты

- **Идентификация метки**: `external_label_hash` — SHA-256 от нормализованной метки (casefold, trim, strip non-word chars)
- **Upsert**: создаёт или обновляет маппинг для пары (user, household, label_hash) → `category_id`
- **Lookup**: `lookup_suggested_category_id()` — ищет ранее сохранённый маппинг по хешу метки
- **Scope-валидация**: маппинг создаётся только для `active` категории типа `expense` с проверкой authz-read
- **Personal vs household**: при `household_id=None` — personal-категории; при наличии — household-категории с проверкой membership

## Связанные термины

- [[Category]] — целевая категория маппинга
- [[OCR_Layout_Parser]] — источник external_label
- [[Screenshot_Source]] — источник capture drafts
- [[Scope_Isolation]] — валидация scope при маппинге
