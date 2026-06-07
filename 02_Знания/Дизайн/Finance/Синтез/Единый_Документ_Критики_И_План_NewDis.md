---
id: "finance-design-synthesis-newdis-20260608"
тип: "дизайн-синтез"
проект: "Finance"
статус: "активно"
ветка_исполнения: "newDis"
создано: "2026-06-08"
обновлено: "2026-06-08"
уверенность: "высокая"
роль: "Design Synthesis Agent"
метод: "кворум 6 дизайн-критик + journey map + KB/release evidence"
теги: ["finance", "design", "critique", "quorum", "newDis", "ux-plan"]
источники:
  - "[[Критика_01_Навигация_IA]]"
  - "[[Критика_02_Формы_И_Скорость]]"
  - "[[Критика_03_Визуальная_Иерархия]]"
  - "[[Критика_04_Privacy_Shared]]"
  - "[[Критика_05_Planning_Analytics]]"
  - "[[Критика_06_Ошибки_OCR_Сервисный_Путь]]"
  - "[[Карта_Пользовательских_Путей_Finance]]"
  - "[[Пакет_Finance_Полный]]"
  - "[[Кворум_Finance]]"
  - "[[Док_Release_Planning_MVP_20260607]]"
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Пакет_Finance_Полный]]"
  - "[[Карта_Пользовательских_Путей_Finance]]"
---

# Единый документ критики и дизайн-план NewDis

## Назначение

Этот документ сводит 6 независимых дизайн-критик Finance в один исполнимый план для ветки `newDis`. Он не заменяет исходные критики: он фиксирует кворум, приоритеты, границы первой итерации и доказательства, которые должны быть принесены после реализации.

Контекст релиза: актуальная поставка `20260607T225457Z-819b5815`, project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`. Planning iteration MVP подтвержден production release, но authenticated login/OCR smoke не запускался, Android APK debug-signed, public/security GO остаются отдельными gates.

## Правило кворума

- 4-6 совпадений между критиками = обязательное изменение для `newDis`.
- 3 совпадения = сильная рекомендация; включать в первую итерацию, если не конфликтует с обязательными изменениями и scope.
- 2 совпадения = гипотеза для проверки; проектировать/тестировать, но не считать обязательным без дополнительного evidence.
- 1 совпадение = заметка; не включать в план без нового доказательства.
- Если severity `P0` указан одним агентом, но не подтвержден другими, это risk review, а не автоматический план.

## Источники

| Источник | Роль в синтезе |
|---|---|
| [[Критика_01_Навигация_IA]] | IA, первый экран, Planning visibility, PWA/Android parity, Settings mobile, wording boundaries. |
| [[Критика_02_Формы_И_Скорость]] | Quick Add, disabled/error states, transfer validation, OCR privacy mismatch, planning form load. |
| [[Критика_03_Визуальная_Иерархия]] | Scope as visual invariant, planning hierarchy, empty states, transfer visual neutrality, tokens. |
| [[Критика_04_Privacy_Shared]] | Personal/shared trust boundary, Overview read-only, report fallback, transfer visibility, household copy. |
| [[Критика_05_Planning_Analytics]] | Planning semantics, allocation-level progress, summary wording, surplus proposal-only, analytics/planning split. |
| [[Критика_06_Ошибки_OCR_Сервисный_Путь]] | OCR service path, production smoke gap, recovery states, offline/loading, stale release copy. |
| [[Карта_Пользовательских_Путей_Finance]] | User journeys and screen map for Android/PWA. |
| [[Пакет_Finance_Полный]], [[Док_Release_Planning_MVP_20260607]] | Release facts, QA gate, residual risks, Planning acceptance clarification. |

## Матрица кворума

| Тема | Кворум | Критики | Статус | Вывод |
|---|---:|---|---|---|
| `Overview` read-only: нельзя сохранять записи, планы, счета или категории в обзор | 5/6 | 01, 02, 03, 04, 05 | Обязательное | Во всех write-flow оставить только `Личное` и `Общее`; из Overview открывать явный scope chooser. |
| Scope/privacy должен быть видимым на экранах, карточках и результатах сохранения | 6/6 | 01, 02, 03, 04, 05, 06 | Обязательное | Scope badge и copy становятся системным UX-инвариантом. |
| Empty/error/disabled states должны объяснять next-best-action и текущий scope | 6/6 | 01, 02, 03, 04, 05, 06 | Обязательное | Общие тексты "нет данных" заменить на state-specific copy с CTA/recovery. |
| OCR должен звучать как черновик на проверку, не импорт и не автосоздание операций | 5/6 | 01, 02, 03, 04, 06 | Обязательное | Уточнить privacy truth source, copy, recovery, pending draft semantics. |
| Planning progress только allocation-level; summary/surplus не должны читаться как plan-level progress или перенос денег | 4/6 | 01, 02, 03, 05 | Обязательное | Запретить plan-level progress bar/copy; `previousMonthSurplus` показывать как proposal-only. |
| Transfer должен быть нейтральным типом и проходить preflight до submit | 4/6 | 01, 02, 03, 04 | Обязательное | Не окрашивать как расход/доход; фильтровать incompatible accounts; не раскрывать hidden side. |
| Planning должен быть явным рабочим путем, а не спрятанным хвостом Analytics | 3/6 | 01, 03, 05 | Сильная рекомендация | Дать заметный вход "План месяца" из Home/Analytics; PWA parity решить явно. |
| Quick Add должен быть быстрее без опасных defaults/demo auto-create | 3/6 | 01, 02, 04 | Сильная рекомендация | Убрать default `1000`, auto-create demo entities и generic "Добавить" как единственный путь. |
| Analytics и Overview нужно развести по смыслу | 3/6 | 01, 03, 05 | Сильная рекомендация | Overview = "сейчас и действия"; Analytics = период, структура, сравнение. |
| Household/shared onboarding copy | 2/6 | 03, 04 | Гипотеза | Добавить точечно в shared empty/settings, но не делать отдельный onboarding в первой итерации. |
| Cross-platform visual tokens | 1/6 | 03 | Заметка | Не включать как отдельный крупный redesign; применять локально для scope/finance polarity. |
| PWA mobile Settings access | 1/6 | 01 | Заметка | Проверить в QA; чинить в `newDis`, если подтверждается навигационный blocker. |

## Prioritized changes

### P0 - must fix / risk-contained before public UX claims

1. **Сделать `Overview` read-only во всех write paths.**
   - Android Quick Add, category/account creation, planning actions: только `Личное`/`Общее`.
   - Если action начат из Overview, показывать выбор "куда сохранить" без silent fallback в personal.
   - После сохранения показывать результат: "Сохранено в личное" или "Сохранено в общее".

2. **Привести OCR privacy/copy к фактической архитектуре.**
   - Если Android OCR реально отправляет изображение на backend, нельзя обещать on-device OCR.
   - Если on-device OCR является продуктовым обещанием, реализация/QA должны это подтвердить до публичной copy.
   - До подтверждения использовать честную временную формулировку: screenshot обрабатывается как OCR-запрос, raw не должен сохраняться, результатом являются черновики на проверку.

3. **Закрыть privacy-sensitive fallback-и в PWA/UI.**
   - `reportForView` не должен отдавать `snapshot.reports[0]` при mismatch режима.
   - Transfer row не должен показывать hidden counterparty/account labels; для MVP показывать transfer только при видимости обеих сторон или нейтрализовать скрытую сторону.
   - Empty states не должны раскрывать hidden counts или намекать, что у другого участника есть данные.

4. **Защитить Planning от ложного plan-level progress.**
   - Любой progress/status показывать на allocation-level: plan/fact/variance/status/attention reason.
   - Summary и `previousMonthSurplus` не называть переносом денег или прогрессом месяца.
   - P0 из [[Критика_05_Planning_Analytics]] считать risk review там, где это только wording/visual risk; автоматический P0 возникает только при фактическом plan-level progress или обещании переноса.

### P1 - first iteration scope

1. **Scope badge everywhere it matters.**
   - Home/Overview, Operations, Assets, Categories, Analytics, Planning.
   - Rows/cards: accounts, categories, operations, capture drafts, planning plans/allocations.
   - Copy for Overview: "Мой обзор: личное + общее, без личного другого участника" или эквивалент.

2. **Empty/error/disabled state library.**
   - Каждый state называет scope, причину и next action.
   - Examples: "В личном режиме видимых расходов нет. Добавьте расход или переключитесь на общее"; "Общий бюджет еще не подключен"; "Для перевода нужны два совместимых счета одного scope и валюты".
   - Disabled primary buttons рядом с формой объясняют, чего не хватает.

3. **Planning entry and hierarchy.**
   - Android: оставить Planning внутри Analytics допустимо, но добавить явный entry "План месяца" из Home/Analytics.
   - PWA: либо реализовать минимальный path `Analytics -> План`, либо явно зафиксировать Android-first limitation в UI/docs/release copy.
   - Planning layout: dominant summary/action, затем allocations/income, затем history/details.

4. **Quick Add / daily capture safety.**
   - PWA amount default empty, не `1000`.
   - No demo auto-create account/category in live flow; если данных нет, дать inline create или next-best-action.
   - Primary actions split by intent: `Расход`, `Доход`, `Перевод`, `Из скрина`; generic `Добавить` не должен быть единственным смысловым entry.

5. **Transfer distinction and validation.**
   - Preflight same-scope/same-currency before submit.
   - Destination list filters incompatible accounts or explains no compatible accounts.
   - Transfer rows visually neutral and do not feed expense analytics.

6. **OCR service path polish.**
   - Replace "импорт" with "скрин расходов", "OCR", "черновики".
   - Confidence/evidence hash should tell the action: check, edit, confirm/discard.
   - Failed OCR should distinguish unsupported file, no candidates, network/backend, unauthorized/session, offline/PWA limitation.
   - Preserve review state after recoverable failure where feasible.

### P2 - later or opportunistic

1. Minimal cross-platform tokens for scope and money polarity.
2. Household explainer in shared empty/settings without a heavy onboarding flow.
3. Repeat-last suggestions for daily expenses, without pre-filling amount as fact.
4. Mobile Settings access audit and fix if current PWA has a real access trap.
5. Documentation sync after IA decision: Android/PWA README, user guide, journey map.
6. Screenshot matrix expansion for Planning and privacy states.

## Что НЕ менять

- Не делать landing page или marketing hero: первый экран остается рабочим обзором финансов.
- Не расширять MVP в bank API, SMS/push interception, Excel/CSV/PDF import или автоматическое создание операций.
- Не добавлять hidden counts, "часть данных скрыта", member contribution или household-wide personal totals.
- Не превращать combined overview в данные всей семьи; это viewer-specific aggregate.
- Не возвращать account target как основной выбор для новых Planning allocations; source of truth: expense category или investment asset category.
- Не добавлять plan-level progress bar.
- Не обещать инвестиционные рекомендации, доходность, налоговую аналитику, котировки или переоценку активов.
- Не раздувать bottom navigation до 6-7 top-level items; сложность решать entry points, subnav и copy.
- Не скрывать release limitations: debug-signed APK, missing authenticated production login/OCR smoke, public/security GO отдельно.

## Implementation plan for `newDis`

### Android write scope

- `apps/android/.../FinanceApp.kt`
  - Remove `Overview` from Quick Add/write visibility choices.
  - Add explicit scope chooser when writing from Overview.
  - Add scope result copy after create/update.
  - Improve transfer validation visibility and neutral transfer presentation.
  - Replace OCR "Импорт" wording with screenshot/draft wording.
  - Add scope-aware empty/error/disabled messages.
- `apps/android/.../PlanningUi.kt`
  - Keep Overview as read-only gate; ensure selector/copy does not present it as writable plan scope.
  - Remove or reword anything that reads as plan-level progress.
  - Improve allocation rows: plan, fact, variance/status, attention reason.
  - Make `previousMonthSurplus` proposal-only in copy.
- Android tests
  - Unit/screenshot assertions for no Overview in write forms, Planning allocation semantics, transfer validation copy, OCR draft copy.

### PWA write scope

- `apps/web-pwa/src/App.tsx`
  - Remove amount default `1000`.
  - Move scope control out of advanced/details where it affects write trust.
  - Replace report mode fallback with mode-specific empty/error state.
  - Filter or neutralize transfer rows when one side is hidden.
  - Add scope badges and scope-aware empty states.
  - Add Planning entry/parity decision: minimal `Analytics -> План` or explicit Android-first limitation.
  - Ensure Settings/privacy/logout remain accessible on mobile if current layout hides them.
- `apps/web-pwa/src/styles.css`
  - Add only necessary token-level support for scope badges, neutral transfer rows, empty/error states.
- PWA tests
  - Vitest/Playwright for mode mismatch, no hidden transfer labels, no default amount, OCR draft copy, mobile layout.

### Backend/API write scope

- No broad backend redesign is required by design alone.
- Backend work is allowed only where UI safety depends on contract/runtime behavior:
  - mode-specific report errors or empty responses instead of ambiguous fallback;
  - transfer visibility guarantees if client-only filtering is insufficient;
  - OCR privacy/retention evidence endpoint/copy source if current docs and runtime disagree;
  - tests proving filter-before-aggregate and neutral denial remain intact.

### Docs/KB write scope

- `docs/user-guide-ru.md`, `docs/product-mvp.md`, `docs/current-status.md`, release notes:
  - align OCR architecture truth, Planning PWA/Android limitation, scope wording.
- Vault:
  - update [[Карта_Пользовательских_Путей_Finance]] after implementation evidence.
  - keep this document linked from [[MOC_Finance]] and [[Пакет_Finance_Полный]].

## Acceptance criteria

- No write form offers `Overview` as a saved visibility/scope.
- Writing from Overview requires explicit `Личное` or `Общее`.
- Every created/updated financial object shows scope in result copy or row/card badge.
- `Мой обзор` copy cannot be read as "all family personal data".
- Planning has no plan-level progress bar/copy; progress/status is allocation-level.
- `previousMonthSurplus` is proposal-only in UI copy.
- PWA no longer falls back to first report on report mode mismatch.
- Transfer creation filters/explains incompatible accounts before submit.
- Transfer rows are visually neutral and do not reveal hidden account/counterparty names.
- OCR copy says screenshot/draft/review/confirm, not import/autocreated operations.
- OCR architecture/privacy copy matches actual processing path.
- Empty/error/disabled states include scope, cause and next action.
- PWA amount field opens empty for Quick Add unless user explicitly repeats a previous operation.
- PWA/Android docs use the same vocabulary for `Личное`, `Общее`, `Мой обзор`, `Операции`, `Активы`, `Категории`, `Аналитика`, `План`.

## QA and evidence requirements

| Area | Required evidence |
|---|---|
| Android build/tests | `:app:testDebugUnitTest`, `:app:assembleDebug`; targeted tests for Overview removal and Planning semantics. |
| PWA tests | Unit tests for report fallback, Quick Add defaults, transfer visibility; Playwright desktop/mobile screenshots. |
| Backend/API | Existing backend suite remains green; targeted privacy/report/transfer tests if backend touched. |
| OCR | Authenticated login/OCR smoke when credentials/session token are available; evidence must state whether OCR is on-device or backend. |
| Privacy | Actor matrix: Owner A, Member B, Other C, Invited, Former across personal/shared/overview, no hidden counts. |
| Visual QA | Screenshots for Home, Operations, Assets, Categories, Analytics, Planning on Android and PWA mobile/desktop. |
| Release evidence | Link final evidence into [[QA_Фиксы]] or a new evidence note; update [[Пакет_Finance_Полный]] only after verified implementation. |

## Risks and escalation triggers

| Severity | Risk | Escalation trigger |
|---|---|---|
| P0 | Personal data leak through overview, transfer labels, report fallback, empty states or aggregates. | Any UI/API path reveals another member's personal account/category/transaction/aggregate, even indirectly. |
| P0 | OCR privacy claim is false. | UI/docs say on-device while runtime sends screenshot to backend, or raw retention is unclear. |
| P0 | `Overview` writes data silently. | Any save/create action from Overview maps to personal/shared without explicit user choice. |
| P1 | Planning UX contradicts release acceptance. | Plan-level progress/copy appears, or surplus is presented as real money transfer. |
| P1 | PWA promises Planning but has no usable path. | Product copy/release/user guide says Planning is available on PWA while UI has no entry. |
| P1 | Transfer gets counted/read as expense. | Timeline/analytics coloring/copy makes transfer look like spending. |
| P1 | Production public/security GO is implied by functional GO. | Docs/UI omit debug-signed APK, missing auth OCR smoke, or security gate limitations. |
| P2 | Density/visual tokens reduce scanability. | New badges/chips make 390px mobile layouts overflow or obscure primary actions. |

## Open questions

1. What is the authoritative OCR architecture for Android in `newDis`: on-device OCR, backend OCR, or temporary hybrid?
2. Should PWA implement minimal Planning in `newDis`, or should release/UI copy explicitly mark Planning as Android-first for this iteration?
3. Who owns the final wording for `Обзор`: `Мой обзор`, `Видимое мне`, or another product term?
4. Are transfer rows with one hidden side impossible by backend invariant, or should client still harden against legacy/stale snapshots?
5. What authenticated production credentials/session will be used for login/OCR smoke evidence?
6. Is release-signed Android artifact in scope for `newDis`, or remains a separate public release gate?

## Recommended execution order

1. Privacy guardrails: Overview read-only, report fallback, transfer hidden-side hardening.
2. OCR truth source and copy, including smoke evidence plan.
3. Planning semantics: allocation-level only, surplus proposal-only, entry path decision.
4. Quick Add/form safety: no default amount, no demo auto-create, visible validation.
5. Empty/error/disabled state pass across Android/PWA.
6. Visual polish: scope badges, neutral transfer rows, lightweight tokens.
7. Docs and KB sync after evidence.

## Definition of Done

`newDis` is done when mandatory quorum items are implemented or explicitly risk-accepted with owner/date, all P0/P1 acceptance criteria have evidence, and MOC/package/journey/docs no longer overpromise Planning, OCR, privacy or production readiness.
