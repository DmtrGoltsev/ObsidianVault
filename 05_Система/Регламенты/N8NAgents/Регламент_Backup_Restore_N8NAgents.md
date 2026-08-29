---
id: "regulation-n8nagents-backup-restore"
тип: "регламент"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/runbook-backup-restore.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/runbook-backup-restore.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
source_status: "source runbook snapshot requiring revalidation before operational use"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

# Signed encrypted backup and isolated restore

## Required custody and remote policy

The VPS holds the public age recipient and a dedicated minisign signing private key mode `0400/0600`. The age private identity and pinned minisign public key stay off-host in independent custody. A server compromise can misuse the signing key, so signing proves archive provenance/tamper resistance in transit and storage, not that a compromised source produced truthful data.

The remote destination must have provider-enforced versioning plus retention/object-lock or equivalent immutability. Set `BACKUP_REMOTE_IMMUTABILITY_CONFIRMED=yes` only after manual policy evidence; `rclone --immutable` is an additional no-overwrite guard, not a substitute. Remote retention/deletion is never automated by this repository and requires a separate approved provider policy.

## Coherent backup

`backup.sh` acquires a nonblocking exclusive `flock`, records whether n8n/Caddy were running, sets restoration intent before each stop attempt, requires each requested stop command to succeed, and verifies both services are absent from the running set before any dump/archive. Its cleanup idempotently restores every service that was initially running, including after a partial/nonzero stop. It then dumps `n8n_metadata` and `assistant_app` while application/file writes are quiesced and snapshots n8n/files/Caddy volumes, server `.env`, contracts, migrations, scripts and workflow exports.

Docker bind sources use only `/var/lib/n8nagents-backup/staging`, created and validated mode `0700`; `/tmp` and systemd `PrivateTmp` are never used as helper-container bind sources. The systemd unit grants this host-visible root explicitly in `ReadWritePaths`. A BOM captures schema version and actual n8n/PostgreSQL/Caddy/helper image digests. The internal manifest hashes every captured file.

The archive is age-encrypted, the encrypted bytes are minisign-signed with a separate server-only key, and the encrypted checksum/signature/archive are immutable-uploaded. A trap restarts exactly the services that were running on every exit path. After a successful upload, local cleanup deletes only matching backup artifacts older than the approved positive retention count inside the explicit non-root backup directory.

Install the supplied service/timer only after reviewing paths and creating protected `.env.backup`. Journaling is local. `OnFailure` calls a placeholder that records only the unit name; external notification destination/credential/data policy remain manually gated.

## Authenticated restore

1. Use a dedicated host/project and new directory; never production volumes/domains/project name.
2. Retrieve `.tar.age`, `.sha256` and `.minisig` through an independent path.
3. `restore-prepare.sh` verifies the detached signature using the pinned public-key file **before** checksum, decryption or extraction. It then verifies the signed internal manifest.
4. Run the tamper-negative script on a disposable copy; appended bytes must be rejected before decrypt/extract.
5. Run `restore-isolated.sh` with project prefix `n8nagents_restore_` and confirmation `ISOLATED_POSTGRES_ONLY`. It uses Compose/migrations and exact pullable image digests from the authenticated BOM.
6. The restore publishes no ports, has an internal-only network, restores databases/volumes, reapplies DB boundary grants, and leaves only PostgreSQL running. No schedules, webhooks, Caddy or n8n main process start.
7. Credential-decryption verification is `BLOCKED-EXTERNAL` until n8n documents a supported non-export verification method. Decrypted credential export is prohibited, including to tmpfs or `/dev/null`.
8. Record only signature/checksum status, BOM digest references, schema sentinel, bounded row counts and grant results. Destruction of drill volumes requires explicit authorization.

Backup status remains `BLOCKED-EXTERNAL` until the schedule, immutable remote, failure journal, tamper rejection and isolated restore drill all pass.
