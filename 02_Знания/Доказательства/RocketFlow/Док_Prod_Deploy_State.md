---
id: "proof-prod-deploy-state-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-06-08"
уверенность: "высокая"
источники: ["docs/60-hexcore-prod-runbook.md", ".github/workflows/backend-hexcore-prod-deploy.yml", "docs/58-github-cicd-policy.md", "prod deploy preflight 2026-06-08"]
доказательства: ["Док_Cleanup_Manifest", "Док_Backend_Verification"]
теги: ["доказательство", "production", "deploy", "hexcore", "blocked"]
---

# Док: Prod Deploy State

## Текущий статус

2026-06-08 backend prod deploy: **NOT DEPLOYED / BLOCKED**. Деплой остановлен до явного решения пользователя.

Блокирующие вопросы:
- target ref/method: `workflow_dispatch` или merge/push в каноническую ветку `MVP2`/`release_1`;
- backup expectation перед deploy;
- готовность secrets/env.

## Фактическая production model

Production сейчас описывается как jar/systemd/web static deploy:

- Backend: Java jar под systemd на [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, service `rocketflow-backend`
- Web: static React build через Nginx
- DB: PostgreSQL 16
- Deploy workflow: `.github/workflows/backend-hexcore-prod-deploy.yml`
- Canonical deploy branches: `MVP2` / `release_1`; текущая локальная ветка delivery — `MVP3`

## Что не является подтверждённым фактом

- `production-deploy.yml` не является актуальным workflow.
- Docker/GHCR deploy не закрыт и остаётся open gate.
- GHCR publish workflow отсутствует или требует восстановления; не считать resolved без отдельного evidence.
- Env/secrets/backup readiness не доказаны из текущего shell: отсутствуют `HEXCORE_PROD_SSH_*` и `ROCKETFLOW_PROD_BACKUP_*`.
- Backup user mismatch: предпочтительный `rocketbackup`, ignored local config указывает на `rocketdeploy`.

## Связанные заметки

- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
- [[Задача_GHCR_Publish]]
- [[HexCore]]
