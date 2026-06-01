---
id: "term-docker-image"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/58-github-cicd-policy.md"]
доказательства: []
теги: ["devops", "развертывание"]
---

# Docker Image (Docker образ)

## Определение

Контейнеризированная упаковка бэкенда RocketFlow для развёртывания на [[HexCore]] и в CI/CD.

## Контекст в проекте

- Бэкенд собирается в Docker образ: `rocketflow-backend:latest`
- Сборка определена в `backend/Dockerfile`
- Локальная сборка и smoke-тест доказаны: контейнер стартует с `/actuator/health = UP` против `postgres:16`
- Целевой registry: GHCR (GitHub Container Registry)
- Имя образа: `ghcr.io/<owner>/rocketflow-backend`
- CI workflow для публикации: `backend-image-publish` (manual trigger)

## Связанные термины

- [[HexCore]] — production-сервер для запуска образа
- [[Modular_Monolith]] — приложение внутри образа
- [[Flyway]] — миграции, запускаемые при старте контейнера
