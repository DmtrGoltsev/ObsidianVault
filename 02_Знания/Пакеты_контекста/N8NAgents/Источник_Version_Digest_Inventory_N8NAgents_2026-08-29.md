---
id: "source-n8nagents-version-digest-inventory-20260829"
тип: "источник"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/version-digest-inventory.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/version-digest-inventory.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source/local parity inventory; production image digests are UNKNOWN"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>
> Production image digests remain **UNKNOWN**. Exact values in this source snapshot are LOCAL/PARITY PINS only.


# Version and digest inventory

| Artifact | Exact tag | Local/test digest pin | Initial draft status | Current production status on 2026-08-29 |
|---|---|---|---|---|
| n8n | `docker.n8n.io/n8nio/n8n:2.36.7` | `sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c` | digest had to be resolved before initial deployment | tag/version observed; production runtime digest **UNKNOWN — not independently reverified** |
| PostgreSQL | `postgres:17.11-alpine3.24` | `sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73` | digest had to be resolved before initial deployment | tag/version observed; production runtime digest **UNKNOWN — not independently reverified** |
| Caddy | `caddy:2.11.4-alpine` | not recorded in the memory acceptance artifact | initially deferred until the public-edge gate | production exists, but this acceptance does not claim an immutable Caddy digest |
| Backup helper | no default | required `image@sha256:...` server input | backup refuses a tag-only helper | outside memory-acceptance scope |
| n8n task runner | omitted | exact 2.36.7 tag/digest unverified | blocker against adding a mismatched runner | still omitted; not required by the accepted memory path |
| Docker host | Engine 29.7.2 / Compose 5.5.0 were initial candidates | n/a | A2 recorded them as absent | current host versions are outside this acceptance artifact |

The n8n and PostgreSQL digest values above are exact repository local/test inputs. They are not proof of the images running in production on 2026-08-29. The initial A2/Phase A wording is historical pre-deployment evidence. For any future release, independently resolve each approved tag, require a `RepoDigest`, record source/platform/UTC, bind `tag@sha256:digest` in protected server configuration, and rerun Compose/health checks. Never silently replace a production pin. The memory acceptance artifact does not promote unknown production digests, Caddy, backup-helper, runner, or host-version facts to PASS.
