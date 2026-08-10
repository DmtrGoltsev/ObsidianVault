---
id: "proof-cicd-production-status-2026-06-14"
type: "evidence"
status: "actual"
created: "2026-06-14"
updated: "2026-06-14"
projects: ["Focus", "Finance", "RocketFlow"]
tags: ["evidence", "ci-cd", "production", "hexcore", "local-preparation"]
---

# CI/CD Production Status 2026-06-14

## Scope

This note records the final state of full CI/CD local preparation for Focus, Finance, and RocketFlow.

Important boundary: no production deploy, rollback, restart, migration, GHCR publish, server mutation, GitHub settings change, commit, push, or PR was executed as part of this status update. The recorded server facts come from read-only HexCore inventory and health checks.

Supersession: final production deploy state for all three projects is PASS in [[CI_CD_Production_Status_20260619]]. This 2026-06-14 note is historical local-preparation evidence only.

## User Confirmation

- User confirmed all three projects are production projects: Focus, Finance, RocketFlow.

## Read-only HexCore Inventory

### Focus

- Service: `focus.service`
- Web route: `/focus/ -> /var/www/focus/`
- API route: `/focus-api/ -> 127.0.0.1:8082/api/`
- Database: `focus_db`
- Environment file: `/opt/focus/.env`
- Health: OK

### Finance

- Service: `finance-backend.service`
- Web route: `/finance/ -> /var/www/finance/current/`
- API route: `/finance-api/ -> 127.0.0.1:8081/`
- Backend current release: `/opt/finance/releases/20260612T045020Z-26b487d6`
- Database: `finance_prod`
- Environment file: `/etc/finance/backend.env`
- Health: OK

### RocketFlow

- Service: `rocketflow-backend.service`
- Web route: `/rocket/ -> /var/www/rocketflow-web/current`
- API route: `/rocket-api/ -> 127.0.0.1:8080/api/`
- Backend current symlink: `/opt/rocketflow/current/rocketflow-backend.jar`
- Database: `rocketflow_prod`
- Flyway state: 18 rows
- Health: OK

## Local CI/CD Preparation Final State

### Focus

- Strengthened `.github/workflows/backend-prod-deploy.yml`.
- Added `.github/workflows/focus-prod-rollback.yml`.
- Added/updated repo docs under `docs/production/focus-*`.
- Nginx example aligned with live route model.
- Historical 2026-06-14 state: release push built/packaged only; superseded by 2026-06-19 production deploy PASS.
- Historical 2026-06-14 state: production mutation was dispatch-gated; superseded by 2026-06-19 production deploy PASS.
- Flyway is guarded.
- Rollback requires current-release confirmation.
- No raw input interpolation.
- Source auto-login deletion was not performed, but production artifact excludes auto-login files.

### Finance

- Added full `.github/workflows/finance-hexcore-prod-deploy.yml`.
- Added `.github/workflows/finance-prod-rollback.yml`.
- Added/updated repo docs under `docs/production/finance-*`.
- Install doc updated.
- Frontend/backend package/deploy design documented.
- Alembic is gated.
- Restart is gated.
- `known_hosts` is pinned.
- DB rollback is not included.

### RocketFlow

- Hardened `.github/workflows/backend-hexcore-prod-deploy.yml`.
- Added GHCR package workflow.
- Added rollback workflow.
- Added/updated repo docs under `docs/production/rocketflow-*`.
- Policy/runbook updated.
- Historical 2026-06-14 state: release push only built artifacts; superseded by 2026-06-19 production deploy PASS.
- Historical 2026-06-14 state: production deploy required manual dispatch; superseded by 2026-06-19 production deploy PASS.
- GHCR publish is gated.
- `known_hosts` is pinned.
- Health URL fixed.

## Final Reviewer PASS

- All 7 workflow YAML files parse.
- No raw `${{ inputs.* }}` usage in `run` or `script` blocks.
- Release push does not perform production mutation.
- Dispatch gates are present.
- No hardcoded secret values found in reviewed workflow scope.
- No production actions were executed.

## Residual Approvals / Gates

- GitHub production environment, secrets, and required reviewers must be configured/approved outside this local preparation.
- First production workflow run requires explicit approval.
- Deploy, restart, migrations, rollback, and GHCR publish require explicit approval.
- DB backup proof remains required before production mutation.
- DB rollback is out of scope for the prepared workflows.

## Related Notes

- [[Focus]]
- [[Finance]]
- [[Регламент_Деплоя_Focus]]
- [[Регламент_Деплоя_Finance]]
- [[Регламент_CI_CD]]
- [[Регламент_Деплоя]]
- [[Док_Prod_Deploy_State]]
