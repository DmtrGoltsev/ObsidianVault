---
id: "finance-design-critic-05-planning-analytics"
тип: "дизайн-критика"
проект: "Finance"
роль: "Designer Critic 05"
фокус: "Planning / Analytics"
статус: "активно"
создано: "2026-06-08"
обновлено: "2026-06-08"
уверенность: "высокая"
источники:
  - "C:\\Users\\style\\Documents\\ObsidianVault\\README.md"
  - "C:\\Users\\style\\Documents\\ObsidianVault\\01_Работа\\Проекты\\Finance\\Finance.md"
  - "C:\\Users\\style\\Documents\\ObsidianVault\\02_Знания\\Пакеты_контекста\\Finance\\Пакет_Finance_Полный.md"
  - "C:\\Users\\style\\Documents\\ObsidianVault\\02_Знания\\Пакеты_контекста\\Finance\\Кворум_Finance.md"
  - "C:\\Users\\style\\Documents\\ObsidianVault\\02_Знания\\Доказательства\\Finance\\Док_Release_Planning_MVP_20260607.md"
  - "C:\\Users\\style\\Documents\\ObsidianVault\\02_Знания\\Дизайн\\Finance\\Карта_Пользовательских_Путей_Finance.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\README.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\docs\\product-mvp.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\docs\\current-status.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\docs\\user-guide-ru.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\docs\\product\\ux-quorum-design-decision-ru.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\api\\openapi\\README.md"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\api\\openapi\\openapi.yaml"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\android\\app\\src\\main\\java\\com\\finance\\mvp\\ui\\PlanningUi.kt"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\android\\app\\src\\main\\java\\com\\finance\\mvp\\ui\\FinanceApp.kt"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\android\\app\\src\\main\\java\\com\\finance\\mvp\\api\\ApiClient.kt"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\backend\\src\\app\\planning\\schemas.py"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\backend\\src\\app\\planning\\service.py"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\backend\\tests\\planning\\test_planning_db_runtime.py"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\android\\app\\src\\test\\java\\com\\finance\\mvp\\api\\ApiClientPlanningAllocationTest.kt"
теги: ["finance", "design-critique", "planning", "analytics", "android", "ux"]
---

# Критика 05 — Planning / Analytics

## Позиция критика

Planning MVP уже держится на правильном продуктово-техническом контракте: план строится только в personal/household scope, `previousMonthSurplus` лежит в summary, а прогресс существует на уровне allocation. Главная UX-опасность сейчас не в отсутствии функций, а в том, что интерфейс может показать правильные данные неправильной ментальной моделью: как общий прогресс плана, как инвестиционный совет, как автоперенос остатка или как “все семейные деньги”.

## Критические наблюдения

### P0-01. Риск ложного plan-level progress всё ещё встроен в Android-клиент

**Наблюдение:** релизное acceptance clarification прямо запрещает искать и вводить `PlanningPlanDto.progress`, но Android-модель и UI всё ещё имеют fallback для `plan.status`, `plan.progressStatus`, `plan.progressPercent` и показывают баннер “Статус плана”, если эти поля появятся.

**Evidence paths:** `C:\Users\style\Documents\ObsidianVault\02_Знания\Доказательства\Finance\Док_Release_Planning_MVP_20260607.md` → Acceptance clarification; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\api\ApiClient.kt:316`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\api\ApiClient.kt:1306`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:667`.

**Рекомендация:** убрать из UX-концепта любые plan-level progress/status affordances. Плановая карточка может показывать только доход, распределено, остаток, сверх и предупреждение under/over allocation. Прогресс, факт и причины внимания должны быть только в allocation rows.

### P0-02. Summary-показатели могут читаться как “прогресс месяца”, хотя это баланс планирования

**Наблюдение:** карточка “Текущий план” показывает “Доход / Распределено / Осталось / Сверх” рядом с `previousMonthSurplus`. Без явного текста “это не факт расходов и не прогресс выполнения” пользователь может принять эти числа за ход месяца.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2107`; `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2120`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:643`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\service.py:633`.

**Рекомендация:** переименовать/структурировать верхнюю карточку как “Баланс плана” и отделить ее от “Факт по распределениям”. `previousMonthSurplus` показывать как “предложение из прошлого месяца”, не как добавленные деньги или автоматическую операцию.

### P0-03. `previousMonthSurplus` визуально выглядит как перенос денег, но API говорит “proposal-only”

**Наблюдение:** OpenAPI описывает `previousMonthSurplus` как proposal-only positive surplus; транзакция не создается. Android показывает “Сальдо прошлого месяца”, что легко прочитать как реальное сальдо/перенос остатка.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2120`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:647`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\service.py:736`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\tests\planning\test_planning_db_runtime.py:781`.

**Рекомендация:** в UI использовать формулировку вроде “Можно учесть из прошлого месяца: X” и короткое пояснение “не меняет счета автоматически”. Не использовать слова “сальдо” и “перенос” без пояснения.

### P1-04. Статусы allocation слишком технические и не объясняют действие

**Наблюдение:** backend различает `EXPENSE_OVER_PLAN`, `INVESTMENT_UNDER_PLAN`, `TARGET_MISSING_OR_INACCESSIBLE`, но Android часто показывает статус через общие строки “выше плана”, “ниже плана”, “требует внимания”. Пользователь видит тревогу, но не видит следующий шаг.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\service.py:874`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\tests\planning\test_planning_db_runtime.py:785`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1189`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1636`.

**Рекомендация:** для каждого `attentionReason` показывать человеко-действие: “расходы превысили план — уменьшите факт или увеличьте лимит”, “инвестиции ниже цели — пополните актив или уменьшите план”, “цель недоступна — выберите новую категорию”.

### P1-05. Allocation row показывает факт, но не показывает variance как первичный смысл отклонения

**Наблюдение:** API и тесты возвращают `varianceAmount`, но Android row показывает “Факт” и процент, а разницу план/факт не выносит явно. Для planning/analytics разница важнее процента, потому что именно она объясняет действие.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\schemas.py:114`; `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2229`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\api\ApiClient.kt:366`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1170`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\test\java\com\finance\mvp\api\ApiClientPlanningAllocationTest.kt:72`.

**Рекомендация:** каждая allocation row должна иметь устойчивую триаду: “План”, “Факт”, “Отклонение”. Цвет и текст статуса должны зависеть от target type: для расходов превышение плохо; для инвестиций недобор плохо.

### P1-06. “Инвестиции” и “Цель накопления” рискуют звучать как advisory

**Наблюдение:** MVP запрещает инвестиционные рекомендации, доходность и рыночную аналитику. В Planning UI инвестиционные категории и цель накопления полезны, но без осторожной копии пользователь может принять их за инвестиционный план/совет.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\docs\product-mvp.md:49`; `C:\Users\style\Documents\Codex\Финансы\docs\product-mvp.md:64`; `C:\Users\style\Documents\Codex\Финансы\docs\product\ux-quorum-design-decision-ru.md:25`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1069`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\tests\planning\test_planning_db_runtime.py:602`.

**Рекомендация:** копия должна говорить “накопить на актив вручную”, “ручная цель”, “без доходности и рекомендаций”. Не использовать “портфельный прогресс”, “инвестиционная цель выполнена”, “доходность”, “лучший актив”.

### P1-07. Создание investment asset category из Planning неочевидно

**Наблюдение:** новые allocations выбирают expense category или investment asset category, account target для новых allocations не предлагается. Но для investment target кнопка создания в editor сейчас не показывается, если target type investment; пользователь может оказаться в пустом списке без понятного пути.

**Evidence paths:** `C:\Users\style\Documents\ObsidianVault\01_Работа\Проекты\Finance\Finance.md` → “новые allocations выбирают expense category или investment asset category”; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:990`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1006`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1531`.

**Рекомендация:** для пустых investment targets показать next action “Создайте инвестиционную категорию в Активы” или безопасный маршрут в asset categories. Не возвращать account target как shortcut.

### P1-08. Planning спрятан внутри Analytics, хотя это сценарий регулярной работы

**Наблюдение:** Android открывает Planning через вкладку Analytics, а не как top-level раздел. Карта путей уже отмечает, что его легко не найти; в PWA отдельный Planning UI не обнаружен.

**Evidence paths:** `C:\Users\style\Documents\ObsidianVault\02_Знания\Дизайн\Finance\Карта_Пользовательских_Путей_Finance.md` → раздел 5; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\FinanceApp.kt:1686`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\FinanceApp.kt:1705`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\FinanceApp.kt:1717`.

**Рекомендация:** минимум — усилить видимость вкладки “Планирование” внутри Analytics, добавить entry point из главного обзора при under/over allocation. Максимум после MVP — отдельный top-level Planning, если сценарий станет еженедельным.

### P1-09. Overview gate правильный, но scope selector всё равно показывает Overview как равноправный выбор

**Наблюдение:** UI корректно блокирует overview planning, но в карточке выбора режима Overview присутствует среди chips. Пользователь сначала делает невозможный выбор, потом получает объяснение.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:258`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:560`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:592`; `C:\Users\style\Documents\ObsidianVault\02_Знания\Дизайн\Finance\Карта_Пользовательских_Путей_Finance.md` → “Overview scope не подходит для planning”.

**Рекомендация:** в Planning selector показывать только “Личное” и “Общее”. Overview можно оставить как disabled chip с tooltip/подписью “обзор не планируется”, если нужен образовательный момент.

### P1-10. История/copy не раскрывает риск copied attention rows

**Наблюдение:** OpenAPI говорит, что при copy недоступные targets становятся `requiresAttention` rows с `targetSnapshot`; UI кнопка “Копировать” не предупреждает о возможных строках, требующих внимания.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:1198`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:460`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1244`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\service.py:420`.

**Рекомендация:** после copy показывать summary: “скопировано N распределений, M требуют внимания”. В списке history добавить маленький текст “копирует доходы и распределения, цели проверяются заново”.

### P2-11. День дохода понятен технически, но UX не объясняет edge case коротких месяцев

**Наблюдение:** OpenAPI фиксирует, что day 31 falls back to last day in shorter months. UI показывает “День месяца”, но не объясняет, что будет в феврале или месяце с 30 днями.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2147`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:742`; `C:\Users\style\Documents\Codex\Финансы\apps\backend\src\app\planning\service.py:813`.

**Рекомендация:** добавить короткий helper text под полем: “Если такого дня нет, используем последний день месяца”. Это снижает тревогу вокруг зарплаты 31-го числа.

### P2-12. Пустые состояния слишком общие для planning decisions

**Наблюдение:** “Источников дохода пока нет”, “Распределений пока нет”, “Истории планов пока нет” не объясняют следующий шаг и не связывают его с personal/shared scope.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:772`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:940`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:1257`; `C:\Users\style\Documents\ObsidianVault\02_Знания\Дизайн\Finance\Карта_Пользовательских_Путей_Finance.md` → раздел 9.

**Рекомендация:** empty state должен быть действием: “Добавьте зарплату или регулярный доход”, “Выберите категорию расходов и задайте лимит”, “Скопируйте прошлый план, когда появится история”.

### P2-13. Analytics и Planning используют разные понятия “остатка”

**Наблюдение:** продуктовая документация просит различать “результат периода” и “остаток сейчас”. Planning добавляет “Осталось” как unallocated amount. Без строгой лексики это третий “остаток”, который пользователь может смешать с балансом счета.

**Evidence paths:** `C:\Users\style\Documents\Codex\Финансы\docs\user-guide-ru.md:113`; `C:\Users\style\Documents\Codex\Финансы\docs\product\ux-quorum-design-decision-ru.md:47`; `C:\Users\style\Documents\Codex\Финансы\apps\android\app\src\main\java\com\finance\mvp\ui\PlanningUi.kt:650`; `C:\Users\style\Documents\Codex\Финансы\api\openapi\openapi.yaml:2118`.

**Рекомендация:** в Planning заменить “Осталось” на “Не распределено”, а в Analytics оставить “остаток сейчас” только для счетов/капитала. Это маленькая копийная правка с большим эффектом.

## Рекомендации

1. Зафиксировать UX-инвариант: plan-level progress запрещен; allocation-level progress обязателен.
2. В верхней карточке Planning показывать “Баланс плана”, а не “ход выполнения”.
3. Переименовать `previousMonthSurplus` в пользовательской копии как предложение, не как автоматический перенос.
4. Сделать allocation rows таблично-сканируемыми: цель, план, факт, отклонение, статус, действие.
5. Локализовать `attentionReason` в actionable copy.
6. Убрать Overview из активного planning selector или сделать disabled.
7. Дать пустым состояниям next-best-action по scope.
8. Для savings goal использовать лексику ручного накопления без advisory.
9. После copy показывать, сколько строк требуют внимания.
10. В Android/PWA дизайн-системе синхронизировать термины: “не распределено”, “сверх дохода”, “факт”, “отклонение”, “цель накопления”.

## Что НЕ менять

- Не добавлять plan-level progress bar, общий процент выполнения плана или “статус плана” как продуктовый показатель.
- Не возвращать account target для новых allocations; текущий путь должен оставаться expense category или investment asset category.
- Не превращать `previousMonthSurplus` в операцию, автоперенос денег или изменение баланса счета.
- Не добавлять Overview planning как агрегированный personal+shared план.
- Не обещать bank API, file import, SMS/push import, broker integration, налоговую аналитику, рекомендации или автоматическую переоценку активов.
- Не смешивать OCR/file import с Planning; OCR остается черновиком операций на подтверждение.
- Не раскрывать personal данные другого участника через shared/overview counters, пустые состояния или history.

## Критерии успеха

- Пользователь может объяснить разницу между “не распределено” и “остаток на счетах” после одного просмотра экрана.
- В UI нет plan-level progress/status; все прогресс-состояния находятся в allocation rows.
- Каждая allocation row показывает план, факт, отклонение и понятный статус.
- `previousMonthSurplus` читается как рекомендация к учету, а не как созданная транзакция.
- Overview не воспринимается как допустимый режим планирования.
- Savings goal воспринимается как ручная цель накопления, без обещания доходности.
- Empty states ведут к следующему действию и учитывают personal/shared scope.
- Copy history явно показывает attention rows после копирования.

## Риски

- **P0:** случайное появление plan-level fields в API/клиенте снова включит ложный “Статус плана”.
- **P0:** пользователь примет `previousMonthSurplus` за реальный остаток и будет ожидать изменения счета.
- **P1:** ambiguous “Инвестиции ниже плана” может звучать как финансовый совет.
- **P1:** shared planning без ясного scope может подорвать privacy-инвариант.
- **P1:** отсутствие видимого Planning entry point снизит adoption регулярного планирования.
- **P2:** разные термины для остатка ухудшат доверие к аналитике.
- **P2:** без скриншотной матрицы по Android/PWA и personal/shared/overview дизайнеры могут улучшить один сценарий и сломать другой.

