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

## Баг найденный и исправленный

| ID | Описание | Статус | Дата |
|---|---|---|---|
| BUG-001 | `TaskService.getById()` вызывает `resolveTaskWithEditAccess` — shared-пользователь с `canEdit=false` получает Forbidden вместо чтения задачи | FIXED | 2026-06-12 |

## Незакоммиченные изменения прошлого агента

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
