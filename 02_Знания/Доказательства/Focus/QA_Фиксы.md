---
id: "qa-fixes"
тип: "доказательство"
статус: "активно"
проект: "Focus"
создано: "2026-06-12"
обновлено: "2026-06-12"
теги:
  - "qa"
  - "focus"
  - "фиксы"
---

# QA Фиксы — Focus

## Фиксы 2026-06-12 (продолжение работы прошлого агента)

| FIX | Описание | Файл | Дата | Верифицирован |
|---|---|---|---|---|
| FIX-U | getById() использует resolveTaskWithEditAccess вместо read-access → Forbidden для shared readonly-пользователей. Добавлен resolveTaskWithReadAccess() | `TaskService.java:153-155,324-348` | 2026-06-12 | Да (mvn test 21/21) |

## Предыдущие фиксы (FIX-A — FIX-T)

| FIX | Описание | Файл |
|---|---|---|
| FIX-A | Calendar controller NPE при null plannedTime | `CalendarController.java` |
| FIX-B | FolderController.update() не возвращал userId | `FolderController.java` |
| FIX-C | Goal sharing: findByGoalIdAndTargetUserEmail → findByGoalIdAndSharedWith | `ShareService.java` |
| FIX-D | TaskResponse.from() LazyInitializationException на goal.user | `TaskResponse.java` |
| FIX-E | Auth refresh: rotation refreshToken при каждом refresh | `AuthService.java` |
| FIX-F | Folder soft delete: cascade на goals/tasks | `FolderService.java` |
| FIX-G | Goal soft delete: cascade на tasks | `GoalService.java` |
| FIX-H | TaskTag deleteByTaskId без @Modifying | `TaskTagRepository.java` |
| FIX-I | TaskLink deleteByTaskId без @Modifying | `TaskLinkRepository.java` |
| FIX-J | RecurrenceRule: next occurrence использует plannedTime а не now | `TaskService.java` |
| FIX-K | ReminderRule deleteByTaskId без @Modifying | `ReminderRuleRepository.java` |
| FIX-L | Calendar: timezone-agnostic сравнение Instant | `CalendarService.java` |
| FIX-M | Settings: PATCH /me/settings не сохранял decay конфиг | `AccountService.java` |
| FIX-N | Sharing: goal owner видит shared tasks | `TaskService.java` |
| FIX-O | Sharing: shared user получает доступ к goal/task | `ShareService.java` |
| FIX-P | Auth: logout инвалидировал все refresh tokens пользователя | `AuthService.java` |
| FIX-Q | Task: priority validation 1-10 | `TaskService.java` |
| FIX-R | Task: status transition validation | `TaskService.java` |
| FIX-S | Folder: displayOrder сохраняется при создании | `FolderService.java` |
| FIX-T | Auth endpoints skip 401 refresh interceptor | `api.ts` |

## Навигация

- [[QA_Результаты]] — результаты прогонов
- [[Focus]] — статус проекта
