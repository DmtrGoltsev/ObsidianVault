---
id: "evidence-n8nagents-local-verification-20260827"
тип: "доказательство"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/local-verification-result.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/local-verification-result.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
source_snapshot: "working tree at import; includes uncommitted evidence reconciliation beyond source_base"
source_file_sha256: "4d3289fe0adc2339eb78f631da787bab9af14c2451c5f5bf52968375d7b406bf"
imported_date: "2026-08-29"
source_status: "historical local verification evidence; not production evidence"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Local verification result — 2026-08-27

Gate: `GO-O4-ATTEMPT1-QUORUM-v2`, state `ATTEMPT1_PRE_CANDIDATE`.

No VPS, SSH, SCP, provider, Vault or network action was performed. No candidate was frozen or submitted, and corrective attempt 1 remains unconsumed.

Host-observed results:

- `PASS`: sealed handoff sizes and SHA-256 values matched its `MANIFEST` for all three content files.
- `PASS`: PowerShell parsing for every project `.ps1` file.
- `PASS`: `sh -n` through local Git `sh.exe` for every project `.sh` file. This is syntax evidence, not privileged Linux behaviour.
- `PASS`: seven canonical K4R evidence unit tests, including exact schemas, derived result rejection, exact 66-case coverage, exact 34-row fault-shim manifest, 28/29 review-ledger binding and semantic UTC checks.
- `PASS`: deterministic two-phase candidate/final package regression, two-build byte equality, stale behaviour rejection and isolated Git mode-`120000` rejection without project object-store writes.
- `PASS`: YAML and migration-sentinel checks reached by `verify-static.ps1`.
- `PASS`: Windows orchestration rejected both `PASS` plus nonzero exit and `BLOCKED-LOCAL` plus zero exit.
- `BLOCKED-LOCAL` (RC 3): `jsonschema` and `referencing` are absent from both the system Python and the bundled Codex Python runtime. No cached offline wheel was found. Draft 2020-12 metaschema and fixture semantics therefore are not a PASS.
- `BLOCKED-LOCAL`: WSL is not installed/configured with a Linux distribution; `wsl --status` returned 50. Docker and Podman are unavailable.
- `BLOCKED-LOCAL`: the required UID-0 private-mount/isolated-network Linux capability record, 66-case actual-runner matrix, canonical fault-shim manifest and eight-case governance/compose Linux static matrix have not executed on this Windows host.
- `PASS` (fail-closed orchestration): `run-k4r-offline.ps1` returned RC 3 with `K4R_OFFLINE_STATUS=BLOCKED` when the Linux capability and matrices were omitted; it did not manufacture evidence or package status.

Consequently this worktree is not `CANDIDATE1_FROZEN`, is not `OFFLINE_READY`, and is not eligible for a commit or package under the current gate. `K4R-REMOTE-1` must not be prepared until the missing offline prerequisites pass and an independent reviewer accepts the exact candidate commit.
