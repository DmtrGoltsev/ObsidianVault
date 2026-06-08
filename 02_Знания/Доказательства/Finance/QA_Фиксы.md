---
id: "qa-fixes-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-06-08"
ссылки:
  - "[[Finance]]"
  - "[[QA_Результаты]]"
  - "[[Док_Release_NewDis_20260608]]"
---

# QA Фиксы — Finance MVP Android

## Волна 1 (2026-06-06)

| ID | Описание | Файл | Дата | Верифицирован |
|----|----------|------|------|---------------|
| BUG-001 | userFacingMessage показывает реальные ошибки | FinanceApp.kt:2870 | 2026-06-06 | Да (сборка OK) |
| BUG-002 | updateTransaction использует реальные данные | ApiClient.kt:498 | 2026-06-06 | Да (сборка OK) |
| BUG-003 | Пароли в remember вместо rememberSaveable | FinanceApp.kt:111-112 | 2026-06-06 | Да (сборка OK) |
| BUG-004 | Фильтрация архивных записей в QuickAdd | FinanceApp.kt:2285-2286 | 2026-06-06 | Да (сборка OK) |
| BUG-005 | Сессия сбрасывается при 401 с понятным сообщением | FinanceApp.kt:319 | 2026-06-06 | Да (сборка OK) |
| BUG-010 | parseSession извлекает displayName из API | ApiClient.kt:731 | 2026-06-06 | Да (сборка OK) |
| BUG-011 | FAB скрыт на экране логина | FinanceApp.kt:613 | 2026-06-06 | Да (сборка OK) |
| BUG-012 | Кнопка «Подтвердить» отключена без выбора счёта/категории | FinanceApp.kt:1447 | 2026-06-06 | Да (сборка OK) |
| BUG-015 | Унификация fallback-валюты на RUB | FinanceApp.kt:518 | 2026-06-06 | Да (сборка OK) |
| BUG-016 | «Включено» вместо «Включить» | FinanceApp.kt:1285 | 2026-06-06 | Да (сборка OK) |
| BUG-017 | editName сбрасывается при отмене | FinanceApp.kt:1859, 2050 | 2026-06-06 | Да (сборка OK) |
| BUG-019 | captureSource локализован (Скриншот/Ручной ввод) | FinanceApp.kt:1382 | 2026-06-06 | Да (сборка OK) |
| BUG-022 | SignInCard не мигает + loading indicator | FinanceApp.kt:634, 663-673 | 2026-06-06 | Да (сборка OK) |
| L10N | 44 английских строки переведены на русский | FinanceApp.kt (全局) | 2026-06-06 | Да (сборка OK) |
| API-URL | Production URL через nginx: /finance-api | build.gradle.kts | 2026-06-06 | Да (curl 401 OK) |

## Волна 2 (2026-06-06)

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ASSETS-UI | Tap category expand/collapse; edit group name без refresh icon; long press >1s confirmation/archive group accounts | Android Assets UI | 2026-06-06 | Да (сборка OK, runtime smoke MainActivity) |
| ACCOUNT-EDIT | Диалог редактирования счёта: `name`, `balance`, `currency`; XAU label `граммы`, icon gold bar | Android account edit | 2026-06-06 | Частично (`NOT_RUN` runtime flow: нет активных счетов/данных на `Codex`) |
| ACCOUNT-PATCH | `PATCH account` принимает `name`/`currentBalance`/`currency`/`version`; `initialBalance` не меняется | Backend/API | 2026-06-06 | Да (`22 passed, 1 warning`) |
| ACCOUNT-CURRENCY-GUARD | Запрет смены валюты счёта с транзакциями: `ACCOUNT_CURRENCY_IMMUTABLE_AFTER_TRANSACTIONS` | Backend/API + business rule | 2026-06-06 | Да (`22 passed, 1 warning`) |
| ACCOUNT-CONFLICT | Optimistic conflict для PATCH account: `CONFLICTING_UPDATE` | Backend/API | 2026-06-06 | Да (`22 passed, 1 warning`) |
| VIRTUAL-ASSET-GROUP-DELETE | Удаление виртуальной категории активов архивирует все активные счета группы | Android + business rule | 2026-06-06 | Частично (сборка OK; риск частичного применения при sequential `archiveAccount` failure) |

## Волна 3 (2026-06-06)

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| PLANNING-BACKEND | Planning package, таблицы `planning_plans`/`planning_income_sources`/`planning_allocations`, миграция `20260606_0010`, derived totals, copy attention rows | Backend/DB | 2026-06-06 | Да (`224 passed`, targeted `29 passed`) |
| PLANNING-OPENAPI | Planning endpoints добавлены в OpenAPI; parse OK, `PATH_COUNT=37`, все planning paths присутствуют | API contract | 2026-06-06 | Да (OpenAPI parse OK) |
| PLANNING-AUTHZ | personal owner-only и household active-member для planning API | Backend/API | 2026-06-06 | Да (targeted planning tests) |
| PLANNING-VALIDATION | Positive income validation; confirm обновляет только план и не создаёт транзакции | Backend/API + business rule | 2026-06-06 | Да (targeted planning tests) |
| PLANNING-ALLOCATIONS | Allocations to expense categories/accounts/assets/investments; режим `amount` или `percent`; underallocated/overallocated states | Backend/API + Android UI | 2026-06-06 | Да (`29 passed`, runtime smoke Planning screen) |
| PLANNING-SCOPE-INHERIT | Создание категории/счёта наследует scope текущего планирования | Backend/API + Android UI | 2026-06-06 | Да (targeted tests + build) |
| PLANNING-ANDROID-API | Planning DTO/methods добавлены в `ApiClient` | Android API client | 2026-06-06 | Да (`assembleDebug` BUILD SUCCESSFUL) |
| PLANNING-ANDROID-UI | `PlanningUi` добавлен во вкладки Analytics; экран показал следующий месяц/current plan/totals | Android UI | 2026-06-06 | Частично (runtime smoke на `Codex`; exhaustive manual scenario не проводился) |
| PLANNING-REMINDERS | Локальные reminders per income через `AlarmManager`/`BroadcastReceiver`, `POST_NOTIFICATIONS`; без FCM/SMS/NotificationListener/exact alarm | Android notifications | 2026-06-06 | Да (`assembleDebug` BUILD SUCCESSFUL, Codex runtime smoke) |
| PLANNING-DEV-SEED | Runtime fix для `dev_seed`: login 201, planning history 200, personal plan 200, без internal server error | Dev seed/runtime | 2026-06-06 | Да (`dev_seed` smoke) |

## Волна 4 (2026-06-07)

Финальный статус: кодовая ветка `codex/finance-planning-mvp-gpt5`, project commit `5bb7ab493d7c3faa323d711ffa1febb2d94b4f7c` (`fix(planning): support asset allocation targets`). Backend-only production release `20260607T121851Z-5bb7ab4` развернут в `/opt/finance/releases/20260607T121851Z-5bb7ab4`; `/opt/finance/current` указывает на новый release. Web frontend не деплоился; Android APK delivered locally.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| PLANNING-ASSET-TARGET-BACKEND | Явный Planning `targetType=asset` на backend; allocation target enum/schema/service/tests синхронизированы с asset/investment целями | Backend/API | 2026-06-07 | Да (`228 passed, 4 warnings`) |
| PLANNING-ASSET-TARGET-OPENAPI | OpenAPI контракт обновлен под явный `targetType=asset` для planning allocation targets; `AllocationTargetType` enum = `expense_category`, `account`, `asset` | API contract | 2026-06-07 | Да (OpenAPI enum evidence) |
| PLANNING-ASSET-TARGET-DB | Миграция `20260607_0011_planning_allocation_asset_target.py` для planning allocation asset target | DB migration | 2026-06-07 | Да (`20260531_0009 -> 20260606_0010 -> 20260607_0011`, after `20260607_0011 (head)`) |
| PLANNING-ASSET-TARGET-ANDROID | Android planning flow поддерживает выбор/создание asset/investment целей из planning flow | Android UI/API | 2026-06-07 | Да (`:app:testDebugUnitTest :app:compileDebugKotlin :app:assembleDebug ...` -> `BUILD SUCCESSFUL`) |
| QA-ARTIFACT-HYGIENE | `.gitignore` hygiene для raw QA artifacts | Repo hygiene | 2026-06-07 | Да (project commit `5bb7ab4`) |
| PROD-BACKEND-DEPLOY | Backend-only deploy release `20260607T121851Z-5bb7ab4`; service active; `/health` direct/nginx OK; unauth `sessions/current` 401 | Production deploy | 2026-06-07 | Да |
| PROD-BACKUP | Backup `/opt/finance/backups/20260607T122105Z-59603b0/finance_prod.dump`, SHA256 `adbed3574f02a4fad94c41ac0fa2e18b4abe3e3cd21d527c3bf08cab04c1a8ae` | Production backup | 2026-06-07 | Да |
| ANDROID-APK-DELIVERY | APK `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54235660`, SHA256 `9E3814A5ABBBD1A9EFB8D484A94C973E4CA2598D21D921B990EE1DFCA568C6D8`, time `2026-06-07 15:00:20 +03:00` | Android delivery | 2026-06-07 | Да |

## Волна 5 (2026-06-07)

Финальный статус: asset categories + Analytics/Planning polish готовы по QA evidence и подтверждены в production. Project commit `be9f8abe1abaed530c1dd503c5e631e935d8a3d5`; release `20260607T163043Z-be9f8ab` в `/opt/finance/releases/20260607T163043Z-be9f8ab`; `/opt/finance/current` указывает на этот release. Backup `/opt/finance/backups/20260607T163554Z-5bb7ab4/finance_prod.dump`, SHA256 `c7e38fae515b60b5d4b7d6588bbc8d03687d1769f222493ad240510f1f54b2d5`. Миграции: before `20260607_0011`, after `20260607_0012 (head)`. Service active/running; health direct/nginx 200; unauth `sessions/current` 401; OpenAPI 200 с asset categories routes.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ASSET-CATEGORIES-SOT | Asset categories стали source of truth: `manualAmount` для пустых категорий, `isInvestment`, `assetType`, связь `account.assetCategoryId`; удалённые счета не оставляют stale totals | Backend/API + data model | 2026-06-07 | Да (`238 passed, 8 warnings`) |
| ASSET-CATEGORIES-ENDPOINTS | Добавлены asset-categories endpoints | Backend/API | 2026-06-07 | Да (`238 passed, 8 warnings`) |
| REPORT-MODE-PERSONAL | Backend report поддерживает `reportMode=personal` | Backend/API | 2026-06-07 | Да (`238 passed, 8 warnings`) |
| MIGRATION-20260607-0012 | Миграция `20260607_0012` для asset categories/report updates | DB migration | 2026-06-07 | Да (`238 passed, 8 warnings`, fixtures `8 passed`) |
| ANALYTICS-INVESTMENTS | Добавлена investments metric; capital structure остаётся только в Analytics | Android UI/API | 2026-06-07 | Да (Android build `BUILD SUCCESSFUL`) |
| CATEGORIES-SCOPE-EDIT | Создание категорий учитывает scope `personal`/`household`; UI редактирования использует edit icon | Android UI/API | 2026-06-07 | Да (Android build `BUILD SUCCESSFUL`) |
| PLANNING-INCOME-ALLOCATIONS | Income day = день месяца; income form за Add; новые allocations выбирают expense category или investment asset category без account target; history text уточнён | Android UI/API + Planning rules | 2026-06-07 | Да (Android build `BUILD SUCCESSFUL`) |
| ANDROID-APK-BUILD | APK `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54235660`, SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26` | Android delivery final | 2026-06-07 | Да |
| PROD-DEPLOY-SUCCESS | Production release `20260607T163043Z-be9f8ab`; `/opt/finance/current` points to `/opt/finance/releases/20260607T163043Z-be9f8ab`; service active/running; health direct/nginx 200; unauth `sessions/current` 401; OpenAPI 200 с asset categories routes | Production deploy | 2026-06-07 | Да |
| PROD-BACKUP-20260607 | Backup `/opt/finance/backups/20260607T163554Z-5bb7ab4/finance_prod.dump`, SHA256 `c7e38fae515b60b5d4b7d6588bbc8d03687d1769f222493ad240510f1f54b2d5` | Production backup | 2026-06-07 | Да |

## Коммиты

| Хэш | Описание |
|------|----------|
| `95c882c` | feat(android): UI overhaul — edit/delete icons, account creation dialog, currency picker, category management, server OCR |
| `50a8f8c` | fix: 12 bugs fixed (P0-P2), full Russian localization, 91 QA test cases |
| `274c88f` | fix(finance): update assets UI and account patch flow |
| `0780944` | feat(finance): add planning MVP |
| `5bb7ab4` | fix(planning): support asset allocation targets |
| `be9f8ab` | asset categories + Analytics/Planning polish production release |
| `819b5815` | Release planning iteration MVP |
| `6ce31f5` | feat(finance): simplify newDis UX flows |

## Волна 6 (2026-06-07)

Финальный статус: planning iteration MVP закрыт и подтверждён в production. Project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8` (`Release planning iteration MVP`); branch `codex/finance-planning-mvp-gpt5` запушен в `origin`; release `20260607T225457Z-819b5815`. Backend current `/opt/finance/releases/20260607T225457Z-819b5815`; web current `/var/www/finance/releases/20260607T225457Z-819b5815`; оба prod `COMMIT` файла указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8`.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| PLANNING-RELEASE-COMMIT | Release commit `819b5815fed8c81bfa6a6e6131e790429454c2e8` с сообщением `Release planning iteration MVP`; ветка запушена в `origin` | Git/release | 2026-06-07 | Да |
| PLANNING-PROD-BACKEND-WEB | Backend и web current указывают на release `20260607T225457Z-819b5815`; prod `COMMIT` файлы совпадают с project commit | Production deploy | 2026-06-07 | Да |
| PLANNING-MIGRATION-0013 | Alembic head `20260607_0013 (head)` | DB migration | 2026-06-07 | Да |
| PLANNING-PROD-SMOKE | `finance-backend.service` active; health direct/nginx OK; `/finance/` 200; manifest scope/start_url `/finance/`; `/finance/sw.js` 200 | Production smoke | 2026-06-07 | Да |
| PLANNING-QA-GATE | OpenAPI parse OK; operationId duplicates `0/58`; backend `243 passed, 9 warnings`; Android unit PASS; Android assembleDebug PASS | QA gate | 2026-06-07 | Да |
| PLANNING-ACCEPTANCE-CLARIFICATION | Planning progress зафиксирован как allocation-level поля `PlanningAllocationDto.actualAmount`/`varianceAmount`/`status`/`attentionReason`; `previousMonthSurplus` в `PlanningSummaryDto` | Product/API contract | 2026-06-07 | Да |
| ANDROID-APK-DEBUG | APK `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54,235,660`, SHA256 `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4`; debug-signed | Android delivery | 2026-06-07 | Да с ограничением |

## Волна 7 (2026-06-08)

Финальный статус: `newDis` UX simplification закрыт по sanitized release closure. Project commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b` (`feat(finance): simplify newDis UX flows`); branch `newDis`, `HEAD = origin/newDis`. Commit не меняет `apps/backend`, `db`, `api`; backend redeploy waiver принят. Evidence: [[Док_Release_NewDis_20260608]].

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| NEWDIS-RELEASE-COMMIT | Release commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; branch `newDis`; `HEAD = origin/newDis` | Git/release | 2026-06-08 | Да |
| NEWDIS-PWA-PARITY | `/finance/COMMIT` 200 совпадает с local `apps/web-pwa/dist/COMMIT`; `/finance/`, `/finance/sw.js`, manifest, JS/CSS byte-hash equal local dist | Production frontend | 2026-06-08 | Да |
| NEWDIS-BACKEND-WAIVER | `/finance-api/health` 200 `{status:ok}`; exact commit endpoints return 404; waiver accepted because no backend/db/api delta | Production backend | 2026-06-08 | Да с ограничением |
| NEWDIS-ANDROID-UNIT | Android unit XML: 9 files, 60 tests, 0 failures, 0 errors, 0 skipped | Android QA | 2026-06-08 | Да |
| NEWDIS-ANDROID-LINT | Android lint: 0 errors, 6 warnings | Android QA | 2026-06-08 | Да с warnings |
| NEWDIS-APK-DEBUG | APK `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D`; debug-signed | Android delivery | 2026-06-08 | Да с ограничением |
