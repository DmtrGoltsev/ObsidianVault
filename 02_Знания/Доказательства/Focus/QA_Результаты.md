---
id: "qa-results"
тип: "доказательство"
статус: "активно"
проект: "Focus"
владелец: "QA_Lead"
создано: "2026-06-05"
обновлено: "2026-06-06"
уверенность: "высокая"
источники:
  - "[[QA_ТестКейсы_v2]]"
теги: ["QA", "результаты", "тестирование", "backend"]
---

# QA Результаты прогонов

## Сводка

| Метрика | Значение |
|---|---|
| Всего тест-кейсов | 253 |
| Протестировано | ~65 |
| PASS | ~63 |
| FAIL (баги) | 2 |
| Фиксов применено | 18 (FIX-A — FIX-R) |

## Волна 1 — Backend retests after @Valid fix

Дата: 2026-06-05. 3 агента параллельно.

| ID | Status | Notes |
|---|---|---|
| BE-034 | PASS | Status transition 200 |
| BE-035 | PASS | Status transition 200 |
| BE-036 | PASS | Status transition 200 |
| BE-038 | PASS | Status transition 200 |
| BE-088 | PASS | 400 DONE→TODO rejected |
| BE-089 | PASS | 400 CANCELLED→IN_PROGRESS rejected |
| BE-090 | PASS | 400 TODO→DONE shortcut rejected |
| BE-091 | PASS | 400 reschedule DONE blocked |
| BE-092 | PASS | 400 reschedule CANCELLED blocked |
| BE-013 | PASS | 400 blank title |
| BE-030 | PASS | 400 blank title (service) |
| BE-107 | PASS | greenDecay present |
| BE-018 | PASS | 204 soft delete |
| BE-019 | PASS | deleted folder not in list |

## Волна 2 — Auth/Sharing/Recurrence

Дата: 2026-06-05. 3 агента параллельно.

| ID | Status | Notes |
|---|---|---|
| BE-008 | PASS | Token refresh 200 |
| BE-011 | PASS | Logout 200, old RT→401 |
| BE-024 | PASS | Goal create+delete |
| BE-042 | PASS | Task links 200 |
| BE-043 | PASS | Task soft delete 204 |
| BE-049 | PASS | Recurrence MONTHLY |
| BE-050 | PASS | Recurrence auto-create next |
| BE-060 | PASS | Priority decay 8→7 |
| BE-063 | PASS | Share goal 201 |
| BE-064 | PASS | Share task 201 |
| BE-066 | PASS | Invitations list |
| BE-067 | PASS | Accept invitation |
| BE-069 | PASS | Shared goal read+edit |
| BE-070 | PASS | 403 Forbidden (FIX-O) |

## Волна 3 — Backend comprehensive P0

Дата: 2026-06-06. Один master-скрипт.

| ID | Status | Notes |
|---|---|---|
| BE-001 | PASS | Register 201 |
| BE-002 | PASS | Wrong password → 401 |
| BE-003 | PASS | GET /me 200 |
| BE-005 | PASS | Update name via /settings |
| BE-006 | PASS | List folders |
| BE-007 | PASS | Create folder 201 |
| BE-009 | PASS | Rename folder |
| BE-010 | PASS | Delete folder 204 |
| BE-012 | PASS | Create goal 201 |
| BE-015 | PASS | Goals by folder |
| BE-040 | PASS | GET tasks |
| BE-093 | PASS | Nested RecurrenceInfo DAILY |
| BE-094 | PASS | Nested ReminderSummary count=1 |
| BE-095 | PASS | isActive=true (camelCase) |
| BE-096 | PASS | Tags flat string[] |
| BE-097 | PASS | Complete recurring → next created |
| BE-098 | PASS | Soft delete cascade |
| BE-103 | PASS | Null priority defaults to 5 |
| BE-108 | PASS | Decay config update |
| BE-112 | PASS | Invalid preset → 400 |
| BE-114 | PASS | WEEKLY INVALIDDAY → 400 (FIX-R) |
| BE-115 | PASS | Multi-reminder count=3 |
| BE-117 | PASS | Remove recurrence |
| BE-060 | PASS | Priority decay 8→6 |
| INT-011 | PASS | TODO→IN_PROGRESS→DONE lifecycle |
| INT-012 | PASS | TODO→IN_PROGRESS→CANCELLED |
| SEC-011 | PASS | Self-sharing → 400 |
| SEC-012 | PASS | XSS stored as literal |
| SEC-013 | PASS | SQL injection stored as literal |
| SEC-015 | PASS | Generic error messages |
| BE-099 | PASS | Self-sharing blocked |
| BE-101 | FAIL | Owner edit shared user task → 404 (pending) |

## Открытые баги

| ID | Описание | Приоритет |
|---|---|---|
| BE-101 | Goal owner не может редактировать task созданный shared user → 404 | P0 |
