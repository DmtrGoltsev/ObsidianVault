---
id: "qa-results-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-06-12"
ссылки:
  - "[[Finance]]"
  - "[[QA_Фиксы]]"
  - "[[Док_Release_NewDis_20260608]]"
---

# QA Результаты — Finance MVP Android

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
