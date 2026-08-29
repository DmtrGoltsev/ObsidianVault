---
id: "source-n8nagents-compatibility-matrix-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/compatibility-matrix.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/compatibility-matrix.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source compatibility snapshot; current production claims require CURRENT_STATE evidence"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Compatibility matrix — initial pins and current evidence

Initial discovery and Phase A statuses below are retained as historical pre-deployment evidence. The current production facts are explicitly dated and linked; they do not retroactively turn every initial gate into PASS.

| Component / contract | Pin or fact | Status | Evidence / required gate |
|---|---|---|---|
| n8n Community | `docker.n8n.io/n8nio/n8n:2.36.7` | CURRENT PROD VERSION OBSERVED — 2026-08-29 | Production runtime digest **UNKNOWN — not independently reverified**. Local/test pin: `sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c`; this is not production `docker inspect` evidence. |
| PostgreSQL | `postgres:17.11-alpine3.24` | CURRENT PROD VERSION OBSERVED — 2026-08-29 | Production runtime digest **UNKNOWN — not independently reverified**. Local/parity pin: `sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73`; direct PG parity PASS is separate from production recall. |
| Caddy | `caddy:2.11.4-alpine` | CONFIRMED tag | Resolve digest and validate Caddyfile with this image before deployment. |
| Docker host | Engine `29.7.2`, Compose `5.5.0` | CANDIDATES ONLY | A2 confirms both absent on Ubuntu 26.04. Phase A stops unless the official Docker apt repository offers both exact candidates for the discovered architecture. |
| n8n runner | Must exactly match `2.36.7` | UNVERIFIED / OMITTED | Exact registry tag/digest was not confirmed. No runner service is present. External runner is a post-spike hardening gate. |
| AI Agent node | `@n8n/n8n-nodes-langchain.agent`, type version `3.1` | TYPE CONFIRMED | Exact exported parameter contract and DeepSeek V4 behavior require import/live spike. |
| DeepSeek model node | `@n8n/n8n-nodes-langchain.lmChatDeepSeek`, type version `1` | TYPE CONFIRMED | Native node defaults are legacy-sensitive; V4 `reasoning_content` preservation is UNVERIFIED. |
| Workflow tool node | `@n8n/n8n-nodes-langchain.toolWorkflow`, type version `2.2`, display name `Call n8n Sub-Workflow Tool` | TYPE CONFIRMED | Must pass two sequential tool calls plus timeout/malformed/tool-result cases. |
| Sub-workflow nodes | `n8n-nodes-base.executeWorkflow`, `n8n-nodes-base.executeWorkflowTrigger` | TYPES CONFIRMED | Exact parameter/export contract is a live import gate. |
| PostgreSQL Chat Memory | `@n8n/n8n-nodes-langchain.memoryPostgresChat`, type version `1.4` | SCOPED PASS | Production single-session A/B recall PASS; direct PostgreSQL 17.11 DDL/add/get/clear parity PASS. Restart persistence and two-session isolation are **UNKNOWN — not tested**. Exact custom-key parameters and mandatory `ai_memory` edge are pinned in the credential-free workflow contract. |
| DeepSeek models | `deepseek-v4-flash`, `deepseek-v4-pro` | CONFIRMED API model names | Tools, JSON and thinking are supported by the API; n8n native-node compatibility remains a required live spike. |
| Telegram webhook auth | `secret_token` → `X-Telegram-Bot-Api-Secret-Token`; `allowed_updates=["message"]` | CONFIRMED | Exact header comparison and numeric allowlists must happen before LLM, DB and tools. [Telegram setWebhook](https://core.telegram.org/bots/api#setwebhook). |
| Caddy route | exact `POST /webhook/telegram-assistant`; fallback `404` | CONFIGURED | `/foo/*` wildcard semantics are intentionally avoided. Validate with pinned Caddy image. [Caddy request matchers](https://caddyserver.com/docs/caddyfile/matchers). |
| Secret files | production `.env` mode `0600` | DESIGN | n8n `_FILE` support is inconsistent/UNVERIFIED; this design does not claim it. |

## n8n hardening choices

The Compose draft explicitly enables SSRF protection, blocks environment access in nodes, restricts file access, disables community packages/public API/Swagger, excludes command/filesystem nodes, and enables execution pruning. Environment names must be rechecked against the exact 2.36.7 container during the local compatibility gate. No model-facing generic SQL, shell, filesystem, arbitrary code, credential, Docker, administration, or unrestricted HTTP tool is designed.

## DeepSeek decision gate

The 2026-08-29 acceptance proves the active single-session native chat/memory path only. It does not prove the full DeepSeek V4 flash/pro, thinking, sequential-tool, timeout, malformed-response, or fallback matrix described here. Those unexecuted cases remain gates for any claim that depends on them. If a native-node case fails, the only pre-approved design fallback remains a deterministic HTTP request with thinking disabled, strict response JSON Schema validation, an allowlisted intent switch, and Execute Sub-workflow. A custom agent loop or gateway needs separate approval.

Sanitized current-production evidence: [[Доказательство_Production_Acceptance_N8NAgents_20260829|production-memory-acceptance-2026-08-29.md]].
