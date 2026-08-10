---
id: "qa-fixes-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-07-27"
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
| `1581a6f` | fix(android): use production API base for APK |
| `16a8be8` | fix(android): refine asset category interactions |
| `f5afcda` | fix(android): complete legacy asset edit and IME handling |
| `09ea647` | fix(finance): compact investment asset categories |

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
| NEWDIS-APK-DEBUG | APK `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D`; debug-signed; superseded by NEWDIS-APK-PROD-BASE | Android delivery | 2026-06-08 | Историческое, superseded |
| NEWDIS-APK-PROD-BASE | Android APK rebuilt after commit `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3`; `BUILD SUCCESSFUL`; unit XML 9 files / 61 tests / 0 failures-errors-skipped; APK SHA256 `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94`; contains `http://45.10.110.42/finance-api`; excludes dev/local bases and duplicated `/api/v1` base | Android delivery | 2026-06-08 | Да с ограничением |

## Волна 8 (2026-06-08)

Финальный статус: Android UX fixes для asset categories и AddAccountSheet закрыты по code-review/unit/Kotlin evidence. Project commit `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`); branch `newDis`, remote parity OK. Изменены только `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt` и `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`. Evidence: [[Док_Release_NewDis_20260608]].

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ANDROID-RECENTS-SAVER | Probable recents/overview crash fixed через custom Saver для nullable `AddAccountState?` | Android state saving | 2026-06-08 | Да (`:app:testDebugUnitTest` 61 tests, 0 failures/errors/skipped; manual recents proof still recommended) |
| ASSET-CATEGORY-EDIT-UX | Asset category edit получил явную edit icon; visible investment checkbox сохраняется через existing update flow | Android asset categories | 2026-06-08 | Да (`:app:testDebugUnitTest`, `:app:compileDebugKotlin`) |
| ADD-ACCOUNT-IME | AddAccountSheet использует IME padding, scroll и BringIntoView для focused fields above keyboard | Android account creation | 2026-06-08 | Да с ограничением (build/unit/Kotlin pass; manual keyboard QA recommended) |
| ASSET-CATEGORY-ARCHIVE-SAFE | Destructive bulk archive gesture removed; trash confirmation added; non-empty category archive blocked with move/delete accounts instruction; empty category archive calls backend category archive endpoint | Android asset categories + API client | 2026-06-08 | Да (`:app:testDebugUnitTest`, `:app:compileDebugKotlin`; confirmation dialog manual QA recommended) |
| ASSET-CATEGORY-REORDER | Long-press drag reorder for asset categories with local `SharedPreferences` persistence | Android asset categories | 2026-06-08 | Да с ограничением (code/build evidence; drag gesture manual QA recommended) |
| ANDROID-UX-QA-GATE | Review P0/P1 clean after P1 fix; unit and Kotlin gates green | Android QA | 2026-06-08 | Да |
| ANDROID-UX-APK | APK `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A`; contains `http://45.10.110.42/finance-api`; no dev/local URLs found | Android delivery | 2026-06-08 | Да с ограничением (debug-signed) |

## Волна 9 (2026-06-08)

Финальный статус: два user misses закрыты Android-only commit `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`); branch `newDis`, remote parity OK. Изменены только `apps/android/app/src/main/AndroidManifest.xml`, `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt` и `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`. Evidence: [[Док_Release_NewDis_20260608]].

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| LEGACY-ASSET-INVESTMENT-CHECKBOX | Legacy old asset group like `Вклад` получил checkbox `Инвестиция` в legacy edit dialog | Android asset categories | 2026-06-08 | Да (`:app:testDebugUnitTest`, `:app:compileDebugKotlin`, final review P0/P1 clean) |
| LEGACY-ASSET-RENAME-COMPAT | Checkbox off сохраняет old rename-only behavior | Android asset categories | 2026-06-08 | Да (`:app:testDebugUnitTest`) |
| LEGACY-ASSET-CONVERT | Checkbox on конвертирует legacy group в real asset category с `isInvestment=true` и links active legacy accounts | Android asset categories + API client | 2026-06-08 | Да с ограничением (unit/Kotlin/build pass; live migration manual QA recommended) |
| LEGACY-ASSET-CONVERT-GUARDS | Блокируются empty group, mixed-currency group, overview/no writable scope | Android asset categories | 2026-06-08 | Да (`:app:testDebugUnitTest`, final review P0/P1 clean) |
| LEGACY-ASSET-ROLLBACK | Rollback на link failure использует updated account versions и archives created category | Android asset categories + API client | 2026-06-08 | Да (`:app:testDebugUnitTest`, final review P0/P1 clean) |
| ADD-ACCOUNT-IME-FINAL | `MainActivity` `adjustResize`; `AddAccountSheet` `skipPartiallyExpanded`, `imePadding`, `navigationBarsPadding`, repeated `BringIntoView`, larger spacer; Material3 `windowInsets` fallback | Android account creation | 2026-06-08 | Да с ограничением (unit/Kotlin/build pass; visual IME manual QA recommended) |
| ANDROID-FINAL-QA-GATE | Review P0/P1 clean; `:app:testDebugUnitTest` PASS, 61 tests, 0 failures/errors/skipped; `:app:compileDebugKotlin` PASS; `assembleDebug` PASS | Android QA | 2026-06-08 | Да |
| ANDROID-FINAL-APK | APK `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B`; production API base found x2; dev URLs absent | Android delivery | 2026-06-08 | Да с ограничением (debug-signed) |

## Волна 10 (2026-06-08)

Финальный статус: compact investment asset category/iconKey/analytics fix закрыт commit `09ea6479451c61b3d06a412e5aaaecec534fc96a` (`fix(finance): compact investment asset categories`); branch `newDis`, remote parity OK. Evidence: [[Док_Release_NewDis_20260608]].

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ASSET-CATEGORY-COMPACT-CARD | `AssetCategoryGroupCard` compacted; linked accounts list removed from card | Android asset categories | 2026-06-08 | Да (`:app:testDebugUnitTest`, `:app:assembleDebug`, integration review P0/P1 clean) |
| ASSET-CATEGORY-EDIT-SIMPLIFIED | Category edit mode simplified; manual amount hidden when linked accounts exist; linked accounts list removed from edit/card | Android asset categories | 2026-06-08 | Да с ограничением (build/unit pass; visual manual QA recommended) |
| ASSET-CATEGORY-INVESTMENT-BADGE | Investment badge uses trending-up icon | Android asset categories | 2026-06-08 | Да с ограничением (build/unit pass; visual screenshot/device check recommended) |
| ASSET-CATEGORY-ICON-KEY | Icon picker added and `asset_categories.icon_key` persisted through backend/API/Android | Backend/API/Android | 2026-06-08 | Да (`31 passed, 2 warnings`; Android unit/build successful) |
| ANALYTICS-INVESTMENT-TOTALS | Android forced currency filter removed; investment totals parsed from backend contract | Android analytics/API contract | 2026-06-08 | Да (`31 passed, 2 warnings`; Android unit/build successful) |
| COMPACT-ASSET-QA-GATE | Backend targeted suite, Android unit/build and integration review all green for P0/P1 | QA | 2026-06-08 | Да (`31 passed, 2 warnings`; `:app:testDebugUnitTest` successful; `:app:assembleDebug` successful; P0/P1 clean) |
| COMPACT-ASSET-APK | APK `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733`; prod API base present, dev URLs absent | Android delivery | 2026-06-08 | Да с ограничением (debug-signed; visual manual QA still required) |

## Волна 11 (2026-06-10)

Финальный статус: asset/planning regression fix закрыт project commit `1013e632d54c6af6ed9326d8b7f761bdd381bade`; branch `newDis`, push completed. Evidence: [[Док_Release_NewDis_20260608]].

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ASSET-LINKED-ROWS-EXPANDED | Expanded asset category card снова показывает linked account rows; `Вклад` ожидаемо показывает 4 linked accounts | Android asset categories | 2026-06-10 | Да (`:app:compileDebugKotlin`, `:app:testDebugUnitTest`, review P0/P1 clean) |
| ASSET-EDIT-MODE-CLEAN | Category edit mode остаётся без linked account list | Android asset categories | 2026-06-10 | Да с ограничением (manual visual QA recommended) |
| LEGACY-ASSET-VISIBILITY | Legacy visibility logic для `Карта`/`Банк` восстановлена без дублей, когда real backend categories представляют тип | Android asset categories | 2026-06-10 | Да (`:app:testDebugUnitTest`, review P0/P1 clean) |
| CATEGORY-INVESTMENT-SAVE | Category-level `isInvestment` save/local state update fixed; `Брокер` investment updates badge/state and analytics inputs | Android asset categories + analytics inputs | 2026-06-10 | Да (`:app:testDebugUnitTest`, packaging gates) |
| PLANNING-MONTH-CLAMP | `План месяца`: months earlier than current are disabled; persisted/selected past month clamps to current-or-future | Android planning | 2026-06-10 | Да (`:app:testDebugUnitTest`, review P0/P1 clean) |
| PLANNING-404-FRIENDLY | Missing plan 404 treated as empty state / friendly planning message instead of raw `Resource not found or not accessible.` | Android planning/API handling | 2026-06-10 | Да (`:app:testDebugUnitTest`) |
| RUSSIAN-INPUT-DIAGNOSIS | App-level Cyrillic filter not found; AVD `Codex` had `hw.keyboard=yes`, likely emulator/IME config | Android input diagnosis | 2026-06-10 | Диагностировано; workaround: Russian Android keyboard or `show_ime_with_hard_keyboard` / hardware keyboard off |
| ASSET-PLANNING-QA-GATE | Kotlin compile, Android unit, packaging unit and assemble gates all green; review has no P0/P1 | QA | 2026-06-10 | Да |
| ASSET-PLANNING-APK | APK `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `FCD7EE0D870A12B3B88416DAEBCB3CF35FC513618C865B427E30E5F77F688411`; prod URL found in `classes7.dex`/`classes5.dex`, dev URLs absent; installed on AVD `Codex` | Android delivery | 2026-06-10 | Да с ограничением (debug-signed; visual manual QA still required) |

## Волна 12 (2026-06-12)

Финальный статус: critical Android regression `Брокер -> Инвестиция -> Сохранить` закрыт по build/unit gates, final APK checksum, quick critical-path QA PASS and fail-fast harness PASS. Project commit `d8175116f5123b6a304d4bd22dc083f2725505a0` (`fix(finance): migrate legacy brokerage assets`) pushed to `origin/newDis`. Evidence: [[QA_Результаты]], [[Док_Release_NewDis_20260608]], `MVP_EVIDENCE/critical-investment-fix-20260612/SUMMARY_SANITIZED.md`.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| CRITICAL-INVESTMENT-CREATE-PAYLOAD | Android больше не отправляет `iconKey` в `POST /api/v1/asset-categories`; deployed strict OpenAPI `AssetCategoryCreateRequest` не получает extra field и не возвращает validation failure до create/link | Android API payload / asset categories | 2026-06-12 | Да (`compileDebugKotlin`, `testDebugUnitTest` 71 tests, `assembleDebug`; quick QA PASS) |
| CRITICAL-INVESTMENT-LINK | `Брокер -> Инвестиция -> Сохранить` создаёт/линкует asset category; after save/restart есть linked asset category id, `isInvestment=True`, `investmentCategories.count=1` | Android asset categories + analytics | 2026-06-12 | Да (quick critical-path QA PASS on `emulator-5556`) |
| CRITICAL-INVESTMENT-TOTALS | Investment totals after save and after restart remain `150000.0000 RUB` | Android analytics/API verification | 2026-06-12 | Да (quick QA PASS; no `Validation failed`) |
| CRITICAL-INVESTMENT-HARNESS | Fail-fast harness verifies selected serial, APK hash, install, launch and bounded UI probe to avoid stale-serial hang mode | QA harness | 2026-06-12 | Да (harness PASS on `emulator-5556`) |
| CRITICAL-INVESTMENT-APK | APK `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk`, size `54235740`, SHA256 `B6960DB5D13198405984C027746343432CB95B0C08BB24F54D6A7FCD5061DCC7` | Android delivery | 2026-06-12 | Да с ограничением (debug-signed) |

## Волна 13 (2026-06-18/2026-06-19)

Финальный статус: offline-first release QA branch `codex/offline-first-release-qa` зеленый на GitHub Actions run `27796358035`, head `b09043e531152bb5f9b2fdb6ef18b21d786bbebf`, release id `20260618T234841Z-b09043e5`. PR `https://github.com/DmtrGoltsev/finance/pull/1` merged at `2026-06-18T23:53:47Z`; remote `main` HEAD и merge commit подтверждены как `cff578df0be001c0af187c5a90d9917fc0b2c1e9` с parents `3f70a3bf...` + release head `b09043e5...`. Workflow files present on `main`; active workflows: `Finance HexCore Production CI/CD` id `298526666`, `Finance Production Manual Rollback` id `298581092`. Историческая deploy boundary этой QA-волны superseded by final production CI/CD state 2026-06-19; текущий production deploy status: PASS.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| OFFLINE-FIRST-RUFF-GATE | Backend ruff gate закрыт до green CI | Backend QA gate | 2026-06-18 | Да (GitHub Actions green run `27796358035`) |
| OFFLINE-FIRST-ROUTE-INTROSPECTION | FastAPI `0.137.2` route introspection переведена на `iter_route_contexts` | Backend API/test infrastructure | 2026-06-18 | Да (backend package `285 passed, 6 skipped`) |
| OFFLINE-FIRST-BACKEND-DEPS-PIN | Backend deps pinned: `fastapi==0.137.2`, `starlette==1.3.1` | Backend dependencies | 2026-06-18 | Да (green CI head `b09043e531152bb5f9b2fdb6ef18b21d786bbebf`) |
| OFFLINE-FIRST-FRONTEND-GATE | Frontend package gate зеленый | Frontend QA | 2026-06-18 | Да (`56 passed`) |
| OFFLINE-FIRST-LOCAL-E2E | Local Android emulator E2E PASS по sanitized report | Android/local QA | 2026-06-18 | Да (`MVP_EVIDENCE/offline-first-release-qa-20260618-234050/QA_REPORT_SANITIZED.md`) |
| OFFLINE-FIRST-PROD-DEPLOY-GATE | Historical QA-wave boundary superseded by final production CI/CD state 2026-06-19 | Release/production readiness | 2026-06-19 | Superseded; current production deploy PASS |

## Волна 14 (2026-06-19)

Финальный статус: native iOS parity branch `codex/IOS` в `C:\Users\style\Documents\Codex\Финансы-ios` обновлен до статуса Windows static QA PASS без FAIL; base `origin/main` commit `66feadd94dbf936faec500f565638973ca270f64`. Native-only target остается `apps/ios`; PWA/Capacitor wrapper under `apps/web-pwa` не является parity target. Release sign-off заблокирован только Mac/Xcode gates: `swift`, `xcodebuild`, `xcodegen` unavailable.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| IOS-NATIVE-CONFIG-AUTH | API config hardening/Release guard, auth/register/session/logout wipe surfaces documented as implemented for native iOS branch | iOS config/auth | 2026-06-19 | Да по Windows static QA; Mac/Xcode runtime proof pending |
| IOS-NATIVE-TRANSACTIONS-CAPTURE | Manual date-only/payment filter fallback and capture editable amount/date with online-only OCR/copy boundary documented | iOS transactions/capture | 2026-06-19 | Да по Windows static QA; simulator/device UX proof pending |
| IOS-NATIVE-ASSETS-ANALYTICS-PLANNING | Payment account/assets/investment/icon preservation, analytics month/category/investments, planning fallback for exposed mutations documented | iOS assets/analytics/planning | 2026-06-19 | Да по Windows static QA; Xcode tests pending |
| IOS-NATIVE-OFFLINE-SYNC | Local JSON store, sync queue, manual sync, sync issues and Russian sync UI documented | iOS offline/sync | 2026-06-19 | Да по Windows static QA; backend push/pull convergence proof pending |
| IOS-NATIVE-MAC-XCODE-GATE | Native iOS release remains blocked until XcodeGen, Debug/Release build, simulator/device, Keychain/cookie wipe, offline queue and OCR/copy online-only UX gates pass | iOS release gate | 2026-06-19 | BLOCKED by missing Mac/Xcode tools |

## Волна 15 (2026-07-12)

Финальный статус: Android Assets / Investment quick add поставка закрыта для ручной установки APK. Backend production deploy не выполнялся; offline sync investment operation требует отдельного release-branch deploy через GitHub Actions. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-assets-investment-postp2-qa-20260712-112610`.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ANDROID-ASSETS-TITLE-LAYOUT | Карточки категорий активов больше не сжимают title до `Б...`/`Вк...`; счетчик не переносится по буквам; сумма и `Править` вынесены из зоны, ломающей title | Android Assets UI | 2026-07-12 | Да (targeted `AppSectionTest`, emulator-5554 Assets smoke) |
| ANDROID-QUICK-ADD-INVESTMENT | Quick add type `Инвестиция` создает `transactionType=asset_buy`, `categoryId=null`, принимает дату/сумму и не проходит как обычный `Расход` | Android quick add / API payload | 2026-07-12 | Да (`ApiClientCaptureDraftTest`, `PlanningUiStatusTest`, emulator-5554 smoke) |
| INVESTMENT-ACCOUNT-FILTER | Для quick add `Инвестиция` выбираются только счета, привязанные к investment asset category | Android quick add / asset categories | 2026-07-12 | Да (targeted tests + manual smoke) |
| INVESTMENT-ACTUAL-SEMANTICS | Investment allocation actual считается по categoryless investment transactions (`brokerage`, `asset_buy`, `interest`, `dividend`, `adjustment`) на linked investment accounts; `expense`/`transfer` исключены | Backend planning/reports domain | 2026-07-12 | Да (backend targeted planning/transactions/reports `30 passed`) |
| LOCAL-SYNC-CATEGORY-NULL | Local sync сохраняет explicit `categoryId:null`; local backend sync allowlist расширен для investment types | Android local sync / backend sync | 2026-07-12 | Да (`SyncManagerTest`; backend sync pytest `21 passed`; ruff sync files) |
| ANDROID-RELEASE-APK-POSTP2 | Финальный APK `finance-android-prod-20260712-112532-POSTP2-manual-install.apk`, SHA256 `cace0eb69e589f8eb0be579a0a4bc83039013d35a29d74e32547367449ee4d79`; prod URL release build, signed by `apksigner` | Android delivery | 2026-07-12 | Да с ограничением (manual install APK; backend deploy not done) |
| BACKEND-DEPLOY-BOUNDARY-POSTP2 | Online direct `asset_buy` uses existing transactions API; offline sync investment operation remains blocked until GitHub Actions release branch deploy | Release/deploy boundary | 2026-07-12 | BLOCKED for prod backend deploy; no SSH/SCP used |

## Волна 16 (2026-07-12)

Финальный статус: POSTP1 transfer/assets/order wave закрыта для ручной установки APK. Исправлен путь, где перевод через `Операции` / quick add на инвестиционный счёт должен отражаться в `Активы`: Android берёт totals категорий активов из свежих `dashboard.accounts.currentBalance` по `assetCategoryId`, backend sync публикует `accounts/update` для source/destination после `transfer`. Backend production deploy не выполнен; prod sync behavior требует GitHub Actions release branch. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-transfer-assets-ordering-postp1-qa-20260712-215452`.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| TRANSFER-ASSET-TOTALS-DASHBOARD | Перевод на investment-linked account отражается в `Активы`, потому Android asset category totals считаются из свежих `dashboard.accounts.currentBalance` по `assetCategoryId` | Android Assets / Dashboard contract | 2026-07-12 | Да (Android targeted/full PASS; emulator-5554 smoke) |
| TRANSFER-ACCOUNT-SYNC-PUSH | Backend transfer REST/sync push emits `accounts/update` для source и destination account после transfer | Backend sync / accounts | 2026-07-12 | Да (backend targeted `49 passed`; `ruff` PASS) |
| TRANSFER-NOT-INVESTMENT-ACTUAL | `transfer` меняет balances/assets, но не считается investment actual плана; `asset_buy` остаётся investment actual | Backend planning/reports domain | 2026-07-12 | Да (reports/planning regression tests included in `49 passed`) |
| TRANSFER-QUICK-ADD-DATE | Android transfer quick add показывает выбор даты и отправляет `transactionDate` | Android Operations quick add | 2026-07-12 | Да (Android targeted/full PASS) |
| OPERATIONS-NEWEST-FIRST-ANDROID | Android вкладка `Операции` сортирует операции newest-first | Android Operations UI | 2026-07-12 | Да (Android targeted/full PASS; emulator-5554 smoke) |
| OPERATIONS-NEWEST-FIRST-PWA | PWA `recentTimeline` сортируется newest-first; Overview/Operations показывают новые операции выше старых | PWA Overview/Operations | 2026-07-12 | Да (PWA targeted ordering/build PASS; broader `App.test` has 2 known date-sensitive failures around June 2026) |
| SYNC-PULL-SEQ-BOUNDARY | Sync pull order by `seq` не менялся, потому это cursor protocol | Sync protocol boundary | 2026-07-12 | Зафиксировано как intentional boundary |
| ANDROID-RELEASE-APK-POSTP1-TRANSFER | Финальный APK `finance-android-prod-20260712-220221-POSTP1-TRANSFER-manual-install.apk`, SHA256 `B4AF3B3CF30E77F5C22075B9EFC47D82CBBF5FBCDDF5356D286F37DDEB3209C6`; prod URL; install/smoke без изменения данных | Android delivery | 2026-07-12 | Да с ограничением: backend deploy not done |
| BACKEND-DEPLOY-BOUNDARY-TRANSFER | DB migration не требуется; prod backend должен быть развёрнут через GitHub Actions release branch для account sync changes | Release/deploy boundary | 2026-07-12 | REQUIRED for prod sync behavior; no SSH/SCP used |

## Волна 17 (2026-07-25)

Финальный статус: Android auth/session wave закрыта по backend auth QA, Android unit/build/signing gates и security review. Android signed-out/restoring больше не выглядит как вкладка: отдельный AuthGate показывается без TopAppBar, NavigationBar, FAB и protected tabs; main tabs доступны только signed-in. Сессия хранится как `SessionTokenBundle` в `EncryptedSharedPreferences` (`accessToken`, `refreshToken`, `expiresAt`, `userId`), пароль не хранится. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-auth-session-qa-20260725-231110`.

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| AUTHGATE-PROTECTED-TABS-SEPARATION | Android signed-out/restoring state renders a separate AuthGate without protected app chrome; protected tabs are reachable only after signed-in state | Android auth UI | 2026-07-25 | Да (Android full unit PASS; emulator manual smoke skipped because emulator unavailable) |
| SESSIONTOKENBUNDLE-ENCRYPTED-STORE | Android persists `SessionTokenBundle` in `EncryptedSharedPreferences`: `accessToken`, `refreshToken`, `expiresAt`, `userId`; password is not stored | Android local session storage | 2026-07-25 | Да (unit/build evidence; no secrets copied to KB) |
| API-CLIENT-REFRESH-RETRY-ONCE | Login/register save token bundle; protected calls on `401`/`403` call `POST /api/v1/sessions/refresh` once and retry once | Android API client | 2026-07-25 | Да (Android full unit PASS; backend auth `71 passed`) |
| API-CLIENT-AUTH-FAILURE-WIPE | Logout or refresh/auth failure clears local token store and protected UI | Android API client/session UX | 2026-07-25 | Да (Android full unit PASS) |
| OCR-REFRESH-RETRY-ONCE | Screenshot OCR follows the same auth refresh/retry-once behavior | Android OCR/API client | 2026-07-25 | Да (Android full unit PASS) |
| BACKEND-SESSION-REFRESH-ENDPOINT | Backend adds `/api/v1/sessions/refresh`; `android_bearer` login/register return `refreshToken`; refresh token rotation is hash-only and invalidates the old refresh token; logout invalidates session; CAS atomic rotation covered | Backend auth/session | 2026-07-25 | Да locally (`71 passed`, `ruff` PASS); production requires deploy |
| AUTH-SESSION-NO-DB-MIGRATION | Auth/session refresh implementation requires no DB migration | Backend/DB | 2026-07-25 | Да |
| AUTH-SESSION-SECURITY-REVIEW | Security review after fixes found no P0/P1/P2 | Security review | 2026-07-25 | Да |
| AUTH-SESSION-APK | APK `finance-android-prod-20260725-231110-AUTH-SESSION-manual-install.apk`, SHA256 `F9ABD3D02D64A06FCB5E78731AC313FD8230165CF9BC8D427E2FED92466BB8A0`; built/signed/verified | Android delivery | 2026-07-25 | Да с ограничением: manual install/smoke skipped because emulator unavailable |
| AUTH-SESSION-PROD-DEPLOY-CAVEAT | Historical pre-deploy caveat superseded by backend auth refresh production deploy on branch `prod/finance-auth-refresh-20260725` | Release/deploy boundary | 2026-07-25 | SUPERSEDED; no direct SSH/SCP used |

## Wave 18 (2026-07-25)

Final status: backend auth refresh production deploy completed through GitHub Actions for branch `prod/finance-auth-refresh-20260725`, commit `9e1ed7903798ed4f1edbcfeb3d98b23ec9ae0763`, release id `finance-backend-auth-refresh-20260725-9e1ed79`. The workflow run `https://github.com/DmtrGoltsev/finance/actions/runs/30174265210` is `completed/failure` only because unrelated `frontend-ci-package`/PWA tests failed; backend-only dispatch skipped frontend deploy and `deploy-backend` succeeded.

| ID | Description | Area | Date | Verified |
|----|-------------|------|------|----------|
| AUTH-REFRESH-PROD-BACKEND-DEPLOY | Production backend contains `/api/v1/sessions/refresh`; empty payload returns 422, confirming route mounted | Backend deploy/auth route | 2026-07-25 | Yes: health 200 and route smoke |
| AUTH-REFRESH-ROTATION-PROD-SMOKE | Registration 201, refresh 200, token fields present, refresh rotated, old refresh rejected 401 | Backend auth/session smoke | 2026-07-25 | Yes; sanitized evidence only, no tokens/passwords |
| AUTH-REFRESH-DEPLOY-ARTIFACT | Backend artifact checksum `da77996a82489e1732a77686eda2965b6f51113d8528828151927ca42b384491` recorded for release `finance-backend-auth-refresh-20260725-9e1ed79` | Release evidence | 2026-07-25 | Yes |
| AUTH-REFRESH-NO-MIGRATION | `run_migrations=false`; DB migrations not run; workflow backup not created; DB migration not required | DB/deploy boundary | 2026-07-25 | Yes |
| AUTH-REFRESH-NO-LOCAL-SSH | Direct local SSH/SCP not used; staged files exactly allowed auth/OpenAPI backend list | Deploy hygiene | 2026-07-25 | Yes |
| AUTH-REFRESH-WORKFLOW-CAVEAT | Workflow emails may report failed due unrelated frontend job, but backend deploy is successful | Release communications | 2026-07-25 | Documented |

## Wave 19 (2026-07-26)

Final status: Android-only category search/category dialog/analytics/top-categories POSTP2 wave closed for manual APK install. Backend deploy was not required; production API already returns `investmentsByCurrency[*].investmentsTotal`. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-category-analytics-postp2-qa-20260726-160224\SUMMARY.md`.

| ID | Description | Area | Date | Verified |
|----|-------------|------|------|----------|
| CATEGORY-EXPENSE-SEARCH | Expense add/confirm category selection supports fast text search by part of word | Android expense UX | 2026-07-26 | Yes: targeted/full unit and Kotlin gates PASS |
| CATEGORY-DIALOG-VERTICAL-LIST | Horizontal category lists were replaced by `Категория` button opening overlay/dialog with vertically scrollable searchable list | Android expense UX | 2026-07-26 | Yes: `AppSectionTest` PASS |
| ANALYTICS-INVESTMENT-TOTAL-MAPPING | `Анализ -> Сводка -> Инвестиции` fills Android investment total from `investmentsByCurrency` with summary fallback | Android analytics/API mapping | 2026-07-26 | Yes: `ApiClientDashboardTest` PASS |
| HOME-TOP-CATEGORIES-ALL | `Главная -> Топ категории` has `Все`, opening all spending categories sorted by amount descending | Android home analytics UX | 2026-07-26 | Yes: `AppSectionTest` PASS |
| TOP-CATEGORIES-EXPENSE-ONLY | Top categories count only expense categories and exclude expense transactions pointing to income/asset `categoryId` | Android dashboard analytics | 2026-07-26 | Yes: POSTP2 source confirmation and unit gate PASS |
| CATEGORY-DIALOG-STATE-KEYED | Category dialog search state is keyed by row/mode and does not leak between selectors | Android Compose state | 2026-07-26 | Yes: POSTP2 source confirmation and unit gate PASS |
| CATEGORY-ANALYTICS-APK | APK `finance-android-prod-20260726-160500-CATEGORY-ANALYTICS-POSTP2-manual-install.apk`, SHA256 `188eae471e36f1cdfe2e4f92ce1f7da7e5fa1d1febb9c80ab5a96c494503d0b1`; prod URL markers present, local markers absent; signed/aligned/verified | Android delivery | 2026-07-26 | Yes with caveat: manual install/e2e skipped because no adb device |
| CATEGORY-ANALYTICS-BACKEND-BOUNDARY | Backend deploy not needed for this wave; no real production data changed | Release boundary | 2026-07-26 | Documented |

## Wave 20 (2026-07-26)

Final status: monthly investment transfers reports/Android QA closure passed locally. The backend fix changes `/reports/summary.investmentsTotal` from broad asset balance semantics to selected-period monthly incoming investment transfers; Android Analytics uses the summary value only and does not derive/fallback from `/reports/account-balances`. Backend production deploy is required and was not performed by this worker. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\monthly-investment-transfers-qa-20260726-221828\SUMMARY.md`.

| ID | Description | Area | Date | Verified |
|----|-------------|------|------|----------|
| REPORTS-MONTHLY-INVESTMENT-TRANSFERS | `/reports/summary.investmentsTotal` means visible incoming `transfer` operations for selected period/month into investment asset accounts/categories, not total asset balance | Backend reports business rule | 2026-07-26 | Yes: backend targeted `25 passed`, backend full `302 passed` |
| ACCOUNT-BALANCES-BOUNDARY | `/reports/account-balances` remains the asset/account balance endpoint and is not the source for Android summary investment fallback | Backend/API boundary | 2026-07-26 | Documented and covered by reports/assets QA |
| ANDROID-SUMMARY-INVESTMENTS-NO-FALLBACK | Android Analytics summary investments consumes summary data only; no account-balances fallback for this metric | Android analytics/API mapping | 2026-07-26 | Yes: `ApiClientDashboardTest`, `AppSectionTest`, full unit `174 tests` |
| MONTHLY-INVESTMENT-TRANSFERS-APK | APK `finance-android-prod-20260726-221828-MONTHLY-INVESTMENT-TRANSFERS-manual-install.apk`, SHA256 `46e85ee4e5c6b4b13cf84abd4da22dcffc2642d0e9afd7d6be16f5c40783a9ca`; prod URL markers present, local markers absent; signed/aligned/verified | Android delivery | 2026-07-26 | Yes with caveat: manual install/launch skipped because no adb device |
| MONTHLY-INVESTMENT-TRANSFERS-BACKEND-DEPLOY | Backend production deploy is required for production semantics; this worker did not deploy, commit, push or mutate production data | Release/deploy boundary | 2026-07-26 | REQUIRED / NOT_DONE |

## Wave 21 (2026-07-27)

Final status: PWA iPhone browser parity post-fix QA passed locally after `TopCategoriesDialog` portal/layer correction. No code changes, deploy, commit or push were performed by this QA/documentation worker. Evidence: [[QA_Результаты]], `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\pwa-iphone-parity-postfix-qa-20260727-005600\SUMMARY.md`.

| ID | Description | Area | Date | Verified |
|----|-------------|------|------|----------|
| PWA-IPHONE-UNIT-BUILD | PWA unit suite and production build are green | PWA QA gate | 2026-07-27 | Yes: `npm.cmd test` 4 files / 65 tests; `npm.cmd run build` PASS |
| PWA-IPHONE-MOBILE-SMOKE | Login, home, quick add, category overlay and analytics match iPhone browser layout expectations without horizontal overflow | PWA iPhone browser UX | 2026-07-27 | Yes: Playwright Chromium iPhone 14 screenshots and hit-tests |
| PWA-TOP-CATEGORIES-SERVER-FIRST | `Все категории трат` uses server category breakdown path without fallback warning | PWA analytics/dashboard | 2026-07-27 | Yes: smoke JSON `fallbackWarnings=0` |
| PWA-TOP-CATEGORIES-LAYER | `TopCategoriesDialog` overlays fixed mobile FAB and bottom nav | PWA modal layering | 2026-07-27 | Yes: `elementFromPoint` at FAB/nav centers returns elements inside modal/dialog |
| PWA-TOP-CATEGORIES-INTERNAL-SCROLL | Long all-categories content scrolls inside the dialog list container | PWA modal scroll | 2026-07-27 | Yes: inner `.listStack` `clientHeight=570`, `scrollHeight=2594`, `after=2024` |
| PWA-PARITY-BACKEND-BOUNDARY | Backend code was not changed in this PWA parity task | Release boundary | 2026-07-27 | Documented |

## Коммиты
