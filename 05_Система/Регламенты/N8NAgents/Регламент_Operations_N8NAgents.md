---
id: "regulation-n8nagents-operations"
тип: "регламент"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/runbook-operations.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/runbook-operations.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source operations runbook snapshot; CURRENT_STATE wins for runtime facts"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Operations runbook

## Daily checks

Use redacted commands: Compose service/health state, filesystem/volume capacity, certificate renewal status, PostgreSQL readiness, failed/dead-letter update/reminder counts and backup upload/checksum outcome. Avoid dumping environment, raw executions, message text or provider responses.

Both successful and failed execution payload persistence are configured `none`. Before activation, prove with success, validation failure, provider timeout and malformed-provider fixtures that stored execution records/logs contain no headers, bodies, prompts, tool arguments, provider bodies or tokens. Alerts carry only UTC time, service/workflow identifier, stable error code, bounded counts and correlation ID; external alert delivery remains manually gated.

For an incident, first stop new ingress by stopping only Caddy if needed; preserve n8n/PostgreSQL state. Capture UTC time, service states, stable error codes, counts and correlation IDs. Do not collect tokens, headers, prompt bodies, credentials or complete environment. Restore service in dependency order PostgreSQL → n8n → Caddy.

## Telegram webhook

Register only production HTTPS exact path, a separately generated `secret_token`, and `allowed_updates=["message"]`. The production bot token is entered in n8n Credentials/UI and must not be shared with test. Negative-test missing/wrong header and unknown user/chat before activation. Rotating a bot token or webhook secret is a coordinated downtime event: stop Caddy, update server-side credential/header secret, set webhook, negative/positive test, resume.

## DeepSeek

No model is activated until compatibility spike PASS. Record model name and thinking setting without API key. On timeout/malformed/tool-call regression, disable the main workflow or route to a safe static error; do not expose a generic HTTP tool or invent a model alias.

## Database maintenance

Migrations run only through reviewed files with a pre-migration encrypted backup and rollback/restore plan. Runtime credentials do not receive DDL. Memory retention is a separate approved cleanup operation; context window length is not retention. Vacuum/analyze and storage monitoring use database administration outside LLM reach.
