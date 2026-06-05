---
id: "term-immutable-scope"
тип: "термин"
проект: "Finance"
термин: "Immutable scope"
термин_en: "Immutable Scope Triggers"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "db/migrations/versions/20260518_0003_accounts_categories_immutable_scope_triggers.py"
ссылки:
  - "[[MOC_Finance]]"
---

PostgreSQL-триггеры `BEFORE UPDATE`, запрещающие изменение scope-колонок (ownership_type, owner_user_id, household_id) для accounts и categories после создания записи. Гарантируют целостность данных на уровне БД.

## Ключевые аспекты

- **Таблица `accounts`**: триггер `trg_accounts_immutable_scope` защищает `ownership_type`, `owner_user_id`, `household_id`
- **Таблица `categories`**: триггер `trg_categories_immutable_scope` защищает `category_scope`, `owner_user_id`, `household_id`
- **Механизм**: функция сравнивает `OLD.*` и `NEW.*` через `IS DISTINCT FROM`, выбрасывает `integrity_constraint_violation`
- **Миграция**: `20260518_0003` — downgrade удаляет триггеры и функции, данные не затрагиваются

## Связанные термины

- [[Scope_Isolation]] — паттерн, который immutable scope защищает
- [[Account]] — защищаемая сущность
- [[Category]] — защищаемая сущность
