---
id: "n8nagents-plan-v2-cross-domain-integration-a64a14c3"
тип: "решение"
статус: "черновик"
проект: "AgentSystem"
владелец: "cross-domain-integration-owner"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[00_FINDINGS_BASELINE]]"
  - "[[01_BASELINE_AUDIT]]"
  - "[[02_V1_WINDOWS_CONTROL_PLANE]]"
  - "[[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]"
  - "[[04_V3_RESOURCE_STORAGE_BOUNDARY]]"
  - "[[05_V4_ISOLATION_NETWORK_EXPOSURE]]"
  - "[[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]"
  - "[[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]"
  - "[[08_V7_SECRETS_PRIVACY_INCIDENT]]"
  - "[[09_V8_BACKUP_COLD_RESTORE]]"
  - "[[10_V9_CANDIDATE_EVIDENCE_GIT_CUSTODY]]"
  - "[[11_V10_OWNER_OPERABILITY]]"
доказательства: []
теги: ["n8nagents", "plan-v2", "integration", "contracts", "docker-desktop", "a-only"]
---

# N8NAgents plan V2 — cross-domain integration decisions

## 0. Статус и граница решения

Это design-only integration record. Он создаёт решения для будущей сборки единого plan V2, но **не** является canonical plan, approval на исполнение или runtime evidence. Никакие download, installation, Windows/WSL/Docker/VPS mutation, network/provider call, secret read/write, repository integration, commit, backup, container start или расход этим документом не разрешены и не объявлены выполненными.

Scope остаётся строго **A-only**: локальный Docker Desktop со штатным WSL 2 backend. Отдельный WSL distro, VM, plan B, VPS, production и remote Docker не являются fallback. Если обязательная capability отсутствует, соответствующий scope получает честный `BLOCKED`; permissions не расширяются.

Design integration status: `RESOLVED_FOR_CANONICAL_PLAN_REWRITE_REVIEW`.

Runtime status: `NOT_RUN`.

Известный scoped outcome: строки O5, которым нужны root, `CAP_SYS_ADMIN`, privileged, device или backend access, остаются `OFFLINE_BLOCKED_CAPABILITY`. Это не LAB/LOCAL failure и не OFFLINE PASS.

## 1. Замороженные входы

Алгоритм aggregate: для файлов, отсортированных ordinal ASCII по имени, `SHA256(UTF8(name + TAB + bytes + TAB + sha256 + LF))`.

`input_set_sha256 = 21f3e3ad4f84792e2f6a7564d7eaeb52a0517774ec4c379dcef09927ef4a52cd` (`1249` bytes canonical list).

| Input | Bytes | SHA-256 |
|---|---:|---|
| `00_FINDINGS_BASELINE.json` | 213739 | `934c449aa75ad157b1702afefcbaac4eab80b750801f172226d065b5a528c4aa` |
| `01_BASELINE_AUDIT.json` | 7607 | `7e7d49eb0b24272ca914330f60d251bafe28bcbb8ad24a82ceb14b13be80a147` |
| `02_V1_WINDOWS_CONTROL_PLANE.md` | 52779 | `32e7b3934453fa5f7e15d76a17e7d1b11503ece597411e69423c65163c79e204` |
| `03_V2_SUPPLY_CHAIN_LICENSE_DRIFT.md` | 45092 | `c25ed30d5254ec24321d08267ffe17858cc597b0ce5975da60d7398b182fb540` |
| `04_V3_RESOURCE_STORAGE_BOUNDARY.md` | 67220 | `80c3c59c1223b33721a98685b570f9df62fbe6e69985de7bb4deaf612b7a3cc2` |
| `05_V4_ISOLATION_NETWORK_EXPOSURE.md` | 67630 | `23a9b50090ce0a42427ded20969f0196f4cc0f4816978dbe6856733b8b36e032` |
| `06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE.md` | 57753 | `634a4fc29800c890387d3da8c0aca5c20e58d2e2dca59f484c94473b01c54f70` |
| `07_V6_TELEGRAM_CORRECTNESS_SECURITY.md` | 64124 | `7b20ea0656752fee8435021f606899a909cc895bccaf9203bb160f1cf8f6b803` |
| `08_V7_SECRETS_PRIVACY_INCIDENT.md` | 65158 | `ef1abe5496815d329e963ab795ac8493d743ef2946249d064082841a4a7f1a2b` |
| `09_V8_BACKUP_COLD_RESTORE.md` | 67199 | `10c4c01b01a7d7a6e50177144e5944465be0c11b7ca397f0bbe1091ce902ca42` |
| `10_V9_CANDIDATE_EVIDENCE_GIT_CUSTODY.md` | 64894 | `4c960555002b2ae58dc7872f626ba7c7784d024d4fdb35daa8c1cd9ecac2744a` |
| `11_V10_OWNER_OPERABILITY.md` | 65703 | `6ed5d528b7828c89c6ff7b009f9a843126e719ab92f45358069bcf5c3eea16db` |

V0 audit state: `PASS`, `114/114` unique findings, baseline SHA-256 указан выше. Эти хеши — inputs решений ниже; изменение любого input требует нового integration record, а не silent edit.

## 2. Реестр явных cross-domain конфликтов

| Conflict ID | Явные источники | Суть | Решение |
|---|---|---|---|
| `XD-CONFLICT-01-NUMBERING` | `DRIFT-V7-01`, `DRIFT-V10-05`, V8 §16, V9 §19.2(1), stale V1/V4/V5 cross-tables | Backup/evidence/secrets owners названы разными V-номерами. | `XD-02` |
| `XD-CONFLICT-02-BRIDGE-DB` | V5 §6.2/§6.3/§17, V6 §1/§7/§18, `DRIFT-V7-02`, `DRIFT-V10-01` | V5 даёт bridge DB role/path; V4/V6 запрещают. | `XD-07` |
| `XD-CONFLICT-03-SERVICE-KEY` | V5 §17, V6 §1/§18, `DRIFT-V7-03`, `DRIFT-V10-02` | `egress-telegram` против stale `telegram-egress-proxy`. | `XD-06`, `XD-08` |
| `XD-CONFLICT-04-FILE-TRANSPORT` | V5 §8.1, `DRIFT-V7-04` | Generic `_FILE`/entrypoint choice не qualified. | `XD-10` |
| `XD-CONFLICT-05-PRIVACY` | V3 `DM-V3-07`/§9, V6 §6/§13, `DRIFT-V7-05` | «raw body не хранится» против protected inbox/outbox до 24 h. | `XD-11`, `XD-12` |
| `XD-CONFLICT-06-AUTOMATION-SECRET` | V5 §9.3, V6 secret matrix, `DRIFT-V7-06` | `automation_runtime` одновременно назван n8n Credential и entrypoint/file secret. | `XD-10` |
| `XD-CONFLICT-07-ARM-ORDER` | V0 `R10-F01`, V6 §3, `DRIFT-V10-03` | Read-only API preflight «до arm» против zero API without arm. | `XD-09` |
| `XD-CONFLICT-08-GLOBAL-RESULT` | V1 §12, V2 §2.3, V3 §3, V4-C12, V5-009, V6 §15, V7-C13, V8 §13, V9-C12, V10-C02, `DRIFT-V10-04` | Overlapping RC и разные schemas/statuses. | `XD-04`, `XD-05` |
| `XD-CONFLICT-09-CANONICALIZATION` | V2 JCS, V1/V3–V8 prose variants, V9 §19.2(3) | Hash inputs могут означать разные bytes. | `XD-03` |
| `XD-CONFLICT-10-CANDIDATE-TRANSFER` | V4 candidate-to-volume, V9 §19.2(2) | Generic Docker archive/copy не равен immutable candidate. | `XD-13` |
| `XD-CONFLICT-11-O5-CAPABILITY` | V4-C10/C12, V9 §19.2(5), V10 residual 10 | A-only запрещает часть O5 requirements. | `XD-05` |
| `XD-CONFLICT-12-GATE-IDENTITIES` | V5 `gate-runner`, V9 §19.2(6) | Один service key скрывает runner, два validator и collector. | `XD-13` |
| `XD-CONFLICT-13-EVIDENCE-AUTHORITY` | V8-C15, V9-C14/§19.2(7) | Backup и run evidence предлагают конкурирующие final truth. | `XD-14` |
| `XD-CONFLICT-14-DIRTY-INTEGRATION` | V9 §15/§19.2(8) | Promotion в checked-out branch меняет semantics 21 dirty paths. | `XD-14` |
| `XD-CONFLICT-15-BACKUP-MOUNT` | V4 mount deny, V8 §16(4) | Backup нужен exact read-only source mount, но V4 row не frozen. | `XD-12` |
| `XD-CONFLICT-16-BRIDGE-AUTHORITY` | V3 `DM-V3-07`, V5/V6/V8 | `local_bridge_state` или PostgreSQL против единственного durable authority. | `XD-07`, `XD-12` |
| `XD-CONFLICT-17-MODE-NAMES` | V4-C09, V5 §1/§3, V10 owner grammar | Generic `real-dev`/profile classes и exact runtime states расходятся. | `XD-06` |
| `XD-CONFLICT-18-BACKUP-PAYLOAD` | V6/V7 TTL, V8 full DB dump | Full DB backup может удержать payload дольше 24 h. | `XD-11`, `XD-12` |
| `XD-CONFLICT-19-GATE-ROUTING` | V1–V9 manual gates, V10 §15 | Дублирующие owner prompts могут быть ошибочно объединены или implied. | `XD-15` |
| `XD-CONFLICT-20-BACKUP-KEY-TYPE` | V7 `V7-S11`/`V7-C12`, V8 §7/§16(7) | Generic/symmetric `backup-AEAD-key` против exact age X25519 private identity. | `XD-12` |

Explicit semantic conflicts found: `20`. Ни один не разрешается union permissions.

## 3. `XD-01` — A-only authority и integration lock

**Inputs/hashes:** весь `input_set_sha256`; особенно V1 `32e7…e204`, V4 `23a9…e032`, V9 `4c96…744a`, V10 `6ed5…16db`.

**Affected:** `V1-000/V1-000A`, `V4-C01`, `V5` invariants 1–4, `V9-C01/C03/C12`, `V10-C01/C02`; findings `R1-WIN-001`, `R3-CTRL-005`, `R8-P1-006`, `R9-F01..04`, `R10-F08/F11`.

**Canonical interface schema / decision:** every later plan, authority, command, result and evidence record consumes one immutable `integration_lock/v2`:

```yaml
schema: n8nagents.integration-lock/v2
scope_policy: A_ONLY_DOCKER_DESKTOP_WSL2_BACKEND
input_set_sha256: 21f3e3ad4f84792e2f6a7564d7eaeb52a0517774ec4c379dcef09927ef4a52cd
canonical_plan_sha256: <future exact hash>
section_map_sha256: <XD-02>
canonicalizer_registry_sha256: <XD-03>
global_result_schema_sha256: <XD-04>
service_network_mode_lock_sha256: <XD-06>
owner_decision_policy_sha256: <XD-15>
forbidden_fallbacks: [SEPARATE_WSL_DISTRO, VM, PLAN_B, VPS, REMOTE_DOCKER, PRODUCTION]
```

Any unknown/mismatch is `G_BLOCKED_CONTRACT_DRIFT`; no action can self-update this lock.

**Rejected:** implicit latest draft; «stricter prose wins» without a frozen interface; fallback to VPS/plan B; runtime inference from design text.

**Rationale:** one hash root prevents domain sections from independently choosing topology, permissions or result meaning.

**AT/NC/EV:** `AT-XD-01` validates every downstream record binds the same lock. `NC-XD-01` changes one input/section hash and requires zero mutation. `EV-XD-01-INTEGRATION-LOCK` contains only hashes, schema IDs and mismatch predicates.

**Residual:** the future canonical plan hash does not yet exist. This is a design dependency, not runtime PASS.

## 4. `XD-02` — canonical section numbering и ID namespace

**Inputs/hashes:** V1–V10 hashes from §1; explicit `XD-CONFLICT-01`.

**Affected:** all cross-tables; `DRIFT-V7-01`, `DRIFT-V10-05`, V8 §16, V9 §19.2(1); no independent V0 finding, with material support to `R8-P1-006`, `R8-P1-010`, `R10-F08`.

**Canonical interface schema / decision:** canonical ownership is fixed:

| Section | Owner |
|---|---|
| `V1` | Windows / Docker Desktop control plane |
| `V2` | supply chain / license / drift |
| `V3` | resources / storage boundary |
| `V4` | isolation / network / exposure |
| `V5` | Compose / PostgreSQL / n8n lifecycle |
| `V6` | Telegram / DeepSeek correctness |
| `V7` | secrets / privacy / incident |
| `V8` | backup / cold restore |
| `V9` | candidate / evidence / Git custody |
| `V10` | owner operability |
| `XD` | cross-domain interfaces only |

Canonical IDs use `V01..V10` in machine records: `VNN-CNN-SLUG`, `AT-VNN-NN`, `NC-VNN-NN`, `EV-VNN-NN`, `MG-VNN-*`; integration IDs use `XD-CNN`, `AT/NC/EV-XD-NN`, `MG-XD-*`. Existing source IDs remain immutable `source_aliases`; canonical plan mechanically rewrites references and records an alias map. A source alias is never accepted as an unqualified runtime ID.

**Rejected:** inferring owner from prose number; keeping V7=backup or V8=evidence aliases; renaming only filenames without hashes.

**Rationale:** machine prefixes and owner map eliminate ambiguous authority.

**AT/NC/EV:** `AT-XD-02` resolves every cross-reference to exactly one canonical ID and owner. `NC-XD-02` injects V7=backup/V8=evidence and must fail schema validation. `EV-XD-02-SECTION-MAP` stores alias map and no missing/duplicate references.

**Residual:** canonical rewrite will change all draft hashes and requires full-plan re-review.

## 5. `XD-03` — one canonicalization registry

**Inputs/hashes:** V2 `c25e…540`, V9 `4c96…744a`; `XD-CONFLICT-09`.

**Affected:** V2 two-lock envelope; V5 manifest family; V8 operation/manifest; V9-C06/C07/C14/C16; findings `R2-003/005/012`, `R8-P1-003/010`, `R9-F05/09`.

**Canonical interface schema / decision:** every hashable schema declares exactly one registry entry:

```yaml
schema: n8nagents.canonicalizer-registry/v2
json: RFC8785_JCS_UTF8_NO_BOM
yaml: PARSE_DUPLICATE_REJECT_THEN_JSON_JCS
text: UTF8_NO_BOM_LF_EXACTLY_ONE_FINAL_LF
binary: OPAQUE_BYTES
file_set: V9_LENGTH_PREFIXED_PATH_BYTES_SIZE_SHA256_V2
identifier_compare: UNICODE_NFC_ORDINAL_CASE_SENSITIVE
schema_unknown_fields: REJECT_UNLESS_SCHEMA_EXPLICITLY_ALLOWS
```

YAML bytes may be retained as source evidence, but semantic lock uses duplicate-rejecting parse then JCS. Raw executable/text artifact identity is always raw-byte SHA-256 in addition to any semantic hash. Schema ID and canonicalizer ID are covered by the hash.

**Rejected:** prose-only sorted keys; implementation-native JSON serialization; newline normalization after freeze; one aggregate over ambiguous child hashes.

**Rationale:** hashes become independently reproducible and cross-domain comparable.

**AT/NC/EV:** `AT-XD-03` uses two independent implementations over Unicode, numeric, ordering and YAML-duplicate fixtures. `NC-XD-03` changes EOL/key order/duplicate key/NFC and requires the specified equal-or-reject result. `EV-XD-03-CANONICALIZERS` contains tool hashes, vectors and two-engine agreement.

**Residual:** exact independent tools remain V2 runtime-lock inputs and are currently `UNKNOWN`.

## 6. `XD-04` — global result envelope, collision-free RC и aggregation

**Inputs/hashes:** all domain drafts; V9 `4c96…744a`, V10 `6ed5…16db`; `XD-CONFLICT-08`.

**Affected:** V1 §12, V2 §2.3, V3 §3, V4-C12, V5-009, V6 §15, V7-C13, V8 §13, V9-C12, V10-C02; findings `R4-F10`, `R8-P1-006`, `R10-F08`.

**Canonical interface schema / decision:** only the global collector emits numeric process RC. A child keeps its original code as a namespaced string `native_rc_key` such as `V06:100`; it cannot collide numerically or determine parent success by itself.

```yaml
schema: n8nagents.global-operation-result/v2
run_id: <uuid>
operation_id: <allowlisted>
requested_scopes: [LAB|LOCAL|OFFLINE|RESTORE|DELIVERY|OWNER_HANDOFF]
plan_sha256: <exact>
integration_lock_sha256: <exact>
authority_ref: <nonsecret|null>
decision: PASS|READY_OWNER_GATE|BLOCKED|FAIL|STOP|NOT_RUN
status: <G_* enum>
rc: <global integer>
mutation_started: <bool>
scope_results: {<scope>: {state, status, rc, required, observed_at_utc, valid_until_utc}}
domain_results: [{domain, schema, native_status, native_rc_key, normalized_class, lock_sha256, observed_at_utc, valid_until_utc, evidence_refs, failed_predicates}]
project_summary: READY|PARTIAL_READY|BLOCKED|STOPPED|NOT_EVALUATED
next_safe_action: <one stable ID>
evidence_anchor_sha256: <hash|null>
```

Global RC map:

| RC | Status |
|---:|---|
| `0` | `G_PASS_EXACT_REQUESTED_SCOPES` |
| `10` | `G_READY_OWNER_GATE` |
| `20` | `G_NOT_RUN` |
| `30` | `G_BLOCKED_UNKNOWN` |
| `31` | `G_BLOCKED_CAPABILITY` / `G_PARTIAL_READY_OFFLINE_BLOCKED` |
| `32` | `G_BLOCKED_CONTRACT_DRIFT` |
| `33` | `G_BLOCKED_POLICY` |
| `34` | `G_BLOCKED_RESOURCE` |
| `35` | `G_BLOCKED_IDENTITY` |
| `36` | `G_BLOCKED_DEPENDENCY` |
| `37` | `G_BLOCKED_MANUAL` |
| `40` | `G_FAIL_VALIDATION` |
| `41` | `G_FAIL_OPERATION` |
| `42` | `G_FAIL_CONTAINMENT` |
| `43` | `G_FAIL_INTEGRITY` |
| `50` | `G_STOP_SCOPE_EXPANSION` |
| `51` | `G_STOP_SECURITY` |
| `52` | `G_STOP_RESULT_INVALID` |
| `53` | `G_EMERGENCY_UNVERIFIED` |
| `54` | `G_INCIDENT_OPEN` |

Aggregation is semantic, never `max(rc)`. Precedence is: invalid schema/stale required child → `52`; security → `51`; scope expansion → `50`; open incident → `54`; unverified emergency → `53`; containment/integrity/operation/validation failure → `42/43/41/40`; contract drift → `32`; identity/policy/resource/dependency/capability/unknown/manual → corresponding block; ready gate; not-run; only then PASS. Parent cannot improve a child. Ties retain all predicates and choose deterministic domain-ID order only for `next_safe_action`.

**Rejected:** sharing overlapping child integers at top level; `max()`; stdout `PASS`; V10 best-effort projection; stale evidence reuse.

**Rationale:** one typed collector boundary preserves every child meaning while making cross-domain aggregation deterministic and collision-free.

**AT/NC/EV:** `AT-XD-04` table-tests all domain status pairs and freshness boundaries. `NC-XD-04` covers unknown mapping, duplicate domain, zero RC with blocked child, forged stdout and expired child. `EV-XD-04-GLOBAL-RESULT` contains schema hash, mapping hash and conformance matrix.

**Residual:** legacy child code translations must be generated mechanically and reviewed before implementation.

## 7. `XD-05` — independent LAB/LOCAL/OFFLINE semantics

**Inputs/hashes:** V4 `23a9…e032`, V9 `4c96…744a`, V10 `6ed5…16db`; `XD-CONFLICT-11`.

**Affected:** `V4-C10/C12`, `V9-C12/C13`, `V10-C02/C08`; findings `R3-PRIV-001`, `R8-P1-006/009`, `R10-F08`.

**Canonical interface schema / decision:** `LAB`, `LOCAL` and `OFFLINE` are independent scope results. `OFFLINE_BLOCKED_CAPABILITY` is terminal `BLOCKED`, global RC `31`, and means a mandatory OFFLINE row requested forbidden/unsupported capability under A-only. It is not `SKIPPED`, `MANUAL_PASS`, `OFFLINE_READY` or overall success.

An operation requesting only proven `LAB` or `LOCAL` predicates may return RC `0` even when the project summary states `PARTIAL_READY` and OFFLINE remains blocked. A status request covering all scopes returns `G_PARTIAL_READY_OFFLINE_BLOCKED`, RC `31`. Any delivery/claim requiring OFFLINE includes OFFLINE in `requested_scopes` and cannot PASS.

Example:

```text
LAB=PASS, LOCAL=PASS, OFFLINE=OFFLINE_BLOCKED_CAPABILITY
project_summary=PARTIAL_READY
LAB-only operation rc=0
all-scope or OFFLINE-required operation rc=31
```

**Rejected:** weakening O5 privileges; automatic plan B/VPS; treating blocked rows as not applicable; blocking useful LAB solely because independent OFFLINE is blocked.

**Rationale:** preserves both safety and the user's explicit local laboratory objective.

**AT/NC/EV:** `AT-XD-05` checks all scope combinations and requirement sets. `NC-XD-05` attempts OFFLINE PASS with a blocked required row and attempts general SUCCESS from LAB/LOCAL only. `EV-XD-05-SCOPES` contains row requirement hashes and independent scope results.

**Residual:** full `OFFLINE_READY` remains unavailable until a later owner-approved, reviewed path satisfies those O5 rows; no such path is selected here.

## 8. `XD-06` — canonical service, network и mode names

**Inputs/hashes:** V4 `23a9…e032`, V5 `634a…4f70`, V6 `7b20…b803`, V8 `10c4…ca42`, V9 `4c96…744a`; `XD-CONFLICT-03/17`.

**Affected:** `V4-C05/C09`, `V5-001/002/008`, `V6-C15/C20`, `V8-C03/C11`, `V9-C08..C14`; findings `R4-F01/F02/F09`, `R3-PROFILE-008`, `R5-F14`, `R8-P2-012`.

**Canonical interface schema / decision — running modes:** exact machine enum is `STOPPED | MOCK | PREARM_TG | REAL_TG | REAL_TG_DEEPSEEK | BACKUP | RESTORE | GATE`. `real-dev` may appear only as human category; it is not an accepted manifest/profile value. Direct hot transition is forbidden: every different running mode drains to `STOPPED` first without volume deletion.

**Canonical long-running service keys:** `postgres`, `n8n`, `mock-telegram`, `mock-llm`, `telegram-bridge`, `egress-telegram`, `deepseek-adapter`, `egress-deepseek`. Canonical one-shot/QA keys: `db-bootstrap`, `db-migrate`, `n8n-volume-init`, `db-secret-apply`, `bridge-key-seed`, `real-arm-guard`, `backup-runner`, `restore-postgres`, `restore-validator`, `gate-loader`, `gate-runner`, `validator-a`, `validator-b`, `evidence-collector`. Alias `telegram-egress-proxy` is rejected.

**Canonical network keys and membership:**

| Network | Class | Exact eligible members |
|---|---|---|
| `db` | internal data | `postgres`, `n8n`, bounded DB one-shots; never `telegram-bridge`/egress |
| `mock_tg` | internal synthetic | `n8n`, `mock-telegram` |
| `mock_llm` | internal synthetic | `n8n`, `mock-llm` |
| `telegram_ingress` | internal app ingress | `telegram-bridge`, `n8n` |
| `telegram_proxy` | internal controlled client | `telegram-bridge`, `egress-telegram` |
| `llm_ingress` | internal app ingress | `n8n`, `deepseek-adapter` |
| `llm_proxy` | internal controlled client | `deepseek-adapter`, `egress-deepseek` |
| `uplink` | external | only active `egress-telegram`/`egress-deepseek` |
| `backup_db` | internal backup | exactly `postgres`, `backup-runner` during BACKUP |
| `restore_db` | internal restore | exact restore services only; never source postgres/n8n |

`GATE` uses `network_mode:none` and creates no network. `PREARM_TG` runs only `telegram-bridge` in prearm command mode plus `egress-telegram`, networks `telegram_proxy/uplink`, no n8n/PostgreSQL. `REAL_TG` adds `postgres/n8n` and `telegram_ingress/db`; DeepSeek services/networks exist only in `REAL_TG_DEEPSEEK`. Only n8n publishes `127.0.0.1:5678/tcp`; every other host port is forbidden.

**Rejected:** implicit/default network; generic `real-dev` profile; duplicate alias services; bridge→db membership; egress broker→db/application membership; one generic gate process.

**Rationale:** exact keys make Compose render, network graph, secret mounts, backup writers and owner status refer to the same objects.

**AT/NC/EV:** `AT-XD-06` renders every mode twice and compares exact service/network/port/mount sets. `NC-XD-06` injects alias, default network, extra member, direct service target, mixed mode and stale real container. `EV-XD-06-TOPOLOGY` stores desired/observed bipartite graphs and render hashes.

**Residual:** exact Docker Desktop behavior is untested; any inability to enforce a row blocks the affected scope.

## 9. `XD-07` — bridge has no PostgreSQL route; authenticated internal ingress and one state authority

**Inputs/hashes:** V4 `23a9…e032`, V5 `634a…4f70`, V6 `7b20…b803`, V7 `ef1a…a2b`, V8 `10c4…ca42`; `XD-CONFLICT-02/16`.

**Affected:** `V4-C05/C07`, `V5-004/005/009`, `V6-C04/C07..C12/C19`, `V7-C02/C11`, `V8-C02/C03/C05`; findings `R4-F03/F06`, `R5-F03/F05..F11`, `R6-P1-004`, `R7-F02`.

**Canonical interface schema / decision:** the canonical path is:

```text
telegram-bridge
  -> telegram_ingress HTTP closed operation
  -> exact active n8n internal control workflow
  -> exact checksummed PostgreSQL SECURITY DEFINER procedure
  -> n8nagents_app.bridge durable authority
  -> structured MACed ACK back unchanged through n8n
```

`telegram-bridge` has no `db` membership, DB hostname route, PostgreSQL credential, `bridge_runtime` login role or raw table access. Canonical V5 removes long-running role `bridge_runtime`. n8n holds `automation_runtime`, which has `EXECUTE` only on an enumerated procedure set and no table `SELECT`, DML, DDL, route/cap/arm/offset override or keyring read. Each HTTP method/path maps one-to-one to one procedure; there is no generic procedure name or free parameter map.

PostgreSQL schema `n8nagents_app.bridge` is the sole durable authority for lease/fence, observation/terminal disposition, contiguous offset, authorized inbox, immutable route, idempotency, outbox, send reservations/cap, replay ledger and verifier/ACK keyring. `local_bridge_state` is optional recreatable cache only, ignored for decisions and excluded from backup truth.

n8n receives the MAC-covered envelope only transiently and relays it unchanged. It has no envelope key. PostgreSQL verifies MAC, timestamp, nonce, bot/arm/fence/tuple and replay before persistence or route creation. ACK is created only after commit and is independently MACed. If the exact n8n version cannot prove bounded nonpersistent relay, exact procedure binding or no raw execution/error payload, REAL_TG is `G_BLOCKED_CAPABILITY`; there is no direct-DB fallback and no invented ingress service.

Host emergency/recovery DB operations use a separate time-bounded `control-db` one-shot path/role under owner/incident authority; it is never available to bridge or workflow.

**Rejected:** V5 direct bridge DB-only network; unioning both paths; second DB/offset file; bridge proxying SQL; n8n holding HMAC key; a new unreviewed ingress-verifier service.

**Rationale:** this preserves V4 network least privilege, V6 pre-storage authentication and PostgreSQL durability without broadening bridge authority.

**AT/NC/EV:** `AT-XD-07` covers valid/duplicate/crash-before/after-commit operations, fenced lease and immutable ACK. `NC-XD-07` covers bridge DB DNS/TCP, injected DB credential, forged/replayed/mutated envelope, arbitrary procedure, n8n body persistence and second offset store; all fail before unauthorized durable state. `EV-XD-07-INGRESS-AUTHORITY` stores route/schema/workflow/procedure/grant/network hashes and counts only.

**Residual:** PostgreSQL and approved DB owner become verifier trust members; exact HMAC primitive and n8n relay behavior require V2/V5 runtime proof.

## 10. `XD-08` — sole Telegram egress service

**Inputs/hashes:** V4 `23a9…e032`, V5 `634a…4f70`, V6 `7b20…b803`, V7 `ef1a…a2b`; `XD-CONFLICT-03`.

**Affected:** `V4-C07`, `V5-001/008`, `V6-C12/C13/C20`, `V7-C11`; findings `R3-NET-003`, `R5-F10..F13`, `R6-P1-010`.

**Canonical interface schema / decision:** exact service key is `egress-telegram`; aliases and duplicate services are invalid. Only `telegram-bridge` holds the token and Telegram client logic. It has no uplink; it can reach only `egress-telegram` over `telegram_proxy`. `egress-telegram` has no token, DB/n8n/bridge volume, secret mount or application network; it is the only Telegram-side member of `uplink`.

The broker accepts only the locked exact Telegram origin at port 443, rejects literal IP, alternate port/name, redirect, unsafe DNS RRset and generic proxy use, and does not terminate provider TLS. Destination policy, CA/client/broker digests and exact methods are arm-bound. n8n/PostgreSQL never receive provider route.

**Rejected:** `telegram-egress-proxy`; n8n Telegram node/Credential/Trigger; n8n/bridge direct Internet; one general-purpose broker for Telegram and DeepSeek.

**Rationale:** one name and one outbound path make cap, incident and destination proof exhaustive.

**AT/NC/EV:** `AT-XD-08` proves valid armed method reaches only locked origin. `NC-XD-08` tests alias, sibling domain, direct IP, redirect, DNS rebind, alternate port and n8n raw socket. `EV-XD-08-EGRESS` stores destination-policy/network/image hashes, decision classes and byte counters, never URLs/headers/body/token.

**Residual:** dynamic provider DNS and public CA remain external trust dependencies; uncertainty blocks real traffic.

## 11. `XD-09` — exactly two Telegram arms: PREARM then ACTIVE_ARM

**Inputs/hashes:** V0 baseline `934c…c4aa`, V6 `7b20…b803`, V10 `6ed5…16db`; `XD-CONFLICT-07`.

**Affected:** `V6-C01/C02/C03/C17`, `V10-C06`; findings `R5-F01/F02/F16`, `R10-F01`.

**Canonical interface schema / decision:** provider API state machine has exactly two owner-authorized phases:

1. `PREARM` (`TTL <= 5 min`) — only one `getMe` and one `getWebhookInfo`, no retry unless a new PREARM. It permits no `deleteWebhook`, `getUpdates`, `sendMessage`, DeepSeek request, offset/cap mutation or application start. PREARM binds offline expected dev bot/production deny, token fingerprint, endpoint/destination/runtime hashes. A successful result auto-closes PREARM and produces a redacted identity/webhook snapshot.
2. `ACTIVE_ARM` (`TTL <= 30 min`) — new owner decision bound to successful PREARM snapshot, exact dev bot, five-part tuple, synthetic data class, webhook/backlog action, cap 20/current ledger, workflow/topology/secret/runtime hashes. Its ordered substates are `WEBHOOK_APPLY` (bounded `getWebhookInfo`, optionally exactly one approved `deleteWebhook`; no poll/send) then `POLL_SEND` (`getUpdates`, ledger-authorized `sendMessage`, bounded webhook drift checks; no further webhook mutation). DeepSeek remains separately armed.

Without current matching phase arm, external API call count is zero. The V0 wording «read-only preflight before arm» is dispositioned as **offline preview before PREARM**; actual `getMe/getWebhookInfo` occur only after PREARM. Stop, expiry, reboot/session/daemon/config/tuple/token/workflow drift, cap exhaustion, 409 conflict or incident disarms atomically. Restart never re-arms.

**Rejected:** unarmed read-only exception; three independent owner arms; ACTIVE before verified PREARM; one broad arm with unordered methods; Telegram arm implying DeepSeek.

**Rationale:** two visible decisions satisfy the required separation while retaining transactional webhook ordering.

**AT/NC/EV:** `AT-XD-09` checks exact method counters and ordered transition. `NC-XD-09` attempts getMe unarmed, deleteWebhook/send under PREARM, poll before webhook postcondition, 21st send, stale snapshot and reboot reuse. `EV-XD-09-ARM` contains phase/decision/snapshot hashes, TTL/method/cap counters and disarm proof, no raw IDs/token.

**Residual:** an external poller can ignore local arms; provider 409 detection and owner revoke remain the final containment.

## 12. `XD-10` — exact secret transport for n8n, automation runtime and bridge

**Inputs/hashes:** V5 `634a…4f70`, V6 `7b20…b803`, V7 `ef1a…a2b`, V8 `10c4…ca42`; `XD-CONFLICT-04/06`.

**Affected:** `V5-004/006/007`, `V6-C07/C09/C16`, `V7-C02/C03/C04/C08/C12`, `V8-C07`; findings `R4-F04/F07`, `R5-F09`, `R6-P1-002/003/008`, `R6-P2-011`.

**Canonical interface schema / decision:** no shared `.env`, Compose interpolation value, argv secret, directory secret mount or generic `_FILE` assumption is allowed.

| Secret slot | Runtime consumer | Canonical transport |
|---|---|---|
| Telegram dev token | `telegram-bridge` only | owner-only restricted leaf → RO `/run/secrets/telegram_token`; bridge direct file API |
| bridge request MAC key | bridge + time-bounded `bridge-key-seed` | separate restricted leaf → `/run/secrets/bridge_request_mac_key`; seed writes protected PG keyring |
| bridge ACK MAC key | bridge + time-bounded `bridge-key-seed` | separate independent restricted leaf → `/run/secrets/bridge_ack_mac_key`; no key reuse/implicit derivation |
| `automation_runtime` password | n8n encrypted PostgreSQL Credential | owner-held password-manager value; masked one-shot DB set/rotate ceremony and masked loopback n8n UI binding; no long-running file/env mount to n8n |
| n8n metadata DB password | n8n process | separate restricted leaf; exact native file option if source+runtime qualified, otherwise only reviewed V7 entrypoint fallback |
| `N8N_ENCRYPTION_KEY` | n8n process only | separate persistent restricted leaf and independent owner recovery custody; same native-file/fallback rule |
| cluster admin/app migrator/password rotation credentials | exact one-shots only | individual time-bounded restricted leaves; absent from long-running services |
| n8n owner password/2FA/recovery | owner/browser only | `NO_LAB_FILE`, masked loopback UI/authenticator; never agent/script/SQL |

`bridge-key-seed` is the only provisioning consumer besides bridge; it runs on `db` without uplink/Telegram networks, writes two key IDs/values into `bridge.envelope_keyring`, proves runtime roles cannot read them, then exits and loses mounts. Request and ACK keys are independent 256-bit values. n8n/`automation_runtime` never see either.

The `automation_runtime` credential is canonicalized to **n8n encrypted Credential only**, resolving V7 drift. The owner must keep/recreate it in independent custody for restore/rotation; database login verifiers are not backup authority. Clipboard is prohibited unless its separate V7 gate is satisfied.

For n8n DB password/instance key, native file support must be proved for exact image/config key. If unsupported, the only permitted fallback is a pinned nonroot entrypoint that reads exact files, validates them, exports immediately before `exec`, and has an explicit owner `/proc` exposure gate. Unsupported bridge/Telegram/DB-admin secret transport blocks; it never receives env fallback.

**Rejected:** one HMAC key reused for request/ACK; automation password as entrypoint env; bridge DB password; token as n8n Credential; common secret root mount; secret in Compose `.env`; assumed `_FILE` convention.

**Rationale:** each value has named consumers and a testable transport surface; the n8n workflow can relay but cannot forge control envelopes.

**AT/NC/EV:** `AT-XD-10` uses unique synthetic markers for every slot across render, inspect, `/proc`, sibling containers, logs/evidence, restart and restore. `NC-XD-10` injects shared file/env, wrong consumer, key reuse, unsupported `_FILE`, unsafe clipboard and stale key ID. `EV-XD-10-SECRETS` stores slot IDs, consumer/mount/keyring hashes, visibility classes and keyed fingerprints only.

**Residual:** approved Docker/Windows control principals and PostgreSQL owner can extract runtime/verifier material; n8n fallback exposes values in process memory and is separately owner-accepted.

## 13. `XD-11` — pre-storage authorization, TTL и backup exclusion

**Inputs/hashes:** V3 `80c3…3cc2`, V6 `7b20…b803`, V7 `ef1a…a2b`, V8 `10c4…ca42`; `XD-CONFLICT-05/18`.

**Affected:** `V3-C04/C08/C09`, `V6-C05/C06/C09/C10/C16`, `V7-C05/C06/C11`, `V8-C02/C03/C13`; findings `R5-F04/F07/F08/F15`, `R6-P1-004/005/006`, `R7-F01/F02/F11`.

**Canonical interface schema / decision:**

- Unauthorized or unsupported Telegram raw payload exists only in bounded bridge process memory until classification. It is never sent to n8n/DB/LLM/tools/log/evidence/backup. Durable terminal state contains only `update_id`, closed reason enum, arm/bot/fence refs, classifier version and purpose-keyed aggregate counter; no raw tuple/body.
- Authorized input is projected to a closed normalized schema after exact five-part tuple authorization. Only protected PostgreSQL `bridge.inbox`/work state may retain normalized text and raw route fields required for immutable routing. Outgoing body exists only in protected outbox. `payload_expires_at <= terminal_at + 24h`; a shorter owner policy wins. n8n execution success/error/manual/progress payload retention is zero.
- Logs/evidence/status/support default sources exclude request/response bodies, tuple, text and raw IDs. Evidence contains only hashes/counts/enums/keyed refs. Scanner failure blocks publication.
- Backup default is `PAYLOAD_EXCLUDED`: backup admission requires every payload-bearing authorized inbox/outbox row to be terminal and purged, with zero-row canary. The backup job does not silently delete active work; nonterminal/unexpired rows block and offer explicit drain/purge decision.
- Including authorized content in a generation requires a separate `MG-XD-DATA-BACKUP-<class>` owner decision specifying data class, exact fields, generations, retention/expiry, custody and residual copies. Telegram `ACTIVE_ARM`/synthetic data-class approval alone does not imply backup inclusion.

The canonical correction to V3 §9 is: authorized raw/normalized text may exist only in protected bridge payload fields for at most 24 h; unauthorized raw never persists; derived non-payload metadata follows its own retention. `local_bridge_state` contains no payload.

**Rejected:** no-storage claim contradicted by inbox; unlimited DB retention; n8n execution payload; regex-after-log redaction; full DB backup silently retaining payload; table-selective inconsistent backup.

**Rationale:** preserves durable ACK/outbox correctness while bounding and explicitly governing sensitive content.

**AT/NC/EV:** `AT-XD-11` uses unauthorized/authorized/terminal/expiry/backup-boundary markers. `NC-XD-11` attempts unauthorized storage, n8n execution persistence, log/evidence leak, 24h+ row, and backup with payload but no gate. `EV-XD-11-PRIVACY` contains field-policy hash, row counts/expiry predicates, purge/backup decision and scanner results, never marker values.

**Residual:** secure erase from VHDX/SSD/pagefile/backups is not promised; owner-gated backup inclusion extends residual lifetime.

## 14. `XD-12` — backup/cold-restore inventory, writer boundary и V4 mount row

**Inputs/hashes:** V3 `80c3…3cc2`, V4 `23a9…e032`, V5 `634a…4f70`, V6 `7b20…b803`, V7 `ef1a…a2b`, V8 `10c4…ca42`, V9 `4c96…744a`; `XD-CONFLICT-15/16/18/20`.

**Affected:** `V3-C08..C12`, `V4-C03/C05/C06`, `V5-004/010`, `V6-C19`, `V7-C02/C04/C12`, `V8-C01..C15`, `V9-C14`; findings `R4-F06`, `R7-F01..F12`, `R10-F03`.

**Canonical interface schema / decision:** V4 gains an exact BACKUP operation row, re-hashed before canonical plan freeze:

Backup encryption key semantics are exact: `V7-S11` is specialized as one age X25519 private identity held outside the runtime; capture receives only its derived public recipient. The private identity is supplied by exact per-operation file transport only to the separately trusted COMPLETE verifier or restore reader, never to `backup-runner`, application services or persistent staging. A generic symmetric caller-provided AEAD key, passphrase mode, caller-controlled nonce/salt or dual interpretation is invalid.

- source application mode drains to `STOPPED`; bridge/n8n/mocks/adapters/brokers/migrations/retention/UI writers are absent;
- `postgres` plus one pinned nonroot `backup-runner` are the only members of internal `backup_db`; zero host ports/uplink/provider secrets;
- PostgreSQL logical dump uses authenticated DB access through its dedicated one-shot file secret;
- n8n volumes are mounted read-only by exact volume ID into the backup runner/archive helper; no Windows directory bind, live secret root, repo, Vault or source-writable mount;
- exact source object IDs, readonly flags, writer/session inventory and generation marker are watched throughout capture.

Recoverable inventory is canonical:

| Class | Backup disposition |
|---|---|
| all PostgreSQL DBs/globals/roles/grants/extensions/schema history | full logical capture; login password verifiers excluded/reseeded |
| n8n metadata/workflows/encrypted Credentials | included in `n8n` DB dump |
| n8n data/files volumes | authenticated encrypted archives or runtime-proven ABSENT |
| bridge offset/inbox/outbox/route/cap/lease/replay/keyring | included in full app DB dump; restored arm/lease forced inactive |
| bridge request/ACK source files and Telegram/DeepSeek tokens | excluded; independently re-supplied/rotated before any later arm |
| `N8N_ENCRYPTION_KEY` and age private identity | excluded; independently supplied and ID-checked |
| `automation_runtime` raw password | excluded; DB verifier reseeded and n8n Credential re-bound/rotated through owner ceremony if needed |
| `local_bridge_state` | `EXCLUDED_RECREATABLE`, restored empty |
| authorized payload | zero rows by default; only included under `MG-XD-DATA-BACKUP-*` from XD-11 |

The protected PostgreSQL verifier/ACK keyring is necessarily inside the encrypted full DB dump. Internal manifest lists only key IDs; raw key bytes never appear in catalog/evidence. Restore always starts disarmed, no provider route/token/source secret mount. Before later ACTIVE_ARM, bridge source keys must match restored key IDs or be rotated by owner-approved seed transaction; restored old keys never auto-arm.

Backup producer stops at `SEALED_PENDING_COLLECTOR`; V9 trusted collector validates and publishes `COMPLETE`. A different restore run yields `RESTORE_VERIFIED_PENDING_COLLECTOR`, then the collector emits final `RESTORE_VERIFIED`.

**Rejected:** VHDX/raw data directory backup; direct source write; broad volume/root bind; self-asserted COMPLETE; live secret-root dependency; in-place restore; silently backing up payload; generic symmetric backup key, passphrase or caller-controlled encryption parameters.

**Rationale:** resolves the missing V4 mount permission without weakening source isolation and makes all new key/payload decisions visible to recovery.

**AT/NC/EV:** `AT-XD-12` covers writer quiesce, exact backup graph, streaming encryption, payload-zero/default, key inventory and fresh cold restore. `NC-XD-12` adds one writer/network member/source-write/live secret mount/payload row/wrong key/keyring mismatch and requires no COMPLETE/target write. `EV-XD-12-BACKUP-BOUNDARY` stores graph/mount/session/generation/BOM/key-ID/collector refs only.

**Residual:** encrypted DB backup contains verifier-key bytes; compromise of both age identity and ciphertext exposes them. Restored environment therefore remains disarmed and key rotation is recommended before resumed real use.

## 15. `XD-13` — immutable candidate transfer и distinct gate processes

**Inputs/hashes:** V2 `c25e…540`, V4 `23a9…e032`, V5 `634a…4f70`, V9 `4c96…744a`; `XD-CONFLICT-10/12`.

**Affected:** `V4-C03/C06/C10/C11`, `V5-001`, `V9-C06..C11/C16/C17`; findings `R8-P1-002/003/004/005/008`, `R8-P2-011/012`, `R9-F05/09`.

**Canonical interface schema / decision:** candidate transfer is a deterministic POSIX pax stream produced only from `candidate_manifest/v2` with ordinal path order, normalized uid/gid/uname/gname/mtime/modes, no links/devices/xattrs/ADS and exact tool lock. The file-set aggregate is primary identity; archive SHA-256 is transport identity.

The V1-guarded wrapper creates an empty run-scoped candidate volume and starts nonroot `gate-loader` with `network_mode:none`. Archive bytes enter only through its bounded stdin. Loader validates path policy before extraction and then independently recomputes exact file-set aggregate. Generic `docker cp`, mutable host bind, repo/Vault bind and candidate rebuild inside Docker are forbidden.

Distinct sequential processes, each pinned and `network_mode:none`, are mandatory:

1. `gate-loader` — writes only candidate volume;
2. `gate-runner` — actual production runner bytes, candidate RO, raw-output volume RW;
3. `validator-a` and `validator-b` — independent implementations/BOMs, input RO, separate output volumes, no cross-read before close;
4. `evidence-collector` — separately pinned, reads closed allowlisted outputs RO and writes final evidence stage only.

Application volumes/secrets are absent. Each process is nonroot, nonprivileged, `CapDrop=ALL`, read-only rootfs except exact volumes/tmpfs, no Docker socket/devices/host namespace. A required O5 row needing broader capability gets scoped `OFFLINE_BLOCKED_CAPABILITY`; the topology is not relaxed.

**Rejected:** one `gate-runner` identity for all roles; validator self-sealing; mutable bind; `docker cp`; root/SYS_ADMIN retry; shared validator output/cache.

**Rationale:** byte identity and process separation satisfy both V4 containment and V9 independence.

**AT/NC/EV:** `AT-XD-13` round-trips archive/file-set identity and proves four distinct image/executable/process/output identities. `NC-XD-13` changes byte/mode/path, adds archive traversal/link, copies validator implementation/output or requests privilege; no false PASS. `EV-XD-13-GATE-TOPOLOGY` stores candidate/archive/tool/process/output/network/privilege hashes.

**Residual:** exact pax implementation and nonroot volume ownership require V2/V4 capability proof; failure blocks, not substitutes another transport.

## 16. `XD-14` — one evidence authority и dirty-worktree-safe Git disposition

**Inputs/hashes:** V8 `10c4…ca42`, V9 `4c96…744a`; `XD-CONFLICT-13/14`.

**Affected:** `V8-C08/C15`, `V9-C01..C18`; findings `R8-P1-003/010`, `R9-F01..F10`, `R10-F06/F10`.

**Canonical interface schema / decision:** V9 trusted collector owns the sole outer exact-set evidence envelope, final scoped state, RC, attempt ledger and anchor. Domain producers, including backup/restore and candidate runner, emit closed child records only; they cannot write final status. V8 semantic `COMPLETE/RESTORE_VERIFIED` becomes final only after collector validation as stated in XD-12.

Candidate/review/test/private commit/package all bind one `delivery_identity/v2`: source custody, candidate aggregate, runner, row manifests, validators, environment, evidence anchor, private commit tree and package projection. Package is generated from verified private commit tree, never mutable worktree.

For the known dirty source state, normal integration may only import the preverified object set and create a new dedicated candidate ref by compare-and-swap. It must not move checked-out branch/HEAD, alter index/worktree/21 dirty paths, invoke hooks/filters or rebase/merge. Promotion/reconciliation is a later owner decision with a fresh source guard; conflict is preserved, never overwritten.

**Rejected:** V8 self-sealed competing evidence; candidate stdout PASS; package from worktree; current-branch promotion as part of candidate integration; rollback over concurrent edits.

**Rationale:** one trust root prevents two incompatible truths and preserves user work while still allowing a verifiable deliverable.

**AT/NC/EV:** `AT-XD-14` verifies child→outer sealing, evidence tamper detection, candidate/tree/package equality and new-ref-only integration. `NC-XD-14` alters child RC/status, transfers a file from another run, changes source index/ref/path or invokes filter/hook. `EV-XD-14-CUSTODY` is the V9 outer envelope plus source/private-commit/package transition manifests.

**Residual:** a candidate ref is not branch integration; owner must later choose reconciliation. Hash identity proves bytes, not semantic correctness.

## 17. `XD-15` — canonical owner decisions, gate routing и emergency UX

**Inputs/hashes:** all domain drafts; especially V1 `32e7…e204`, V2 `c25e…540`, V3 `80c3…3cc2`, V6 `7b20…b803`, V7 `ef1a…a2b`, V8 `10c4…ca42`, V9 `4c96…744a`, V10 `6ed5…16db`; `XD-CONFLICT-19`.

**Affected:** all `MG-V*`; `V10-C01..C11`; findings `R10-F01..F11`, `R6-P2-011`, `R9-F06`.

**Canonical interface schema / decision:** V10 renders owner cards, but domain gates remain authorities. One `owner_decision_record/v2` may satisfy several listed domain gate IDs only when all refer to the same exact action, hashes, expiry and effect set. It never implies an omitted gate.

```yaml
schema: n8nagents.owner-decision-record/v2
decision_id: <uuid>
owner_ref: <keyed nonsecret>
integration_lock_sha256: <exact>
domain_gate_ids: [<exact nonempty set>]
action_id: <one exact action>
effect_classes: [READ_ONLY|HOST_WRITE|ELEVATED|REBOOT|PROVIDER_READ|PROVIDER_MUTATION|SECRET|COST|DESTRUCTIVE|REPO_INTEGRATION]
artifact_and_config_hashes: [<exact>]
limits: {ttl, bytes, messages, usd, retries}
excluded_effects: [<explicit>]
issued_at_utc: <utc>
expires_at_utc: <utc>
decision_mac: <host control MAC>
```

Canonical owner decision moments:

1. full frozen plan/integration lock — design/authorized implementation scope only;
2. metadata discovery origins/ceilings; then separate acquisition/runtime locks;
3. exact Docker/n8n/third-party licenses and eligibility;
4. exact Windows feature/UAC/install delta; each reboot and post-reboot resume separately;
5. roots, control principals, resource limits and any at-rest exception;
6. each secret class creation/transport; n8n key custody; owner/2FA and workflow reconciliation;
7. Telegram identity plus `PREARM`; then separate `ACTIVE_ARM`; webhook backlog drop separately irreversible; recipient/data class and payload-backup inclusion separately;
8. DeepSeek model/price/USD/request authorization separately;
9. backup root/key custody/RPO-retention and per-run owner key proof;
10. incident revoke/rotate/resume and support bundle before creation;
11. every material cleanup, backup/key retirement, failed-target deletion, VHDX/host-loss drill;
12. candidate start, optional new-ref integration, package publication; REMOTE/production always new scope.

Plan-wide approval can cover offline authoring/static/mock preparation only to the exact plan authority. It cannot supply secret values, accept changing license terms, perform UAC/reboot/provider identity/backlog drop, arm real traffic, spend money, delete data, promote dirty Git state or authorize remote work.

Every decision expires on plan/host/endpoint/boot/artifact/config/identity/tuple/cap/price/custody drift or stated TTL. Cancel/no answer is `G_READY_OWNER_GATE`/`G_BLOCKED_MANUAL`, zero mutation and no retry pressure.

Owner-operable real test sequence is: start MOCK and verify loopback n8n → manually complete n8n owner/2FA and inactive credential/workflow binding → create PREARM and inspect redacted result → create ACTIVE_ARM → start exact REAL_TG/optional separately armed REAL_TG_DEEPSEEK → perform bounded test → disarm/stop → backup only after XD-11 payload policy. The owner can execute the same versioned commands by hand from a new unelevated PowerShell session.

Emergency sequence remains host-first: publish disarm marker, revoke DB arm/lease if reachable, stop bridge then broker, prove no poll/send/socket/secret mount, preserve volumes/secrets, and report RC `53` if Engine/effect cannot be proved stopped. Provider revoke is an explicit owner incident action, never automated.

**Rejected:** one blanket approval for future unknown deltas; implicit gate inheritance; repeated prompts for identical exact action; auto-reboot/rearm; secret/cost/destructive decision hidden inside start; claiming emergency success from Docker CLI alone.

**Rationale:** owner sees materially different consequences once, while sensitive/destructive/external effects retain exact authority.

**AT/NC/EV:** `AT-XD-15` table-tests compatible batched gates, expiry and complete black-box owner flow. `NC-XD-15` attempts to reuse plan approval for UAC/secret/provider/cost/delete/REMOTE, reuse stale PREARM/ACTIVE_ARM after reboot, and claim emergency success with Engine unavailable. `EV-XD-15-OWNER-DECISIONS` stores gate/action/hash/effect/limit/result refs only.

**Residual:** some actions necessarily remain manual: licenses, UAC/reboot, secret/2FA entry, provider identity/webhook decisions, revoke, independent keys, destructive cleanup and dirty-branch reconciliation.

## 18. Resolution matrix

| Conflict | Canonical disposition | Design state |
|---|---|---|
| `DRIFT-V7-01`, `DRIFT-V10-05`, V8/V9 numbering | V1..V10 map in XD-02 | `RESOLVED_REWRITE_REQUIRED` |
| `DRIFT-V7-02`, `DRIFT-V10-01`, V5 direct bridge DB | no bridge DB path/role; n8n ingress → PG authority | `RESOLVED_REHASH_V4/V5/V6/V7/V8/V10` |
| `DRIFT-V7-03`, `DRIFT-V10-02`, V5 stale alias | only `egress-telegram` | `RESOLVED_REWRITE_REQUIRED` |
| `DRIFT-V7-04` | exact native-file canary or gated n8n-only entrypoint fallback | `RESOLVED_DESIGN_RUNTIME_UNKNOWN` |
| `DRIFT-V7-05` | authorized protected payload <=24 h; unauthorized never stored | `RESOLVED_REHASH_V3/V6/V7/V8` |
| `DRIFT-V7-06` | `automation_runtime` only as n8n encrypted Credential | `RESOLVED_OWNER_BINDING_PENDING` |
| `DRIFT-V10-03` | PREARM then ACTIVE_ARM | `RESOLVED_REHASH_V6/V10` |
| `DRIFT-V10-04`, V9 RC conflict | XD-04 global envelope and namespaced child RC | `RESOLVED_REWRITE_REQUIRED` |
| V9 canonicalizers | XD-03 registry | `RESOLVED_TOOL_PROOF_PENDING` |
| V9 candidate transfer | deterministic pax → `gate-loader` → exact volume | `RESOLVED_CAPABILITY_PROOF_PENDING` |
| V9 gate process identities | loader/runner/A/B/collector separate | `RESOLVED_CAPABILITY_PROOF_PENDING` |
| V9/V4 O5 privilege | scoped OFFLINE block, no relaxation | `RESOLVED_AS_SCOPED_BLOCK` |
| V8/V9 evidence authority | V9 outer collector is sole final authority | `RESOLVED_REHASH_V8/V9` |
| V9 dirty branch | new candidate ref only; promotion later | `RESOLVED_OWNER_GATE_PENDING` |
| V8 missing backup mount row | new exact V4 BACKUP row | `RESOLVED_REHASH_V4/V8` |
| V3 file-or-DB bridge authority | PostgreSQL only; file cache nonauthoritative | `RESOLVED_REHASH_V3/V5/V6/V8` |
| mode/service names | exact XD-06 sets | `RESOLVED_REWRITE_REQUIRED` |
| backup payload retention | default zero payload; separate inclusion gate | `RESOLVED_REHASH_V6/V7/V8` |
| V7/V8 backup-key interpretation | `V7-S11` is exact age X25519 private identity; capture gets public recipient only | `RESOLVED_REHASH_V7/V8` |
| overlapping/manual gate routing | XD-15 exact multi-gate decision record | `RESOLVED_REWRITE_REQUIRED` |

## 19. Acceptance of this integration record

This record is ready for a canonical-plan rewrite review only if all of the following hold:

- all 12 input hashes still equal §1 and aggregate recomputes exactly;
- `20/20` conflict rows map to at least one `XD-*` decision;
- decision IDs `XD-01..XD-15` are unique and each contains inputs, affected contracts/findings, rejected alternatives, rationale, canonical interface, AT/NC/EV and residual risk;
- bridge has no DB network/credential/role and no alternate path;
- sole Telegram egress key is `egress-telegram`;
- PREARM precedes ACTIVE_ARM and zero API exists without a current matching phase;
- unauthorized raw payload never persists; authorized protected payload TTL is <=24 h and backup is default-excluded;
- automation/bridge/n8n secret transports are mutually unambiguous;
- global numeric RC exists only at collector boundary; child RC is namespaced;
- LAB/LOCAL can remain useful while OFFLINE is honestly blocked;
- no runtime PASS, host observation, current provider fact, download, installation or execution is claimed.

## 20. Remaining unknowns and STOP conditions

`unresolved_design_conflicts = 0` for the 20 explicit conflicts above.

`runtime_unknowns = 6`:

1. exact n8n version can relay the internal envelope with zero raw execution/error/manual persistence;
2. exact n8n image supports native DB-password/instance-key file input, or the gated fallback is accepted;
3. exact PostgreSQL image/tool closure supplies reviewed HMAC/constant-time verifier behavior;
4. Docker Desktop exact fingerprint enforces network/mount/nonroot/loopback rows;
5. exact official provider origins, API schema, licenses, prices and supply artifacts remain to be acquired and locked;
6. deterministic pax/validator/collector tool closure and nonroot volume semantics remain to be qualified.

`scoped_blockers = 1`: A-only cannot satisfy O5 rows requiring forbidden privileged-equivalent capabilities; OFFLINE remains `OFFLINE_BLOCKED_CAPABILITY` until a new owner-reviewed path exists.

Any failed runtime unknown produces the corresponding `BLOCKED`, not a weaker fallback. Any canonical plan that omits or changes an XD decision without a new integration review is `INTEGRATION_BLOCKED / G_BLOCKED_CONTRACT_DRIFT`. This document itself provides no runtime proof.

## Связи

- [[00_FINDINGS_BASELINE]]
- [[01_BASELINE_AUDIT]]
- [[02_V1_WINDOWS_CONTROL_PLANE]]
- [[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]
- [[04_V3_RESOURCE_STORAGE_BOUNDARY]]
- [[05_V4_ISOLATION_NETWORK_EXPOSURE]]
- [[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]
- [[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]
- [[08_V7_SECRETS_PRIVACY_INCIDENT]]
- [[09_V8_BACKUP_COLD_RESTORE]]
- [[10_V9_CANDIDATE_EVIDENCE_GIT_CUSTODY]]
- [[11_V10_OWNER_OPERABILITY]]
