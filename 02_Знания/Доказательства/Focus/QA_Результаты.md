---
id: "qa-results"
тип: "доказательство"
статус: "активно"
проект: "Focus"
создано: "2026-06-12"
обновлено: "2026-06-14"
теги:
  - "qa"
  - "focus"
  - "тестирование"
---

# QA Результаты — Focus

## Верификация сборки (2026-06-12)

| Компонент | Команда | Результат | Примечание |
|---|---|---|---|
| Backend compile | `mvn compile -q` | PASS | 0 ошибок |
| Backend tests | `mvn test` | PASS | 21/21 (0 failures, 0 errors) |
| Android assembleDebug | `gradlew assembleDebug` | PASS | BUILD SUCCESSFUL |
| AdvisoryLock H2 | `ReminderScheduler` | NOISE | PG_TRY_ADVISORY_LOCK не поддерживается H2 — известный noise, не блокер |

## Баги найденные и исправленные

| ID | Описание | Статус | Дата |
|---|---|---|---|
| BUG-001 | `TaskService.getById()` вызывает `resolveTaskWithEditAccess` — shared-пользователь с `canEdit=false` получает Forbidden вместо чтения задачи | FIXED | 2026-06-12 |

## Верификация 2026-06-14 (завершение recurring reminders)

| Компонент | Команда | Результат | Примечание |
|---|---|---|---|
| Backend compile | `mvn compile -q` | PASS | 0 ошибок после изменений RemindAtType/ReminderRule/ReminderScheduler/TaskService |
| Backend tests | `mvn test` | PASS | 21/21 (0 failures, 0 errors) |
| Frontend build | `npm run build` | PASS | 0 ошибок после изменений TasksPage/types/i18n |
| Android assembleDebug | `gradlew assembleDebug` | PASS | 0 ошибок после обновления TaskDtos.kt |

### Коммит: повторяющиеся напоминания

- **SHA:** `50a5a0f` (branch `feature/softer-green-and-reminders`)
- **Backend (8 файлов):** RemindAtType +HOURLY/DAILY/WEEKLY, ReminderRule +startAt/lastFiredAt, ReminderRuleRequest +startAt, ReminderScheduler calculateRecurringTrigger() с период-выравниванием, TaskService setStartAt/setLastFiredAt при копировании, TaskResponse поля, V5 Flyway миграция
- **Frontend (5 файлов):** TasksPage условный UI (datetime-local для recurring типов, minutesBefore для стандартных), ReminderRuleDto обновлён, i18n строки (hourly/daily/weekly/reminderStartAt)
- **Android (1 файл):** TaskDtos.kt — ReminderRuleDto/ReminderSummaryDto +startAt/lastFiredAt, VALID_REMIND_TYPES обновлён
- **CI (1 файл):** backend-prod-deploy.yml правка

## Навигация

- [[QA_Фиксы]] — журнал фиксов
- [[Focus]] — статус проекта
- [[MOC_Focus]] — карта проекта
