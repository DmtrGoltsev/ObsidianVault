---
id: "term-fcm"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/03-domain-specification.md", "docs/04-architecture-blueprint.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md"]
теги: ["android", "push", "интеграция"]
---

# FCM (Firebase Cloud Messaging)

## Определение

Сервис Firebase для доставки push-уведомлений на Android-устройства. Единственный канал push-уведомлений в RocketFlow.

## Контекст в проекте

- Бэкенд вычисляет доставки и отправляет push через FCM
- Отправка реализована в `FirebaseAdminFcmSender.java` (`backend/src/main/java/com/rocketflow/notifications/FirebaseAdminFcmSender.java`)
- Android принимает push через `RocketFlowMessagingService.kt` (`android/app/src/main/java/com/rocketflow/companion/notifications/RocketFlowMessagingService.kt`)
- Интеграция доказана локально: E2E proof `reminder → push → tap → task open`

## Бизнес-правила

- Каждое устройство регистрирует FCM-токен через [[Device_Registration]]
- Токен обновляется при переустановке приложения
- Бэкенд должен обрабатывать ошибки доставки FCM (предположение)

## Связанные термины

- [[Device_Registration]] — регистрация токена
- [[Notification_Delivery]] — запись о доставке
- [[Reminder_Rule]] — источник уведомления
