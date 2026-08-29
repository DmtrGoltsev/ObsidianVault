---
id: "source-n8nagents-threat-model-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/threat-model.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/threat-model.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source threat-model snapshot; unresolved items remain planned until verified"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Threat model

| Threat | Boundary | Primary controls | Evidence gate / residual risk |
|---|---|---|---|
| Forged Telegram webhook | Internet→workflow | TLS, exact POST route, secret header checked first | Live negative tests: missing/wrong secret causes zero DB/LLM/tool calls. Secret compromise still requires rotation. |
| Unauthorized user/chat | Payload→trusted context | Numeric server allowlists before DB/LLM/tools; trusted destination derived from payload | Test unknown user and chat separately. Telegram account/chat compromise remains possible. |
| Prompt injection from message/memory/note/tool result | Untrusted data→LLM | Treat as data; narrow workflow tools; fixed trusted identity/destination; no generic capabilities | LLM can still generate poor text; deterministic authorization owns side effects. |
| Replay/duplicate delivery | Webhook→side effect | Unique `(bot_id,update_id)`, leases, bounded retry and explicit state | Crash windows and ambiguous Telegram send outcomes are tracked; no exactly-once claim. |
| Tool retry with changed payload | LLM→tool | Actor+operation+idempotency key unique; SHA-256 payload hash conflict rejection | Test same key/same payload and same key/different payload. |
| Cross-user memory/data leak | n8n→PostgreSQL | Derived session key, trusted actor/chat SQL predicates, separate DB role/schema | Requires live two-user persistence/isolation tests. Runtime credential compromise can read its granted dataset. |
| SSRF / metadata access | n8n HTTP capability | SSRF protection enabled; no unrestricted model-facing HTTP tool; allowlisted fallback endpoint | Exact 2.36.7 env behavior and IPv4/IPv6 blocks require container tests. |
| Shell/filesystem/code execution | LLM→n8n | Execute Command and read/write file nodes excluded; node env access blocked; file path restricted | Exact exclusions verified after startup/security audit. Code node exposure must be reviewed before import. |
| Credential disclosure | Git/logs/export | placeholders only, server `.env` 0600, n8n Credentials, pruning/redaction, secret scan | UI operator and backups remain privileged. Never use decrypted credential export. |
| Public editor/API | Internet→Caddy/n8n | separate domain, HTTPS, owner auth+2FA, public API/Swagger disabled; access proxy/VPN/IP gate recommended | Editor access-control choice is a manual input; do not deploy if risk is unaccepted. |
| Database privilege escalation | n8n→PostgreSQL | separate roles, schema ownership NOLOGIN, runtime no DDL/admin/cross-database connect | Disposable role/grant tests required. n8n metadata role necessarily controls its own DB. |
| Supply-chain drift | Registry→host | exact version tags now, immutable digests before deploy, no `latest`, runner omitted | Tags are mutable until digest gate is closed. |
| Backup theft / failed recovery | Host→off-host | age encryption before upload, checksum, private identity off-host, isolated restore drill | Backup helper digest/destination/key custody/RPO/RTO are manual gates. |
| Reverse-proxy bypass | Internet→container | Phase A disables Caddy and binds bootstrap n8n to loopback only; data network internal; later external IPv4/IPv6 scan | A2 found no local firewall and provider firewall remains unknown, so public-edge is blocked. |

## Approval boundary

Ordinary approved scope is Telegram → approved DeepSeek path → allowlisted narrow tool → response to the original chat. Deletion, publication, new recipients, new data classes, destructive side effects, schema/permission changes, payments and external sends require a separate one-time server-side approval bound to actor, chat, tool, payload hash, expiry and nonce. No such approval mechanism is claimed implemented in Wave 1.
