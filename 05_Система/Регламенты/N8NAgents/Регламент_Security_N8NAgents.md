---
id: "regulation-n8nagents-security"
тип: "регламент"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/runbook-security.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/runbook-security.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source security runbook snapshot; destructive actions still require fresh authority"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Security runbook

## Pre-activation checklist

- Exact image digests, n8n 2.36.7 env names and node contracts verified.
- Only Caddy publishes 80/443; external IPv4 and IPv6 scans confirm no 5678/5432/Docker API.
- Editor was first exposed only on `127.0.0.1:5678` through an SSH tunnel; owner and 2FA were verified before starting public Caddy. Access proxy/VPN/IP policy is recorded.
- Public API/Swagger/community packages disabled; SSRF enabled; env/file access and node exclusions verified by a redacted n8n security audit.
- Missing/wrong Telegram secret and unknown IDs terminate before DB/LLM/tool calls.
- Credential and secret scans clean; successful chat executions are not retained.
- PostgreSQL role/grant tests and backup/isolated restore PASS.
- Error and success fixture runs prove execution storage/logs contain no request headers/body, prompts, tool arguments, provider payloads or credentials.

## Secret response

If a token/key/password appears in Git, logs, exports, screenshots or chat: stop affected ingress/workflows; revoke/rotate at the issuer; rotate dependent credentials; remove the exposed artifact from active systems; investigate access and backups; document only secret type, time window and rotation status. Do not repeat the value. Git history rewriting and backup deletion are destructive, separately approved actions.

`N8N_ENCRYPTION_KEY` is not routine-rotated independently: it must remain paired with the metadata database and encrypted backups. A planned rotation requires supported n8n credential re-encryption/migration evidence and a restore drill.

## SSRF and capability regression

After every n8n update, prove metadata (`169.254.169.254` and IPv6 equivalent), loopback, link-local and disallowed private targets are blocked, while only explicitly required Telegram/DeepSeek/PostgreSQL destinations work. Confirm excluded command/filesystem nodes remain unavailable and no community node is installed. Model-facing arbitrary URL/SQL/shell/filesystem/code/admin capabilities are a release blocker.
