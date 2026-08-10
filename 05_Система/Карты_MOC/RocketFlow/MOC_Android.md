---
id: "moc-android"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md", "docs/50-notification-runtime-clean-pass.md", "docs/67-weekly-focus-production-rollout-evidence.md"]
доказательства: ["Док_Android_Build", "Док_Android_Verification", "Док_Production_Rollout_20260810", "Док_Нотификации_E2E"]
теги: ["moc", "android", "rocketflow"]
---

# MOC Android

Карта Android-клиента RocketFlow. Kotlin 1.9.24, minSdk 26, targetSdk 34.

## Активности

Основные экраны приложения:
- **LoginActivity** — вход
- **RegisterActivity** — регистрация
- **MainActivity** — главный экран (папки)
- **BrowseActivity** — просмотр целей и задач
- **DetailActivity** — детали задачи/цели
- **PlanningActivity** — планирование
- **SettingsActivity** — настройки
- **NotificationsActivity** — уведомления

## Сервисы

- **FCMService** — приём push-уведомлений через [[FCM]]
- **ReminderWorker** — WorkManager для фоновых напоминаний
- **SessionManager** — управление [[JWT]] сессией

## Модули

### auth
Аутентификация, хранение токенов, автообновление сессии.

### planning
Полный цикл офлайн-планирования с синхронизацией. [[TaskPlan|План задач]] с приоритетной сортировкой, drag-drop. [[PlanningSync|Офлайн-синхронизация]] через PlanningSyncWorker, ConflictResolver.

### browse
Навигация по дереву: папки → цели → задачи.

### detail
Детальный просмотр задачи/цели, редактирование.

### notifications
[[Notification_Delivery|Доставка уведомлений]]. [[Device_Registration|Регистрация устройства]]. Интеграция с [[FCM]]. Расширен: TaskReminderAlarmActivity, AlarmReceiver, AlarmScheduler — fullscreen alarm при просроченных напоминаниях.

### sharing
[[Share_Invitation|Совместный доступ]], управление [[Collaborator|соавторами]]. Модели: ShareTarget, ShareInvitation, fullAccess.

## FCM

[[FCM]] — Firebase Cloud Messaging. Приём push-уведомлений бэкенда. Обработка reminder push → открытие задачи.

## Smoke-процедуры

Локальная проверка нотификаций:
1. Создать задачу с напоминанием
2. Дождаться push
3. Тап по уведомлению → открытие задачи

См. [[Док_Нотификации_E2E]], [[Источник_Нотификация_Смок]], [[Источник_Нотификация_Пруф]].

## Сборка

Gradle. Android CI lane больше не build-only: unit/build/lint. Для source SHA `910c061de4af9395d9bb682624bd966b2977a738` актуальный `RocketFlow-0.1.0-prod-debugcert.apk` является installable direct-sideload build: v2/v3/zipalign valid, `debuggable=false`, production API, install/runtime checks PASS, `77` tests и lint `0` errors. Это не Play Store production identity; updates требуют тот же debug certificate, Firebase/FCM config отсутствует. Прежний unsigned SHA-256 `1763de390dd587c686fe84152c521a2d92e65b747fb2689ec2076c0560c576d7` сохранён как superseded damaged/non-installable evidence.

См. [[Док_Android_Build]], [[Док_Android_Verification]], [[Док_Production_Rollout_20260810]], [[Задача_CI_Runtime_Lanes]].

## Эмулятор

Тестирование на Android Emulator. Локально исправлено: SDK `C:\Users\style\AppData\Local\Android\Sdk`, `android/local.properties` ignored by git, emulator `emulator-5554` видим. См. [[Источник_Android_Local_Setup]].

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — бэкенд API
- [[MOC_DevOps]] — CI/CD
- [[Источник_Android_Local_Setup]]
