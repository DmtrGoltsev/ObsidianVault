---
id: "spec-n8nagents-workflow-artifacts-import-gate"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/README.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/README.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source specification snapshot; production activation is governed by CURRENT_STATE"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Workflow artifacts and import gate

This repository contains specifications and a credential-free structural contract, but no credential-bearing workflow export. The production-proven n8n 2.36.7 Trusted Session Memory node and its mandatory `ai_memory` edge are pinned in `templates/trusted-session-memory.contract.json`; `scripts/verify-contracts.py` rejects legacy parameters, stateless edge removal and a `public` schema fallback. The structural contract deliberately contains no node ID, credential ID or secret and is not an importable workflow export.

Any later full export must still come from the exact n8n 2.36.7 instance with credentials removed/rebound in the UI. Each export must be parsed, imported into a second clean 2.36.7 instance, inspected for unknown nodes/parameters, scanned for secrets and committed with its evidence record. Draft JSON is never production evidence.

Required eventual publication order:

1. Tool sub-workflows.
2. DeepSeek compatibility spike.
3. Main Telegram workflow.
4. Reminder dispatcher and error handler.
