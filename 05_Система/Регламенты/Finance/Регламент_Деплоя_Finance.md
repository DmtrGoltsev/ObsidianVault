---
id: "reg-deploy-finance"
тип: "регламент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-13"
обновлено: "2026-07-26"
уверенность: "средняя"
источники: ["docs/deploy/finance-production-install.md", ".github/workflows/finance-hexcore-prod-deploy.yml"]
доказательства: []
теги: ["регламент", "деплой", "production", "finance", "hexcore"]
---

# Регламент Деплоя Finance

## Цель

Зафиксировать production deploy policy для Finance на [[HexCore]] без хранения значений секретов.

## Основной production deploy

Основной путь production deploy для Finance frontend/backend — GitHub Actions workflow `.github/workflows/finance-hexcore-prod-deploy.yml`.

- Workflow выполняет frontend/backend package/deploy на HexCore.
- Auto deploy запускается только при push в ветки, имя которых содержит `release`.
- GitHub environment: `production`.
- Concurrency включен.
- Required GitHub Actions secrets by name: `HEXCORE_PROD_SSH_HOST`, `HEXCORE_PROD_SSH_USER`, `HEXCORE_PROD_SSH_PRIVATE_KEY`, optional `HEXCORE_PROD_SSH_PORT`.
- Backend deploy automation включен в актуальный production workflow.

Примечание: финальный production deploy через этот путь подтвержден 2026-06-19; см. [[CI_CD_Production_Status_20260619]].

## Fallback / alternative deploy

Direct SSH/SCP upload to HexCore остается fallback/alternative способом для ручного восстановления или разового deploy при недоступности GitHub Actions.

Fallback boundary:
- PWA static build может быть загружен в nginx docroot через SCP;
- backend deploy через workflow является основным путем; direct SSH/SCP остается fallback;
- secret values не документируются и не выводятся;
- перед ручным fallback требуется явный smoke plan и rollback plan.

## Известные blockers/risks

- Residual runtime risk: production uses `python3 3.14.4`, because `python3.12`/`python3.11` отсутствуют; условие `>=3.12` выполнено, но runtime новее CI 3.12.
- 2026-07-12 investment/transfer sync boundary: Android/local changes for explicit `categoryId:null`, investment sync allowlist, and transfer `accounts/update` sync changes are verified locally, but production backend deploy was not executed. Offline sync investment behavior and transfer account sync changes require GitHub Actions release branch deploy and are blocked until release scope/protection checklist is cleared. Direct SSH/SCP is not the path for this blocked deploy.
- 2026-07-25 auth/session boundary: superseded by the backend auth refresh deploy record below. Android auth/session APK is built/signed/verified, and production backend `/api/v1/sessions/refresh` is deployed through GitHub Actions backend-only path.
- 2026-07-26 monthly investment transfers boundary: backend production deploy is REQUIRED for `/reports/summary.investmentsTotal` to mean selected-period/monthly visible incoming `transfer` into investment asset account/category. The QA/build/documentation worker did not deploy production; Android APK is only a manual-install artifact until backend deploy occurs.
- DB rollback не автоматизирован; restore из backup выполняется вручную после approval.
- Required secrets зафиксированы только по именам; значения не должны попадать в KB, логи или evidence.
- HTTPS/domain/PWA install proof может требовать отдельного evidence, если scope release включает install behavior.

## Transfer assets/order deploy note (2026-07-12)

Status: backend production deploy required for POSTP1 transfer/assets/order prod sync behavior. DB migration is not required.

- Android APK `finance-android-prod-20260712-220221-POSTP1-TRANSFER-manual-install.apk` points to the production API URL and may be installed manually.
- Backend account sync changes for `transfer` are not production-active until deployed through a GitHub Actions release branch.
- Required backend behavior: after transfer, sync publishes `accounts/update` for both source and destination accounts so Android can refresh `dashboard.accounts.currentBalance` and recalculate asset category totals by `assetCategoryId`.
- Planning semantic invariant: `transfer` changes balances/assets but is not investment actual; `asset_buy` remains the investment actual operation type.
- Sync pull ordering by `seq` must remain unchanged because it is the cursor protocol.
- Evidence: `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-transfer-assets-ordering-postp1-qa-20260712-215452`.

## Связанные заметки

- [[Finance]]
- [[HexCore]]

## Final CI/CD local preparation status (2026-06-14)

Status: PASS for local CI/CD preparation. This does not claim that a new production deploy was executed.

- User confirmed Finance is production.
- Read-only HexCore inventory confirmed live service `finance-backend.service`.
- Live routes: `/finance/ -> /var/www/finance/current/`; `/finance-api/ -> 127.0.0.1:8081/`.
- Backend current release: `/opt/finance/releases/20260612T045020Z-26b487d6`.
- Database: `finance_prod`.
- Environment file: `/etc/finance/backend.env`.
- Health: OK.
- Workflow state: `.github/workflows/finance-hexcore-prod-deploy.yml` prepared; `.github/workflows/finance-prod-rollback.yml` added.
- Repo docs: `docs/production/finance-*` prepared; install doc updated.
- Design: frontend/backend package/deploy design documented.
- Safety: Alembic gated; restart gated; pinned `known_hosts`; no DB rollback.
- Final review: workflow YAML parses, no raw input interpolation, no hardcoded secret values in reviewed workflow scope, no production actions executed.
- Residual approvals: GitHub production environment/secrets/required reviewers, first production workflow run, deploy/restart/migration/rollback approvals, DB backup proof; DB rollback out of scope.
- Evidence: [[CI_CD_Production_Status_20260614]].

## Final production CI/CD state (2026-06-19)

Status: PASS. GitHub Actions release-branch production deploy is now the primary path.

- Release branch: `release/finance-prod-ci-cd-27730f5`; release commit `d10ac448a12c6681577d13433ef6225a094afbc2`.
- Final green run: `https://github.com/DmtrGoltsev/finance/actions/runs/27802865321`.
- Current frontend/backend release: `20260619T030640Z-d10ac448`.
- Trigger rule: branch name must contain `release`; push/cherry-pick/merge desired commit into `release/<project>-prod-...`, then watch GitHub Actions.
- Manual `workflow_dispatch` remains available.
- Direct SSH/SCP remains documented fallback, not primary.
- GitHub `production` environment and environment secrets are configured; secret values must never be stored in docs.
- Verify after deploy: `http://45.10.110.42/finance/` and `http://45.10.110.42/finance-api/health`.
- Rollback: use project rollback workflow where available; DB rollback is not automated and requires manual restore from backups after approval.
- Evidence: [[CI_CD_Production_Status_20260619]].

## Auth/session deploy note (2026-07-25)

Status: historical pre-deploy note. Superseded by successful backend production deploy on 2026-07-25. DB migration was not required.

- Android APK `finance-android-prod-20260725-231110-AUTH-SESSION-manual-install.apk` was built, signed and verified for manual install.
- Android stores `SessionTokenBundle` in `EncryptedSharedPreferences`: `accessToken`, `refreshToken`, `expiresAt`, `userId`; password is not stored.
- Backend endpoint required in production: `POST /api/v1/sessions/refresh`.
- Required backend behavior: `android_bearer` login/register return `refreshToken`; refresh token rotation is hash-only, invalidates old refresh tokens, invalidates on logout and uses CAS atomic rotation.
- Client behavior after backend deploy: on `401`/`403`, refresh once and retry once; logout or auth/refresh failure clears local token store and protected UI; screenshot OCR uses the same refresh/retry-once path.
- Deploy caveat: until the backend refresh endpoint is deployed through GitHub Actions release branch, the Android app can store the access token, but refresh fails after access-token TTL.
- Security review after fixes: no P0/P1/P2.
- QA evidence: backend auth `71 passed`, `ruff` PASS, Android full unit PASS, APK built/signed/verified; emulator unavailable, so manual install/smoke skipped.
- Artifact: `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260725-231110-AUTH-SESSION-manual-install.apk`.
- SHA256: `F9ABD3D02D64A06FCB5E78731AC313FD8230165CF9BC8D427E2FED92466BB8A0`.
- Evidence: `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\android-auth-session-qa-20260725-231110`.

## Auth/session backend deploy record (2026-07-25)

Status: backend production deploy successful for auth refresh. GitHub Actions run status is `completed/failure` only because unrelated `frontend-ci-package`/PWA tests failed; backend deploy succeeded.

- Branch: `prod/finance-auth-refresh-20260725`.
- Commit: `9e1ed7903798ed4f1edbcfeb3d98b23ec9ae0763`.
- Release ID: `finance-backend-auth-refresh-20260725-9e1ed79`.
- Actions run: `https://github.com/DmtrGoltsev/finance/actions/runs/30174265210`.
- Dispatch: backend-only; `deploy-frontend` skipped; `deploy-backend` success.
- Health: `http://45.10.110.42/finance-api/health` -> 200 `{"status":"ok"}`.
- Route smoke: `/finance-api/api/v1/sessions/refresh` returns 422 on empty payload, route mounted.
- Refresh smoke: registration 201, refresh 200, token fields present, refresh rotated, old refresh rejected 401; no tokens/passwords in evidence.
- Backend artifact checksum: `da77996a82489e1732a77686eda2965b6f51113d8528828151927ca42b384491`.
- Migrations/backup: `run_migrations=false`; DB migrations not run; workflow backup not created; DB migration not required.
- Direct local SSH/SCP was not used.
- Staged files were exactly allowed auth/OpenAPI backend list.
- Caveat: workflow emails may say failed due frontend job; backend deploy is successful.

## Monthly investment transfers deploy note (2026-07-26)

Status: historical pre-deploy note. Superseded by successful backend production deploy on 2026-07-26.

- Required backend behavior: `/reports/summary.investmentsTotal` must count selected-period/monthly visible incoming `transfer` operations into investment asset accounts/categories. It must not mean total asset balance.
- Boundary: `/reports/account-balances` remains the asset/account balance endpoint.
- Android behavior: Analytics summary investments reads summary data only and does not fallback from account-balances.
- Local QA: backend targeted reports/assets `25 passed`; backend full `302 passed`; Android targeted/full unit PASS; Kotlin compile PASS; release assemble/sign/align/URL scan PASS.
- Artifact: `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260726-221828-MONTHLY-INVESTMENT-TRANSFERS-manual-install.apk`.
- SHA256: `46e85ee4e5c6b4b13cf84abd4da22dcffc2642d0e9afd7d6be16f5c40783a9ca`.
- Evidence: `C:\Users\style\Documents\Codex\Финансы\MVP_EVIDENCE\monthly-investment-transfers-qa-20260726-221828\SUMMARY.md`.
- Direct local SSH/SCP was not used. Production data was not changed. Manual install/launch smoke was skipped because no adb device/emulator was attached.

## Monthly investment transfers backend deploy record (2026-07-26)

Status: backend production deploy successful for monthly investment transfer summary semantics. GitHub Actions run status is `completed/failure` only because unrelated `frontend-ci-package`/PWA tests failed; backend deploy succeeded.

- Branch: `prod/finance-monthly-investment-transfers-release-20260726`.
- Commit: `6a8d2656a4423d80363fb5230f2bb5ddcc8bd937`.
- Release ID: `20260726T194858Z-6a8d2656`.
- Actions run: `https://github.com/DmtrGoltsev/finance/actions/runs/30217638420`.
- Trigger: push to release branch; `backend-ci-package` success; `deploy-backend` success; `deploy-frontend` skipped after `frontend-ci-package` failure.
- Health: `http://45.10.110.42/finance-api/health` -> 200 `{"status":"ok"}`.
- API smoke: `http://45.10.110.42/finance-api/openapi.json` -> 200; unauth `/finance-api/api/v1/reports/summary` -> 401, route mounted/authenticated.
- Migrations/backup: Alembic before `20260618_0017`, target `20260618_0017`; workflow no-op upgrade validation passed and backup was created.
- Backup: `/opt/finance/backups/postgres/finance_prod-20260726T195057Z-20260726T194858Z-6a8d2656-20260618_0017-to-20260618_0017.dump`.
- Backup SHA256: `209f7587277bec2b0e81e464e0da6f81d49ce1cafebede0648f0dab133111553`.
- Backup evidence file: `/opt/finance/backups/postgres/finance_prod-20260726T195057Z-20260726T194858Z-6a8d2656-20260618_0017-to-20260618_0017.dump.evidence.txt`.
- Direct local SSH/SCP was not used.
- Caveat: workflow emails may say failed due frontend job; backend deploy itself is successful. PWA failure signatures: `apps/web-pwa/src/App.test.tsx:709` expected `70`, got `Расходы месяца0 $`; `apps/web-pwa/src/App.test.tsx:799` date-range assertion.
