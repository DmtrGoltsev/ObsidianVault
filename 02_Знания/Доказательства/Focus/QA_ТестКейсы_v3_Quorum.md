---
id: "qa-testcases-v3-quorum"
тип: "доказательство"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-09"
обновлено: "2026-06-09"
уверенность: "высокая"
источники:
  - "[[QA_ТестКейсы_v2]]"
  - "[[QA_Результаты]]"
  - "[[Focus]]"
теги:
  - "focus"
  - "QA"
  - "e2e"
  - "quorum"
  - "тест-кейсы"
---

# QA Тест-кейсы v3 — E2E (Кворум)

> **Методология:** 3 независимых QA-лида (максимально критичных) предложили тест-кейсы.
> В финальный файл вошли только темы, подтверждённые **≥2 из 3** QA-лидов (кворум).
> 
> **Продакшн-сервер:** HexCore (`45.10.110.42`), API: `http://45.10.110.42/focus-api/`
> **Android эмулятор:** `OpenCode` (запущен локально)
> **Всего кворумных кейсов:** 47

---

## Статистика

| Категория | Всего | P0 | P1 | P2 | Prod | Emulator |
|-----------|---|------|------|------|------|----------|
| Auth & JWT | 6 | 5 | 1 | 0 | 4 | 1 |
| Data Isolation & Security | 7 | 6 | 1 | 0 | 4 | 0 |
| Sharing Flow | 6 | 4 | 2 | 0 | 2 | 2 |
| Recurrence | 3 | 2 | 1 | 0 | 0 | 0 |
| Priority Decay | 2 | 1 | 1 | 0 | 0 | 1 |
| Tasks CRUD & Lifecycle | 5 | 3 | 2 | 0 | 0 | 1 |
| Soft Delete Cascade | 2 | 2 | 0 | 0 | 0 | 0 |
| Calendar | 2 | 0 | 2 | 0 | 0 | 1 |
| Settings | 2 | 0 | 2 | 0 | 1 | 1 |
| Emulator Core | 8 | 5 | 2 | 1 | 0 | 8 |
| Emulator Sync | 6 | 4 | 1 | 1 | 2 | 6 |
| Cross-Client | 2 | 2 | 0 | 0 | 2 | 2 |
| Concurrent & Race | 2 | 2 | 0 | 0 | 0 | 0 |
| **ИТОГО** | **47** | **33** | **12** | **2** | **14** | **20** |

---

## 1. Auth & JWT (6 кейсов — кворум 3/3)

### QE-001 — JWT Refresh Flow + Token Rotation
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-001, QA2-005, QA3-010

**Шаги:**
1. `POST /focus-api/api/auth/register` → сохранить accessToken1, refreshToken1
2. `POST /focus-api/api/auth/refresh` с refreshToken1 → получить accessToken2, refreshToken2
3. Повторный `POST /focus-api/api/auth/refresh` с refreshToken1
4. `GET /focus-api/api/folders` с accessToken1 (старый, до истечения)

**Ожидаемый результат:**
- Шаг 2: 200 OK, новые токены (refreshToken2 ≠ refreshToken1)
- Шаг 3: 401 Unauthorized — старый refresh инвалидирован
- Шаг 4: 200 OK — старый access работает до истечения (refresh rotation не отзывает access)

---

### QE-002 — Logout инвалидирует все refresh токены
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-002, QA2-007, QA3 (token persistence)

**Шаги:**
1. Login user A → accessTokenA, refreshTokenA1
2. Повторный login user A → accessTokenA2, refreshTokenA2
3. `POST /focus-api/api/auth/logout` с accessTokenA2
4. `POST /focus-api/api/auth/refresh` с refreshTokenA1
5. `POST /focus-api/api/auth/refresh` с refreshTokenA2

**Ожидаемый результат:**
- Шаг 3: 200 OK
- Шаги 4-5: 401 Unauthorized — ВСЕ refresh токены пользователя revoked

---

### QE-003 — Неавторизованный доступ → 401 на все защищённые endpoint'ы
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-027, QA2-038, QA3-001

**Шаги:**
Без Authorization header выполнить: GET /api/folders, POST /api/folders, GET /api/goals/{id},
GET /api/tasks/{id}, GET /api/calendar, GET /api/me, GET /api/shares

**Ожидаемый результат:**
Все возвращают 401. Только `/api/auth/**` и `/api/health` доступны без токена.

---

### QE-004 — Password Hashing: BCrypt, без plaintext в ответах
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA2-004, QA1 (security implied), QA3-002

**Шаги:**
1. Зарегистрировать пользователя через API
2. Проверить тело ответа на наличие password/passwordHash
3. Проверить БД: `SELECT password_hash FROM users WHERE email=...`

**Ожидаемый результат:**
Ответ не содержит password/passwordHash. В БД хеш начинается с `$2a$` (BCrypt).

---

### QE-005 — Refresh token разных пользователей не пересекаются
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA2-029, QA1 (token isolation), QA3-034

**Шаги:**
1. User A: login → refreshTokenA
2. User B: login → refreshTokenB
3. User A: `POST /api/auth/refresh` с refreshTokenB

**Ожидаемый результат:**
Шаг 3: 401. Refresh token привязан к конкретному пользователю. Cross-user refresh недопустим.

---

### QE-006 — Android: Login Persistence — токен переживает перезапуск приложения
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-011, QA1-028, QA2-032

**Шаги:**
1. Эмулятор OpenCode: авторизоваться
2. Закрыть приложение (force stop)
3. Открыть заново
4. Проверить что LoginFragment не показывается

**Ожидаемый результат:**
TokenManager сохранил токены в EncryptedSharedPreferences. Приложение стартует с главного экрана. GET /api/me возвращает 200.

---

## 2. Data Isolation & Security (7 кейсов)

### QE-007 — Cross-User Isolation: User A не видит данные User B
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-004, QA2-018, QA3 (implied in architecture)

**Шаги:**
1. User A: создать FolderA → GoalA → TaskA1
2. User B: с токеном B попытаться GET/PATCH/DELETE/complete/reschedule/tags/links/recurrence/reminders/share для TaskA1 и GoalA1

**Ожидаемый результат:**
Все запросы User B к данным User A возвращают 404 (не 403, не 200). Ни один эндпоинт не раскрывает чужие данные.

---

### QE-008 — IDOR: Подмена ID чужой задачи → 404
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA2-018, QA1-004, QA3 (cross-user)

**Шаги:**
1. User A создаёт task id=X
2. User B: GET /api/tasks/X, PATCH /api/tasks/X, DELETE /api/tasks/X, POST /api/tasks/X/complete

**Ожидаемый результат:**
Все 404. User B не может прочитать/изменить/удалить/завершить чужую задачу через подмену ID.

---

### QE-009 — Share IDOR: Нельзя принять/отклонить чужое приглашение
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA2-030, QA1 (share flow validates), QA3-025

**Шаги:**
1. User A делится с User C (shareId=S1)
2. User B пытается: POST /api/shares/S1/accept, POST /api/shares/S1/decline

**Ожидаемый результат:**
404. ShareRepository.findByIdAndSharedWithEmail проверяет email текущего пользователя.

---

### QE-010 — Self-Share заблокирован
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-008, QA2-016, QA3 (implied)

**Шаги:**
1. User A создаёт Goal
2. User A: POST /api/goals/{id}/share с email=свой_же_email

**Ожидаемый результат:**
400 Bad Request. Сообщение: «Нельзя поделиться с самим собой». Share запись не создана.

---

### QE-011 — SQL Injection защита (email, folder name, task title)
- **Модуль:** Integration
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA2-009, QA2-010, QA1-025 (validation)

**Шаги:**
1. Register с email `test@test.com' OR '1'='1`
2. Создать folder с name `test'); DROP TABLE folders; --`
3. Проверить что таблицы целы

**Ожидаемый результат:**
Шаг 1: 400 (email validation) или создание с буквальной строкой. Шаг 2: 201 (имя как строка). Никаких 500 ошибок. JPA параметризованные запросы предотвращают инъекцию.

---

### QE-012 — XSS Protection: script-теги в title/description
- **Модуль:** Integration
- **Приоритет:** P1
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA2-011, QA2-012, QA1 (validation)

**Шаги:**
1. Создать task с title `<script>alert(1)</script>` и description `<img src=x onerror=alert(1)>`
2. GET /api/tasks/{id}

**Ожидаемый результат:**
201 Created. API возвращает строку как есть (без модификации). React-фронтенд экранирует при рендеринге. Нет 500 ошибок.

---

### QE-013 — Валидация входных данных (email формат, priority, title length)
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-025, QA2-026, QA2-027

**Шаги:**
1. Register с email `not-an-email` → 400 (@Email)
2. Register с password `12345` → 400 (@Size min=6)
3. Create task с priority=0 → 400 (@Min(1))
4. Create task с priority=11 → 400 (@Max(10))
5. Create task с title из 501 символа → 400 (@Size max=500)
6. Create folder с name='' → 400 (@NotBlank)

**Ожидаемый результат:**
Все 400 Bad Request с типом Validation Error, конкретным field error сообщением.

---

## 3. Sharing Flow (6 кейсов)

### QE-014 — Полный Sharing Flow: Share → Accept → Edit → Owner verify
- **Модуль:** Integration
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-005, QA2 (sharing theme), QA3-009

**Шаги:**
1. User A: FolderA → GoalA, share GoalA с User B (canEdit=true)
2. User B: GET /api/shares/invitations → PENDING
3. User B: POST /api/shares/{id}/accept → ACCEPTED
4. User B: POST /api/goals/{id}/tasks → 201 (создать задачу)
5. User B: PATCH /api/tasks/{id} → 200 (редактировать)
6. User A: GET /api/goals/{id}/tasks → видит задачу User B

**Ожидаемый результат:**
Полный цикл работает. Shared user может создавать/редактировать/завершать задачи. Owner видит изменения.

---

### QE-015 — Sharing Read-Only: canEdit=false запрещает запись
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-006, QA2-019, QA3 (sharing theme)

**Шаги:**
1. User A: share Goal с User C, canEdit=false
2. User C: accept → GET /api/goals/{id} → 200 (READ ok)
3. User C: POST /api/goals/{id}/tasks → ожидать 400/403
4. User C: PATCH /api/tasks/{id} → ожидать 403

**Ожидаемый результат:**
canEdit=false: shared user может только читать. Создание/редактирование goals/tasks запрещено.

---

### QE-016 — Sharing: Decline → Re-Share переиспользует существующую запись
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-007, QA2-015

**Шаги:**
1. User A share Goal с User D → share_id=X, PENDING
2. User D: POST /api/shares/X/decline → DECLINED
3. User A: повторный share того же Goal с User D

**Ожидаемый результат:**
Шаг 3: 200 OK. Статус меняется DECLINED→PENDING. Новая запись не создаётся (переиспользуется существующая).

---

### QE-017 — Owner всегда имеет доступ без share записи
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA2-017, QA1 (owner access implied)

**Шаги:**
1. User A создаёт task
2. Проверить БД: нет share записи для User A к этой задаче
3. User A: GET /api/tasks/{id}

**Ожидаемый результат:**
200 OK. Владелец имеет доступ по праву ownership (findByIdAndUserId) без проверки share записей.

---

### QE-018 — Android: Принятие share invitation и просмотр расшаренной цели
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-031, QA3-025

**Шаги:**
1. User A (через API) шарит Goal с email Android-пользователя
2. Эмулятор OpenCode: Sharing → Invitations → видит PENDING
3. Нажать Accept → статус ACCEPTED
4. Перейти в Goals → расшаренная цель видна
5. Открыть цель → задачи внутри видны

**Ожидаемый результат:**
Android корректно отображает invitation list. Accept меняет статус. Расшаренная цель доступна в Goals.

---

### QE-019 — Android: Создание share через Android UI
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Да
- **Emulator:** Да
- **Кворум:** QA3-025, QA1 (sharing on emulator)

**Шаги:**
1. Эмулятор OpenCode: Goal → Share
2. Ввести email получателя, подтвердить
3. Проверить через API: GET /api/shares → запись присутствует, PENDING
4. Получатель: GET /api/shares/invitations → видит приглашение

**Ожидаемый результат:**
Шаринг создаётся через Android UI. Сервер возвращает share с корректными полями.

---

## 4. Recurrence (3 кейса)

### QE-020 — DAILY Recurrence: Complete → Next Occurrence создан
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-009, QA2-023, QA3-020

**Шаги:**
1. Создать task с plannedTime=завтра 10:00, deadline=завтра 12:00
2. PUT /api/tasks/{id}/recurrence DAILY, intervalDays=1
3. POST /api/tasks/{id}/complete → статус DONE
4. GET /api/goals/{goalId}/tasks

**Ожидаемый результат:**
Новая задача создана с plannedTime=послезавтра 10:00, deadline=послезавтра 12:00.
Теги, напоминания, recurrence rule скопированы. Исходная задача DONE, новая TODO.

---

### QE-021 — WEEKLY Recurrence с daysOfWeek: правильный переход по дням
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-010, QA2-040

**Шаги:**
1. Создать task с plannedTime=понедельник 10:00 UTC
2. PUT recurrence WEEKLY, daysOfWeek="WED,FRI"
3. POST /api/tasks/{id}/complete

**Ожидаемый результат:**
Next occurrence: среда 10:00. Затем пятница 10:00. Затем следующий понедельник (через неделю).

---

### QE-022 — Recurrence не создаёт бесконечный цикл
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA2-023, QA1-009 (implicit)

**Шаги:**
1. Создать task с DAILY recurrence
2. Complete 5 раз подряд
3. GET /api/goals/{goalId}/tasks

**Ожидаемый результат:**
5 задач DONE + 1 задача TODO (последняя). Каждый complete создаёт ровно 1 новый task.
Нет рекурсивного создания. PlannedTime корректно сдвигается.

---

## 5. Priority Decay (2 кейса)

### QE-023 — Priority Decay: Reschedule 5 раз снижает priority до 1
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-013, QA2 (decay theme), QA3-019

**Шаги:**
1. Настроить greenDecay.decayPerReschedule=2
2. Создать GREEN task priority=10
3. Reschedule +30m ×5 (priority: 10→8→6→4→2→1)
4. Reschedule +30m ещё раз

**Ожидаемый результат:**
После 5 решедулов: priority=1 (floor). 6-й решедул не опускает priority ниже 1.

---

### QE-024 — Android: Reschedule чипсы + проверка decay на эмуляторе
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-029 (reschedule), QA3-019

**Шаги:**
1. Эмулятор OpenCode: открыть задачу с plannedTime
2. Нажать чипс +30m → plannedTime +30min
3. Нажать чипс +1h → plannedTime +1h
4. Нажать чипс +3h → +3h
5. Нажать чипс +24h → +24h
6. Проверить через API priority уменьшился

**Ожидаемый результат:**
API: POST /api/tasks/{id}/reschedule с preset. Priority уменьшается согласно decayPerReschedule.

---

## 6. Tasks CRUD & Lifecycle (5 кейсов)

### QE-025 — Complete/Cancel: Валидные и невалидные переходы статусов
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-017, QA2-039, QA3-020/021

**Шаги:**
1. TODO → IN_PROGRESS (PATCH) → DONE (complete) — 200
2. TODO → CANCELLED (cancel) — 200
3. IN_PROGRESS → CANCELLED — 200
4. DONE → complete повторно — 400
5. CANCELLED → complete — 400
6. DONE → TODO — 400
7. Создание с status=DONE — 400

**Ожидаемый результат:**
Валидные переходы: TODO→IN_PROGRESS→DONE, TODO→CANCELLED, IN_PROGRESS→CANCELLED.
Невалидные возвращают 400 с понятным сообщением.

---

### QE-026 — Reschedule: 4 пресета работают, невалидный → 400
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-018, QA2 (preset tests), QA3-019

**Шаги:**
1. Создать task plannedTime=now
2. Reschedule "+30m", "+1h", "+3h", "+24h" → каждый 200
3. Reschedule "+5h" → 400
4. Reschedule "" → 400
5. Complete task → Reschedule → 400

**Ожидаемый результат:**
4 валидных пресета работают. Неизвестный/пустой → 400. Reschedule завершённой задачи → 400.

---

### QE-027 — Tags: Полная замена, очистка, null
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-019, QA2 (tags theme), QA3-022

**Шаги:**
1. PUT /api/tasks/{id}/tags {tags:["a","b","c"]} → 200, tags=["a","b","c"]
2. PUT {tags:["new"]} → tags=["new"] (старые удалены)
3. PUT {tags:[]} → tags=[] (очистка)
4. PUT {} → tags остаётся [] (null не очищает)

**Ожидаемый результат:**
Теги полностью заменяются при каждом PUT. Пустой массив очищает.

---

### QE-028 — Multiple Reminders + fired flag не дублируется
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-021/022, QA2-024

**Шаги:**
1. Создать task, установить 3 reminder'а (BEFORE_START, AT_START, BEFORE_DEADLINE)
2. GET /api/tasks/{id} → 3 reminder'а, все fired=false
3. Reschedule task → все fired сброшены в false
4. Установить 1 reminder (старые удалены при setReminders)

**Ожидаемый результат:**
Можно установить несколько reminder'ов. fired сбрасывается при reschedule. setReminders полностью заменяет список. ReminderScheduler выставляет fired=true однократно.

---

### QE-029 — Android: Complete/Cancel задачи на эмуляторе
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-020, QA3-021, QA1 (task lifecycle)

**Шаги:**
1. Эмулятор OpenCode: создать задачу с DAILY recurrence
2. Нажать Complete → задача DONE + next occurrence создан
3. Создать задачу2 → нажать Cancel → CANCELLED

**Ожидаемый результат:**
API: POST /api/tasks/{id}/complete → 200, DONE. При recurrence создаётся next occurrence.
Cancel: CANCELLED, recurrence не создаёт новое вхождение.

---

## 7. Soft Delete Cascade (2 кейса)

### QE-030 — Soft-Delete Folder → Goals + Tasks каскадно недоступны
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-015, QA2-013, QA3-014/035

**Шаги:**
1. Folder → Goal1(Task1, Task2) → Goal2(Task3)
2. DELETE /api/folders/{id} → 204
3. GET /api/folders → folder не отображается
4. GET /api/folders/{id}/goals → 404
5. GET /api/goals/{Goal1_id} → 404
6. GET /api/tasks/{Task1_id} → 404

**Ожидаемый результат:**
Все дочерние сущности недоступны через API. В БД deleted=true у всех.

---

### QE-031 — Soft-Delete Goal → Tasks каскадно; Folder остаётся
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-016, QA2-013

**Шаги:**
1. Folder с GoalA(TaskA1,TaskA2) и GoalB(TaskB1)
2. DELETE /api/goals/{GoalA_id} → 204
3. GET /api/folders/{id}/goals → только GoalB
4. GET /api/tasks/{TaskA1_id} → 404
5. GET /api/tasks/{TaskB1_id} → 200

**Ожидаемый результат:**
GoalA и его tasks недоступны. GoalB не затронут. Folder не удалён.

---

## 8. Calendar (2 кейса)

### QE-032 — Calendar: Day/Week/Month границы и фильтрация
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-023, QA2 (calendar params), QA3-007

**Шаги:**
1. Создать задачи: сегодня, today+3d, today+10d, today+35d
2. GET /api/calendar?from=<today>&to=<today 23:59> → только сегодня
3. GET /api/calendar?from=<today>&to=<today+7d> → сегодня + today+3d
4. GET /api/calendar?from=<today>&to=<today+30d> → первые три
5. GET /api/calendar?from=<today+30d>&to=<today+40d> → только today+35d

**Ожидаемый результат:**
Корректная фильтрация по plannedTime/deadline в заданном диапазоне.

---

### QE-033 — Android: Calendar Views — переключение Day/Week/Month
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-032, QA3-023

**Шаги:**
1. Эмулятор OpenCode: Calendar tab
2. MONTH view → задачи на соответствующих днях
3. WEEK view → 7-дневная сетка
4. DAY view → задачи на выбранный день с временем
5. GREEN/RED задачи визуально различимы

**Ожидаемый результат:**
Все три view отображаются без крешей. API запросы с корректными from/to. Цветовая индикация работает.

---

## 9. Settings (2 кейса)

### QE-034 — Settings: Сохранение language, timezone, decay config
- **Модуль:** Backend
- **Приоритет:** P1
- **Prod:** Да
- **Emulator:** Нет
- **Кворум:** QA1-024, QA2-025, QA3-008

**Шаги:**
1. GET /api/me → сохранить текущие настройки
2. PATCH /api/me/settings с language, timezone, greenDecay, redDecay
3. GET /api/me → все поля обновлены
4. PATCH только language → остальные поля не сброшены

**Ожидаемый результат:**
Настройки сохраняются и возвращаются. Частичный PATCH не сбрасывает неуказанные поля.

---

### QE-035 — Android: Language Switch и Settings Persistence
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-033, QA3-024, QA3-027

**Шаги:**
1. Эмулятор OpenCode: Settings → RU (default)
2. Переключить на EN → UI обновляется мгновенно
3. Перезапустить приложение → язык EN сохранился
4. Изменить timezone, decay, перезапустить → все сохранилось

**Ожидаемый результат:**
Смена языка применяется без перезапуска. После перезапуска настройки восстанавливаются.
Сервер получает PATCH /api/me/settings с корректными значениями.

---

## 10. Emulator Core (8 кейсов)

### QE-036 — EMU: Установка APK и запуск на эмуляторе OpenCode
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA2-031, QA3-011, QA1-028

**Шаги:**
1. `adb -s OpenCode install apk/app-debug.apk`
2. `adb -s OpenCode shell am start -n com.focus.android/.ui.MainActivity`
3. Проверить logcat на FATAL EXCEPTION

**Ожидаемый результат:**
APK устанавливается. Приложение запускается без crash. Отображается LoginFragment или FoldersFragment.

---

### QE-037 — EMU: Логин с валидными credentials
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA2-032, QA1-028, QA3-011

**Шаги:**
1. Эмулятор OpenCode: экран Login
2. Ввести email + password тестового пользователя
3. Нажать ВОЙТИ
4. Проверить переход на FoldersFragment

**Ожидаемый результат:**
ProgressBar во время запроса. После успеха — список папок. Token сохранён в EncryptedSharedPreferences.

---

### QE-038 — EMU: Логин с неверным паролем — ошибка
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA2-033, QA3 (login flow)

**Шаги:**
1. Эмулятор OpenCode: Login
2. Правильный email + неправильный пароль
3. Нажать ВОЙТИ

**Ожидаемый результат:**
Toast с ошибкой. Приложение остаётся на экране логина. Нет перехода на Folders.

---

### QE-039 — EMU: FAB Create Folder
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA2-035, QA3-012

**Шаги:**
1. Эмулятор OpenCode: Folders tab
2. Нажать FAB (+)
3. Ввести имя папки, нажать Создать
4. Проверить Room: SELECT * FROM folders WHERE name=...
5. Проверить API: GET /api/folders

**Ожидаемый результат:**
Папка в UI. В Room synced=1, serverId != null. Сервер возвращает папку.

---

### QE-040 — EMU: Pull-to-Refresh списка папок
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-013, QA2-034

**Шаги:**
1. Эмулятор OpenCode: Folders tab
2. Через API создать новую папку на сервере
3. Выполнить pull-to-refresh
4. Проверить что новая папка появилась

**Ожидаемый результат:**
SwipeRefreshLayout показывает индикатор. После обновления новая папка в списке. Нет дубликатов.

---

### QE-041 — EMU: Swipe-to-Delete папки/цели/задачи
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-014, QA3-035, QA2 (swipe navigation)

**Шаги:**
1. Эмулятор OpenCode: свайп влево по папке → подтвердить
2. Проверить что папка исчезла из UI
3. Проверить API: deleted=true (soft delete)
4. Повторить для Goal и Task

**Ожидаемый результат:**
Свайп работает для всех трёх сущностей. Soft-delete на сервере. В Room запись синхронизирована.

---

### QE-042 — EMU: Навигация Folders → Goals → Tasks
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA2-036, QA1 (navigates goals/tasks)

**Шаги:**
1. Эмулятор OpenCode: тап по папке → GoalsFragment
2. Тап по цели → TasksFragment
3. Проверить GREEN/RED различие, priority badge
4. Проверить reschedule чипсы

**Ожидаемый результат:**
Корректная навигация. Задачи с цветовой индикацией. Reschedule чипсы работают.

---

### QE-043 — EMU: FCM Push уведомление
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-030, QA3-026

**Шаги:**
1. Эмулятор OpenCode: авторизоваться (FCM token зарегистрирован)
2. Свернуть приложение
3. Создать задачу с reminder AT_START (plannedTime +2min)
4. Дождаться срабатывания ReminderScheduler
5. Проверить системное уведомление

**Ожидаемый результат:**
Push-уведомление в системном трее. При нажатии открывается приложение.

---

## 11. Emulator Sync (6 кейсов)

### QE-044 — EMU: Offline Create → Sync
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA1-029, QA3-015

**Шаги:**
1. Эмулятор OpenCode: Airplane mode ON
2. Создать задачу → в Room synced=0, serverId=null
3. Airplane mode OFF
4. Дождаться SyncWorker
5. Проверить API: задача на сервере
6. Проверить Room: synced=1, serverId != null

**Ожидаемый результат:**
Офлайн задача синхронизируется. Все поля корректны. Нет дубликатов.

---

### QE-045 — EMU: Offline Update → Sync
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-016, QA1 (offline sync)

**Шаги:**
1. Создать задачу онлайн (синхронизирована)
2. Airplane mode ON
3. Изменить title, priority, сохранить
4. Airplane mode OFF → SyncWorker
5. Проверить API: изменения применены

**Ожидаемый результат:**
Изменения сохранены локально. После синхронизации сервер отражает новые значения.

---

### QE-046 — EMU: Offline Delete → Sync
- **Модуль:** Android
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-017, QA1 (offline sync)

**Шаги:**
1. Создать задачу онлайн
2. Airplane mode ON
3. Удалить задачу → исчезла из UI, Room deleted=1, synced=0
4. Airplane mode OFF → SyncWorker
5. Проверить API: deleted=true
6. Проверить Room: запись физически удалена

**Ожидаемый результат:**
Удаление синхронизировано. Сервер soft-delete. Room хард-делит после синхронизации.

---

### QE-047 — EMU: Full Offline Cycle (Create + Update + Delete) → Sync
- **Модуль:** Integration
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-018, QA1 (offline test), QA2 (cross-client)

**Шаги:**
1. Airplane mode ON
2. Создать папку → цель → Task1(update), Task2(delete)
3. Изменить Task1 priority 5→2
4. Удалить Task2
5. Airplane mode OFF → синхронизация
6. API: папка, цель, Task1 созданы/обновлены, Task2 deleted=true
7. Порядок: CREATE → UPDATE → DELETE

**Ожидаемый результат:**
Все операции синхронизированы в правильном порядке. Сервер консистентен. Room synced=1 для всех.

---

### QE-048 — EMU: Предотвращение дублирования синхронизации (Idempotency)
- **Модуль:** Android
- **Приоритет:** P1
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-031, QA2 (duplicate sync)

**Шаги:**
1. Эмулятор OpenCode: создать задачу онлайн
2. Форсировать SyncWorker 3 раза подряд
3. Проверить API: ровно одна запись задачи
4. Повторить с офлайн созданием + форсировать SyncWorker 2 раза

**Ожидаемый результат:**
Множественные вызовы SyncWorker не создают дубликатов. synced=1 предотвращает повторные CREATE.

---

### QE-049 — EMU: Slow Connection Sync + Exponential Backoff
- **Модуль:** Android
- **Приоритет:** P2
- **Prod:** Нет
- **Emulator:** Да
- **Кворум:** QA3-028, QA3-033, QA2 (backoff)

**Шаги:**
1. Airplane mode ON → создать 3 задачи, 1 цель, 1 папку
2. Включить сеть с троттлингом (2G/EDGE, 10% packet loss)
3. Наблюдать за синхронизацией

**Ожидаемый результат:**
Все 5 сущностей синхронизированы. Exponential backoff при таймаутах. Частично синхронизированные не дублируются.

---

## 12. Cross-Client Consistency (2 кейса)

### QE-050 — Web → Android: Создать на Web, увидеть на Android
- **Модуль:** Integration
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Да
- **Кворум:** QA2-037, QA3-029, QA1 (full flow)

**Шаги:**
1. Web (через API): создать folder, goal, task
2. Эмулятор OpenCode: тот же пользователь, pull-to-refresh
3. Открыть папку → цель → задача

**Ожидаемый результат:**
Android отображает все данные с Web. Названия, статусы, priority консистентны.

---

### QE-051 — Android → Web: Создать на Android, увидеть на Web
- **Модуль:** Integration
- **Приоритет:** P0
- **Prod:** Да
- **Emulator:** Да
- **Кворум:** QA3-030, QA2-037, QA1-034

**Шаги:**
1. Эмулятор OpenCode: создать задачу
2. Дождаться синхронизации
3. Web (через API): GET /api/goals/{goalId}/tasks → задача присутствует
4. Проверить все поля: title, taskType, priority, goalId

**Ожидаемый результат:**
Задача видна в Web-интерфейсе. Круговой цикл Android→Server→Web работает без потери данных.

---

## 13. Concurrent & Race Conditions (2 кейса)

### QE-052 — Race Condition: Два одновременных complete одной задачи
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-035, QA2-020

**Шаги:**
1. Создать task status=TODO
2. Отправить ДВА параллельных POST /api/tasks/{id}/complete
3. Проверить оба HTTP статуса и конечное состояние задачи

**Ожидаемый результат:**
Один: 200 DONE. Второй: 400 «Нельзя завершить задачу в статусе DONE». Нет двойного завершения. Нет 500.

---

### QE-053 — Optimistic Locking: Два клиента → 409 Conflict
- **Модуль:** Backend
- **Приоритет:** P0
- **Prod:** Нет
- **Emulator:** Нет
- **Кворум:** QA1-003, QA2-021, QA3-032

**Шаги:**
1. Создать task (version=0)
2. Клиент A: PATCH с version=0 → 200, version=1
3. Клиент B: PATCH с version=0 → 409 Conflict
4. Клиент B: PATCH без version → 200 (безусловный update)

**Ожидаемый результат:**
409 при несовпадении version. @Version предотвращает lost update. Безусловный PATCH (без version) применяется.

---

## Сводка по приоритетам

| Приоритет | Количество | Кейсы |
|-----------|-----------|-------|
| P0 | 33 | QE-001–004, QE-006–010, QE-013, QE-014, QE-017, QE-020, QE-021, QE-023, QE-031, QE-036–039, QE-044–048, QE-050–053 |
| P1 | 12 | QE-005, QE-012, QE-016, QE-018, QE-019, QE-022, QE-024–029, QE-032–035, QE-040–043 |
| P2 | 2 | QE-025? Нет — QE-049 |

---

## Порядок выполнения

1. **Фаза 1 — Prod Smoke (6 кейсов, все P0):** QE-001, QE-002, QE-003, QE-004, QE-011, QE-013
2. **Фаза 2 — Backend Core (15 кейсов):** QE-005, QE-007–010, QE-014–017, QE-020–023, QE-030–031, QE-052–053
3. **Фаза 3 — Tasks & Features (10 кейсов):** QE-012, QE-025–029, QE-032, QE-034
4. **Фаза 4 — Emulator Setup (3 кейса):** QE-036, QE-037, QE-039
5. **Фаза 5 — Emulator Full (17 кейсов):** QE-006, QE-018, QE-019, QE-024, QE-029, QE-033, QE-035, QE-038, QE-040–043
6. **Фаза 6 — Sync & Cross-Client (6 кейсов):** QE-044–051
7. **Фаза 7 — Concurrent (2 кейса):** QE-052–053

**Параллельно можно:** Фазы 1+2+3 (все Backend), Фазы 4+5 (Emulator). Фаза 6 зависит от Фаз 1–5. Фаза 7 независима.

---

## Ссылки

- [[Focus]] — главная заметка проекта
- [[QA_ТестКейсы_v2]] — предыдущая версия тест-кейсов (253)
- [[QA_Результаты]] — результаты прогонов
- [[Регламент_Деплоя_Focus]] — процедура деплоя на прод
- [[HexCore]] — production-сервер
