---
id: "proof-prod-deploy-state-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["docs/60-hexcore-prod-runbook.md", "docs/66-weekly-focus-calendar-delivery.md", ".github/workflows/backend-hexcore-prod-deploy.yml", "docs/58-github-cicd-policy.md", "prod deploy preflight 2026-06-08"]
доказательства: ["Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification"]
теги: ["доказательство", "production", "deploy", "hexcore", "blocked"]
---

# Док: Prod Deploy State

## Текущий статус

Feature checkpoint 2026-08-10: Calendar/Weekly Focus/Web Push **NOT DEPLOYED**. Нет evidence применения `V19`/`V20`, promotion текущего backend/web, signed Android production APK, notification enablement или production provider smoke.

Последний документированный production baseline был успешно развёрнут 2026-06-19 из commit `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`. Этот historical PASS не распространяется на текущую feature-ветку.

## Фактическая production model

Production сейчас описывается как jar/systemd/web static deploy:

- Backend: Java jar под systemd на [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, service `rocketflow-backend`
- Web: static React build через Nginx
- DB: PostgreSQL 16
- Deploy workflow: `.github/workflows/backend-hexcore-prod-deploy.yml`
- Canonical deploy trigger: ветка с `release` в имени; текущая feature-ветка delivery — `codex/weekly-focus-calendar-web-push` и сама по себе не является deploy evidence.
- Production deploy path: GitHub Actions release-branch deploy is the primary production deploy path; direct SSH/SCP upload to HexCore is retained only as a manual/emergency fallback.

## Что не является подтверждённым фактом

- `production-deploy.yml` не является актуальным workflow.
- Docker/GHCR deploy не закрыт и остаётся open gate.
- GHCR publish workflow отсутствует или требует восстановления; не считать resolved без отдельного evidence.
- Для feature rollout не доказаны production backup/rollback decision, VAPID/FCM configuration, signed Android artifact и provider/runtime smoke.
- На checkpoint отсутствуют Android release keystore и Firebase client config; production Android signing остаётся blocked.

## Связанные заметки

- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
- [[Задача_GHCR_Publish]]
- [[HexCore]]
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]]

## Final CI/CD local preparation and inventory status (2026-06-14)

Status: PASS for local CI/CD preparation. This section supersedes the older 2026-06-08 "blocked" wording only for CI/CD preparation evidence; it does not claim that a new production deploy was executed.

- User confirmed RocketFlow is production.
- Read-only HexCore inventory confirmed live service `rocketflow-backend.service`.
- Live routes: `/rocket/ -> /var/www/rocketflow-web/current`; `/rocket-api/ -> 127.0.0.1:8080/api/`.
- Backend current symlink: `/opt/rocketflow/current/rocketflow-backend.jar`.
- Database: `rocketflow_prod`.
- Flyway state: 18 rows.
- Health: OK.
- Local workflow/docs prepared: hardened `.github/workflows/backend-hexcore-prod-deploy.yml`, new GHCR package and rollback workflows, `docs/production/rocketflow-*`, policy/runbook updated.
- Historical 2026-06-14 preparation state: release push only built artifacts and production deploy required manual dispatch; superseded by 2026-06-19 release-branch deploy evidence.
- Final reviewer PASS: all 7 workflow YAML files parse; no raw `${{ inputs.* }}` in `run` or `script`; release push no prod mutation; dispatch gates present; no hardcoded secret values.
- Historical note: no production deploy was executed during the 2026-06-14 preparation update; superseded by final deploy evidence on 2026-06-19.
- Residual approvals: GitHub production environment/secrets/required reviewers, first production workflow run, deploy/restart/migration/rollback/GHCR publish approvals, DB backup proof; DB rollback out of scope.
- Evidence: [[CI_CD_Production_Status_20260614]].

## Final production deploy state (2026-06-19)

Status: PASS.

- Repo: `C:\Users\style\Documents\Codex\RocketFlow`, remote `DmtrGoltsev/RocketFlow`.
- Implementation branch: `codex/rocketflow-cicd-prod-deploy-update`.
- Release branch: `release/rocketflow-prod-ci-cd-ec377a7`.
- Release commit: `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`.
- Final green deploy run: `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/27803394498`; package/deploy success.
- Companion verify runs on previous release commit succeeded; final release-branch companion workflows also completed successfully per worker.
- Production backend symlink: `rocketflow-backend-sha-4dbf10b0d693.jar`.
- Production web symlink: `rocketflow-web-sha-4dbf10b0d693`.
- Health public/local: `UP`; frontend `http://45.10.110.42/rocket/` -> 200; API `http://45.10.110.42/rocket-api/health` -> 200, `{"status":"UP"}`.
- Flyway rows `18 -> 18`; app Flyway lifecycle no migration necessary.
- Residual risk: independent DB read via local SSH principal unavailable; evidence from deploy logs.
- Evidence: [[CI_CD_Production_Status_20260619]].
