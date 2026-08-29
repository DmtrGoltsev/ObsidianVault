---
id: "spec-n8nagents-01-telegram-assistant"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/specs/01-telegram-assistant.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/specs/01-telegram-assistant.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source workflow specification; verified current limits are in canonical architecture"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# `01_telegram_assistant`

## Entry and deterministic trust gate

Webhook is production path `POST /webhook/telegram-assistant`. Bind a dedicated n8n Webhook Header Auth credential whose fixed header name is `X-Telegram-Bot-Api-Secret-Token`; verify its exact 2.36.7 contract in the import gate. Authentication must happen at the trigger boundary, before workflow execution. A missing/wrong header terminates immediately: zero DB, memory, DeepSeek, Telegram or tool calls.

Then require JSON within the Caddy 1 MB limit, one item, a private/group/supergroup `message.text`, UTF-8 text length 1–8000, numeric bot/update/user/chat/message IDs, and supported `allowed_updates=["message"]`. Reject edits, channels, files, albums, callbacks and all events without text.

Normalize exactly to `contracts/telegram-normalized.schema.json`; derive private session key from `chat_id` and group key from `chat_id:user_id`. Apply both numeric user and chat allowlists before any DB/LLM/memory/tool access. The operator enters these non-secret personal IDs into a deterministic authorization node after import; exports/evidence replace them with invalid placeholders. Do not read them from `$env` while node environment access is blocked.

Only after header auth, normalization, and both numeric allowlists may the workflow touch idempotency/update storage or any effect/LLM/tool.

## Trusted session memory

The production-proven n8n `2.36.7` node is named `Trusted Session Memory`, uses `@n8n/n8n-nodes-langchain.memoryPostgresChat` type version `1.4`, and has exactly these parameters: `sessionIdType=customKey`, `sessionKey={{ $('Normalize and Authorize').item.json.session_key }}`, `tableName=n8n_chat_histories`, and `contextWindowLength=20`. The unsupported legacy `sessionId` parameter is absent. Its `ai_memory` output is connected to `Native AI Agent`; removing this edge creates a stateless workflow and is a contract failure. See the credential-free structural contract in `../templates/trusted-session-memory.contract.json`.

## Idempotency and processing

Atomically insert or claim `(bot_id, update_id)` with `received → processing → completed|failed`, lease expiry, bounded attempts and dead-letter handling. Completed duplicates return success without side effects. Active leases are not stolen; expired leases may be reclaimed. Do not hold a transaction across network calls.

Call the compatibility-approved native agent or deterministic fallback. Trusted identity and destination always reference the named Normalize output, never ambiguous `$json` and never `$fromAI()`. Expose only named workflow tools.

Split the final text near 3500 Unicode code points, preserving code-point boundaries. Do not enable parse mode by default. Send only to the normalized original chat. Record ambiguous send results as `uncertain`; do not claim exactly-once.

## Negative tests

Wrong/missing secret, non-POST path, invalid JSON, oversized body/text, unsupported update, absent text, nonnumeric IDs, unknown user, unknown chat, duplicate completed update, active lease, expired lease, DeepSeek timeout/malformed response, Telegram timeout and restart between send and completion.
