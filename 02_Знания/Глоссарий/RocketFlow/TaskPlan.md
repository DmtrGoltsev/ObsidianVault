---
id: "term-taskplan"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["android/README.md", "docs/68-scroll-and-priority-retirement-delivery.md"]
доказательства: ["Док_V21_Scroll_Priority_20260822"]
теги: ["глоссарий", "rocketflow", "taskplan", "android"]
---

# TaskPlan

## Определение

TaskPlan — представление задач в Android-модуле `planning`. Числовой task priority и priority decay не участвуют в отображении или порядке.

## Бизнес-правила

- Запланированные задачи: `plannedTime ASC`, затем `createdAt ASC`, затем `id ASC`; отсутствие `plannedTime` идёт последним
- Tie-break по `id` обеспечивает стабильный порядок
- Planner сохраняет stable visible anchor id и pixel offset при перестроении и возврате из деталей
- Синхронизируется с бэкендом через [[PlanningSync]]

## Связанные термины

- [[Green_Task]] — зелёная задача
- [[Red_Task]] — красная задача
- [[ADR_Отказ_От_Приоритета_Задач]] — отказ от приоритета и compatibility shadow
- [[PlanningSync]] — синхронизация плана
