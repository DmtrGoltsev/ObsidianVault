---
id: "adr-finance-0005"
тип: "решение"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["ADR", "finance", "архитектура", "безопасность", "scope", "БД"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[ADR_0001_Stack_Repo_Layout]]"
  - "[[ADR_0002_Auth_Model]]"
---

# ADR-0005: Scope isolation на уровне БД

## Статус

Утверждено. Реализовано в migration `0003` и `apps/backend/src/app/authz/`.

## Контекст

Finance разделяет данные на два scope:

- **Personal** — личные финансы пользователя. Доступен только owner (`owner_user_id`).
- **Shared / Household** — совместные финансы домохозяйства. Доступны только active members (`MembershipStatus.ACTIVE`).

Нарушение scope isolation — критический security incident. Приложение использует server-side authz predicates (`authz/predicates.py`) для enforcement, но application-level enforcement уязвимо к багам (забытая проверка, race condition, migration oversight). БД — последний рубеж защиты.

Отчёты (`ReportMode.SHARED_FAMILY_REPORT`, `COMBINED_VIEWER_OVERVIEW`) должны фильтровать данные до агрегации — aggregate по rows, которые пользователь не должен видеть, leaks информацию через totals.

## Решение

### Immutable scope triggers на уровне PostgreSQL

Migration `20260518_0003` создаёт два BEFORE UPDATE триггера:

**`trg_accounts_immutable_scope`**
- Срабатывает при UPDATE `ownership_type`, `owner_user_id`, `household_id` на таблице `accounts`.
- Если любое из трёх полей изменилось — `RAISE EXCEPTION 'account ownership scope is immutable'` с `ERRCODE = 'integrity_constraint_violation'`.
- Запрещает перенос аккаунта между personal и shared scope или между пользователями.

**`trg_categories_immutable_scope`**
- Срабатывает при UPDATE `category_scope`, `owner_user_id`, `household_id` на таблице `categories`.
- Аналогичная логика: `RAISE EXCEPTION 'category scope is immutable'`.
- Запрещает перенос категории между scope.

Это не ACL — это immutability constraint. Scope нельзя изменить после создания, даже если application code ошибочно попытается.

### Server-side authz predicates

`authz/predicates.py` реализует deny-by-default авторизацию через чистые функции:

- **`canReadAccount`** — personal: `owner_user_id == actor.user_id`. Shared: actor имеет active membership в household.
- **`canMutateAccount`** — read check + archived check + ownership immutability check.
- **`canUseCategory`** — account scope == category scope (cross-scope запрещён).
- **`canUseTransferScope`** — только `personal_same_owner` или `household_same_household`.
- **`resolveReportVisibleScope`** — `SHARED_FAMILY_REPORT`: только household scope. `COMBINED_VIEWER_OVERVIEW`: household + personal actor scope.

Все predicates возвращают `AuthzDecision` с `Decision.ALLOW/DENY`, `DenialReason`, `resolved_scope`, `visible_scope`, и `AuditClass`.

### Filter-before-aggregate для отчётов

`resolveReportVisibleScope` вычисляет `VisibleReportScope` — набор scope refs, которые viewer видит. Этот scope применяется как SQL WHERE filter **до** любой агрегации (SUM, COUNT, GROUP BY). Нарушение этого принципа leaks totals по невидимым rows.

## Альтернативы

1. **Только application-level enforcement** — отклонено. Один баг в application code может нарушить scope isolation. DB triggers — safety net, который не обойти из application.
2. **PostgreSQL Row-Level Security (RLS)** — отклонено для MVP. RLS требует `SECURITY DEFINER` функций, session variables, и сложной отладки. Текущий подход (triggers + application predicates) проще для аудита и тестирования. RLS может быть добавлен как defense-in-depth в P2.

## Последствия

### Положительные

- **Impossible to change scope** — даже если application code содержит bug, DB trigger отвергнет UPDATE с изменением scope.
- **Trigger errors are testable** — integration tests подтверждают, что scope change вызывает `integrity_constraint_violation`.
- **Authz predicates — чистые функции** — легко unit-test со всеми комбинациями Actor/Resource/Scope.
- **Filter-before-aggregate** — отчёты не leaks totals по невидимым данным.

### Издержки

- **Performance overhead** — триггеры выполняются на каждый UPDATE затронутых колонок. Для текущего масштаба (closed MVP) negligible, но требует monitoring при росте.
- **Migration complexity** — downgrade должен корректно удалить триггеры и функции. Migration `0003` обеспечивает это.
- **Невозможно исправить ошибочный scope** — если аккаунт/категория создана в неправильном scope, единственный путь — создать новую запись в правильном scope и archive старую.
- **Server-side only authz** — клиент не может обойти predicates. Все данные проходят через server-side checks.

## Ссылки

- `db/migrations/versions/20260518_0003_accounts_categories_immutable_scope_triggers.py` — триггеры и функции
- `apps/backend/src/app/authz/predicates.py` — deny-by-default predicates, `AuthzDecision`, scope resolution
- `apps/backend/src/app/authz/__init__.py` — public API модуля authz
- `db/migrations/versions/20260517_0001_accounts_categories_slice.py` — начальная схема с scope columns
