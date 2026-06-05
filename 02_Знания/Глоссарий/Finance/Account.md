---
id: "term-account"
тип: "термин"
проект: "Finance"
термин: "Счёт"
термин_en: "Account"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/accounts/"
ссылки:
  - "[[MOC_Finance]]"
---

Финансовый счёт пользователя — хранилище денежных средств с привязкой к валюте, типу и scope владения. Связь с household определяется через `ownership_type`.

## Ключевые аспекты

- **Типы**: `cash`, `bank`, `card`, `deposit`, `brokerage`, `metal`, `other` — enum `AccountType`
- **Scope владения**: `personal` (привязан к `owner_user_id`) или `shared` (привязан к `household_id`)
- **Immutable scope**: колонки `ownership_type`, `owner_user_id`, `household_id` защищены триггером БД от изменения после создания
- **Статусы жизненного цикла**: `active` → `archived` → `deleted` (enum `RecordStatus`)
- **Authz**: чтение и мутация через `canReadAccount` / `canMutateAccount` с учётом membership actor'а

## Связанные термины

- [[Scope_Isolation]] — изоляция personal/shared
- [[Immutable_Scope]] — триггеры защиты scope
- [[Money]] — формат денежных сумм
- [[Category]] — аналогичная модель scope
- [[Report]] — агрегация по счетам
