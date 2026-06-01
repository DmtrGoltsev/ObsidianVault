---
id: "moc-devops"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/04-architecture-blueprint.md"]
доказательства: []
теги: ["moc", "devops", "rocketflow"]
---

# MOC DevOps

Карта DevOps и CI/CD RocketFlow. GitHub Actions (ubuntu-24.04), [[HexCore]] production, [[Docker_Image|Docker]], [[Flyway]].

## CI/CD воркфлоу (4 основных)

### 1. backend-verify.yml
- `mvn test` — модульные тесты с Embedded PostgreSQL
- `mvn compile` — компиляция
- Триггер: push, pull_request в backend/
- См. [[Док_Backend_Тесты]]

### 2. web-verify.yml
- `npm ci` + `npm run build` — сборка веб-клиента
- Триггер: push, pull_request в web/
- См. [[Док_Web_Build]]
- Статус: build-only (без runtime тестов) — см. [[Задача_CI_Runtime_Lanes]]

### 3. android-verify.yml
- `assembleDebug` — сборка Android
- Триггер: push, pull_request в android/
- См. [[Док_Android_Build]]
- Статус: build-only (без runtime тестов) — см. [[Задача_CI_Runtime_Lanes]]

### 4. production-deploy.yml
- Сборка [[Docker_Image|Docker-образа]] бэкенда
- Публикация в GHCR — см. [[Задача_GHCR_Publish]]
- Деплой на [[HexCore]]
- [[Flyway]] миграции при старте
- См. [[Регламент_Деплоя]]

## HexCore (production)

[[HexCore]] — production-сервер (45.10.110.42):
- systemd — управление сервисами
- Nginx — reverse proxy + статика веб-клиента
- PostgreSQL 16 — база данных
- Docker — контейнеризация бэкенда

## Окружения

- **local** — локальная разработка (Docker Compose)
- **CI** — GitHub Actions (сборка и тесты)
- **staging** — предпродакшен (опционально)
- **production** — [[HexCore]]

## Скрипты автоматизации

- `docker-compose.yml` — локальное окружение
- `Dockerfile` — сборка образа бэкенда
- Flyway миграции — автозапуск при старте

## Бэкапы

- PostgreSQL — pg_dump по расписанию (определяется runbook)
- Docker-образы — хранение в GHCR

## Мониторинг и оповещения

См. [[Регламент_Нотификационного_Смока]], [[Источник_Продакшен_Runbook]].

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — бэкенд
- [[MOC_Веб]] — веб-клиент
- [[MOC_Android]] — Android-клиент

## Связанные задачи

- [[Задача_GHCR_Publish]]
- [[Задача_CI_Runtime_Lanes]]
- [[Ограничения_и_Риски]]
