---
id: "term-db-schema"
тип: "термин"
проект: "Finance"
термин: "DB Schema"
термин_en: "DB Schema"
создано: "2026-06-05"
обновлено: "2026-06-05"
уровень_уверенности: "высокая"
теги: ["глоссарий", "finance", "database", "backend"]
источник: "db/migrations/versions/"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Transaction]]"
  - "[[Personal_Shared]]"
  - "[[Household]]"
  - "[[Capture_Draft]]"
---

# DB Schema (Схема базы данных)

## Определение

Схема БД проекта Finance — реляционная модель PostgreSQL 16, управляемая через **Alembic** (9 миграций, `2026-05-17` — `2026-05-31`). ORM-слой — SQLAlchemy 2.x (declarative, `mapped_column`).

Все модели определены в `apps/backend/src/app/db/models.py`. Enum-словари — в `model_enums.py`. Переиспользуемые типы колонок — в `model_types.py`.

---

## Таблицы

### users

Пользователи системы. Хранит учётные данные, статус аутентификации и soft-delete.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| email_normalized | Text | nullable; partial unique index (`record_status <> 'deleted'`) |
| password_hash | Text | |
| display_name | Text | nullable |
| auth_status | Text | `'active'`, `'deactivated'` |
| record_status | Text | `'active'`, `'deleted'` |
| session_version | BigInteger | default 1; инвалидация сессий |
| deactivated_at | Timestamptz | nullable |
| deleted_at | Timestamptz | nullable |

Constraints: `auth_status_valid`, `record_status_valid`.

### households

Домохозяйства (семейные бюджеты).

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| name | Text | |
| created_by_user_id | UUID | FK → users.id |
| status | Text | `'active'`, `'archived'` |
| record_status | Text | `'active'`, `'deleted'` |
| membership_version | BigInteger | default 1; optimistic lock для состава |
| archived_at | Timestamptz | nullable |
| deleted_at | Timestamptz | nullable |

### memberships

Членство пользователей в домохозяйствах.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| household_id | UUID | FK → households.id |
| user_id | UUID | FK → users.id |
| membership_status | Text | `'invited'`, `'active'`, `'left'`, `'revoked'` |
| invited_by_user_id | UUID | nullable; FK → users.id |
| invited_at / joined_at / ended_at | Timestamptz | nullable |

Constraints: partial unique index (`membership_status = 'active'`) → один active membership на (household, user).

### invites

Приглашения в домохозяйства.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| household_id | UUID | FK → households.id |
| invited_user_id | UUID | nullable; FK → users.id |
| invited_email_hash | Text | nullable |
| token_hash | Text | unique |
| invite_status | Text | `'pending'`, `'accepted'`, `'declined'`, `'revoked'`, `'expired'` |
| created_by_user_id / accepted_by_user_id | UUID | FK → users.id |
| expires_at / accepted_at / declined_at / revoked_at | Timestamptz | |

### accounts

Финансовые счета. Scope: **personal** (владелец — user) или **shared** (владелец — household). Scope immutable через DB-триггер.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| name | Text | |
| account_type | Text | `'cash'`, `'bank'`, `'deposit'`, `'brokerage'`, `'card'`, `'metal'`, `'other'` |
| ownership_type | Text | `'personal'`, `'shared'` |
| owner_user_id | UUID | nullable; FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| currency | String(3) | ISO 4217, uppercase enforced |
| initial_balance_amount | Numeric(20,4) | default 0 |
| current_balance_amount | Numeric(20,4) | nullable |
| record_status | Text | `'active'`, `'archived'`, `'deleted'` |
| created_by_user_id | UUID | FK → users.id |
| archived_at / deleted_at | Timestamptz | nullable |

Constraints: `exactly_one_scope` (personal → user, shared → household), `currency_iso_shape`.

### categories

Категории доходов/расходов. Scope: personal или household. Scope immutable через DB-триггер.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| name | Text | |
| category_type | Text | `'income'`, `'expense'` |
| category_scope | Text | `'personal'`, `'household'` |
| owner_user_id | UUID | nullable; FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| icon_key | Text | nullable |
| color | Text | nullable |
| record_status | Text | `'active'`, `'archived'`, `'deleted'` |
| created_by_user_id | UUID | FK → users.id |
| archived_at / deleted_at | Timestamptz | nullable |

Constraints: `exactly_one_scope`.

### transactions

Транзакции (income, expense, transfer, brokerage, asset_buy/sell, interest, dividend, adjustment).

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| transaction_type | Text | см. Enum типы |
| account_id | UUID | FK → accounts.id |
| counterparty_account_id | UUID | nullable; FK → accounts.id (для transfer) |
| category_id | UUID | nullable; FK → categories.id |
| amount | Numeric(20,4) | > 0 (CHECK) |
| currency | String(3) | ISO 4217 |
| occurred_at | Timestamptz | |
| description | Text | nullable |
| source_type | Text | `'manual'` (только) |
| transfer_scope | Text | nullable; `'personal_same_owner'`, `'household_same_household'` |
| transfer_status | Text | nullable; `'posted'`, `'voided'` |
| record_status | Text | `'active'`, `'deleted'` |
| created_by_user_id | UUID | FK → users.id |
| last_edited_by_user_id | UUID | FK → users.id |
| deleted_at | Timestamptz | nullable |

Constraints: `source_type_manual_only`, `positive_amount`, `currency_iso_shape`, `transfer_shape`, `income_expense_category_required`.

### capture_drafts

Черновики автозахвата транзакций (OCR скриншотов).

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| owner_user_id | UUID | FK → users.id |
| status | Text | `'pending'`, `'confirmed'`, `'discarded'` |
| capture_source | Text | `'screenshot'` (только) |
| idempotency_key | Text | unique per owner |
| captured_at | Timestamptz | |
| occurred_at | Timestamptz | nullable |
| amount | Numeric(20,4) | > 0 |
| currency | String(3) | ISO 4217 |
| description | Text | |
| merchant_name | Text | nullable |
| account_id | UUID | nullable; FK → accounts.id |
| category_id | UUID | nullable; FK → categories.id |
| transaction_id | UUID | nullable; FK → transactions.id (заполнен при confirmed) |
| confidence | Numeric(20,4) | nullable; 0–1 |
| source_app_package / source_app_label | Text | nullable |
| evidence_hash | Text | nullable |

Constraints: `positive_amount`, `currency_iso_shape`, `confidence_range`, `confirmed_transaction_shape`.

### capture_category_mappings

Хеш-маппинг внешних меток на категории (для автокатегоризации capture drafts).

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| owner_user_id | UUID | FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| category_id | UUID | FK → categories.id |
| external_label_hash | Text | SHA-256 (len = 64) |

Constraints: `external_label_hash_sha256`, partial unique indexes (personal и household scope).

### sessions

DB-backed аутентификационные сессии.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| session_token_hash | Text | nullable; unique |
| refresh_token_hash | Text | nullable; unique |
| transport | Text | `'cookie'`, `'android_bearer'` |
| session_version | BigInteger | |
| csrf_token_hash | Text | nullable |
| status | Text | `'active'`, `'revoked'`, `'expired'` |
| last_seen_at | Timestamptz | nullable |
| expires_at | Timestamptz | |
| revoked_at | Timestamptz | nullable |
| revoked_reason | Text | nullable |

Constraints: `at_least_one_token_hash`.

### password_reset_tokens

Токены сброса пароля.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | nullable; FK → users.id |
| email_hash | Text | |
| token_hash | Text | unique |
| status | Text | `'pending'`, `'used'`, `'expired'`, `'revoked'` |
| created_at / expires_at / used_at / revoked_at | Timestamptz | |
| request_ip_hash | Text | nullable |

### export_jobs

Фоновые задачи экспорта данных.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| requested_by_user_id | UUID | FK → users.id |
| export_type | Text | |
| scope_type | Text | `'personal'`, `'household'`, `'combined'` |
| owner_user_id | UUID | nullable; FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| membership_version_at_request | BigInteger | nullable |
| status | Text | `'queued'`, `'running'`, `'ready'`, `'failed'`, `'expired'`, `'revoked'` |
| storage_key / file_hash | Text | nullable |
| ready_at / expires_at / revoked_at | Timestamptz | nullable |

Constraints: `export_scope_shape`.

### deletion_requests

Запросы на удаление аккаунта (self-service).

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| requested_by_user_id | UUID | FK → users.id |
| target_user_id | UUID | FK → users.id |
| request_status | Text | `'pending'`, `'approved'`, `'completed'`, `'cancelled'`, `'rejected'` |
| requested_at | Timestamptz | |
| approved_at / completed_at / cancelled_at / fresh_auth_at | Timestamptz | nullable |
| reason_code | Text | nullable |

Constraints: `self_only_request` (requested_by = target).

### audit_events

Аудит-лог действий в системе.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| occurred_at | Timestamptz | |
| actor_user_id | UUID | nullable; FK → users.id |
| system_actor | Text | nullable |
| action | Text | |
| target_type / target_id | Text / UUID | nullable |
| scope_type | Text | nullable; `'personal'`, `'household'`, `'system'` |
| owner_user_id | UUID | nullable; FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| result | Text | `'allow'`, `'deny'`, `'state-deny'`, `'error'` |
| request_id | Text | nullable |
| reason_code | Text | nullable |
| metadata_safe | JSONB | default `'{}'` |

Constraints: `audit_scope_shape`.

### outbox_events

Transactional outbox для доставки событий.

| Колонка | Тип | Примечание |
|---|---|---|
| id | UUID | PK |
| event_type / aggregate_type | Text | |
| aggregate_id | UUID | |
| scope_type | Text | nullable |
| owner_user_id | UUID | nullable; FK → users.id |
| household_id | UUID | nullable; FK → households.id |
| membership_version | BigInteger | nullable |
| payload_safe | JSONB | default `'{}'` |
| status | Text | `'pending'`, `'processing'`, `'processed'`, `'failed'`, `'dead'` |
| created_at / available_at | Timestamptz | |
| processed_at | Timestamptz | nullable |
| attempt_count | Integer | default 0 |

---

## Enum типы

Все enum хранятся как `Text` + `CHECK constraint`. Определения — `apps/backend/src/app/db/model_enums.py`.

| Имя (переменная) | Значения |
|---|---|
| ACCOUNT_TYPES | `cash`, `bank`, `deposit`, `brokerage`, `card`, `metal`, `other` |
| AUTH_STATUSES | `active`, `deactivated` |
| ACTIVE_DELETED_STATUSES | `active`, `deleted` |
| RECORD_STATUSES | `active`, `archived`, `deleted` |
| HOUSEHOLD_STATUSES | `active`, `archived` |
| MEMBERSHIP_STATUSES | `invited`, `active`, `left`, `revoked` |
| INVITE_STATUSES | `pending`, `accepted`, `declined`, `revoked`, `expired` |
| OWNERSHIP_TYPES | `personal`, `shared` |
| CATEGORY_SCOPES | `personal`, `household` |
| CATEGORY_TYPES | `income`, `expense` |
| TRANSACTION_TYPES | `income`, `expense`, `transfer`, `brokerage`, `asset_buy`, `asset_sell`, `interest`, `dividend`, `adjustment` |
| SOURCE_TYPES | `manual` |
| TRANSFER_SCOPES | `personal_same_owner`, `household_same_household` |
| TRANSFER_STATUSES | `posted`, `voided` |
| CAPTURE_DRAFT_STATUSES | `pending`, `confirmed`, `discarded` |
| CAPTURE_SOURCES | `screenshot` |
| SESSION_TRANSPORTS | `cookie`, `android_bearer` |
| SESSION_STATUSES | `active`, `revoked`, `expired` |
| RESET_TOKEN_STATUSES | `pending`, `used`, `expired`, `revoked` |
| EXPORT_SCOPE_TYPES | `personal`, `household`, `combined` |
| EXPORT_STATUSES | `queued`, `running`, `ready`, `failed`, `expired`, `revoked` |
| DELETION_REQUEST_STATUSES | `pending`, `approved`, `completed`, `cancelled`, `rejected` |
| AUDIT_SCOPE_TYPES | `personal`, `household`, `system` |
| AUDIT_RESULTS | `allow`, `deny`, `state-deny`, `error` |
| OUTBOX_STATUSES | `pending`, `processing`, `processed`, `failed`, `dead` |

---

## Custom types

Определены в `apps/backend/src/app/db/model_types.py`:

- **MONEY_NUMERIC** — `Numeric(20, 4)`, используется для всех денежных сумм (amount, balance).
- **uuid_pk()** — UUID PK с auto-default `uuid.uuid4`.
- **uuid_fk(target)** — UUID FK на указанную таблицу.
- **created_timestamp()** — `Timestamptz`, `server_default = now()`.
- **updated_timestamp()** — `Timestamptz`, `server_default = now()`, `onupdate = now()`.

---

## Triggers

### Immutable scope triggers (миграция 0003)

Файл: `db/migrations/versions/20260518_0003_accounts_categories_immutable_scope_triggers.py`

Два триггера **BEFORE UPDATE** запрещают изменение scope-колонок после создания записи:

**accounts** — триггер `trg_accounts_immutable_scope`:
- Защищаемые колонки: `ownership_type`, `owner_user_id`, `household_id`
- Функция: `prevent_accounts_scope_update()` — при изменении любой из трёх колонок выбрасывает `integrity_constraint_violation`

**categories** — триггер `trg_categories_immutable_scope`:
- Защищаемые колонки: `category_scope`, `owner_user_id`, `household_id`
- Функция: `prevent_categories_scope_update()` — аналогично

---

## Safety constraints

### Transfer safety (миграция 0005)

Файл: `db/migrations/versions/20260518_0005_transaction_transfer_safety.py`

Триггер `trg_transactions_transfer_safety` (функция `finance_validate_transaction_transfer_safety`) — **BEFORE INSERT OR UPDATE** на transactions:

- Проверяет, что для `transaction_type = 'transfer'`:
  - Оба счёта (source и counterparty) существуют
  - Валюта транзакции совпадает с валютой обоих счетов
  - При `transfer_scope = 'personal_same_owner'` — оба счёта personal с одним owner_user_id
  - При `transfer_scope = 'household_same_household'` — оба счёта shared с одним household_id

### API vocabulary constraints (миграция 0006)

Файл: `db/migrations/versions/20260519_0006_align_api_vocabulary_constraints.py`

Расширяет CHECK constraints для соответствия API-словарю:
- `accounts.account_type` — расширено с 4 до 7 значений (`+card`, `+metal`, `+other`)
- `transactions.transaction_type` — расширено с 4 до 9 значений (`+asset_buy`, `+asset_sell`, `+interest`, `+dividend`, `+adjustment`)

### Capture source restriction (миграция 0008)

Файл: `db/migrations/versions/20260528_0008_restrict_capture_drafts_screenshot_source.py`

Сужает `capture_source` с `('sms', 'notification', 'screenshot')` до `('screenshot')`. Перед сужением проверяет отсутствие legacy-записей с удалёнными источниками.

---

## Хронология миграций

| # | Дата | Назначение | Файл |
|---|---|---|---|
| 0001 | 2026-05-17 | Базовый slice: users, households, memberships, accounts, categories | `20260517_0001_accounts_categories_slice.py` |
| 0002 | 2026-05-18 | Auth-сессии (sessions) | `20260518_0002_auth_sessions.py` |
| 0003 | 2026-05-18 | Immutable scope triggers для accounts и categories | `20260518_0003_accounts_categories_immutable_scope_triggers.py` |
| 0004 | 2026-05-18 | Транзакции (transactions) | `20260518_0004_transactions.py` |
| 0005 | 2026-05-18 | Transfer safety trigger (scope + currency checks) | `20260518_0005_transaction_transfer_safety.py` |
| 0006 | 2026-05-19 | Расширение CHECK constraints (account_type, transaction_type) | `20260519_0006_align_api_vocabulary_constraints.py` |
| 0007 | 2026-05-23 | Capture drafts (автозахват скриншотов) | `20260523_0007_capture_drafts.py` |
| 0008 | 2026-05-28 | Сужение capture_source до screenshot | `20260528_0008_restrict_capture_drafts_screenshot_source.py` |
| 0009 | 2026-05-31 | Категорные маппинги (capture_category_mappings) | `20260531_0009_capture_category_mappings.py` |

---

## Связи между таблицами

```
users
 ├──< households (created_by_user_id)
 │     ├──< memberships (household_id → user_id)
 │     ├──< invites (household_id)
 │     ├──< accounts (household_id, ownership_type = 'shared')
 │     ├──< categories (household_id, category_scope = 'household')
 │     ├──< capture_category_mappings (household_id)
 │     ├──< export_jobs (household_id)
 │     └──< audit_events / outbox_events (household_id)
 │
 ├──< accounts (owner_user_id, ownership_type = 'personal')
 │     └──< transactions (account_id)
 │           └──< capture_drafts (transaction_id)
 │
 ├──< categories (owner_user_id, category_scope = 'personal')
 │     ├──< transactions (category_id)
 │     └──< capture_category_mappings (category_id)
 │
 ├──< capture_drafts (owner_user_id)
 │     └── capture_category_mappings (owner_user_id + external_label_hash → category_id)
 │
 ├──< sessions (user_id)
 ├──< password_reset_tokens (user_id)
 ├──< export_jobs (requested_by_user_id)
 ├──< deletion_requests (target_user_id, self_only)
 ├──< audit_events (actor_user_id)
 └──< outbox_events (owner_user_id)

transactions
 ├──→ accounts (account_id)          — счёт-источник
 ├──→ accounts (counterparty_account_id) — счёт-контрагент (для transfer)
 └──→ categories (category_id)       — категория (обязательна для income/expense)
```

---

## Связанные термины

- [[Transaction]] — транзакции и их типы
- [[Transfer]] — переводы между счетами
- [[Household]] — домохозяйство
- [[Personal_Shared]] — personal/shared scope
- [[Capture_Draft]] — автозахват скриншотов
- [[Account]] — финансовые счета
- [[Category]] — категории доходов/расходов

---

## Источник

- Модели: `apps/backend/src/app/db/models.py`
- Enum-словари: `apps/backend/src/app/db/model_enums.py`
- Custom types: `apps/backend/src/app/db/model_types.py`
- Миграции: `db/migrations/versions/`
