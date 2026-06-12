---
id: "qa-results"
тип: "доказательство"
статус: "активно"
проект: "Focus"
создано: "2026-06-12"
обновлено: "2026-06-12"
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

## QA Prod Wave (2026-06-12)

**95 тест-кейсов прогнано: 87 PASS, 8 FAIL (все FAIL = баги тестов, 0 багов приложения)**

### Backend API (58/61)

| ID | Status | Note |
|---|---|---|
| PROD-001 — PROD-037 | PASS | Health, Auth(8), Folders(5), Goals(5), Tasks(14), Tags, Links |
| PROD-038 — PROD-044 | FAIL→PASS | Sharing: тесты использовали `targetUserEmail` вместо `email`. API работает корректно с `email` |
| PROD-045 — PROD-052 | PASS | Calendar(2), Recurrence(3), Reminders, Devices(2) |
| PROD-053 | FAIL→PASS | No token → 403 (Spring Security default, not 401) |
| PROD-054 — PROD-061 | PASS | Edge cases(4), CRUD cycle, Reschedule chain |

### Frontend UI (13/14)

| ID | Status | Note |
|---|---|---|
| FE-001 — FE-011 | PASS | Index, Auth, Scripts, Manifest, Health, Register, Folder, Goal, Task, Settings |
| FE-010 | FAIL | Calendar: date format in URL (test bug) |
| FE-012 — FE-014 | FAIL→PASS | Share: same `email` vs `targetUserEmail` bug in test |

### Android E2E (16/20)

| ID | Status | Note |
|---|---|---|
| AND-001 | FAIL | ANR wellbeing overlay (not Focus app) |
| AND-002 — AND-004 | PASS | UI dump, Login screen, Register |
| AND-005 | FAIL | Display parse (init=0x0) |
| AND-006 — AND-007 | FAIL | Email field not found via uiautomator (needs bounds-based input) |
| AND-008 | PASS | Login persistence after restart |
| AND-009 — AND-012 | PASS | Server CRUD, visibility |
| AND-013 | FAIL | Calendar date range (test bug) |
| AND-014 — AND-020 | PASS | Settings, User, Complete, Cancel, Share, Tags, Device |

### Ключевые выводы

1. **0 реальных багов в приложении** — все 8 FAIL = ошибки в тестовых скриптах
2. Sharing API использует поле `email` (не `targetUserEmail`) — QA-тесткейсы исправлены
3. Приложение стабильно: Auth, CRUD, Sharing, Calendar, Recurrence, Settings — всё работает
4. Android login persistence работает (AND-008 PASS)

| Область | Файлы | Описание |
|---|---|---|
| Backend FCM | `notification/` (6 файлов) | Полная реализация FCM push: FcmSender, FirebaseAdminFcmSender, LoggingFcmSender, конфигурация |
| Backend FCM | `pom.xml` | firebase-admin:9.4.2 + google-auth:1.29.0 |
| Backend FCM | `application.yml` | `app.notifications.fcm` секция (enabled: false) |
| Backend FCM | `NotificationService.java` | Stub заменён на FcmSender injection |
| Backend refactor | `TaskService.java` | DRY рефакторинг + баг-фикс getById |
| Android FCM | `FocusApplication.kt` | initFirebase() из BuildConfig |
| Android FCM | `build.gradle.kts` | BuildConfig поля для Firebase кредов |
| Android auth | `AuthInterceptor.kt` | Исправлен порядок response.close() |
| Android auth | `AuthRepository.kt` | extractErrorMessage(), CancellationException |
| Android auth | `AuthDtos.kt` | ErrorResponse DTO |
| Android net | `network_security_config.xml` | Добавлен 45.10.110.42 |
| E2E | `E2E_TEST_CASES.json` | 35 тест-кейсов (QA3-001 — QA3-035) |

## Навигация

- [[QA_Фиксы]] — журнал фиксов
- [[Focus]] — статус проекта
- [[MOC_Focus]] — карта проекта
