---
id: "qa-testcases-v2-001"
тип: "доказательство"
статус: "активно"
проект: "Focus"
владелец: "QA_Lead"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "средняя"
источники:
  - "[[Focus]]"
  - "[[Источник_API]]"
  - "[[Priority_Decay]]"
  - "[[Recurrence_Rule]]"
  - "[[Reminder_Rule]]"
теги: ["QA", "тест-кейсы", "e2e", "backend", "frontend", "android"]
---

# QA Тест-кейсы Focus v2

> Расширенный набор тест-кейсов (v2) с учётом фиксов FIX-A — FIX-N.
> Покрывает: Backend API, Frontend Web, Android Emulator E2E, Integration, Security.
> Эмулятор: emulator-5554 (Android 14, x86_64, 560dpi, 1440x3120).
> Backend: localhost:8080. Frontend: localhost:5173. Android API: http://10.0.2.2:8080/

## Изменения v2 относительно TEST_CASES.md (177 кейсов)

- Добавлены тесты на все фиксы FIX-A — FIX-N
- Добавлены Android E2E тесты с точными координатами экрана
- Добавлены тесты на status transitions validation
- Добавлены тесты на self-sharing prevention
- Добавлены тесты на goal-ownership fallback
- Добавлены тесты на TokenManager lazy init
- Добавлены тесты на ReminderRule @JsonProperty("isActive")
- Добавлены тесты на CalendarService @Transactional
- Добавлены edge cases на Priority Decay tiered calculation
- Добавлены тесты на reschedule blocked for DONE/CANCELLED

---

## 1. Backend API Tests (87 + 30 new = 117)

Оригинальные BE-001 — BE-087 остаются без изменений. Новые кейсы:

| ID | Module | Test Name | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| BE-088 | Tasks | Status transition: DONE → TODO (invalid) | Create task, complete it (`POST /tasks/{id}/complete`), then `PATCH /tasks/{id}` `{"status":"TODO"}` | 400 Bad Request. Invalid transition DONE→TODO rejected. | P0 |
| BE-089 | Tasks | Status transition: CANCELLED → IN_PROGRESS (invalid) | Cancel task, then try to set status=IN_PROGRESS | 400 Bad Request. Invalid transition rejected. | P0 |
| BE-090 | Tasks | Status transition: TODO → DONE (invalid shortcut) | `PATCH /tasks/{id}` `{"status":"DONE"}` on a TODO task | 400 Bad Request. Must go through IN_PROGRESS first. Only TODO→IN_PROGRESS→DONE/CANCELLED allowed. | P0 |
| BE-091 | Tasks | Reschedule DONE task blocked | Complete a task, then `POST /tasks/{id}/reschedule` `{"preset":"30m"}` | 400 Bad Request. Cannot reschedule completed task. | P0 |
| BE-092 | Tasks | Reschedule CANCELLED task blocked | Cancel a task, then `POST /tasks/{id}/reschedule` `{"preset":"30m"}` | 400 Bad Request. Cannot reschedule cancelled task. | P0 |
| BE-093 | Tasks | TaskResponse nested RecurrenceInfo | Create task with DAILY recurrence, `GET /tasks/{id}` | Response contains `recurrence: {ruleType:"DAILY", intervalDays:1, daysOfWeek:null}` as nested object, not flat fields. | P0 |
| BE-094 | Tasks | TaskResponse nested ReminderSummary | Create task with reminder, `GET /tasks/{id}` | Response contains `reminders: [{remindAtType:"BEFORE_START", minutesBefore:15, isActive:true}]` as nested array. | P0 |
| BE-095 | Tasks | @JsonProperty isActive serialization | Create reminder with isActive=true, GET task | Field appears as `"isActive": true` (camelCase), not `"is_active"` or `"active"`. | P0 |
| BE-096 | Tasks | Tags as flat string[] | Create task, PUT tags `["urgent","work"]`, GET task | `tags: ["urgent","work"]` — flat array of strings, not `[{name:"urgent"},{name:"work"}]`. | P0 |
| BE-097 | Tasks | Complete task creates recurrence next occurrence | 1. Create task with WEEKLY recurrence daysOfWeek=MON,WED,FRI; 2. Complete task | New task auto-created. New task has same recurrence rule. Original task status=DONE. TaskLinks NOT copied to new task. | P0 |
| BE-098 | Tasks | Soft delete cascade to children | Delete a goal that has tasks | Goal marked deleted. Tasks under goal also soft-deleted (not physically removed). | P0 |
| BE-099 | Sharing | Self-sharing prevention | User A tries `POST /api/goals/{id}/share` `{"email":"<userA's own email>"}` | 400 Bad Request. Cannot share with yourself. | P0 |
| BE-100 | Sharing | Duplicate share prevention | Share goal with user B twice | Second call returns 400/409. No duplicate share created. | P1 |
| BE-101 | Sharing | Goal owner can edit shared user's task | 1. User A shares goal with User B; 2. User B creates task in shared goal; 3. User A tries `PATCH /tasks/{B's task}` | 200 OK. Goal owner (User A) can edit tasks created by shared user (User B) via goal-ownership fallback. | P0 |
| BE-102 | Sharing | Shared user READ-only cannot edit task | 1. Share task canEdit=false; 2. Accept; 3. Try PATCH | 403 Forbidden. Read-only access enforced. | P0 |
| BE-103 | Priority | NPE on null priority | Create task without specifying priority (default null) | Task created with priority=5 (default), no NPE. | P0 |
| BE-104 | Priority | Tiered decay calculation (months>weeks>days) | 1. Configure decay: perMonth=20, perWeek=5, perDay=1; 2. Reschedule task that's 45 days old | Decay calculated as: months first (20 per 30 days), then weeks (5 per 7 days), then days (1 per day). NOT sum of all. Priority never below 1. | P0 |
| BE-105 | Priority | lastDecayAppliedAt separate from updatedAt | Reschedule task, check response | `lastDecayAppliedAt` updates on reschedule, `updatedAt` also updates. But `lastDecayAppliedAt` used for next decay calculation, not `updatedAt`. | P1 |
| BE-106 | Auth | Refresh token expiry enforced | Use refresh token after 7+ days (past expiry) | 401 Unauthorized. Expired refresh token rejected. | P0 |
| BE-107 | Settings | UserResponse includes decay config | `GET /api/me` | Response includes `greenDecay` and `redDecay` objects with `decayPerReschedule`, `decayPerDay`, `decayPerWeek`, `decayPerMonth`. | P0 |
| BE-108 | Settings | Update decay config via nested DTO | `PATCH /api/me/settings` `{"greenDecay":{"decayPerReschedule":2,"decayPerDay":1,"decayPerWeek":5,"decayPerMonth":20}}` | 200 OK. Green decay config updated. Red config unchanged. | P0 |
| BE-109 | Calendar | CalendarService transactional | Query calendar during concurrent writes | No stale reads. `@Transactional(readOnly=true)` ensures consistent snapshot. | P1 |
| BE-110 | Tasks | Generic error messages (no ex.getMessage) | Trigger any server error (e.g. 500) | Error response body contains generic message, never raw `ex.getMessage()` or stack trace. `ErrorResponse.message` is user-friendly. | P0 |
| BE-111 | Security | H2 console only in dev profile | `GET /h2-console` without dev profile | 404 Not Found. H2 console only accessible when `@Profile("dev")` is active. | P1 |
| BE-112 | Tasks | Input validation on reschedule preset | `POST /tasks/{id}/reschedule` `{"preset":"invalid"}` | 400 Bad Request. Only valid presets: "30m", "+1h", "+3h", "+24h". | P0 |
| BE-113 | Tasks | Advisory lock prevents concurrent decay | Two concurrent reschedule requests on same task | Only one succeeds at a time. No race condition on priority calculation. | P1 |
| BE-114 | Tasks | Recurrence WEEKLY daysOfWeek validation | `PUT /tasks/{id}/recurrence` `{"ruleType":"WEEKLY","intervalDays":1,"daysOfWeek":"INVALIDDAY"}` | 400 Bad Request. Only valid day abbreviations accepted. | P1 |
| BE-115 | Tasks | Multi-reminder support (3+ reminders) | `PUT /tasks/{id}/reminders` with 3 different rules | 200 OK. All 3 reminders stored and returned. Each with independent `isActive` flag. | P1 |
| BE-116 | Tasks | Links between tasks - bidirectional check | `POST /tasks/A/links` `{"linkedTaskIds":[B]}` then `GET /tasks/B` | Task B's `linkedTaskIds` may or may not include A (depends on implementation). Link at least stored on A. | P2 |
| BE-117 | Tasks | Remove recurrence | Create task with recurrence, then `DELETE /tasks/{id}/recurrence` | 200 OK. Task's recurrence field becomes null. Task still exists. | P0 |

---

## 2. Frontend Web Tests (45 + 15 new = 60)

Оригинальные FE-001 — FE-045 остаются. Новые:

| ID | Module | Test Name | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| FE-046 | Tasks | Complete task button visible | Navigate to task list, view any TODO task | "ВЫПОЛНИТЬ" (green) button visible on each task card. | P0 |
| FE-047 | Tasks | Cancel task button visible | View any task in list | "ОТМЕНИТЬ" (red) button visible on each task card. | P0 |
| FE-048 | Tasks | Click Complete sets DONE | Click "ВЫПОЛНИТЬ" on a TODO task | Toast "Задача выполнена". Task status badge changes to "ВЫПОЛНЕНО" (green). | P0 |
| FE-049 | Tasks | Click Cancel sets CANCELLED | Click "ОТМЕНИТЬ" on a task | Toast "Задача отменена". Task status badge changes to "ОТМЕНЕНО" (red). | P0 |
| FE-050 | Tasks | Links UI - add link | Click edit on task, add linked task ID, save | Linked task ID appears in task details. API call `POST /tasks/{id}/links` sent. | P1 |
| FE-051 | Tasks | Recurrence UI - set daily | Open task edit, set recurrence to DAILY, interval=1 | Recurrence badge "ЕЖЕДНЕВНО" appears on task card. `PUT /tasks/{id}/recurrence` sent. | P0 |
| FE-052 | Tasks | Recurrence UI - remove recurrence | Click remove recurrence on recurring task | Recurrence badge removed. `DELETE /tasks/{id}/recurrence` sent. | P0 |
| FE-053 | Tasks | Reminders UI - add BEFORE_START | Open task edit, add reminder BEFORE_START 15min | Reminder saved. `PUT /tasks/{id}/reminders` with `{"rules":[{"remindAtType":"BEFORE_START","minutesBefore":15,"isActive":true}]}`. | P1 |
| FE-054 | Tasks | 409 Conflict toast | Open same task in two tabs, edit in both | Second edit shows toast: "Конфликт версий. Обновите страницу." (409 handling). | P0 |
| FE-055 | Settings | Decay config UI saves correctly | Change green decay rate to 3, save | `PATCH /me/settings` sent with correct nested DTO. Reload shows persisted value. | P0 |
| FE-056 | Tasks | Tags batch save | Add 3 tags at once, save | Single `PUT /tasks/{id}/tags` with all 3 tags. No individual API calls. | P1 |
| FE-057 | PWA | PWA icons present | Check manifest.json and icon files | manifest.json has icons array with 192x192 and 512x512 PNGs. Icons load without 404. | P1 |
| FE-058 | Tasks | Status transition validation in UI | Complete a task, then try to reschedule it | Reschedule buttons disabled or hidden for DONE/CANCELLED tasks. | P0 |
| FE-059 | Calendar | Month view with shared tasks | Share goal with user B, accept, view calendar | Shared tasks appear in calendar view alongside own tasks. | P1 |
| FE-060 | Sharing | Share by email form | Navigate to sharing, enter email, select permission | Share request sent. Invitation appears in recipient's invitations list. | P0 |

---

## 3. Android E2E Tests (22 + 18 new = 40)

Оригинальные AND-001 — AND-022 остаются. Новые кейсы с точными координатами экрана (1440x3120, 560dpi):

### Координаты экрана (без клавиатуры)
- etEmail: center `(720, 954)` — bounds `[84,856][1356,1052]`
- etPassword: center `(720, 1225)` — bounds `[84,1127][1356,1323]`
- btnLogin ("Войти"): center `(720, 1431)` — bounds `[84,1347][1356,1515]`
- btnRegister ("Регистрация"): below login button
- fabAdd: center `(1286, 2602)` — bounds `[1188,2504][1384,2700]`
- Bottom nav: Calendar ~y=2900, Settings ~y=2900, Sharing ~y=2900

### Важно: adb input text требует правильного фокуса!
- Сначала `input tap` на поле для фокуса
- Затем `input text` для ввода
- НЕ нажимать BACK (keyevent 4) — закрывает диалог/активити
- Для навигации между полями использовать TAB (keyevent 61)

| ID | Module | Test Name | Steps (adb commands) | Expected Result | Priority |
|---|---|---|---|---|---|
| AND-023 | Login | Full login flow E2E | 1. `am start -n com.focus.android/.ui.MainActivity` 2. Wait 8s 3. `input tap 720 954` (email) 4. `input text "test@test.com"` 5. `input keyevent 61` (TAB) 6. `input text "password123"` 7. `input keyevent 66` (ENTER) 8. Wait 5s 9. uiautomator dump | MainActivity focused (no ANR). Folders list shown. | P0 |
| AND-024 | Login | No ANR on cold start | 1. `pm clear com.focus.android` 2. `am start` 3. Wait 12s 4. `dumpsys window \| grep mCurrentFocus` | Window = `com.focus.android/.ui.MainActivity`. No ANR dialog. TokenManager lazy init works. | P0 |
| AND-025 | Folders | Folder card visible after sync | After login, wait for sync. uiautomator dump. | `tvFolderName = "Work"` visible in CardView. RecyclerView has 1+ cards. | P0 |
| AND-026 | Navigation | Navigate folder → goal → task | 1. `input tap 720 286` (Work folder card, adjust for actual bounds) 2. Wait 5s 3. uiautomator dump shows "Sprint 1" 4. `input tap 720 526` (Sprint 1 goal card) 5. Wait 5s 6. uiautomator dump shows "Test Task 1" | Full drill-down works: Folder→Goal→Task visible. | P0 |
| AND-027 | Tasks | Task shows TODO status | Navigate to task list. uiautomator dump. | Task item shows "TODO" text and GREEN type indicator. | P0 |
| AND-028 | Tasks | Task shows reschedule buttons | Navigate to task list. uiautomator dump. | Buttons "+30м", "+1ч", "+3ч", "+24ч" visible on task card. | P0 |
| AND-029 | Tasks | Create task via FAB (GREEN) | 1. `input tap 1286 2602` (FAB) 2. Wait 3s 3. Dialog appears 4. Tap EditText area 5. `input text "NewGreenTask"` 6. Tap "Зелёная" button (positive dialog button) 7. Wait 5s 8. uiautomator dump | Dialog closes. Task list refreshes. New task "NewGreenTask" visible. | P0 |
| AND-030 | Tasks | Create task via FAB (RED) | Same as AND-029 but tap "Красная" button | Task created with RED type. Red visual indicator shown. | P0 |
| AND-031 | Bottom Nav | Calendar tab | 1. `input tap 480 2900` (Calendar tab approx) 2. Wait 3s 3. uiautomator dump | CalendarFragment shown. Calendar grid or date picker visible. | P1 |
| AND-032 | Bottom Nav | Settings tab | 1. `input tap 720 2900` (Settings tab approx) 2. Wait 3s 3. uiautomator dump | SettingsFragment shown. Language/timezone options visible. | P1 |
| AND-033 | Bottom Nav | Sharing tab | 1. `input tap 960 2900` (Sharing tab approx) 2. Wait 3s 3. uiautomator dump | SharingFragment shown. Tabs: "Поделился я", "Доступно мне", "Приглашения". | P1 |
| AND-034 | Sync | Pull-to-refresh on folders | 1. `input swipe 720 1500 720 500 500` (pull down) 2. Wait 3s 3. uiautomator dump | SwipeRefreshLayout triggers. Folders re-fetched from API. | P1 |
| AND-035 | Tasks | Task tags display | Create task with tags via API, navigate to task list. uiautomator dump. | Tags displayed as chips or text on task card. | P1 |
| AND-036 | Calendar | Day/Week/Month toggle | Navigate to Calendar, find toggle buttons. Tap each. | Calendar view switches between Day/Week/Month modes. Content adjusts. | P1 |
| AND-037 | Tasks | Edit task dialog | Long-tap or tap on task card. uiautomator dump. | Edit dialog opens with title, tags, tag input field pre-filled. | P0 |
| AND-038 | Tasks | Add tag to existing task | 1. Open edit dialog 2. Focus tag input 3. `input text "testtag"` 4. Submit 5. uiautomator dump | Tag "testtag" appears in chip group. API `PUT /tasks/{id}/tags` called. | P1 |
| AND-039 | Login | Register new user via UI | 1. `input tap` Register button 2. Fill name+email+password 3. Tap register 4. Wait 5s | User registered. Navigates to FoldersFragment. | P1 |
| AND-040 | Tasks | Priority display | View task list with different priority tasks. | Priority number shown on task card (e.g., "P5", "P10"). | P0 |

---

## 4. Integration / E2E Tests (10 + 8 new = 18)

Оригинальные INT-001 — INT-010 остаются. Новые:

| ID | Module | Test Name | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| INT-011 | Status | Full lifecycle: TODO → IN_PROGRESS → DONE | 1. Create task (status=TODO) 2. `PATCH /tasks/{id}` status=IN_PROGRESS 3. `POST /tasks/{id}/complete` | Status transitions: TODO→IN_PROGRESS→DONE. Each step returns 200. Invalid reverse transitions rejected. | P0 |
| INT-012 | Status | Full lifecycle: TODO → IN_PROGRESS → CANCELLED | 1. Create task 2. Set IN_PROGRESS 3. `POST /tasks/{id}/cancel` | Status: TODO→IN_PROGRESS→CANCELLED. | P0 |
| INT-013 | Decay | lastDecayAppliedAt not overwritten | 1. Create task 2. Wait 1min 3. Update task title 4. Check lastDecayAppliedAt | `lastDecayAppliedAt` unchanged by title update (only changed on reschedule). `updatedAt` changed by both. | P1 |
| INT-014 | Sharing | Goal owner edits shared user's task | 1. User A creates goal with task 2. Share goal with User B (canEdit=true) 3. User B creates task in goal 4. User A edits User B's task | 200 OK. Goal ownership grants edit access to all tasks in goal. | P0 |
| INT-015 | Recurrence | WEEKLY next occurrence correct day | 1. Create task plannedTime=Monday 2. Set WEEKLY recurrence daysOfWeek=MON,WED,FRI 3. Complete task | New task created for Wednesday (next valid day in daysOfWeek). plannedTime correct. | P0 |
| INT-016 | Android | Backend→Android sync verified | 1. Create folder+goal+task via API 2. Restart Android app 3. Navigate to folder→goal | Task "Test Task 1" visible on Android. Sync Worker fetched from server. | P0 |
| INT-017 | Android | Android task appears on backend | 1. Create task on Android 2. Check `GET /api/goals/{id}/tasks` on backend | Task created by Android visible via API. Data consistent. | P0 |
| INT-018 | Multi-reminder | Set 3 reminders, verify all fire | 1. Create task with 3 reminders (BEFORE_START 15m, AT_START 0m, BEFORE_DEADLINE 60m) 2. GET task | All 3 reminders returned in array. Each with unique remindAtType and correct minutesBefore. | P1 |

---

## 5. Security & Performance (13 + 5 new = 18)

Оригинальные SEC-001 — SEC-010, PERF-001 — PERF-003 остаются. Новые:

| ID | Module | Test Name | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| SEC-011 | Sharing | Self-sharing via share endpoint | `POST /api/goals/{id}/share` with own email | 400 Bad Request. Self-sharing explicitly blocked. | P0 |
| SEC-012 | Input | XSS in task title | Create task with title `<script>alert(1)</script>` | Title stored as-is (escaped in response). No script execution on frontend. | P0 |
| SEC-013 | Input | SQL injection in folder name | Create folder with name `'; DROP TABLE folders;--` | 200 OK. Folder name stored as literal string. No SQL injection. Table still exists. | P0 |
| SEC-014 | Auth | Brute force rate limiting | Send 50 login attempts with wrong password | After N failures, additional attempts return 429 Too Many Requests or increasing delay. | P1 |
| SEC-015 | Error | No stack trace in error responses | Trigger 500 error (e.g., malformed JSON body) | Response body contains `ErrorResponse` with generic message. No Java stack trace, no `ex.getMessage()`. | P0 |
| PERF-004 | Decay | Priority calculation with 1000 tasks | Create 1000 tasks, trigger batch decay calculation | Batch completes in < 10 seconds. Advisory lock prevents concurrent decay. | P2 |

---

## Итоговая таблица v2

| Секция | Оригинал | Новые | Итого | P0 | P1 | P2 |
|---|---|---|---|---|---|---|
| 1. Backend API | 87 | 30 | 117 | 72 | 34 | 11 |
| 2. Frontend Web | 45 | 15 | 60 | 40 | 17 | 3 |
| 3. Android E2E | 22 | 18 | 40 | 25 | 13 | 2 |
| 4. Integration | 10 | 8 | 18 | 13 | 5 | 0 |
| 5. Security/Perf | 13 | 5 | 18 | 10 | 5 | 3 |
| **Итого** | **177** | **76** | **253** | **160** | **74** | **19** |

### Приоритеты
- **P0**: Критичный функционал. Блокеры релиза. Должны проходить при каждом билде.
- **P1**: Важные edge cases и вторичные флои. Должны проходить до релиза.
- **P2**: Желательные. Неблокирующие. Можно отложить.

### Порядок выполнения
1. Backend API P0 → все эндпоинты с валидными/невалидными данными
2. Security P0 → JWT, хеширование, CORS, изоляция данных
3. Frontend Web P0 → после зеленого бэкенда
4. Android E2E P0 → на эмуляторе emulator-5554 после бэкенда
5. Integration P0 → кросс-платформенные флои
6. P1/P2 → после всех P0

### Инструменты
- Backend: `Invoke-WebRequest` (PowerShell) / curl
- Frontend: `WebFetch` (opencode) + URL fetch + DOM inspection
- Android: `adb shell input tap/text/keyevent` + `uiautomator dump`
- Security: `rg` (ripgrep), ручные curl-запросы
