---
id: "spec-n8nagents-00-import-compatibility-gate"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/specs/00-import-and-compatibility-gate.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/specs/00-import-and-compatibility-gate.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source specification snapshot; execute only under a new reviewed task"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Import and DeepSeek compatibility gate

## Exact target

- n8n `2.36.7` only.
- AI Agent: `@n8n/n8n-nodes-langchain.agent` v3.1.
- DeepSeek Chat Model: `@n8n/n8n-nodes-langchain.lmChatDeepSeek` v1.
- Call n8n Sub-Workflow Tool: `@n8n/n8n-nodes-langchain.toolWorkflow` v2.2.
- Execute Sub-workflow / Trigger: `n8n-nodes-base.executeWorkflow` and `n8n-nodes-base.executeWorkflowTrigger` with versions exported by the exact target.
- Postgres Chat Memory: `@n8n/n8n-nodes-langchain.memoryPostgresChat` v1.4.

## PASS evidence

1. Import into a clean disposable 2.36.7 project produces zero unknown nodes, missing parameters or implicit credential IDs.
2. Native DeepSeek node is tested with `deepseek-v4-flash` and `deepseek-v4-pro`, thinking disabled and enabled where supported.
3. One agent makes at least two sequential calls to a harmless echo/fixture sub-workflow; input and result are captured with secrets/prompt content redacted.
4. Test success, timeout, malformed response, rejected tool input and valid tool result.
5. Confirm whether `reasoning_content` is preserved correctly. If not, native path is FAIL.
6. Postgres Chat Memory reads/writes the precreated table, survives restart and isolates two session keys. Its exact LangChain initialization requires `CREATE TABLE IF NOT EXISTS`, so `memory_runtime` has `CREATE` only on `memory`; `search_path` remains exactly `memory, pg_catalog` and no `public` fallback is allowed.
7. Export, scrub credential references, re-import into a second clean 2.36.7 instance and repeat a smoke run.

## Fallback

On native-node failure, use only: HTTP Request to the configured DeepSeek base URL, thinking disabled, a strict JSON response schema, deterministic validation/switch over the six allowlisted intents, then Execute Sub-workflow. The model output cannot choose a workflow ID, URL, credential, actor, chat or destination. A custom agent loop is out of scope.
