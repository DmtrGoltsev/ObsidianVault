---
id: "task-n8nagents-historical-manual-inputs"
тип: "задача"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/manual-inputs.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/manual-inputs.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "historical pre-production input queue; current scope is in CURRENT_STATE"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Manual and external inputs

No secrets belong in this file, chat, Git or evidence.

| Priority | Input / action | Current state |
|---|---|---|
| P0 | Redacted VPS discovery | `PASS` after reboot; see `server-discovery.md` |
| P0 | Publish approved plan envelope `N8NAgents-FULL-DELIVERY-v1` once as root-owned immutable mode `0400`: exact scope hash, plaintext 2 GiB swap, max 2 retries/gate, USD 5 DeepSeek test budget, 20 Telegram test messages | AUTHORIZED-IN-CHAT; RECORD-AT-EXECUTION |
| P0 | Record distinct safe `IMPLEMENTER_ID`/`REVIEWER_ID`; independent reviewer supplies the canonical exact-release artifact with `REVIEW_STATUS=GO` and its SHA-256, then publish immutable artifact and bound ledger before activation | REQUIRED-PER-RELEASE |
| P0 | Fresh provider-console recovery test and verified client authorization-key fingerprint before Phase A | WAITING |
| P0 | Server SSH host key accepted/pinned by user under TOFU; no independent verification claimed | USER-ACCEPTED-TOFU |
| P0 | Exact `amd64`/`x86_64` platform plus official Docker 29.7.2/Compose 5.5.0 apt candidates | WAITING-PREFLIGHT |
| P0 | Acknowledge plaintext 2 GiB swap confidentiality risk fixed by the approved envelope; any change requires separate authorization | APPROVED-PLAINTEXT-2G |
| P1 | Phase A n8n/PostgreSQL image digests for target platform | WAITING-PREFLIGHT |
| P1 | Editor/webhook domains, DNS provider/readiness and ACME email | DEFERRED-PUBLIC-EDGE |
| P1 | Separate dev/prod Telegram bots, non-secret usernames and numeric allowed IDs; tokens entered only in server credentials | WAITING |
| P1 | Manually confirm the single allowlisted Telegram test chat, non-secret test data class, message count, rollback and stop condition; new recipient/data class or extra spend/messages needs new authorization | WAITING |
| P1 | DeepSeek base URL/model choice after spike; API key entered only in server credential | WAITING |
| P1 | n8n owner account, 2FA and credential bindings | WAITING |
| P1 | Backup destination, public age recipient, separate minisign key custody/pinned public key, immutable+versioned remote policy, retention/RPO/RTO and isolated restore host | WAITING |
| P1 | Localhost-only owner bootstrap over SSH tunnel; owner+2FA evidence before public Caddy GO | PHASE-A-GATE |
| P2 | Provider firewall and IPv6 policy (not changed/needed for loopback-only Phase A; mandatory before public edge), editor access policy and downtime window | DEFERRED-PUBLIC-EDGE |
| P2 | Final E2E, persistence, fault, external exposure and restore evidence | WAITING |
