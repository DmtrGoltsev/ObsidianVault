---
id: "finance-pwa-iphone-parity-prod-deploy-20260727"
тип: "доказательство"
статус: "выполнено"
проект: "Finance"
владелец: "codex-release-worker"
создано: "2026-07-27"
обновлено: "2026-07-27"
уверенность: "высокая"
источники:
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\apps\\web-pwa"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\.github\\workflows\\finance-hexcore-prod-deploy.yml"
доказательства:
  - "https://github.com/DmtrGoltsev/finance/actions/runs/30222446226"
  - "C:\\Users\\style\\Documents\\Codex\\Финансы\\MVP_EVIDENCE\\pwa-iphone-parity-postfix-qa-20260727-005600\\SUMMARY.md"
теги: ["finance", "pwa", "iphone", "production", "deploy", "github-actions"]
---

# Finance PWA iPhone parity production deploy — 2026-07-27

## Результат

Production deploy выполнен через основной путь GitHub Actions. Direct local SSH/SCP не использовался.

- Branch: `prod/finance-pwa-iphone-parity-release-20260727`.
- Commit: `55f4ac53146f504cf688a60ad1b0ff95e1937e14`.
- Release ID: `20260726T220603Z-55f4ac53`.
- GitHub Actions: `https://github.com/DmtrGoltsev/finance/actions/runs/30222446226`, status `completed/success`.
- Jobs: `frontend-ci-package`, `deploy-frontend`, `backend-ci-package`, `deploy-backend` all success.
- Frontend artifact digest: `sha256:758e14575cbb42c208904aaf6a4ae5b1dac9c7a8401b524cf2bcb3693c82a663`.
- Backend artifact digest: `sha256:9a9a9b9c630db239496b29a78bb60a7033732d95fdfa9ed9760c201f34495407`.

## Production smoke

- Frontend URL: `http://45.10.110.42/finance/` -> HTTP 200.
- Deployed HTML includes `viewport-fit=cover`.
- Deployed assets:
  - JS: `/finance/assets/index-BeS24vSE.js` -> HTTP 200.
  - CSS: `/finance/assets/index-BFLim9JM.css` -> HTTP 200.
  - Manifest: `/finance/manifest.webmanifest` -> HTTP 200, `start_url=/finance/`, `scope=/finance/`.
  - Icon: `/finance/pwa-icon.svg` -> HTTP 200.
- Backend health: `http://45.10.110.42/finance-api/health` -> HTTP 200, `{"status":"ok"}`.
- Backend OpenAPI: `http://45.10.110.42/finance-api/openapi.json` -> HTTP 200.
- API route smoke:
  - `/finance-api/api/v1/reports/summary?...` -> HTTP 401 unauthenticated, route mounted/protected.
  - `/finance-api/api/v1/reports/category-breakdown?...` -> HTTP 401 unauthenticated, route mounted/protected.
- OpenAPI confirms `/api/v1/reports/summary`, `/api/v1/reports/category-breakdown`, `TransactionCreateRequest.transactionDate`, and `TransactionUpdateRequest.transactionDate`.

## DB / migrations / backup

- Release branch push resolved `run_migrations=true` automatically.
- Alembic current before migration: `20260618_0017`.
- Alembic target: `20260618_0017`.
- Result: no-op migration validation; backend deploy/restart succeeded.
- Workflow created automatic production DB backup before Alembic validation.
- Backup path and SHA are partially redacted by GitHub secret masking in logs:
  - `backup_file=/opt/finance/backups/postgres/finance_prod-20260726T***0746Z-20260726T***0603Z-55f4ac53-20260618_0017-to-20260618_0017.dump`
  - `backup_sha256=9fb487eb63a02c7960b6d469b0f623ecdd3a162d47ace39***879a4dbed13edc6`
  - `evidence_file=/opt/finance/backups/postgres/finance_prod-20260726T***0746Z-20260726T***0603Z-55f4ac53-20260618_0017-to-20260618_0017.dump.evidence.txt`

## Scope

Committed scope:

- `apps/web-pwa/index.html`.
- `apps/web-pwa/src/App.tsx`.
- `apps/web-pwa/src/App.test.tsx`.
- `apps/web-pwa/src/api/client.ts`.
- `apps/web-pwa/src/api/client.test.ts`.
- `apps/web-pwa/src/api/types.ts`.
- `apps/web-pwa/src/styles.css`.
- `MVP_EVIDENCE/pwa-iphone-parity-postfix-qa-20260727-005600/**`.

Excluded from release commit: pre-existing dirty Android files, APK/artifact byproducts, old evidence directories, and unrelated project docs currently dirty in the worktree.

## Risks

- Production is served as plain HTTP IP: `http://45.10.110.42/finance/`.
- `https://45.10.110.42/finance/` failed TLS handshake during smoke.
- Because the browser-facing production origin is not HTTPS, iPhone/Safari Secure cookie persistence, service worker registration, and installability remain a release risk/blocker until a valid HTTPS origin or approved waiver exists.
- Real iPhone/Safari manual run was not performed in this deploy worker pass; local evidence remains Playwright Chromium iPhone 14 smoke.
