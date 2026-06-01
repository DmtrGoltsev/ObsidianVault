---
id: "agent-android"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/04-architecture-blueprint.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md"]
теги: ["агент", "android", "kotlin", "mobile"]
---

# Агент Android

## Зона ответственности

- Kotlin 1.9.24, Android SDK (minSdk 26, targetSdk 34)
- Архитектура: `auth/`, `browse/`, `detail/`, `network/`, `notifications/`, `planning/`, `settings/`, `sharing/`
- [[FCM]] push-уведомления через `RocketFlowMessagingService.kt`
- WorkManager 2.9.1 для фоновой синхронизации
- [[Device_Registration]] — регистрация устройства в бэкенде

## Ключевые файлы

- `android/app/src/main/java/com/rocketflow/companion/MainActivity.kt` — главная Activity
- `android/app/src/main/java/com/rocketflow/companion/notifications/RocketFlowMessagingService.kt` — приём FCM push

## Права на решения

- Архитектура Android-приложения
- Выбор Android-библиотек
- Стратегия синхронизации с бэкендом

## Активные задачи

- MVP3 полировка Android UI
- Подтверждение push-tap flow на staging
- Android plan item delete (коммит `381b4e8`)

## Выполненные волны

- Wave C: Android foundation, notification entry

## Доказательства

- E2E notification proof: `reminder → push → tap → task open` — пройден локально (источник: [[Источник_Нотификация_Пруф]])

## Связанные заметки

- [[FCM]] — канал push
- [[Device_Registration]] — регистрация устройства
- [[RocketFlow]] — проект
