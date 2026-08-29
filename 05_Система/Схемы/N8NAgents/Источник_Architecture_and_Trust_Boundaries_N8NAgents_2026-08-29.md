---
id: "source-n8nagents-architecture-trust-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/architecture.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/architecture.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "historical source architecture snapshot; canonical current architecture is the Obsidian AS-IS/API-tools note"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current canonical architecture: [[Архитектура_AS_IS_и_API_Tools_N8NAgents]].
>

# Architecture, trust boundaries and data flow

## Deployment shape

```text
Internet
  ├─ editor.example → Caddy :443 → n8n :5678
  └─ hooks.example  → Caddy :443 → exact POST webhook only → n8n :5678
                                             │
                 DeepSeek API / Telegram API │ (explicit workflows only)
                                             ▼
                              PostgreSQL :5432 (internal network)
                         ┌────────────┬───────────────┐
                         │ n8n DB     │ assistant DB  │
                         │ metadata   │ app + memory  │
                         └────────────┴───────────────┘
```

Only Caddy publishes host ports `80/443`, and it is disabled by the `public-edge` Compose profile unless explicitly selected. In Phase A, the bootstrap override publishes n8n only on `127.0.0.1:5678`; PostgreSQL never has a host port. Caddy+n8n share `edge`; n8n+PostgreSQL share the Docker-internal `data` network. Persistent named volumes hold PostgreSQL, n8n state and, after the later public gate, Caddy certificates/config state.

## Trust boundaries

1. **Internet → Caddy.** All input is untrusted. Direct edge mode trusts no incoming proxy ranges or spoofable forwarding headers. The webhook vhost admits only JSON on one exact POST path, caps the body at 1 MB, and returns `404` for all other matches. The editor hostname stays offline until localhost-only owner bootstrap and 2FA finish.
2. **Caddy → webhook workflow.** A dedicated n8n Webhook Header Auth credential rejects the Telegram secret header at the trigger boundary, before workflow execution, identity parsing, database access or LLM calls. The exact 2.36.7 auth contract is an import gate. The body is size/type checked and only `message.text` is accepted.
3. **Telegram payload → trusted context.** `user_id`, `chat_id`, `bot_id`, `update_id` and the reply destination are normalized deterministically, cast to numeric types and matched against server configuration. The LLM never supplies or overrides them.
4. **n8n → LLM.** Prompt text, memory, notes and third-party results remain untrusted data. The LLM may select only named workflow tools with narrow schemas. It cannot choose credentials, arbitrary recipients, URLs, SQL, filesystem paths, shell commands or administrative capabilities.
5. **n8n → PostgreSQL.** Separate credentials isolate n8n metadata, assistant data and chat memory. Runtime roles have no superuser, role/database creation, replication or bypass-RLS privileges. Only `memory_runtime` has schema-creation privilege, restricted to the dedicated `memory` schema because the production-proven LangChain node always checks `CREATE TABLE IF NOT EXISTS`; it has no `CREATE` on `public` or any other schema. Workflow SQL is parameterized and includes trusted actor/chat predicates.
6. **Backup boundary.** Plaintext exists only in a mode-0700 temporary directory, is encrypted locally with an age recipient whose private identity is off-host, checksummed, copied off-host, and removed. Backup plus the exact `N8N_ENCRYPTION_KEY` form a restore pair.

## Inbound data flow

1. Caddy matches `POST /webhook/telegram-assistant` on `WEBHOOK_DOMAIN`; all other webhook-host routes return `404`.
2. Webhook Header Auth checks `X-Telegram-Bot-Api-Secret-Token` using a dedicated server-side n8n credential. Mismatch terminates before workflow execution and therefore without LLM/DB/tool calls.
3. Validate JSON content, supported update kind, text presence/length, and numeric identifiers.
4. Apply numeric user/chat allowlists stored as manually bound deterministic runtime configuration, not model input or node environment access. Unauthorized IDs terminate before any database/effect/model/memory/tool access.
5. Only after authentication, normalization and both allowlists, insert/claim unique `(bot_id, update_id)` in `app.telegram_updates`. Duplicate/completed updates do not re-run side effects; expired processing leases may be reclaimed with bounded retries.
6. Derive the memory key: private `chat_id`; group `chat_id:user_id`.
7. Invoke the compatibility-approved native DeepSeek agent or deterministic fallback router. Trusted identity is wired from the normalization node, never `$fromAI()`.
8. Tool sub-workflows validate schemas, reserve idempotency, perform a narrow parameterized operation, append audit, and return the common response envelope.
9. Split a reply near 3500 Unicode code points without parse mode and send only to the original trusted chat.
10. Mark update complete. Telegram send uncertainty is recorded separately; the design promises effectively-once only for tested duplicate/retry windows, not global exactly-once.

## Data ownership

- `n8n_metadata` database: internal n8n metadata/credentials/executions, managed only by `n8n_runtime`.
- `assistant_app.app`: tables are private; `assistant_runtime` can execute only five fixed-search-path Security Definer APIs. It has no direct table DML, DELETE, TEMPORARY or cross-database access.
- `assistant_app.memory`: chat history table with `SELECT`, `INSERT`, and `DELETE` plus schema `CREATE` only by `memory_runtime`; table `UPDATE` and sequence `SELECT` remain denied. The exact n8n 2.36.7 memory-node DDL contract and stateful `ai_memory` edge are pinned and regression-tested.
- Schema ownership belongs to `NOLOGIN` owner roles. Migrations run through an explicit privileged bootstrap/migration process, never through LLM tools.

## Discovered host boundary

A2 read-only discovery is `PASS`: Ubuntu 26.04/kernel 7.0, 2 vCPU, 1.6 GiB RAM with about 1.4 GiB available, no swap, 39 GiB disk with about 34 GiB free, UTC with NTP, public IPv4+IPv6, only SSH on port 22, free 80/443/5678/5432, working outbound DNS/HTTPS, empty `/opt` and `/srv`, and no Docker/Compose/Caddy/PostgreSQL/n8n/Redis or local firewall tooling. Architecture, provider-console recovery, provider firewall policy and intended IPv6 exposure still require preflight evidence. These are discovery facts, not deployment evidence; see [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826|server-discovery.md]].
