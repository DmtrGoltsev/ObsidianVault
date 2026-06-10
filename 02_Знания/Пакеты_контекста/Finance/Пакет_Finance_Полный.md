---
id: "context-package-finance-full"
тип: "пакет_контекста"
проект: "Finance"
название: "Пакет Finance — Полный контекст"
создано: "2026-06-01"
обновлено: "2026-06-08"
уверенность: "высокая"
теги: ["пакет_контекста", "finance", "агрегация"]
источники:
  - "[[Источник_README]]"
  - "[[Источник_Продукт_MVP]]"
  - "[[Источник_Текущий_Статус]]"
  - "[[Источник_ADR_0001]]"
  - "[[Источник_Security_Baseline]]"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
  - "[[Кворум_Finance]]"
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
  - "[[Док_Release_NewDis_20260608]]"
  - "[[Док_Release_Planning_MVP_20260607]]"
  - "[[Карта_Пользовательских_Путей_Finance]]"
  - "[[Единый_Документ_Критики_И_План_NewDis]]"
---

# Пакет Finance — Полный контекст

Агрегирующая заметка, собирающая все ключевые ссылки по проекту Finance.

## Проект

- [[Finance]] — главная заметка проекта

## Навигация

- [[MOC_Finance]] — MOC-карта проекта
- [[Карта_Пользовательских_Путей_Finance]] — UX journey map для дизайнеров
- [[Единый_Документ_Критики_И_План_NewDis]] — кворум-синтез дизайн-критики и план для `newDis`
- [[Док_Release_NewDis_20260608]] — sanitized closure/evidence для release `newDis`

## Источники

| Источник | Файл |
|----------|------|
| [[Источник_README]] | `README.md` |
| [[Источник_Продукт_MVP]] | `docs/product-mvp.md` |
| [[Источник_Текущий_Статус]] | `docs/current-status.md` |
| [[Источник_ADR_0001]] | `docs/architecture/decision-records/adr-0001-stack-repo-layout.md` |
| [[Источник_Security_Baseline]] | `docs/security/security-baseline.md` |

## Глоссарий

| Термин | Определение |
|--------|------------|
| [[Household]] | Семейное пространство |
| [[Personal_Shared]] | Личное vs совместное |
| [[Transaction]] | Финансовая операция |
| [[Transfer]] | Перевод между счетами |
| [[Capture_Draft]] | OCR черновик |

## Кворум

- [[Кворум_Finance]] — кворум-саммари с высокой уверенностью

## Release context (2026-06-08)

| Область | Статус |
|---------|--------|
| Code branch | `newDis` |
| Production frontend commit | `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Android APK fix commit | `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`), branch `newDis`, remote parity OK |
| Previous Android UX fix commit | `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`), branch `newDis`, remote parity OK |
| Previous Android final fix commit | `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`), branch `newDis`, remote parity OK |
| Latest finance fix commit | `09ea6479451c61b3d06a412e5aaaecec534fc96a` (`fix(finance): compact investment asset categories`), branch `newDis`, remote parity OK |
| Current release scope | UX simplification release; production frontend byte parity; backend redeploy waiver because final HEAD has no backend/db/api delta |
| Backend/API | `/finance-api/health` 200 `{status:ok}`; exact commit endpoint absent; route surface matches post-808/newDis |
| PWA/frontend | `/finance/COMMIT` 200 -> `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; `/finance/`, `/finance/sw.js`, manifest, JS/CSS byte-hash equal local `apps/web-pwa/dist` |
| QA | Compact asset category backend targeted suite: `31 passed, 2 warnings`; Android `:app:testDebugUnitTest` successful; `:app:assembleDebug` successful; integration review P0/P1 clean; P2 staging risk handled by curated commit; PWA/backend/OpenAPI reports are historical unless stated otherwise |
| Android APK final | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`; size `54,235,740`; SHA256 `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733`; debug-signed; production API base present; dev URLs absent |
| Release evidence | [[Док_Release_NewDis_20260608]] |

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19). Текущая поставка 2026-06-08 — `newDis` UX simplification + compact investment asset category/iconKey/analytics fix — закрыта с production frontend byte parity, backend redeploy waiver и latest finance addendum `09ea6479451c61b3d06a412e5aaaecec534fc96a`; подробности в [[Док_Release_NewDis_20260608]].

## Release newDis (текущий контекст)

- Project commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b` (`feat(finance): simplify newDis UX flows`), branch `newDis`, `HEAD = origin/newDis`.
- Android APK prod-path fix commit `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`) pushed on branch `newDis`; `/finance/COMMIT` remains web context `6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- Android UX fix commit `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`) pushed on branch `newDis`; changed only `ApiClient.kt` and `FinanceApp.kt`; superseded by final correction APK.
- Android final correction commit `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`) pushed on branch `newDis`; changed `AndroidManifest.xml`, `ApiClient.kt`, `FinanceApp.kt`.
- Compact investment asset category fix commit `09ea6479451c61b3d06a412e5aaaecec534fc96a` (`fix(finance): compact investment asset categories`) pushed on branch `newDis`; remote parity OK.
- Production frontend: `/finance/COMMIT` возвращает commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; `/finance/`, `/finance/sw.js`, manifest и JS/CSS assets byte-hash equal local `apps/web-pwa/dist`.
- Backend health: `/finance-api/health` 200 `{status:ok}`; exact commit endpoint отсутствует, принят waiver, потому что final HEAD не содержит backend/db/api delta.
- Android UX fixes: custom Saver for `AddAccountState?`, explicit category edit icon and investment checkbox, keyboard-safe AddAccountSheet, safe trash+confirmation archive flow, non-empty category archive block, long-press drag reorder with local `SharedPreferences` persistence.
- Android final correction: legacy group like `Вклад` can show `Инвестиция` checkbox; checkbox off keeps rename-only, checkbox on converts to `isInvestment=true` real asset category and links active legacy accounts; empty/mixed-currency/overview/no writable scope blocked; rollback archives created category after link failure.
- Android IME final correction: `adjustResize`, `skipPartiallyExpanded`, `imePadding`, `navigationBarsPadding`, repeated `BringIntoView`, larger spacer; Material3 `windowInsets` fallback.
- Compact investment asset categories: compact `AssetCategoryGroupCard`, simplified edit mode, manual amount hidden for linked accounts, linked accounts list removed from category edit/card, investment badge with trending-up icon, icon picker and persisted `asset_categories.icon_key`, analytics fixed by backend-contract investment totals parsing and no forced Android currency filter.
- Android QA: backend targeted suite `31 passed, 2 warnings`; `:app:testDebugUnitTest` successful; `:app:assembleDebug` successful; integration review P0/P1 clean; P2 staging risk handled by curated commit; lint historical `0 errors`, 6 warnings.
- APK: `finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733`, `applicationId=com.finance.mvp`, `versionName=0.1.0`, `minSdk=26`, `targetSdk=34`; production API base present, dev URLs absent.
- Limits: full PWA install/service worker proof requires HTTPS/domain; authenticated production login/OCR smoke and retention/privacy evidence остаются отдельными gates; actual recents/keyboard/drag/confirmation dialogs plus visual IME and live legacy migration need device or emulator manual QA; compact card/edit mode/icon picker/investment badge need visual screenshot/device check; APK debug-signed.

## Release Planning iteration MVP (текущий контекст)

- Project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8` (`Release planning iteration MVP`), branch `codex/finance-planning-mvp-gpt5` запушен в `origin`.
- Backend current: `/opt/finance/releases/20260607T225457Z-819b5815`; web current: `/var/www/finance/releases/20260607T225457Z-819b5815`; оба prod `COMMIT` файла указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8`.
- Alembic head: `20260607_0013 (head)`.
- Production checks: service active, health direct/nginx OK, `/finance/` 200, manifest scope/start_url `/finance/`, `/finance/sw.js` 200.
- QA evidence: OpenAPI parse OK, operationId duplicates `0/58`, backend `243 passed, 9 warnings`, Android unit PASS, Android `assembleDebug` PASS.
- Acceptance clarification: planning progress является allocation-level (`PlanningAllocationDto.actualAmount`/`varianceAmount`/`status`/`attentionReason`), не `PlanningPlanDto.progress`; `previousMonthSurplus` находится в `PlanningSummaryDto`.
- Release evidence: [[Док_Release_Planning_MVP_20260607]].
- Residual risk: authenticated QA login/OCR smoke не запускался из-за отсутствия operator password/session token; APK debug-signed.

## Asset categories + Analytics/Planning polish (текущий контекст)

- Asset categories — source of truth: `manualAmount` для пустых категорий, `isInvestment`, `assetType`, связь `account.assetCategoryId`; удалённые счета не дают stale totals.
- Latest compact category update: `icon_key` persisted through backend/API/Android; manual amount hidden when linked accounts exist; linked accounts list removed from compact card/edit; investment badge uses trending-up icon.
- Backend/API: `reportMode=personal`, asset-categories endpoints, миграция `20260607_0012`.
- Analytics: investments metric; capital structure отображается только в Analytics.
- Categories: создание учитывает scope `personal`/`household`; редактирование через edit icon.
- Planning: income day = день месяца; income form скрыта за Add; новые allocations выбирают expense category или investment asset category, без account target; history text уточнён.
- QA evidence: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`, APK SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26`.
- Release boundary: production deploy текущей поставки подтверждён; `/opt/finance/current` указывает на `/opt/finance/releases/20260607T163043Z-be9f8ab`.

## Planning MVP (текущий контекст)

- Вкладка Analytics получила Planning flow: personal/shared scope, income sources, allocations, history/copy, локальные Android reminders.
- Backend/API включает planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, OpenAPI planning endpoints и authz/validation правила.
- Allocation targets для новых allocations поддерживают expense categories и investment asset categories; account target больше не предлагается для новых allocations.
- Миграция release: `20260607_0011_planning_allocation_asset_target.py`.
- Android flow расширен выбором и созданием asset/investment из planning flow.
- QA evidence по Planning лежит в [[QA_Результаты#Волна 3 Аналитика - Планирование MVP (2026-06-06)]], [[QA_Фиксы#Волна 4 (2026-06-07)]] и [[QA_Фиксы#Волна 5 (2026-06-07)]]. Актуальные цифры текущей поставки: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`.

## Риски

P1-B02, P1-B03, tag misalignment; production deploy текущей поставки подтверждён release agent.

## Release context update (2026-06-10)

- Latest project commit on `newDis`: `1013e632d54c6af6ed9326d8b7f761bdd381bade`.
- Regression fix scope: expanded asset category card restores linked account rows (`Вклад` should show 4 linked accounts), edit mode keeps no account list, legacy `Карта`/`Банк` visibility avoids duplicates with real backend categories, category-level `isInvestment` save/local state updates `Брокер` badge/state and analytics inputs, `План месяца` blocks past months and clamps persisted/selected past month to current-or-future, missing plan 404 becomes friendly empty state.
- Russian input: no app-level Cyrillic filter found; AVD `Codex` had `hw.keyboard=yes`; likely emulator/IME configuration. Suggested workaround is Russian Android keyboard or `show_ime_with_hard_keyboard` / disabling hardware keyboard.
- QA evidence: `:app:compileDebugKotlin` SUCCESS; `:app:testDebugUnitTest` SUCCESS; packaging unit SUCCESS (`BUILD SUCCESSFUL in 2s`); packaging assembleDebug with `-PfinanceApiBaseUrl=http://45.10.110.42/finance-api` SUCCESS (`BUILD SUCCESSFUL in 36s`); review no P0/P1, P2 only missing UI/Compose coverage.
- APK: `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk`, size `54,235,740`, SHA256 `FCD7EE0D870A12B3B88416DAEBCB3CF35FC513618C865B427E30E5F77F688411`; prod URL found in `classes7.dex` and `classes5.dex`; dev URLs absent; installed on AVD `Codex` (`emulator-5554`) as `com.finance.mvp`.
- Residual risks: no prod auth/DB access during data-check, no UI/Compose automated visual regression coverage, Russian input likely emulator settings rather than app bug.
