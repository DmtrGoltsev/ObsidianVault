---
id: "source-n8nagents-repository-overview-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents README.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "README.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source snapshot at final GO; production/runtime claims are superseded by CURRENT_STATE"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# N8NAgents foundation

Local, secret-free foundation for a self-hosted Telegram assistant on n8n Community Edition. It defines a three-container edge/application/data stack, least-privilege PostgreSQL boundaries, deterministic trust gates, workflow contracts, encrypted off-host backup design, and verification/runbooks.

## Current delivery status

**Current production: deployed before this source-truth reconciliation; sanitized memory A/B acceptance passed on 2026-08-29.** The original foundation and A2 documents describe the initial pre-deployment state and remain historical gate evidence, not the current runtime status. Current acceptance scope, observed runtime versions, and the explicit `UNKNOWN` production-digest boundary are recorded in [[Доказательство_Production_Acceptance_N8NAgents_20260829|docs/production-memory-acceptance-2026-08-29.md]].

Observed production versions, exact local/parity digest pins, the verified memory-node contract, and remaining unknown gates are distinguished in [[Источник_Compatibility_Matrix_Source_2026-08-29|docs/compatibility-matrix.md]]. The repository still omits an n8n task-runner container and credential-bearing workflow export; the sanitized structural memory contract contains no credential or node IDs.

## Layout

- `infra/` — Compose, Caddy, PostgreSQL bootstrap, backup and restore utilities.
- `contracts/` — machine-readable JSON Schemas for trusted workflow boundaries.
- `workflows/specs/` — implementation specifications and import gates; no invented credential IDs or node parameters.
- `docs/` — architecture, threat model, compatibility, deployment/rollback and operator runbooks.
- `scripts/` — deterministic local checks.

## Safe local validation

On PowerShell:

```powershell
./scripts/verify-static.ps1
```

On a POSIX shell:

```sh
./scripts/verify-static.sh
```

If Docker is present, the verification script also runs `docker compose config --no-interpolate`. The PostgreSQL 17.11 disposable parity gate is documented separately from production A/B evidence; see [[Матрица_Верификации_N8NAgents_2026-08-29|docs/verification-matrix.md]].

## Deployment gate

Do not treat local static PASS as authorization for a new deployment or production mutation. The Phase A manifest remains the historical procedure for an initial deployment; any current production change requires its own reviewed release envelope, stop conditions, rollback plan, and fresh evidence. Hashes bind evidence integrity but are not claimed as cryptographic signatures. Follow [[Исторический_Манифест_Phase_A_Deploy_Rollback_N8NAgents|docs/deploy-rollback-manifest.md]].
