---
id: "proof-prod-deploy-state-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/60-hexcore-prod-runbook.md", ".github/workflows/backend-hexcore-prod-deploy.yml"]
доказательства: ["Док_Cleanup_Manifest"]
теги: ["доказательство", "production", "deploy", "hexcore"]
---

# Док: Prod Deploy State

## Фактическая production model

Production сейчас описывается как jar/systemd/web static deploy:

- Backend: Java jar под systemd на [[HexCore]]
- Web: static React build через Nginx
- DB: PostgreSQL 16
- Deploy workflow: `backend-hexcore-prod-deploy.yml`

## Что не является подтверждённым фактом

- `production-deploy.yml` не является актуальным workflow.
- Docker/GHCR deploy не закрыт и остаётся open gate.
- GHCR publish workflow отсутствует или требует восстановления; не считать resolved без отдельного evidence.

## Связанные заметки

- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
- [[Задача_GHCR_Publish]]
- [[HexCore]]
