---
id: "proj-focus-fixplan-001"
тип: "задача"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-04"
обновлено: "2026-06-04"
уверенность: "высокая"
источники:
  - "[[Аудит_Реальный_Статус]]"
  - "[[Источник_Промпт]]"
  - "[[Focus]]"
теги:
  - "focus"
  - "план"
  - "исправления"
  - "баги"
---

# План исправлений Focus

> Этот документ — самодостаточный план для исполнителя (нового чата).
> Все пути файлов указаны от корня проекта `C:\Users\style\Documents\VS_Agents\Focus`.

## Контекст проекта

**Focus** — планировщик задач с GREEN/RED типами, Priority Decay, Recurrence, Reminders, Sharing.
Стек: Backend (Java 21, Spring Boot 3.4.1, PostgreSQL), Frontend (React 18, TypeScript, Vite 5), Android (Kotlin, Room, WorkManager, FCM).

**Репозиторий:** `C:\Users\style\Documents\VS_Agents\Focus`
**Полный аудит:** [[Аудит_Реальный_Статус]]

---

## Этап 1: Backend — критические исправления

### 1.1 Sharing — дать реальный доступ к shared ресурсам

**Проблема:** `GoalService` и `TaskService` фильтруют по `userId` владельца. Shared user получает 404.
**Файлы:**
- `backend/src/main/java/com/focus/service/GoalService.java`
- `backend/src/main/java/com/focus/service/TaskService.java`
- `backend/src/main/java/com/focus/repository/ShareRepository.java`

**Что сделать:**

1. В `GoalService.getById()` (и `TaskService.getById()`) — после проверки владельца, если не найдено, проверить есть ли ACCEPTED share для этого пользователя:
```java
// Сначала пробуем как владелец
Optional<Goal> opt = goalRepository.findByIdAndUserIdAndDeletedFalse(id, userId);
if (opt.isEmpty()) {
    // Проверяем shared access
    List<Share> shares = shareRepository.findBySharedWithEmailAndGoalIdAndStatus(email, goalId, ShareStatus.ACCEPTED);
    if (!shares.isEmpty()) {
        opt = goalRepository.findByIdAndDeletedFalse(id);
    }
}
```

2. Добавить в `ShareRepository`:
```java
List<Share> findBySharedWithEmailAndGoalIdAndStatus(String email, Long goalId, ShareStatus status);
List<Share> findBySharedWithEmailAndTaskIdAndStatus(String email, Long taskId, ShareStatus status);
```

3. Аналогично для `TaskService.getById()`, `TaskService.update()`, `GoalService.update()` — проверять `canEdit` флаг для write операций.

4. Для `getAllByGoal()` / `getAllByFolder()` — добавить список shared goal/task IDs из accepted shares и включить их в результат.

### 1.2 Recurrence — исправить вычисление next occurrence

**Проблема:** `createNextOccurrence` уже исправлен — использует `completedTask.getPlannedTime()` (строка 250). **НО** `daysOfWeek` поле не используется для WEEKLY.

**Файл:** `backend/src/main/java/com/focus/service/TaskService.java` строка 254

**Что сделать:** В ветке WEEKLY (строка 254-255) добавить логику учёта `daysOfWeek`:
```java
} else if (rule.getRuleType() == RuleType.WEEKLY) {
    if (rule.getDaysOfWeek() != null && !rule.getDaysOfWeek().isBlank()) {
        // Парсим daysOfWeek (MON,WED,FRI) и находим следующий подходящий день
        // Иначе fallback на intervalDays * 7
        nextTime = baseTime.plus(rule.getIntervalDays() * 7L, ChronoUnit.DAYS);
    } else {
        nextTime = baseTime.plus(rule.getIntervalDays() * 7L, ChronoUnit.DAYS);
    }
}
```

### 1.3 ReminderScheduler — добавить трекинг "уже отправлено"

**Проблема:** Нет поля `fired` в `ReminderRule` → напоминание повторяется каждую минуту в течение 60 секунд.

**Файлы:**
- `backend/src/main/java/com/focus/model/ReminderRule.java` — добавить `private boolean fired = false;`
- `backend/src/main/resources/db/migration/` — создать `V3__reminder_fired.sql`:
```sql
ALTER TABLE reminder_rules ADD COLUMN fired BOOLEAN NOT NULL DEFAULT FALSE;
CREATE INDEX idx_reminder_rules_fired ON reminder_rules(fired) WHERE fired = false;
```
- `backend/src/main/java/com/focus/service/ReminderScheduler.java` строка 45 — после отправки установить `rule.setFired(true)` и сохранить:
```java
notificationService.sendReminder(task.getUser(), task, rule);
rule.setFired(true);
reminderRuleRepository.save(rule);
```
- `ReminderRuleRepository.findAllActiveWithTaskAndUser()` — добавить условие `AND r.fired = false`

### 1.4 Reminders — поддержать несколько правил

**Проблема:** `setReminders` создаёт только 1 правило за вызов.

**Файл:** `backend/src/main/java/com/focus/service/TaskService.java` строки 227-238

**Что сделать:** Изменить endpoint и сервис для принятия списка правил:
1. Создать `ReminderRuleListRequest` DTO с полем `List<ReminderRuleRequest> rules`
2. В `TaskController.java` строка 97 — изменить параметр на `ReminderRuleListRequest`
3. В `TaskService.setReminders()` — удалить старые правила, создать все из списка

### 1.5 FCM NotificationService — реальная отправка (если Firebase проект доступен)

**Проблема:** `NotificationService.sendReminder()` — stub (только log).

**Файл:** `backend/src/main/java/com/focus/service/NotificationService.java`

**Что сделать:**
1. Добавить в `backend/pom.xml`:
```xml
<dependency>
    <groupId>com.google.firebase</groupId>
    <artifactId>firebase-admin</artifactId>
    <version>9.2.0</version>
</dependency>
```
2. Добавить конфигурацию Firebase Admin SDK в `application.yml`:
```yaml
app:
  firebase:
    config-path: ${FIREBASE_CONFIG_PATH:}
```
3. Реализовать `sendReminder()` через `FirebaseMessaging.getInstance().sendAsync()`
4. Добавить логирование доставки — создать таблицу `notification_log` и entity

**ВАЖНО:** Для этого нужен Firebase проект и `serviceAccountKey.json`. Если его нет — пропустить этот шаг, оставив улучшенный stub с логированием.

### 1.6 TaskRequest — добавить поле status

**Проблема:** Frontend отправляет `status` в create/update, но backend `TaskRequest` не имеет этого поля. Статус не сохраняется.

**Файл:** `backend/src/main/java/com/focus/dto/TaskRequest.java`

**Что сделать:** Добавить поле:
```java
private TaskStatus status;
// getter/setter
```

В `TaskService.create()` после строки 67:
```java
if (request.getStatus() != null) task.setStatus(request.getStatus());
```

В `TaskService.update()` после строки 81:
```java
if (request.getStatus() != null) task.setStatus(request.getStatus());
```

### 1.7 GoalService/TaskService list — добавить проверку ownership

**Проблема:** `getAllByGoal` и `getAllByFolder` не проверяют что цель/папка принадлежит пользователю.

**Файлы:**
- `backend/src/main/java/com/focus/service/GoalService.java`
- `backend/src/main/java/com/focus/service/TaskService.java`

**Что сделать:** Добавить проверку ownership в начале методов:
```java
// GoalService
public List<GoalResponse> getAllByFolder(Long folderId, User user) {
    folderRepository.findByIdAndUserIdAndDeletedFalse(folderId, user.getId())
        .orElseThrow(() -> new ResourceNotFoundException("Папка не найдена"));
    return goalRepository.findByFolderIdAndDeletedFalseOrderByCreatedAtDesc(folderId)...
}

// TaskService
public List<TaskResponse> getAllByGoal(Long goalId, User user) {
    goalRepository.findByIdAndUserIdAndDeletedFalse(goalId, user.getId())
        .orElseThrow(() -> new ResourceNotFoundException("Цель не найдена"));
    return taskRepository.findByGoalIdAndDeletedFalseOrderByCreatedAtDesc(goalId)...
}
```

---

## Этап 2: Frontend — исправления и новый UI

### 2.1 SettingsPage — исправить decay settings DTO

**Проблема:** Frontend отправляет `greenDecay: number`, backend ожидает объект.

**Файлы:**
- `frontend/src/types/index.ts` строки 141-157
- `frontend/src/pages/SettingsPage.tsx` строки 62-83
- `frontend/src/services/settingsService.ts`

**Что сделать:**

1. В `frontend/src/types/index.ts` — заменить:
```typescript
// Удалить:
export interface UserSettings { greenDecay: number; redDecay: number; }

// Добавить:
export interface PriorityDecayConfig {
  decayPerReschedule: number;
  decayPerDay: number;
  decayPerWeek: number;
  decayPerMonth: number;
}

export interface UserSettings {
  id: number;
  email: string;
  username: string;
  language: string;
  timezone: string;
  greenDecay: PriorityDecayConfig | null;
  redDecay: PriorityDecayConfig | null;
  createdAt: string;
}

export interface UpdateSettingsDto {
  language?: string;
  timezone?: string;
  greenDecay?: PriorityDecayConfig;
  redDecay?: PriorityDecayConfig;
}
```

2. В `SettingsPage.tsx` — изменить форму decay: вместо 2 полей (greenDecay, redDecay) сделать 2 группы по 4 поля (decayPerReschedule, decayPerDay, decayPerWeek, decayPerMonth) для каждого типа.

3. Обновить `handleSave()` для отправки правильной структуры DTO.

### 2.2 TasksPage — добавить кнопки Complete и Cancel

**Проблема:** Нет кнопок для завершения/отмены задачи. Backend endpoints существуют.

**Файлы:**
- `frontend/src/services/taskService.ts`
- `frontend/src/pages/TasksPage.tsx`

**Что сделать:**

1. Добавить в `taskService.ts`:
```typescript
async complete(id: number): Promise<Task> {
  const response = await api.post<Task>(`/tasks/${id}/complete`);
  return response.data;
},
async cancel(id: number): Promise<Task> {
  const response = await api.post<Task>(`/tasks/${id}/cancel`);
  return response.data;
},
```

2. В `TasksPage.tsx` — добавить кнопки "✓ ЗАВЕРШИТЬ" (green) и "✗ ОТМЕНИТЬ" (red) в `task-item__actions` для каждой задачи, visible только если статус TODO или IN_PROGRESS.

### 2.3 TasksPage — добавить UI для Links (связи между задачами)

**Проблема:** Нет UI для связей. Backend endpoint `POST /tasks/{id}/links` существует.

**Файлы:**
- `frontend/src/services/taskService.ts`
- `frontend/src/pages/TasksPage.tsx`

**Что сделать:**

1. Добавить в `taskService.ts`:
```typescript
async updateLinks(id: number, linkedTaskIds: number[]): Promise<Task> {
  const response = await api.post<Task>(`/tasks/${id}/links`, { linkedTaskIds });
  return response.data;
},
```

2. В `TasksPage.tsx` в edit modal — добавить секцию "Связанные задачи": multi-select или input для ID задач через запятую. Отображать linked task IDs в карточке задачи.

### 2.4 TasksPage — добавить UI для Recurrence

**Проблема:** Нет UI для настройки повторяющихся задач.

**Файлы:**
- `frontend/src/services/taskService.ts`
- `frontend/src/pages/TasksPage.tsx`

**Что сделать:**

1. Добавить в `taskService.ts`:
```typescript
async updateRecurrence(id: number, rule: RecurrenceRuleDto): Promise<any> {
  const response = await api.put(`/tasks/${id}/recurrence`, rule);
  return response.data;
},
```

2. Создать тип `RecurrenceRuleDto`:
```typescript
export interface RecurrenceRuleDto {
  ruleType: 'DAILY' | 'WEEKLY' | 'MONTHLY';
  intervalDays: number;
  daysOfWeek?: string;
}
```

3. В `TasksPage.tsx` в edit modal — добавить секцию "Повторение": dropdown (DAILY/WEEKLY/MONTHLY), number input для interval, опционально checkboxes для дней недели. Показывать бейдж "🔄 DAILY" на задаче с recurrence.

### 2.5 TasksPage — добавить UI для Reminders

**Проблема:** Нет UI для напоминаний.

**Файлы:**
- `frontend/src/services/taskService.ts`
- `frontend/src/pages/TasksPage.tsx`

**Что сделать:**

1. Добавить в `taskService.ts`:
```typescript
async updateReminders(id: number, reminders: ReminderRuleDto[]): Promise<any> {
  // Если backend поддерживает список — отправить массив
  // Иначе — вызывать по одному для каждого правила
  const response = await api.put(`/tasks/${id}/reminders`, reminders[0]);
  return response.data;
},
```

2. Создать тип `ReminderRuleDto`:
```typescript
export interface ReminderRuleDto {
  remindAtType: 'BEFORE_START' | 'AT_START' | 'BEFORE_DEADLINE';
  minutesBefore: number;
  isActive: boolean;
}
```

3. В `TasksPage.tsx` в edit modal — добавить секцию "Напоминания": dropdown типа, number input минут, toggle active. Показывать бейдж "🔔" на задачах с reminders.

### 2.5 CalendarPage — реализовать drag-and-drop (опционально)

**Проблема:** Подсказка о drag-and-drop показывается, но не реализована.

**Файл:** `frontend/src/pages/CalendarPage.tsx`

**Что сделать (опционально):**
- Установить `@dnd-kit/core` + `@dnd-kit/sortable`
- При drop на другой день — вызвать `taskService.update(id, { plannedTime: newDate })`
- Или убрать текст-подсказку `calendar.dragHint` из UI

---

## Этап 3: Android — исправления и новый UI

### 3.1 SettingsDTO — исправить структуру decay

**Проблема:** `UpdateSettingsRequest` не содержит decay config.

**Файл:** `android/app/src/main/java/com/focus/android/data/remote/dto/SettingsDtos.kt`

**Что сделать:** Заменить на:
```kotlin
data class PriorityDecayConfigDto(
    val decayPerReschedule: Int = 1,
    val decayPerDay: Int = 0,
    val decayPerWeek: Int = 0,
    val decayPerMonth: Int = 0
)

data class UpdateSettingsRequest(
    val language: String? = null,
    val timezone: String? = null,
    val greenDecay: PriorityDecayConfigDto? = null,
    val redDecay: PriorityDecayConfigDto? = null
)
```

Обновить `SettingsViewModel` для отправки decay config через `UpdateSettingsRequest`.

### 3.2 RegisterDeviceRequest — исправить field name

**Проблема:** `platform` вместо `deviceType`.

**Файл:** `android/app/src/main/java/com/focus/android/data/remote/dto/SettingsDtos.kt` строка 9

**Что сделать:**
```kotlin
data class RegisterDeviceRequest(
    val fcmToken: String,
    val deviceType: String = "ANDROID"
)
```

### 3.3 FcmService — реализовать onMessageReceived

**Проблема:** Пустое тело — нет уведомлений.

**Файл:** `android/app/src/main/java/com/focus/android/sync/FcmService.kt`

**Что сделать:**
```kotlin
override fun onMessageReceived(message: RemoteMessage) {
    super.onMessageReceived(message)

    val title = message.data["title"] ?: message.notification?.title ?: "Focus"
    val body = message.data["body"] ?: message.notification?.body ?: ""
    val taskId = message.data["taskId"]

    val intent = Intent(this, MainActivity::class.java).apply {
        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        putExtra("taskId", taskId)
    }

    val pendingIntent = PendingIntent.getActivity(
        this, 0, intent,
        PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_IMMUTABLE
    )

    val channel = NotificationChannel(
        "focus_reminders", "Напоминания",
        NotificationManager.IMPORTANCE_HIGH
    )
    val manager = getSystemService(NotificationManager::class.java)
    manager.createNotificationChannel(channel)

    val notification = NotificationCompat.Builder(this, "focus_reminders")
        .setSmallIcon(R.drawable.ic_launcher_foreground)
        .setContentTitle(title)
        .setContentText(body)
        .setAutoCancel(true)
        .setContentIntent(pendingIntent)
        .build()

    NotificationManagerCompat.from(this).notify(taskId?.hashCode() ?: 0, notification)
}
```

**Также в `AndroidManifest.xml`:**
- Убедиться что `POST_NOTIFICATIONS` permission есть (есть)
- Добавить runtime request для `POST_NOTIFICATIONS` в `MainActivity.onCreate()` (Android 13+)

### 3.4 SyncWorker — синхронизировать UPDATE и DELETE

**Проблема:** SyncWorker обрабатывает только CREATE (serverId == null).

**Файл:** `android/app/src/main/java/com/focus/android/sync/SyncWorker.kt`

**Что сделать:**

1. Добавить методы для синхронизации обновлений:
```kotlin
private suspend fun syncUpdatedFolders(app: FocusApplication) {
    val folders = app.database.folderDao().getUpdatedUnsynced() // synced=true, обновлённые локально
    folders.forEach { folder ->
        try {
            val serverId = folder.serverId ?: return@forEach
            val response = app.apiService.updateFolder(
                serverId,
                UpdateFolderRequest(folder.name)
            )
            if (response.isSuccessful) {
                app.database.folderDao().markSynced(folder.id)
            }
        } catch (_: Exception) { }
    }
}
```

2. Добавить методы для синхронизации удалений:
```kotlin
private suspend fun syncDeletedFolders(app: FocusApplication) {
    val folders = app.database.folderDao().getDeletedUnsynced() // deleted=true, synced=false
    folders.forEach { folder ->
        try {
            val serverId = folder.serverId ?: return@forEach
            val response = app.apiService.deleteFolder(serverId)
            if (response.isSuccessful) {
                app.database.folderDao().delete(folder) // физическое удаление из Room
            }
        } catch (_: Exception) { }
    }
}
```

3. Добавить в DAO:
```kotlin
// FolderDao
@Query("SELECT * FROM folders WHERE synced = 0 AND serverId IS NOT NULL AND deleted = 0")
 suspend fun getUpdatedUnsynced(): List<FolderEntity>

@Query("SELECT * FROM folders WHERE deleted = 1 AND synced = 0")
 suspend fun getDeletedUnsynced(): List<FolderEntity>

@Query("UPDATE folders SET synced = 1 WHERE id = :id")
 suspend fun markSynced(id: String)
```

4. Вызвать новые методы в `doWork()` после `syncUnsyncedTasks`.

### 3.5 Android — добавить UI для Tags

**Проблема:** Нет UI для управления тегами, хотя `ApiService.updateTaskTags()` существует.

**Файлы:**
- `android/app/src/main/java/com/focus/android/ui/tasks/TasksFragment.kt`
- `android/app/src/main/java/com/focus/android/ui/tasks/TasksViewModel.kt`

**Что сделать:**

1. В `showEditTaskDialog()` — добавить поле ввода тега и список текущих тегов с кнопкой удаления.
2. В `TasksViewModel` — добавить методы `addTag(task, tag)` и `removeTag(task, tag)`, вызывающие `apiService.updateTaskTags()`.
3. В `item_task.xml` — добавить `FlowLayout` или `ChipGroup` для отображения тегов.

### 3.6 Android — добавить Sharing экран (опционально)

**Проблема:** Нет UI для шаринга, хотя все API endpoints есть в `ApiService`.

**Файлы для создания:**
- `android/app/src/main/java/com/focus/android/ui/sharing/SharingFragment.kt`
- `android/app/src/main/java/com/focus/android/ui/sharing/SharingViewModel.kt`
- `android/app/src/main/res/layout/fragment_sharing.xml`
- `android/app/src/main/res/layout/item_share.xml`

**Что сделать:**
1. Создать SharingFragment с табами: "Мои шаринги" / "Доступно мне" / "Приглашения"
2. Форма шаринга: type select (GOAL/TASK), ID input, email input, canEdit checkbox
3. Списки с accept/decline кнопками для приглашений
4. Добавить в `nav_graph.xml` и `bottom_nav_menu.xml`

### 3.7 Android — добавить Week/Month view в Calendar (опционально)

**Проблема:** Только Day view.

**Файл:** `android/app/src/main/java/com/focus/android/ui/calendar/CalendarFragment.kt`

**Что сделать (опционально):**
- Добавить toggle кнопки: Day / Week / Month
- Week: 7-колоночный grid
- Month: CalendarView с маркерами на днях с задачами
- Или оставить Day view как есть (MVP)

---

## Этап 4: Инфраструктура и качество

### 4.1 PWA — добавить иконки

**Файл:** `frontend/public/manifest.json`

**Что сделать:** Создать иконки 192x192 и 512x512 в PNG, добавить в массив `icons`:
```json
"icons": [
  { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
  { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
]
```

### 4.2 Optimistic Locking — обработка 409 на Frontend

**Файл:** `frontend/src/services/api.ts`

**Что сделать:** В response interceptor добавить обработку 409:
```typescript
if (error.response?.status === 409) {
  // Показать toast: "Данные были изменены другим клиентом. Обновите страницу."
  // Опционально: auto-retry после re-fetch
}
```

### 4.3 FolderEntity ID type — String → Long (опционально)

**Проблема:** Android использует `String` для ID, backend `Long`. Gson конвертирует, но хрупко.

**Файлы:**
- `android/app/src/main/java/com/focus/android/data/model/FolderEntity.kt`
- `android/app/src/main/java/com/focus/android/data/model/GoalEntity.kt`
- `android/app/src/main/java/com/focus/android/data/model/TaskEntity.kt`
- Все DTO и DAO

**Что сделать (опционально, breaking change):** Заменить `serverId: String?` на `serverId: Long?` во всех entities и DTO. Обновить DAO queries. Это требует миграцию Room (v2→v3).

**Приоритет низкий** — текущая конвертация через Gson работает.

---

## Порядок выполнения

Приоритет от высокого к низкому:

### Фаза 1 — Must Have (базовый функционал работает)
1. **1.6** — TaskRequest.status (backend) — 15 мин
2. **2.1** — SettingsPage decay DTO fix (frontend) — 30 мин
3. **2.2** — Complete/Cancel кнопки (frontend) — 30 мин
4. **1.7** — Ownership check в list endpoints (backend) — 20 мин
5. **3.1** — SettingsDTO decay fix (Android) — 15 мин
6. **3.2** — RegisterDeviceRequest field name fix (Android) — 5 мин

### Фаза 2 — Should Have (ключевые фичи)
7. **1.1** — Sharing access enforcement (backend) — 2 часа
8. **1.3** — Reminder fired tracking (backend) — 45 мин
9. **1.4** — Multiple reminders support (backend) — 30 мин
10. **2.3** — Links UI (frontend) — 1 час
11. **2.4** — Recurrence UI (frontend) — 1.5 часа
12. **2.5** — Reminders UI (frontend) — 1.5 часа
13. **3.3** — FcmService onMessageReceived (Android) — 1 час
14. **3.5** — Tags UI (Android) — 1 час

### Фаза 3 — Nice to Have
15. **1.2** — Recurrence daysOfWeek logic (backend) — 1 час
16. **1.5** — FCM real implementation (backend) — 2 часа (требует Firebase проект)
17. **3.4** — SyncWorker UPDATE/DELETE (Android) — 2 часа
18. **3.6** — Sharing screen (Android) — 3 часа
19. **3.7** — Calendar week/month (Android) — 2 часа
20. **4.1** — PWA icons — 15 мин
21. **4.2** — 409 handling (frontend) — 30 мин

---

## Существующие ключевые файлы (для навигации)

### Backend
```
backend/src/main/java/com/focus/
├── controller/
│   ├── AuthController.java          (4 endpoints: register/login/refresh/logout)
│   ├── UserController.java          (GET /me, PATCH /me/settings)
│   ├── FolderController.java        (5 endpoints)
│   ├── GoalController.java          (5 endpoints + share)
│   ├── TaskController.java          (13 endpoints: CRUD + complete/cancel/reschedule/tags/links/recurrence/reminders/share)
│   ├── ShareController.java         (GET /shares, /accepted, /invitations, POST accept/decline)
│   ├── CalendarController.java      (GET /calendar)
│   ├── DeviceController.java        (POST/DELETE devices)
│   └── HealthController.java        (GET /health)
├── service/
│   ├── AuthService.java
│   ├── FolderService.java
│   ├── GoalService.java
│   ├── TaskService.java             (262 строки — основной сервис задач)
│   ├── ShareService.java            (102 строки — шаринг)
│   ├── CalendarService.java
│   ├── DeviceService.java
│   ├── NotificationService.java     (38 строк — STUB!)
│   ├── PriorityPolicyService.java
│   └── ReminderScheduler.java       (81 строка — scheduled каждые 60 сек)
├── dto/
│   ├── TaskRequest.java             (42 строки — НЕТ поля status!)
│   ├── SettingsRequest.java         (54 строки — PriorityDecayConfigDto внутри)
│   └── ReminderRuleRequest.java     (25 строк — single rule, не list)
├── model/
│   ├── Task.java                    (taskType, priority, status, plannedTime, deadline, @Version)
│   ├── ReminderRule.java            (remindAtType, minutesBefore, isActive — НЕТ fired!)
│   ├── Share.java                   (owner, sharedWithEmail, goal/task, canEdit, status)
│   └── RecurrenceRule.java          (ruleType, intervalDays, daysOfWeek)
├── repository/
│   └── ShareRepository.java         (НЕТ findBySharedWithEmailAndGoalId/TaskId)
├── security/
│   ├── SecurityConfig.java
│   ├── JwtTokenProvider.java
│   └── JwtAuthenticationFilter.java
└── exception/
    └── GlobalExceptionHandler.java  (400/404/405/409/500)
```

### Frontend
```
frontend/src/
├── types/index.ts                   (187 строк — UserSettings.greenDecay: number — WRONG!)
├── pages/
│   ├── TasksPage.tsx                (428 строк — НЕТ complete/cancel/links/recurrence/reminders)
│   ├── SettingsPage.tsx             (188 строк — decay отправляет number вместо объекта)
│   ├── CalendarPage.tsx             (drag-and-drop не реализован)
│   └── ... (Auth/Folders/Goals/Sharing — OK)
├── services/
│   ├── taskService.ts               (40 строк — НЕТ complete/cancel/links/recurrence/reminders)
│   ├── settingsService.ts           (16 строк — OK, DTO mismatch в types)
│   └── ... (auth/folder/goal/calendar/sharing — OK)
├── i18n/
│   ├── ru.json                      (197 строк)
│   └── en.json                      (197 строк)
└── styles/
    └── retro.css                    (1216 строк)
```

### Android
```
android/app/src/main/java/com/focus/android/
├── data/remote/dto/
│   ├── SettingsDtos.kt              (11 строк — НЕТ decay, platform→deviceType)
│   └── TaskDtos.kt
├── sync/
│   ├── FcmService.kt                (16 строк — onMessageReceived ПУСТОЙ!)
│   ├── SyncWorker.kt                (111 строк — только CREATE sync)
│   └── FcmTokenWorker.kt
├── ui/tasks/
│   ├── TasksFragment.kt             (224 строки — НЕТ tags/links/recurrence/reminders UI)
│   └── TasksViewModel.kt
└── ... (login/folders/goals/calendar/settings — OK)
```

---

## Как проверять

После каждого этапа:
1. **Backend:** `mvn compile` + `mvn test` — должны быть зелёными
2. **Frontend:** `npm run build` — должен быть зелёным
3. **Android:** `./gradlew assembleDebug` — должен быть зелёным
4. **Backend запущен:** curl тесты ключевых endpoints
5. **Frontend в браузере:** проверка UI новых элементов
6. **Android эмулятор:** ручная проверка на `emulator-5554`

## Ссылки

- [[Аудит_Реальный_Статус]] — полный аудит с деталями
- [[Focus]] — главная заметка проекта
- [[Источник_Промпт]] — бизнес-требования
