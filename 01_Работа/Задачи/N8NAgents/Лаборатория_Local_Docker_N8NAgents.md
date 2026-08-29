---
id: "task-n8nagents-local-docker-lab"
тип: "задача"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents local/README.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "local/README.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
source_snapshot: "untracked working-tree source document at import"
source_file_sha256: "5b8fd8ff8c9860a42c349499eb34b2d1eb6b8204ce3635490257931126d3e66f"
imported_date: "2026-08-29"
source_status: "local laboratory source snapshot; never production evidence"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# N8NAgents local Docker laboratory

This directory is the permanent Plan A laboratory. It is isolated from the VPS
delivery files and preserves every pre-existing dirty path in the repository.

## Readiness milestones

- `LOCAL_CORE_READY`: PostgreSQL and n8n are healthy, n8n is reachable only at
  `http://127.0.0.1:5678`, PostgreSQL has no host port, and the named volumes
  preserve a synthetic record across `stop`/`start` or `down`/`up`.
- `TELEGRAM_LOCAL_READY`: the Docker mock test passes. A real dev/test bot is a
  later owner-gated check and does not block `LOCAL_CORE_READY`.

Neither milestone means production readiness. DeepSeek, Caddy, public webhooks,
DNS and VPS actions are out of scope here.

## First use

Open PowerShell in the repository root:

```powershell
./local/n8nagents-local.ps1 init
./local/n8nagents-local.ps1 preflight
./local/n8nagents-local.ps1 render
./local/n8nagents-local.ps1 start
./local/n8nagents-local.ps1 status
./local/n8nagents-local.ps1 mock-test
```

`init` creates ignored local secret leaves and leaves Telegram disarmed. `start`
starts core plus mock services; it never starts the real Telegram profile.
`render` displays paths and placeholders, never secret values. The first Docker
run may pull the two existing project pins:

- `postgres:17.11-alpine3.24`
- `docker.n8n.io/n8nio/n8n:2.36.7`

The stack publishes exactly one port: `127.0.0.1:5678`, through a fixed-upstream
loopback proxy. n8n itself remains attached only to internal Docker networks.
The host PostgreSQL on 5432 is deliberately untouched. `stop` performs Compose
`down` without `-v`, so named volumes are preserved.

## Static tests without Docker

```powershell
./local/tests/run-static.ps1
```

These tests need only the already installed local Node.js and Python runtimes.
They do not use Docker or the network.

## Real dev/test Telegram profile

The real profile is intentionally inactive. It uses the same bridge source and
same pinned runtime image as mock mode, but has no host port and is unavailable
to `start`/`mock-test`.

After a separate owner gate, write the dev/test token and numeric allowlists
directly into these ignored files without passing values in the command line:

```text
local/secrets/telegram_bot_token
local/secrets/telegram_allowed_user_ids
local/secrets/telegram_allowed_chat_ids
```

Then arm and start explicitly:

```powershell
./local/n8nagents-local.ps1 arm-real -AllowRealTelegram
./local/n8nagents-local.ps1 start-real -AllowRealTelegram
```

The bridge accepts only the canonical Telegram API origin, both numeric
allowlists, the fixed internal n8n URL and a persistent maximum of 20 outbound
messages. It does not retry an ambiguous send. To stop and revoke the local arm
marker:

```powershell
./local/n8nagents-local.ps1 disarm-real
```

Arming is not proof that the bot or n8n workflow is correctly configured. Never
use a production token in this laboratory.

## Persistence check and rollback

Create a synthetic n8n workflow or test database record, then run `stop`,
`start`, and verify it remains. Do not use `docker compose down --volumes`.

Rollback is non-destructive: run `stop` and leave named volumes intact. Deleting
containers, images, volumes, Docker Desktop data or Windows/WSL components is a
separate destructive action and is not part of this runbook.
