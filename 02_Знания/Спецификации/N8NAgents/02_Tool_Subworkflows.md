---
id: "spec-n8nagents-02-tool-subworkflows"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/specs/02-tools.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/specs/02-tools.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source tool specification; five tools are imported but not model-facing AS-IS"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Tool sub-workflows

Every tool starts with Execute Sub-workflow Trigger, validates the common request envelope and its payload schema before side effects, receives trusted actor/chat/correlation fields through fixed parent expressions, uses the appropriate least-privilege PostgreSQL credential, and returns `contracts/tool-response.schema.json`.

The common sequence is: validate → canonicalize payload → SHA-256 hash → reserve idempotency → reject key/hash conflict → parameterized operation with trusted actor/chat predicate → sanitized audit → complete reservation → return envelope. No raw prompt/body/token/provider error is stored in audit.

## `tool_save_note`

- Payload: `tool-save-note.payload.schema.json`.
- Insert note for the trusted actor/chat. The UUID is generated deterministically outside the LLM or validated from the request.
- Duplicate identical idempotency request returns the stored result; same key/different hash is rejected.

## `tool_search_notes`

- Payload: `tool-search-notes.payload.schema.json`.
- Parameterized case-insensitive title/body search, constrained by trusted actor and chat, excluding `deleted_at`, ordered newest first, limit 1–50.
- Return only note ID, title, bounded snippet and timestamp.

## `tool_list_notes`

- Payload: `tool-list-notes.payload.schema.json`.
- Return only the trusted actor/chat's nondeleted notes in stable `(created_at,id)` order, with limit 1–50 and bounded snippets.

## `tool_create_reminder`

- Payload: `tool-create-reminder.payload.schema.json`.
- Validate date-time, future/policy bounds and trusted original destination; insert `scheduled` row.
- External send occurs only in dispatcher, not inside creation transaction.

## `tool_list_reminders`

- Payload: allowlisted status set, optional limit 1–50 and validated cursor.
- Filter trusted actor/chat and return bounded fields; no arbitrary sort/filter expressions.

## Explicitly absent model-facing capabilities

Generic SQL, shell, filesystem, code execution, arbitrary/unrestricted HTTP or URL, credentials, Docker, n8n administration, workflow IDs and recipient/destination choice.
