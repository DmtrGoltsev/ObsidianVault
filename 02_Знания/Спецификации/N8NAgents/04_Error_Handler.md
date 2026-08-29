---
id: "spec-n8nagents-04-error-handler"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/specs/04-error-handler.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/specs/04-error-handler.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source workflow specification; production workflow is inactive"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# `error_handler`

Accept only a bounded internal error envelope: workflow identifier, execution identifier, correlation ID, stage, stable error code, retryability and timestamp. Strip message bodies, prompts, headers, credentials, tokens, database connection data and raw third-party responses before audit or notification.

Write a sanitized `failed` audit event through a fixed query and optionally notify a preconfigured administrator chat only after a separate recipient approval. The model cannot invoke this workflow as a generic tool. Notification failure must not recursively invoke the same handler without a depth guard.
