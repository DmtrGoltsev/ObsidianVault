---
id: "moc-android"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md", "docs/68-scroll-and-priority-retirement-delivery.md", "docs/50-notification-runtime-clean-pass.md", "docs/67-weekly-focus-production-rollout-evidence.md"]
доказательства: ["Док_Prod_Deploy_State", "Док_V21_Scroll_Priority_20260822", "Док_Android_Build", "Док_Android_Verification", "Док_Production_Rollout_20260810", "Док_Нотификации_E2E"]
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
Полный цикл офлайн-планирования с синхронизацией. [[TaskPlan|План задач]] сортируется детерминированно без task priority. Home/Planner восстанавливает stable visible anchor и pixel offset при перестроении списка и возврате из деталей. [[PlanningSync|Офлайн-синхронизация]] выполняется через `PlanningSyncWorker`.

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

V21 source 2026-08-22: `90/90` unit PASS, `assembleDebug` PASS, lint `0` errors / `34` existing warnings, debug Android-test APK PASS. Visual scroll и portrait/landscape IME checks PASS; SQLite short-lived store lifecycle исправлен. Backend/web V21 rollout PASS; см. [[Док_V21_Scroll_Priority_20260822]].

Current personal APK: `0.1.1`, `versionCode 2`, signed, SHA-256 `3DF9EB210D801D932A4C736A0EF682C8C0AADCB36536B81CA19267F326C52AF7`. `adb install -r` сохранил UID и `firstInstallTime`; cold launch PASS, crash/ANR `0/0`, current screen Login. Это direct-sideload artifact, не Play Store production identity. Исторические APK сохранены в [[Док_Android_Verification]].

См. [[Док_Android_Build]], [[Док_Android_Verification]], [[Док_Production_Rollout_20260810]], [[Задача_CI_Runtime_Lanes]].

## Эмулятор

Тестирование на Android Emulator. Локально исправлено: SDK `C:\Users\style\AppData\Local\Android\Sdk`, `android/local.properties` ignored by git, emulator `emulator-5554` видим. См. [[Источник_Android_Local_Setup]].

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — бэкенд API
- [[MOC_DevOps]] — CI/CD
- [[Источник_Android_Local_Setup]]
