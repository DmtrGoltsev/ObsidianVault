---
id: "project-finance"
тип: "проект"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-07"
уверенность: "средняя"
теги: ["проект", "finance", "финансы", "учёт", "MVP"]
источники:
  - "docs/product-mvp.md"
  - "docs/current-status.md"
  - "docs/architecture/decision-records/adr-0001-stack-repo-layout.md"
  - "README.md"
ссылки:
  - "[[MOC_Finance]]"
  - "[[MOC_Все_Проекты]]"
---

# Finance — ручной учёт личных и семейных финансов

> ⚠️ **СКЕЛЕТ.** Эта заметка — каркас проекта на основе кворум-исследования (3 агента). Слой знаний (глоссарий, источники) заполнен. Delivery-слои (задачи, агенты, ADR, доказательства, пакеты контекста бэкенда/Android/PWA) отсутствуют. Не полный source of truth. Требуется достройка.

## Цель

Ручной учёт личных и семейных финансов. Personal/shared разделение, user-initiated OCR черновики. Закрытый MVP.

**Production GO:** 2026-05-19

## Стек

| Слой | Технологии |
|------|-----------|
| Backend | Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x (async), Alembic, Pydantic |
| БД | PostgreSQL 16 (decimal numeric) |
| PWA | TypeScript, React 19, Vite 7, TanStack Query, Capacitor iOS, Vitest, Playwright |
| Android | Kotlin, Jetpack Compose, Retrofit/OkHttp, Room (scoped cache), JUnit, on-device OCR |
| API | OpenAPI 3.1 contract-first (`api/openapi/openapi.yaml`) |
| Auth | PWA: HttpOnly Secure SameSite cookie + CSRF; Android: Bearer + rotating refresh (Keystore) |
| OCR | Android on-device; PWA/iOS: Tesseract backend (временная загрузка) |
| Деплой | Self-hosted Linux (systemd/nginx), `/finance/` + `/finance-api/`, без Docker |
| QA | pytest, Schemathesis, Vitest, Playwright, JUnit |
| Security | Argon2id/bcrypt, gitleaks, pip-audit, npm audit |

## Архитектура

Contract-first монолит-монорепо. Backend FastAPI — единственный сервер. Клиенты: PWA (React/Vite + Capacitor iOS), Android (Kotlin/Compose). OpenAPI 3.1 — source of truth → генерация клиентов. REST API `/api/v1`.

## Модули

| Модуль | Путь | Назначение |
|--------|------|-----------|
| Backend | `apps/backend/` | FastAPI сервер |
| PWA | `apps/web-pwa/` | React/Vite PWA + Capacitor iOS |
| Android | `apps/android/` | Kotlin/Compose приложение |
| API Spec | `api/openapi/` | OpenAPI 3.1 контракт |
| Миграции | `db/migrations/` | Alembic миграции |
| Фикстуры | `db/seeds/` | Тестовые фикстуры |
| QA | `qa/` | Чек-листы |
| Security | `security/` | Сканы, evidence |
| Ops | `ops/` | Backup/restore |
| Docs | `docs/` | Архитектура, compliance, planning |
| Клиенты | `packages/` | Генерация клиентов |
| Evidence | `MVP_EVIDENCE/` | Production QA evidence |

## Текущая стадия

**Production MVP functional GO (2026-05-19)** — закрытый MVP в production.

### Обновление 2026-06-06

- **Русификация:** 44 строки UI переведены на русский
- **QA-аудит:** 25 багов найдено (3 P0, 8 P1, 14 P2), 12 исправлено
- **API-аудит:** 26 endpoint'ов проверено, 0 критических расхождений
- **Тест-кейсы:** 91 кейс создан (`docs/testing/mvp-android-qa-test-cases.md`)
- **APK:** `artifacts/apk/finance-mvp-0.1.0-debug.apk` (51.72 MB), production URL `http://45.10.110.42/finance-api`

### Поставка Assets UI + account edit + backend PATCH (2026-06-06)

- **Backend/API:** `PATCH account` принимает `name`, `currentBalance`, `currency`, `version`; `initialBalance` не меняется.
- **Конфликты API:** `CONFLICTING_UPDATE`, `ACCOUNT_CURRENCY_IMMUTABLE_AFTER_TRANSACTIONS`.
- **Бизнес-решение:** нельзя менять валюту счёта, если у счёта уже есть транзакции.
- **Бизнес-решение:** удаление виртуальной категории активов архивирует все активные счета группы.
- **Android Assets UI:** tap по категории раскрывает/сворачивает группу; редактирование имени группы без refresh icon; long press >1s показывает подтверждение и архивирует счета группы.
- **Android account edit:** диалог редактирования счёта поддерживает `name`, `balance`, `currency`; для XAU используется label `граммы` и иконка gold bar.
- **QA:** backend targeted tests — `22 passed, 1 warning`; Android `assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` — `BUILD SUCCESSFUL in 57s`; `git diff --check` — exit 0, только CRLF warnings.
- **Runtime smoke:** только эмулятор `Codex`; `Android1` не трогали; APK установлен и `MainActivity` открыт. Account edit flow — `NOT_RUN`, потому что на `Codex` нет активных счетов/данных.

### Поставка Аналитика -> Планирование MVP (2026-06-06)

- **Возможности:** personal + shared scope, одна валюта плана, источники дохода `amount`/`source`/`dayOfMonth`, локальные Android reminders по каждому доходу.
- **Планирование:** подтверждение обновляет только план и не создаёт транзакции; allocations поддерживают категории расходов, счета, активы и инвестиции; режимы `amount` или `percent`.
- **Контроль:** underallocated banner, overallocated warning, history/copy; создание категории или счёта наследует scope текущего планирования.
- **Backend/API:** добавлен planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, миграция `20260606_0010`, OpenAPI planning endpoints.
- **Authz/валидации:** personal owner-only, household active-member, derived totals, copy attention rows, positive income validation; исправлен runtime `dev_seed` для planning.
- **Android:** planning DTO/methods в `ApiClient`, `PlanningUi` во вкладках Analytics, локальные уведомления через `AlarmManager`/`BroadcastReceiver`, `POST_NOTIFICATIONS`; без FCM/SMS/NotificationListener/exact alarm.
- **QA:** `python -m pytest` — `224 passed`, 4 warnings; targeted planning/openapi/db tests — `29 passed`; Android `assembleDebug` — `BUILD SUCCESSFUL`; OpenAPI parse ok, `PATH_COUNT=37`, все planning paths присутствуют.
- **Runtime smoke:** только `Codex`; `Android1` не targeted. Экран Planning открылся и показал следующий месяц, текущий план и totals.
- **Dev seed smoke:** login 201, planning history 200, personal plan 200, без internal server error.
- **Diff hygiene:** `git diff --check` pass, только LF/CRLF warnings.

### Planning asset target sync (WIP, 2026-06-07)

- **Кодовая ветка:** `codex/finance-planning-mvp-gpt5`; HEAD `0780944` (`feat(finance): add planning MVP`), поверх HEAD есть незакоммиченный WIP.
- **Asset target gap:** закрывается явный Planning `targetType=asset` на backend/OpenAPI/Android.
- **DB:** добавлена миграция `20260607_0011_planning_allocation_asset_target.py`.
- **Android:** planning flow расширен выбором/созданием asset/investment целей.
- **Repo hygiene:** `.gitignore` обновляется для raw QA artifacts.
- **Важно:** финальные QA/deploy цифры и deploy success пока не зафиксированы; их должен добавить оркестратор/QA после завершения проверки.

### Открытые баги (P1)

- BUG-006: AddAccountSheet всегда создаёт shared-счёт
- BUG-007: Нет защиты от double-tap на деструктивные действия
- BUG-008: Удаление транзакции без подтверждения
- BUG-009: Суммирование мультивалют без конвертации
- BUG-023: quickAddCategoryFor молча подменяет выбор

## Ветки

- `codex/finance-planning-mvp-gpt5` — текущая кодовая ветка Planning MVP / asset-target WIP
- `fix/aggregate-parser-multiline-labels` — базовая ветка UI overhaul + bug fixes
- `main` — стабильная

## Правила поставки

- После завершения конечной задачи исполнитель автоматически обновляет релевантную базу знаний Obsidian по проекту Finance, затем выполняется commit изменений.
- Ветка для изменений должна быть человекочитаемой и отражать проект и модель/агента, которыми выполнялись изменения, например `codex/finance-gpt5-update-kb-and-rules`.
- Основной чат-оркестратор не обновляет базу знаний и не делает commit напрямую: он поручает это ограниченному исполнителю или git-агенту.

## Окружения

| Окружение | Описание |
|-----------|----------|
| Development | Локально, .venv, npm run dev, Android emulator |
| Staging | Упоминается |
| Production | Self-hosted Linux, nginx |

## Ключевые термины

См. [[MOC_Finance#Глоссарий|глоссарий проекта]].

## Privacy/Security инварианты

1. Personal owner-only
2. Shared active-only
3. Filter-before-aggregate
4. Same-scope transfers
5. Neutral responses
6. Capture drafts user-initiated
7. No secrets in logs
8. No bank/broker credentials
9. Server-side authz only
10. Backup encryption

## Риски

| ID | Описание |
|----|----------|
| P1-B02 | Критический баг №02 |
| P1-B03 | Критический баг №03 |
| Tag | Tag misalignment |

## Связанные заметки

- [[MOC_Finance]] — навигационная MOC-карта
- [[MOC_Все_Проекты]] — все проекты vault
