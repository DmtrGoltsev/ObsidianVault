---
id: "term-flyway"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md"]
доказательства: []
теги: ["база-данных", "миграции"]
---

# Flyway

## Определение

Инструмент версионирования и миграции базы данных, используемый в RocketFlow. Управляет схемой PostgreSQL через последовательные SQL-миграции.

## Контекст в проекте

- Миграции находятся в `backend/src/main/resources/db/migration/`
- Выполняются при старте приложения (Spring Boot + Flyway автоконфигурация)
- Гарантирует, что схема БД всегда соответствует версии кода
- Используется как альтернатива Liquibase (выбран Flyway согласно `docs/04-architecture-blueprint.md`)

## Таблицы в миграциях

`users`, `user_credentials`, `user_settings`, `folders`, `goals`, `tasks`, `tags`, `task_tags`, `task_links`, `goal_shares`, `recurrence_rules`, `reminder_rules`, `reschedule_events`, `device_registrations`, `notification_deliveries`, `share_invitations` (предположение на основе доменных сущностей)

## Связанные термины

- [[PostgreSQL_Advisory_Lock]] — механизм блокировок в БД
- [[Soft_Delete]] — паттерн удаления (флаг archived)
- [[Modular_Monolith]] — приложение, использующее Flyway
