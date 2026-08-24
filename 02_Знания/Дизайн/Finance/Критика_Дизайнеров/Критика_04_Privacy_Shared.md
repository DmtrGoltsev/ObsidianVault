---
id: "finance-design-critic-04-privacy-shared"
тип: "критика_дизайнера"
проект: "Finance"
роль: "Designer Critic 04"
специализация: "private/shared money, trust, household privacy"
создано: "2026-06-08"
обновлено: "2026-06-08"
статус: "draft"
уверенность: "средняя"
источники:
  - "C:/Users/style/Documents/ObsidianVault/README.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Пакеты_контекста/Finance/Пакет_Finance_Полный.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Пакеты_контекста/Finance/Кворум_Finance.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Глоссарий/Finance/Personal_Shared.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Глоссарий/Finance/Household.md"
  - "README.md"
  - "docs/product-mvp.md"
  - "docs/architecture/domain-model.md"
  - "docs/architecture/report-api-contracts.md"
  - "docs/architecture/backend-authz-predicates.md"
  - "docs/compliance/privacy-flows-mvp.md"
  - "docs/security/security-baseline.md"
  - "docs/testing/wave-2-fixture-evidence-matrix.md"
  - "qa/fixtures/owner-member-other-invited-former-v1/goldens/report-expected.json"
  - "apps/web-pwa/src/App.tsx"
  - "apps/web-pwa/src/api/client.ts"
  - "apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt"
  - "apps/android/app/src/main/java/com/finance/mvp/ui/PlanningUi.kt"
  - "apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt"
  - "apps/backend/src/app/reports/service.py"
  - "apps/backend/src/app/authz/predicates.py"
  - "apps/backend/tests/reports/test_reports_runtime_safety.py"
  - "apps/web-pwa/src/App.test.tsx"
  - "apps/android/app/src/test/java/com/finance/mvp/ui/AppSectionTest.kt"
теги: ["finance", "design-critique", "privacy", "shared-money", "household", "trust"]
---

# Критика 04: Privacy / Shared Money / Household Trust

## Вывод

Backend-модель и документация уже хорошо держат главный privacy-инвариант: personal owner-only, shared active-only, filter-before-aggregate. Самый хрупкий слой для доверия сейчас не в SQL-агрегации, а в UX: режимы называются коротко, но не всегда объясняют границы; Android quick add допускает `Обзор` как видимость записи; empty states не всегда говорят, что именно пусто: видимые данные, общий бюджет или семейный доступ.

Главное правило дизайна: пользователь не должен гадать, куда попадет запись и чьи деньги он сейчас видит. Для Finance это не cosmetic polish, а trust boundary.

## Критические наблюдения

### 1. P0 - Android quick add дает выбрать `Обзор` как видимость записи

**Проблема.** В `QuickAddSheet` Android visibility chips строятся из всех `FinanceMode`, включая `Overview`. При submit `Overview` не является shared и silently мапится в personal через условие `draft.visibility == FinanceMode.Shared ? householdId : null`. Пользователь может думать, что добавляет в сводный/семейный контекст, а запись, счет или категория создаются как personal. Это прямой риск ошибочного создания семейных данных и потери доверия к scope.

**Evidence paths.**
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2936` - `visibility` по умолчанию personal.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2996` - chips показывают все `FinanceMode.entries`, включая `Overview`.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:509`, `522`, `550-553` - только `Shared` получает householdId; все остальное становится personal.

**Рекомендация.** В любых write-формах оставить только `Личное` и `Общее`; `Обзор` должен быть read-only режимом. Если пользователь открыл quick add из Overview, форма должна заставить выбрать `Личное` или `Общее` с коротким объяснением.

### 2. P1 - `Обзор` звучит как "все семейные деньги", хотя это viewer-specific aggregate

**Проблема.** Документы точно говорят, что `combined_viewer_overview` включает shared household + personal текущего пользователя, но не personal второго участника. UI показывает короткое "Обзор" / "Сводный обзор". Этого недостаточно в продукте про семейные финансы: пользователь может читать цифру как "общий семейный капитал".

**Evidence paths.**
- `docs/product-mvp.md:61-62` - personal-агрегаты другого участника не раскрываются; два явных режима отчетов.
- `docs/architecture/domain-model.md:276-279`, `345-347` - `combined viewer overview` не включает personal другого участника.
- `apps/web-pwa/src/App.tsx:537-570`, `2070-2075` - switch и description: `Обзор`, `Сводный обзор`.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:3222-3225` - Android enum: `Личное`, `Общее`, `Обзор`.

**Рекомендация.** Переименовать или дополнить `Обзор`: "Мой обзор: личное + общее" / "Видимое мне". Не использовать "семейный обзор" для combined mode.

### 3. P1 - PWA fallback отчета может скрыть mismatch режима

**Проблема.** `reportForView` для shared/overview ищет нужный report, но если не находит, берет `snapshot.reports[0]`. В privacy-продукте fallback на первый отчет опасен как UX-паттерн: пользователь может увидеть метрики другого режима под выбранным label.

**Evidence paths.**
- `apps/web-pwa/src/App.tsx:2084-2098` - `snapshot.reports.find(...) ?? snapshot.reports[0] ?? emptyReport(...)`.
- `apps/web-pwa/src/api/client.ts:754-775` - PWA получает `shared_family_report` и `combined_viewer_overview`.
- `docs/architecture/report-api-contracts.md:455-481` - report cache и mode должны кодировать полный visibility context.

**Рекомендация.** Если report нужного mode отсутствует, показывать mode-specific empty/error state, а не первый доступный report. Текст: "Не удалось получить отчет для выбранного режима".

### 4. P1 - Android dashboard пересчитывает overview client-side, не опираясь на report mode label

**Проблема.** Android `viewFor(Overview)` агрегирует локально `this` по всем accounts после загрузки dashboard. Если dashboard snapshot когда-либо содержит больше, чем actor-visible rows, UI не имеет отдельного UX-стопора. Backend может быть корректен, но дизайн не показывает, что это "видимое мне", а не "все".

**Evidence paths.**
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:3278-3310` - `viewFor` суммирует capital/income/expense/transactions из локального набора.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:3383-3388` - `Overview -> this`.
- `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt:505-515`, `525-535` - API dashboard берет combined overview при наличии household.

**Рекомендация.** В UI рядом с метриками overview показывать "только данные, доступные вам". Для QA требовать fixture, где A и B имеют одинаковые даты/суммы, чтобы ошибка фильтрации была видима.

### 5. P1 - PWA `visibleTransfers` показывает transfer, если видима хотя бы одна сторона

**Проблема.** `visibleTransfers` использует OR по source/counterparty account. Timeline title затем показывает `fromAccountName -> toAccountName`. Сейчас backend запрещает mixed-scope transfer, но UX-компонент сам по себе не защищает от будущего или legacy состояния, где одна сторона hidden. Это потенциальная утечка названия личного счета/counterparty.

**Evidence paths.**
- `apps/web-pwa/src/App.tsx:1975-1984` - transfer включается, если видима любая сторона.
- `apps/web-pwa/src/App.tsx:2031-2050` - timeline показывает оба account names.
- `apps/web-pwa/src/api/client.ts:961-979` - `mapTransfer` подставляет account names из snapshot.
- `docs/security/security-baseline.md:152-157` - personal/shared transfer является high privacy-risk; личная сторона не должна раскрываться.

**Рекомендация.** Для MVP показывать transfer только если обе стороны находятся в выбранном visible account set. Для будущих split-visibility transfers нужен отдельный редактируемый дизайн, где скрытая сторона отображается нейтрально.

### 6. P1 - Empty states слишком общие для privacy-sensitive режимов

**Проблема.** "Нет активов", "Пока нет расходов", "Категорий пока нет" не различают: у пользователя нет данных, нет household, нет доступа, фильтр скрывает чужие данные, или выбран shared mode без общего бюджета. В privacy UX пустота должна означать "нет видимых данных в этом scope", без намека на hidden counts.

**Evidence paths.**
- `apps/web-pwa/src/App.tsx:620`, `632`, `1284`, `1327`, `1493`, `1504`, `1928`.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1273`, `1652`, `1845`, `1864`, `2652`.
- `docs/architecture/backend-authz-predicates.md:215-218`, `245-253` - empty states считаются после access filter, без hidden counts.
- `docs/testing/wave-2-fixture-evidence-matrix.md:286-287` - empty states mean no visible data for current filter/scope.

**Рекомендация.** Стандартизировать copy: "В этом режиме видимых активов нет", "Общий бюджет еще не подключен", "Нет видимых расходов за период". Не писать "часть скрыта" или "у другого участника есть данные".

### 7. P1 - Household как термин остается техническим и не получает понятного onboarding boundary

**Проблема.** Глоссарий определяет household как семейное пространство active members, но UI в основном говорит "Общее" / "Общие финансы". Нет отдельного объяснения: кто участники, что становится видимым, что останется личным, что будет после выхода.

**Evidence paths.**
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Глоссарий/Finance/Household.md` - household = active members shared space.
- `apps/web-pwa/src/api/client.ts:352-356` - `householdName` как "Общие финансы" или "Личный режим".
- `docs/compliance/privacy-flows-mvp.md:110-143` - leave household и former access имеют отдельные privacy rules.

**Рекомендация.** Ввести short household explainer в settings/shared empty state: "Общее видно активным участникам семейного пространства. Личное не показывается семье".

### 8. P1 - Write path в PWA лучше Android, но scope explanation спрятан в `Еще`

**Проблема.** PWA quick add блокирует shared asset без household и disabled shared radio, но выбор видимости находится внутри details `Еще`. Для денег scope должен быть primary control, а не advanced field. Иначе пользователь сохраняет в default personal и потом не понимает, почему семья не видит запись.

**Evidence paths.**
- `apps/web-pwa/src/App.tsx:1611-1615` - submit guard для shared asset без household.
- `apps/web-pwa/src/App.tsx:1727-1751` - visibility fieldset находится в `details className="moreFields"`.
- `apps/web-pwa/src/App.tsx:240-258` - asset creation передает shared householdId только при shared visibility.

**Рекомендация.** Поднять visibility control выше `Еще` и показывать выбранный scope в submit button/status: "Сохранить в личное" / "Сохранить в общее".

### 9. P2 - Category management в Android не фильтрует список по выбранному режиму

**Проблема.** В Android category card есть chips `Личное/Общее`, но список `visibleCategories` фильтруется только по active status, не по выбранному mode. Это не обязательно data leak, если backend snapshot actor-visible, но UX ломает ментальную модель: пользователь выбирает "Общее", а видит личные категории рядом.

**Evidence paths.**
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2600-2607` - mode есть, но `visibleCategories` не применяет mode.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2627-2630` - UI показывает "Режим".
- `docs/architecture/domain-model.md:196-200`, `336-347` - категории имеют personal/household scope.

**Рекомендация.** Фильтровать список категорий по mode или явно разделить секции "Личное" и "Общее". На строке категории всегда показывать scope badge.

### 10. P2 - Planning хорошо блокирует Overview, но этот паттерн не перенесен на остальные write flows

**Проблема.** Planning уже правильно говорит: "Обзор не создает единый план" и направляет в личный/общий. Остальные write-flow, особенно Android quick add, не используют этот же запрет. Это создает inconsistent trust: в одном месте overview безопасный read-only, в другом доступен как visibility chip.

**Evidence paths.**
- `apps/android/app/src/main/java/com/finance/mvp/ui/PlanningUi.kt:258-265` - overview gate и shared без household message.
- `apps/android/app/src/main/java/com/finance/mvp/ui/PlanningUi.kt:592-610` - explicit copy про небезопасный агрегат.
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2996` - quick add показывает all modes.

**Рекомендация.** Сделать reusable UX rule: `Overview` read-only везде. Write action from overview opens scope chooser with two choices only.

### 11. P2 - Filter-before-aggregate силен в backend, но дизайнерские evidence должны проверять и copy, и screenshots

**Проблема.** Backend tests покрывают важные privacy cases, но design acceptance пока должен требовать screenshot/state матрицу по режимам. Иначе можно получить технически корректный API и UX, который неверно интерпретирует "Обзор" или пустые states.

**Evidence paths.**
- `apps/backend/tests/reports/test_reports_runtime_safety.py:60-98`, `100-128`, `368-380` - backend доказывает filter-before-aggregate и neutral denial.
- `qa/fixtures/owner-member-other-invited-former-v1/goldens/report-expected.json:15-24`, `27-70` - forbidden fields и expected accounts.
- `apps/web-pwa/src/App.test.tsx:753-775` - PWA test проверяет mode labels и отсутствие technical wording, но не весь trust copy matrix.

**Рекомендация.** Добавить design QA matrix: screenshots для personal/shared/overview на Home, Operations, Assets, Categories, Analytics, Planning; expected copy для no household, empty visible rows, former/invited deny.

### 12. P2 - OCR trust boundary нужно держать как "черновик", а не "импорт"

**Проблема.** Документы верно фиксируют: capture draft pending не меняет счета и отчеты, file import вне MVP. UX должен не давать этому сползти в "импорт отчета" или автоматическое создание операций, особенно в shared context.

**Evidence paths.**
- `docs/security/security-baseline.md:73-81` - OCR boundary, no raw screenshot storage, draft does not affect reports.
- `docs/product-mvp.md:65`, `98` - file import вне MVP, capture drafts только после подтверждения.
- `apps/web-pwa/src/App.test.tsx:720-728` - test не допускает "Импорт отчета" / `report-preview`.
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md:191-210` - OCR path как review drafts.

**Рекомендация.** В shared OCR flow показывать "Черновики для проверки" и scope перед confirm. Не показывать "операции созданы" до user confirm.

## Evidence paths, которые считать опорными

- Product invariant: `docs/product-mvp.md:61-66`.
- Domain model: `docs/architecture/domain-model.md:21-25`, `276-279`, `336-347`.
- Report contract: `docs/architecture/report-api-contracts.md:7-12`, `160-187`, `246-283`, `455-481`, `491-499`.
- Authz predicates: `docs/architecture/backend-authz-predicates.md:166-188`, `191-207`, `215-234`, `245-253`, `259-278`, `374-384`.
- Privacy flows: `docs/compliance/privacy-flows-mvp.md:17-24`, `110-157`.
- Security baseline: `docs/security/security-baseline.md:73-81`, `104-105`, `152-157`, `163`.
- PWA UI: `apps/web-pwa/src/App.tsx:537-570`, `1518-1531`, `1937-1984`, `2031-2050`, `2070-2098`.
- Android UI: `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:2936-3019`, `3278-3310`, `3383-3423`; `apps/android/app/src/main/java/com/finance/mvp/ui/PlanningUi.kt:258-265`, `592-610`.
- Backend implementation: `apps/backend/src/app/reports/service.py:147-209`, `279-363`, `409-531`; `apps/backend/src/app/authz/predicates.py:330-344`, `430-478`, `607-613`.

## Рекомендации

1. Сделать `Overview` read-only системным UX-инвариантом: ни одна форма не должна сохранять в overview.
2. Переименовать `Обзор` в "Мой обзор" или "Видимое мне"; рядом с метриками добавить "личное + общее, без личного другого участника".
3. В PWA убрать fallback `snapshot.reports[0]` для report mode mismatch.
4. В transfer timeline требовать видимость обеих сторон или нейтрализовать скрытую сторону.
5. Вынести scope control в quick add из advanced/details на уровень основного решения.
6. Стандартизировать empty/error copy по scope: no visible rows, no household, no active membership, neutral deny.
7. На всех cards/rows финансовых объектов показывать scope badge: `Личное`, `Общее`.
8. Для shared creation без household показывать блокирующую причину до submit, не только после ошибки.
9. Для design QA завести матрицу screenshots по actor/mode/platform, не ограничиваться backend proof.
10. Сохранить OCR как draft review, не как import.

## Что НЕ менять

- Не ослаблять backend-инвариант `filter-before-aggregate`.
- Не добавлять hidden counts, `filteredOutCount`, "часть данных скрыта", member contribution или "у другого участника есть данные".
- Не превращать `combined_viewer_overview` в household-wide aggregate.
- Не разрешать personal/shared transfers без отдельной split-visibility модели, legal/security/design review и новых тестов.
- Не добавлять file import/report-preview в MVP под видом OCR.
- Не автоподтверждать OCR/capture drafts.
- Не давать former/invited members historical shared read access.
- Не переносить account ownership personal/shared после создания без отдельного security decision.

## Критерии успеха

- В write-формах доступны только `Личное` и `Общее`; `Обзор` нигде не является вариантом сохранения.
- Пользователь на Home/Analytics понимает, что `Обзор` = "мои личные + общие", а не "все деньги семьи".
- Shared empty state без household объясняет следующий шаг и не намекает на hidden data.
- PWA/Android screenshots показывают scope badge на счетах, категориях, операциях, planning plans.
- Report mode mismatch в PWA дает mode-specific empty/error, а не чужой fallback report.
- Transfer rows не раскрывают hidden counterparty labels.
- QA evidence содержит Owner A, Member B, Other C, Invited, Former для personal/shared/overview и no hidden counts.
- OCR flow создает только pending drafts до confirm; copy не использует "импорт отчета".

## Риски и триггеры эскалации

- **P0 escalation:** любой UI или API путь показывает personal account/category/transaction/aggregate другого участника, даже агрегированно.
- **P0 escalation:** `Overview` сохраняет данные без явного выбора personal/shared.
- **P1 escalation:** product asks for personal/shared transfer, household-wide personal totals, member contribution, export of former shared history or hidden counts.
- **P1 escalation:** cache/offline snapshot cannot be invalidated by user/household/membership version.
- **P1 escalation:** authenticated production smoke for login/OCR remains unavailable before public/security GO.
- **P2 risk:** inconsistent copy between Android and PWA trains users to distrust numbers even when backend is correct.

## Ограничения этой критики

- Ручное UI-тестирование и запуск тестов не выполнялись.
- Project repo не изменялся.
- Выводы основаны на чтении vault, docs/product/security/compliance, backend service/authz, PWA/Android UI code и существующих test/evidence files.
