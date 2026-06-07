---
id: "pkg-android"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "средняя"
источники: ["docs/04-architecture-blueprint.md", "docs/50-notification-runtime-clean-pass.md", "docs/47-device-registration-logical-device-upsert-repair.md"]
доказательства: ["Док_Android_Build", "Док_Android_Verification", "Док_Нотификации_E2E"]
теги: ["пакет_контекста", "android"]
---

# Пакет контекста: Android

Выжимка знаний для [[Агент_Android|Android-агента]]. Структура модулей, FCM, smoke-процедуры, эмулятор.

## Архитектурная карта
- [[MOC_Android]] — полная карта Android-клиента

## Модули и экраны
- **auth** — логин, регистрация, управление [[JWT]] сессией
- **planning** — папки, цели, задачи, календарь
- **browse** — навигация по дереву: папки → цели → задачи
- **detail** — детальный просмотр и редактирование
- **notifications** — приём push, регистрация устройства
- **sharing** — совместный доступ, соавторы

## FCM и нотификации
- [[FCM]] — Firebase Cloud Messaging
- [[Device_Registration|Регистрация устройства]] через installationId upsert
- `FirebaseAdminFcmSender.java` на бэкенде → Android-клиент получает push
- WorkManager для фоновых напоминаний

## Smoke-процедура нотификаций
1. Создать задачу с [[Reminder_Rule|напоминанием]]
2. Дождаться push-уведомления
3. Тап по уведомлению → открытие задачи
4. Проверка: задача открыта, напоминание сработало

См. [[Док_Нотификации_E2E]], [[Источник_Нотификация_Смок]], [[Источник_Нотификация_Пруф]].

## Сборка и тестирование
- Kotlin 1.9.24, minSdk 26, targetSdk 34
- Android CI lane: unit/build/lint
- Robolectric 4.12.2 — модульные тесты
- CI: android-verify.yml → [[Док_Android_Build]]
- Финальный full Android result после cleanup зелёный: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon`, exit code `0` → [[Док_Android_Verification]]

## Эмулятор
- Android SDK: `C:\Users\style\AppData\Local\Android\Sdk`
- `android/local.properties` ignored by git
- emulator `emulator-5554` видим
- См. [[Источник_Android_Local_Setup]]

## Ключевые решения
- [[ADR_Firebase_Admin_SDK]]
- [[ADR_Logical_Device_Upsert]]
- [[ADR_JWT_Токены]]

## Ключевые источники
- [[Источник_Нотификация_Смок]]
- [[Источник_Нотификация_Пруф]]
- [[Источник_Архитектура]]
- [[Источник_Текущее_Состояние]]
- [[Источник_Android_Local_Setup]]
