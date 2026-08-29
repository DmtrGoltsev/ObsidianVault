---
id: "source-n8nagents-credential-binding-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/credential-binding.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/credential-binding.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "logical binding design snapshot; contains no credential IDs or values"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Credential binding table

Credentials are created manually in the protected n8n editor after owner/2FA bootstrap. Names below are logical labels, not credential IDs; workflow exports must not embed usable IDs or secret values.

| Logical credential | Type / target | Allowed consumers | Prohibited consumers / notes |
|---|---|---|---|
| `telegram_webhook_secret` | dedicated Webhook Header Auth credential with fixed header name `X-Telegram-Bot-Api-Secret-Token` | production Webhook trigger only, after exact 2.36.7 auth contract is verified | Secret is generated server-side; never in workflow JSON or `.env.example`. Authentication must reject before workflow execution. |
| `telegram_prod` | Telegram Bot API production bot | main send nodes, reminder dispatcher, explicit webhook registration procedure | Never dev/test workflows; token not in webhook URL, Git or `.env.example`. |
| `telegram_dev` | separate Telegram dev bot | disposable compatibility/E2E project only | Never production webhook/workflows. |
| `deepseek_prod` | DeepSeek API key + approved base URL | approved native model node or deterministic fallback request | Never arbitrary/unrestricted model-facing HTTP tool. |
| `postgres_n8n_metadata` | internal Compose configuration for `n8n_runtime@n8n_metadata` | n8n service only | Not a workflow credential or LLM tool; role controls only the metadata DB. |
| `postgres_assistant_runtime` | `assistant_runtime@assistant_app` | five tool sub-workflows only | Only five named Security Definer functions; no table DML/DELETE/TEMP, memory schema, metadata DB or generic SQL tool. |
| `postgres_memory_runtime` | `memory_runtime@assistant_app`, schema `memory` | production-proven Postgres Chat Memory v1.4 only | Table `SELECT`/`INSERT`/`DELETE` and sequence `USAGE` only; no table `UPDATE`, sequence `SELECT`, app schema, metadata DB or TEMP. `CREATE` is restricted to `memory` because LangChain always checks `CREATE TABLE IF NOT EXISTS`; no `public` or other-schema `CREATE`. |

Credential binding is a manual import-time action. Validate each workflow's selected credential in the UI before publish/activate; never update n8n credential metadata tables directly or use decrypted credential exports.

Numeric user/chat allowlists are non-secret but personal runtime configuration. Enter them manually into the deterministic normalization/authorization node after import, and scrub them from exported JSON/evidence. Because node environment access is blocked, this foundation does not pretend the allowlists are read from `.env`.
