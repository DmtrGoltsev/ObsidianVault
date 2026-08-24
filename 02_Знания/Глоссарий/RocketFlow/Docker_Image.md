---
id: "term-docker-image"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/58-github-cicd-policy.md"]
доказательства: ["Док_Prod_Deploy_State"]
теги: ["devops", "развертывание"]
---

# Docker Image (Docker образ)

## Определение

Контейнеризированная упаковка бэкенда RocketFlow. На 2026-06-07 Docker/GHCR не является подтверждённой production model; фактический production deploy — jar/systemd + web static на [[HexCore]].

## Контекст в проекте

- Бэкенд собирается в Docker образ: `rocketflow-backend:latest`
- Сборка определена в `backend/Dockerfile`
- Локальная сборка и smoke-тест доказаны: контейнер стартует с `/actuator/health = UP` против `postgres:16`
- Целевой registry для open gate: GHCR (GitHub Container Registry)
- Имя образа-кандидата: `ghcr.io/<owner>/rocketflow-backend`
- Актуальный GHCR publish workflow отсутствует или требует восстановления; см. [[Задача_GHCR_Publish]]

## Связанные термины

- [[HexCore]] — production-сервер для запуска образа
- [[Modular_Monolith]] — приложение внутри образа
- [[Flyway]] — миграции, запускаемые при старте контейнера
- [[Док_Prod_Deploy_State]] — factual deploy state
