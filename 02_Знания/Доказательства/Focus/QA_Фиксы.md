---
id: "qa-fixes"
тип: "доказательство"
статус: "активно"
проект: "Focus"
владелец: "QA_Lead"
создано: "2026-06-05"
обновлено: "2026-06-06"
уверенность: "высокая"
источники:
  - "[[QA_ТестКейсы_v2]]"
теги: ["QA", "фиксы", "bugfix"]
---

# QA Журнал фиксов

## Применённые фиксы

| FIX | Что исправлено | Файл | Дата | Верифицирован |
|---|---|---|---|---|
| FIX-A | @Valid на TaskRequest | TaskController.java | 2026-06-05 | Да |
| FIX-B | Status transitions validation (TODO→IN_PROGRESS→DONE/CANCELLED) | TaskService.java | 2026-06-05 | Да |
| FIX-C | Self-sharing prevention | ShareService.java | 2026-06-05 | Да |
| FIX-D | Goal-ownership fallback for shared tasks | TaskService.java | 2026-06-05 | Частично (BE-101 FAIL) |
| FIX-E | TokenManager lazy init (ANR fix) | TokenManager.kt | 2026-06-05 | Да |
| FIX-F | TaskRequest: убраны @NotBlank/@NotNull для PATCH | TaskRequest.java | 2026-06-05 | Да |
| FIX-G | Title validation перенесена в service | TaskService.java:107-109 | 2026-06-05 | Да |
| FIX-H | Reschedule presets (+30m/+1h/+3h/+24h) | TaskService.java | 2026-06-05 | Да |
| FIX-I | TaskResponse nested RecurrenceInfo | TaskResponse.java | 2026-06-05 | Да |
| FIX-J | ReminderRule @JsonProperty("isActive") | ReminderRule.java | 2026-06-05 | Да |
| FIX-K | CalendarService @Transactional | CalendarService.java | 2026-06-05 | Да |
| FIX-L | Generic error messages (no stack trace) | GlobalExceptionHandler.java | 2026-06-05 | Да |
| FIX-M | UserResponse greenDecay/redDecay | UserResponse.java | 2026-06-05 | Да |
| FIX-N | Task links CRUD | TaskService.java | 2026-06-05 | Да |
| FIX-O | ForbiddenException — 403 вместо 400 | ForbiddenException.java (новый), TaskService.java, GlobalExceptionHandler.java | 2026-06-05 | Да (BE-070) |
| FIX-P | Optimistic lock — version check в update() | TaskRequest.java (+version), TaskService.java | 2026-06-06 | Да (BE-084) |
| FIX-Q | taskType default GREEN при null | TaskService.java:117 | 2026-06-06 | Да (BE-103) |
| FIX-R | WEEKLY daysOfWeek validation — parseDaysOfWeek бросает BadRequestException | TaskService.java:495-507 | 2026-06-06 | Да (BE-114) |
| FIX-S | Register endpoint возвращает 201 вместо 200 | AuthController.java | 2026-06-06 | Да (FE-006) |

## Новые файлы созданные при фиксах

| Файл | FIX | Описание |
|---|---|---|
| ForbiddenException.java | FIX-O | @ResponseStatus(FORBIDDEN) |
