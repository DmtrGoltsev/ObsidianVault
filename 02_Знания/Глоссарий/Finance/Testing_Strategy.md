---
id: "term-testing-strategy"
тип: "термин"
проект: "Finance"
термин: "Testing Strategy"
термин_en: "Testing Strategy"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance", "testing", "qa"]
источник: "apps/backend/tests/"
ссылки:
  - "[[MOC_Finance]]"
---

# Testing Strategy (Стратегия тестирования)

## Определение

Многоуровневая стратегия тестирования Finance MVP: покрытие backend (pytest), PWA (Vitest), Android (JUnit 4 + AndroidX Test), контрактное тестирование (Schemathesis/OpenAPI), privacy/security-тесты и production QA evidence. Цель — обеспечить корректность бизнес-логики, изоляцию данных пользователей и воспроизводимые доказательства качества перед релизом.

## Backend (pytest)

Корневая директория: `apps/backend/tests/`

Фреймворк: **pytest** + `fastapi.testclient.TestClient`. Точка входа — `conftest.py`, создаёт `TestClient` через `create_app()`.

Результат свежего прогона: **149 passed, 3 warnings** (~15 с).

### Структура тестов по доменам

| Папка | Назначение | Ключевые файлы |
|---|---|---|
| `auth/` | Аутентификация, сессии, rate limits, security primitives | `test_session_flow.py`, `test_registration_flow.py`, `test_rate_limits.py`, `test_security_primitives.py`, `test_db_session_persistence.py`, `test_neutral_responses.py`, `test_provision_initial_owner.py`, `test_router_contract.py` |
| `api/` | Route contract, privacy guards, error envelope | `test_openapi_mvp_manual_first_contract.py`, `test_accounts_categories_route_contract.py`, `test_w3_ttr_contract_guards.py`, `test_accounts_categories_privacy.py`, `test_accounts_categories_db_runtime.py`, `test_auth_context.py`, `test_error_envelope_contract.py` |
| `db/` | Миграции, репозитории, DB constraints, runtime policy | `test_accounts_categories_migration_slice.py`, `test_transactions_migration_slice.py`, `test_transaction_transfer_safety_migration.py`, `test_sqlalchemy_accounts_categories_repositories.py`, `test_api_vocabulary_db_constraints.py`, `test_db_runtime_policy.py`, `test_model_metadata.py`, `test_session.py` |
| `accounts/` | Accounts router | `test_accounts_router.py` |
| `categories/` | Categories router | `test_categories_router.py` |
| `transactions/` | Transactions DB runtime | `test_transactions_db_runtime.py` |
| `transfers/` | Transfer runtime safety | `test_transfer_runtime_safety.py` |
| `capture_drafts/` | OCR parser, screenshot endpoint, draft lifecycle | `test_screenshot_ocr_parser.py`, `test_screenshot_ocr_endpoint.py`, `test_capture_drafts_runtime.py` |
| `reports/` | Reports runtime safety | `test_reports_runtime_safety.py` |
| `domain/` | Domain types validation | `test_domain_types.py` |
| `authz/` | Authorization predicates | `test_predicates.py` |
| (root) | Health, dev surface | `test_health.py`, `test_dev_surface.py` |

## PWA (Vitest)

Директория проекта: `apps/web-pwa/`

Фреймворк: **Vitest** + `@testing-library/react` + `@testing-library/jest-dom` + `@testing-library/user-event` + `jsdom`.

Команды:
- `vitest run` — однократный прогон
- `vitest` — watch-режим

Результат: **2 test files, 7 tests passed**; production build успешен.

Типы тестов: unit и component-тесты React-компонентов в jsdom-окружении.

## Android (JUnit 4 + AndroidX Test)

Конфигурация: `apps/android/app/build.gradle.kts`

Фреймворки:
- **JUnit 4** (`junit:junit:4.13.2`) — unit-тесты (`testImplementation`)
- **AndroidX Test** (`androidx.test.ext:junit:1.2.1`) — instrumented-тесты (`androidTestImplementation`)
- **Compose UI Test** (`androidx.compose.ui:ui-test-junit4`) — тестирование Jetpack Compose UI
- `testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"`

Команды: `:app:testDebugUnitTest`, `:app:connectedDebugAndroidTest`, `:app:assembleDebug`.

## Contract testing

Инструмент: **Schemathesis** для валидации OpenAPI-контракта (`api/openapi/openapi.yaml`).

Контрактные guard-тесты:
- `test_openapi_mvp_manual_first_contract.py` — проверяет точное соответствие mounted MVP `paths`
- `test_accounts_categories_route_contract.py` — runtime route inventory
- `test_w3_ttr_contract_guards.py` — W3 TTR (transactions/transfers/reports) contract guards
- `test_error_envelope_contract.py` — canonical error envelope

Документация: `docs/testing/mvp-api-contract-qa-matrix.md`, `docs/testing/w3-ttr-privacy-safety-matrix.md`.

## QA Evidence

### MVP_EVIDENCE/

Production QA evidence для MVP release gate:
- `test-matrix.md` — полная тестовая матрица MVP (19 flow-покрытий)
- `MVP_RELEASE_REPORT.md` — итоговый отчёт релиза
- `reports/` — детальные QA-репорты по платформам и flows
- `screenshots/` — скриншоты PWA desktop, iOS-like PWA, Android native
- `test-runs/` — логи прогонов (включая PNG validation)
- `release-checklist.md`, `reports-index.md`

Статус MVP gate: **GO** (функциональный MVP подтверждён).

### qa-artifacts/

Результаты QA-прогонов в production-окружении:
- `android-ocr-qa-*`, `iphone-prod-*`, `iphone-prod-ocr-draft-ui-*` — мобильные QA-артефакты
- `ocr-layout-prod-*` — OCR layout-тестирование
- `server-side-ocr-prod-*` — server-side OCR production evidence (auth, final pass, transient diagnostics)

### qa/

QA fixtures и чеклисты:
- `fixtures/owner-member-other-invited-former-v1/` — canonical fixture manifest для multi-role testing
- `device-qa-android-iphone-checklist-2026-05-18.md` — девайс-чеклист

## Типы тестов

| Тип | Область | Инструмент | Где |
|---|---|---|---|
| **Unit** | Отдельные функции, predicates, domain types | pytest / Vitest / JUnit 4 | `tests/*/`, `*.test.*`, `testDebugUnitTest` |
| **Integration** | DB runtime, репозитории, миграции | pytest + SQLAlchemy | `tests/db/`, `tests/transactions/`, `tests/transfers/`, `tests/reports/` |
| **Contract** | OpenAPI surface, route inventory, error envelope | pytest + Schemathesis | `tests/api/`, `docs/testing/` |
| **Privacy** | Visibility guards, neutral responses, cross-household denial | pytest | `tests/api/test_*_privacy.py`, `tests/auth/test_neutral_responses.py` |
| **Security** | Rate limits, session persistence, security primitives | pytest | `tests/auth/test_rate_limits.py`, `tests/auth/test_security_primitives.py`, `tests/auth/test_db_session_persistence.py` |
| **E2E (Playwright)** | PWA recovery lifecycle, CRUD flows | Playwright | `MVP_EVIDENCE/reports/` |
| **Instrumented** | Android Compose UI, native CRUD | AndroidX Test + Compose UI Test | `androidTest/`, `connectedDebugAndroidTest` |

## Test fixtures

Пакет: `packages/test-fixtures/finance_fixtures/`

Назначение: runner-neutral fixture tooling для QA evidence work. Не зависит от production-кода и не подключается к БД.

Модули:
- `loader.py` — загрузка и валидация manifest-файлов (shape checks, deterministic synthetic IDs)
- `sanitization.py` — санитизация fixture-данных, redaction scan

Поддерживаемые контракты:
- `sanitizedLabelToIdMap`
- `fixtureGraphSummary`
- `evidenceManifest`
- `redactionScanSummary`

W3 TTR Contract Fixtures:
- `canonical-uuid-graph.json` — canonical UUID-граф
- `goldens/visibility-expected.json`, `goldens/report-expected.json`, `goldens/transfer-denials-expected.json` — ожидаемые результаты для contract-тестов

Fixture manifest: `qa/fixtures/owner-member-other-invited-former-v1/` — определяет 5 canonical actors (Owner, Member, Other, Invited, Former) для multi-role privacy-тестирования.

Запуск: `python -m unittest discover -s packages/test-fixtures/tests`

---

Связанные заметки: [[MOC_Finance]]
