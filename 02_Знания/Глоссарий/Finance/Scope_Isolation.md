---
id: "term-scope-isolation"
тип: "термин"
проект: "Finance"
термин: "Изоляция scope"
термин_en: "Scope Isolation"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/authz/, db/migrations/versions/20260518_0003_accounts_categories_immutable_scope_triggers.py"
ссылки:
  - "[[MOC_Finance]]"
---

Архитектурный паттерн разделения данных на personal (привязаны к пользователю) и shared (привязаны к household). Гарантирует, что пользователь видит только свои personal-ресурсы и household-ресурсы, где он — active member.

## Ключевые аспекты

- **Два уровня scope**: `personal` (`owner_user_id`) и `household` (`household_id`) — для Account и Category
- **Filter-before-aggregate**: ресурсы фильтруются по видимости actor'а ДО агрегации в отчётах и списках
- **Immutable scope**: триггеры БД запрещают изменение scope-колонок после INSERT
- **Authz predicates**: `canReadAccount`, `canReadCategory`, `canReadReport` проверяют scope + membership
- **Report modes**: `shared_family_report` — только shared; `combined_viewer_overview` — personal + shared

## Связанные термины

- [[Immutable_Scope]] — триггеры защиты scope на уровне БД
- [[Account]] — ownership_type определяет scope
- [[Category]] — category_scope определяет scope
- [[Report]] — filter-before-aggregate по scope
- [[Membership]] — определяет доступ к shared scope
