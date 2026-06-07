---
id: "moc-backend"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md", "docs/03-domain-specification.md"]
доказательства: ["Док_Backend_Verification", "Док_Prod_Deploy_State"]
теги: ["moc", "backend", "rocketflow"]
---

# MOC Бэкенд

Карта бэкенд-компонентов RocketFlow. Java 21, Spring Boot 3.4.5, Spring Security, Spring Data JPA, PostgreSQL 16, Flyway, Docker.

## Модули

Бэкенд построен как [[Modular_Monolith]]:

- **auth** — аутентификация и авторизация, [[JWT]] access + refresh токены
- **accounts** — управление учётными записями пользователей
- **settings** — настройки пользователя
- **folders** — управление [[Folder|папками]], [[Soft_Delete|мягкое удаление]]
- **goals** — управление [[Goal|целями]], [[Soft_Delete|мягкое удаление]]
- **tasks** — управление [[Task|задачами]], [[Green_Task]], [[Red_Task]], [[Soft_Delete|мягкое удаление]]
- **sharing** — [[Share_Invitation|совместный доступ]], [[Collaborator|соавторы]]
- **calendar** — календарное планирование, [[Planned_Time]], [[Due_Time]]
- **recurrence** — [[Recurrence_Rule|повторяющиеся задачи]]
- **reminders** — [[Reminder_Rule|напоминания]], интеграция с [[FCM]]
- **prioritypolicy** — политика [[Priority_Decay|снижения приоритета]]
- **notifications** — [[Notification_Delivery|доставка уведомлений]], [[Device_Registration|регистрация устройств]]
- **ideas** — [[Idea|идеи]] внутри папки с историей правок
- **links** — обобщённые [[EntityLink|связи]] между сущностями (goal/task/idea/note)
- **notes** — [[FolderNote|заметки]] в папке (замена folder_notes)
- **health** — health-check endpoint
- **common** — ApiError, ApiException, унифицированная обработка ошибок
- **config** — конфигурация безопасности, CORS, аутентификации

## API эндпоинты

[[REST_API]] — см. [[Источник_API_Контракты]]

## База данных

- [[PostgreSQL_Advisory_Lock]] — advisory lock для планировщика напоминаний
- [[Optimistic_Locking]] — конкурентные обновления
- [[Soft_Delete]] — мягкое удаление

## Миграции

[[Flyway]] — 18 миграций (V1–V18). См. [[ADR_Flyway_Миграции]].

## Тестирование

- JUnit 5 + Embedded PostgreSQL (zonky)
- CI: `mvn test` в backend-verify.yml
- [[Док_Backend_Тесты]]
- [[Док_Backend_Verification]] — audit/current verifier status

## Docker

[[Docker_Image]] — Docker/GHCR open gate, не текущий production deploy fact. См. [[Задача_GHCR_Publish]], [[Док_Prod_Deploy_State]].

## CI/CD

[[Регламент_CI_CD]] — backend-verify.yml, production deploy pipeline `backend-hexcore-prod-deploy.yml`.

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_DevOps]] — DevOps и развёртывание

## Связанные решения

- [[ADR_Модульный_Монолит]]
- [[ADR_PostgreSQL]]
- [[ADR_JWT_Токены]]
- [[ADR_Flyway_Миграции]]
- [[ADR_Мягкое_Удаление]]
- [[ADR_Оптимистичная_Блокировка]]
- [[ADR_Firebase_Admin_SDK]]
- [[ADR_Scheduler_Advisory_Lock]]
- [[ADR_Logical_Device_Upsert]]
