---
id: "n8nagents-plan-v2-v5-compose-postgres-n8n-lifecycle"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V5 Compose/PostgreSQL/n8n lifecycle architect"
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
  - "[[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]"
доказательства:
  - "[[00_FINDINGS_BASELINE]]"
  - "[[01_BASELINE_AUDIT]]"
теги: ["n8nagents", "plan-v2", "compose", "postgresql", "n8n", "lifecycle", "draft"]
---

# V5 — deterministic Compose, PostgreSQL и n8n lifecycle

## 0. Статус, область и запрет на runtime-утверждения

Это implementation-ready design-секция будущего полного plan v2. Она не является разрешением на download, install, Docker/Windows/VPS mutation, чтение секретов, изменение project repo, запуск контейнеров или создание production state. Все runtime-предикаты имеют статус `DESIGN_ONLY` до исполнения после отдельных gates.

V5 владеет:

- точным Compose merge/mode/convergence contract;
- service dependency, health, readiness и migration graph;
- PostgreSQL databases/schemas/roles/grants/bootstrap/migrations;
- allowlisted n8n configuration, persistent ownership и single-process topology;
- owner/2FA onboarding и workflow import/binding lifecycle;
- project-scoped runtime object identity и migration-safe updates.

V5 не владеет Windows/Docker endpoint, acquisition/signatures/OCI provenance, Windows storage/backup crypto, network enforcement, Telegram semantics/secrets, B2r/O5 evidence или dirty-worktree integration. Эти области являются fail-closed cross-dependencies.

## 1. Непереговорные инварианты

1. Только три взаимоисключающих requested mode classes: `mock`, `real-dev`, `gate`. Одновременно активен не более одного class; `gate` требует `n8nagents-local` в состоянии `STOPPED`. `real-dev` разрешается ровно в одном V4 submode: `REAL_TG` или `REAL_TG_DEEPSEEK`; hot-enable/совместный render двух submodes запрещён.
2. Все Docker/Compose вызовы проходят через `V1-001 local-daemon-guard` с explicit approved context. Прямой `docker compose`, `docker`, SDK или service targeting пользователем/child script не является поддерживаемым интерфейсом.
3. Compose project name, ordered `-f`, ordered `--env-file`, `--profile`, project directory и allowed subcommand фиксируются immutable operation manifest. `COMPOSE_*` и Docker endpoint env overrides запрещены V1.
4. Никаких implicit `.env`, auto-selected profile, tag-only image, `latest`, implicit default network, `container_name`, external unowned volume или произвольного service target.
5. PostgreSQL не публикует host port. n8n публикуется только согласно V1/V4 loopback contract. Caddy, public edge, webhook и public listener отсутствуют.
6. `mock` не получает реальные Telegram/DeepSeek secrets и не имеет external egress. `real-dev` не стартует без current time-bounded arm contract из V6. `gate` не получает application secrets или persistent application volumes.
7. n8n использует только PostgreSQL. Обнаружение SQLite file/config/runtime artifact блокирует start; silent fallback запрещён.
8. n8n работает в `regular`, one-main-process topology. Queue mode, Redis, workers и external task runners отсутствуют. Их добавление — новый reviewed plan, image lock, resource envelope и network contract.
9. `N8N_ENCRYPTION_KEY` существует до первого n8n boot, имеет stable key ID и не меняется между restart/restore. Отсутствие/подмена блокируют n8n до process start.
10. Custom/community nodes запрещены. Runtime node/package inventory должен быть подмножеством reviewed pinned image; writable node-install directories отсутствуют или пусты.
11. Ни Compose convergence, ни rollback не удаляют named volumes. `down -v`, prune, factory reset и reuse неизвестного volume запрещены.
12. Любой unknown, drift, extra service/network/volume, failed health, migration checksum mismatch или unresolved ownership даёт nonzero и не агрегируется в `PASS`.

## 2. Immutable manifest family

До первого Compose render создаётся signed/hash-bound family из secret-free records:

| Record | Обязательное содержание |
|---|---|
| `V5-compose-lock` | schema/version, plan/execution lock, approved endpoint hash, exact Compose build, project directory physical identity, ordered files/env files/profiles, project name, command grammar, expected rendered hash |
| `V5-mode-lock` | mode, allowed transition, exact desired/forbidden services, networks, volumes, ports, secret slots, arm ref, timeout policy |
| `V5-db-lock` | cluster/database/schema/role identifiers, normalized SQL templates and hashes, migration manifest, grants/default privileges/search paths |
| `V5-n8n-lock` | exact n8n image child/config digests, config allowlist, process identity, writable paths, readiness probe, workflow inventory, instance-key ID |
| `V5-runtime-lock` | V1 endpoint, V2 image/tool lock, V3 roots/resources/volumes, V4 network/mount identity, V6 arm/Telegram contract hashes |

Record canonicalization uses UTF-8 without BOM, LF, final LF, sorted object keys where schema declares maps, ordinal case-sensitive identifiers and SHA-256. Secret values, raw user/chat/bot IDs, passwords, tokens and encryption keys не входят ни в один record.

Изменение любого record после render означает `BLOCKED_V5_DRIFT`, требует нового render/review и запрещает reuse старого runtime PASS.

## 3. V5-001 — exact Compose invocation и mode matrix

### 3.1. Canonical files и env sources

Future repo touchset после отдельного repo-write gate должен реализовать logical layout; exact paths фиксирует integration domain:

```text
local/compose/compose.base.yaml
local/compose/compose.mock.yaml
local/compose/compose.real-dev.yaml
local/compose/compose.gate.yaml
local/config/common.env              # generated secret-free, protected root
local/config/mock.env                # generated secret-free
local/config/real-dev.env            # generated secret-free
local/config/gate.<run-id>.env       # generated secret-free, disposable
```

Ни один файл с именем `.env` не допускается в project directory или ancestor, используемом Compose. Wrapper задаёт `--project-directory` exact physical path и перед render хеширует все explicit env files. Container secrets передаются только через V3-qualified secret files/Compose secret mounts или reviewed in-container file-to-process adapter; secret value не является Compose interpolation source.

Canonical argv после V1 guard:

```text
MOCK:
docker --context <approved> compose
  --project-directory <approved-project-dir>
  --project-name n8nagents-local
  --env-file <approved-common.env>
  --env-file <approved-mock.env>
  -f <compose.base.yaml>
  -f <compose.mock.yaml>
  --profile mock <allowlisted-subcommand>

REAL-DEV:
docker --context <approved> compose
  --project-directory <approved-project-dir>
  --project-name n8nagents-local
  --env-file <approved-common.env>
  --env-file <approved-real-dev.env>
  -f <compose.base.yaml>
  -f <compose.real-dev.yaml>
  --profile <real-tg | real-tg-deepseek> <allowlisted-subcommand>

GATE:
docker --context <approved> compose
  --project-directory <approved-project-dir>
  --project-name n8nagents-k4r-<authorized-run-id>
  --env-file <approved-common.env>
  --env-file <approved-gate.run-id.env>
  -f <compose.gate.yaml>
  --profile gate <allowlisted-subcommand>
```

Line breaks above are explanatory. Actual argv is an array in operation manifest; no shell concatenation/eval. For `real-dev` the arm record selects exactly one profile token, never both. File order is normative and cannot be supplied via `COMPOSE_FILE`. Multiple/missing profile flags, extra `-f`/env file, alternate project name, current-directory discovery or direct service argument are rejected before Docker API mutation.

### 3.2. Exact expected objects

Compose service keys are fixed; `container_name` запрещён. One-shot services exist in rendered model but are not counted as required running services after successful completion.

| Mode | Project | Required running services | Required successful one-shot services | Forbidden services | Persistent volumes |
|---|---|---|---|---|---|
| `mock` | `n8nagents-local` | `postgres`, `n8n`, `mock-telegram`, `mock-llm` | `db-bootstrap`, `db-migrate`, `n8n-volume-init` | `telegram-bridge`, `egress-telegram`, `deepseek-adapter`, `egress-deepseek`, `gate-runner` | `local_postgres_data`, `local_n8n_data`, `local_n8n_files` |
| `real-dev/REAL_TG` | `n8nagents-local` | `postgres`, `n8n`, `telegram-bridge`, `egress-telegram` | `db-bootstrap`, `db-migrate`, `n8n-volume-init`, `real-dev-arm-guard` | mocks, `deepseek-adapter`, `egress-deepseek`, `gate-runner` | те же exact local volumes + non-authoritative `local_bridge_state` |
| `real-dev/REAL_TG_DEEPSEEK` | `n8nagents-local` | `REAL_TG` set + `deepseek-adapter`, `egress-deepseek` | те же one-shots с arm, дополнительно bound к model/cost policy | mocks, `gate-runner` | те же exact local volumes + non-authoritative `local_bridge_state` |
| `gate` | `n8nagents-k4r-<run-id>` | none after completion | `gate-runner` | все local application services | только run-scoped disposable evidence/work volumes; application volumes forbidden |

`real-dev-arm-guard` получает только opaque current arm reference и проверяет V6 state; он не читает raw token/recipient identifiers. `telegram-bridge`, `egress-telegram`, опциональные `deepseek-adapter`/`egress-deepseek` принадлежат V6 по application/security semantics, но включены в V5 mode convergence. `local_bridge_state` не является offset/arm/outbox authority: он содержит только проверяемый recreatable client cache; authoritative state находится в PostgreSQL `bridge`, поэтому backup объявляет volume `EXCLUDED_NONAUTHORITATIVE` и restore безопасно создаёт его заново.

Exact V4 network keys являются частью render lock: `db`, `mock_tg`, `mock_llm`, `telegram_ingress`, `telegram_proxy`, `llm_ingress`, `llm_proxy`, `uplink`. Membership обязан совпасть с `V4-C05-NETWORK-GRAPH`: PostgreSQL только `db`; n8n получает только нужные internal networks; bridge/adapters не входят в `uplink`; только secretless `egress-*` brokers входят в `uplink`; gate имеет `network_mode:none`. Implicit `default` не создаётся.

### 3.3. Render gate

До mutation wrapper выполняет `compose config` тем же argv prefix и:

1. нормализует JSON/YAML render pinned parser-ом;
2. отклоняет unresolved interpolation, implicit image, build outside reviewed context, unknown extension, host path, device, capability, privileged, Docker socket, host namespace, external network/volume, extra port или secret source;
3. сравнивает exact service/network/volume/profile/port/mount/image/resource/restart/logging set с mode lock;
4. проверяет explicit `platform: linux/amd64` и digest reference каждой image через V2;
5. проверяет V3 hard resource/log limits и V4 network/mount policy;
6. сохраняет redacted rendered-config hash, но не unrestricted render.

Rendered mismatch — `RC 65 BLOCKED_V5_RENDER`; `up/start/create` не вызываются.

Поддерживаемый wrapper никогда не выполняет `compose up <service>`, включая profiled real service: Compose может активировать profile при direct targeting, поэтому это отдельный negative canary.

## 4. V5-002 — deterministic convergence и lifecycle state machine

### 4.1. States

```text
STOPPED
  -> PREFLIGHTED
  -> RENDERED
  -> CONVERGING
  -> STARTING_DEPENDENCIES
  -> MIGRATING
  -> STARTING_N8N
  -> MOCK_READY | REAL_TG_ARMED_READY | REAL_TG_DEEPSEEK_ARMED_READY | GATE_RUNNING

GATE_RUNNING -> GATE_COMPLETE -> STOPPED
REAL_TG*_ARMED_READY -> DRAINING -> DISARMED -> STOPPED
any state -> BLOCKED | FAILED
```

V6 may expose `REAL_DEV_DISARMED`, `DRAINING` и `EMERGENCY_UNVERIFIED` substates. V5 aggregation maps only verified stopped polling to `DISARMED`; `EMERGENCY_UNVERIFIED` is nonzero and never `STOPPED/PASS`.

State identity is `(project_name, mode, config_hash, mode_lock_hash, volume_set_hash, endpoint_hash, arm_ref|null)`. Human label alone is insufficient.

### 4.2. Convergence from any known state

`lab start --mode <mode>`:

1. acquires one Windows process lock plus PostgreSQL advisory lock when DB is reachable;
2. validates V1/V2/V3/V4/V6 prerequisites and current mode record;
3. renders desired configuration and inventories all Docker objects with exact Compose project labels;
4. if object labels/config/ownership are missing, conflicting or unknown, returns `BLOCKED_V5_OBJECT_DRIFT`; it never adopts or removes them;
5. if current mode equals desired and all postconditions hold, returns idempotent `PASS` without recreate;
6. for `mock -> real-dev`: obtain current V6 arm, then fully drain/remove exact current-mode containers and networks without volumes; verify no process/listener/connection remains; create the selected `REAL_TG` or `REAL_TG_DEEPSEEK` graph from `STOPPED`;
7. for `real-dev -> mock/stop` or `REAL_TG <-> REAL_TG_DEEPSEEK`: V6 disarm first, drain bounded in-flight work, stop bridge/adapter then brokers, fully remove exact current-mode containers/networks without volumes, verify `STOPPED`, then optionally create target graph; hot-enable is forbidden;
8. for changed base render: orderly stop application writers, never remove volumes, recreate only exact owned containers/networks, then run full bootstrap/migration/readiness graph;
9. `gate` starts only after verified local `STOPPED`; run-scoped object labels include run ID, authority ID, candidate digest and resource class;
10. re-inventorys expected running/exited/absent sets and publishes result schema.

Removal of an incompatible container/network is permitted only when its full label tuple and object ID match both current-mode record and exact transition manifest. Unknown orphan yields block. `--remove-orphans`, broad orphan adoption/removal and guessed `down` are forbidden. Named volumes are never transition targets.

Docker Desktop restart:

- `postgres`, `n8n`, `mock-telegram`, `mock-llm` use `restart: unless-stopped` only after qualification;
- one-shot services use `restart: "no"`;
- `telegram-bridge`, `egress-telegram`, `deepseek-adapter`, `egress-deepseek` use `restart: "no"`; they must not resume polling/provider traffic because Docker restarted; V6 current arm and emergency state govern a new explicit start;
- wrapper `status` after daemon restart re-evaluates health, migration checksum, arm and object identity before reporting ready.

`lab stop` is idempotent, uses the recorded exact mode manifest, disarms real-dev first, performs bounded graceful stop, preserves volumes and emits `STOPPED` only after container/process/polling postconditions. Unknown mode record returns nonzero; no guessed `down`.

## 5. V5-003 — startup, health, readiness и failure graph

### 5.1. Dependency graph

```text
V1/V2/V3/V4 guards
       |
       +--> n8n-volume-init (one-shot, completed=0)
       |
       +--> postgres (healthy)
               |
               +--> db-bootstrap (one-shot, completed=0)
                         |
                         +--> db-migrate (one-shot, completed=0)
                                  |
                                  +--> n8n (vendor migration + ready/healthy)
                                           |
                                           +--> mock services (mock)
                                           |
                                           +--> real-dev-arm-guard -> egress broker -> bridge/adapter (real-dev)
```

Compose `depends_on` conditions express ordering, but wrapper independently validates timestamps, exit codes, restart counts, health log and expected dependency hash. Container creation order is not readiness evidence.

### 5.2. Probes и bounds

| Component | Readiness predicate | Initial bound | Restart/stop policy |
|---|---|---:|---|
| PostgreSQL | server accepts authenticated connection; expected cluster/database identity and recovery state are valid | 120 s | `unless-stopped`; 90 s stop grace |
| `db-bootstrap` | exact bootstrap state/checksum and role/database assertions; exit `0` once | 60 s after PG health | no restart; failure blocks downstream |
| `db-migrate` | advisory lock, all ordered checksums applied, post-schema assertions; exit `0` once | 180 s | no restart; failure blocks n8n |
| `n8n-volume-init` | exact UID/GID/mode/write probe on each declared path; exit `0` once | 60 s | no restart |
| n8n | exact-version supported readiness endpoint plus DB-backed sentinel; internal migrations complete; restart count within bound | 180 s | `unless-stopped`; 60 s stop grace; wrapper stops loop on bound failure |
| mocks | internal health and zero-egress V4 assertion | 60 s | `unless-stopped`; 30 s stop grace |
| proxy/bridge | V6 arm, lease, bounded polling/readiness, no unexpected destination | 60 s | V6 fail-closed; 45 s drain/stop grace |
| gate | exact result envelope and zero exit; timeout from frozen gate contract | gate-specific | no restart |

Initial bounds are owner-reviewable defaults and must fit V3 operation resource/time policy. Timeout is failure/block, not automatic extension. One automatic restart of a recoverable dependency is observable; repeated restart count above frozen threshold makes wrapper stop affected application containers and return `FAILED_V5_DEPENDENCY_LOOP`.

Slow PostgreSQL leaves downstream unstarted. Partially applied project migration must either roll back its transaction or record a failed non-transactional exception that blocks all starts; v2 initially forbids non-transactional migrations. Delayed n8n readiness prevents mocks/bridge readiness. PostgreSQL restart after READY causes `DEGRADED`; n8n may reconnect or restart according to pinned-version qualification, but status returns READY again only after authenticated DB and application sentinel revalidation.

## 6. V5-004 — PostgreSQL authority model

### 6.1. Logical databases и schemas

| Database | Schema | Purpose | Direct n8n metadata access |
|---|---|---|---|
| `n8n` | exact pinned n8n schema (`public` only if lock explicitly selects it) | vendor-owned n8n metadata/credentials/workflows/executions | n8n service only |
| `n8nagents_app` | `app` | application state and approved domain records | no |
| `n8nagents_app` | `memory` | isolated agent/user memory records | no |
| `n8nagents_app` | `bridge` | fenced lease, arm/cap/offset, authenticated inbox ACK, immutable reply route, idempotent outbox and send-attempt ledger required by V6 | no |
| `n8nagents_control` | `control` | bootstrap/migration versions and non-secret consistency markers | no runtime role |

`PUBLIC` loses `CREATE` on every database/schema and loses `CONNECT` on non-template project databases. Each role receives only explicit `CONNECT`, schema `USAGE` and object privileges. `search_path` is fixed per login as `<one approved schema>,pg_catalog`; `$user`, implicit `public` and caller-controlled search path are forbidden.

V6 owns the semantic invariants and procedure signatures for `bridge`; V5 owns their checksummed SQL delivery and grant enforcement. If V6 schema lock is absent or differs, `db-migrate` blocks.

### 6.2. Roles and least privilege

| Role | LOGIN | Authority | Explicit prohibitions |
|---|---:|---|---|
| `lab_cluster_admin` | yes, secret-file only | official image physical-cluster owner; logical bootstrap, controlled globals backup/restore only | never mounted into n8n/bridge/mocks; no external egress; no workflow use |
| `n8n_runtime` | yes | owner/migration authority only inside dedicated `n8n` database/schema because pinned n8n performs vendor migrations at startup | `NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`; no connect to app/control DBs |
| `app_owner`, `memory_owner`, `bridge_owner` | no | own one schema and objects/default privileges | no login; no cross-schema membership |
| `app_migrator` | yes, one-shot secret | may `SET ROLE` only to the three NOLOGIN owners while checksummed migrations run | no cluster/database creation, no n8n DB/control runtime access |
| `app_runtime` | yes | approved DML or preferably EXECUTE on `app` API procedures | no DDL, no `memory`/`bridge` raw access |
| `memory_runtime` | yes | narrow EXECUTE/DML within `memory`, with row/tenant policy defined elsewhere | no app/bridge/n8n/control access |
| `automation_runtime` | yes, n8n Credential | EXECUTE only on approved app/memory and V6 `bridge.claim_*`/`bridge.enqueue_*` procedures | no raw tables, route/cap/arm/offset mutation, no DDL |
| `bridge_runtime` | yes, bridge only | EXECUTE on V6 lease/ingress/ack/outbox/send-attempt/offset procedures | no raw tables, app/memory/n8n/control access |
| `backup_reader` | optional one-shot | exact read/metadata scope proven sufficient for logical backup; globals still via isolated admin job if required | no writes, no runtime service mount |

No role except `lab_cluster_admin` has `SUPERUSER`; no application role has `CREATEDB`, `CREATEROLE`, `REPLICATION` or `BYPASSRLS`. Admin/migrator secrets are not present in long-running application containers.

Object creation occurs after `SET LOCAL ROLE <schema_owner>` inside migration transaction. `ALTER DEFAULT PRIVILEGES FOR ROLE <schema_owner> IN SCHEMA <schema>` grants only the matching runtime role/procedure execution and explicitly revokes `PUBLIC`. Post-migration assertions query role attributes, memberships, owners, grants, default ACLs, RLS state and `search_path` from every effective runtime identity.

The unavoidable n8n runtime+vendor-migration authority in its isolated database is a documented residual of the pinned product. It is not generalized to application schemas.

### 6.3. Minimum transactional bridge interface

V6 freezes exact procedure names/arguments, but V5 requires these database semantics before SQL implementation can pass:

1. `bridge.acquire_poller_lease`/`renew_poller_lease` establish one global fenced poller for `(environment_ref, verified_bot_ref)`. Every later terminal/offset/cap/outbox mutation validates `(lease_id, fence_epoch, arm_id)`; stale fence affects zero rows and forces drain.
2. An authorized Update enters `bridge.accept_authorized_inbox` directly from `telegram-bridge` over a V4-approved DB-only path. A locked PostgreSQL verifier validates the versioned HMAC-SHA256 envelope, timestamp/nonce, current fence/arm/authorization and atomic replay ledger through a protected `bridge.envelope_keyring`; runtime roles cannot read key material. The procedure inserts a unique inbox/dedup row with immutable reply route and returns the V6 signed durable ACK identity. Duplicate delivery returns the same `work_id`/equivalent ACK without changing route/cap or creating duplicate work.
3. Unauthorized/unsupported Updates use `bridge.record_terminal_drop`, retaining only the V6 minimal control fields. Durable authorized acceptance and terminal drops may invoke the same contiguous-offset CAS inside their transaction; `bridge.advance_contiguous_offset` is the explicit fenced operation for remaining terminal transitions. In every case offset advances only through the maximum prefix in received-batch order whose records all have durable terminal disposition. A failed middle Update prevents checkpoint past it even if a later `update_id` is terminal.
4. `automation_runtime` can call only `bridge.claim_work`, `bridge.complete_work` and `bridge.enqueue_reply`. It cannot select raw routing/identity tables, choose a recipient, update offset/arm/cap or modify a committed reply route.
5. `bridge_runtime` can call only the V6 lease, terminal-drop/inbox/offset, outbox claim, send reservation/result and redacted status procedures. `enqueue_reply` is idempotent by the V6 logical reply key and atomically reserves one initial cap slot per deterministic output chunk or rolls back the whole enqueue. Each later retry needs a new reservation. A safely cancelled pre-dispatch reservation may be released only by the fenced procedure; only an attempt entering `DISPATCHING` becomes consumed/ambiguous-consumed. Ambiguous provider send is recorded terminally according to V6 and is never blindly retried.
6. Every procedure is `SECURITY DEFINER` only where V6 requires it, fixes `search_path` internally, revokes `PUBLIC`, validates caller role and returns a closed result schema. Dynamic SQL and caller-supplied table/schema/route names are forbidden.

This makes PostgreSQL the single durable offset/inbox/dedup/outbox authority. Crash after durable inbox ACK but before processing causes reclaim/redelivery without loss; crash before contiguous-offset CAS causes provider redelivery and idempotent acceptance; no path checkpoints past nonterminal work. `local_bridge_state` may cache the last observed value but is ignored during recovery and never included in the consistency decision.

## 7. V5-005 — first-volume bootstrap и existing-volume migrations

### 7.1. Physical cluster initialization

Exact V2-reviewed PostgreSQL image initializes an empty `local_postgres_data` volume using `lab_cluster_admin` and password-file input while its process identity remains the V4-approved nonzero PostgreSQL UID/GID. This built-in first-volume action creates only the physical cluster/minimal control database. Arbitrary application SQL in `/docker-entrypoint-initdb.d` is forbidden because it is not replayed on existing volumes. If the exact image/volume-copy semantics cannot initialize and run without UID 0, root helper or privilege relaxation, result is `V4_LAB_BLOCKED_CAPABILITY`; no root fallback.

Before first start, volume identity/labels/emptiness come from V3. On an existing volume, image initialization is not assumed; `db-bootstrap` authenticates and verifies exact cluster identity. Wrong/missing admin credential, unexpected system identifier, newer major version, unknown database/role/schema or absent bootstrap marker gives nonzero and stops project.

### 7.2. Logical bootstrap on every start

`db-bootstrap` is an idempotent, checksummed one-shot service. Under advisory lock it chooses exactly one branch:

- `FIRST_LOGICAL_BOOTSTRAP`: target roles/databases absent and control marker absent; create declared NOLOGIN owners/login roles/databases/schemas, revoke defaults, set role attributes/search paths, install control marker and verify matrix;
- `EXISTING_VERIFIED`: marker/version/hash present; no creation/repair; assert exact identities, memberships, grants, owners and allowed extensions;
- `BLOCKED_EXISTING_DRIFT`: any partial, extra, conflicting or unknown object; no auto-adoption/drop/grant repair.

Passwords are created/rotated by a separate secret ceremony and passed as parameterized secret-file input; SQL transcripts/evidence contain only role names and keyed secret IDs.

### 7.3. Ordered migrations

`db-migrate` consumes a manifest sorted by ordinal ID:

```text
migration_id, target_database, target_schema, sha256, min_schema,
max_schema, transactional=true, owner_role, postcondition_hash
```

Algorithm:

1. authenticate as `app_migrator`, acquire one transaction-scoped advisory lock;
2. read migration history and reject duplicate ID/different checksum, gaps, downgrade, unknown ahead version or dirty marker;
3. begin; `SET LOCAL ROLE` exact NOLOGIN owner; set exact `search_path`; apply one migration; run postconditions; insert history row with checksum/tool/image/config identity; commit;
4. repeat in order; after all, run full permission/schema assertions from each runtime identity;
5. release and exit `0`; downstream starts only on successful completion.

All v2 project migrations are transactional. Any operation requiring non-transactional DDL is `BLOCKED_V5_MIGRATION_POLICY` until a separately reviewed two-phase migration contract exists. Fault injection after each statement must prove rollback and unchanged history. Re-run is no-op with identical checksum.

n8n vendor schema migrations remain n8n-owned and run only in its isolated database during n8n startup. Normal start accepts only the exact locked image/schema compatibility. Update uses cloned volumes under V5-010; an older n8n image is never started against forward-migrated data.

## 8. V5-006 — n8n exact configuration и persistent identity

### 8.1. Configuration allowlist

For the pinned n8n release, the future image-acceptance gate must verify spelling, support, default and secret-file behavior for every key below against authoritative release source/config schema. Unknown/removed key blocks image acceptance; the implementation may not silently drop it.

Allowed Compose-visible keys only:

```text
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n_runtime
DB_POSTGRESDB_SCHEMA=<locked-n8n-schema>
EXECUTIONS_MODE=regular
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_EDITOR_BASE_URL=http://127.0.0.1:5678
WEBHOOK_URL=http://127.0.0.1:5678
N8N_LISTEN_ADDRESS=0.0.0.0
N8N_SECURE_COOKIE=false
N8N_DIAGNOSTICS_ENABLED=false
N8N_VERSION_NOTIFICATIONS_ENABLED=false
N8N_TEMPLATES_ENABLED=false
N8N_PERSONALIZATION_ENABLED=false
N8N_COMMUNITY_PACKAGES_ENABLED=false
N8N_BLOCK_ENV_ACCESS_IN_NODE=true
N8N_LOG_LEVEL=warn
N8N_LOG_OUTPUT=console
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
EXECUTIONS_DATA_SAVE_ON_ERROR=none
EXECUTIONS_DATA_SAVE_ON_PROGRESS=false
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=false
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=24
EXECUTIONS_DATA_PRUNE_MAX_COUNT=1000
N8N_DEFAULT_BINARY_DATA_MODE=filesystem
N8N_BINARY_DATA_STORAGE_PATH=/files
NODE_OPTIONS=--max-old-space-size=1024
GENERIC_TIMEZONE=<owner-approved-IANA-zone>
TZ=<same-owner-approved-IANA-zone>
```

Secret-bearing process settings are limited to DB password and `N8N_ENCRYPTION_KEY`. Preferred exact-version-supported `_FILE` keys are used if authoritative verification proves them. Otherwise a reviewed minimal entrypoint reads `/run/secrets/n8n_db_password` and `/run/secrets/n8n_encryption_key`, validates file owner/mode/size/newline policy, exports values only inside container process and `exec`s n8n. They never appear in Compose env/render, command args, logs or evidence.

Before image acceptance, exact-version tests must also determine task-runner defaults. External/sidecar task runner is forbidden; if disabling it makes approved workflows unsupported, plan returns `BLOCKED_SCOPE` rather than adding queue/runner topology. Queue/Redis variables and services are forbidden by static config test.

The exact effective config is asserted at runtime from redacted semantic values, not by dumping process environment. Any non-allowlisted `N8N_*`, `DB_*`, `EXECUTIONS_*`, queue/Redis setting or unexpected default affecting egress/storage/execution blocks.

### 8.2. Process user and volumes

Image lock records numeric n8n UID/GID from exact child image. Compose uses that non-root identity; no runtime root, privileged, Docker socket or host-root mount.

| Volume | Mount | Writable by | Initialization |
|---|---|---|---|
| `local_n8n_data` | exact n8n user directory | locked n8n UID/GID only | reviewed image owns seed directory; empty-volume copy/init plus non-root `n8n-volume-init` write sentinel; existing volume verify-only |
| `local_n8n_files` | `/files` | locked n8n UID/GID only | reviewed image owns seed directory; same non-root verification; archive/restore validation belongs V3 |
| `local_postgres_data` | pinned image data directory | locked postgres UID/GID only | reviewed non-root image first init; V3 identity and restore ownership |
| `local_bridge_state` | `/state` | locked bridge UID/GID only | non-root verify; recreatable/non-authoritative cache, never offset/arm/outbox authority |

`n8n-volume-init` runs as the exact nonzero n8n UID/GID, `CapDrop=ALL`, no-egress, read-only rootfs, with exactly the two n8n volumes. It never calls `chown`, repairs permissions or recursively mutates existing data. Empty-volume ownership comes only from V2-reviewed image seed directories plus qualified Docker copy semantics. Owner/mode mismatch or inability to create/delete a sentinel blocks with V4 capability/mount status. No root helper is allowed.

No host bind provides `.n8n/custom`, global npm path or package manager cache. At every start scanner compares installed node/package inventory to V2 locked image and verifies writable custom/community directories absent/empty. Any extra package/node blocks before workflow execution.

### 8.3. Encryption-key continuity

Before first n8n process start:

1. V3-qualified owner-only secret root contains exactly one generated instance key with key ID; generation/custody is owned by secrets/V3 contracts;
2. key ID is bound to volume-set identity and n8n lock; raw key is never persisted in DB/evidence;
3. empty n8n state with missing key is `BLOCKED_MANUAL`, never auto-generated by n8n;
4. existing state requires the recorded key ID; missing/changed key stops before n8n process;
5. credential decryptability canary is performed through supported n8n behavior, never plaintext export/direct metadata SQL.

Rotation is only a separately reviewed supported n8n migration or controlled credential recreation. Replacing file bytes and restarting is forbidden.

## 9. V5-007 — owner, 2FA, workflow import и credential binding

### 9.1. Onboarding state machine

```text
INSTANCE_EMPTY
  -> OWNER_PENDING_MANUAL
  -> OWNER_CREATED_2FA_PENDING
  -> OWNER_2FA_VERIFIED
  -> WORKFLOWS_IMPORTED_INACTIVE
  -> CREDENTIALS_BOUND_INACTIVE
  -> MOCK_VERIFIED
```

State is determined only by an exact-version supported n8n UI/API/CLI observation contract established before implementation. Direct metadata DB read/write, undocumented endpoint and scripted password/2FA seed entry are forbidden.

- On `INSTANCE_EMPTY`, wrapper prints loopback URL and one safe next action; owner creates exactly one local owner manually.
- Raw email, password, 2FA secret/recovery material never enters arguments, chat, logs, screenshots or evidence.
- If owner already exists and the expected pseudonymous owner/2FA state matches, onboarding is no-op.
- Zero owner after claimed initialization, multiple owners, owner identity drift, disabled 2FA after readiness or unsupported recovery state is `BLOCKED_V5_ONBOARDING_DRIFT`.
- Account recovery uses only upstream-supported exact-version runbook after complete backup/manual gate. Direct SQL reset is forbidden.

### 9.2. Inactive workflow import

Import input is a secret-free, checksummed exact-version export plus manifest:

```text
logical_workflow_id, export_sha256, n8n_version, active=false,
allowed_node_types, required_credential_slots, trigger_classes,
expected_normalized_hash
```

Before import, static validator rejects secrets, active workflows, unsupported/community/custom nodes, Code/Execute Command/arbitrary HTTP nodes outside reviewed mock contract, embedded recipient IDs/routes and credential IDs. Import runs first only in `mock`, as inactive. Supported n8n importer/API must preserve inactive state. Post-import inventory must equal expected IDs/count/hashes; duplicates, missing entries or drift block rather than overwrite/delete.

Repeated setup on fresh/persistent instance is either exact no-op or explicit owner-approved reconciliation producing a before/after diff. It never creates duplicate owner/workflow/credential objects.

### 9.3. Credential slots and activation

Repository stores only logical slots such as `APP_DB_RUNTIME`, `MEMORY_DB_RUNTIME` and mock endpoints. Exact local credential object IDs and keyed fingerprints live in protected control state; values remain only in n8n encrypted credential store or V3 secret root.

Telegram bot token is never an n8n Credential in this architecture. Only `telegram-bridge` receives it; all real outbound Telegram traffic passes through V6 bridge/proxy. n8n receives a narrow `automation_runtime` PostgreSQL credential and/or authenticated internal adapter contract sufficient only for approved claim/enqueue procedures; it cannot read raw route, mutate arm/cap/offset or call Bot API directly.

Binding is allowed only while workflows remain inactive. Wrapper verifies all required slots resolved, all unexpected slots absent, mock manual execution succeeds and exports remain secret-free. Real trigger activation is a separate V6 manual gate, time-bounded arm and exact workflow inventory decision; no workflow is activated merely by import or mode switch.

## 10. V5-008 — project-scoped objects, restart и persistence

1. Local volumes omit top-level explicit `name:` and are created by Compose under fixed project `n8nagents-local`; expected engine names and labels are derived and recorded after render, not guessed.
2. Every container/network/volume has full label tuple: plan, authority, project, mode/config hash, resource class, and persistent/disposable classification. Missing/extra/conflicting labels block adoption and cleanup.
3. `local`, `gate` and `restore` projects never share volume IDs/mountpoints. Gate cannot mount local application volumes even read-only unless a separate exact contract explicitly changes scope; current design forbids it.
4. Start/stop/restart preserves `local_postgres_data`, `local_n8n_data`, `local_n8n_files` and the explicitly non-authoritative `local_bridge_state`. Persistence acceptance creates synthetic DB/workflow/credential/file canaries, restarts project and Docker Desktop, and verifies supported semantic access/decryptability; authoritative bridge continuity is proven from PostgreSQL, not the cache volume.
5. PostgreSQL/n8n health after daemon restart must revalidate migration and key IDs. Restart policy alone never yields READY.
6. Cleanup selects only run-scoped disposable objects with exact V4/V8 labels and dry-run inventory. Persistent volumes are absent from cleanup operation manifests.
7. No Caddy, public edge, host port 5432, host bridge/proxy port or `0.0.0.0/[::]` publication is present in any render.

## 11. V5-009 — status, result schema и return codes

V5 contributes component substates to the global versioned result envelope. Final integrator must reconcile naming with V1/V3/V4/V6; conflict is `BLOCKED_CONTRACT_DRIFT`.

Required redacted fields:

```yaml
schema: n8nagents.v5-runtime-result/v2
run_id: <uuid>
requested_mode: mock | real-dev | gate | stop | status
resolved_mode: STOPPED | MOCK | REAL_TG | REAL_TG_DEEPSEEK | GATE
project_ref: <allowlisted pseudonymous ref>
compose_lock_sha256: <sha256>
rendered_config_sha256: <sha256|null>
mode_lock_sha256: <sha256>
db_lock_sha256: <sha256>
n8n_lock_sha256: <sha256>
state: <V5 enum>
services: {<service>: {state, health, restart_count, image_ref}}
one_shots: {<service>: {exit_code, completed_at_utc, evidence_ref}}
migration: {expected, applied, checksum_state, dirty}
owner_state: <redacted enum>
workflow_inventory_sha256: <sha256|null>
volume_set_sha256: <sha256|null>
decision: PASS | READY_FOR_MANUAL_GATE | BLOCKED | FAIL | STOP
rc: <integer>
mutation_started: <bool>
failed_predicates: [<stable IDs>]
evidence_refs: [<EV-V5 IDs>]
next_safe_action: <one stable action ID>
```

| RC | Status | Meaning |
|---:|---|---|
| `0` | `STOPPED_VERIFIED`, `MOCK_READY`, `REAL_TG_ARMED_READY`, `REAL_TG_DEEPSEEK_ARMED_READY`, `GATE_COMPLETE` | exact scoped postconditions only |
| `10` | `READY_FOR_MANUAL_GATE` | owner action/gate needed; no unauthorized mutation |
| `36` | `BLOCKED_MANUAL` | missing owner/secret/2FA/arm decision |
| `41/42/43/44/45` | inherited V1/V3 block | endpoint/drift/project/port/storage |
| `51/52/53/61` | inherited integrity/scope/security/operation failure | global fail-closed semantics |
| `64` | `BLOCKED_V5_MODE` | mixed/forbidden transition or gate while local active |
| `65` | `BLOCKED_V5_RENDER` | render differs from lock |
| `66` | `FAILED_V5_POSTGRES_HEALTH` | bounded PostgreSQL health/identity failure |
| `67` | `FAILED_V5_BOOTSTRAP` | logical bootstrap or grant assertion failure |
| `68` | `FAILED_V5_MIGRATION` | project migration/checksum/atomicity failure |
| `69` | `FAILED_V5_N8N_READINESS` | n8n migration/readiness/restart bound failure |
| `71` | `BLOCKED_V5_CONFIG` | non-allowlisted/unsupported config or SQLite/queue/custom node |
| `72` | `BLOCKED_V5_VOLUME_IDENTITY` | label/collision/UID/GID/mode drift |
| `73` | `BLOCKED_V5_ONBOARDING_DRIFT` | owner/2FA/workflow/credential lifecycle mismatch |
| `74` | `BLOCKED_V5_UPDATE_COMPATIBILITY` | update/rollback path not proven |
| `75` | `FAILED_V5_DEPENDENCY_LOOP` | restart/recovery exceeds bound |
| `76` | `BLOCKED_V5_OBJECT_DRIFT` | unknown/extra/mislabelled project object |
| `77` | `BLOCKED_V5_MIGRATION_POLICY` | dirty/ahead/non-transactional migration state |

Unknown field/status, missing required evidence, stdout `PASS` with nonzero child, zero RC with unhealthy/extra service or schema mismatch makes caller return `STOP_RESULT_INVALID`.

## 12. V5-010 — migration-safe update и rollback

### 12.1. Common preconditions

Every n8n/PostgreSQL/Compose/config update is a separate owner-approved operation and depends on V2 current/new image locks and V3 `COMPLETE+RESTORE_VERIFIED` pre-upgrade generation. Source volumes are stopped and never mutated by rehearsal.

Procedure:

1. verify current exact digests, schema/migration/key/volume identity;
2. freeze writes and create verified pre-upgrade backup;
3. restore into unique cloned project/volumes with no real egress, ports or active triggers;
4. verify from/to compatibility from authoritative exact-version evidence;
5. run bootstrap/project migrations and n8n vendor migration against clone only;
6. run permission, workflow, credential decryptability, persistence and regression acceptance;
7. promote only through explicit owner gate and exact object transition plan; original generation remains LKG;
8. on failure quarantine clone evidence and restore old exact version from pre-upgrade generation into new clean volumes.

Never start old n8n against forward-migrated clone/source. Image replacement over migrated state is not rollback.

### 12.2. n8n patch/minor update

Requires supported version path, changed config/default diff, node/workflow compatibility scan, vendor migration inventory, owner/2FA/login, inactive import roundtrip, credential decryptability and mock execution. Real-dev remains disarmed until V6 regression.

### 12.3. PostgreSQL major update

Direct reuse of `local_postgres_data` by a different major is rejected before container start. Use only an exact supported logical dump/restore or reviewed `pg_upgrade` procedure with both versions/tools locked. Recreate roles, memberships, owners, grants, extensions and databases, then run all V5 permission/schema tests. Promotion failure restores the pre-upgrade generation in new volumes; destructive deletion of old volumes is a later manual gate.

Config-only changes that alter DB/backend/execution/topology/key/paths are treated as migrations, not routine restart.

## 13. Manual gates

| Gate | Before | Exact owner decision |
|---|---|---|
| `MG-V5-PLAN` | any V5 implementation/runtime | frozen full plan v2 hash and V5 locks |
| `MG-V5-REPO-WRITE` | create Compose/scripts/migrations/workflow exports | exact touchset/preconditions/custody; owned by integration domain |
| `MG-V5-DB-SECRETS` | first logical bootstrap/password rotation | secret slots, custody and role set; values never in approval |
| `MG-V5-N8N-KEY` | first n8n boot/restore | instance-key ID, independent custody and volume-set binding |
| `MG-V5-OWNER-ONBOARD` | owner creation and 2FA | owner manually completes loopback UI; no automation of credentials/2FA secret |
| `MG-V5-WORKFLOW-RECONCILE` | any non-no-op inventory drift | exact inactive add/update set; no silent overwrite/delete |
| `MG-V5-REAL-DEV` | real-dev start/trigger activation | current V6 bot/recipient/data/cap/time arm; not implied by V5 |
| `MG-V5-UPDATE` | n8n/PostgreSQL/config migration | exact from/to locks, backup+restore proof, clone results, rollback limits |
| `MG-V5-VOLUME-DELETE` | any volume deletion | exact object IDs/labels/backup/recovery effect; outside normal lifecycle |

Missing, expired or hash-mismatched gate returns RC `10/36`. One gate does not imply another.

## 14. Acceptance tests, negative canaries и evidence

All tests are future obligations. Fixture/static tests may run before installation under their own authority; Docker/runtime tests only after approved execution gates. Every record is secret-free, schema-valid, SHA-256-bound and tied to exact plan/runtime locks.

| ID | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `AT-V5-001` | fresh/repeated mock, both real-dev submodes, all full-drain transitions, daemon restart and stop converge to exact service/network/volume sets | `NC-V5-001`: mixed profiles, hot-enable DeepSeek, extra file/env, direct real service target, implicit `.env`, alternate project and stale mode record block before mutation | `EV-V5-001` Compose argv/render/convergence ledger |
| `AT-V5-002` | slow/restarting dependencies remain bounded; downstream starts only after successful one-shots/readiness | `NC-V5-002`: PG timeout, failed/partial migration, delayed n8n, repeated restart and forged health prevent READY | `EV-V5-002` dependency timeline, health and restart ledger |
| `AT-V5-003` | empty and existing clusters produce exact roles/grants/default ACL/search paths; runtime positive/negative permission matrix passes | `NC-V5-003`: cross-schema DML/DDL, PUBLIC privilege, prohibited role attribute, checksum change and unexpected object block | `EV-V5-003` redacted DB authority/grant/migration ledger |
| `AT-V5-004` | pinned n8n runs regular/PostgreSQL/non-root, survives restart and decrypts canary credential with stable key | `NC-V5-004`: SQLite artifact, queue/Redis key, missing/substituted key, unsupported env, writable custom node or UID/GID drift blocks before READY | `EV-V5-004` n8n effective-config/process/volume/key-ID ledger |
| `AT-V5-005` | supported n8n and PostgreSQL upgrades succeed on clones; injected failure restores exact pre-upgrade generation | `NC-V5-005`: old n8n on migrated state, PostgreSQL major data-dir reuse, absent restore proof or from/to incompatibility blocks before source mutation | `EV-V5-005` update rehearsal, migration and rollback ledger |
| `AT-V5-006` | crash before/after bridge ACK/offset operations yields V6-documented bounded duplicates and consistent restored offset/dedup state | `NC-V5-006`: offset/cap/route update outside fenced procedure or backup generation mismatch blocks real-dev | `EV-V5-006` bridge DB procedure/consistency marker ledger, redacted |
| `AT-V5-007` | setup twice on fresh and twice on persistent state keeps one owner, stable workflow inventory, inactive import and explicit credential slots; mock roundtrip passes | `NC-V5-007`: active import, unsupported/custom node, duplicate/drifted workflow, missing credential or Telegram token in n8n blocks activation | `EV-V5-007` onboarding/workflow/credential inventory hashes and manual attestations |
| `AT-V5-008` | all operational images/stages resolve locked linux/amd64 identities; offline restart uses local verified content | `NC-V5-008`: tag-only/latest, wrong arch/config digest, unlocked one-shot/helper image or unreviewed node package blocks render/start | `EV-V5-008` image coverage/render-to-V2-lock ledger |
| `AT-V5-009` | local/gate/restore project objects have disjoint IDs/mounts and restored volumes are writable only by expected non-root identities | `NC-V5-009`: collision, explicit external name, missing/conflicting label, foreign/non-empty volume or cleanup selector overlap blocks without deletion | `EV-V5-009` project object/label/mount/ownership ledger |
| `AT-V5-010` | status/doctor returns deterministic states/RC and one safe action for failed migration, unhealthy n8n and stale prior mode | `NC-V5-010`: zero RC with missing service/row/evidence, stdout PASS/nonzero child, unknown state or secret-bearing diagnostic is rejected | `EV-V5-010` schema-validation and operator recovery transcript, redacted |

## 15. Traceability к source findings

V5 принимает первичное владение только десятью findings domain R4. Cross-domain support не означает, что V5 закрывает findings других reviewers.

| Source finding | V5 contract | Acceptance | Canary | Evidence | Design disposition |
|---|---|---|---|---|---|
| `R4-F01` | `V5-001`, `V5-002` | `AT-V5-001` | `NC-V5-001` | `EV-V5-001` | `DESIGN_CLOSED`; runtime pending |
| `R4-F02` | `V5-003` | `AT-V5-002` | `NC-V5-002` | `EV-V5-002` | `DESIGN_CLOSED`; runtime pending |
| `R4-F03` | `V5-004`, `V5-005` | `AT-V5-003` | `NC-V5-003` | `EV-V5-003` | `DESIGN_CLOSED`; exact SQL pending implementation review |
| `R4-F04` | `V5-006` | `AT-V5-004` | `NC-V5-004` | `EV-V5-004` | `DESIGN_CLOSED`; exact-version key support pending V2 acquisition |
| `R4-F05` | `V5-010` | `AT-V5-005` | `NC-V5-005` | `EV-V5-005` | `DESIGN_CLOSED`; upgrade rehearsal pending |
| `R4-F06` | `V5-004`, `V5-005`, V6 bridge semantics | `AT-V5-006` | `NC-V5-006` | `EV-V5-006` | `DESIGN_CLOSED_WITH_CROSS_DEP`; V6 schema lock pending |
| `R4-F07` | `V5-007` | `AT-V5-007` | `NC-V5-007` | `EV-V5-007` | `DESIGN_CLOSED`; owner/manual runtime pending |
| `R4-F08` | `V5-001`, V2 OCI lock | `AT-V5-008` | `NC-V5-008` | `EV-V5-008` | `DESIGN_CLOSED_WITH_CROSS_DEP`; V2 runtime lock pending |
| `R4-F09` | `V5-008`, V3/V4 object custody | `AT-V5-009` | `NC-V5-009` | `EV-V5-009` | `DESIGN_CLOSED_WITH_CROSS_DEP`; runtime IDs pending |
| `R4-F10` | `V5-009` | `AT-V5-010` | `NC-V5-010` | `EV-V5-010` | `DESIGN_CLOSED`; global schema integration pending |

## 16. Cross-domain dependencies

1. **V1 Windows/control plane:** `V1-001` approved local daemon guard, project allowlist, endpoint drift and port result are mandatory before render/mutation. V5 never changes global context.
2. **V2 supply chain:** every service, one-shot/helper image, Dockerfile stage, parser, migration tool and readiness probe binary must appear in V2 OCI/tool lock. Exact n8n/PostgreSQL config/version compatibility is acquired there.
3. **V3 resources/storage/backup:** roots, named-volume identity, UID/GID restore behavior, compute/log limits, encryption-key custody, backup consistency and clone/restore operations come from V3. V5 supplies writer inventory and DB logical unit.
4. **V4 isolation/network/privilege:** final network names, internal/uplink rules, proxy-only egress, mounts, root one-shot capability and containment evidence are V4-owned. V5 render must consume exact V4 lock; draft expectation is not authority.
5. **V6 Telegram/security:** arm/disarm/drain/emergency state, token custody, bridge/proxy behavior, destination allowlist and `bridge` schema/procedure semantics are V6-owned. V5 owns SQL migration/grant realization after V6 interface freeze. n8n has no token/direct Bot API.
6. **B2r/O5/evidence:** gate candidate, runner/result schema, no-NIC proof, cleanup labels and evidence custody come from V8. V5 only enforces separate project/no application volume.
7. **Repo integration:** exact paths, line endings, file modes, touchset/candidate/commit/package are R9/integration-owned. This design does not authorize repo changes.
8. **Operability:** final `lab` command grammar, emergency runbook and black-box owner handoff are V10-owned. V5 exports deterministic lifecycle/status primitives.

Any missing or contradictory cross-domain lock produces `BLOCKED_CONTRACT_DRIFT`, not a local assumption or fallback. Plan B/VPS are never selected.

## 17. Residual risks и stop triggers

| Risk | Disposition |
|---|---|
| Exact n8n 2.36.7 variable names/defaults/readiness/secret-file support are not runtime-verified in this design task | V2 authoritative-source and image tests required before implementation; unknown = RC 71 |
| n8n must own/migrate its isolated metadata schema | Accepted product-bound residual only inside dedicated DB; clone upgrade/backup required |
| `N8N_SECURE_COOKIE=false` is required only if exact loopback HTTP setup needs it | Must be exact-version reviewed; remote/non-loopback access forbidden; otherwise select supported safer local setting |
| Docker restart behavior and application reconnection may differ by exact Engine/Compose/image | Runtime fault matrix required; no readiness claim from YAML alone |
| V6 bridge schema/procedure signatures were not frozen when V5 draft started | Draft semantics now reconciled to V6; migration implementation remains blocked until canonical V6 hash and locked PostgreSQL HMAC/verifier support are integrated |
| V4 graph gives `telegram-bridge` no direct DB membership, while V6/V5 require `bridge_runtime` procedures | `BLOCKED_CONTRACT_DRIFT`: canonical integration must add one reviewed DB-only bridge path without giving bridge general n8n/uplink reach; no runtime render until V4 network hash is revised |
| V4 calls the secretless Telegram broker `egress-telegram`, while current V6 cross-table says `telegram-egress-proxy` | `BLOCKED_CONTRACT_DRIFT`: one exact service key must be chosen in revised frozen V4/V6; aliases/duplicate services are forbidden |
| Owner/2FA recovery may require version-specific manual upstream flow | No direct SQL workaround; owner gate and backup first |
| Queue/task-runner/custom node might later be requested | Explicit scope expansion and new review; current plan blocks |

Immediate STOP triggers include: mixed modes; local stack active before gate; unknown object/volume; render drift; PostgreSQL public bind; SQLite; queue/Redis; absent/changed n8n key; unreviewed node/package; failed/dirty/ahead migration; owner/workflow drift; direct Telegram credential/API in n8n; old image against migrated state; any Caddy/public edge; any plan B/VPS requirement.

## 18. Реализация и Definition of Done V5

Sequential order after full plan approval and relevant manual gates:

1. freeze V1–V6 cross-contract IDs and V5 records;
2. create repo artifacts in isolated integration workflow under exact touchset;
3. validate Compose renders/negative fixtures without secrets;
4. acquire/verify all images/tools via V2;
5. qualify volumes, networks, limits and one-shot privileges via V3/V4;
6. test empty/existing PostgreSQL bootstrap, migrations and role matrix;
7. test n8n config/key/UID/GID/persistence and no SQLite/queue/custom nodes;
8. owner performs manual owner/2FA onboarding;
9. import/bind inactive workflows and run mock lifecycle twice plus Docker restart;
10. only under V6 arm, run bounded real-dev lifecycle and emergency/disarm tests;
11. run clone upgrade failure/rollback and cold restore dependencies;
12. publish all EV-V5 records and independent review exact implementation.

V5 design is ready for integration when:

- all R4 findings map one-to-one to contract/AT/NC/EV as in §15;
- exact Compose argv/mode/object/state/RC contracts have no ambiguous default;
- PostgreSQL authority and migration model has no implicit PUBLIC/cross-schema access;
- n8n is explicit PostgreSQL/regular/non-root with pre-boot key continuity;
- owner/workflow/credential lifecycle cannot activate real behavior implicitly;
- update rollback restores pre-upgrade data, not images over migrated data;
- V4/V6 pending interfaces are integrated by hash before canonical plan freeze;
- document formatting checks pass: UTF-8 no BOM, LF only, one final LF.

No runtime item is `PASS` as a result of this document alone.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[02_V1_WINDOWS_CONTROL_PLANE]]
- [[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]
- [[04_V3_RESOURCE_STORAGE_BOUNDARY]]
- [[05_V4_ISOLATION_NETWORK_EXPOSURE]]
- [[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]
