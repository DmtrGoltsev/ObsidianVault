---
id: "moc-android"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "средняя"
источники: ["docs/04-architecture-blueprint.md", "docs/50-notification-runtime-clean-pass.md"]
доказательства: ["Док_Android_Build", "Док_Нотификации_E2E"]
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
Управление [[Folder|папками]], [[Goal|целями]], [[Task|задачами]]. [[Green_Task]], [[Red_Task]], [[Priority_Decay]].

### browse
Навигация по дереву: папки → цели → задачи.

### detail
Детальный просмотр задачи/цели, редактирование.

### notifications
[[Notification_Delivery|Доставка уведомлений]]. [[Device_Registration|Регистрация устройства]]. Интеграция с [[FCM]].

### sharing
[[Share_Invitation|Совместный доступ]], управление [[Collaborator|соавторами]].

## FCM

[[FCM]] — Firebase Cloud Messaging. Приём push-уведомлений бэкенда. Обработка reminder push → открытие задачи.

## Smoke-процедуры

Локальная проверка нотификаций:
1. Создать задачу с напоминанием
2. Дождаться push
3. Тап по уведомлению → открытие задачи

См. [[Док_Нотификации_E2E]], [[Источник_Нотификация_Смок]], [[Источник_Нотификация_Пруф]].

## Сборка

Gradle. `assembleDebug` — отладочная сборка. CI: android-verify.yml.

См. [[Док_Android_Build]], [[Задача_CI_Runtime_Lanes]].

## Эмулятор

Тестирование на Android Emulator (API 34).

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — бэкенд API
- [[MOC_DevOps]] — CI/CD
