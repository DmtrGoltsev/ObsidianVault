---
id: "project-finance"
тип: "проект"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-08"
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
  - "[[Док_Release_NewDis_20260608]]"
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

### Planning asset target production release (2026-06-07)

- **Кодовый commit:** `5bb7ab493d7c3faa323d711ffa1febb2d94b4f7c` (`fix(planning): support asset allocation targets`); KB previous commit `b7729f9`.
- **Asset target gap:** закрыт явный Planning `targetType=asset` на backend/OpenAPI/Android.
- **OpenAPI:** `AllocationTargetType` enum = `expense_category`, `account`, `asset`.
- **DB/deploy:** backend-only release `20260607T121851Z-5bb7ab4` в `/opt/finance/releases/20260607T121851Z-5bb7ab4`; `/opt/finance/current` указывает на новый release.
- **Миграции:** before `20260531_0009`; applied `20260531_0009 -> 20260606_0010 -> 20260607_0011`; after `20260607_0011 (head)`.
- **Backup:** `/opt/finance/backups/20260607T122105Z-59603b0/finance_prod.dump`, SHA256 `adbed3574f02a4fad94c41ac0fa2e18b4abe3e3cd21d527c3bf08cab04c1a8ae`.
- **QA:** backend full pytest — `228 passed, 4 warnings`; Android gate `:app:testDebugUnitTest :app:compileDebugKotlin :app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api --console=plain` — `BUILD SUCCESSFUL`.
- **Production smoke:** service active; `/health` direct and nginx OK; unauth `sessions/current` returns 401.
- **Android APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54235660`, SHA256 `9E3814A5ABBBD1A9EFB8D484A94C973E4CA2598D21D921B990EE1DFCA568C6D8`, time `2026-06-07 15:00:20 +03:00`.
- **Delivery boundary:** web frontend не деплоился; Android APK delivered locally.

### Поставка Asset categories + Analytics/Planning polish (2026-06-07)

- **Статус релиза:** production deploy success; release agent завершил деплой.
- **Кодовый commit:** `be9f8abe1abaed530c1dd503c5e631e935d8a3d5`.
- **Production release:** `20260607T163043Z-be9f8ab` в `/opt/finance/releases/20260607T163043Z-be9f8ab`; `/opt/finance/current` указывает на этот release.
- **Backup:** `/opt/finance/backups/20260607T163554Z-5bb7ab4/finance_prod.dump`, SHA256 `c7e38fae515b60b5d4b7d6588bbc8d03687d1769f222493ad240510f1f54b2d5`.
- **Миграции:** before `20260607_0011`; after `20260607_0012 (head)`.
- **Production smoke:** service active/running; health direct/nginx 200; unauth `sessions/current` 401; OpenAPI 200 с asset categories routes.
- **Asset categories source of truth:** категории активов стали явной моделью данных: `manualAmount` используется для пустых категорий, `isInvestment` отделяет инвестиционные категории, `assetType` фиксирует тип актива, `account.assetCategoryId` связывает счёт с категорией; удалённые счета не оставляют stale totals.
- **Backend/API:** добавлены asset-categories endpoints; backend report поддерживает `reportMode=personal`; миграция `20260607_0012`.
- **Analytics:** добавлена метрика investments; структура капитала остаётся только во вкладке Analytics.
- **Categories:** создание категорий учитывает scope `personal`/`household`; UI редактирования использует edit icon.
- **Planning:** income day трактуется как день месяца; форма дохода скрыта за Add; новые allocations выбирают expense category или investment asset category, target account для новых allocations не предлагается; текст истории уточнён.
- **QA:** backend latest — `238 passed, 8 warnings`; fixtures — `8 passed`; Android build — `BUILD SUCCESSFUL`.
- **Android APK final:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54235660`, SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26`.

### Release planning iteration MVP (2026-06-07)

- **Статус релиза:** MVP planning iteration закрыт и выведен в production; branch `codex/finance-planning-mvp-gpt5` запушен в `origin`.
- **Project commit:** `819b5815fed8c81bfa6a6e6131e790429454c2e8` (`Release planning iteration MVP`).
- **Release id:** `20260607T225457Z-819b5815`.
- **Production current:** backend `/opt/finance/releases/20260607T225457Z-819b5815`; web `/var/www/finance/releases/20260607T225457Z-819b5815`; оба prod `COMMIT` файла указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8`.
- **Миграции:** Alembic head `20260607_0013 (head)`.
- **Production checks:** `finance-backend.service` active; `127.0.0.1:8081/health` OK; `/finance-api/health` OK; `/finance/` 200; manifest scope/start_url `/finance/`; `/finance/sw.js` 200.
- **QA:** OpenAPI parse OK; operationId duplicates `0/58`; backend `243 passed, 9 warnings`; Android unit PASS; Android `assembleDebug` PASS.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`, size `54,235,660`, SHA256 `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4`.
- **Acceptance clarification:** planning progress хранится на allocation-level (`PlanningAllocationDto.actualAmount`/`varianceAmount`/`status`/`attentionReason`), не как plan-level `PlanningPlanDto.progress`; `previousMonthSurplus` находится в `PlanningSummaryDto`.
- **Ограничения:** authenticated QA login/OCR smoke не запускался из-за отсутствия operator password/session token; выполнены только health/static deploy checks; debug APK не release-signed.
- **Evidence:** [[Док_Release_Planning_MVP_20260607]].

### Release newDis UX simplification (2026-06-08)

- **Статус релиза:** `newDis` закрыт по sanitized release closure с ограничениями; project branch `newDis` синхронизирован с `origin/newDis`.
- **Project commit:** `6ce31f53f6150050b4cb0dad8488254bd04ff31b` (`feat(finance): simplify newDis UX flows`).
- **Android APK fix commit:** `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`); `/finance/COMMIT` остается web context `6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- **Scope:** UI/test changes; `apps/backend`, `db`, `api` не менялись, поэтому backend redeploy waiver принят.
- **Production frontend:** `/finance/COMMIT` -> HTTP `200`, body `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; `/finance/`, `/finance/sw.js`, manifest, JS/CSS assets byte-hash equal local `apps/web-pwa/dist`.
- **Production backend:** `/finance-api/health` -> HTTP `200`, body `{status:ok}`; exact commit endpoints отсутствуют (`404`), route surface matches post-808/newDis.
- **QA:** Android prod-path correction unit XML — 9 files, 61 tests, 0 failures, 0 errors, 0 skipped; Android lint historical — 0 errors, 6 warnings.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94`, `applicationId=com.finance.mvp`, `versionName=0.1.0`, debug-signed; previous SHA `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D` superseded due to emulator dev base URL.
- **Ограничения:** full PWA install/service worker proof требует HTTPS/domain; authenticated production login/OCR smoke и retention/privacy evidence остаются отдельными gates; historical PWA/backend/OpenAPI reports не считаются direct `6ce31f5` closure.
- **Evidence:** [[Док_Release_NewDis_20260608]].

### Android asset category UX fixes (2026-06-08)

- **Статус:** Android-only post-release UX fixes закрыты по code-review/unit/Kotlin evidence; branch `newDis`, remote parity OK.
- **Project commit:** `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`).
- **Changed files:** `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt`, `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`.
- **Recents/overview:** probable crash fixed через custom Saver для nullable `AddAccountState?`.
- **Asset categories:** explicit edit icon; visible investment checkbox saved via existing update; destructive bulk archive gesture removed; trash confirmation added; P1 fix blocks archiving non-empty category and asks user to move/delete accounts first; empty category archive calls backend category archive endpoint.
- **AddAccountSheet:** IME padding, scroll и BringIntoView для focused fields above keyboard.
- **Reorder:** long-press drag reorder for asset categories with local `SharedPreferences` persistence.
- **QA:** P0/P1 clean after P1 fix; `:app:testDebugUnitTest` BUILD SUCCESSFUL, 61 tests, 0 failures/errors/skipped; `:app:compileDebugKotlin` BUILD SUCCESSFUL.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A`; content verification keeps `http://45.10.110.42/finance-api` and no dev URLs.
- **Ограничения:** actual recents/overview, keyboard, drag gestures and confirmation dialogs still need emulator/device manual QA; no visual gesture proof was available.

### Android final legacy asset edit + IME correction (2026-06-08)

- **Статус:** финальные два user misses закрыты Android-only commit/push; branch `newDis`, remote parity OK.
- **Project commit:** `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`).
- **Changed files:** `apps/android/app/src/main/AndroidManifest.xml`, `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt`, `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`.
- **Legacy old asset group edit:** старая группа вроде `Вклад` получила checkbox `Инвестиция` в legacy edit dialog. Если checkbox off — сохраняется старое rename-only поведение. Если on — legacy group конвертируется в реальную asset category с `isInvestment=true` и связывает active legacy accounts.
- **Safety guards:** конвертация блокирует empty group, mixed-currency group, overview/no writable scope; rollback на link failure использует updated account versions и архивирует созданную категорию.
- **Account creation IME:** `MainActivity` использует `adjustResize`; `AddAccountSheet` усилен через `skipPartiallyExpanded`, `imePadding`, `navigationBarsPadding`, repeated `BringIntoView` и larger spacer. Material3 `windowInsets` unavailable, использован совместимый fallback.
- **QA:** final review P0/P1 clean; `:app:testDebugUnitTest` PASS, 61 tests, 0 failures/errors/skipped; `:app:compileDebugKotlin` PASS; `assembleDebug` PASS.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,660`, SHA256 `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B`; production API base found x2, dev URLs absent.
- **Ограничения:** manual QA на device/emulator всё ещё нужна для visual IME и live migration legacy group.

### Compact investment asset categories + analytics fix (2026-06-08)

- **Статус:** compact investment asset category/iconKey/analytics fix закрыт по backend targeted tests, Android unit/build gates и integration review; branch `newDis`, remote parity OK.
- **Project commit:** `09ea6479451c61b3d06a412e5aaaecec534fc96a` (`fix(finance): compact investment asset categories`).
- **Scope:** compact `AssetCategoryGroupCard`; edit mode упрощён; manual amount скрыт при linked accounts; linked accounts list убран из category edit/card; investment badge использует trending-up icon; icon picker и persisted `asset_categories.icon_key` добавлены в backend/API/Android; analytics исправлена удалением Android forced currency filter и parsing investment totals из backend contract.
- **QA:** backend targeted suite через project `.venv` — `31 passed, 2 warnings`; Android `:app:testDebugUnitTest` successful; Android `:app:assembleDebug` successful.
- **Review:** integration review P0/P1 clean; P2 staging risk handled by curated commit.
- **APK:** `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733`; production API base present, dev URLs absent.
- **Ограничения:** residual manual QA остаётся для visual screenshot/device check compact card, edit mode, icon picker и investment badge.

### Открытые баги (P1)

- BUG-006: AddAccountSheet всегда создаёт shared-счёт
- BUG-007: Нет защиты от double-tap на деструктивные действия
- BUG-008: Удаление транзакции без подтверждения
- BUG-009: Суммирование мультивалют без конвертации
- BUG-023: quickAddCategoryFor молча подменяет выбор

## Ветки

- `newDis` — текущая UX simplification release branch; production frontend commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; latest finance fix commit `09ea6479451c61b3d06a412e5aaaecec534fc96a`
- `codex/finance-planning-mvp-gpt5` — кодовая ветка Planning MVP / production release `819b5815`
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
