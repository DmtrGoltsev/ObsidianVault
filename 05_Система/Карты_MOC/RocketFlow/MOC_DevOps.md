---
id: "moc-devops"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/04-architecture-blueprint.md"]
доказательства: ["Док_Cleanup_Manifest", "Док_Prod_Deploy_State"]
теги: ["moc", "devops", "rocketflow"]
---

# MOC DevOps

Карта DevOps и CI/CD RocketFlow. GitHub Actions (ubuntu-24.04), [[HexCore]] production, jar/systemd + web static deploy, [[Flyway]]. [[Docker_Image|Docker/GHCR]] остаётся open gate.

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
- Unit/build/lint lane: Android unit tests, debug build, lint
- Триггер: push, pull_request в android/
- См. [[Док_Android_Build]]
- Статус: не build-only; instrumented/runtime verifier остаётся отдельным gate — см. [[Док_Android_Verification]], [[Задача_CI_Runtime_Lanes]]

### 4. backend-hexcore-prod-deploy.yml
- Деплой backend jar на [[HexCore]] через systemd
- Деплой web static через Nginx
- [[Flyway]] миграции при старте
- См. [[Регламент_Деплоя]], [[Док_Prod_Deploy_State]]

### GHCR publish
- Актуальный GHCR workflow отсутствует или требует восстановления
- Docker/GHCR не считать resolved без отдельного evidence — см. [[Задача_GHCR_Publish]]

## HexCore (production)

[[HexCore]] — production-сервер (45.10.110.42):
- systemd — управление сервисами
- Nginx — reverse proxy + статика веб-клиента
- PostgreSQL 16 — база данных
- Production model — Java jar под systemd + web static через Nginx

## Окружения

- **local** — локальная разработка
- **CI** — GitHub Actions (сборка и тесты)
- **staging** — предпродакшен (опционально)
- **production** — [[HexCore]]

## Скрипты автоматизации

- `backend-hexcore-prod-deploy.yml` — фактический production deploy workflow
- `Dockerfile` — сборка образа бэкенда; GHCR publish остаётся open gate
- Flyway миграции — автозапуск при старте

## Бэкапы

- PostgreSQL — pg_dump по расписанию (определяется runbook)
- Релизные tar.gz архивы вынесены в `C:\Users\style\Documents\RocketFlow_Archive\release-packages\`
- Docker-образы/GHCR — open gate

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
- [[Док_Cleanup_Manifest]]
- [[Док_Prod_Deploy_State]]
