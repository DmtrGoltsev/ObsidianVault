---
id: "project-finance"
тип: "проект"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-07-27"
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

### Production deploy policy (2026-06-13)

- Основной путь production deploy для frontend/backend: GitHub Actions workflow `.github/workflows/finance-hexcore-prod-deploy.yml`.
- Auto deploy разрешен только для push в ветки, имя которых содержит `release`.
- GitHub environment: `production`; required secrets by name: `HEXCORE_PROD_SSH_HOST`, `HEXCORE_PROD_SSH_USER`, `HEXCORE_PROD_SSH_PRIVATE_KEY`, optional `HEXCORE_PROD_SSH_PORT`.
- Direct SSH/SCP upload to HexCore остается fallback/alternative.
- Backend deploy automation включен в актуальный production workflow; direct SSH/SCP остается fallback, не primary.
- Финальный реальный deploy подтвержден 2026-06-19; см. [[CI_CD_Production_Status_20260619]].
- Подробно: [[Регламент_Деплоя_Finance]].

### PWA URL для iPhone / браузера (2026-06-12)

- **URL:** `http://45.10.110.42/finance/`.
- **Назначение:** это production PWA URL для открытия Finance на iPhone или в обычном браузере.
- **Терминология:** `PWE` из пользовательского запроса трактуется как `PWA`.
- **Как открыть на iPhone:** открыть Safari или другой браузер, перейти по `http://45.10.110.42/finance/`; при желании добавить на экран «Домой» через Share -> Add to Home Screen.
- **Ограничение:** HTTPS или домен не заявляются, потому что в evidence подтверждён только HTTP IP URL.

### Date-only capture / Analysis QA status (2026-06-12)

- **Статус:** release closure PASS по backend/PWA/Android date-only analysis, asset-edit stabilization и capture confirmation live Android flow.
- **Project release integration commit:** `5a59f29335d307931f94e561b5120750bbfd260b` (`fix(finance): stabilize android asset editing`), pushed to `origin/newDis`.
- **Project capture closure docs commit:** `a9f143e37515b53cc617165621ebf1708e0b0ee4` (`docs(finance): record capture confirmation pass`), pushed to `origin/newDis`.
- **Backend production:** deployed commit `26b487d61b7d2d6de704f0a632bcb08ff7f240f7`, release `/opt/finance/releases/20260612T045020Z-26b487d6`, Alembic `20260607_0013 -> 20260612_0015`, backup SHA256 `6b48a4e8f73cbabeb40553eb052869c861bb2954edad0d960d3bbc7a34316ef8`, health/OpenAPI/auth smoke PASS.
- **PWA production:** `http://45.10.110.42/finance/`, release `20260612T091555Z-26b487d61b7d`, JS asset `/finance/assets/index-BxFzW0Su.js`, npm test/build/nginx/public smoke PASS; evidence `MVP_EVIDENCE/reports/2026-06-12_pwa_prod_deploy_SANITIZED.md`.
- **Android final APK:** `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk`, size `54235740`, SHA256 `6AEE934A8817055B1738B32E1468D2A4C5415502C224115F9C7953F63EC3D893`; local-only artifact because `*.apk` is intentionally ignored.
- **Android QA:** payment account filter/date-only/analysis PASS; asset edit regression fixed. Latest final evidence `MVP_EVIDENCE/date-only-capture-analysis-qa-metal-fix-20260612-133358/QA_REPORT_SANITIZED.md`: legacy `Металл` manual amount PASS; Broker/Card no icon picker/no manual amount PASS; secret scan PASS. D401 FAIL report remains historical pre-fix evidence only.
- **Capture confirmation:** PASS by later escalation report `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/QA_REPORT_SANITIZED.md`; secret scan `MVP_EVIDENCE/date-only-capture-confirmation-escalation-20260612-141033/secret_scan_summary.json` PASS/finding_count `0`. Live proof: emulator `emulator-5554`, APK SHA256 `6AEE934A8817055B1738B32E1468D2A4C5415502C224115F9C7953F63EC3D893`, pending capture draft edited to amount `45.67` and date `2026-06-11`, then `Подтвердить` removed the draft row and Operations showed the edited backend-backed amount/date. Previous `MVP_EVIDENCE/date-only-capture-confirmation-qa-20260612-100149/QA_REPORT_SANITIZED.md` remains historical pre-escalation BLOCKED fixture evidence only.
- **Curated release report:** `MVP_EVIDENCE/reports/2026-06-12_date-only_capture_analysis_release_SANITIZED.md`.
- **Sanitization:** no raw OCR payloads, screenshots, UI XML, production financial data, UUIDs, tokens, cookies, passwords, or secret values are stored in KB.
- **Residual risk:** capture confirmation PASS is scoped to the escalation run with an existing authenticated Android app session; fresh login from credentials and deterministic seed/deep-link fixture remain future hardening, not current release blockers.

### Safe QA account metadata (2026-06-12)

| Environment | Safe alias / identifier | Purpose | Secret handling |
|-------------|-------------------------|---------|-----------------|
| Production QA | `finance.qa@local.test` | Owner-operated production smoke and authenticated QA flows | Password value is never stored in KB. Out-of-band locator only: `/etc/finance/qa-owner.env`, key `FINANCE_QA_PASSWORD`. |
| Development | `demo.owner@example.test` | Local/dev seeded flows, emulator/PWA development checks | No passwords, tokens, cookies, or sessions are stored in KB. |

### Production QA persistent account (2026-07-11)

**Status:** ACTIVE / PERSISTENT / NEVER DELETE.

Security boundary: the persistent QA account is documented for continuity, but its password remains in an owner-managed secret store and is not copied into the vault.

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
| Registration result | `POST /api/v1/users` -> HTTP `201` on 2026-07-11 |
| Login result | `POST /api/v1/sessions` -> HTTP `201` on 2026-07-11; access token present and deliberately not stored |
| Full QA locator | [[QA_Результаты#Production QA persistent account (2026-07-11)]] |

Search tags / keywords: Finance Production QA account; persistent production test account; NEVER DELETE; qa login; Android prod E2E; PWA prod smoke; Finance Production QA Persistent Test Account - NEVER DELETE; finance.qa.prod.20260711.6cb15851@local.test.

### Android Assets / Investment quick add closure (2026-07-12)

- **Статус:** Android-поставка закрыта для ручной установки; backend production deploy не выполнялся.
- **Android Assets UI:** во вкладке `Активы` карточки категорий больше не сжимают названия до `Б...`/`Вк...`; счетчик не переносится по буквам; сумма и `Править` вынесены так, чтобы не ломать title.
- **Quick add:** добавлен тип `Инвестиция`; это не обычный `Расход`. Сохранение создает `transactionType=asset_buy`, `categoryId=null`, требует дату/сумму и выбирает только счета, привязанные к investment asset category.
- **Analytics / Planning semantics:** `Факт` у `Вклад`/`Брокер` в `Аналитика -> План месяца` должен считаться по categoryless investment transactions на linked investment accounts. Investment allocation actual включает `brokerage`, `asset_buy`, `interest`, `dividend`, `adjustment`; `expense`/`transfer` не считаются investment fact.
- **Sync boundary:** local sync поддерживает explicit `categoryId:null`; backend sync allowlist локально расширен для investment types. Online direct `asset_buy` должен идти через существующий transactions API, но offline sync investment operation требует production backend deploy через GitHub Actions release branch.
- **Deploy blocker:** backend deploy заблокирован release scope/protection checklist; SSH/SCP не использовались и не заявляются.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260712-112532-POSTP2-manual-install.apk`, SHA256 `cace0eb69e589f8eb0be579a0a4bc83039013d35a29d74e32547367449ee4d79`.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-assets-investment-postp2-qa-20260712-112610`.
- **QA:** Android targeted `SyncManagerTest`, `ApiClientCaptureDraftTest`, `AppSectionTest`, `PlanningUiStatusTest`; Android full `:app:testDebugUnitTest`; backend sync pytest `21 passed`; backend targeted planning/transactions/reports `30 passed`; ruff sync files; `assembleRelease` с prod URL; `apksigner`; `emulator-5554` install/smoke `Assets`/`Analytics`.

### Android transfer assets / ordering closure (2026-07-12)

- **Статус:** POSTP1 transfer/assets/order wave закрыта для ручной установки Android APK; backend production deploy ещё требуется для prod sync behavior.
- **Исправлено:** перевод через `Операции` / quick add на инвестиционный счёт теперь должен отражаться в `Активы`: Android категории активов считают total из свежих `dashboard.accounts.currentBalance` по `assetCategoryId`, а backend sync публикует `accounts/update` для source/destination после `transfer`.
- **Семантика плана:** `transfer` меняет balances/assets, но НЕ является investment actual для плана; investment actual остаётся за `asset_buy` и другими investment fact типами. `transfer` исключён из факта `Вклад`/`Брокер`.
- **Android:** transfer quick add показывает выбор даты и отправляет `transactionDate`; вкладка `Операции` сортирует newest-first.
- **PWA:** `recentTimeline` newest-first; Overview/Operations показывают новые операции выше старых.
- **Backend:** transfer REST/sync push emits account sync changes; reports/planning regression tests обновлены и пройдены. Sync pull order by `seq` не меняли: это cursor protocol.
- **Deploy:** DB migration не требуется. Android APK указывает на prod URL, но prod backend должен быть развёрнут через GitHub Actions release branch, чтобы account sync changes заработали в production.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260712-220221-POSTP1-TRANSFER-manual-install.apk`, SHA256 `B4AF3B3CF30E77F5C22075B9EFC47D82CBBF5FBCDDF5356D286F37DDEB3209C6`.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-transfer-assets-ordering-postp1-qa-20260712-215452`.
- **QA:** Android targeted/full PASS; backend targeted `49 passed`; `ruff` PASS; PWA targeted ordering/build PASS; PWA broader `App.test` имеет 2 known date-sensitive failures around June 2026; `emulator-5554` install/smoke PASS без изменения данных.

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

### Critical investment save regression closure (2026-06-12)

- **Статус:** critical Android regression `Брокер -> Инвестиция -> Сохранить` закрыт по build/unit evidence, quick critical-path QA PASS and fail-fast harness PASS.
- **Project commit:** `d8175116f5123b6a304d4bd22dc083f2725505a0` (`fix(finance): migrate legacy brokerage assets`), pushed to `origin/newDis`.
- **Root cause:** Android отправлял `iconKey` в `POST /api/v1/asset-categories`, а deployed OpenAPI для `AssetCategoryCreateRequest` strict `additionalProperties=false`; backend возвращал validation failure до create/link.
- **Fix:** create payload больше не содержит `iconKey`; изменённые project files: `FinanceApp.kt`, `AppSectionTest.kt`, `ApiClient.kt`, `ApiClientPlanningAllocationTest.kt`.
- **QA:** `compileDebugKotlin` PASS; `testDebugUnitTest` PASS, 71 tests; `assembleDebug` PASS. Quick QA PASS: after save/restart linked asset category id present, `isInvestment=True`, `investmentCategories.count=1`, totals `150000.0000 RUB`, no `Validation failed`; secret scan PASS. Harness PASS on `emulator-5556`.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `B6960DB5D13198405984C027746343432CB95B0C08BB24F54D6A7FCD5061DCC7`.
- **Evidence:** `MVP_EVIDENCE/critical-investment-fix-20260612/SUMMARY_SANITIZED.md`, `MVP_EVIDENCE/critical-investment-qa-quick-20260612-013822/QA_REPORT_SANITIZED.md`, `MVP_EVIDENCE/critical-investment-qa-harness-20260612-015225/HARNESS_REPORT_SANITIZED.md`.
- **Ограничения:** APK debug-signed; backend deploy не заявляется; failed/incomplete evidence folders остаются historical context only.

### Открытые баги (P1)

- BUG-006: AddAccountSheet всегда создаёт shared-счёт
- BUG-007: Нет защиты от double-tap на деструктивные действия
- BUG-008: Удаление транзакции без подтверждения
- BUG-009: Суммирование мультивалют без конвертации
- BUG-023: quickAddCategoryFor молча подменяет выбор

## Ветки

- `newDis` — текущая UX simplification/release branch; production frontend historical commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; backend/PWA date-only deploy commit `26b487d61b7d2d6de704f0a632bcb08ff7f240f7`; latest Android release integration commit `5a59f29335d307931f94e561b5120750bbfd260b`
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

## Обновление KB: asset/planning regression fix (2026-06-10)

- **Статус:** regression fix закрыт и запушен в project repo на `newDis`; KB обновлена как evidence addendum.
- **Project commit:** `1013e632d54c6af6ed9326d8b7f761bdd381bade`.
- **Scope:** восстановлены linked account rows в expanded asset category card (`Вклад` ожидаемо показывает 4 linked accounts), edit mode остаётся без account list; восстановлена legacy visibility logic для `Карта`/`Банк` без дублей при real backend categories; исправлено сохранение/local state `isInvestment` на category level для `Брокер`; в `План месяца` прошедшие месяцы недоступны, persisted/selected past month clamp к current-or-future; missing planning 404 теперь friendly empty state вместо raw `Resource not found or not accessible.`.
- **Russian input diagnosis:** app-level Cyrillic filter не найден; AVD `Codex` имел `hw.keyboard=yes`, вероятная причина в emulator/IME config. Workaround: добавить Russian Android keyboard или настроить `show_ime_with_hard_keyboard` / отключить hardware keyboard.
- **QA:** `:app:compileDebugKotlin` SUCCESS; `:app:testDebugUnitTest` SUCCESS; packaging `:app:testDebugUnitTest` SUCCESS (`BUILD SUCCESSFUL in 2s`); packaging `:app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api --console=plain` SUCCESS (`BUILD SUCCESSFUL in 36s`); review без P0/P1, только P2 missing UI/Compose coverage.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `FCD7EE0D870A12B3B88416DAEBCB3CF35FC513618C865B427E30E5F77F688411`; prod URL `http://45.10.110.42/finance-api` найден в `classes7.dex` и `classes5.dex`, dev URLs absent.
- **Install:** AVD `Codex`, serial `emulator-5554`, package `com.finance.mvp`, install `Success`.
- **Ограничения:** prod auth/DB read-only verification не выполнялась; нет UI/Compose automated coverage для visual regressions; manual visual QA на установленном APK остаётся рекомендованной.

## Обновление KB: critical investment save regression (2026-06-12)

- **Статус:** closure PASS; project commit `d8175116f5123b6a304d4bd22dc083f2725505a0` (`fix(finance): migrate legacy brokerage assets`) recorded.
- **Root cause:** Android create payload для asset category содержал `iconKey`, несовместимый с deployed strict OpenAPI `AssetCategoryCreateRequest`.
- **QA:** build/unit PASS (`compileDebugKotlin`, `testDebugUnitTest` 71 tests, `assembleDebug`), quick QA PASS and harness PASS on `emulator-5556`.
- **Runtime proof:** after save/restart linked category id present, `isInvestment=True`, investment categories count `1`, totals `150000.0000 RUB`, no `Validation failed`.
- **APK:** `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `B6960DB5D13198405984C027746343432CB95B0C08BB24F54D6A7FCD5061DCC7`.
- **Evidence:** `MVP_EVIDENCE/critical-investment-fix-20260612/SUMMARY_SANITIZED.md`; final PASS reports are quick QA and harness only.

## Обновление KB: PWA URL для iPhone (2026-06-12)

- **Добавлено:** краткая инструкция подключения с iPhone/браузера к Finance PWA по `http://45.10.110.42/finance/`.
- **Уточнение:** пользовательский термин `PWE` зафиксирован как `PWA`.
- **Связанный релизный контекст:** последний release closure уже задокументирован выше: date-only операции, payment account flag/filter, capture confirmation edit amount/date PASS, analysis month switching, Android asset edit fix, backend/PWA deploy и APK SHA256 `6AEE934A8817055B1738B32E1468D2A4C5415502C224115F9C7953F63EC3D893`.

### Final CI/CD local preparation status (2026-06-14)

- User confirmed Finance is prod.
- Read-only HexCore inventory: `finance-backend.service`, `/finance/ -> /var/www/finance/current/`, `/finance-api/ -> 127.0.0.1:8081/`, backend current `/opt/finance/releases/20260612T045020Z-26b487d6`, DB `finance_prod`, env `/etc/finance/backend.env`, health OK.
- Local CI/CD preparation PASS: full `.github/workflows/finance-hexcore-prod-deploy.yml`, `.github/workflows/finance-prod-rollback.yml`, `docs/production/finance-*`, install doc updated.
- Frontend/backend package/deploy design prepared; Alembic gated; restart gated; pinned `known_hosts`; no DB rollback.
- Final review: workflow YAML parses, no raw `${{ inputs.* }}` in `run` or `script`, release push no prod mutation, dispatch gates present, no hardcoded secret values.
- Historical note: no production deploy was executed during the 2026-06-14 preparation update; superseded by final deploy evidence on 2026-06-19.
- Residual approvals: GitHub production environment/secrets/required reviewers, first production run, deploy/restart/migration/rollback approvals, DB backup proof; DB rollback out of scope.
- Evidence: [[CI_CD_Production_Status_20260614]].

### Offline-first release QA closure (2026-06-18/2026-06-19)

- **Статус:** branch `codex/offline-first-release-qa` зеленый на GitHub Actions run `27796358035`, head `b09043e531152bb5f9b2fdb6ef18b21d786bbebf`.
- **Release id:** `20260618T234841Z-b09043e5`.
- **Package gates:** frontend package `56 passed`; backend package `285 passed, 6 skipped`.
- **Local Android E2E:** PASS зафиксирован в `MVP_EVIDENCE/offline-first-release-qa-20260618-234050/QA_REPORT_SANITIZED.md`.
- **Исправленные release blockers:** backend ruff gate; FastAPI `0.137.2` route introspection через `iter_route_contexts`; backend deps pinned to `fastapi==0.137.2`, `starlette==1.3.1`.
- **PR/main:** `https://github.com/DmtrGoltsev/finance/pull/1` merged at `2026-06-18T23:53:47Z`; remote `main` HEAD и merge commit подтверждены как `cff578df0be001c0af187c5a90d9917fc0b2c1e9` с parents `3f70a3bf...` + release head `b09043e5...`.
- **Workflows on main:** workflow files present; active workflows confirmed: `Finance HexCore Production CI/CD` id `298526666`, `Finance Production Manual Rollback` id `298581092`.
- **Historical deploy boundary:** на момент offline-first QA production deploy не заявлялся; этот блок superseded by final production CI/CD state ниже. Текущий production deploy status: PASS.
- **Sanitization:** KB фиксирует только sanitized summary/IDs/counts; raw logs, raw OCR, screenshots, APK/build artifacts, passwords, tokens and secret values не переносились.

### Final production CI/CD state (2026-06-19)

- **Статус:** production deploy через GitHub Actions выполнен и зеленый.
- **Repo:** `C:\Users\style\Documents\Codex\Финансы`, remote `DmtrGoltsev/finance`.
- **Branches:** implementation `codex/finance-cicd-prod-deploy-update`; release `release/finance-prod-ci-cd-27730f5`.
- **Release commit:** `d10ac448a12c6681577d13433ef6225a094afbc2`.
- **GitHub Actions:** `https://github.com/DmtrGoltsev/finance/actions/runs/27802865321`, success; все jobs succeeded.
- **Production release:** frontend/backend `20260619T030640Z-d10ac448`.
- **Production smoke:** `http://45.10.110.42/finance/` -> 200; `http://45.10.110.42/finance-api/health` -> 200, `{"status":"ok"}`.
- **Alembic:** current `20260618_0017`; migration from `20260612_0015` happened in earlier retry; final run had current/target `20260618_0017`.
- **Backup evidence:** `/opt/finance/backups/postgres/finance_prod-20260619T030824Z-20260619T030640Z-d10ac448-20260618_0017-to-20260618_0017.dump`, sha256 `72cf70b10d927cb5be7291148bd83fbcfb7a6342ff9d669634a0e152efa57104`.
- **Residual risk:** production uses `python3 3.14.4`, because `python3.12`/`python3.11` отсутствуют; условие `>=3.12` выполнено, но runtime новее CI 3.12.
- **Evidence:** [[CI_CD_Production_Status_20260619]].

### Native iOS parity branch status (2026-06-19)

- **Статус:** Windows static QA PASS для native iOS parity branch `codex/IOS`; FAIL не зафиксированы.
- **Worktree/base:** `C:\Users\style\Documents\Codex\Финансы-ios`; base `origin/main` commit `66feadd94dbf936faec500f565638973ca270f64`.
- **Native-only boundary:** parity target только `apps/ios` SwiftUI/UIKit; PWA/Capacitor under `apps/web-pwa` остается отдельным и не является iOS parity target.
- **Реализовано:** API config hardening/Release guard; auth/register/session/logout wipe improvements; manual transactions date-only/payment filter fallback; capture editable amount/date online-only; payment account/assets/investment/icon preservation; analytics month/category/investments; planning fallback for exposed mutations; icon-only tabs; offline-first local JSON store, sync queue, manual sync, issues and Russian sync UI.
- **Ограничение релиза:** native iOS release sign-off остается BLOCKED только Mac/Xcode gates: `swift`, `xcodebuild`, `xcodegen` unavailable. Future gates: XcodeGen, Debug/Release build, simulator/device flows, Keychain/cookie wipe, offline queue backend push/pull, OCR/copy online-only UX.
- **Sanitization:** KB фиксирует только concise sanitized summary; secrets, raw logs, screenshots, APK/evidence binaries and raw OCR payloads не переносились.

## Auth/session wave (2026-07-25)

- **Status:** Android auth/session wave documented as sanitized KB update; no secrets, passwords, tokens, cookies, session IDs, raw OCR payloads or screenshots copied into Obsidian.
- **Android AuthGate:** signed-out and restoring states no longer render as a protected tab. They show a separate AuthGate without TopAppBar, NavigationBar, FAB or protected tabs; main tabs are available only after signed-in state.
- **Local session storage:** Android stores `SessionTokenBundle` in `EncryptedSharedPreferences`: `accessToken`, `refreshToken`, `expiresAt`, `userId`. User password is not stored.
- **API client session behavior:** login/register persist the token bundle. On `401`/`403`, protected calls refresh once through `POST /api/v1/sessions/refresh`, retry once, and clear local token store plus protected UI on logout or refresh/auth failure. Screenshot OCR uses the same refresh/retry-once path.
- **Backend session behavior:** `/api/v1/sessions/refresh` added; login/register with `android_bearer` return `refreshToken`; refresh tokens rotate with hash-only storage, old refresh invalidation, logout invalidation and CAS atomic rotation. No DB migration required.
- **Security review:** P0/P1/P2 none after fixes.
- **QA:** backend auth `71 passed`, `ruff` passed, Android full unit passed, APK built/signed/verified. Emulator unavailable, so manual install/smoke was skipped.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260725-231110-AUTH-SESSION-manual-install.apk`; SHA256 `F9ABD3D02D64A06FCB5E78731AC313FD8230165CF9BC8D427E2FED92466BB8A0`.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-auth-session-qa-20260725-231110`.
- **Deploy caveat:** superseded by the 2026-07-25 backend production deploy record below; backend refresh is now deployed.

### Auth/session backend production deploy (2026-07-25)

- **Status:** backend production deploy successful for auth refresh; GitHub Actions run status is `completed/failure` only because unrelated `frontend-ci-package`/PWA tests failed.
- **Branch:** `prod/finance-auth-refresh-20260725`.
- **Commit:** `9e1ed7903798ed4f1edbcfeb3d98b23ec9ae0763`.
- **Release ID:** `finance-backend-auth-refresh-20260725-9e1ed79`.
- **Actions run:** `https://github.com/DmtrGoltsev/finance/actions/runs/30174265210`; backend-only dispatch, `deploy-frontend` skipped, `deploy-backend` success.
- **Health:** `http://45.10.110.42/finance-api/health` -> 200 `{"status":"ok"}`.
- **Route smoke:** `/finance-api/api/v1/sessions/refresh` returns 422 on empty payload, route mounted.
- **Refresh smoke:** registration 201, refresh 200, token fields present, refresh rotated, old refresh rejected 401; no tokens/passwords in evidence.
- **Backend artifact checksum:** `da77996a82489e1732a77686eda2965b6f51113d8528828151927ca42b384491`.
- **Migrations/backup:** `run_migrations=false`; DB migrations not run; workflow backup not created; DB migration not required.
- **Deploy boundary:** direct local SSH/SCP not used; staged files exactly allowed auth/OpenAPI backend list.
- **Caveat:** workflow emails may say failed due frontend job; backend deploy is successful.

### Android category search / analytics POSTP2 closure (2026-07-26)

- **Статус:** Android-only поставка закрыта для ручной установки APK; backend deploy не требовался.
- **Исправлено:** в добавлении/подтверждении расхода выбор категории получил быстрый поиск по части слова; горизонтальные списки заменены на кнопку `Категория`, которая открывает overlay/dialog с вертикальной прокруткой и поиском.
- **Аналитика:** `Анализ -> Сводка -> Инвестиции` на Android заполняет total из `investmentsByCurrency`/summary fallback; `Главная -> Топ категории` получила кнопку `Все` для полного списка категорий трат по убыванию суммы.
- **P2:** top categories учитывают только expense-категории и исключают expense-транзакции с income/asset `categoryId`; search state category dialog стабилен key-based и не протекает между строками/режимами.
- **QA:** targeted `AppSectionTest`/`ApiClientDashboardTest`, expanded targeted auth/session tests, full `:app:testDebugUnitTest`, `:app:compileDebugKotlin`, release assemble, `zipalign`, `apksigner verify`, final `zipalign -c` PASS; prod URL markers present, local markers absent.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260726-160500-CATEGORY-ANALYTICS-POSTP2-manual-install.apk`; SHA256 `188eae471e36f1cdfe2e4f92ce1f7da7e5fa1d1febb9c80ab5a96c494503d0b1`.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-category-analytics-postp2-qa-20260726-160224\SUMMARY.md`.
- **Ограничение:** эмулятор/устройство недоступны (`adb devices` пустой), поэтому install/launch/manual e2e не выполнялись; реальные production данные не менялись.

### Monthly investment transfers summary QA closure (2026-07-26)

- **Бизнес-правило:** `/reports/summary.investmentsTotal` теперь означает monthly investment transfers за выбранный период/month: только видимые incoming `transfer` в investment asset account/category. Это не общий баланс активов.
- **API boundary:** `/reports/account-balances` остаётся endpoint'ом балансов активов/счетов; Android Analytics summary investments берёт только summary data и не fallback-ит из account-balances.
- **Backend REQUIRED:** production backend deploy требуется, чтобы новая семантика `/reports/summary.investmentsTotal` стала active в production. Этот worker production deploy не выполнял.
- **QA:** backend targeted reports/assets `25 passed, 8 warnings`; backend full `302 passed, 16 warnings`; Android targeted `ApiClientDashboardTest`/`AppSectionTest` PASS; Android full unit `174 tests, 0 failures/errors/skipped`; `:app:compileDebugKotlin` PASS; release assemble/sign/align/URL scan PASS.
- **APK:** `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260726-221828-MONTHLY-INVESTMENT-TRANSFERS-manual-install.apk`; SHA256 `46e85ee4e5c6b4b13cf84abd4da22dcffc2642d0e9afd7d6be16f5c40783a9ca`.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\monthly-investment-transfers-qa-20260726-221828\SUMMARY.md`.
- **Ограничение:** `adb` не был доступен в PATH; SDK adb доступен, но attached devices/emulator отсутствуют, поэтому install/launch smoke не выполнялся; реальные production данные не менялись.

### Monthly investment transfers backend production deploy (2026-07-26)

- **Статус:** backend production deploy successful through GitHub Actions; direct local SSH/SCP не использовался.
- **Branch:** `prod/finance-monthly-investment-transfers-release-20260726`.
- **Commit:** `6a8d2656a4423d80363fb5230f2bb5ddcc8bd937`.
- **Release ID:** `20260726T194858Z-6a8d2656`.
- **Actions run:** `https://github.com/DmtrGoltsev/finance/actions/runs/30217638420`; run status `completed/failure` только из-за unrelated `frontend-ci-package`/PWA tests; `backend-ci-package` success и `deploy-backend` success.
- **Health/API:** `http://45.10.110.42/finance-api/health` -> 200 `{"status":"ok"}`; `http://45.10.110.42/finance-api/openapi.json` -> 200; unauth `/finance-api/api/v1/reports/summary` -> 401, route mounted/authenticated.
- **Migrations/backup:** Alembic before `20260618_0017`, target `20260618_0017`; workflow ran no-op upgrade validation and created backup `/opt/finance/backups/postgres/finance_prod-20260726T195057Z-20260726T194858Z-6a8d2656-20260618_0017-to-20260618_0017.dump`, SHA256 `209f7587277bec2b0e81e464e0da6f81d49ce1cafebede0648f0dab133111553`; evidence file `/opt/finance/backups/postgres/finance_prod-20260726T195057Z-20260726T194858Z-6a8d2656-20260618_0017-to-20260618_0017.dump.evidence.txt`.
- **Frontend caveat:** PWA job failed on existing date-sensitive tests in `apps/web-pwa/src/App.test.tsx:709` and `:799`; frontend deploy skipped. Backend deploy is successful.

### PWA server-first iPhone browser parity closure (2026-07-27)

- **Статус:** PASS после post-fix проверки `TopCategoriesDialog` portal/layer; деплой, commit и push не выполнялись.
- **Scope:** PWA iPhone browser parity для server-first сценариев login/home/quick add/category overlay/analytics/top categories all. Backend code в этой PWA parity задаче не менялся.
- **Android features covered in PWA parity:** быстрый выбор категории через `Категория` searchable overlay, mobile quick add sheet, analytics summary cards, `Главная -> Топ категории -> Все` со server category breakdown.
- **QA:** `npm.cmd test` в `apps/web-pwa` PASS: 4 files, 65 tests; `npm.cmd run build` PASS: `tsc -b && vite build`, 1704 modules; local Vite `http://127.0.0.1:5173/`; Playwright Chromium iPhone 14 smoke PASS.
- **TopCategoriesDialog proof:** dialog overlays FAB and bottom nav by hit-test; inner `.listStack` scrolls inside dialog (`clientHeight=570`, `scrollHeight=2594`, `after=2024`); screenshots include initial and scrolled states.
- **Evidence:** `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\pwa-iphone-parity-postfix-qa-20260727-005600\SUMMARY.md`.
- **Residual risks:** реальный iPhone/Safari руками не прогнан; production HTTPS/secure-cookie/service-worker/installability остаются риском, если prod доступен только по plain HTTP IP; PWA/iOS OCR остается online-only и не был перепроверен этим smoke.
