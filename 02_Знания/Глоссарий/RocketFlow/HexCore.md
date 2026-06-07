---
id: "term-hexcore"
тип: "термин"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "средняя"
источники: ["docs/60-hexcore-prod-runbook.md", "docs/33-current-state-summary.md"]
доказательства: ["Док_Prod_Deploy_State"]
теги: ["devops", "развертывание", "production"]
---

# HexCore

## Определение

Production-сервер RocketFlow. IP: 45.10.110.42. Фактическая модель: backend Java jar под systemd, web static через Nginx, PostgreSQL 16.

## Контекст в проекте

- Развёрнут бэкенд RocketFlow (Java jar через systemd)
- Статика web (React build) отдаётся через Nginx
- База данных: PostgreSQL 16
- Деплой автоматизирован через GitHub Actions workflow: `backend-hexcore-prod-deploy.yml`
- Docker/GHCR deploy не закрыт; это open gate, а не текущий production path
- Runbook: `docs/60-hexcore-prod-runbook.md`

## Окружение

- OS: Linux (systemd)
- Веб-сервер: Nginx
- Java-рантайм: systemd service unit
- БД: PostgreSQL 16 (локально на сервере или отдельно — предположение)

## Связанные термины

- [[Docker_Image]] — альтернативный способ упаковки (jar vs контейнер)
- [[REST_API]] — API, работающее на HexCore
- [[PostgreSQL_Advisory_Lock]] — механизм БД на HexCore
- [[Док_Prod_Deploy_State]] — factual deploy state
