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
