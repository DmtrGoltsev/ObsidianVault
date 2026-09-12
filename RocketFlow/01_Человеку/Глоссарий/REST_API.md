---
id: "term-rest-api"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/04-architecture-blueprint.md", "docs/05-api-contracts.md"]
доказательства: []
теги: ["архитектура", "api"]
---

# REST API

## Определение

Архитектурный стиль взаимодействия между клиентами (web, Android) и бэкендом RocketFlow. Все endpoints — REST over HTTP/JSON.

## Контекст в проекте

- Бэкенд предоставляет REST API для web (React SPA) и Android (нативный клиент)
- Контракты описаны в `docs/05-api-contracts.md`
- Аутентификация через [[JWT]] токены, передаваемые в заголовках
- Контроллеры: `AuthController.java`, `TaskController.java`, `SharingController.java` и др. в `backend/src/main/java/com/rocketflow/`

## Примеры endpoints (из структуры backend)

- `backend/src/main/java/com/rocketflow/auth/AuthController.java` — регистрация, вход
- `backend/src/main/java/com/rocketflow/tasks/TaskController.java` — CRUD задач
- `backend/src/main/java/com/rocketflow/sharing/SharingController.java` — совместный доступ

## Связанные термины

- [[JWT]] — механизм аутентификации
- [[Modular_Monolith]] — бэкенд, предоставляющий REST API
- [[Docker_Image]] — упаковка API в контейнер
