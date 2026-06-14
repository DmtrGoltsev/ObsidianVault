---
id: "reg-deploy-finance"
тип: "регламент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-13"
обновлено: "2026-06-13"
уверенность: "средняя"
источники: ["docs/deploy/finance-production-install.md", ".github/workflows/finance-hexcore-prod-deploy.yml"]
доказательства: []
теги: ["регламент", "деплой", "production", "finance", "hexcore"]
---

# Регламент Деплоя Finance

## Цель

Зафиксировать production deploy policy для Finance на [[HexCore]] без хранения значений секретов и без утверждения, что новый deploy уже выполнен.

## Основной production deploy

Основной путь production deploy для Finance PWA — GitHub Actions workflow `.github/workflows/finance-hexcore-prod-deploy.yml`.

- Workflow выполняет frontend-only PWA deploy на HexCore.
- Auto deploy запускается только при push в ветки, имя которых содержит `release`.
- GitHub environment: `production`.
- Concurrency включен.
- Required GitHub Actions secrets by name: `HEXCORE_PROD_SSH_HOST`, `HEXCORE_PROD_SSH_USER`, `HEXCORE_PROD_SSH_PRIVATE_KEY`, optional `HEXCORE_PROD_SSH_PORT`.
- Backend deploy automation не включен в этот workflow и остается manual/future.

Примечание: наличие workflow и этого регламента не означает, что production deploy уже выполнен.

## Fallback / alternative deploy

Direct SSH/SCP upload to HexCore остается fallback/alternative способом для ручного восстановления или разового deploy при недоступности GitHub Actions.

Fallback boundary:
- PWA static build может быть загружен в nginx docroot через SCP;
- backend deploy остается отдельной manual/future процедурой;
- secret values не документируются и не выводятся;
- перед ручным fallback требуется явный smoke plan и rollback plan.

## Известные blockers/risks

- Backend automation not included: текущий workflow покрывает PWA frontend-only deploy.
- Rollback partial: rollback для PWA и backend должен рассматриваться отдельно.
- Required secrets зафиксированы только по именам; значения не должны попадать в KB, логи или evidence.
- HTTPS/domain/PWA install proof может требовать отдельного evidence, если scope release включает install behavior.

## Связанные заметки

- [[Finance]]
- [[HexCore]]
