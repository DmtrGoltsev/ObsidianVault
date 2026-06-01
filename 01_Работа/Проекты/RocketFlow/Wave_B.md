---
id: "wave-b"
тип: "проект"
статус: "выполнено"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/27-wave-b-backend-calendar-priority.md", "docs/28-wave-b-backend-notifications.md", "docs/29-wave-b-web-planning-flows.md", "docs/30-wave-b-qa-scheduling-validation.md", "docs/31-wave-b-devops-staging-secrets.md"]
доказательства: []
теги: ["волна", "завершено", "расширение"]
---

# Wave B: Calendar, Notifications & Web Planning

## Статус: выполнено

## Цель волны

Реализовать calendar, приоритеты, нотификации, web planning flows, QA валидацию.

## Состав волны

| Задача | Документ | Результат |
|--------|----------|-----------|
| Backend Calendar + Priority | `docs/27-wave-b-backend-calendar-priority.md` | Calendar API, Priority Decay |
| Backend Notifications | `docs/28-wave-b-backend-notifications.md` | [[FCM]] интеграция, планировщик уведомлений |
| Web Planning Flows | `docs/29-wave-b-web-planning-flows.md` | UI планирования, CRUD задач в web |
| QA Scheduling Validation | `docs/30-wave-b-qa-scheduling-validation.md` | Тесты планирования |
| DevOps Staging Secrets | `docs/31-wave-b-devops-staging-secrets.md` | Secrets для staging |

## Ключевые результаты

- [[Notification_Delivery]] — сущность доставки реализована
- [[Priority_Decay]] — автоснижение приоритета работает
- Web planning UI функционирует

## Связанные заметки

- [[Wave_A]] — предыдущая волна
- [[Wave_C]] — следующая волна
- [[RocketFlow]] — проект
