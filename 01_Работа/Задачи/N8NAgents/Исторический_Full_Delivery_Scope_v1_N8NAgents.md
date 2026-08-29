---
id: "source-n8nagents-full-delivery-scope-v1"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/full-delivery-scope-v1.txt @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/full-delivery-scope-v1.txt"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "historical authorization envelope; source machine-contract migration is separate"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Full Delivery Authorization Scope v1 — historical source

N8NAgents full delivery authorization scope v1

Baseline: 9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b.

Authorization is limited to independently reviewed, immutable-ledger-bound releases that preserve every packaging, network, secret-handling, rollback, manual approval, and phase gate in this repository. Delivery may progress through internal foundation, owner bootstrap, public edge, workflow and credential binding, backup and restore, and final verification only after the manual gate for that phase passes.

Telegram test traffic is authorized only to the single allowlisted test chat recorded by the operator at its manual gate. No production recipient, group, channel, contact, or unlisted chat is authorized. Before any live test, an operator must confirm the recipient, non-secret test data, expected message count, rollback path, and stop condition. Owner creation and 2FA, domain and DNS activation, provider firewall and IPv6 policy, credential entry, workflow activation, public webhook traffic, backup destination and restore, and final external exposure each retain their documented manual gates.

The authorization fixes plaintext 2 GiB swap, at most two retries per gate, a total DeepSeek test budget of five US dollars, and at most twenty Telegram test messages. A new recipient, a new data class, any production or personal data, or any spend or message above these limits requires separate explicit authorization before work continues.

Secret disclosure, destructive cleanup or deletion, payments outside the fixed test budget, firewall or IPv6 weakening, SSH weakening, unreviewed code, branch or wildcard releases, mutable release pointers, executor self-review, bypass of a manual gate, or traffic to a non-allowlisted recipient is excluded. Any scope expansion requires separate explicit authorization outside this envelope.
