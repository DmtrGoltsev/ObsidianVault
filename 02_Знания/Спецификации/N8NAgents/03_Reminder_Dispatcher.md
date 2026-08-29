---
id: "spec-n8nagents-03-reminder-dispatcher"
тип: "спецификация"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents workflows/specs/03-reminder-dispatcher.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "workflows/specs/03-reminder-dispatcher.md"
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

# `reminder_dispatcher`

Run on a bounded schedule only after Phase A passes. In one short transaction, select due `scheduled|failed` rows with attempts remaining using `FOR UPDATE SKIP LOCKED`, mark a bounded batch `claimed`, assign a unique lease and commit. Never keep the transaction open during Telegram calls.

For each claim, send to its stored trusted chat, without parse mode. On definitive success, store the Telegram message ID and mark `sent`. On definitive retryable failure, increment attempts, calculate bounded exponential backoff with jitter, clear lease and mark `failed`; after maximum attempts mark `dead_letter`. On timeout/connection loss after request transmission, mark `delivery_uncertain=true`, audit `uncertain` and require a conservative recovery policy; do not blindly duplicate-send.

Concurrency tests require two dispatchers claiming the same fixture set, zero double claims, lease expiry recovery, bounded retries, dead-letter transition and an ambiguous-send fixture. This provides effectively-once for tested cases, not a global exactly-once guarantee.
