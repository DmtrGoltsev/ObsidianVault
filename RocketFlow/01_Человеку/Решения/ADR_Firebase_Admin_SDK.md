---
id: "adr-firebase-admin-sdk"
тип: "решение"
статус: "утверждено"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md", "docs/50-notification-runtime-clean-pass.md"]
доказательства: ["Док_Нотификации_E2E"]
теги: ["adr", "нотификации", "android", "backend"]
---

# ADR: Firebase Admin SDK для push-уведомлений

## Контекст

Бэкенд должен отправлять push-уведомления на Android-устройства при срабатывании напоминаний. Требовался надёжный канал доставки.

## Решение

Использовать [[FCM]] через Firebase Admin SDK (Java) на бэкенде.

## Обоснование

- FCM — стандарт для Android push-уведомлений, бесплатный
- Firebase Admin SDK — официальная Java-библиотека от Google
- `FirebaseAdminFcmSender.java` — основная реализация отправки
- `LoggingFcmSender` — fallback для локальной разработки без FCM-ключей (логирует вместо отправки)
- Интеграция проверена локально: напоминание → push → tap → открытие задачи (см. [[Док_Нотификации_E2E]])

## Последствия

- Требуется Firebase service account key (хранится в secrets, не в коде)
- Зависимость от Google-инфраструктуры
- Fallback-реализация обязательна для локальной разработки

## Альтернативы

- **Собственный WebSocket-канал** — отвергнут: требует постоянного соединения, разряд батареи на Android
- **SMS** — отвергнут: платно, неинтерактивно

## Связанные заметки

- [[FCM]] (глоссарий)
- [[Notification_Delivery]] (глоссарий)
- [[Device_Registration]] (глоссарий)
- [[MOC_Бэкенд]]
- [[MOC_Android]]
- [[ADR_Logical_Device_Upsert]]
