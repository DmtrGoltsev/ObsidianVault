---
id: "qa-results-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-08-23"
ссылки:
  - "[[Finance]]"
  - "[[QA_Фиксы]]"
  - "[[Док_Release_NewDis_20260608]]"
---

# QA Результаты — Finance MVP

## Волна 1: Статический аудит кода (2026-06-06)

**Метод:** Статический анализ FinanceApp.kt (~3030 строк) + ApiClient.kt (~936 строк) + аудит API-контрактов

**Агенты:** 2 параллельных (ревьюер кода + API-ревьюер)

### Сводка

| Метрика | Значение |
|---------|----------|
| Всего багов найдено | 25 |
| P0 (критические) | 3 |
| P1 (важные) | 8 |
| P2 (минорные) | 14 |
| API endpoint'ов проверено | 26 |
| Критических API расхождений | 0 |
| Исправлено в этой волне | 12 |

### Результаты по багам

#### P0 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-001 | `userFacingMessage()` скрывает реальные ошибки API | FIXED |
| BUG-003 | Пароли в `rememberSaveable` (persisted state) | FIXED |
| BUG-005 | Сессия не сбрасывается при 401 — UI остаётся «авторизованным» | FIXED |

#### P1 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-002 | `updateTransaction` хардкодит сумму и описание | FIXED |
| BUG-004 | Архивированные счета/категории видны в QuickAdd | FIXED |
| BUG-010 | `parseSession` игнорирует displayName пользователя | FIXED |

#### P1 — Открытые

| ID | Описание | Статус |
|----|----------|--------|
| BUG-006 | AddAccountSheet всегда создаёт shared-счёт | OPEN |
| BUG-007 | Нет защиты от double-tap на деструктивные действия | OPEN |
| BUG-008 | Удаление транзакции без подтверждения | OPEN |
| BUG-009 | Суммирование мультивалют без конвертации | OPEN |
| BUG-023 | `quickAddCategoryFor` молча подменяет выбор | OPEN |

#### P2 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-011 | FAB и кнопки TopAppBar видны неавторизованному | FIXED |
| BUG-012 | Кнопка «Подтвердить» активна без выбора счёта/категории | FIXED |
| BUG-015 | Несогласованность fallback-валюты RUB/USD | FIXED |
| BUG-016 | «Включить» вместо «Включено» для включённого элемента | FIXED |
| BUG-017 | editName не сбрасывается при отмене редактирования | FIXED |
| BUG-019 | captureSource отображается на английском | FIXED |
| BUG-022 | SignInCard мигает при загрузке авторизованного пользователя | FIXED |

#### P2 — Открытые

| ID | Описание | Статус |
|----|----------|--------|
| BUG-013 | HttpURLConnection никогда не disconnect() | OPEN |
| BUG-014 | Dashboard делает 4-6 последовательных запросов | OPEN |
| BUG-018 | AssetChips onClick не делает ничего | OPEN |
| BUG-020 | Избыточный запрос /sessions/current в dashboard() | OPEN |
| BUG-021 | Нет валидации формата email | OPEN |
| BUG-024 | restoreAccount/restoreCategory/restoreTransaction не вызываются из UI | OPEN |
| BUG-025 | Race condition между loadDashboard и loadCaptureDrafts | OPEN |

### API-аудит

| Проверка | Результат |
|----------|-----------|
| Все endpoint'ы существуют на backend | OK |
| HTTP-методы совпадают | OK |
| Имена полей JSON корректны | OK |
| Response parsing корректен | OK |
| Dashboard обрезает данные при >50 записях | WARN |
| CaptureDraft description nullable vs required | WARN |

### Русификация

| Метрика | Значение |
|---------|----------|
| Строк переведено | 44 |
| Непереведённых пользовательских строк | 0 |
| Сборка после русификации | OK |

### Тест-кейсы

| Модуль | Кейсов |
|--------|--------|
| AUTH | 14 |
| HOME | 11 |
| OPERATIONS | 9 |
| CAPTURE | 13 |
| ASSETS | 12 |
| CATEGORIES | 9 |
| ANALYTICS | 7 |
| QUICK-ADD | 16 |
| **Итого** | **91** |

### Сборка

| Параметр | Значение |
|----------|----------|
| APK | `artifacts/apk/finance-mvp-0.1.0-debug.apk` |
| Размер | 51.72 MB |
| URL | `http://45.10.110.42/finance-api` |
| Сборка | BUILD SUCCESSFUL |
| Дата | 2026-06-06 |

## Волна 2: Assets UI + account edit + backend account PATCH (2026-06-06)

**Метод:** targeted backend tests, Android debug build, `git diff --check`, runtime smoke на эмуляторе `Codex`.

**Scope:** Assets UI, редактирование счёта, backend `PATCH account`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Backend targeted tests | `22 passed, 1 warning` |
| Android build | `BUILD SUCCESSFUL in 57s` |
| Android build command | `assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` |
| `git diff --check` | exit 0, только CRLF warnings |
| Runtime smoke | APK установлен на `Codex`, `MainActivity` открыт |
| Эмуляторы | `Codex` использован; `Android1` не трогали |
| Account edit runtime flow | `NOT_RUN` — на `Codex` нет активных счетов/данных |

### Backend/API

| Проверка | Результат |
|----------|-----------|
| `PATCH account` payload | `name`, `currentBalance`, `currency`, `version` |
| `initialBalance` | Не меняется через PATCH |
| Optimistic conflict | `CONFLICTING_UPDATE` |
| Валюта счёта с транзакциями | `ACCOUNT_CURRENCY_IMMUTABLE_AFTER_TRANSACTIONS` |

### Android

| Область | Результат |
|---------|-----------|
| Assets category tap | expand/collapse группы |
| Edit group name | без refresh icon |
| Archive group accounts | long press >1s + confirmation |
| Account edit dialog | `name`, `balance`, `currency` |
| XAU | label `граммы`, icon gold bar |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Нет runtime proof для existing account edit flow | OPEN |
| Архивация группы может примениться частично, если последовательный `archiveAccount` упадёт | OPEN |
| Имя виртуальной группы хранится только в локальном UI state | OPEN |

## Волна 3: Аналитика -> Планирование MVP (2026-06-06)

**Метод:** full backend pytest, targeted planning/openapi/db tests, OpenAPI parse, Android debug build, runtime smoke на эмуляторе `Codex`, `dev_seed` smoke.

**Scope:** Planning MVP во вкладке Analytics, backend planning API/DB, Android planning UI и локальные reminders.

### Сводка

| Проверка | Результат |
|----------|-----------|
| `python -m pytest` | `224 passed`, 4 warnings |
| Targeted planning/openapi/db tests | `29 passed` |
| Android build | `BUILD SUCCESSFUL` |
| OpenAPI parse | OK |
| OpenAPI paths | `PATH_COUNT=37`, все planning paths присутствуют |
| `dev_seed` smoke | login 201, planning history 200, personal plan 200, без internal server error |
| `git diff --check` | pass, только LF/CRLF warnings |
| Runtime smoke | Planning screen открыт на `Codex`, показал следующий месяц/current plan/totals |
| Эмуляторы | `Codex` использован; `Android1` не targeted |

### Возможности

| Область | Результат |
|---------|-----------|
| Scope | personal + shared |
| Валюта | one currency |
| Income sources | `amount`, `source`, `dayOfMonth` |
| Reminders | local Android reminders per income |
| Confirm | обновляет только план, транзакции не создаёт |
| Allocations | expense categories, accounts, assets, investments |
| Allocation mode | `amount` или `percent` |
| Контроль заполнения | underallocated banner, overallocated warning |
| История | history/copy |
| Создание сущностей | category/account creation inherits scope |

### Backend/API

| Проверка | Результат |
|----------|-----------|
| Package | new planning package |
| DB tables | `planning_plans`, `planning_income_sources`, `planning_allocations` |
| Migration | `20260606_0010` |
| OpenAPI | planning endpoints добавлены |
| Authz personal | owner-only |
| Authz household | active-member |
| Totals | derived totals |
| Copy | attention rows |
| Validation | positive income validation |
| Seed/runtime | `dev_seed` planning runtime fix |

### Android

| Область | Результат |
|---------|-----------|
| API client | planning DTO/methods в `ApiClient` |
| UI | `PlanningUi` во вкладках Analytics |
| Notifications | `AlarmManager` + `BroadcastReceiver` |
| Permission | `POST_NOTIFICATIONS` |
| Explicitly excluded | без FCM/SMS/NotificationListener/exact alarm |
| Runtime | Codex smoke |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Exact visual/end-to-end creation flow только smoke-tested, не exhaustive manual scenario | OPEN |
| Local alarms reset if app force-stopped; boot/package replace covered | OPEN |
| `dev_seed` planning targets need sync if demo seed expands | OPEN |
| Past plans not strictly read-only at API level; history/copy implemented | OPEN |

## Волна 4: Planning asset target production release (2026-06-07)

**Метод:** full backend pytest, OpenAPI enum verification, Android unit/Kotlin/APK gate, backend-only production deploy, migration verification, production smoke через direct backend и nginx.

**Scope:** явный Planning `targetType=asset` на backend/OpenAPI/Android; миграция `20260607_0011_planning_allocation_asset_target.py`; Android выбор/создание asset/investment из planning flow; `.gitignore` hygiene для raw QA artifacts.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Code branch | `codex/finance-planning-mvp-gpt5` |
| Project commit | `5bb7ab493d7c3faa323d711ffa1febb2d94b4f7c` (`fix(planning): support asset allocation targets`) |
| KB previous commit | `b7729f9` |
| Backend full pytest | `228 passed, 4 warnings` |
| OpenAPI AllocationTargetType enum | `expense_category`, `account`, `asset` |
| Android gate | `:app:testDebugUnitTest :app:compileDebugKotlin :app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api --console=plain` -> `BUILD SUCCESSFUL` |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk` |
| APK size | `54235660` |
| APK SHA256 | `9E3814A5ABBBD1A9EFB8D484A94C973E4CA2598D21D921B990EE1DFCA568C6D8` |
| APK time | `2026-06-07 15:00:20 +03:00` |
| Production release | backend-only `20260607T121851Z-5bb7ab4`, `/opt/finance/releases/20260607T121851Z-5bb7ab4` |
| Current symlink | `/opt/finance/current` points to new release |
| Backup | `/opt/finance/backups/20260607T122105Z-59603b0/finance_prod.dump` |
| Backup SHA256 | `adbed3574f02a4fad94c41ac0fa2e18b4abe3e3cd21d527c3bf08cab04c1a8ae` |
| Migration before | `20260531_0009` |
| Migration applied | `20260531_0009 -> 20260606_0010 -> 20260607_0011` |
| Migration after | `20260607_0011 (head)` |
| Service status | active |
| Health smoke | `/health` direct and nginx OK |
| Auth smoke | unauth `sessions/current` -> 401 |
| Web frontend | не деплоился |
| Android delivery | APK delivered locally |

## Волна 5: Asset categories + Analytics/Planning polish (2026-06-07)

**Метод:** backend full pytest, fixtures tests, Android build gate, production deploy verification release agent.

**Scope:** asset categories как source of truth, Analytics investments/capital structure, Categories scope/edit icon, Planning income/allocation UX, backend `reportMode=personal`, asset-categories endpoints, миграция `20260607_0012`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Backend latest | `238 passed, 8 warnings` |
| Fixtures | `8 passed` |
| Android build | `BUILD SUCCESSFUL` |
| APK SHA256 | `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26` |
| Migration | `20260607_0012` |
| Project commit | `be9f8abe1abaed530c1dd503c5e631e935d8a3d5` |
| Production release | `20260607T163043Z-be9f8ab`, `/opt/finance/releases/20260607T163043Z-be9f8ab` |
| Current symlink | `/opt/finance/current` points to `/opt/finance/releases/20260607T163043Z-be9f8ab` |
| Backup | `/opt/finance/backups/20260607T163554Z-5bb7ab4/finance_prod.dump` |
| Backup SHA256 | `c7e38fae515b60b5d4b7d6588bbc8d03687d1769f222493ad240510f1f54b2d5` |
| Migration before | `20260607_0011` |
| Migration after | `20260607_0012 (head)` |
| Service status | active/running |
| Health smoke | direct 200, nginx 200 |
| Auth smoke | unauth `sessions/current` -> 401 |
| OpenAPI smoke | 200, asset categories routes present |
| Deploy | SUCCESS |
| APK final | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54235660`, SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26` |

### Backend/API

| Проверка | Результат |
|----------|-----------|
| Asset categories source of truth | `manualAmount` для пустых категорий; `isInvestment`; `assetType`; `account.assetCategoryId` |
| Deleted accounts | Не оставляют stale totals в агрегатах категорий активов |
| Asset categories endpoints | Добавлены и покрыты backend tests |
| Reports | Поддержан `reportMode=personal` |
| Migration | `20260607_0012` |

### Android/UI

| Область | Результат |
|---------|-----------|
| Analytics | Добавлена investments metric; структура капитала остаётся только в Analytics |
| Categories | Создание учитывает scope `personal`/`household`; редактирование через edit icon |
| Planning income | Income day трактуется как день месяца; форма дохода скрыта за Add |
| Planning allocations | Новые allocations выбирают expense category или investment asset category; account target для новых allocations не предлагается |
| Planning history | Текст истории уточнён |

## Открытые вопросы (NEEDS_CLARIFICATION)

1. Фильтрация категорий — какие типы доступны в каких режимах?
2. Transfer-фильтрация по режиму видимости
3. Ограничение длины имени категории/счёта
4. Restore без UI — как пользователь восстанавливает удалённое?
5. Мультивалютная конвертация — как отображать капитал?

## Волна 6: Release planning iteration MVP (2026-06-07)

**Метод:** OpenAPI parse/operationId audit, backend full tests, Android unit/build gate, production backend/web release verification, health/static checks.

**Scope:** финализация planning iteration MVP, production backend + web release `20260607T225457Z-819b5815`, Alembic `20260607_0013`, release evidence без лог-дампов.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project commit | `819b5815fed8c81bfa6a6e6131e790429454c2e8` (`Release planning iteration MVP`) |
| Project branch | `codex/finance-planning-mvp-gpt5` -> `origin` |
| Release id | `20260607T225457Z-819b5815` |
| Backend current | `/opt/finance/releases/20260607T225457Z-819b5815` |
| Web current | `/var/www/finance/releases/20260607T225457Z-819b5815` |
| Prod COMMIT files | оба указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8` |
| Alembic head | `20260607_0013 (head)` |
| Service status | `finance-backend.service` active |
| Health checks | `127.0.0.1:8081/health` OK; `/finance-api/health` OK |
| Web checks | `/finance/` 200; manifest scope/start_url `/finance/`; `/finance/sw.js` 200 |
| OpenAPI parse | OK |
| OperationId duplicates | `0/58` |
| Backend tests | `243 passed, 9 warnings` |
| Android unit | PASS |
| Android assembleDebug | PASS |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54,235,660`, SHA256 `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4` |

### Acceptance clarification

| Область | Решение |
|---------|---------|
| Planning progress | allocation-level: `PlanningAllocationDto.actualAmount`, `varianceAmount`, `status`, `attentionReason` |
| Plan DTO | не использовать plan-level `PlanningPlanDto.progress` |
| Previous month surplus | `previousMonthSurplus` находится в `PlanningSummaryDto` |

### Ограничения

| Риск | Статус |
|------|--------|
| Authenticated QA login/OCR smoke | `NOT_RUN` — нет operator password/session token |
| Production runtime checks | только health/static deploy checks |
| APK signing | debug-signed, не release-signed |

## Волна 7: newDis UX simplification release closure (2026-06-08)

**Метод:** sanitized release handoff, production frontend byte parity, backend health/route-surface waiver, Android unit XML/lint evidence.

**Scope:** release `newDis`, commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b` (`feat(finance): simplify newDis UX flows`). Commit меняет UI/test files; `apps/backend`, `db`, `api` не менялись.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis`, `HEAD = origin/newDis` |
| Project commit | `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Production frontend commit | `/finance/COMMIT` -> HTTP `200`, body `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Frontend static parity | `/finance/`, `/finance/sw.js`, manifest, JS/CSS byte-hash equal local `apps/web-pwa/dist` |
| Backend health | `/finance-api/health` -> HTTP `200`, body `{status:ok}` |
| Backend exact commit | Not directly proven: `/finance-api/COMMIT`, `/commit`, `/version` return `404`; waiver accepted |
| Android unit XML | 9 files, 60 tests, 0 failures, 0 errors, 0 skipped |
| Android lint | 0 errors, 6 warnings |
| APK | `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D`; superseded by Wave 8 production-path APK |
| Evidence note | [[Док_Release_NewDis_20260608]] |

### Ограничения

| Риск | Статус |
|------|--------|
| Full PWA install/service worker proof | OPEN — HTTP IP limits; нужен HTTPS/domain |
| Authenticated production login/OCR smoke | OPEN — не закрыто этой поставкой |
| Retention/privacy evidence | OPEN — не закрыто этой поставкой |
| APK signing | debug-signed, не release-signed |
| Historical reports | PWA Vitest, backend pytest `152 passed, 4 warnings`, OpenAPI redocly PASS и Android prod rerun старых commits — historical context only |
| Connected instrumentation stale failing XML | Не используется как green evidence |

## Волна 8: Android APK production API base correction (2026-06-08)

**Метод:** Android rebuild after prod-path fix, unit XML summary, APK string-content verification, production smoke without auth-sensitive payloads.

**Scope:** Android-only fix on branch `newDis`, project commit `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`). Project commit/push completed before this KB update; `/finance/COMMIT` remains web context `6ce31f53f6150050b4cb0dad8488254bd04ff31b` and is not a blocker for Android-only commit.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Android fix commit | `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3`, branch `newDis`, remote parity OK |
| Build/test command | `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` -> `BUILD SUCCESSFUL` |
| Unit XML summary | 9 XML files, 61 tests, 0 failures, 0 errors, 0 skipped |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54,235,660` |
| APK SHA256 | `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94` |
| Superseded APK SHA256 | `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D` retained `http://10.0.2.2:8000` and missed `/finance-api` |
| Superseded by | Wave 9 Android UX APK SHA256 `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` |
| APK content verification | PASS: contains `http://45.10.110.42/finance-api`; does not contain dev/local bases or duplicated `/api/v1` base |
| Production smoke | PASS: `/finance-api/health` -> HTTP `200` `{status:ok}`; protected current session and accounts endpoints -> HTTP `401` without auth |
| Known waiver | Plain HTTP remains accepted until HTTPS/domain |

### Ограничения

| Риск | Статус |
|------|--------|
| APK signing | debug-signed, не release-signed |
| HTTPS/domain | OPEN: plain HTTP waiver remains active |
| Authenticated production login/OCR smoke | OPEN: not covered by this Android prod-path correction |

## Волна 9: Android asset category UX fixes (2026-06-08)

**Метод:** post-review Android fix verification, unit gate, Kotlin compile gate, APK content verification. Без raw logs, raw screenshots, secrets и financial payload.

**Scope:** Android-only fixes after `newDis` UX closure: `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt` и `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project commit | `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`) |
| Remote parity | OK |
| Review result | P0/P1 clean after P1 fix |
| Unit gate | `:app:testDebugUnitTest` -> `BUILD SUCCESSFUL`; 61 tests, 0 failures/errors/skipped |
| Kotlin compile | `:app:compileDebugKotlin` -> `BUILD SUCCESSFUL` |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54,235,660` |
| APK SHA256 | `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` |
| APK content verification | Contains `http://45.10.110.42/finance-api`; no dev/local URLs found |

### UX fixes

| Область | Результат |
|---------|-----------|
| Recents/overview | Probable crash fixed через custom Saver для nullable `AddAccountState?` |
| Asset category edit | Явная edit icon; investment checkbox виден и сохраняется через existing update flow |
| AddAccountSheet keyboard | IME padding, scroll и BringIntoView держат focused fields выше клавиатуры |
| Category archive safety | Bulk archive gesture removed; trash action has confirmation; non-empty category archive blocked with instruction to move/delete accounts first; empty category archive calls backend category archive endpoint |
| Reorder | Long-press drag reorder for asset categories with local `SharedPreferences` persistence |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Recents/overview actual runtime | OPEN: emulator/device manual proof still recommended |
| Keyboard behavior on real device | OPEN: no visual IME proof available |
| Long-press drag gesture | OPEN: no emulator/device gesture proof available |
| Confirmation dialogs | OPEN: manual QA still recommended |

## Волна 10: Android final legacy asset edit + IME correction (2026-06-08)

**Метод:** final review, Android unit gate, Kotlin compile gate, debug APK build, APK content verification. Без raw logs, raw screenshots, secrets и raw financial payload.

**Scope:** финальная коррекция двух user misses после `newDis` Android UX fixes: legacy old asset group edit/conversion и account creation IME handling. Изменены `AndroidManifest.xml`, `ApiClient.kt`, `FinanceApp.kt`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project commit | `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`) |
| Remote parity | OK |
| Review result | P0/P1 clean |
| Unit gate | `:app:testDebugUnitTest` PASS; 61 tests, 0 failures/errors/skipped |
| Kotlin compile | `:app:compileDebugKotlin` PASS |
| APK build | `assembleDebug` PASS |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54,235,660` |
| APK SHA256 | `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B` |
| Superseded APK SHA256 | `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` |
| APK content verification | Production API base found x2; dev URLs absent |

### UX fixes

| Область | Результат |
|---------|-----------|
| Legacy asset edit | Legacy old asset group like `Вклад` now has `Инвестиция` checkbox in legacy edit dialog |
| Rename-only compatibility | Checkbox off keeps old rename-only behavior |
| Legacy investment conversion | Checkbox on converts legacy group to real asset category with `isInvestment=true` and links active legacy accounts |
| Conversion safety | Empty group, mixed-currency group and overview/no writable scope are blocked |
| Rollback safety | Link failure rollback uses updated account versions and archives created category |
| Account creation IME | `adjustResize`, `skipPartiallyExpanded`, `imePadding`, `navigationBarsPadding`, repeated `BringIntoView`, larger spacer |
| Material3 compatibility | `windowInsets` unavailable; compatible fallback used |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Visual IME behavior | OPEN: device/emulator manual proof still required |
| Live legacy migration | OPEN: device/emulator manual proof with real legacy group data still required |

## Волна 11: Compact investment asset categories + analytics fix (2026-06-08)

**Метод:** targeted backend pytest через project `.venv`, Android unit gate, Android debug APK build, APK content verification, integration review. Без raw logs, screenshots, secrets и raw financial payload.

**Scope:** compact investment asset category/card/edit UX, persisted category icon key and analytics parsing fix.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project commit | `09ea6479451c61b3d06a412e5aaaecec534fc96a` (`fix(finance): compact investment asset categories`) |
| Remote parity | OK |
| Backend targeted tests | `31 passed, 2 warnings` via project `.venv` pytest targeted suite |
| Android unit | `:app:testDebugUnitTest` successful |
| Android build | `:app:assembleDebug` successful |
| Integration review | P0/P1 clean; P2 staging risk handled by curated commit |
| APK | `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54,235,740` |
| APK SHA256 | `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733` |
| APK content verification | Prod API base present; dev URLs absent |

### Backend/API/Android

| Область | Результат |
|---------|-----------|
| Asset category icon | `asset_categories.icon_key` persisted through backend/API/Android |
| Icon picker | Android icon picker added for category edit flow |
| Compact card | `AssetCategoryGroupCard` compacted |
| Edit mode | Edit mode simplified; manual amount hidden when linked accounts exist |
| Linked accounts list | Removed from category edit and card |
| Investment badge | Investment badge uses trending-up icon |
| Analytics | Android forced currency filter removed; investment totals parsed from backend contract |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Compact card visual layout | OPEN: visual screenshot/device check still required |
| Edit mode visual behavior | OPEN: device/emulator manual proof still required |
| Icon picker UX | OPEN: device/emulator manual proof still required |
| Investment badge rendering | OPEN: visual screenshot/device check still required |

## Волна 12: Asset/planning regression fix evidence (2026-06-10)

**Метод:** post-plan KB/evidence capture from implementation, QA, packaging and review workers. Без raw logs, secrets, screenshots или financial payload.

**Scope:** Android regression fixes for asset category expanded rows, legacy `Карта`/`Банк` group visibility, category-level `isInvestment`, `План месяца` past-month handling, friendly planning empty state for missing plan 404, and Russian input diagnosis.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project commit | `1013e632d54c6af6ed9326d8b7f761bdd381bade` |
| Remote push | Completed before KB update |
| Review result | No P0/P1; P2 only for missing UI/Compose coverage |
| Kotlin compile | `.\gradlew.bat :app:compileDebugKotlin --console=plain` -> SUCCESS |
| Android unit | `.\gradlew.bat :app:testDebugUnitTest --console=plain` -> SUCCESS |
| Packaging unit gate | `.\gradlew.bat :app:testDebugUnitTest --console=plain` -> SUCCESS (`BUILD SUCCESSFUL in 2s`) |
| APK build | `.\gradlew.bat :app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api --console=plain` -> SUCCESS (`BUILD SUCCESSFUL in 36s`) |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54,235,740` |
| APK SHA256 | `FCD7EE0D870A12B3B88416DAEBCB3CF35FC513618C865B427E30E5F77F688411` |
| APK content verification | Prod URL `http://45.10.110.42/finance-api` found in `classes7.dex`, `classes5.dex`; dev URLs absent (`10.0.2.2`, `localhost`, `127.0.0.1`, `0.0.0.0`, `192.168.`) |
| Install smoke | AVD `Codex`, serial `emulator-5554`, package `com.finance.mvp`, install `Success` |

### Fix evidence

| Область | Результат |
|---------|-----------|
| Expanded asset category | Linked account rows restored; `Вклад` should show 4 linked accounts when expanded |
| Edit mode | Remains clean; no linked account list in edit mode |
| Legacy groups | Legacy asset group visibility for `Карта`/`Банк` restored without duplicates when real backend categories represent the type |
| Investment flag | Category-level `isInvestment` save/local state update fixed; marking `Брокер` investment updates badge/state and analytics inputs |
| План месяца | Months earlier than current are not selectable; persisted/selected past month clamps to current-or-future |
| Missing plan 404 | Raw `Resource not found or not accessible.` replaced by empty state / friendly planning message |
| Russian input | No app-level Cyrillic filter found; AVD `Codex` had `hw.keyboard=yes`, likely emulator/IME config |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Prod auth/DB data check | OPEN: no prod auth/DB access during data-check; live ids/archived/isInvestment values not independently verified read-only |
| Visual regressions | OPEN: no UI/Compose automated tests; manual visual QA recommended on installed APK |
| Russian input | OPEN: likely emulator settings, not app bug; workaround is Russian Android keyboard or `show_ime_with_hard_keyboard` / hardware keyboard off |

## Волна 13: Critical Android investment save regression closure (2026-06-12)

**Метод:** sanitized closure по build/unit evidence, final APK checksum, quick critical-path QA and fail-fast harness. Без raw auth, Bearer tokens, сырых payloads или секретов.

**Scope:** critical Android regression `Брокер -> Инвестиция -> Сохранить`. Root cause: Android отправлял `iconKey` в `POST /api/v1/asset-categories`, а deployed OpenAPI для `AssetCategoryCreateRequest` strict `additionalProperties=false`; backend возвращал validation failure до create/link. Fix: create payload больше не содержит `iconKey`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project commit | `d8175116f5123b6a304d4bd22dc083f2725505a0` (`fix(finance): migrate legacy brokerage assets`), pushed to `origin/newDis` |
| Modified project files | `FinanceApp.kt`; `AppSectionTest.kt`; `ApiClient.kt`; `ApiClientPlanningAllocationTest.kt` |
| Kotlin compile | `compileDebugKotlin` PASS, exit 0 |
| Android unit | `testDebugUnitTest` PASS, 71 tests, exit 0 |
| APK build | `assembleDebug` PASS, exit 0 |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54235740` bytes |
| APK SHA256 | `B6960DB5D13198405984C027746343432CB95B0C08BB24F54D6A7FCD5061DCC7` |
| Project summary | `MVP_EVIDENCE/critical-investment-fix-20260612/SUMMARY_SANITIZED.md` |
| Quick QA evidence | `MVP_EVIDENCE/critical-investment-qa-quick-20260612-013822/QA_REPORT_SANITIZED.md` |
| Harness evidence | `MVP_EVIDENCE/critical-investment-qa-harness-20260612-015225/HARNESS_REPORT_SANITIZED.md` |
| Live serial | `emulator-5556` |
| Secret scan | PASS; no raw auth/token evidence stored |

### Critical-path evidence

| Область | Результат |
|---------|-----------|
| Save flow | Assets -> Broker -> checked `Инвестиция` -> Save completed |
| Linked category | After save/restart, `assetCategoryId` and `linkedAssetCategory.id` present |
| Investment flag | `linkedAssetCategory.isInvestment=True` |
| Investment categories | `investmentCategories.count=1` |
| Totals | `150000.0000 RUB` after save and after restart |
| Regression signal | No `Validation failed` in final PASS evidence |
| Harness | Device selection, APK hash verification, install, launch and bounded UI probe PASS on `emulator-5556` |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Commit hash | RECORDED: `d8175116f5123b6a304d4bd22dc083f2725505a0` |
| APK signing | Debug-signed, not release-signed |
| Backend deploy | Not claimed; Android payload now matches deployed strict OpenAPI contract |
| Historical evidence | `critical-investment-qa-20260612-003254` FAIL and `critical-investment-qa-20260612-010747` stale/incomplete remain historical context only, not final PASS evidence |

## Волна 14: Date-only capture / Analysis QA plan (2026-06-12)

**Статус:** implementation in progress; pending final QA and commit. Это план покрытия, не final PASS report. Commit hash не заявляется.

**Project QA plan:** `MVP_EVIDENCE/reports/2026-06-12_date-only-capture-analysis-qa-plan.md`.

### P0 coverage

| ID | Область | Проверка | Статус |
|----|---------|----------|--------|
| P0-DATE-ANDROID-01 | Android manual date picker | Ручной выбор даты при create/edit операции, включая границы месяца; reports используют date-only без timezone drift | PLANNED |
| P0-DATE-PWA-01 | PWA manual date picker | Ручной date input в PWA сохраняет `transactionDate`, legacy timestamp нормализуется совместимо | PLANNED |
| P0-CAPTURE-01 | Capture confirmation | Перед confirm можно изменить amount/date; transaction получает отредактированные значения | PLANNED |
| P0-PAYMENT-01 | Payment account flag/filter | Expense/capture account selection исключает non-payment asset/investment accounts | PLANNED |
| P0-ANALYSIS-01 | Analysis month/category | Month switcher не смешивает месяцы; category aggregation корректна на date-only границах | PLANNED |
| P0-ANALYSIS-02 | Analysis investment history | Investment history не содержит stale/duplicate totals после broker/investment изменений | PLANNED |
| P0-MIGRATION-01 | Backend migration/API | Alembic migration/API/OpenAPI контракт проверены до release gate | PLANNED |
| P0-PROD-GATE-01 | Prod deploy gate | Миграция, health, PWA/static, Android prod base и authenticated QA smoke имеют явный PASS/waiver | PLANNED |
| P0-EMULATOR-01 | Emulator QA | Fresh install, selected serial, data clear, login and critical flows без stale-run confusion | PLANNED |
| P0-BROKER-01 | Broker investment regression | `Брокер -> Инвестиция -> Сохранить` повторно проходит после date/payment/report changes | PLANNED |

### P1 coverage

| ID | Область | Проверка | Статус |
|----|---------|----------|--------|
| P1-DATE-ANDROID-02 | Android date picker | Reopen/restart показывает persisted date-only value | PLANNED |
| P1-DATE-PWA-02 | PWA date picker | Refresh PWA не ломает locale/date display | PLANNED |
| P1-CAPTURE-02 | Capture confirmation | Частичные edits: только amount, только date, без edits | PLANNED |
| P1-PAYMENT-02 | Payment flag history | Toggle payment flag не ломает historical transactions, но исключает account из новых expenses | PLANNED |
| P1-ANALYSIS-03 | Analysis month switcher | Повторные переключения месяцев сохраняют totals/category rows/investment history consistent | PLANNED |
| P1-ANALYSIS-04 | Category aggregation scope | Одинаковые labels в разных scopes не смешивают недоступные данные | PLANNED |
| P1-MIGRATION-02 | Migration readiness | Backup/rollback gate зафиксирован до prod migration | PLANNED |
| P1-EMULATOR-02 | Emulator locale | Date input проверен с non-English locale settings where practical | PLANNED |

### Sanitization constraints

Не хранить raw OCR payloads, screenshots, UI XML, production financial data, UUIDs, Bearer/session tokens, cookies, passwords или secret values. Для QA account допускаются только safe aliases and out-of-band secret locator.

## Волна 15: Date-only capture / Analysis release closure (2026-06-12)

**Метод:** release/KB integration по sanitized backend/PWA/Android evidence, APK checksum, git status hygiene and secret scan. Raw screenshots, UI XML, raw OCR payloads, auth payloads, Bearer tokens, cookies, passwords and production financial payloads are excluded.

**Scope:** final status for date-only capture/analysis release after Android Metal manual amount fix; backend/PWA production deploys; safe QA account metadata; capture confirmation blocker routing.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project release integration commit | `5a59f29335d307931f94e561b5120750bbfd260b` (`fix(finance): stabilize android asset editing`), pushed to `origin/newDis` |
| Backend deployed commit | `26b487d61b7d2d6de704f0a632bcb08ff7f240f7` |
| Backend release | `/opt/finance/releases/20260612T045020Z-26b487d6` |
| Alembic | `20260607_0013 -> 20260612_0015` |
| Backend backup SHA256 | `6b48a4e8f73cbabeb40553eb052869c861bb2954edad0d960d3bbc7a34316ef8` |
| Backend smoke | health/OpenAPI/auth smoke PASS |
| PWA target | `http://45.10.110.42/finance/` |
| iPhone/browser PWA access | Open `http://45.10.110.42/finance/` in Safari/browser; optional Share -> Add to Home Screen. User term `PWE` interpreted as `PWA`; HTTPS/domain not claimed. |
| PWA release | `20260612T091555Z-26b487d61b7d` |
| PWA JS asset | `/finance/assets/index-BxFzW0Su.js` |
| PWA gates | npm test/build/nginx/public smoke PASS |
| Android final APK | `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk` |
| APK size | `54235740` bytes |
| APK SHA256 | `6AEE934A8817055B1738B32E1468D2A4C5415502C224115F9C7953F63EC3D893` |
| APK Git status | Local artifact only; `*.apk` intentionally ignored |
| Curated release report | `MVP_EVIDENCE/reports/2026-06-12_date-only_capture_analysis_release_SANITIZED.md` |
| Final Android evidence | `MVP_EVIDENCE/date-only-capture-analysis-qa-metal-fix-20260612-133358/QA_REPORT_SANITIZED.md` |
| PWA deploy evidence | `MVP_EVIDENCE/reports/2026-06-12_pwa_prod_deploy_SANITIZED.md` |
| Capture confirmation evidence | `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/QA_REPORT_SANITIZED.md`; previous blocker report retained as historical only |
| Secret scan | PASS for curated project/KB touched files; no real secrets found |

### PASS evidence

| Область | Результат |
|---------|-----------|
| Payment account filter | Expense account selection excludes non-payment asset/investment accounts; income remains broader |
| Date-only / Analysis | Date-only analysis/report release evidence accepted as PASS after final Android regression closure |
| Asset edit dialogs | Broker/Card edit dialogs have no icon picker and no manual amount field for account-backed groups |
| Legacy `Металл` | Manual-only legacy Metal now exposes `Ручная сумма`, saves manual amount, reopens with saved value, and has no icon picker |
| Broker/Card negative checks | Account-backed Card and Broker remain without manual amount and without icon picker |
| Android build/tests | Focused JVM, full Android JVM, and debug APK build PASS in final Metal fix report |
| PWA deploy | Production PWA release switched and public smoke PASS |
| Backend deploy | Production backend release/migration/smoke PASS |

### Historical evidence

| Evidence | Статус |
|----------|--------|
| `MVP_EVIDENCE/date-only-capture-analysis-qa-final-D401-20260612-130029/QA_REPORT_SANITIZED.md` | Historical FAIL for Metal before fix; retained for regression history only |
| `MVP_EVIDENCE/date-only-capture-analysis-qa-metal-fix-20260612-133358/QA_REPORT_SANITIZED.md` | Final PASS source for Metal/manual amount/no icon picker closure |

### Capture confirmation

| Область | Статус |
|---------|--------|
| Live Android confirmation edit amount/date and confirm | PASS by Wave 16 escalation |
| Escalation report | `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/QA_REPORT_SANITIZED.md` |
| Escalation secret scan | PASS/finding_count `0` |
| Previous blocker report | `MVP_EVIDENCE/date-only-capture-confirmation-qa-20260612-100149/QA_REPORT_SANITIZED.md`, historical only |
| Backend focused coverage | `26 passed, 1 warning` |
| Android focused JVM coverage | `BUILD SUCCESSFUL` |
| Live UI proof | Pending row shown, amount/date edited, `Подтвердить` removed draft row, Operations showed edited backend-backed amount/date |

### Safe QA account metadata

| Environment | Safe alias / identifier | Purpose | Secret handling |
|-------------|-------------------------|---------|-----------------|
| Production QA | `finance.qa@local.test` | Owner-operated production smoke and authenticated QA flows | Password value is never stored. Locator only: `/etc/finance/qa-owner.env`, key `FINANCE_QA_PASSWORD`. |
| Development | `demo.owner@example.test` | Local/dev seeded flows and emulator/PWA development checks | No passwords, tokens, cookies, or sessions are stored. |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Capture confirmation live Android proof | CLOSED by Wave 16 escalation PASS |
| APK signing | Debug-signed, not release-signed |
| Raw evidence | Intentionally local/ignored; only curated sanitized Markdown/JSON should be committed |

## Волна 16: Capture confirmation escalation closure (2026-06-12)

**Метод:** sanitized escalation closure после release integration commit. Без raw screenshots, UI XML, raw OCR payloads, auth payloads, Bearer tokens, cookies, passwords или secret values.

**Scope:** live Android capture confirmation UI: edit amount/date before confirming a screenshot-derived pending draft.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Project branch | `newDis` |
| Project release integration commit before escalation | `5a59f29335d307931f94e561b5120750bbfd260b` (`fix(finance): stabilize android asset editing`), pushed to `origin/newDis` |
| Project capture closure docs commit | `a9f143e37515b53cc617165621ebf1708e0b0ee4` (`docs(finance): record capture confirmation pass`), pushed to `origin/newDis` |
| Escalation evidence | `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/QA_REPORT_SANITIZED.md` |
| Escalation secret scan | `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/secret_scan_summary.json`, PASS/finding_count `0` |
| Live serial | `emulator-5554` |
| APK SHA256 | `6AEE934A8817055B1738B32E1468D2A4C5415502C224115F9C7953F63EC3D893` |
| Backend focused tests | `26 passed, 1 warning` |
| Android focused JVM tests | `BUILD SUCCESSFUL` |
| Final capture confirmation status | PASS |

### Live proof

| Область | Результат |
|---------|-----------|
| Pending draft | Live Android UI showed a pending capture confirmation row |
| Amount edit | Amount changed to `45.67` before confirmation |
| Date edit | Operation date changed to `2026-06-11` before confirmation |
| Confirm | After `Подтвердить`, the pending row disappeared |
| Operations refresh | Operations showed the edited amount/date from the refreshed backend-backed dashboard |

### Historical evidence

| Evidence | Статус |
|----------|--------|
| `MVP_EVIDENCE/date-only-capture-confirmation-qa-20260612-100149/QA_REPORT_SANITIZED.md` | Historical pre-escalation `BLOCKED_CAPTURE_FIXTURE`; no longer final release status |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Fresh login from credentials | NOT_CLAIMED: escalation used an existing authenticated Android app session |
| Deterministic repeatability | FUTURE_HARDENING: test-only seed/deep link or documented parseable OCR fixture remains useful |
| APK signing | Debug-signed, not release-signed |

## Волна 17: Offline-first release QA closure (2026-06-18/2026-06-19)

**Метод:** sanitized closure по GitHub Actions green run, package test counts, локальному Android emulator E2E PASS и release-blocker remediation summary. Raw logs, raw OCR payloads, screenshots, APK/build artifacts, auth payloads, Bearer tokens, cookies, passwords and secret values are excluded.

**Scope:** offline-first release QA для branch `codex/offline-first-release-qa`; backend/frontend package gates; FastAPI route introspection compatibility; deploy readiness boundary.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Branch | `codex/offline-first-release-qa` |
| GitHub Actions run | `27796358035` |
| Head | `b09043e531152bb5f9b2fdb6ef18b21d786bbebf` |
| Release id | `20260618T234841Z-b09043e5` |
| Frontend package | `56 passed` |
| Backend package | `285 passed, 6 skipped` |
| Local emulator E2E | PASS |
| Local E2E evidence | `MVP_EVIDENCE/offline-first-release-qa-20260618-234050/QA_REPORT_SANITIZED.md` |
| PR | `https://github.com/DmtrGoltsev/finance/pull/1` |
| Merge status | VERIFIED: PR #1 merged at `2026-06-18T23:53:47Z`; remote `main` HEAD = merge commit `cff578df0be001c0af187c5a90d9917fc0b2c1e9`; parents `3f70a3bf...` + release head `b09043e5...` |
| Workflows on `main` | VERIFIED: workflow files present; active `Finance HexCore Production CI/CD` id `298526666`, `Finance Production Manual Rollback` id `298581092` |

### Release blockers fixed

| Blocker | Closure |
|---------|---------|
| Backend ruff gate | Fixed before green CI |
| FastAPI route introspection | Updated for FastAPI `0.137.2` via `iter_route_contexts` |
| Backend dependency drift | Pinned `fastapi==0.137.2`, `starlette==1.3.1` |

### Production deploy boundary

| Gate | Статус |
|------|--------|
| Production deploy | Historical QA-wave boundary superseded by final production CI/CD state 2026-06-19; current status PASS |
| Public health | PASS: backend health PASS, frontend PASS |
| `workflow_dispatch` readiness | Superseded by final production CI/CD state 2026-06-19 |
| Raw evidence handling | Raw logs/OCR/screenshots/APK/build artifacts intentionally not copied into KB |

## Волна 18: Native iOS parity static QA closure (2026-06-19)

**Метод:** sanitized docs/source inventory по текущей native iOS ветке. Raw logs, raw screenshots, APK/build artifacts, `.xcresult`, OCR payloads, cookies, CSRF, passwords, tokens and secret values are excluded.

**Scope:** native-only iOS parity branch `codex/IOS` в `C:\Users\style\Documents\Codex\Финансы-ios`; base `origin/main` commit `66feadd94dbf936faec500f565638973ca270f64`. PWA/Capacitor wrapper under `apps/web-pwa` не является parity target.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Native-only target | PASS: целевой клиент `apps/ios` SwiftUI/UIKit; PWA/WebView wrapper не заявлен как parity |
| Implemented scope | API config hardening/Release guard; auth/register/session/logout wipe; manual date-only/payment filter fallback; capture editable amount/date online-only; assets/investment/icon preservation; analytics month/category/investments; planning fallback; icon-only tabs; local JSON store/sync queue/manual sync/issues/Russian sync UI |
| Windows static QA | PASS |
| FAIL | None recorded |
| BLOCKED | Mac/Xcode gates only: `swift`, `xcodebuild`, `xcodegen` unavailable |
| Future gates | XcodeGen, Debug/Release build, simulator/device flows, Keychain/cookie wipe, offline queue backend push/pull, OCR/copy online-only UX |
| Evidence handling | Sanitized summary only; no secrets/raw logs/screenshots/APK/evidence binaries copied |

## Production QA persistent account (2026-07-11)

**Status:** ACTIVE / PERSISTENT / NEVER DELETE.

Credential boundary superseded on 2026-08-22 by explicit vault-owner instruction:
use [[QA_Учетная_Запись_Production_20260822]]. Do not copy credentials into the
project repository, release evidence, logs or chat output. Tokens, cookies,
session IDs, Bearer values, OCR raw payloads, screenshots and production
financial data remain prohibited here.

| Field | Value |
|-------|-------|
| Environment | production |
| Production API base | `http://45.10.110.42/finance-api` |
| Purpose | Android/PWA/API QA; Android prod E2E; PWA prod smoke; authenticated production smoke |
| Retention | NEVER DELETE / persistent test account |
| Cleanup | Do not delete unless owner explicitly requests |
| Display name | `Finance Production QA Persistent Test Account - NEVER DELETE` |
| Email / login | `finance.qa.prod.20260711.6cb15851@local.test` |
| Password | Not stored in KB; use the owner-managed production QA credential store |
| Transport | `android_bearer` |
| Registration endpoint | `POST http://45.10.110.42/finance-api/api/v1/users` |
| Registration result | HTTP `201` on 2026-07-11 |
| Login endpoint | `POST http://45.10.110.42/finance-api/api/v1/sessions` |
| Login result | HTTP `201` on 2026-07-11; access token present in API response and deliberately not stored |

Search tags / keywords: Finance Production QA account; persistent production test account; NEVER DELETE; qa login; Android prod E2E; PWA prod smoke; Finance Production QA Persistent Test Account - NEVER DELETE; finance.qa.prod.20260711.6cb15851@local.test.

## Волна 19: Android Assets / Investment quick add QA closure (2026-07-12)

**Метод:** sanitized closure по Android targeted/full unit gates, backend targeted sync/planning gates, release APK signing checks and emulator smoke. Raw logs, screenshots, UI XML, tokens, cookies, passwords and production financial data are excluded.

**Scope:** Android вкладка `Активы`, quick add type `Инвестиция`, investment allocation actual semantics, local/offline sync payload handling for explicit `categoryId:null`, deploy boundary for backend sync changes.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Android Assets title layout | PASS: category titles no longer collapse to `Б...`/`Вк...`; counter does not wrap by letters; amount/`Править` no longer break title |
| Android quick add `Инвестиция` | PASS: creates investment operation as `transactionType=asset_buy`, `categoryId=null`, with date/amount input |
| Account filtering | PASS: investment quick add offers only accounts linked to investment asset category |
| Planning/Analytics refresh | PASS: after save, plan/analytics refresh path covered; `Факт` for `Вклад`/`Брокер` should count in `Аналитика -> План месяца` |
| Backend domain semantics | PASS in targeted tests: investment allocation actual counts categoryless `brokerage`, `asset_buy`, `interest`, `dividend`, `adjustment` on linked investment accounts; `expense`/`transfer` excluded |
| Local sync explicit null | PASS: explicit `categoryId:null` preserved; backend sync allowlist locally extended for investment types |
| Android targeted tests | PASS: `SyncManagerTest`, `ApiClientCaptureDraftTest`, `AppSectionTest`, `PlanningUiStatusTest` |
| Android full unit suite | PASS: `:app:testDebugUnitTest` |
| Backend sync pytest | PASS: `21 passed` |
| Backend planning/transactions/reports targeted | PASS: `30 passed` |
| Lint/style | PASS: ruff sync files |
| Release APK | PASS: `assembleRelease` with prod URL, `apksigner` |
| Emulator smoke | PASS: `emulator-5554` install/smoke for Assets and Analytics |
| Backend production deploy | NOT_DONE: requires GitHub Actions release branch; blocked by release scope/protection checklist; no SSH/SCP |

### APK / evidence

| Artifact | Value |
|----------|-------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260712-112532-POSTP2-manual-install.apk` |
| SHA256 | `cace0eb69e589f8eb0be579a0a4bc83039013d35a29d74e32547367449ee4d79` |
| Evidence folder | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-assets-investment-postp2-qa-20260712-112610` |

### Deploy boundary

| Gate | Статус |
|------|--------|
| Online direct investment operation | Expected to use existing transactions API for `asset_buy` |
| Offline sync of investment operation | BLOCKED until production backend deploy through GitHub Actions release branch |
| Release protection | BLOCKED by release scope/protection checklist |
| Direct SSH/SCP | NOT_USED / NOT_CLAIMED |

## Волна 20: Android transfer assets / ordering QA closure (2026-07-12)

**Метод:** sanitized closure по Android targeted/full JVM gates, backend targeted regression tests, PWA targeted ordering/build gates, final release APK signing/hash and `emulator-5554` install/smoke. Raw logs, screenshots, UI XML, tokens, cookies, passwords and production financial data are excluded.

**Scope:** transfer quick add date handling, Android/PWA newest-first operation ordering, asset totals after transfer into investment-linked account, backend account sync changes for transfer source/destination, planning/report semantics that keep `transfer` out of investment actual.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Android transfer quick add date | PASS: transfer quick add shows date picker and sends `transactionDate` |
| Android Operations ordering | PASS: `Операции` tab sorts newest-first |
| Android asset totals after transfer | PASS expectation covered: asset categories compute totals from fresh `dashboard.accounts.currentBalance` by `assetCategoryId` |
| Backend transfer account sync | PASS in targeted tests: transfer REST/sync push emits `accounts/update` for source and destination |
| Planning semantics | PASS: `transfer` changes balances/assets but does not count as investment actual; `asset_buy` remains investment actual |
| PWA ordering | PASS: `recentTimeline` newest-first; Overview/Operations show newer operations above older ones |
| Sync pull order | NOT_CHANGED: pull remains ordered by `seq` as cursor protocol |
| Android targeted/full | PASS |
| Backend targeted regression | PASS: `49 passed` |
| Lint/style | PASS: `ruff` |
| PWA targeted ordering/build | PASS |
| PWA broader `App.test` | KNOWN_RESIDUAL: 2 date-sensitive failures around June 2026 |
| Emulator smoke | PASS: `emulator-5554` install/smoke without changing data |
| DB migration | NOT_REQUIRED |
| Backend production deploy | REQUIRED: prod account sync behavior needs GitHub Actions release branch deploy |

### APK / evidence

| Artifact | Value |
|----------|-------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260712-220221-POSTP1-TRANSFER-manual-install.apk` |
| SHA256 | `B4AF3B3CF30E77F5C22075B9EFC47D82CBBF5FBCDDF5356D286F37DDEB3209C6` |
| Evidence folder | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-transfer-assets-ordering-postp1-qa-20260712-215452` |

### Deploy boundary

| Gate | Статус |
|------|--------|
| Android APK prod URL | PASS: APK points to production API URL |
| Backend account sync changes in prod | NOT_DEPLOYED: requires GitHub Actions release branch deploy |
| DB migration | NOT_REQUIRED |
| Direct SSH/SCP | NOT_USED / NOT_CLAIMED |

## Wave 21: Android auth/session QA closure (2026-07-25)

**Method:** sanitized documentation update from completed auth/session QA evidence. Raw logs, screenshots, OCR payloads, cookies, tokens, passwords, secret values and production financial data are excluded.

**Scope:** Android AuthGate separation, encrypted local session bundle, refresh-token retry path, OCR refresh/retry behavior, backend refresh endpoint and refresh-token rotation semantics.

### Summary

| Check | Result |
|-------|--------|
| Android signed-out/restoring UI | PASS: signed-out/restoring show separate AuthGate without TopAppBar, NavigationBar, FAB or protected tabs |
| Android signed-in UI | PASS: main tabs render only in signed-in state |
| Android session storage | PASS: `SessionTokenBundle` stored in `EncryptedSharedPreferences` with `accessToken`, `refreshToken`, `expiresAt`, `userId`; password not stored |
| API client login/register | PASS: token bundle persisted after login/register |
| API client refresh/retry | Historical wave result superseded on 2026-08-22: current Android refreshes once on `401`; `403` preserves session |
| Logout/auth failure handling | PASS: logout or refresh/auth failure clears local token store and protected UI |
| Screenshot OCR auth handling | PASS: OCR path refreshes/retries once on auth failure |
| Backend refresh endpoint | PASS in local/backend QA: `/api/v1/sessions/refresh` added |
| Backend token rotation | PASS: `android_bearer` login/register return `refreshToken`; refresh rotation is hash-only, invalidates old refresh token, logout invalidates refresh session, CAS atomic rotation covered |
| DB migration | NOT_REQUIRED |
| Security review | PASS: P0/P1/P2 none after fixes |
| Backend auth tests | PASS: `71 passed` |
| Backend style | PASS: `ruff` passed |
| Android full unit | PASS |
| APK build/sign/verify | PASS |
| Emulator manual install/smoke | SKIPPED: emulator unavailable |

### APK / evidence

| Artifact | Value |
|----------|-------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260725-231110-AUTH-SESSION-manual-install.apk` |
| SHA256 | `F9ABD3D02D64A06FCB5E78731AC313FD8230165CF9BC8D427E2FED92466BB8A0` |
| Evidence folder | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-auth-session-qa-20260725-231110` |

### Deploy boundary

| Gate | Status |
|------|--------|
| Android APK prod URL/session storage | READY for manual install after QA caveats |
| Backend refresh endpoint in production | DEPLOYED on 2026-07-25 through GitHub Actions backend-only deploy |
| Without backend deploy | Historical pre-deploy caveat; superseded by Wave 22 deploy record |
| Direct SSH/SCP | NOT_USED / NOT_CLAIMED |

## Wave 22: Backend auth refresh production deploy (2026-07-25)

**Method:** sanitized deploy documentation from completed GitHub Actions backend-only production deploy and production smoke. No tokens, passwords, cookies, session values, raw logs or production financial data are stored.

**Scope:** production backend deployment of `/api/v1/sessions/refresh` and refresh-token rotation behavior for Android long-lived sessions.

### Summary

| Check | Result |
|-------|--------|
| Branch | `prod/finance-auth-refresh-20260725` |
| Commit | `9e1ed7903798ed4f1edbcfeb3d98b23ec9ae0763` |
| Release ID | `finance-backend-auth-refresh-20260725-9e1ed79` |
| Actions run | `https://github.com/DmtrGoltsev/finance/actions/runs/30174265210` |
| Workflow status | `completed/failure` because unrelated `frontend-ci-package`/PWA tests failed |
| Deploy dispatch | PASS: backend-only; `deploy-frontend` skipped |
| Backend deploy job | PASS |
| Health | PASS: `http://45.10.110.42/finance-api/health` -> 200 `{"status":"ok"}` |
| Refresh route mounted | PASS: `/finance-api/api/v1/sessions/refresh` returns 422 on empty payload |
| Refresh smoke | PASS: registration 201, refresh 200, token fields present, refresh rotated, old refresh rejected 401 |
| Backend artifact checksum | `da77996a82489e1732a77686eda2965b6f51113d8528828151927ca42b384491` |
| DB migration | NOT_RUN / NOT_REQUIRED: `run_migrations=false` |
| Workflow backup | NOT_CREATED because migrations were not run |
| Direct local SSH/SCP | NOT_USED |
| Staged files | PASS: exactly allowed auth/OpenAPI backend list |
| Evidence hygiene | PASS: no tokens/passwords in evidence |

### Caveat

Workflow emails may say failed due to the unrelated frontend job. The backend deploy is successful.

## Wave 23: Android category search and analytics POSTP2 QA closure (2026-07-26)

**Method:** sanitized documentation update from Android-only category/analytics POSTP2 evidence. Raw logs, screenshots, tokens, cookies, passwords, session values and production financial data are excluded.

**Scope:** Android expense category picker/search UX, category dialog state isolation, top categories filtering, investments summary mapping. Backend deploy was not required because the production API already returns `investmentsByCurrency[*].investmentsTotal`.

### Summary

| Check | Result |
|-------|--------|
| Expense category quick search | PASS: add/confirm expense flows support text search by word part |
| Category picker UX | PASS: horizontal category lists in add/confirm expense flows replaced by `Категория` button opening overlay/dialog with vertical scroll and search |
| Analytics investments summary | PASS: `Анализ -> Сводка -> Инвестиции` on Android fills investment total from `investmentsByCurrency` with summary fallback |
| Home top categories all button | PASS: `Главная -> Топ категории` has `Все`, opening all expense categories sorted by descending amount |
| P2 top categories filtering | PASS: top categories use expense categories only and drop expense transactions whose `categoryId` points to income/asset category |
| P2 category dialog state | PASS: search state is key-based and does not leak between rows/modes |
| Android targeted unit gate | PASS: `AppSectionTest`, `ApiClientDashboardTest`, `ApiClientAuthRefreshTest`, `FinanceSessionRestoreTest` |
| Android full unit gate | PASS: `.\gradlew.bat :app:testDebugUnitTest` |
| Kotlin compile | PASS: `.\gradlew.bat :app:compileDebugKotlin` |
| Release assemble | PASS: `.\gradlew.bat :app:assembleRelease -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` |
| APK signing/alignment | PASS: `zipalign`, `apksigner verify --verbose --print-certs`, final `zipalign -c` |
| URL scan | PASS: prod markers `45.10.110.42` and `finance-api` present; local markers `10.0.2.2`, `localhost`, `127.0.0.1` absent |
| Emulator/manual e2e | SKIPPED: `adb devices` returned no attached devices; install/launch/manual e2e not run |
| Production data | NOT_CHANGED: real production data was not modified |

### APK / evidence

| Artifact | Value |
|----------|-------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260726-160500-CATEGORY-ANALYTICS-POSTP2-manual-install.apk` |
| SHA256 | `188eae471e36f1cdfe2e4f92ce1f7da7e5fa1d1febb9c80ab5a96c494503d0b1` |
| Evidence summary | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-category-analytics-postp2-qa-20260726-160224\SUMMARY.md` |

### Deploy boundary

| Gate | Status |
|------|--------|
| Backend deploy | NOT_REQUIRED: Android mapping/UI-only change for investments analytics; API already returns `investmentsByCurrency[*].investmentsTotal` |
| Android APK prod URL | READY for manual install after QA caveat |
| Manual install/launch | NOT_RUN because emulator/device was unavailable |

## Wave 24: Monthly investment transfers reports/Android QA closure (2026-07-26)

**Method:** sanitized documentation update from local backend/Android QA evidence. Raw logs, screenshots, tokens, cookies, passwords, session values and production financial data are excluded.

**Scope:** `/reports/summary.investmentsTotal` business semantics and Android Analytics summary investments source. Backend production deploy is required before the new backend behavior is production-active.

### Summary

| Check | Result |
|-------|--------|
| Business rule | PASS documented: `summary.investmentsTotal` means visible incoming `transfer` operations for the selected period/month into investment asset accounts/categories; it is not total asset balance |
| Account balances boundary | PASS documented: `/reports/account-balances` remains the asset/account balance endpoint |
| Android summary source | PASS: Analytics summary investments uses summary data only and does not fallback from account-balances |
| Backend targeted reports/assets | PASS: `25 passed, 8 warnings` |
| Backend full pytest | PASS: `302 passed, 16 warnings` |
| Android targeted unit gate | PASS: `ApiClientDashboardTest`, `AppSectionTest` |
| Android full unit gate | PASS: `.\gradlew.bat :app:testDebugUnitTest`; XML total `174 tests, 0 failures, 0 errors, 0 skipped` |
| Kotlin compile | PASS: `.\gradlew.bat :app:compileDebugKotlin` |
| Release assemble | PASS: `.\gradlew.bat :app:assembleRelease -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` |
| APK signing/alignment | PASS: `zipalign`, `apksigner verify --verbose --print-certs`, final `zipalign -c` |
| URL scan | PASS: APK binary contains `45.10.110.42` and `finance-api`; no `localhost`, `10.0.2.2`, `127.0.0.1` markers |
| Emulator/manual smoke | SKIPPED: `adb` not in PATH; SDK adb available but no attached devices/emulator |
| Production deploy/data | NOT_DONE/NOT_CHANGED: this worker did not deploy production and did not mutate real production data |

### APK / evidence

| Artifact | Value |
|----------|-------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260726-221828-MONTHLY-INVESTMENT-TRANSFERS-manual-install.apk` |
| SHA256 | `46e85ee4e5c6b4b13cf84abd4da22dcffc2642d0e9afd7d6be16f5c40783a9ca` |
| Evidence summary | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\monthly-investment-transfers-qa-20260726-221828\SUMMARY.md` |

### Deploy boundary

| Gate | Status |
|------|--------|
| Backend production deploy | REQUIRED: production `/reports/summary.investmentsTotal` needs backend deploy for monthly incoming investment transfer semantics |
| Android APK prod URL | READY for manual install after QA caveat |
| Manual install/launch | NOT_RUN because emulator/device was unavailable |

## Wave 25: PWA iPhone browser parity post-fix QA closure (2026-07-27)

**Method:** sanitized local PWA QA evidence after `TopCategoriesDialog` portal/layer fix. Raw logs, tokens, cookies, passwords, session values and production financial data are excluded. Screenshots remain in project evidence, not copied into Obsidian.

**Scope:** server-first PWA iPhone browser parity smoke for login, home, quick add, category overlay, analytics and top categories all. Backend code was not changed in this PWA parity task.

### Summary

| Check | Result |
|-------|--------|
| PWA unit tests | PASS: `npm.cmd test` in `apps/web-pwa`, 4 files, 65 tests |
| PWA build | PASS: `npm.cmd run build`, `tsc -b && vite build`, 1704 modules |
| Local Vite | PASS: `npm.cmd run dev -- --port 5173`, `http://127.0.0.1:5173/` |
| Login/home iPhone smoke | PASS: no horizontal overflow, mobile FAB and bottom nav hit-test in viewport |
| Quick add sheet | PASS: sheet and submit controls remain reachable on iPhone viewport |
| Category picker overlay | PASS: searchable vertical overlay visible and hit-testable |
| Analytics | PASS: 4 metric cards visible/reachable by scroll |
| Top categories all | PASS: server breakdown path used, no fallback warning |
| TopCategoriesDialog stacking | PASS: dialog overlays FAB and bottom nav by `elementFromPoint` hit-test |
| TopCategoriesDialog scroll | PASS: inner `.listStack` scrolls inside dialog, `clientHeight=570`, `scrollHeight=2594`, `after=2024` |

### Evidence

| Artifact | Value |
|----------|-------|
| Evidence summary | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\pwa-iphone-parity-postfix-qa-20260727-005600\SUMMARY.md` |
| Smoke JSON | `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\pwa-iphone-parity-postfix-qa-20260727-005600\iphone-parity-smoke.json` |
| Screenshots | `screenshots/01-login.png` through `screenshots/07-top-categories-all-scrolled.png` |

### Residual risks

Real iPhone/Safari manual run was not performed. Production HTTPS/secure-cookie behavior remains a risk if production is served only as plain HTTP IP. PWA/iOS OCR remains online-only and was not re-tested in this parity smoke.

## Wave 26: Personal-only/native iOS final regression (2026-08-21)

**Scope:** финальная доступная регрессия branch
`codex/ios-native-personal-parity-20260820`, commit
`96aa58226ad8f80834ea333192ebace7885d69c2`. Commit/push/deploy этим QA/docs
worker не выполнялись.

| Gate | Result |
| --- | --- |
| Backend full pytest | PASS: 296 passed, 6 skipped, 13 deprecation warnings |
| Backend Ruff | PASS: all checks passed |
| Android full unit | PASS: 143 tests, 0 failures/errors/skipped |
| Android assembleDebug | PASS; debug V2-signed APK generated |
| Android assembleRelease | PASS; unsigned release APK generated and verified unsigned |
| PWA `npm ci` | PASS |
| PWA tests | PASS: 4 files, 69 tests |
| PWA production build | PASS |
| PWA `npm audit --omit=dev` | PASS: 0 runtime vulnerabilities |
| Service worker/HTTP guards | PASS: 5/5; plain HTTP IP registration skipped; API/OCR not cached |
| GitHub iOS run | PASS: `32523201106`, exact branch/commit |
| Native iOS Debug/Release | PASS: both `BUILD SUCCEEDED` |
| Native iOS XCTest/UI | PASS: 47/47 + 1/1 |
| Personal-only runtime/API scan | PASS for reachable behavior |
| Categories | PASS: `Категории расходов`, expense-only list/create, no mode selectors |

GitHub evidence artifact: `ios-build-test-evidence-32523201106`, id
`9461389241`, digest
`sha256:df99fa5b33d6292f84adf010f5e6ad5fa170cca5d4431100a80734cb129fff6b`.
Bulky `.xcresult` не копировался в Vault/repo evidence.

Sanitized evidence:
`MVP_EVIDENCE/personal-native-ios-final-regression-20260821-234120/SUMMARY_SANITIZED.md`.
Test cases: [[QA_ТестКейсы_Native_iOS_Personal_20260821]].

**Статус:** native iOS code/CI ready. Actual prod login на физическом iPhone
BLOCKED до выбора trusted HTTPS API endpoint; arbitrary ATS exception запрещён.
Допустимы собственный домен с trusted TLS либо trusted short-lived Let's Encrypt
IP certificate. Legacy Capacitor не является target native app.

Persistent production QA account: использовать locator из
[[QA_Результаты#Production QA persistent account (2026-07-11)]], `NEVER DELETE`;
credentials for the current reusable account are stored only in
[[QA_Учетная_Запись_Production_20260822]].

## Wave 27: Android production release (2026-08-22)

**Scope:** secure persistent Android session, account-isolated offline sync,
selected-month investment transfers, newest-first operations, searchable category
dialog, payment-account refresh, transfer date and compact analytics month switcher.

| Gate | Result |
| --- | --- |
| Final source | PASS: `43f4b1780e3bdcf6891b877fe03ee53971f74500` |
| Android unit | PASS: `167/167`, no failures/errors/skips |
| Android lint | PASS: `0` errors |
| APK install | PASS on `emulator-5554` |
| Session persistence | PASS after production login and force-stop/relaunch |
| Investment transfer | PASS for selected-month incoming transfer |
| Operations ordering | PASS: transfers included, newest-first |
| Category picker | PASS: vertical dialog, partial-text search and selection |
| Payment account | PASS after refresh without activity recreation |
| APK integrity | PASS: URL, non-debuggable, ZIP, alignment, v2/v3 signature, certificate continuity |
| Backend Actions | PASS: run `32540824773`, backend deployed, frontend skipped |
| Production API | PASS: health/OpenAPI/login/refresh |
| DB | Unchanged: migrations and backup skipped; revision `20260618_0017` |

Final APK:
`C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260822-035412-personal-FINAL-manual-install.apk`,
SHA-256 `b7244a339eb71bcb91dc8a02066e93bc219707691a350488315255a57f5cb1c4`,
size `8119142` bytes.

Backend release:
`/opt/finance/releases/finance-personal-backend-20260822-12a1b91f`; rollback
candidate `/opt/finance/releases/20260726T220603Z-55f4ac53`.

Residual coverage: full UI offline create/reconnect/sync was not rerun on the
final APK; OCR real-image upload was not run; Android 17 Espresso fails in
framework setup before assertions; production HTTP remains a TLS risk.

Evidence: [[Док_Release_Android_Production_20260822]]. Test model:
[[QA_ТестКейсы_Android_Production_20260822]]. Reusable production account:
[[QA_Учетная_Запись_Production_20260822]].

## Wave 28 Native iOS final code approval (2026-08-22, historical predecessor)

> Superseded by [[#Wave 29 Native iOS and production release closure (2026-08-23)]].

**Scope:** secure iOS bearer session, account-scoped SwiftData/sync and current
Android behavior parity integrated into native SwiftUI.

| Gate | Result |
| --- | --- |
| Final source | PASS: `a5a332093587fc2467383686cca089877d03f90e` |
| GitHub Actions | PASS: run `32563222674` on exact SHA |
| Backend full local | PASS: 313 passed, 6 skipped |
| Backend auth/migration CI | PASS: 63 tests, Ruff, one Alembic head `20260822_0019` |
| Native builds | PASS: XcodeGen, Debug and Release |
| XCTest | PASS: 77/77 |
| Launch UI | PASS: 1/1 |
| Secure session/refresh/403/logout | PASS automated |
| A -> B isolation, SwiftData migration and transactional sync | PASS automated |
| Category/newest-first/edit/investments/payment/month | PASS automated |
| Personal-only and OCR online-only | PASS automated |
| Physical iPhone/signing | NOT RUN/BLOCKED |
| Production HTTPS/ATS | NOT RUN/BLOCKED |
| Final reviewer | APPROVE for code/CI; no open P0/P1 in reviewed scope |
| Backend production deploy/migration | PREFLIGHT BLOCKED / NOT PERFORMED |

Worker evidence: secure session run `32554005096`, SwiftData/sync run
`32554343934`, UX parity run `32552813248`. Final code/CI conclusion uses run
`32563222674`.

Review cycle 1 closed the real-path 72-hour offline restore cap, refresh
lifetime, offline edit/delete analytics and logout-vs-refresh race. Review
cycle 2 closed access/refresh expiry separation, partial edit -> delete
analytics rebase and uncategorized expense breakdown.

Production preflight facts: environment `production` has
`protection_rules=[]`; branch `prod/release-finance-ios-backend-20260822` is
local and not pushed; production DB remains `20260618_0017`; health HTTP 200;
HTTPS/FQDN absent; Alembic `20260822_0019` not applied.

Evidence: [[Док_Release_Native_iOS_Current_Parity_20260822]]. Test model:
[[QA_ТестКейсы_Native_iOS_Personal_20260821]]. Existing production QA account
remains only in [[QA_Учетная_Запись_Production_20260822]]; no credentials were
copied to project Git.
## Wave 29 Native iOS and production release closure (2026-08-23)

**Scope:** exact-SHA native iOS CI closure, independent review and GitHub Actions
production deployment. Physical iPhone signing/install was not performed.

| Check | Result |
| --- | --- |
| Integration branch | `codex/ios-native-current-parity-20260822` |
| Immutable release branch | `prod/release-finance-ios-current-parity-20260823-db7ebdd` |
| Deployed code | `db7ebdd41a35018ae59e1fc4f5c5e38f0ed37de6` |
| iOS CI | PASS: run `32603535573`; Debug/Release/Personal; normal 87/0; personal 10/0 |
| iOS artifact | `9483613408`; `sha256:52d98838dd947420e0093c308c58286ab3f5db831017030c4f64be61f6c7bc43` |
| CI-only package proof | PASS: run `32604090062`; packages/common gate green; host/deploy skipped |
| CI-only frontend artifact | `9483667044`; `sha256:0e430fdb2cfca47dcac29d18cec1351b45e17807fb2524800337c78a1db28bed` |
| CI-only backend artifact | `9483674722`; `sha256:d38af135dab7b04ca1ce5c72c920f9e3f5b542eb73284964465d60fe3b522864` |
| Independent review | APPROVE on exact SHA; no P0-P3 |
| Production deploy | PASS: run `32604838031` |
| New release | backend/frontend `20260822T231803Z-db7ebdd4` |
| Previous releases | backend `finance-personal-backend-20260822-12a1b91f`; frontend `20260726T220603Z-55f4ac53` |
| DB | PASS: `20260618_0017 -> 20260822_0018 -> 20260822_0019` |
| Backup | PASS; SHA-256 `238d8d441b5bacca2a5f0ddba728cdf4066c34bd0e32a6c1a589f13cfcd57142` |
| Smoke | PASS: health/OpenAPI/frontend/SW/auth rotation/logout/read-only personal endpoints |
| Rollback | NOT REQUIRED; release branch retained |
| Physical iPhone | NOT RUN: no signing/install/device smoke proof |

Backup path:
`/opt/finance/backups/postgres/finance_prod-20260822T232027Z-20260822T231803Z-db7ebdd4-20260618_0017-to-20260822_0019.dump`;
sibling evidence suffix `.dump.evidence.txt`.

Owner/family PersonalSideloadHTTP is isolated by target, bundle identity, exact
ATS allowlist, development signing and no-archive/export policy. Waiver review:
2026-11-22. Plaintext residual risk remains accepted only in that scope.

Persistent production QA account remains discoverable through
[[QA_Учетная_Запись_Production_20260822]] and must never be deleted. Credentials
were not copied into this result.

Project source of truth:
`MVP_EVIDENCE/native-ios-current-parity-20260822/SUMMARY_SANITIZED.md` and
`docs/ios-native-mac-codex-install-prompt.md`.
