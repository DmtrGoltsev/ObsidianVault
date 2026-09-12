---
id: "proof-cicd-production-status-2026-06-19"
type: "evidence"
status: "actual"
created: "2026-06-19"
updated: "2026-06-19"
projects: ["Focus", "Finance", "RocketFlow"]
tags: ["evidence", "ci-cd", "production", "hexcore", "deploy"]
---

# CI/CD Production Status 2026-06-19

## Scope

Final actual CI/CD production state for Focus, Finance, and RocketFlow.

Common state:
- GitHub `production` environments and environment secrets are configured for all three repos.
- Secrets are stored as environment secrets; never put secret values in docs.
- Release branch push now triggers production deploy; manual `workflow_dispatch` remains available.
- Branch naming rule: branch name must contain `release`.
- Trigger: push/cherry-pick/merge desired commit into a release branch, e.g. `release/<project>-prod-...`; then watch GitHub Actions and verify endpoints.
- Direct SSH/SCP remains documented fallback, not primary.
- Rollback: use project rollback workflow where available; DB rollback is not automated and requires manual restore from backups after approval.

## Finance

- Repo: `C:\Users\style\Documents\Codex\Финансы`, remote `DmtrGoltsev/finance`.
- Implementation branch: `codex/finance-cicd-prod-deploy-update`.
- Release branch: `release/finance-prod-ci-cd-27730f5`.
- Final release commit: `d10ac448a12c6681577d13433ef6225a094afbc2`.
- Final green run: `https://github.com/DmtrGoltsev/finance/actions/runs/27802865321`, success; all jobs succeeded.
- Current frontend/backend release: `20260619T030640Z-d10ac448`.
- Public frontend: `http://45.10.110.42/finance/` -> 200.
- API health: `http://45.10.110.42/finance-api/health` -> 200, `{"status":"ok"}`.
- Alembic current: `20260618_0017`; migration from `20260612_0015` happened in an earlier retry; final run had current/target `20260618_0017`.
- Backup evidence: `/opt/finance/backups/postgres/finance_prod-20260619T030824Z-20260619T030640Z-d10ac448-20260618_0017-to-20260618_0017.dump`, sha256 `72cf70b10d927cb5be7291148bd83fbcfb7a6342ff9d669634a0e152efa57104`.
- Earlier retry created backup before applying `0016`/`0017`.
- Residual risk: production uses `python3 3.14.4`, because `python3.12`/`python3.11` are missing; satisfies `>=3.12`, but is newer than CI 3.12.

## RocketFlow

- Repo: `C:\Users\style\Documents\Codex\RocketFlow`, remote `DmtrGoltsev/RocketFlow`.
- Implementation branch: `codex/rocketflow-cicd-prod-deploy-update`.
- Release branch: `release/rocketflow-prod-ci-cd-ec377a7`.
- Final release commit: `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`.
- Final green deploy run: `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/27803394498`, success; package/deploy success.
- Companion verify runs on previous release commit succeeded; final release-branch companion workflows also completed successfully per worker.
- Production backend symlink: `rocketflow-backend-sha-4dbf10b0d693.jar`.
- Production web symlink: `rocketflow-web-sha-4dbf10b0d693`.
- Health public/local: `UP`.
- Frontend: `http://45.10.110.42/rocket/` -> 200.
- API health: `http://45.10.110.42/rocket-api/health` -> 200, `{"status":"UP"}`.
- Flyway rows: `18 -> 18`; app Flyway lifecycle reported no migration necessary.
- Residual risk: independent DB read via local SSH principal unavailable; evidence from deploy logs.

## Focus

- Repo: `C:\Users\style\Documents\VS_Agents\Focus`, remote `DmtrGoltsev/Focus`.
- Implementation branch: `feature/softer-green-and-reminders`.
- Release branch: `release/focus-prod-ci-cd-fe6f5af`.
- Final release-green commit: `ddb4262`.
- Final green production run: `https://github.com/DmtrGoltsev/Focus/actions/runs/27804739744`, success; all production jobs success. Earlier production success `https://github.com/DmtrGoltsev/Focus/actions/runs/27804213793` remains valid historical evidence.
- Android Verify on release branch: `https://github.com/DmtrGoltsev/Focus/actions/runs/27804739739`, success.
- Feature proof Android Verify: `https://github.com/DmtrGoltsev/Focus/actions/runs/27804587155`, success.
- Android rerun fix: `android/gradlew` executable mode restored in git (`100644 -> 100755`); keep the Gradle wrapper executable.
- Public frontend: `http://45.10.110.42/focus/` -> 200.
- API health: `http://45.10.110.42/focus-api/health` -> 200.
- Flyway applied V5/V6 during retry; current version is `6`; final run evidence `6 -> 6`.
- Backup evidence: `/opt/focus/backups/github-actions/release-focus-prod-ci-cd-fe6f5af-7/focus_db-release-focus-prod-ci-cd-fe6f5af-7-pre-flyway.evidence.txt`, sha256 `c8d60f1b54b2b0f1dc64d8141fa19920c59d276be5e18220abf9dcf48a0e7936`, bytes `93618`.
- Earlier backup for V4 -> V6: `/opt/focus/backups/github-actions/release-focus-prod-ci-cd-fe6f5af-6/...`, sha256 `786bf0bd2d938ee569f2b64449956cc8289e386a5c956de818b16c10889466e4`.

## Related Notes

- [[Focus]]
- [[Finance]]
- [[RocketFlow]]
- [[Регламент_Деплоя_Focus]]
- [[Регламент_Деплоя_Finance]]
- [[Регламент_CI_CD]]
- [[Регламент_Деплоя]]
- [[Док_Prod_Deploy_State]]
