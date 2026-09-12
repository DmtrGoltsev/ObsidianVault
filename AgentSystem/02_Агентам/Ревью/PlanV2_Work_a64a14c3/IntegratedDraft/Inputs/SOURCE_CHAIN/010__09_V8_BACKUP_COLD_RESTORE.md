---
id: "n8nagents-plan-v2-v8-backup-cold-restore-a64a14c3"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V8 database backup/cold restore architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[02_V1_WINDOWS_CONTROL_PLANE]]"
  - "[[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]"
  - "[[04_V3_RESOURCE_STORAGE_BOUNDARY]]"
  - "[[05_V4_ISOLATION_NETWORK_EXPOSURE]]"
  - "[[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]"
  - "[[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]"
  - "[[08_V7_SECRETS_PRIVACY_INCIDENT]]"
доказательства:
  - "[[00_FINDINGS_BASELINE]]"
  - "[[01_BASELINE_AUDIT]]"
теги: ["n8nagents", "plan-v2", "backup", "cold-restore", "postgresql", "n8n", "recovery", "draft"]
---

# V8 — database backup и независимый cold restore

## 0. Статус, область и запрет на runtime-утверждения

Этот документ проектирует backup/cold-restore часть будущего полного plan v2 для локальной постоянной лаборатории N8NAgents по строгому плану A: Docker Desktop с WSL 2 backend. Он не разрешает installation, download, Docker/Windows/VPS mutation, работу с секретами, repository write, запуск Telegram/DeepSeek или удаление данных.

Ни один backup, restore, ключ, tool, image, filesystem capability, RPO или RTO фактически не проверен. Exact tool versions/digests, Windows roots, volume identities, размеры, PostgreSQL/n8n compatibility и owner custody остаются `UNKNOWN` до соответствующих V1–V7 gates. Поэтому этот документ может закрыть только design gap; runtime disposition остаётся `PENDING` либо `BLOCKED_*`.

Область V8:

- единая граница согласованности generation и исчерпывающий writer quiesce;
- полный recoverable inventory PostgreSQL, n8n files/binary state и authoritative bridge state;
- authenticated streaming encryption без persistent plaintext;
- атомарные publication/catalog/retention semantics;
- независимая custody backup identity и `N8N_ENCRYPTION_KEY`;
- cold restore только в новый project/volumes, без live volumes, live secret root, egress и host ports;
- archive/path/UID/GID/mode safety;
- fault injection, RPO/RTO, upgrade restore-first и evidence.

V8 не владеет provenance tools/images, Windows ACL/BitLocker, Docker endpoint, network implementation, exact n8n trigger-disable feature, секретными значениями, production/VPS или destructive cleanup. Эти свойства потребляются только через frozen cross-domain hashes; отсутствие либо конфликт означает `BLOCKED_CONTRACT_DRIFT`, а не локальный fallback.

## 1. Непереговорные решения и реестр contracts

### 1.1. Непереговорные решения

1. Backup — logical/application backup, не копия Docker VHDX и не raw PostgreSQL data-directory archive.
2. Каждый backup имеет один immutable `generation_id`; bridge, n8n, migrations, UI/API и все другие writers полностью quiesced на всю capture window.
3. PostgreSQL остаётся единственным работающим state service; его network имеет exact members `{postgres, backup-runner}` и не имеет host port/uplink.
4. На persistent Windows или Docker storage никогда не появляется plaintext dump/archive/manifest. Plaintext существует только в bounded anonymous pipes/process memory и, где tool строго требует, в size-bounded nonpersistent tmpfs; tmpfs use отдельно указан в operation manifest.
5. Backup шифруется только recipient-based `age v1` X25519. Passphrase/scrypt mode, custom cryptography, OpenSSL `enc`, unauthenticated encryption и caller-supplied nonce/salt запрещены.
6. Один generation состоит из independently authenticated ciphertext components и encrypted internal manifest. Только internal manifest является authority состава; external catalog secret-free и обязан совпасть с ним после decryption.
7. `COMPLETE` не выдаётся только по exit code encryptor. Нужны полное закрытие всех streams, hash/format checks, owner proof-of-possession backup identity, current independent n8n-key custody attestation и no-write decrypt/authentication pass.
8. `RESTORE_VERIFIED` выставляет только отдельный cold-restore run; backup writer не может self-assert restore.
9. Restore никогда не использует source/live volumes, live secret root, current runtime secret files, existing project object или provider credential. Нужные ключи подаются из независимой owner custody раздельными non-echo ceremonies.
10. Restore создаёт только новый cryptographic-nonce project и пустые project-scoped volumes. Collision/foreign label/nonempty object блокирует до первой target write; auto-adopt и overwrite отсутствуют.
11. Restore сначала полностью аутентифицирует и валидирует backup без target writes, затем выполняет отдельный decrypt pass в fresh target.
12. Старый n8n/PostgreSQL никогда не запускается на forward-migrated data. Upgrade сначала репетируется как restore в clone; rollback восстанавливает pre-upgrade generation в другие fresh volumes.
13. Backup/restore не удаляют source, failed target, last-good generation или expired data автоматически. Любое material deletion — отдельный exact-target manual gate.
14. План B, отдельный WSL distro, VPS и production не являются recovery fallback V8.

### 1.2. Реестр contracts

| Contract | Обязательство |
|---|---|
| `V8-C01-OPERATION-IDENTITY` | Каждая backup/verify/restore mutation связана с exact local endpoint, execution lock, project, roots, tool/runtime locks и operation manifest. |
| `V8-C02-RECOVERABLE-BOM` | Все PostgreSQL databases/globals/grants/extensions, n8n directories/files/binary backend, bridge authority и exclusions имеют closed disposition. |
| `V8-C03-EPOCH-QUIESCE` | Один exclusive generation lock и исчерпывающий writer fence сохраняются на всей capture window. |
| `V8-C04-POSTGRES-CAPTURE` | Logical capture воспроизводит полный cluster/application authority без raw data-directory reuse и без password plaintext. |
| `V8-C05-FILE-BRIDGE-CAPTURE` | n8n file classes и PostgreSQL-authoritative bridge state связаны тем же epoch; recreatable cache явно исключён. |
| `V8-C06-AGE-AEAD-STREAM` | Exact age/X25519 authenticated streaming pipeline записывает только ciphertext; nonce/salt/key schedule не переопределяются. |
| `V8-C07-KEY-CUSTODY` | Backup identity и n8n instance key имеют разные IDs, live locations и independently recoverable owner custody. |
| `V8-C08-ATOMIC-COMPLETE-RETENTION` | Partial generation не selectable; COMPLETE публикуется crash-safe; retention защищает минимум и LKG. |
| `V8-C09-RESTORE-PREFLIGHT` | Auth, BOM, version/tool/key/disk/target/source-deny checks завершаются до target write. |
| `V8-C10-SAFE-RESTORE` | Restore в new volumes rejects archive escapes/unsafe metadata и восстанавливает DB/permissions/files/key semantics. |
| `V8-C11-RESTORE-ISOLATION` | Restore имеет internal-only exact peer graph, zero host ports/provider secrets/triggers/egress и source/live-root deny. |
| `V8-C12-FAULT-RECOVERY` | Interruption/corruption/wrong key/disk-full/collision/compatibility faults fail closed без source/last-good damage. |
| `V8-C13-RPO-RTO-POLICY` | Cadence, age, measured RPO/RTO, retention и uncovered failures owner-approved и visible в status. |
| `V8-C14-UPGRADE-RESTORE-FIRST` | Любая schema/major update зависит от pre-upgrade COMPLETE+RESTORE_VERIFIED generation и clone promotion. |
| `V8-C15-EVIDENCE-RESULT` | Trusted collector выпускает content-addressed secret-free evidence; stable status/RC не допускают false PASS. |

## 2. Immutable records и canonical identity

До первой mutation V8 получает frozen records и создаёт только secret-free operation records. Canonical JSON: RFC 8785/JCS, UTF-8 без BOM, ordinal case-sensitive identifiers, SHA-256; duplicate/unknown required fields запрещены.

### 2.1. `backup_operation_lock/v2`

```yaml
schema: n8nagents.backup-operation-lock/v2
plan_sha256: <exact-full-plan-v2>
authority_id: <opaque>
execution_lock_sha256: <V1>
approved_endpoint_sha256: <V1>
source_project: n8nagents-local
source_project_object_set_sha256: <V4/V5>
root_policy_sha256: <V3>
resource_policy_sha256: <V3>
supply_chain_runtime_lock_sha256: <V2>
compose_db_n8n_lock_sha256: <V5>
telegram_state_contract_sha256: <V6>
secret_key_contract_sha256: <V7-frozen-secret-registry-and-key-binding>
backup_policy_sha256: <V8-C13>
operation_manifest_sha256: <exact-argv/process/pipe/write-set>
generation_id: <128-bit-CSPRNG-lower-hex>
created_utc: <RFC3339-UTC>
expires_utc: <RFC3339-UTC>
```

`generation_id` never derives from timestamp, counter, project name or secret. Reuse anywhere in catalog/stage/quarantine/complete/control DB returns `V8_BLOCKED_COLLISION`. Every V1 local-daemon guard is repeated immediately before Docker mutation; any endpoint/context/env/project drift invalidates lock.

### 2.2. `backup_internal_manifest/v2`

Internal manifest is encrypted as the last component and contains:

- `generation_id`, backup epoch start/end and source project/object-set identities;
- exact plan, authority, operation, endpoint, Desktop/Engine/Compose/kernel/storage-driver/runtime hashes;
- complete V2 image/tool BOM: OCI index/`linux/amd64` child/config/layer digests for PostgreSQL, n8n and every backup/restore/validator image; exact executable hashes and feature probes for `pg_dump`, `pg_dumpall`, `pg_restore`, `psql`, archive tool, `age`, canonicalizer and collector;
- V5 database/schema/migration/role lock and n8n config/workflow/key-ID/UID/GID locks;
- V6 bridge schema, arm/disarm, cap/offset/inbox/outbox/route consistency marker and data-retention classification;
- one record per component: logical ID, media type/format version, ciphertext filename, ciphertext bytes/SHA-256, plaintext stream bytes/SHA-256, capture process statuses, expected restore destination and semantic validator;
- database census, role/membership/grant/owner/default-ACL inventory hashes, extension/collation/encoding/locale inventory and schema migration versions;
- file inventory counts/bytes/types/UID/GID/modes and canonical path-tree hash;
- n8n instance-key ID, age recipient ID and independent custody attestation IDs, never raw material;
- declared exclusions and rationale;
- source data classification, generation `expires_utc`, RPO reference and logical/uncompressed restore size bounds.

Manifest cannot list itself. External `catalog.json` binds the ciphertext hash/bytes of encrypted manifest and duplicates only secret-free selection fields. On restore, decrypted manifest must equal those external fields; mismatch is integrity failure.

## 3. `V8-C02` — complete recoverable inventory

### 3.1. PostgreSQL census

Immediately after quiesce and before capture, the pinned same-major client records every `pg_database` row and chooses exactly one disposition:

| Class | Required disposition |
|---|---|
| Every non-template/connectable database, including `postgres`, `n8n`, `n8nagents_app`, `n8nagents_control` and any discovered extra | `DUMP_PRESENT`; unknown extra blocks rather than silent omission |
| `template0`, `template1` | `RECREATED_FROM_EXACT_POSTGRES_IMAGE`; encoding/locale/provider/collation flags still inventoried |
| Unconnectable/disallowed database | `BLOCKED_UNKNOWN` unless explicitly declared by V5 and recoverability procedure exists |

For every dumped DB manifest includes database owner/config, encoding/collation/ctype/locale provider, schemas, extensions+versions, large-object count/hash inventory, object owner/grant/default-ACL/row-security summary and migration history hash. No schema/table selection is allowed: full-database dumps only.

Cluster globals include every role, attributes, memberships, database grants, tablespace declaration and per-role/per-database settings. Plan A forbids custom tablespaces; discovery of one blocks. Password verifiers are intentionally absent from logical backup and represented as `RESEED_FROM_INDEPENDENT_SECRET_CUSTODY`; restore rotates login passwords before application start.

### 3.2. n8n and application census

Required classes:

| Logical component | Authority | Backup disposition |
|---|---|---|
| n8n metadata/workflows/encrypted credentials | PostgreSQL database `n8n` | full custom-format DB dump |
| app/memory/bridge/control schemas | PostgreSQL DBs from V5 | full DB dump, no raw-table omission |
| `local_n8n_data` | project-scoped named volume | authenticated encrypted POSIX-pax stream |
| `local_n8n_files`/binary backend | exact V5 configured volume | `PRESENT` archive or runtime-proven `ABSENT` |
| bridge offset/inbox/outbox/route/cap/lease authority | PostgreSQL `bridge` schema | included in DB dump; semantic marker required |
| `local_bridge_state` | non-authoritative cache | `EXCLUDED_RECREATABLE`; never used for restore truth |
| custom/community nodes | prohibited by V2/V5 | runtime-proven `ABSENT`; otherwise backup blocks as scope drift |
| Compose/config/migrations/workflow exports | versioned V2/V5 LKG set | exact hashes/availability references; secret-free bytes need not duplicate backup |
| cache, container logs, evidence, writable layers | non-authoritative | `EXCLUDED` with retention/evidence disposition |

Unknown mount/volume/database/file authority, writable custom-node path or second bridge offset store blocks `COMPLETE`.

## 4. `V8-C03` — one epoch, exclusive lock and full writer quiesce

### 4.1. State machine

```text
IDLE
  -> PRECHECKED
  -> HOST_LOCKED
  -> DISARMING
  -> WRITERS_DRAINING
  -> DB_FENCED
  -> QUIESCED
  -> CAPTURING
  -> SEALED
  -> READY_OWNER_KEY_PROOF
  -> AUTH_VERIFIED
  -> COMPLETE
  -> RESTORE_VERIFIED

any pre-COMPLETE failure -> QUARANTINED
any restore failure      -> RESTORE_FAILED_ISOLATED
```

Only one transition writer owns a generation. Every transition is append-only and hash-chained in the protected control record. Resume revalidates all locks and observed states; it never assumes the previous writer fence still exists.

### 4.2. Exclusive lock

1. Acquire an OS-level exclusive no-share lock file in V3-qualified `LAB_CONTROL_ROOT`, keyed by endpoint+source project+backup root. A stale lock is not auto-broken: process/boot/operation identity must prove abandonment, otherwise `BLOCKED_LOCK`.
2. Verify generation ID absent from control DB, stage, quarantine, complete catalog and all Docker object labels.
3. Through V6 emergency-safe path atomically disarm real-dev, revoke poller lease/arm and verify no pending dispatch. Backup does not silently discard inbox/outbox state.
4. Drain and stop in order: Telegram/DeepSeek adapters and brokers, bridge, n8n main, any task runner/worker, mocks, migration/bootstrap jobs, retention/prune jobs and manual execution channel. All have bounded stop grace and `restart:no` for the transaction.
5. Remove the n8n loopback publication with the stopped application containers. Exact runtime object/network/process/socket inventory must show no remaining writer or provider path.
6. PostgreSQL remains running alone on an internal backup network. Start one pinned non-root backup-runner; exact network membership becomes `{postgres, backup-runner}` and host-published ports remain empty.
7. Backup-runner acquires one PostgreSQL advisory lock and inserts immutable generation/consistency marker in `n8nagents_control` in a committed transaction. V6 bridge consistency values are captured in the same marker transaction.
8. Verify no DB sessions except PostgreSQL internals and the single backup session, no prepared transaction, no recovery, no pending/dirty migration and no uncommitted application writer. Unknown session/application name/role blocks.
9. During capture a trusted watcher repeatedly checks DB sessions, Docker network members, source volume identity and writer process set. Any drift closes pipes, quarantines generation and does not continue.

`QUIESCED` means all declared writer paths are either stopped or technically denied and tested: UI/API/manual workflow, n8n main/task runner/worker, bridge poll/ACK/outbox, application/memory jobs, migrations/bootstrap, retention and direct runtime DB roles. Merely saying “n8n stopped” is insufficient.

### 4.3. Release/resume

After `SEALED` or failure, backup session closes, advisory lock releases and source remains stopped while postconditions are checked. Resuming the previous application mode is a separate V5 convergence operation with fresh V1–V6 guards. Real-dev never auto-rearms; owner must create a new V6 arm. Failure to prove release yields nonzero `V8_STOP_WRITER_FENCE_UNKNOWN` and no success claim.

## 5. `V8-C04/C05` — exact component capture

### 5.1. PostgreSQL logical format

All PostgreSQL tools come from one V2-locked helper image whose client major equals source server major and whose feature probes are in the manifest. Authentication uses a one-file read-only secret mount; password value is absent from argv/env/log/evidence. Connection is only over the internal backup network.

Required streams:

1. `postgres/globals.sql.age`: `pg_dumpall --globals-only --no-role-passwords --no-password`; plaintext is PostgreSQL SQL text, captured completely and later executed only with `psql --set ON_ERROR_STOP=on --single-transaction` where PostgreSQL syntax permits. The tool lock must prove exact flags for the selected major.
2. One `postgres/db-<ordinal>.pgdump.age` for every non-template database. Format is PostgreSQL custom archive (`pg_dump --format=custom --blobs --no-password`), no schema/table filters, no `--no-owner`, no `--no-acl`. Project databases use a restore contract that recreates exact DB owner/config; the pre-existing `postgres` maintenance DB uses an explicit existing-database branch.
3. `postgres/inventory.json.age`: canonical census/inventory and tool/server/cluster/system-identifier keyed references; no passwords or raw PII.

`--clean`, destructive target SQL and password verifiers are not part of source capture. Globals/DB order is recorded. Restore never applies dump into a nonempty/unknown cluster.

### 5.2. n8n volume archive format

Each present n8n volume is mounted read-only into a non-root V2-locked archive helper under the exact V4 backup mount manifest. Plaintext archive format is POSIX pax with:

- UTF-8 relative paths rooted under one fixed logical prefix;
- ordinal bytewise sorted entries and unique normalized names;
- numeric UID/GID and permission modes;
- regular files and directories only in v2;
- no absolute paths, `..`, empty/NUL names, Windows separators/drive/ADS syntax;
- no symlink, hardlink, FIFO, socket, block/character device, sparse extent, ACL/xattr/capability, setuid/setgid/sticky bit;
- per-entry and total size/count/depth/path-length bounds from encrypted manifest;
- every UID/GID exactly equals the V5 locked nonzero n8n identity; mismatch blocks capture instead of using root/chown repair.

If exact n8n image legitimately requires a forbidden entry class, V8 returns `BLOCKED_ARCHIVE_POLICY`; widening policy requires a new reviewed contract and canaries.

Archive plaintext flows directly `archiver stdout -> age stdin`; archive/listing is never written to disk. The archive helper mounts source read-only, has read-only rootfs, bounded tmpfs, `CapDrop=ALL`, no devices/socket/host bind and no external network.

### 5.3. Bridge consistency

PostgreSQL is the sole authority. Internal manifest binds:

- V6 environment/bot/authorization/classifier keyed refs;
- `next_offset`, highest terminal prefix, monotonic revision and checksum/MAC state;
- poller fence/arm state, which must be restored as `DISARMED/NO_ACTIVE_LEASE`;
- inbox/outbox terminal counts, cap/send ledger and immutable route consistency hash;
- generation marker from `n8nagents_control`.

Restore rejects a DB where offset advances past a nonterminal record, restored arm/lease appears active, route/cap generation differs or a second file offset exists. `local_bridge_state` is recreated empty.

## 6. `V8-C06` — authenticated streaming encryption

### 6.1. Format and tool

Mandatory format: canonical `age-encryption.org/v1` file format with exactly one approved X25519 recipient. Mandatory implementation: official `age` CLI, exact version/executable/image/config digest locked by V2 before use. Until V2 records the exact version, source/spec hash, signer/provenance, feature probes and OCI child digest, state is `V8_BLOCKED_TOOL`.

Cryptographic contract:

- a fresh CSPRNG file key and fresh ephemeral X25519 key are generated independently for every component;
- recipient wrapping uses X25519. For its stanza, `salt = ephemeral_public_key || recipient_public_key`; wrapping key is HKDF-SHA-256 over the X25519 shared secret with exact info `age-encryption.org/v1/X25519`; the 16-byte file key is wrapped by ChaCha20-Poly1305 with 12 zero nonce bytes and empty associated data, exactly per frozen age v1 specification;
- header MAC key is age v1 HKDF-SHA-256 from the file key with the specification-defined empty salt and info `header`; HMAC-SHA-256 authenticates the canonical header;
- payload begins with a fresh 16-byte CSPRNG nonce. Payload key is age v1 HKDF-SHA-256 from the file key with that nonce as salt and info `payload`; STREAM uses ChaCha20-Poly1305 chunks with the specification-defined 11-byte big-endian counter plus one-byte final flag as each 12-byte AEAD nonce;
- passphrase mode and its scrypt KDF are prohibited. The only KDF in approved mode is the age v1 HKDF-SHA-256 key schedule;
- caller never supplies, persists, derives, reuses or overrides file key, ephemeral key, nonce, salt, chunk counter or final flag;
- one recipient only in v2. Adding another recipient changes confidentiality/custody and requires a new owner-reviewed lock;
- custom parser/crypto, “compatible” implementation or fallback cipher is forbidden.

The exact frozen age v1 specification bytes/hash are a V2 source-evidence item. Implementation tests use official known-answer/tamper fixtures plus cross-version decrypt compatibility before tool acceptance; this draft does not claim those tests passed.

### 6.2. No-plaintext pipeline

For every component the trusted supervisor creates anonymous binary pipes without shell interpolation:

```text
producer stdout -> age stdin
age stdout       -> Windows CREATE_NEW <component>.partial
```

Producer and encryptor stderr go only through source-allowlisted redaction; neither stdout is attached to console/transcription. Pipe/process exit codes are checked independently; `pipefail` inferred from a shell is insufficient. A trusted in-container supervisor hashes the exact plaintext bytes while forwarding them from producer to age and emits only SHA-256/byte count through a separate fixed-schema control channel. Host writer calculates ciphertext SHA-256/bytes while writing, flushes and closes, then reopens by file identity and rehashes. No plaintext excerpt is retained.

On failure, only ciphertext `.partial` moves to `LAB_QUARANTINE_ROOT`; no plaintext cleanup claim is needed because none was persistently created. Unique plaintext canaries are scanned across approved Windows roots, Docker writable layers, temp, logs, evidence and process transcripts. Any occurrence is `V8_FAIL_PLAINTEXT`.

### 6.3. Authentication before COMPLETE and restore write

After encrypted manifest is sealed, owner provides the backup private identity from independent custody through non-echo/non-argv/non-clipboard input to a disposable verifier. It is held only in locked memory or bounded tmpfs secret file, wiped by process teardown without claiming physical secure erase.

Verifier performs a full decrypt-to-hash/null pass over every component, consumes the final age authentication tag, compares plaintext/ciphertext hashes and validates internal manifest/archive/database formats. It creates no target volume/file. Missing/wrong identity, bit flip, truncation, reordered/missing/extra component or manifest mismatch blocks `COMPLETE`.

Restore repeats this full no-write authentication pass before creating any target Docker object. Prior verification evidence cannot replace current ciphertext authentication.

## 7. `V8-C07` — separate key domains and owner custody

| Key class | Live use | Backup payload | Independent recovery |
|---|---|---|---|
| n8n instance key | Exact one-file live secret used only by n8n; stable V5/V7 key ID | Raw key excluded; encrypted DB contains credentials; manifest stores only key ID | Separate owner custody copy required; possession check before COMPLETE/cold restore |
| age X25519 recipient public key | Non-secret backup encryption input in control lock | Recipient ID in every age header/manifest | May be retained with config/manifest |
| age X25519 private identity | Never required for capture; not stored in backup root/VHDX/repo/Vault/evidence | Excluded | Owner custody independent from ciphertext and n8n key; temporarily entered for verify/restore only |
| PostgreSQL runtime/admin passwords | One-file exact consumer secrets | Password/verifier excluded; role structure retained | Recreated/rotated from separate owner ceremony before restored services start |
| Telegram/DeepSeek/bridge credentials | Not needed for restore | Excluded | Never mounted into restore; real-dev separately rebinds after restore acceptance |

Requirements:

1. `V7-S11 backup-AEAD-key` is specialized by V8 as the private X25519 age identity; it is not a caller-provided content-encryption key. Its public recipient is the only key input to capture. V7's per-operation ephemeral-file rule applies when the private identity is temporarily supplied for COMPLETE verification or restore. If canonical V7 retains a conflicting symmetric-key interpretation, V8 is `BLOCKED_CONTRACT_DRIFT`.
2. Backup private identity and n8n recovery key are two distinct generated secrets with different purpose/IDs/files and cannot be derived from one another.
3. Their independent custody locations/mediums, owner, creation, recovery test, rotation/revocation rule and loss consequence are approved in `MG-V8-KEY-CUSTODY`; raw locations/values are not in Vault/evidence.
4. Neither custody item may be protected solely by the other. A backup containing the n8n key or an n8n key file encrypted only inside the same backup is not independent recovery.
5. `COMPLETE` requires current owner proof-of-possession for both IDs. For n8n this is exactly the V7 purpose-separated HMAC key-ID challenge; for age it is successful manifest decryption. Raw values never leave the trusted local input/verifier boundary.
6. Loss of either item is terminally reported: ciphertext without age private identity is unreadable; DB without matching n8n key cannot recover credentials. Tooling never generates a replacement key and calls it recovery.
7. Rotation of the age recipient creates a successor generation; old generations remain decryptable only while their old custody identity is retained. Rotation of `N8N_ENCRYPTION_KEY` uses only an exact-version supported n8n migration or controlled credential revocation/recreation.

## 8. `V8-C08` — atomic publication, catalog and retention

### 8.1. Layout and publication

Logical roots are V3-owned and path-qualified. Exact raw paths remain local:

```text
LAB_CIPHERTEXT_STAGE_ROOT/<generation-id>/
LAB_QUARANTINE_ROOT/<generation-id>/
LAB_BACKUP_ROOT/generations/<generation-id>/
LAB_BACKUP_ROOT/catalog/<generation-id>.json
LAB_BACKUP_ROOT/catalog/COMPLETE-<generation-id>.json
```

All three roots reside on the same approved NTFS volume for same-volume atomic publication and have protected DACL. The generation directory is created exclusive. Each component is written `.partial`, flushed, closed, identity/hash-verified and atomically renamed inside stage. Encrypted internal manifest is last.

After owner key proof/full authentication:

1. stage directory inventory must equal internal manifest and operation write-set; extra/missing path blocks;
2. every handle is closed and ciphertext rehashed;
3. generation directory is atomically renamed into `generations/<id>` on the same volume;
4. secret-free catalog is written create-new, flushed and atomically published;
5. `COMPLETE-<id>.json` is create-new and published last with generation/catalog/manifest hashes and state `COMPLETE`;
6. only catalog entries with valid COMPLETE marker, exact hashes and successful manifest authentication are selectable.

Crash between any steps yields nonselectable orphan/partial state. Recovery scans and quarantines it by exact identity; it never manufactures COMPLETE. Reused ID, cross-volume rename, replace-existing, broad recursive move/delete and overwrite are forbidden.

`RESTORE_VERIFIED` is a successor catalog record referencing immutable COMPLETE generation and exact cold-restore evidence; it does not edit prior records.

### 8.2. Retention

Initial plan-v2 policy, pending owner `MG-V8-RPO-RETENTION`:

- backup after each credential, workflow, schema/migration, bridge-policy or key-ID change and before every update;
- at least one new COMPLETE generation per 7 calendar days of active use;
- warning when latest COMPLETE or RESTORE_VERIFIED is older than 7 days; real-dev blocked at 14 days;
- retain at least two `COMPLETE+RESTORE_VERIFIED` generations and every current pre-upgrade/LKG generation;
- byte cap must be at least `2 × largest restore-verified generation + one pre-upgrade generation + V3 peak margin`;
- a generation containing data with shorter V6 expiry inherits the earliest applicable `expires_utc`; expired sensitive generation cannot silently satisfy freshness;
- no generation is deleted automatically. Retention pressure blocks next growth and produces exact preview. Deleting last verified, sole decryptable, current pre-upgrade or legal/incident hold generation is forbidden without a named destructive gate.

Backup root outside Docker VHDX proves only L2 VHDX-loss readiness. If backup and keys remain on the same physical Windows disk/machine, host-loss DR remains explicitly uncovered.

## 9. `V8-C09/C10/C11` — cold restore

### 9.1. Pre-write gate

`lab restore-drill <generation-id>` performs zero target writes until all conditions below are `KNOWN_VALID`:

1. V1 explicit local endpoint/daemon/project guard and V2/V3/V4/V5/V6/V8 locks are current.
2. Generation ID is allowlisted, `COMPLETE`, nonexpired for the intended purpose and has no catalog/marker/path identity drift.
3. Owner supplies age private identity and n8n key from independent custody; live `LAB_SECRET_ROOT` is absent from environment, mounts and process permissions.
4. Every ciphertext SHA-256/size matches catalog. Full decrypt-to-null authentication and plaintext hashes match encrypted manifest before any Docker target object exists.
5. Tool/image/runtime/config/migration/extension/collation/locale compatibility is exact. Default restore uses recorded exact PostgreSQL major and n8n digest; an upgrade requires `V8-C14`.
6. V3 `G(restore)` includes new PostgreSQL+n8n volumes, decompressed logical sizes, image/LKG import, temporary target overhead, failure quarantine and non-consumable host reserve. Unknown or one-byte-under threshold blocks.
7. New project name is `n8nagents-restore-<128-bit-run-nonce>`. No object/name/label/run collision exists; target containers/networks/volumes are absent.
8. Operation mount denylist includes every source/live volume ID, Docker VHDX/root, live secret root, backup root as a directory, repo, Vault and foreign object. Ciphertexts enter verifier by allowlisted file handle/API stream, never broad root bind.
9. Exact restore Compose render has only `restore-postgres`, one-shot restore/validator services and optional trigger-disabled `restore-n8n`; only `restore_db internal:true`, zero host ports/uplink/provider services/secrets.
10. V5 provides a version-locked supported mechanism that prevents all active workflows/triggers/task runners on restored n8n before its first process. If not proven, DB/files restore may be structurally inspected but n8n start/credential check remains `V8_BLOCKED_TRIGGER_DISABLE` and no RESTORE_VERIFIED.

### 9.2. Safe target creation and archive extraction

After preflight, wrapper creates only fresh project-scoped named volumes with full plan/authority/generation/run/resource/disposable labels. Any pre-existing or nonempty target blocks; no `--force`, adopt or repair.

Each pax archive is authenticated again, then parsed by a V2-locked strict validator before extraction. Validator rejects:

- absolute, parent-traversal, empty/NUL, duplicate, noncanonical UTF-8, case/Unicode-alias, Windows drive/UNC/ADS or over-limit path;
- symlink/hardlink/device/FIFO/socket/sparse/xattr/ACL/capability/setuid/setgid/sticky entries;
- owner other than exact locked service UID/GID, unexpected executable mode, world/group write outside exact policy, size/count/depth mismatch;
- entry escaping fixed target prefix or any disagreement with encrypted path-tree inventory.

Extraction runs as the exact nonzero service UID/GID, `CapDrop=ALL`, `no-new-privileges`, read-only rootfs and only its new volume. It does not run `chown`, preserve host ACLs, follow links or write elsewhere. After extraction, a second tree inventory must equal manifest. If Docker volume semantics cannot preserve the required ownership/modes non-root, result is `V8_BLOCKED_CAPABILITY`; root helper is not a fallback.

### 9.3. PostgreSQL restore order

1. Initialize a fresh same-major cluster in a new empty volume under an ephemeral restore bootstrap admin; source data directory is never mounted/reused.
2. Verify exact cluster/image identity, locale/collation/encoding prerequisites and available extension binaries before applying logical data.
3. Decrypt/authenticate globals again and apply structural roles/memberships/settings with `ON_ERROR_STOP`; password verifiers remain absent. Ephemeral bootstrap identity is removed only after exact intended admin exists and postconditions pass.
4. Restore each database in manifest order with pinned `pg_restore`; create/owner/config behavior is explicit for project DBs and the existing `postgres` maintenance DB. No restore targets an unknown/nonempty database.
5. Recreate/rotate login-role passwords through restore-specific one-file secrets supplied independently, then run full V5 positive/negative permission, owner/grant/default-ACL/search-path/extension/schema/migration checks.
6. Validate DB, large-object, workflow, application/memory and V6 offset/inbox/outbox/route/cap canaries. Restored arm/lease must be disabled and bridge cache empty.
7. Failed/partial DB is labelled `RESTORE_FAILED_ISOLATED`, never retried in place and never exposed to application. Cleanup is a separate exact-target gate.

### 9.4. n8n semantic validation

Only after DB/files/permissions/key-ID/trigger-disable/no-egress gates pass may restore n8n start with `restart:no`, zero host ports and only internal DB network. Telegram/DeepSeek/bridge/brokers/mocks are absent; provider credentials are absent. Checks:

- exact PostgreSQL backend, regular topology, non-root UID/GID and expected file paths;
- workflow inventory and all workflows inactive/trigger-disabled;
- supported credential decryptability canary with escrowed matching n8n key, without plaintext export/direct metadata SQL;
- no SQLite, queue/Redis, task runner, custom/community node or provider attempt;
- immediate stop after bounded semantic check.

Any provider DNS/socket, active trigger, unexpected listener, secret mount or workflow execution is containment failure, not degraded PASS.

### 9.5. Recovery tiers

| Tier | V8 claim allowed after evidence |
|---|---|
| `L1_COLD_LOGICAL_RESTORE` | Same qualified Docker Desktop, but source containers/volumes and live secret root inaccessible to restore operation; full new-project semantic restore. |
| `L2_VHDX_LOSS_READY` | Backup and owner custody are outside source VHDX, LKG config/images available; actual VHDX loss is not simulated without destructive gate. |
| `L3_HOST_LOSS_DR` | Not in approved scope. Requires independently off-host backup+both key custodies and clean-host destructive/manual drill. |

L1/L2 cannot be described as full disaster recovery.

## 10. `V8-C12` — mandatory fault matrix

Every case has exact fixture/tool/image/operation hashes, expected RC, source/last-good invariance and zero-secret evidence. Integrity/auth/collision/disk failures have zero automatic retries.

### 10.1. Backup faults

- competing backup process, stale/live host lock, reused generation ID and stage/catalog name collision;
- failure after each state transition and after each component byte boundary, including producer nonzero, encryptor nonzero, broken pipe and collector failure;
- SIGTERM/SIGKILL/Docker stop/restart and approved reboot/power-loss simulation boundaries;
- disk-full at one byte below projected peak, mid-component and immediately before manifest/catalog/COMPLETE publish;
- permission/read failure, source volume identity/mode drift, new DB/session/network member/writer during capture;
- missing/extra database, extension, archive entry or bridge consistency marker;
- wrong age recipient, unavailable owner key proof, wrong n8n key ID, ciphertext bit flip, truncation, reorder, missing/extra component and altered external catalog/internal manifest;
- duplicate/case/Unicode path and unique plaintext canary.

Expected invariant: no invalid case reaches COMPLETE; source volumes and previous good generations remain unchanged; failed ciphertext is nonselectable quarantine only; writer state is either safely stopped or explicitly `STOP_WRITER_FENCE_UNKNOWN`.

### 10.2. Restore faults

- missing/wrong age identity or n8n key, key-ID mismatch and lost custody item;
- incompatible PostgreSQL/n8n/tool/image digest, unavailable extension/collation/locale and old image against migrated state;
- target project/volume collision, foreign/missing label, nonempty volume and source/live volume/root made visible;
- archive traversal, absolute/ADS/case/Unicode alias, symlink/hardlink/device/FIFO/socket, wrong UID/GID/mode and decompression-size overflow;
- disk-full before first write and after every PostgreSQL/file phase; PostgreSQL/restore-n8n crash and Docker restart;
- corrupted globals/DB/archive, failed grant/owner/migration check, inactive-trigger mechanism unavailable, restored active arm/lease or provider socket;
- evidence/catalog from another generation/run.

Expected invariant: preflight faults create zero target objects; post-write faults leave only labelled isolated failed target, never source mutation or network/port exposure; same clean generation can restore successfully into a new nonce target afterward.

## 11. `V8-C13` — RPO, RTO and owner policy

Initial measurable proposal:

| Objective | Proposal before measured owner acceptance |
|---|---|
| RPO | Event-based backup after every credential/workflow/schema/key/bridge-policy change and before update; otherwise no more than 7 calendar days of active use. |
| Freshness stop | Warning at 7 days; block `real-dev` at 14 days or when required changed-state generation is absent. |
| RTO-L1 | 60 minutes from qualified Docker availability and custody readiness to completed semantic cold restore. |
| RTO-L2 | `UNQUALIFIED` until a separately gated clean-Docker/VHDX-loss rehearsal; no promised duration. |
| Retention | Minimum two COMPLETE+RESTORE_VERIFIED plus every current pre-upgrade/LKG; no auto-delete; data-class expiry still enforced as status/block. |
| Owner | One named owner for backup cadence, custody checks, restore drill and retention decisions; agent may report but not self-approve keys/destruction. |

`MG-V8-RPO-RETENTION` approves exact values after first measured cold restore. Evidence records start/end for quiesce, capture, owner-key wait separately, preflight, data restore and semantic validation. Human waiting for a key does not hide technical restore duration; both elapsed values are reported.

If actual data loss or technical restore time exceeds approved objective, status is `V8_FAIL_RPO`/`V8_FAIL_RTO`; tooling does not revise target after the fact. Covered failures are logical corruption/loss of local project volumes and source VHDX unavailability readiness. Same-host physical disk loss, owner custody loss, provider account loss and Docker Desktop reinstall/downgrade are explicit residuals until separate drills.

## 12. `V8-C14` — upgrade restore-first recovery

Every Docker/n8n/PostgreSQL/config/schema/data-layout update consumes V2 `UPDATE_PENDING` and follows:

1. Current endpoint/runtime/data/key identities are exact and real-dev is disarmed.
2. Create a pre-upgrade generation after full quiesce; it must become COMPLETE and then RESTORE_VERIFIED on exact current versions.
3. Preserve exact current/LKG images, tools, Compose/config/migrations and custody IDs. V3 peak budget includes at least source + backup + clone + failure quarantine + host reserve.
4. Restore pre-upgrade generation into new clone volumes with no egress/ports/triggers; never clone by sharing or mutating live volume.
5. Verify authoritative from/to compatibility. n8n patch/minor migrations run only on clone. PostgreSQL major change uses exact supported logical dump/restore by default; raw data directory reuse is rejected.
6. Run DB/grant/extension/workflow/key/file/Telegram-state/mock/cold-restore regression and exact new runtime evidence.
7. Promotion is a separate owner gate with exact old/new object plan. Original volumes and pre-upgrade generation remain LKG until successor itself has a new successful backup+cold restore and owner retirement gate.
8. Failure never starts old binary on migrated data. Recovery restores pre-upgrade generation with matching old images/config/key into another fresh project/volume set. Source and failed clone remain preserved pending exact cleanup decision.

Docker Desktop itself cannot be restored or downgraded by V8; unavailable vendor-supported reinstall/downgrade remains `BLOCKED_PLATFORM_RECOVERY`, not an application rollback success.

## 13. Status, RC and manual gates

### 13.1. Stable result envelope

```yaml
schema: n8nagents.v8-backup-restore-result/v2
run_id: <uuid>
operation: BACKUP | VERIFY | RESTORE | STATUS | UPDATE_REHEARSAL
generation_id: <opaque-or-null>
source_project_ref: <pseudonymous>
target_project_ref: <pseudonymous-or-null>
operation_lock_sha256: <hash>
manifest_ciphertext_sha256: <hash-or-null>
runtime_lock_sha256: <hash>
state: <V8-enum>
decision: PASS | READY_FOR_MANUAL_GATE | BLOCKED | STOP | FAIL
rc: <integer>
mutation_started: <bool>
source_writers_state: <enum>
components: {expected, captured, authenticated, restored, validated}
keys: {age_recipient_id_state, n8n_key_id_state, custody_attestation_state}
resources: {preflight_state, projected_peak_bytes, reserve_state}
isolation: {source_deny, live_secret_deny, no_egress, zero_ports, triggers_disabled}
rpo_rto: {freshness_state, technical_elapsed_ms, objective_state}
failed_predicates: [<stable IDs>]
evidence_refs: [<EV-V8 IDs>]
next_safe_action: <one stable action ID>
```

Raw paths, usernames, SIDs, DB contents, IDs, keys, ciphertext plaintext, tokens and secret-bearing commands are absent.

### 13.2. RC namespace

| RC | State | Meaning |
|---:|---|---|
| `0` | `V8_COMPLETE_VERIFIED`, `V8_RESTORE_VERIFIED`, `V8_STATUS_HEALTHY` | Exact scoped result only; never overall project PASS. |
| `10` | `V8_READY_OWNER_GATE` | Exact owner decision/input required; no unauthorized next mutation. |
| `121` | `V8_BLOCKED_CONTRACT_DRIFT` | Required V1–V7/V8 lock missing/mismatched. |
| `122` | `V8_BLOCKED_ENDPOINT` | Local daemon/project/operation identity not exact. |
| `123` | `V8_BLOCKED_LOCK` | Concurrent/stale/ambiguous writer lock or generation collision. |
| `124` | `V8_BLOCKED_WRITER` | Full quiesce/session/network writer set not proven. |
| `125` | `V8_BLOCKED_INVENTORY` | DB/data/bridge/exclusion inventory incomplete. |
| `126` | `V8_BLOCKED_TOOL` | Exact tool/image/spec/feature/compatibility lock absent. |
| `127` | `V8_BLOCKED_KEY_CUSTODY` | Required independent key ID/possession/custody unavailable. |
| `128` | `V8_BLOCKED_DISK` | Peak/host reserve or retention capacity fails. |
| `129` | `V8_BLOCKED_TARGET` | Target/path/object/label/emptiness/archive policy fails before write. |
| `130` | `V8_BLOCKED_TRIGGER_DISABLE` | Safe offline n8n start cannot be proven. |
| `131` | `V8_BLOCKED_CAPABILITY` | Plan A cannot provide required non-root/filesystem/restore property. |
| `132` | `V8_BLOCKED_PLATFORM_RECOVERY` | Docker/VHDX/host recovery not supported/proven in scope. |
| `140` | `V8_FAIL_BACKUP` | Capture/publish failed; no COMPLETE. |
| `141` | `V8_FAIL_AUTH` | age authentication/wrong key/tamper/truncation failure. |
| `142` | `V8_FAIL_PLAINTEXT` | Plaintext marker found in prohibited persistent/log/evidence sink. |
| `143` | `V8_FAIL_RESTORE` | Target write began but semantic restore failed. |
| `144` | `V8_FAIL_CONTAINMENT` | Source/live-root/egress/port/trigger/path boundary violated. |
| `145` | `V8_FAIL_RPO` | Measured recoverable point exceeds approved target. |
| `146` | `V8_FAIL_RTO` | Measured technical restore duration exceeds approved target. |
| `147` | `V8_STOP_WRITER_FENCE_UNKNOWN` | Source resume/stop state cannot be proven after failure. |
| `150` | `V8_STOP_RESULT_INVALID` | Result/evidence/schema/RC contradiction or collector error. |

Unknown/missing field, child `PASS`, zero RC with failed predicate or stale evidence is `V8_STOP_RESULT_INVALID`.

### 13.3. Manual gates

| Gate | Before | Exact owner decision |
|---|---|---|
| `MG-V8-PLAN` | implementation/runtime | frozen full-plan v2 and integrated V8 hashes |
| `MG-V8-BACKUP-ROOT` | first ciphertext write | exact V3 root/volume/ACL/at-rest/failure-domain disposition |
| `MG-V8-KEY-CUSTODY` | first credential/backup COMPLETE | distinct n8n/age IDs, custody, loss/rotation/recovery consequences |
| `MG-V8-RPO-RETENTION` | active use/D10 | exact RPO/RTO/cadence/caps/minimum/expiry behavior |
| `MG-V8-OWNER-KEY-PROOF` | each COMPLETE/restore | non-echo temporary use of independent custody items; no secret value in gate record |
| `MG-V8-UPDATE-RESTORE-FIRST` | each data/schema/major update | from/to locks, pre-upgrade restore evidence, peak and rollback limits |
| `MG-V8-FAILED-TARGET-CLEANUP` | deletion of failed restore | exact project/object IDs/labels/hashes and no source/LKG overlap |
| `MG-V8-BACKUP-RETIRE` | deletion of any generation/key | exact generation/key dependencies and surviving verified restore set |
| `MG-V8-L2/L3-DRILL` | actual Docker data/VHDX/host unavailability | destructive scope, independent media, rebuild path and rollback limitations |

Plan approval cannot supply secret values, accept custody loss, delete a generation/volume or authorize VHDX/host destruction implicitly.

## 14. Acceptance tests, negative canaries and evidence

All rows are future obligations. Tests use synthetic canaries until separately approved real-secret/data gates. Every evidence record is schema-valid, secret-free, SHA-256-bound to exact locks and emitted by trusted collector, not backup/restore candidate text.

| ID | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `AT-V8-01` | Every operation uses exact V1 local endpoint/project/execution lock before/after each mutation. | `NC-V8-01`: `DOCKER_HOST/CONTEXT/TLS`, current-context change, remote sentinel or project substitution yields RC 122 before first API mutation. | `EV-V8-01-OPERATION-IDENTITY` guard/argv/lock hashes and zero-mutation attestation. |
| `AT-V8-02` | Full database/data/bridge census has one disposition per class and expected census hashes. | `NC-V8-02`: extra DB/volume/mount/offset store, missing extension or unknown custom node yields RC 125. | `EV-V8-02-RECOVERABLE-BOM` component/disposition/inventory hashes. |
| `AT-V8-03` | Concurrent write attempts through every declared writer fail while one epoch marker remains stable. | `NC-V8-03`: new DB session, restarted n8n/bridge/migration, second network member or reused generation aborts capture. | `EV-V8-03-EPOCH-QUIESCE` transition/session/network/writer ledger. |
| `AT-V8-04` | Fresh cluster restore recreates every DB, role/membership/owner/grant/default ACL/extension/large object and passes V5 permission tests. | `NC-V8-04`: omit one DB/global/ACL/extension, corrupt custom dump or expose role password; no COMPLETE/RESTORE_VERIFIED. | `EV-V8-04-POSTGRES` census, tool/server, dump and semantic hashes. |
| `AT-V8-05` | n8n data/files and PostgreSQL-authoritative bridge canaries restore under same generation; cache is recreated empty. | `NC-V8-05`: file/DB generation mismatch, second file offset, active restored lease/arm or orphan binary object blocks. | `EV-V8-05-N8N-BRIDGE` tree/semantic/consistency hashes. |
| `AT-V8-06` | Every producer streams directly through locked age; full decrypt-to-null/auth pass matches plaintext/ciphertext hashes. | `NC-V8-06`: wrong recipient/key, bit flip, truncate/reorder/extra/missing component, altered manifest/BOM gives RC 141. | `EV-V8-06-CRYPTO` age spec/tool/recipient refs, component hashes and auth results. |
| `AT-V8-07` | Unique plaintext markers appear only after authorized in-memory decryption and never in Windows/Docker persistent/temp/log/evidence sinks. | `NC-V8-07`: producer writes one plaintext temp/dump/archive or stdout transcript; RC 142 and no COMPLETE. | `EV-V8-07-NO-PLAINTEXT` sink inventory and marker absence counts, never marker values. |
| `AT-V8-08` | Owner independently proves possession of matching age and n8n keys; no live-root dependency. | `NC-V8-08`: missing/wrong/cross-generation key, same-file/same-derivation custody or live-root-only key blocks. | `EV-V8-08-KEY-CUSTODY` keyed IDs, attestation refs and proof outcomes only. |
| `AT-V8-09` | Interruption at every publish boundary produces either valid COMPLETE or nonselectable quarantine; two concurrent runs cannot share ID. | `NC-V8-09`: disk-full before marker, partial catalog, cross-volume rename, replace-existing and crash orphan never selectable. | `EV-V8-09-PUBLICATION` state/hash/file-identity/fault ledger. |
| `AT-V8-10` | Restore preflight authenticates all components, versions, keys, space, target and source deny before object create. | `NC-V8-10`: one-byte-low reserve, incompatible image/tool, expired catalog, target collision or visible source/live root creates zero target objects. | `EV-V8-10-RESTORE-PREFLIGHT` predicate/budget/no-change records. |
| `AT-V8-11` | Strict pax restore recreates expected tree as locked non-root UID/GID/modes in fresh volume. | `NC-V8-11`: traversal, absolute/ADS/case-Unicode alias, link/device/FIFO/socket, UID/GID/mode/size overflow yields RC 129/131. | `EV-V8-11-ARCHIVE-SAFETY` encrypted listing/tree hashes and negative matrix. |
| `AT-V8-12` | Restore graph has exact internal DB peers, zero host ports/provider secrets/triggers/egress and source IDs; credential canary decrypts without export. | `NC-V8-12`: attach uplink, publish port, mount source/live root, restore active workflow/arm or provider HTTP canary yields RC 144. | `EV-V8-12-COLD-RESTORE` V4 isolation refs, object/mount hashes and semantic results. |
| `AT-V8-13` | Full backup/restore fault matrices leave source and previous verified generation invariant; a subsequent fresh target restore succeeds. | `NC-V8-13`: stale evidence, in-place retry/adopt/repair, auto-delete/quarantine promotion or source mutation is rejected. | `EV-V8-13-FAULT-MATRIX` case/RC/assertion/source-LKG hashes. |
| `AT-V8-14` | Simulated failure measures recoverable point and technical cold-restore time against owner policy. | `NC-V8-14`: stale/missing backup, hidden owner-wait time or objective exceeded cannot report healthy. | `EV-V8-14-RPO-RTO` cadence/freshness/timeline/objective result. |
| `AT-V8-15` | Supported n8n and PostgreSQL update succeeds on restored clone; injected migration failure recovers old generation in other fresh volumes. | `NC-V8-15`: old image on migrated volume, PostgreSQL major data-dir reuse, absent LKG/restore proof or early source mutation blocks. | `EV-V8-15-UPGRADE-RECOVERY` from/to locks, clone/restore/migration/promotion hashes. |
| `AT-V8-16` | Owner from clean session selects generation, reads status, performs key ceremonies, cold restore and failure diagnosis only by runbook. | `NC-V8-16`: implicit cwd/live secrets, agent hint, hidden destructive cleanup or ambiguous status leaves handoff incomplete. | `EV-V8-16-OWNER-HANDOFF` redacted black-box transcript and exact result refs. |

## 15. Traceability: source finding → V8 contract/AT/NC/EV

V8 принимает primary ownership findings R7 и backup/cold-restore часть cross-domain findings. `DESIGN_CLOSED` означает только наличие непротиворечивого проектного контракта; runtime остаётся pending. `XDEP` означает, что V8 не может закрыть finding без frozen соседнего domain.

| Finding | V8 contract | AT / NC / EV | Disposition |
|---|---|---|---|
| `R1-WIN-001` | `V8-C01` | `AT/NC/EV-V8-01` | `XDEP-V1`; endpoint guard consumed |
| `R1-WIN-007` | `V8-C09`, `V8-C13` | `AT/NC/EV-V8-10`, `14` | `XDEP-V3`; peak guard consumed |
| `R1-WIN-008` | `V8-C06`, `V8-C08` | `AT/NC/EV-V8-07`, `09` | `XDEP-V3`; qualified roots required |
| `R1-WIN-009` | `V8-C01`, `V8-C14` | `AT/NC/EV-V8-01`, `15` | `XDEP-V1/V2`; drift/update consumed |
| `R2-004` | `V8-C02`, `V8-C14` | `AT/NC/EV-V8-02`, `15` | `XDEP-V2`; all helper/runtime images locked |
| `R2-006` | `V8-C14` | `AT/NC/EV-V8-15` | `XDEP-V2`; restore-first recovery |
| `R2-009` | `V8-C08`, `V8-C14` | `AT/NC/EV-V8-09`, `15` | `XDEP-V2`; LKG availability required |
| `R2-012` | `V8-C06` | `AT/NC/EV-V8-06` | `XDEP-V2`; age/tool/spec source evidence |
| `R3-NET-002` | `V8-C11` | `AT/NC/EV-V8-12` | `XDEP-V4`; restore no-egress runtime proof |
| `R3-MOUNT-006` | `V8-C09`, `V8-C10` | `AT/NC/EV-V8-10`, `11` | `XDEP-V3/V4`; mount/path deny |
| `R3-CLEAN-007` | `V8-C08`, `V8-C12` | `AT/NC/EV-V8-09`, `13` | `XDEP-V3/V4`; no automatic deletion |
| `R4-F03` | `V8-C02`, `V8-C04`, `V8-C10` | `AT/NC/EV-V8-02`, `04` | `DESIGN_CLOSED_WITH_XDEP-V5` |
| `R4-F04` | `V8-C02`, `V8-C07`, `V8-C10` | `AT/NC/EV-V8-05`, `08`, `12` | `DESIGN_CLOSED_WITH_XDEP-V5` |
| `R4-F05` | `V8-C14` | `AT/NC/EV-V8-15` | `DESIGN_CLOSED_WITH_XDEP-V2/V5` |
| `R4-F06` | `V8-C02`, `V8-C03`, `V8-C05` | `AT/NC/EV-V8-03`, `05` | `DESIGN_CLOSED`; single PostgreSQL bridge authority |
| `R4-F08` | `V8-C02`, `V8-C06`, `V8-C14` | `AT/NC/EV-V8-02`, `06`, `15` | `XDEP-V2`; operational images/tools included |
| `R4-F09` | `V8-C09`, `V8-C10` | `AT/NC/EV-V8-10`, `11` | `DESIGN_CLOSED_WITH_XDEP-V3/V4/V5` |
| `R5-F06` | `V8-C02`, `V8-C05` | `AT/NC/EV-V8-02`, `05` | `XDEP-V6`; offset authority and namespace bound |
| `R5-F15` | `V8-C02`, `V8-C08`, `V8-C13` | `AT/NC/EV-V8-02`, `09`, `14` | `XDEP-V6`; backup inherits data expiry |
| `R5-F16` | `V8-C05`, `V8-C11`, `V8-C13`, `V8-C15` | `AT/NC/EV-V8-05`, `12`, `14`, `16` | `XDEP-V6/V10`; owner recovery flow |
| `R6-P1-003` | `V8-C02`, `V8-C07`, `V8-C10` | `AT/NC/EV-V8-05`, `08`, `12` | `DESIGN_CLOSED_WITH_SECRET-XDEP` |
| `R6-P1-005` | `V8-C02`, `V8-C08`, `V8-C13` | `AT/NC/EV-V8-02`, `09`, `14` | `XDEP-V6`; PII retention/copies visible |
| `R6-P1-006` | `V8-C15` | `AT/NC/EV-V8-07`, `13` | `XDEP-evidence`; source allowlist required |
| `R6-P1-007` | `V8-C06`, `V8-C07`, `V8-C08` | `AT/NC/EV-V8-07`, `08`, `09` | `XDEP-V3`; at-rest remnants remain residual |
| `R6-P1-008` | `V8-C06` | `AT/NC/EV-V8-06`, `07` | `DESIGN_CLOSED`; no persistent plaintext |
| `R6-P1-009` | `V8-C07`, `V8-C08` | `AT/NC/EV-V8-08`, `09` | `XDEP-secret/incident`; retained generations inventoried |
| `R7-F01` | `V8-C03` | `AT/NC/EV-V8-03` | `DESIGN_CLOSED` |
| `R7-F02` | `V8-C02`, `V8-C05` | `AT/NC/EV-V8-02`, `05` | `DESIGN_CLOSED` |
| `R7-F03` | `V8-C02`, `V8-C04`, `V8-C10` | `AT/NC/EV-V8-02`, `04` | `DESIGN_CLOSED` |
| `R7-F04` | `V8-C07` | `AT/NC/EV-V8-08` | `DESIGN_CLOSED_WITH_SECRET-XDEP` |
| `R7-F05` | `V8-C06` | `AT/NC/EV-V8-06`, `07` | `DESIGN_CLOSED_WITH_XDEP-V2` |
| `R7-F06` | `V8-C08`, `V8-C12` | `AT/NC/EV-V8-09`, `13` | `DESIGN_CLOSED` |
| `R7-F07` | `V8-C09`, `V8-C11` | `AT/NC/EV-V8-10`, `12` | `DESIGN_CLOSED_WITH_XDEP-V4/V5` |
| `R7-F08` | `V8-C09`, `V8-C10`, `V8-C12` | `AT/NC/EV-V8-10`, `11`, `13` | `DESIGN_CLOSED` |
| `R7-F09` | `V8-C14` | `AT/NC/EV-V8-15` | `DESIGN_CLOSED` |
| `R7-F10` | `V8-C07`, `V8-C09`, `V8-C11` | `AT/NC/EV-V8-08`, `10`, `12` | `DESIGN_CLOSED`; L1/L2/L3 labels explicit |
| `R7-F11` | `V8-C13` | `AT/NC/EV-V8-14` | `DESIGN_CLOSED_PENDING_OWNER_VALUES` |
| `R7-F12` | `V8-C12` | `AT/NC/EV-V8-13` | `DESIGN_CLOSED` |
| `R8-P1-010` | `V8-C15` | `AT/NC/EV-V8-13` | `XDEP-evidence`; content-addressed envelope required |
| `R8-P2-011` | `V8-C02`, `V8-C06` | `AT/NC/EV-V8-02`, `06` | `XDEP-V2`; tool BOM/feature probes |
| `R8-P2-012` | `V8-C08`, `V8-C10`, `V8-C12` | `AT/NC/EV-V8-09`, `11`, `13` | `XDEP-V4`; exact labels/custody |
| `R9-F03` | `V8-C08`, `V8-C09`, `V8-C10` | `AT/NC/EV-V8-09..11` | `XDEP-V3/V9`; Windows/archive path safety |
| `R9-F08` | `V8-C01`, `V8-C15` | `AT/NC/EV-V8-01`, `13` | `XDEP-V9`; repo/Vault remain forbidden |
| `R9-F10` | `V8-C06`, `V8-C15` | `AT/NC/EV-V8-07` | `XDEP-secret/repo`; temp/sink policy |
| `R10-F03` | `V8-C07`, `V8-C09`, `V8-C11` | `AT/NC/EV-V8-08`, `10`, `12` | `DESIGN_CLOSED` |
| `R10-F04` | `V8-C08`, `V8-C09`, `V8-C13` | `AT/NC/EV-V8-09`, `10`, `14` | `XDEP-V3`; hard resource enforcement |
| `R10-F05` | `V8-C01`, `V8-C14` | `AT/NC/EV-V8-01`, `15` | `DESIGN_CLOSED_WITH_XDEP-V1/V2/V5` |
| `R10-F06` | `V8-C13`, `V8-C15` | `AT/NC/EV-V8-14`, `16` | `XDEP-V10`; black-box owner handoff |
| `R10-F08` | `V8-C15` | `AT/NC/EV-V8-14`, `16` | `XDEP-V10`; global status integration |
| `R10-F11` | `V8-C13`, `V8-C15` | `AT/NC/EV-V8-14`, `16` | `XDEP-V10`; daily runbook integration |

## 16. Cross-domain dependencies and current conflicts

1. **V1 Windows/control plane:** exact endpoint/project guard, execution lock, roots and immediate drift check wrap every operation. V8 never changes global context.
2. **V2 supply chain:** official age binary/spec, PostgreSQL/archive/validator tools and every helper image must be in runtime lock with linux/amd64 child/config/layer digests and feature probes. No tool fallback.
3. **V3 resources/storage:** roots, DACL/effective principals, at-rest decision, peak equation, retention capacity and Windows atomic/file identity primitives are authoritative. V8 specializes V3 backup/restore semantics without weakening them.
4. **V4 isolation:** backup RO mount and restore new-volume mount manifests, exact internal restore graph, zero ports/egress/source mounts and non-root capabilities are required. V4 currently says its backup-source mount is not yet authorized; integrated plan must add an explicit V8-bound read-only backup operation, not reinterpret generic restore permissions.
5. **V5 Compose/PostgreSQL/n8n:** database/role/schema lock, UID/GID, migration state, exact source writer set, n8n key continuity and supported trigger-disable/decryptability mechanism are required. Current V4/V5/V6 bridge network-role conflict must be resolved before backup writer inventory can be frozen.
6. **V6 Telegram/privacy:** PostgreSQL bridge is the single offset/inbox/outbox/cap/route authority; restored state begins disarmed. Data TTL and generation expiry come from V6.
7. **V7 secrets/privacy/incident:** `V7-S03`, `V7-S10`, `V7-S11`, `V7-C04` and `V7-C12` supply raw-key generation, purpose-separated n8n key ID, non-echo transport, custody and incident semantics. V8 specializes `V7-S11` as the age X25519 private identity and never reads or stores values outside its future trusted verifier.
8. **Evidence/K4R:** global collector/candidate/run envelope may have its own section number. V8 contributes EV records; candidate stdout cannot seal COMPLETE/RESTORE_VERIFIED.
9. **Repo/Vault:** future scripts/config need exact touchset/candidate/commit authority; this design writes only this draft and does not authorize repository changes.
10. **Operability:** global `lab backup`, `lab restore-drill`, `lab backup status`, `lab recovery status` grammar, one safe next action and owner black-box handoff are V10-owned.

Numbering note: some neighboring drafts refer to backup/recovery as `V7`, while this assigned file/contract is `V8`. Canonical integrator must choose one section number and rewrite cross-links mechanically without renaming contract semantics. Until hashes agree, status is `V8_BLOCKED_CONTRACT_DRIFT`.

## 17. Residual risks and STOP triggers

Residual risks:

1. Backup and keys may be outside VHDX but on the same physical Windows disk; host/disk loss remains uncovered.
2. Approved Windows administrator/SYSTEM/Docker control principal can access live data and may subvert runtime; this is trust-boundary risk, not solved by encryption of backups.
3. Deletion cannot promise secure erase from SSD/VHDX/pagefile/crash dump or third-party backup/sync agents.
4. Age/PostgreSQL/n8n exact-version support and non-root archive semantics are unknown until runtime qualification.
5. PostgreSQL logical backup does not restore Docker Desktop, Windows/WSL state or vendor ability to reinstall/downgrade Desktop.
6. n8n active-trigger suppression may be unavailable in the pinned release. In that case structural DB/file restore can run, but semantic n8n cold restore remains blocked; direct DB edits are not a fallback.
7. Manual owner key proof can increase elapsed recovery. Technical and human-wait durations are reported separately.
8. Backup with retained PII may expire before minimum generation count is safely replenished; status blocks real-dev/retirement rather than extending PII retention silently.

Immediate STOP/BLOCKED before next mutation:

- endpoint/execution/plan/authority/runtime lock drift;
- unknown writer, session, database, volume, extension, key ID, data class or tool;
- real-dev still armed, provider activity unverified or source writer restarts;
- plaintext host/container staging, passphrase/custom cipher or caller-controlled age nonce/salt;
- backup key/n8n key custody missing, co-dependent or mismatched;
- component/BOM/catalog/authentication/hash mismatch;
- disk/retention peak does not preserve V3 host reserve;
- existing/nonempty/foreign restore object, unsafe archive entry or non-root ownership capability failure;
- source/live-root mount, provider secret, host port, external route or active trigger in restore;
- old image against migrated state or raw PostgreSQL data-directory reuse across major;
- requested auto-delete, broad prune, factory reset, VHDX/WSL action, plan B or VPS.

## 18. Implementation order and Definition of Done V8

Sequential future order after full plan v2 owner approval:

1. Resolve section numbering and freeze V1–V7 cross-domain contracts/hashes, including bridge role/network conflict and secret key-ID transport.
2. Implement only offline schemas, canonicalizers, state machines, catalog verifier, archive validator and fault fixtures under exact repo-write authority.
3. Acquire and lock age/PostgreSQL/archive/validator images/tools and official specifications through V2.
4. Qualify V1/V3/V4 endpoint, roots, resources, read-only source mounts, non-root ownership and restore isolation using synthetic data.
5. Implement PostgreSQL/n8n/bridge census and quiesce; prove every writer canary blocked.
6. Execute streaming crypto/plaintext/fault/publication matrices on synthetic components and owner test keys.
7. Create first COMPLETE generation only after independent key proof, then perform cold restore into fresh isolated project.
8. Run semantic DB/grant/file/n8n-key/bridge checks, record L1/L2 status and measured RPO/RTO.
9. Rehearse n8n and PostgreSQL update failure/restore-first rollback on clones.
10. Owner performs black-box backup/status/cold-restore/failure procedure without agent command hints.
11. Publish redacted EV-V8 records and independently review exact implementation/candidate.

V8 design is ready for canonical integration only when:

- all `R7-F01..F12` and every cross-domain row in §15 retains contract+AT+NC+EV mapping;
- component inventory is closed and PostgreSQL globals/databases/roles/grants/extensions plus n8n/bridge state are unambiguous;
- single epoch/quiesce and writer-resume failure semantics are executable, not prose alternatives;
- age format/tool/KDF/nonce/salt/key rules prohibit custom/passphrase/plaintext fallback;
- COMPLETE/RESTORE_VERIFIED, catalog, retention and fault states cannot select partial output;
- cold restore has zero live dependency, egress, ports and triggers and rejects archive/ownership attacks;
- update rollback restores data+matching key+matching images in fresh volumes;
- residual L1/L2/L3 scope and owner RPO/RTO decisions are explicit;
- UTF-8 without BOM, LF only and exactly one final LF are verified;
- no design statement is represented as runtime PASS, installation authority or destructive permission.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[02_V1_WINDOWS_CONTROL_PLANE]]
- [[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]
- [[04_V3_RESOURCE_STORAGE_BOUNDARY]]
- [[05_V4_ISOLATION_NETWORK_EXPOSURE]]
- [[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]
- [[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]
- [[08_V7_SECRETS_PRIVACY_INCIDENT]]
- [[00_FINDINGS_BASELINE]]
- [[01_BASELINE_AUDIT]]
