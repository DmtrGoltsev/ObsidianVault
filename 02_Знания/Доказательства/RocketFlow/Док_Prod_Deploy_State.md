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
доказательства: ["Док_Production_Rollout_20260810", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification"]
теги: ["доказательство", "production", "deploy", "hexcore", "rollout"]
---

# Док: Prod Deploy State

## Текущий статус

Current production PASS 2026-08-10: Calendar/Weekly Focus backend и web развёрнуты из exact source SHA `910c061de4af9395d9bb682624bd966b2977a738` как release `sha-910c061de4af`. [Deploy run 31357406631](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/31357406631) завершился `success`; Flyway current `V20`, `20/20` successful, `0` failed; local/public health `UP/200`.

Формулировка feature checkpoint 2026-08-10 **NOT DEPLOYED** была верна до release branch rollout и сохранена как история в [[Док_Calendar_Weekly_Focus_WebPush_20260810]]. Baseline 2026-06-19 из commit `4dbf10b0d693ea9f160993fe15199bc0047bb2ea` также остаётся historical evidence.

## Фактическая production model

Production сейчас описывается как jar/systemd/web static deploy:

- Backend: Java jar под systemd на [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, service `rocketflow-backend`
- Web: static React build через Nginx
- DB: PostgreSQL 16
- Deploy workflow: `.github/workflows/backend-hexcore-prod-deploy.yml`
- Canonical deploy trigger: ветка с `release` в имени; rollout выполнен из `release-weekly-focus-calendar-910c061de4af`.
- Production deploy path: GitHub Actions release-branch deploy is the primary production deploy path; direct SSH/SCP upload to HexCore is retained only as a manual/emergency fallback.

## Что не является подтверждённым фактом

- `production-deploy.yml` не является актуальным workflow.
- Docker/GHCR deploy не закрыт и остаётся open gate.
- GHCR publish workflow отсутствует или требует восстановления; не считать resolved без отдельного evidence.
- Feature rollout backup и rollback readiness доказаны в [[Док_Production_Rollout_20260810]]; rollback не использовался.
- Focus cadence и Web Push остаются disabled; provider delivery smoke не заявляется.
- Android release keystore и Firebase client config отсутствуют. Production-configured APK собран unsigned и не является installable/publishable production release.
- Authenticated read smoke остаётся evidence gap; unauthenticated protection checks прошли.

## Связанные заметки

- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
- [[Задача_GHCR_Publish]]
- [[HexCore]]
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]]
- [[Док_Production_Rollout_20260810]]

## Production rollout state (2026-08-10)

Status: PASS for backend/web rollout; Android signing/provider delivery остаются отдельными gates.

- Source/deployed SHA: `910c061de4af9395d9bb682624bd966b2977a738`; release ID `sha-910c061de4af`.
- Backend/web symlinks указывают на `sha-910c061de4af` artifacts.
- Flyway: `V18 -> V20`; `20` total, `20` successful, `0` failed.
- Service active/running, `NRestarts=0`; journal errors/exceptions `0`; Nginx `5xx` `0`.
- Backup metadata: `rocketflow_prod_20260810T045958Z.dump`, `2026-08-10T04:59:58Z`, `223191` bytes, SHA-256 `783590b8fa26f6d2882aab0a5cf670b483be5895fd80b6a915cd4c9946841b39`, `pg_restore -l` PASS with `238` catalog entries.
- Rollback readiness: PR `#1` merged в `master` commit `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb`; workflow ID `330828165` active; rollback не запускался.
- Focus cadence/Web Push disabled. Authenticated smoke gap остаётся; unauthenticated protections вернули ожидаемые `400/401`.
- Full evidence: [[Док_Production_Rollout_20260810]].

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
