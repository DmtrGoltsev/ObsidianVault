---
id: "term-category"
тип: "термин"
проект: "Finance"
термин: "Категория"
термин_en: "Category"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/categories/"
ссылки:
  - "[[MOC_Finance]]"
---

Категория расходов или доходов — метка классификации транзакций с scope-изоляцией. Определяет, к какому контексту (личный или household) привязана классификация.

## Ключевые аспекты

- **Типы**: `income`, `expense` — enum `CategoryType`
- **Scope**: `personal` (привязан к `owner_user_id`) или `household` (привязан к `household_id`)
- **Immutable scope**: колонки `category_scope`, `owner_user_id`, `household_id` защищены триггером БД
- **Дополнительные поля**: `icon_key`, `color` — визуальная кастомизация
- **Authz**: видимость через `canReadCategory`, мутация через `canMutateCategory` с проверкой scope и membership

## Связанные термины

- [[Scope_Isolation]] — изоляция personal/shared
- [[Immutable_Scope]] — триггеры защиты scope
- [[Account]] — аналогичная модель scope
- [[Capture_Category_Mapping]] — маппинг OCR-категорий
- [[Report]] — breakdown по категориям
