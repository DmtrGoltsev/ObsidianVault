---
id: "finance-user-journey-map-20260608"
тип: "дизайн"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-08"
обновлено: "2026-06-08"
уверенность: "средняя"
источники:
  - "[[Пакет_Finance_Полный]]"
  - "[[Кворум_Finance]]"
  - "[[Док_Release_Planning_MVP_20260607]]"
  - "README.md"
  - "docs/product-mvp.md"
  - "docs/current-status.md"
  - "docs/user-guide-ru.md"
  - "docs/product/ux-quorum-design-decision-ru.md"
  - "apps/android/app/src/main/java/com/finance/mvp/ui/AppSection.kt"
  - "apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt"
  - "apps/android/app/src/main/java/com/finance/mvp/ui/PlanningUi.kt"
  - "apps/web-pwa/src/App.tsx"
доказательства:
  - "[[Док_Release_Planning_MVP_20260607]]"
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
теги: ["finance", "ux", "journey-map", "design", "planning-mvp"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
---

# Карта пользовательских путей — Finance

## Назначение

Практичная карта для дизайнеров Finance: какие пользовательские пути уже видны в продуктовой документации и UI-слое Android/PWA, где смотреть экраны, какие боли и риски упрощать. Карта актуализирована под release `20260607T225457Z-819b5815` и Planning iteration MVP.

Старая актуальная journey map по Finance в vault не найдена. Этот документ считается первой отдельной картой пользовательских путей.

## Контекст продукта

Finance — ручной учет личных и семейных финансов. Первый экран должен быть рабочим обзором, а не landing page. Основная модель: личные данные видит только владелец; общие семейные данные видят активные участники household; обзор текущего пользователя объединяет shared + personal текущего пользователя без раскрытия personal другого участника.

Актуальные релизные ограничения:

- Production release: `20260607T225457Z-819b5815`, project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`.
- Planning progress — на уровне allocation, не plan-level.
- Authenticated production login/OCR smoke не запускался из-за отсутствия operator password/session token.
- APK debug-signed, не release-signed.
- Public launch, full security GO, HTTPS/domain, backup/restore proof и production QA data retention остаются отдельными gates.
- MVP не включает bank API, Excel/CSV/PDF import pipeline, SMS/push/notification interception, налоговую аналитику, инвестиционные рекомендации и автоматическую переоценку активов.

## Сводная карта экранов

| Платформа | Навигация / экран | Что проверять дизайнерам |
|---|---|---|
| Android | `AppSection.Home` — Главная | Капитал, расходы месяца, доходы, топ категории, последние операции. |
| Android | `AppSection.Operations` — Операции | Ручные доходы/расходы/переводы, review OCR drafts, отличимость перевода от расхода. |
| Android | `AppSection.Assets` — Активы | Карты, банки, наличные, вклады, брокерские счета, металлы, группы asset categories. |
| Android | `AppSection.Categories` — Категории | Создание/редактирование income/expense category, личное/общее, пустые состояния. |
| Android | `AppSection.Analytics` — Аналитика | Summary/categories/capital structure и вкладка Planning. |
| Android | `PlanningUi` | Личный/общий план, income sources, allocations, savings goals, history/copy, reminders. |
| Web PWA | `money` — Обзор | Метрики доход/расход/итог, активы, топ категории, timeline. |
| Web PWA | `operations` — Операции | Screenshot OCR upload, pending drafts, quick add. |
| Web PWA | `assets` — Счета и активы | Empty state и плотность списка активов. |
| Web PWA | `categories` — Категории | Форма категории: направление, scope, иконка, цвет. |
| Web PWA | `analytics` — Аналитика | Категории и капитал; в текущем PWA-коде отдельного Planning UI не видно. |
| Web PWA | `settings` — Настройки | Переключение режима и privacy messaging. |

## 1. Вход и сессия

**Задача пользователя:** войти или зарегистрироваться, восстановить понятный контекст после повторного открытия.

**Шаги:** открыть приложение -> увидеть форму входа/регистрации -> ввести email/password -> получить рабочую панель -> при logout вернуться к unauthenticated state.

**Боль и риски:**

- Ошибки авторизации должны быть нейтральными и не раскрывать наличие пользователя.
- После входа пользователь должен сразу понять текущий режим: личное, общее или обзор.
- Для Android важна проверка session restore и secure token storage; для PWA — cookie/CSRF и service worker constraints.

**Точки упрощения:**

- Сделать на первом рабочем экране явный scope indicator рядом с переключателем режима.
- Сохранять объяснение scope коротким: "Личное видно только вам", "Общее для семьи", "Обзор".

**Screens/components to inspect:** `LoginScreen` в `FinanceApp.kt`, `LoginScreen` в `apps/web-pwa/src/App.tsx`, `TokenStore.kt`, `auth` routes.

## 2. Обзор денег и счетов

**Задача пользователя:** быстро понять, где деньги, сколько видно сейчас и что изменилось за период.

**Шаги:** открыть обзор -> выбрать режим personal/shared/overview -> посмотреть общий видимый капитал -> перейти в активы/операции/аналитику по подозрительной цифре.

**Боль и риски:**

- "Итог периода" и "текущий остаток" легко спутать.
- Overview не должен звучать как "все деньги семьи": он не включает personal второго участника.
- Пустые states по shared mode могут выглядеть как ошибка, если у пользователя нет household.

**Точки упрощения:**

- Отдельно маркировать "остаток сейчас" и "результат периода".
- В shared empty state объяснять, что нужен общий бюджет/household, а не просто "нет данных".
- В карточках активов использовать одинаковые термины: счет, актив, категория активов.

**Screens/components to inspect:** `MoneyDashboard`, `ViewSwitch`, `Metric`, `AssetGroupRow`, `TimelineList`, `HomeContent`, `ModeSelector`.

## 3. Операции и переводы

**Задача пользователя:** внести доход, расход или перевод без искажения аналитики.

**Шаги:** открыть операции -> выбрать quick add/manual form -> выбрать тип: expense/income/transfer/asset -> выбрать счет и категорию или счет-получатель -> указать сумму/дату/комментарий -> сохранить -> увидеть обновленный timeline/балансы.

**Боль и риски:**

- Перевод визуально похож на расход, но не должен попадать в расходы.
- Для shared операции нужен household; если его нет, shared submit должен быть недоступен или объяснен.
- Пустой список счетов/категорий блокирует операцию; нужен короткий путь создать недостающую сущность.

**Точки упрощения:**

- Развести affordance для "перевести" и "потратить" цветом/иконкой/копией.
- В quick add показывать причину disable submit: нет счета, нет категории, нет shared budget.
- После сохранения давать обратную связь и маршрут к измененной записи.

**Screens/components to inspect:** `QuickAdd`, `OperationsPage`, `TimelineList`, `operationsContent`, `QuickEntryType`, `CaptureDraftReviewCard`.

## 4. Активы и категории

**Задача пользователя:** завести места хранения денег, ручные активы и категории смысла операций.

**Шаги:** открыть активы -> создать счет/актив или asset category -> указать тип, валюту, сумму, personal/shared -> открыть категории -> создать income/expense category -> выбрать scope, иконку/цвет -> использовать в операциях/planning.

**Боль и риски:**

- "Актив", "счет", "категория активов" могут смешиваться.
- Investment asset categories являются source of truth для planning targets; designers должны не возвращать account target для новых allocations.
- Личные категории не должны раскрывать private semantics через shared views, counters или empty states.

**Точки упрощения:**

- В assets UI разделить "место хранения" и "группа/категория активов".
- В category cards всегда показывать направление и scope: доход/расход, личное/общее.
- Для пустых режимов предлагать следующий конкретный шаг: создать личный счет, общий счет или категорию.

**Screens/components to inspect:** `AssetsPage`, `AssetTile`, `CategoryForm`, `CategoryTile`, `assetsContent`, `categoriesContent`, `AssetCategoryEditor`, `AccountEditDialog`.

## 5. Планирование бюджета и накопительных целей

**Задача пользователя:** спланировать месяц: доходы, распределения, инвестиционные/накопительные цели и увидеть факт/отклонения.

**Шаги:** открыть Analytics -> Planning -> выбрать personal/shared scope и месяц -> создать план -> добавить источники дохода -> добавить allocations по expense category или investment asset category -> опционально включить savings goal -> смотреть факт, статус, attention reason -> копировать историю на новый месяц.

**Боль и риски:**

- Planning в Android находится внутри Analytics, а не как отдельный top-level раздел; его легко не найти.
- Overview scope не подходит для planning: план должен быть personal или shared, без небезопасного агрегата.
- Progress существует на allocation-level, поэтому plan-level progress bar будет вводить в заблуждение.
- Account target для новых allocations больше не предлагается; возврат этого паттерна будет регрессией.

**Точки упрощения:**

- Сделать Planning заметной вкладкой в Analytics с короткой подсказкой "планируем отдельно личное или общее".
- В allocation rows показать триаду: план, факт, внимание/статус.
- Для savings goal отделить "цель накопления" от обычного расходного лимита.

**Screens/components to inspect:** `AnalyticsSubsectionTabs`, `PlanningUi`, `PlanningScopeCard`, `PlanningPlanCard`, `PlanningIncomeSourcesCard`, `PlanningAllocationsCard`, `PlanningHistoryCard`.

## 6. Аналитика

**Задача пользователя:** понять результат периода и структуру расходов/капитала без ручного анализа таблиц.

**Шаги:** выбрать Analytics -> выбрать personal/shared/overview -> посмотреть доход/расход/итог -> оценить категории расходов -> оценить структуру капитала/инвестиции -> перейти к операциям или активам для исправления.

**Боль и риски:**

- Категории расходов пустые при отсутствии операций; это должно читаться как "пока нет расходов", не как поломка отчета.
- Shared report и combined overview имеют разные privacy boundaries.
- Investments metric и capital structure должны оставаться ручным учетом, без обещания доходности/котировок.

**Точки упрощения:**

- Для каждого report mode использовать одно предложение объяснения.
- Указывать период и режим рядом с метриками.
- Не использовать инвестиционные термины, которые подразумевают advisory.

**Screens/components to inspect:** `AnalyticsPage`, `AnalyticsSummaryCard`, `CategoryBreakdownCard`, `CapitalStructureCard`, `reportForView`, `/reports` API.

## 7. OCR / capture drafts

**Задача пользователя:** ускорить ручной ввод по выбранному скриншоту, но подтвердить данные перед влиянием на финансы.

**Шаги:** открыть операции -> выбрать screenshot OCR -> выбрать PNG/JPEG/WebP -> получить candidates -> выбрать счет и категории -> создать pending drafts -> проверить сумму/дату/описание -> сохранить правки -> подтвердить или отклонить draft.

**Боль и риски:**

- OCR confidence не гарантирует точность; UI должен подталкивать к проверке.
- Draft сам по себе не меняет счета и отчеты; это надо ясно показать.
- Реальный file import/report-preview вне MVP; нельзя визуально смешивать OCR screenshot flow с импортом банковских файлов.
- Проверить implementation mismatch: продуктовая документация говорит про Android on-device OCR, но текущий Android UI/API path вызывает backend `screenshot-ocr`; нужен security/privacy review перед публичным утверждением.

**Точки упрощения:**

- Называть путь "Скрин расходов" / "Черновики OCR", не "импорт".
- После OCR показывать статус "черновики готовы к подтверждению", а не "операции созданы".
- Для пустых результатов сразу предлагать ручной ввод.

**Screens/components to inspect:** `ScreenshotOcrCapture`, `PendingCaptureDraftsPanel`, `CaptureDraftReviewCard`, `CaptureDraftRow`, `apiClient.screenshotOcr`, `capture_drafts/router.py`.

## 8. Shared / personal scope

**Задача пользователя:** вести личные и семейные деньги без случайного раскрытия личных данных.

**Шаги:** переключить режим -> увидеть только разрешенные счета/категории/операции -> создать personal/shared сущность -> проверить, что reports и empty states не раскрывают private data другого участника.

**Боль и риски:**

- Overview легко принять за "весь household"; это неправильно.
- Empty states и counters могут случайно раскрыть наличие чужих personal данных.
- Shared category/account creation должен блокироваться без household.

**Точки упрощения:**

- Сделать scope badge обязательным на счетах, категориях, операциях, planning plans.
- В settings оставить privacy copy, но продублировать ее рядом с переключателем режима.
- QA-дизайнеру проверять все три режима на каждом разделе.

**Screens/components to inspect:** `ViewSwitch`, `visibleAccounts`, `visibleCategories`, `visibleOperations`, `FinanceMode`, `filterByMode`, `localizedScope`.

## 9. Ошибки и пустые состояния

**Ключевые состояния:**

- Нет активов в режиме.
- Пока нет расходов.
- Нет категорий в режиме.
- Записей пока нет.
- Нет ожидающих OCR drafts.
- Нет активных счетов или категорий расходов при подтверждении drafts.
- Нет доступа (`403`) и ошибка сервера (`5xx`).
- Shared planning недоступен без активного общего бюджета.

**UX-правило:** empty state должен объяснять следующий шаг и scope, error state — действие восстановления. Для privacy-sensitive states нельзя показывать детали чужих private entities.

**Screens/components to inspect:** `EmptyState`, `userFacingFailure`, `PlanningMessageCard`, `ApiResult.Failure.planningMessage`.

## Рекомендации для 6 дизайнеров

1. **Навигационный дизайнер:** привести Android и PWA к одной ментальной карте: Обзор/Операции/Активы/Категории/Аналитика, а Planning сделать явно доступным внутри Analytics или как согласованный sub-entry.
2. **Privacy UX дизайнер:** пройти все personal/shared/overview states и добавить scope badges там, где пользователь может принять overview за "все семейные данные".
3. **Forms UX дизайнер:** упростить quick add и planning allocation forms: показывать причины disabled submit и быстрый путь создать недостающий счет/категорию.
4. **Analytics дизайнер:** разделить "результат периода" и "остаток сейчас"; не вводить plan-level progress, использовать только allocation-level факт/статус.
5. **OCR/capture дизайнер:** оформить OCR как "помощник черновика", не как импорт; усилить review, confidence, confirm/discard и ручной fallback.
6. **Empty/error states дизайнер:** заменить общие пустые states на next-best-action по scope: создать личный счет, создать общую категорию, войти в household, добавить операцию вручную.

## Открытые вопросы и риски

- Нужно подтвердить фактическую Android OCR архитектуру: on-device OCR по продуктовой документации или backend screenshot OCR по текущему UI/API вызову.
- Нужен authenticated production smoke для login/OCR после предоставления operator session/password.
- Нужно решить, появится ли Planning в PWA; сейчас в PWA-коде top-level Analytics есть, но отдельный Planning UI не обнаружен.
- Нужен владелец решения по release-signed Android artifact и public production/security gates.
- Нужна проверка, что stale/current release notes не расходятся: vault содержит более ранние release boundaries рядом с актуальным `20260607T225457Z-819b5815`.
- Для дизайнеров нужна скриншотная матрица по всем режимам и платформам; в этой задаче ручное UI-тестирование не выполнялось.
