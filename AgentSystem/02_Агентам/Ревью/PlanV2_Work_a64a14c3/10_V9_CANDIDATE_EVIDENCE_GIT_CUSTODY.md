---
id: "n8nagents-plan-v2-v9-candidate-evidence-git-custody-20260827"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V9 Git/release/candidate/evidence custody architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
доказательства: []
теги: ["n8nagents", "plan-v2", "v9", "git", "candidate", "evidence", "custody", "design-only"]
---

# V9 — candidate, evidence, Git и release custody

## 0. Статус, область и запрет на исполнение

Это implementation-ready проект секции `V9` для будущего полного plan v2. Он является только design input для интеграции и независимого ревью. Он не разрешает изменение project repository, `.git`, Vault за пределами этого назначенного draft, Windows, Docker, WSL, VPS, provider UI, Telegram, DeepSeek, secrets, сеть, download, commit, ref update, package publication или удаление данных.

Секция относится только к плану A: Docker Desktop с его штатным WSL 2 backend. Отдельный пользовательский WSL-дистрибутив, VM, plan B и VPS не являются fallback. Если Docker Desktop или Windows не обеспечивают обязательную custody/capability, результатом является scoped `BLOCKED`, а не ослабление контракта.

V9 владеет:

- исходным custody snapshot пользовательского project worktree, index и `.git`;
- exact repo-write allowlist и защитой physical path identity;
- private authoring copy вне dirty worktree;
- immutable candidate, runner, row contracts, commit tree, package и delivery identity;
- двумя независимыми validators и deterministic clean-run protocol;
- fault-trigger receipts, positive controls и canaries против ложного `PASS`;
- scoped result/RC model `LAB | LOCAL | OFFLINE | REMOTE` и append-only attempt ledger;
- trusted evidence collector, manifest, anchor и chain of custody;
- isolated index/commit provenance, EOL/mode/attributes и package-from-commit-tree.

V9 не владеет Windows eligibility, Docker endpoint, artifact provenance, resource thresholds, network enforcement, Compose lifecycle, Telegram authorization, secrets, backup cryptography или production deployment. Эти области являются fail-closed dependencies V1–V8.

Ниже нет runtime claims. Значения `PASS`, `verified`, `immutable` и `complete` описывают будущие predicates и состояния, а не текущий факт.

## 1. Проверенные design inputs и baseline

| Вход | Identity/status | Использование |
|---|---|---|
| V0 findings baseline | `934c449aa75ad157b1702afefcbaac4eab80b750801f172226d065b5a528c4aa`, `114` findings | source finding identity |
| V0 audit | `PASS`, `114/114` | completeness of review import |
| Frozen plan v1 | `a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79`, `46234` bytes | rejected design baseline only |
| Quorum report | `08a59e4838d42102f94bb0bb826201d5edec704fcd90a6fe401f8e05f4eff5e7` | source dispositions |
| Project branch | `codex/n8nagents-foundation` | expected source identity; runtime revalidation required |
| Project HEAD | `11974a33fa78bb72598059671cef9465402ab091` | immutable expected base; runtime revalidation required |
| Dirty custody expectation | exactly `21` allowlisted draft paths: `12` tracked modifications and `9` untracked path roots; index changes `0`; outside allowlist `0` | mandatory precondition, not reconstructed from chat |
| Existing remote state | prior `REMOTE` K4 retry budget exhausted | imported only from authoritative attempt evidence; LOCAL/OFFLINE cannot change it |

The exact 21 path names and their bytes are deliberately not copied into this prose. They must come from a machine-generated `source_custody_manifest/v2`; count-only or chat-derived inventory is invalid.

## 2. Непереговорные инварианты

1. Source repository root, its 21 dirty paths, current `HEAD`, checked-out symbolic ref, user index bytes and existing `.git` state remain unchanged throughout discovery, authoring, candidate freeze, validators, B2r/O5 and package rehearsal.
2. `git stash`, `git reset`, `git clean`, `git checkout`, `git restore`, `git switch`, `git add`, `git commit` against the source repository, broad copy-back and worktree-wide formatters are prohibited before an explicit integration gate. There is no automatic exception.
3. `git worktree add` against the source repository is prohibited because it writes shared `.git` metadata. Authoring happens in a private, non-source copy with an independent object/index boundary.
4. Every source read uses a frozen custody snapshot. The candidate and tests never consume a mutable host bind of the source repository or Vault.
5. Every write has an exact manifest entry, a physical-root guard, a transactional journal entry and before/after evidence. Unknown, extra, ignored, ADS or metadata write is a containment failure.
6. Candidate, actual production runner, 66/34/8 contracts, commit tree, package projection and evidence are joined by one content-addressed delivery identity. A changed byte, type, mode, path spelling, EOL or attribute invalidates the chain.
7. Candidate stdout, runner stdout and validator stdout cannot seal evidence or choose final state. Only the trusted collector/reconciler can emit the final scope result and anchor.
8. A row count is never proof of row identity. Missing, extra, duplicate, renamed or hash-drifted row fails before aggregation.
9. Validators are independently implemented and independently execute against the same immutable inputs. They cannot consume each other's output.
10. Two clean, independently provisioned sequential runs are required for deterministic gates. Shared writable cache, prior output and mutable host source are forbidden.
11. `RC=0` is valid only for full `PASS` of the named exact scope. `LAB_READY` may coexist with `OFFLINE_BLOCKED_CAPABILITY`, but cannot become `OFFLINE_PASS`, `REMOTE_GO` or general `SUCCESS`.
12. `LAB`, `LOCAL`, `OFFLINE` and `REMOTE` have separate append-only attempt namespaces. No local artifact can increment, reset, satisfy or authorize REMOTE.
13. Evidence is source-allowlisted, secret-minimal and exact-set. Redaction cannot alter semantic status, RC, counts, hashes or row identity.
14. No old evidence is reusable after drift in plan, authority, source custody, candidate, runner, row manifest, validator, image, tool, environment, network or collector identity.
15. Physical containment is checked by handle/object identity, not string prefix. Reparse points, symlinks, junctions, hardlinks, case/Unicode aliases, ADS and TOCTOU fail closed.

## 3. Реестр контрактов V9

| Contract | Обязательство |
|---|---|
| `V9-C01-SOURCE-CUSTODY` | Full reproducible snapshot of repo root, worktree, 21 paths, index and `.git`; source stays unchanged. |
| `V9-C02-PRIVATE-AUTHORING` | Base tree + dirty overlay are materialized into a private non-source copy; all authoring occurs there. |
| `V9-C03-WRITE-SCOPES` | Repo, `.git`, Vault and lab roots have separate exact pre/post manifests and write authorities. |
| `V9-C04-PATH-SAFETY` | Windows path writes resist reparse/symlink/junction/hardlink/case/Unicode/ADS/TOCTOU substitution. |
| `V9-C05-WRITE-TRANSACTION` | Every approved write is journaled, atomic and conflict-safe; rollback is exact-target only. |
| `V9-C06-CANDIDATE-IDENTITY` | Immutable candidate archive/tree manifest binds base, dirty overlay and authorized authoring changes. |
| `V9-C07-ROW-CONTRACTS` | Sets 66/34/8 are immutable row-by-row manifests with stable IDs, fixture and expected-result hashes. |
| `V9-C08-INDEPENDENT-VALIDATORS` | Two independently pinned implementations produce independent row results; reconciler detects disagreement/copying. |
| `V9-C09-ACTUAL-RUNNER` | Tests execute exact bytes intended for production/package, not a surrogate harness. |
| `V9-C10-CLEAN-RUN-FINGERPRINT` | Two clean runs, deterministic inputs and an exact environment/tool/image/kernel fingerprint are mandatory. |
| `V9-C11-FAULT-AND-CANARIES` | Faults have collector-observed trigger receipts, paired controls and fake-PASS/network/cleanup canaries. |
| `V9-C12-SCOPED-RESULTS` | Versioned row/gate/run/project state machine and stable RC namespaces fail closed. |
| `V9-C13-ATTEMPT-LEDGER` | Append-only LAB/LOCAL/OFFLINE/REMOTE attempt ledger preserves budgets and history. |
| `V9-C14-EVIDENCE-ENVELOPE` | Trusted collector creates exact-set manifest, aggregate anchor and redaction audit. |
| `V9-C15-GIT-INTEGRATION` | Private object DB/index creates an exact commit; source integration is explicit CAS and preserves user index/worktree. |
| `V9-C16-PACKAGE-DELIVERY` | Package is generated only from verified commit tree and is projection-equal to candidate. |
| `V9-C17-EOL-MODE-ATTRIBUTES` | Raw bytes, Git modes, EOL, encoding and attributes are frozen and checked across candidate/index/tree/package. |
| `V9-C18-TEMP-SECRET-GUARD` | Temp roots precede generators; ignored/ADS/archive secret canaries block staging/package. |

## 4. `V9-C01-SOURCE-CUSTODY` — исходный worktree, index, Git и physical roots

### 4.1. Read-only guard

Before snapshot, trusted wrapper opens source repo root, worktree root, `.git` indirection if any, gitdir, common-dir and index path without following reparse points. It records exact local protected identities and emits only run-scoped keyed fingerprints to evidence.

All Git discovery commands use an explicit absolute executable and repository path with:

```text
GIT_OPTIONAL_LOCKS=0
maintenance.auto=false
gc.auto=0
credential.helper disabled for this invocation
pager disabled
hooks never invoked
network protocols denied by operation policy
```

If a required read would write an index refresh, lock, maintenance state or object, snapshot returns `V9_BLOCKED_GIT_READ_SAFETY`. A preliminary before/after `.git` inventory proves no discovery write.

### 4.2. `source_custody_manifest/v2`

Canonical payload is RFC 8785/JCS UTF-8 without BOM; envelope hash is outside the payload.

```yaml
schema: n8nagents.source-custody-manifest/v2
plan_sha256: <full-plan-v2>
authority_id: <opaque>
snapshot_id: <uuid>
created_utc: <RFC3339 UTC>
repo:
  root_logical_id: PROJECT_SOURCE
  physical_root_fingerprint: <keyed>
  volume_fingerprint: <keyed>
  filesystem_type: <observed>
  root_reparse_state: NONE
  git_worktree_layout: NORMAL | LINKED
git:
  gitdir_fingerprint: <keyed>
  common_dir_fingerprint: <keyed>
  head_file_sha256: <hash>
  head_kind: SYMBOLIC | DETACHED
  symbolic_ref: <expected exact>
  head_oid: 11974a33fa78bb72598059671cef9465402ab091
  ref_file_or_packed_identity: <hash>
  index_file_bytes: <integer>
  index_file_sha256: <hash>
  index_stage_entries: []
  index_extension_inventory_sha256: <hash>
  config_scope_hashes: {system, global, local, worktree}
  effective_attributes_inventory_sha256: <hash>
  hooks_inventory_sha256: <hash>
  object_database_manifest_sha256: <hash>
  refs_reflogs_manifest_sha256: <hash>
worktree:
  full_no_ignore_manifest_sha256: <hash>
  tracked_modified_count: 12
  untracked_path_root_count: 9
  custody_path_count: 21
  outside_allowlist_count: 0
  custody_entries: [<entry>]
aggregate_sha256: <computed outside payload>
```

Each `custody_entry` includes:

- exact relative path encoded as length-prefixed UTF-8 bytes without normalization;
- ordinal case and NFC assertion; non-NFC names are rejected rather than silently normalized;
- SHA-256 of the original Windows UTF-16LE path code units to detect spelling aliases;
- path type `regular | directory-root | symlink | other`; only allowed types proceed;
- tracked state and porcelain-v2 status;
- base blob OID/mode from exact HEAD or `null` for untracked;
- working file bytes, SHA-256, Git blob OID and intended Git mode;
- file/volume identity fingerprints, link count, reparse/ADS result;
- for an untracked directory root, a completely expanded, sorted recursive file set. Directory count alone is invalid.

The full worktree inventory includes tracked, untracked and ignored entries, but excludes the separately inventoried gitdir only by exact physical identity. `.gitignore` does not hide evidence. Empty directories are recorded explicitly for custody even though Git does not version them.

The `.git` manifest separately enumerates index, HEAD, refs, packed-refs, logs, config, worktrees, hooks, info/attributes/exclude, shallow state, alternates and every object-store file/pack by path/type/bytes/SHA-256. Before/after equality is exact except in `V9-C15` integration, where allowed Git transitions are separately enumerated.

### 4.3. Independent reproducibility

Two independent manifest builders with distinct implementation identities read the same handles/snapshot and must emit byte-identical canonical payload and aggregate. Difference is `V9_STOP_CUSTODY_DISAGREEMENT`; no authoring copy is created.

Guard tuple:

```text
SOURCE_GUARD = SHA256(
  plan + authority + physical repo/git/index identities +
  symbolic ref + HEAD + index bytes + full worktree aggregate +
  .git manifest + Vault pre-manifest + lab-root identity
)
```

The tuple is rechecked before and after every phase, not just before commit.

## 5. `V9-C02/C03` — private authoring и разделение write scopes

### 5.1. Four physical scopes

| Scope | Normal phase authority | Required evidence |
|---|---|---|
| `PROJECT_SOURCE_WORKTREE` | read-only for all V9 phases | full no-ignore before/after equality and 21-path custody equality |
| `PROJECT_SOURCE_GIT` | read-only until explicit `INTEGRATE_REF` gate | full `.git` before/after; later exact object/ref/reflog transition only |
| `OBSIDIAN_VAULT` | immutable during runtime/candidate/evidence runs; documentation is a separate operation | full Vault before/after and exact documentation write allowlist |
| `LAB_PRIVATE_ROOT` / Docker candidate volumes | exact run-scoped allowlist | root physical identity, journal and full before/after manifest |

One phase cannot silently borrow another scope's authority. Writing a Vault report after a run requires a new documentation transaction and may only copy source-allowlisted, redacted evidence. Runtime evidence does not write directly to Vault.

### 5.2. Private copy construction

1. Create an unpredictable approved private lab root or fresh labelled Docker volume using V3/V4 custody.
2. Materialize exact base tree `11974...` into that private root through a read-only Git object stream. Do not create a linked worktree and do not reuse source index.
3. Overlay exact bytes/types/modes of the frozen 21-path custody snapshot. No later read from the mutable source worktree is allowed.
4. Verify the materialized baseline independently against `source_custody_manifest/v2`.
5. Apply authoring changes only inside this private copy, using frozen `authoring_write_manifest/v2` and `V9-C05` journal.
6. Candidate/test containers receive only a read-only candidate volume/archive and a fresh output volume. Source repo and Vault are never bind-mounted.

The private authoring environment may have its own independent Git object database for provenance, but no alternates path that allows writes into source `.git`. If read-only alternates are used for object lookup, OS and wrapper policy must prove writes target only the private object directory; inability to prove this blocks.

### 5.3. Exact write manifest

Every phase has an immutable `write_manifest/v2`:

```yaml
schema: n8nagents.write-manifest/v2
phase: DOC_DRAFT | PRIVATE_AUTHOR | FREEZE | RUN | COLLECT | PRIVATE_COMMIT | INTEGRATE_REF | PUBLISH_PACKAGE
plan_sha256: <exact>
authority_id: <exact>
run_id: <exact>
root_identities: [{logical_id, physical_fingerprint, allowed_access}]
operations:
  - operation_id: <stable>
    root_logical_id: <exact>
    relative_path_bytes_sha256: <hash>
    action: CREATE_NEW | REPLACE_EXACT | APPEND_NEW_RECORD | CREATE_GIT_OBJECT | CAS_CREATE_REF
    expected_pre: {absent | type, file_id, bytes, sha256, mode}
    expected_post: {type, bytes, sha256, mode}
    parent_identity_sha256: <hash>
    rollback_policy: <stable-id>
```

No wildcard, glob, recursive implicit target, environment-derived root, `*`, `..`, default current directory or guessed path is valid. Each ancestor and leaf is checked immediately before open. Extra write or missing expected write is `V9_FAIL_OUTSIDE_WRITESET`.

## 6. `V9-C04` — Windows-safe path, alias и TOCTOU contract

The trusted host writer follows one algorithm for source manifests, lab files, evidence export, package and future Git integration:

1. Accept only absolute local NTFS paths under an approved root; reject UNC, mapped/SUBST/removable/network/device namespaces, wildcards, relative paths and environment expansion after manifest freeze.
2. Open root and each ancestor by handle without following reparse points. Capture volume identity, file ID, type, DACL hash and exact name returned by the filesystem.
3. Reject every reparse tag, symlink, junction, mount point, Cloud Files placeholder/recall flag and unknown filesystem feature.
4. Require ordinal-exact case and exact Unicode code-unit sequence; require NFC for new names; reject NFC/NFD and case-fold collisions, alternate 8.3 alias and trailing dot/space ambiguity.
5. Allow colon only in drive designator. Enumerate alternate data streams; any ADS other than the unnamed data stream is rejected.
6. For an existing regular-file target require expected file ID and link count `1`. Hardlink count greater than one is a containment failure.
7. Create new `.partial` with create-new/no-overwrite, restricted sharing and exact DACL; write, flush, close, re-open, hash and only then same-volume atomic rename/replace according to manifest.
8. Hold parent/leaf handles across security-sensitive open/replace where Windows permits. Revalidate parent, target, volume, reparse, DACL, link count and hash after open and after replace.
9. A directory/file swap, ancestor replacement, link creation, rename race or concurrent editor drift causes `V9_STOP_TOCTOU`; no retry against a new identity under the same authority.
10. Evidence exposes only logical IDs and keyed fingerprints; exact paths and raw file IDs stay in protected local control records.

The source worktree is never a write target, so any source identity drift blocks rather than invokes rollback.

## 7. `V9-C05` — transactional write journal и rollback

The journal is append-only, create-new and stored in an approved protected journal root outside source repo/Vault and outside the target directory. Each record is length-delimited canonical JSON with previous-record hash.

State machine per operation:

```text
DECLARED -> PRECONDITION_VERIFIED -> PREIMAGE_SEALED -> WRITE_STARTED
         -> POSTIMAGE_VERIFIED -> COMMITTED
         -> ROLLBACK_PRECHECK -> ROLLED_BACK
         -> CONFLICT_PRESERVED | FAILED_PRESERVED
```

Requirements:

- `CREATE_NEW` records expected absence and every newly created parent;
- `REPLACE_EXACT` stores preimage bytes/metadata in a content-addressed recovery object before write;
- every state has UTC, operation/write-manifest hash, target identity, expected/observed hash and collector identity;
- crash recovery resumes only from the last valid hash-linked record and rechecks target identity;
- rollback removes only an exact current-run created object or restores one exact preimage after postimage identity/hash still matches;
- concurrent edits, unexpected link count, changed DACL or different bytes yield `CONFLICT_PRESERVED`; rollback does not overwrite them;
- rollback never uses reset/checkout/clean/stash, recursive deletion, directory replacement or broad restore;
- success requires final full-scope manifest equality and zero orphan `.partial`, lock, temp or recovery target outside the journal's exact set.

## 8. `V9-C06` — immutable candidate and delivery identity

### 8.1. Candidate construction

Candidate is a content object, not a mutable directory. It is frozen from the private authoring root after static policy checks:

```yaml
schema: n8nagents.candidate-manifest/v2
candidate_id: <uuid>
plan_sha256: <exact>
authority_id: <exact>
source_custody_sha256: <exact>
base_head_oid: 11974a33fa78bb72598059671cef9465402ab091
base_tree_oid: <exact>
authoring_write_manifest_sha256: <exact>
full_tree_entries: [
  {path_bytes, type, bytes, sha256, git_blob_oid, git_mode, eol_class, attributes_sha256}
]
base_to_candidate_delta: [<exact path/action/pre/post>]
dirty_snapshot_to_candidate_delta: [<exact path/action/pre/post>]
runner_manifest_sha256: <exact>
row_contract_family_sha256: <exact>
candidate_tree_oid: <computed>
candidate_aggregate_sha256: <computed outside payload>
```

The full tree set, not only changed files, is included. Paths are sorted by unsigned ordinal UTF-8 bytes. Entries with path collision, unsupported type, secret marker, ignored surprise or unknown attribute block freeze.

An archive is emitted deterministically from this manifest: fixed path order, fixed owner/group numeric values, fixed modes, fixed UTC epoch from lock, no absolute path, no device/FIFO/socket, no PAX nondeterministic fields and no duplicate member. Archive hash is additional custody; extracted full-tree manifest must reproduce the candidate aggregate.

After freeze, authoring copy is not a valid test input. Every consumer verifies candidate archive and manifest into a fresh read-only volume. Any mutation creates a new candidate ID/hash and invalidates prior reviews/runs.

### 8.2. Single delivery identity

```yaml
schema: n8nagents.delivery-identity/v2
plan_sha256: <exact>
authority_id: <exact>
source_custody_sha256: <exact>
candidate_manifest_sha256: <exact>
candidate_aggregate_sha256: <exact>
candidate_tree_oid: <exact>
runner_manifest_sha256: <exact>
row_contract_family_sha256: <exact>
validator_family_sha256: <exact>
private_commit_oid: <exact-after-creation>
private_commit_tree_oid: <must equal candidate_tree_oid>
package_projection_manifest_sha256: <exact>
package_archive_sha256: <exact>
evidence_anchor_sha256: <exact-after-runs>
delivery_anchor_sha256: <computed outside payload>
```

Fields that do not yet exist are not filled with placeholders in an approved object; immutable successor identities are created in phase order. Earlier records remain append-only. There is no circular hash: run evidence first binds pre-commit candidate identity; a successor release identity binds commit/package and the already sealed run anchor.

## 9. `V9-C07` — immutable 66/34/8 row manifests

Three independent manifests are mandatory. Canonical integrated plan assigns their final semantic names; until then they are `SET66`, `SET34` and `SET8` and remain distinct.

```yaml
schema: n8nagents.row-contract-set/v2
set_id: SET66 | SET34 | SET8
expected_cardinality: 66 | 34 | 8
plan_sha256: <exact>
candidate_aggregate_sha256: <exact>
runner_manifest_sha256: <exact-if-applicable>
validator_policy_sha256: <exact>
rows:
  - row_id: <stable ASCII unique ID>
    purpose: <closed enum/text hash>
    input_manifest: [{logical_id, path/member identity, bytes, sha256}]
    fixture_setup_sha256: <exact>
    operation_manifest_sha256: <exact>
    applicable_validators: [A, B] | [RUNNER, COLLECTOR]
    expected_terminal_status: PASS | EXPECTED_REJECT | EXPECTED_BLOCK
    expected_rc: <exact>
    assertions: [{assertion_id, predicate_schema_sha256, expected}]
    fault_contract_sha256: <hash|null>
    cleanup_contract_sha256: <hash>
    evidence_required: [<stable EV IDs>]
set_aggregate_sha256: <computed outside payload>
```

Rules:

- row IDs are exact-set, unique across their set and stable across runs;
- fixture bytes, runner inputs, expected statuses/RC and assertions are hash-bound;
- expected/observed set equality is proven before any gate aggregation;
- deletion, duplicate, extra row, rename, reordered semantic list, changed fixture or changed expected status causes failure;
- `skipped`, `not applicable` and missing result are never `PASS`; applicability itself is frozen per row;
- counts `66/34/8` are secondary assertions only.

## 10. `V9-C08/C09` — independent validators и actual production runner

### 10.1. Validator independence

Validator family contains exact source, dependency, build, image and command identities for `A` and `B`:

- different implementation/source identities and independently reviewed dependency roots;
- no shared custom parser, canonicalizer, schema traversal, assertion engine or result aggregator;
- separate read-only candidate/contract inputs and separate fresh output volumes;
- no network, no secret, no Docker socket, no source/Vault bind and no read access to the other validator output;
- each recomputes candidate, runner, row-set and environment bindings independently;
- each emits every row result under its own schema and implementation hash;
- the third trusted reconciler reads both only after they close, verifies exact-set equality and compares semantic outcomes.

Same prohibited implementation hash, copied output bytes, impossible timestamp/process lineage, shared writable output or missing implementation BOM gives `V9_BLOCKED_VALIDATOR_INDEPENDENCE`. A/B disagreement is terminal `V9_FAIL_VALIDATOR_DISAGREEMENT`; no majority or preferred validator hides it.

Concrete validator tools are not chosen by V9 prose. V2 runtime lock must supply two qualifying implementations and V9 must prove independence before first row. Absence gives zero validator starts.

### 10.2. Actual production runner

`runner_manifest/v2` lists exact entrypoint paths, raw bytes/SHA-256/Git blob IDs/modes, invoked interpreter/binary, dependency/config files and canonical argv/environment. The runner is extracted from the immutable candidate/commit projection and is the same byte sequence intended for release/package.

Forbidden:

- a test-only copy or regenerated runner;
- wrapper logic that reimplements product behavior and is then tested instead;
- modification/monkey-patch of runner bytes for fault injection;
- PATH, current-directory or shell lookup of a different executable;
- package runner whose bytes differ from executed candidate runner.

Trusted launcher may set the frozen environment and attach external fault shims, but launcher/shim bytes are separately locked. Pre-exec and post-exec identity checks prove the actual process image/script chain. Package gate extracts runner bytes from commit-tree package and compares them to the executed runner manifest.

## 11. `V9-C10` — two clean runs and exact execution fingerprint

Each accepted gate executes two sequential runs, `RUN-A` and `RUN-B`, with new unpredictable IDs and independently provisioned resources:

- new empty candidate verification volume;
- new empty output/evidence work volume;
- no reused container, writable layer, tmpfs, process, IPC state or previous result;
- cache disabled, or read-only cache content fully content-addressed and explicitly allowed by row contract;
- fail before validator start if any expected-empty root contains an entry;
- same immutable candidate, row contracts, runner, validator family and environment lock;
- fixed locale, timezone, umask, UID/GID, workdir, random seeds and normalization policy;
- bounded wall/CPU/memory/output/time limits from V3;
- V4 network mode and positive-control evidence;
- cleanup after seal, never before evidence export.

Normalized semantic output excludes only explicitly enumerated nondeterministic fields such as run ID and timestamps. Raw outputs remain hashed. Both runs must have exact row-set/status/RC/assertion equality and equal normalized semantic hash. Difference is `V9_FAIL_NONDETERMINISTIC`.

`execution_fingerprint/v2` includes:

- Windows build class and host boot/session pseudonyms;
- CPU architecture and Docker platform `linux/amd64`;
- Docker Desktop, Engine, API and Compose exact builds;
- WSL kernel `uname`, build/config feature probes;
- OCI index/child/config/layer digests for every image;
- container image/rootfs identity and storage driver/backing filesystem;
- cgroup/security mode, seccomp/AppArmor state, capabilities, UID/GID;
- filesystem types/options, mount IDs/options/propagation and candidate volume identity;
- network mode, namespace, interfaces, routes, resolver and V4 policy hash;
- tool executable path, bytes/hash, implementation/version and feature probes;
- environment-variable name allowlist with value classes/hashes, locale/TZ/umask/workdir/seeds;
- resource limits and collector clock policy.

Missing field or drift invalidates old evidence. LOCAL/OFFLINE fingerprint cannot be relabelled REMOTE. Remote promotion always requires a new exact-candidate remote run under a separately authorized remote fingerprint.

## 12. `V9-C11` — fault receipts, controls and anti-false-PASS canaries

### 12.1. Fault contract

Every injected fault row has:

```yaml
fault_id: <stable>
target_phase_and_operation: <exact>
shim_or_adapter_sha256: <exact>
trigger_predicate: <machine-readable>
collector_observation: <independent source>
expected_intermediate_failure: {status, rc, invariant}
required_recovery_invariants: [<exact assertions>]
paired_control_row_id: <non-injected row>
cleanup_assertions: [<exact object/path/process checks>]
```

Candidate and runner cannot write the final trigger receipt. Trusted collector observes a causally unique event outside candidate output, writes a hash-bound receipt and correlates it with process/container/object identity. No-op, disabled, mistimed or wrong-target shim yields `TRIGGER_NOT_PROVEN` even if recovery output says `PASS`.

`PASS` for a fault row requires: positive trigger receipt, expected intermediate failure, all recovery invariants, paired non-injected control and cleanup. A real trigger plus broken rollback is `FAIL`, not `BLOCKED`.

### 12.2. Required canary classes

- **Fake PASS:** stdout/stderr contains `PASS` with nonzero RC; RC 0 with missing row; schema-invalid result; stale result; changed status with same transcript; copied validator output.
- **Candidate/runner TOCTOU:** one byte/mode/path/EOL changes after freeze, during run and before package.
- **Rows:** missing/extra/duplicate/renamed row and fixture substitution in each 66/34/8 set.
- **Network:** V4 positive-control reaches controlled sentinel; isolated target has no non-loopback interface/default route and denies direct IPv4/IPv6 TCP/UDP, gateway, host, metadata/link-local and DNS classes. Positive-control failure blocks target conclusion.
- **Filesystem/path:** junction parent, symlink leaf, external hardlink, case-only/NFC-NFD/8.3 alias, ADS and ancestor/leaf swap; outside sentinel unchanged.
- **Writes:** ignored repo file, `.git`, Vault, external junction target and unmanifested lab path are detected.
- **Cleanup:** same run label with wrong authority/candidate/class, missing label, changed object ID and persistent-volume lookalike delete zero objects.
- **Signals/faults:** interrupt at every transactional boundary; stale locks/results never produce PASS; collector death cannot be reported by child as success.

## 13. `V9-C12/C13` — scoped states, RC and append-only attempts

### 13.1. Result hierarchy

Each level has an exact schema: `ROW_RESULT`, `GATE_RESULT`, `RUN_RESULT`, `SCOPE_RESULT`, `PROJECT_SUMMARY`. Aggregation is deterministic bottom-up; parent cannot override a child with a more favorable state.

Allowed terminal states:

| State | Meaning |
|---|---|
| `PASS` | Every required exact row/assertion/control/evidence item passed for this scope and RC is `0`. |
| `FAIL` | Test executed and product/contract invariant failed. |
| `BLOCKED` | Required authority/tool/capability/identity/prerequisite unavailable; not a PASS. |
| `MANUAL_PASS` | Only an explicitly manual row with owner attestation schema; never substitutes autonomous B2r/O5 rows. |
| `NOT_RUN` | Execution never started; cannot aggregate to PASS. |
| `STOP` | Integrity, containment, scope, evidence or state-machine contradiction; no automatic continuation. |

Scope meanings:

- `LAB`: local application/mock/real-dev laboratory readiness only;
- `LOCAL`: exact Docker Desktop local execution result;
- `OFFLINE`: K4R/B2r/O5 offline gate result with no external traffic;
- `REMOTE`: separately authorized VPS/production-like execution only.

Examples of valid coexistence:

```text
LAB=PASS, LOCAL=PASS, OFFLINE=BLOCKED_CAPABILITY, REMOTE=EXHAUSTED
```

This may be summarized as `LAB_READY_WITH_OFFLINE_BLOCK`, never `SUCCESS`, `OFFLINE_READY`, `REMOTE_GO` or production readiness.

### 13.2. V9 RC namespace

| RC | Stable status |
|---:|---|
| `0` | `V9_SCOPE_PASS` — exact named scope only |
| `160` | `V9_BLOCKED_AUTHORITY` |
| `161` | `V9_BLOCKED_SOURCE_DRIFT` |
| `162` | `V9_BLOCKED_GIT_READ_SAFETY` |
| `163` | `V9_BLOCKED_PATH` |
| `164` | `V9_BLOCKED_TOOL` |
| `165` | `V9_BLOCKED_VALIDATOR_INDEPENDENCE` |
| `166` | `V9_BLOCKED_CAPABILITY` |
| `167` | `V9_BLOCKED_ENVIRONMENT_DRIFT` |
| `168` | `V9_BLOCKED_ATTEMPT_BUDGET` |
| `169` | `V9_BLOCKED_CONTRACT_DRIFT` |
| `170` | `V9_FAIL_ROW_SET` |
| `171` | `V9_FAIL_VALIDATOR_DISAGREEMENT` |
| `172` | `V9_FAIL_RUNNER_IDENTITY` |
| `173` | `V9_FAIL_FAULT_TRIGGER` |
| `174` | `V9_FAIL_ASSERTION` |
| `175` | `V9_FAIL_NONDETERMINISTIC` |
| `176` | `V9_FAIL_CLEANUP` |
| `177` | `V9_FAIL_OUTSIDE_WRITESET` |
| `178` | `V9_FAIL_SECRET_OR_PII` |
| `179` | `V9_STOP_TOCTOU` |
| `180` | `V9_STOP_CUSTODY_DISAGREEMENT` |
| `181` | `V9_STOP_CANDIDATE_DRIFT` |
| `182` | `V9_STOP_EVIDENCE_INVALID` |
| `183` | `V9_STOP_RESULT_INVALID` |
| `184` | `V9_STOP_SCOPE_EXPANSION` |
| `185` | `V9_STOP_INTEGRATION_CONFLICT` |
| `186` | `V9_STOP_ROLLBACK_CONFLICT` |

Unknown/missing status, duplicate field, invalid RC/state pair, child `PASS` text, zero RC with missing evidence or `MANUAL_PASS` without exact owner attestation becomes `V9_STOP_RESULT_INVALID`.

### 13.3. Append-only attempt ledger

```yaml
schema: n8nagents.attempt-ledger-record/v2
record_id: <uuid>
previous_record_sha256: <hash|null>
scope: LAB | LOCAL | OFFLINE | REMOTE
gate_id: <exact>
authority_id: <exact>
candidate_aggregate_sha256: <exact>
attempt_id: <uuid>
event: RESERVED | RUN_STARTED | TERMINAL | SUPERSEDED | BUDGET_EXHAUSTED
terminal_state: <state|null>
terminal_rc: <integer|null>
run_evidence_anchor_sha256: <hash|null>
created_utc: <RFC3339 UTC>
record_sha256: <computed outside payload>
```

An attempt consumes budget only at `RUN_STARTED`, after all preflight/authority/candidate/tool/environment checks pass and immediately before first test action. `BLOCKED` before this marker is recorded but does not consume a corrective attempt unless the governing authority explicitly says otherwise. A terminal attempt is never edited or deleted.

The ledger imports prior REMOTE exhaustion only from verified historical evidence. It then fixes `REMOTE=BUDGET_EXHAUSTED`; LOCAL/OFFLINE records use different keys and cannot change it. A new remote attempt requires a new named remote authority and explicit budget; V9 cannot synthesize it from plan approval.

## 14. `V9-C14` — trusted evidence envelope, manifest and anchor

### 14.1. Trust separation

Trusted collector/reconciler is separately pinned from candidate, runner and validators. Candidate processes have write access only to their raw invocation output volume. They cannot write final manifest, final state, RC mapping, attempt ledger, anchor or published evidence.

Collector reads only source-allowlisted artifacts after producer close/exit, independently captures process/container RC and hashes, validates schema and writes to a new empty evidence stage. Unknown producer, extra file, archive, symlink, ADS or output path blocks sealing.

### 14.2. Envelope

```yaml
schema: n8nagents.evidence-envelope/v2
scope: LAB | LOCAL | OFFLINE | REMOTE
gate_id: <exact>
run_id: <exact>
attempt_record_sha256: <exact>
plan_sha256: <exact>
authority_id: <exact>
source_custody_sha256: <exact>
candidate_manifest_sha256: <exact>
candidate_aggregate_sha256: <exact>
runner_manifest_sha256: <exact>
row_contract_family_sha256: <exact>
validator_family_sha256: <exact>
tool_bom_sha256: <exact>
execution_fingerprint_sha256: <exact>
network_evidence_sha256: <exact>
collector_manifest_sha256: <exact>
result_schema_sha256: <exact>
canonical_command_records: [{argv_sha256, cwd_logical_id, env_name_set_sha256}]
process_results: [{process_id, start_utc, end_utc, rc, stdout_sha256, stderr_sha256}]
row_results: [{set_id, row_id, validator_id, status, rc, assertions_sha256}]
fault_receipts: [{fault_id, receipt_sha256, control_row_id}]
cleanup_result_sha256: <exact>
write_scope_before_after_sha256: <exact>
redaction_audit_sha256: <exact>
scope_result: {state, rc, failed_predicates}
```

### 14.3. Exact-set manifest and aggregate

Published evidence root contains only files enumerated by `evidence_manifest/v2`. Each entry has length-prefixed canonical relative path bytes, type, bytes and SHA-256. Paths are NFC, ordinal case-unique and free of absolute/device/traversal/reserved/ADS forms. Directories, symlinks, hardlinks, devices and alternate streams are forbidden in published evidence.

Aggregate:

```text
entry_digest = SHA256(
  uint64_be(path_byte_length) || path_utf8_bytes ||
  uint64_be(file_length) || file_sha256_bytes
)
evidence_anchor = SHA256(
  "N8NAGENTS-EVIDENCE-V2\0" ||
  ordered_concat(entry_digest) ||
  envelope_payload_sha256
)
```

Manifest excludes itself and anchor from entry recursion; outer seal records their hashes and previous seal for append-only publication. Moving a file from another run, replacing, removing, adding, duplicating or renaming an entry changes verification. Evidence is published create-new; an existing target run ID is never overwritten.

### 14.4. Redaction audit

Evidence uses source allowlists and structured extraction, not unrestricted log capture followed by regex-only redaction. Raw environment, headers, message bodies, IDs, tokens, secrets, paths, SIDs, support bundles and dumps are never eligible sources.

For an allowed field requiring pseudonymization, collector emits purpose-separated keyed pseudonym and a field-level action record containing schema path, source class, transform policy ID and before/after length class, never the raw value. Re-running redaction on the same allowed structured input must produce the same semantic fields and audit hash. Any scanner error, unsupported schema or marker hit blocks the entire evidence envelope.

## 15. `V9-C15` — private commit, isolated index and source integration

### 15.1. Private commit creation

Commit preparation happens in a private object database, not in source `.git` and not from mutable worktree:

1. Import/read exact base commit/tree into a private independent Git object database.
2. Create a private temporary index from exact expected parent tree.
3. Hash candidate raw bytes directly into private objects; do not run checkout clean/smudge filters or `git add` against source.
4. Apply exact path/mode/blob entries from `candidate_manifest/v2` to the private index.
5. `write-tree`; require generated tree OID equals `candidate_tree_oid` independently derived from candidate manifest.
6. Create commit with expected single parent `11974...`, frozen author/committer policy, deterministic message/trailers and no hooks.
7. Commit trailers bind plan, authority, source custody, candidate, runner, row contracts, two-run evidence anchor and review disposition hashes.
8. Verify commit parent/tree/message/changed-path set and full tree against candidate with two independent verifiers.

Low-level plumbing is used so hooks and filters cannot silently change content. Effective system/global/local Git configs, attributes and hooks are still inventoried; an active required filter on a candidate path causes `BLOCKED_CONTRACT_DRIFT` unless a reviewed exact byte policy explicitly resolves it.

### 15.2. Optional source-repository integration gate

Integration is not implied by candidate PASS. It requires a new exact authority containing private commit OID, expected source guard, target ref and exact `.git` write manifest.

To preserve the user's dirty worktree and current `HEAD`, normal V9 integration may only:

- import an exact precomputed object set/pack into source object database;
- create a new dedicated candidate ref with compare-and-swap from expected absence;
- append its exact reflog record if repository policy requires it.

It must not move the checked-out branch, change the `HEAD` file, update the source index, checkout files or alter the 21 dirty paths. Promotion of the checked-out branch is a separate owner/integration decision after safe reconciliation and is outside this contract.

Before integration: recheck source guard, source index byte hash, full worktree/.git manifests, target ref absence and object collision safety. After integration: verify only the enumerated object files/pack-index, candidate ref and its reflog changed; `HEAD`, index and source worktree remain byte-identical. Any concurrent edit/ref move/object maintenance gives `V9_STOP_INTEGRATION_CONFLICT`; no auto-merge/rebase/retry.

## 16. `V9-C16/C17/C18` — package, byte policy and temp safety

### 16.1. Package from commit tree

Release package is generated only from the verified private commit tree, never from source/private worktree. A frozen `package_projection_manifest/v2` lists exact included paths and modes. Export is deterministic and then re-extracted into a new empty root.

Pass conditions:

- commit tree equals candidate tree;
- every package entry equals its candidate projection by path bytes, type, bytes/SHA-256 and mode;
- actual production runner bytes equal executed runner manifest;
- no extra/ignored/temp/evidence/secret path enters package;
- package archive path order, metadata epoch, uid/gid/mode and format follow frozen rules;
- package manifest/archive hashes enter successor delivery identity;
- package publication target is create-new and separately authorized.

### 16.2. EOL, encoding, mode and attributes

Default candidate policy:

| Class | Bytes policy | Git mode |
|---|---|---|
| Linux shell/executable entrypoint | UTF-8 no BOM, LF, exactly one final LF, no CR | `100755` when actually invoked directly; otherwise reviewed `100644` |
| PowerShell/JSON/YAML/Markdown/text config | UTF-8 no BOM, LF, exactly one final LF unless format forbids | `100644` |
| Binary/archive/fixture | exact opaque bytes, no normalization | `100644` unless reviewed otherwise |
| Symlink/submodule/device/FIFO/socket | prohibited unless separately reviewed path contract | none |

Effective `.gitattributes`, `.git/info/attributes`, system/global/local config, `core.autocrlf`, `core.eol`, `core.filemode`, filters, working-tree-encoding and text attributes are inventoried. Candidate uses raw manifest bytes and explicit Git modes; no implicit checkout normalization. Tests with `core.autocrlf=true/false` must derive the same candidate tree/package. Existing 21 source paths receive no EOL-only source diff because source bytes are never rewritten.

### 16.3. Temp and secret safeguard order

Before any generator/build/test:

1. qualify external private temp, journal, candidate, raw-output and evidence roots under V3/V9 path policy;
2. freeze exact generator outputs and write manifests;
3. verify repo/Vault roots are not descendants/ancestors/aliases of temp roots;
4. install/verify `.gitignore` only later under exact candidate authority for nonsensitive convenience; secrets never rely on ignore;
5. run full no-ignore secret/PII canaries across source snapshot, private candidate, ignored/untracked files, ADS inventory and recursively validated archives;
6. reject generator paths that resolve into repo/Vault or outside approved lab root before first create.

Secret values are never test fixtures. Synthetic unique markers are used, and evidence records only marker IDs/counts. A marker in ignored file, ADS, archive, logs, package or evidence gives `V9_FAIL_SECRET_OR_PII`.

## 17. Acceptance tests, negative canaries and evidence catalog

| ID | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `AT-V9-01` | Two independent builders produce byte-identical source custody manifest for exact HEAD/index/21 paths/full no-ignore worktree/`.git`. | `NC-V9-01`: byte/mode/type/HEAD/index/ignored/nested-untracked drift blocks before write. | `EV-V9-01-SOURCE-CUSTODY` manifests, aggregates and no-write discovery ledger. |
| `AT-V9-02` | Base tree plus frozen dirty overlay materializes private baseline; source/Vault never mounted or written. | `NC-V9-02`: private builder attempts source/`.git`/Vault write or rereads changed source after freeze. | `EV-V9-02-PRIVATE-BASELINE` materialization manifest and source invariance. |
| `AT-V9-03` | Every scope has exact root/write allowlist and full before/after equality outside set. | `NC-V9-03`: ignored repo file, `.git`, Vault, ADS or unlisted lab write. | `EV-V9-03-WRITE-SCOPES` root identities, operation records and diffs. |
| `AT-V9-04` | Handle-based safe path tests pass for private roots and every authorized host write. | `NC-V9-04`: junction/symlink/hardlink/case/NFC/8.3/ADS/ancestor swap; outside sentinel unchanged. | `EV-V9-04-PATH-CUSTODY` handle/identity timeline and sentinel result. |
| `AT-V9-05` | Fault after every journal boundary restores byte-identical prestate or preserves explicit conflict. | `NC-V9-05`: concurrent edit before rollback; wrapper must not overwrite it. | `EV-V9-05-WRITE-JOURNAL` chain, pre/post/recovery hashes and orphan scan. |
| `AT-V9-06` | Candidate archive extraction reproduces full manifest and aggregate; all consumers use same digest. | `NC-V9-06`: mutate byte/mode/path/EOL or add ignored file after freeze. | `EV-V9-06-CANDIDATE` manifest/archive/tree identities and consumer receipts. |
| `AT-V9-07` | Expected and observed stable row-ID sets match exactly for 66/34/8, including fixture and expectation hashes. | `NC-V9-07`: delete/duplicate/add/rename/substitute one row in every set. | `EV-V9-07-ROW-CONTRACTS` three manifests and set-equality results. |
| `AT-V9-08` | A/B independently validate same immutable inputs; reconciler proves implementation separation and result equality. | `NC-V9-08`: same implementation hash, copied output or crafted edge disagreement. | `EV-V9-08-VALIDATORS` BOMs, process lineage, separate outputs and reconciliation. |
| `AT-V9-09` | Executed runner and package-extracted runner have exact same bytes/dependencies/argv identity. | `NC-V9-09`: surrogate harness, PATH substitution, post-freeze runner replacement. | `EV-V9-09-RUNNER` pre/post-exec and package extraction receipts. |
| `AT-V9-10` | Two independently provisioned clean runs have equal row/status/RC/normalized semantic hashes. | `NC-V9-10`: stale PASS/output, shared writable cache or fingerprint drift. | `EV-V9-10-CLEAN-RUNS` emptiness proofs, fingerprints and comparison. |
| `AT-V9-11` | Each fault proves external trigger, expected intermediate failure, recovery invariants and paired control. | `NC-V9-11`: disabled/no-op/mistimed shim or broken rollback. | `EV-V9-11-FAULT-RECEIPTS` shim/trigger/control/assertion records. |
| `AT-V9-12` | Table-driven row/gate/run/scope aggregation accepts every legal and rejects every illegal state/RC transition. | `NC-V9-12`: forged PASS, zero RC missing row, unbacked MANUAL_PASS, OFFLINE block promoted to SUCCESS. | `EV-V9-12-RESULTS` schema/state-machine conformance matrix. |
| `AT-V9-13` | LOCAL/OFFLINE records append without changing imported REMOTE_EXHAUSTED; every started attempt has one terminal. | `NC-V9-13`: reuse local evidence/run ID as REMOTE or edit/delete an old record. | `EV-V9-13-ATTEMPTS` hash-linked ledger and per-scope budget report. |
| `AT-V9-14` | Exact-set evidence envelope verifies manifest, anchor, commands, RC, rows, writes and deterministic redaction. | `NC-V9-14`: remove/add/replace/move cross-run file; alter status with same transcript; redaction changes semantic field. | `EV-V9-14-EVIDENCE-SEAL` envelope/manifest/anchor/redaction audit. |
| `AT-V9-15` | Private index produces expected tree/commit; optional new-ref CAS leaves source HEAD/index/worktree identical. | `NC-V9-15`: pre-staged unrelated index, hook/filter drift, branch/ref move, concurrent worktree edit. | `EV-V9-15-GIT-PROVENANCE` parent/tree/commit/object/ref/index/worktree transition manifests. |
| `AT-V9-16` | Package generated from commit tree is exact candidate projection and contains executed runner. | `NC-V9-16`: package from worktree, extra ignored file, path/mode/EOL drift. | `EV-V9-16-PACKAGE` projection, archive/extraction and delivery successor identity. |
| `AT-V9-17` | Windows checkout/config variants yield identical candidate tree and Linux scripts satisfy raw LF/mode policy. | `NC-V9-17`: CRLF/BOM/filter/mode-only drift. | `EV-V9-17-BYTE-POLICY` config/attribute inventories and blob-level comparison. |
| `AT-V9-18` | Qualified temp roots and full no-ignore/ADS/archive scan precede every generator and package. | `NC-V9-18`: generator targets repo-relative temp or marker hidden in ignored/ADS/archive. | `EV-V9-18-TEMP-SECRET` root guard, write-zero proof and scans. |

All EV artifacts are future obligations. None exists or passes merely because this draft defines it.

## 18. Traceability: V0 finding → V9 contract / AT / NC / EV

### 18.1. Primary R8 evidence/K4R findings

| Source finding | V9 contracts | AT / NC / EV | Disposition |
|---|---|---|---|
| `R8-P1-001` | `V9-C07` | `AT/NC/EV-V9-07` | `DESIGN_CLOSED`; row hashes pending future freeze |
| `R8-P1-002` | `V9-C08` | `AT/NC/EV-V9-08` | `DESIGN_CLOSED`; tools/independence pending V2/runtime |
| `R8-P1-003` | `V9-C06`, `V9-C09`, `V9-C15`, `V9-C16` | `AT/NC/EV-V9-06`, `09`, `15`, `16` | `DESIGN_CLOSED`; candidate/commit/package pending |
| `R8-P1-004` | `V9-C10` | `AT/NC/EV-V9-10` | `DESIGN_CLOSED`; two runtime runs pending |
| `R8-P1-005` | `V9-C11` | `AT/NC/EV-V9-11` | `DESIGN_CLOSED`; fault execution pending |
| `R8-P1-006` | `V9-C12` | `AT/NC/EV-V9-12` | `DESIGN_CLOSED`; global namespace integration pending |
| `R8-P1-007` | `V9-C13` | `AT/NC/EV-V9-13` | `DESIGN_CLOSED`; historical ledger import pending |
| `R8-P1-008` | `V9-C10`, `V9-C11` | `AT/NC/EV-V9-10`, `11` | `XDEP-V4`; V9 consumes network proof and positive control |
| `R8-P1-009` | `V9-C10` | `AT/NC/EV-V9-10` | `DESIGN_CLOSED`; observed fingerprint pending V1/V2/V4 |
| `R8-P1-010` | `V9-C14` | `AT/NC/EV-V9-14` | `DESIGN_CLOSED`; trusted collector implementation pending |
| `R8-P2-011` | `V9-C08`, `V9-C10` | `AT/NC/EV-V9-08`, `10` | `XDEP-V2`; exact tool BOM pending |
| `R8-P2-012` | `V9-C11`, `V9-C14` | `AT/NC/EV-V9-11`, `14` | `XDEP-V4`; exact object labels/cleanup runtime pending |

### 18.2. Primary R9 dirty-worktree/Git findings

| Source finding | V9 contracts | AT / NC / EV | Disposition |
|---|---|---|---|
| `R9-F01` | `V9-C01` | `AT/NC/EV-V9-01` | `DESIGN_CLOSED`; exact machine snapshot pending |
| `R9-F02` | `V9-C02`, `V9-C03` | `AT/NC/EV-V9-02`, `03` | `DESIGN_CLOSED`; authoring touchset pending freeze |
| `R9-F03` | `V9-C04` | `AT/NC/EV-V9-04` | `DESIGN_CLOSED`; runtime Windows fixtures pending |
| `R9-F04` | `V9-C01`, `V9-C02`, `V9-C15` | `AT/NC/EV-V9-01`, `02`, `15` | `DESIGN_CLOSED`; concurrency canaries pending |
| `R9-F05` | `V9-C06`, `V9-C15`, `V9-C16` | `AT/NC/EV-V9-06`, `15`, `16` | `DESIGN_CLOSED`; exact candidate pending |
| `R9-F06` | `V9-C15` | `AT/NC/EV-V9-15` | `DESIGN_CLOSED`; private commit/integration pending explicit gate |
| `R9-F07` | `V9-C05` | `AT/NC/EV-V9-05` | `DESIGN_CLOSED`; fault matrix pending |
| `R9-F08` | `V9-C03`, `V9-C14`, `V9-C15` | `AT/NC/EV-V9-03`, `14`, `15` | `DESIGN_CLOSED`; full pre/post runtime manifests pending |
| `R9-F09` | `V9-C17` | `AT/NC/EV-V9-17` | `DESIGN_CLOSED`; effective attributes pending snapshot |
| `R9-F10` | `V9-C18` | `AT/NC/EV-V9-18` | `DESIGN_CLOSED`; generator/package scans pending |

### 18.3. Material cross-findings

| Source finding | V9 contribution | AT / NC / EV | Remaining owner |
|---|---|---|---|
| `R2-003` | `V9-C04/C05` artifact/file TOCTOU mechanics | `AT/NC/EV-V9-04`, `05` | V2 signer/source/acquisition |
| `R2-005` | `V9-C06/C16` immutable build/package context | `AT/NC/EV-V9-06`, `16` | V2 dependency/build provenance |
| `R2-012` | `V9-C14` content-addressed audit envelope | `AT/NC/EV-V9-14` | V2 authoritative sources |
| `R3-CLEAN-007` | `V9-C11/C14` cleanup receipts and evidence identity | `AT/NC/EV-V9-11`, `14` | V4 Docker object custody |
| `R6-P1-006` | `V9-C14/C18` source allowlist, redaction audit and canaries | `AT/NC/EV-V9-14`, `18` | V7 privacy/schema policy |
| `R10-F06` | owner can independently verify delivery/evidence hashes | `AT/NC/EV-V9-06`, `14`, `16` | V10 black-box runbook |

## 19. Cross-domain dependencies and conflicts

### 19.1. Required interfaces

| Owner section | V9 consumes | V9 provides |
|---|---|---|
| V1 Windows/control plane | approved local endpoint, execution lock, operator identity, read-only host guard | operation/candidate/evidence hashes; no source mutation |
| V2 supply chain | exact Git/tool/validator/collector/archive/image BOM, OCI digests and provenance | candidate/build/package context identity and delivery anchor |
| V3 resources/storage | approved private/journal/evidence/temp roots, ACL/volume identity, peak limits | exact writes, sizes, evidence retention inputs and no-source-write proof |
| V4 isolation/network | archive-to-fresh-volume path, no source binds, network-none/positive controls, labels/object IDs, environment fingerprint | candidate/runner/row digests and cleanup/evidence identities |
| V5 Compose/n8n/PostgreSQL | exact gate project/service/runner integration and application-volume prohibition | actual runner/package identity, gate result and release provenance |
| V6 Telegram | no real-dev/arming/provider side effects during gate; candidate/workflow inventory hash | exact candidate/workflow/run evidence IDs only |
| V7 secrets/privacy | source allowlist, forbidden fields, pseudonym/redaction/scanner schemas | field-level redaction audit, package/candidate no-secret proof |
| V8 backup/cold restore | operation/result records and source/target invariance | shared evidence-envelope protocol; V8 child cannot seal its own COMPLETE |
| V10 operability | owner CLI/status/verify/package handoff and global mapping | stable V9 substates, exact next-safe-action and offline verification commands |

### 19.2. Conflicts requiring canonical integration

1. Neighboring drafts sometimes call evidence/K4R `V8` and backup/recovery `V7`, while assigned files make backup `V8` and this custody domain `V9`. Canonical integrator must freeze one numbering map and mechanically rewrite links before review; until then `V9_BLOCKED_CONTRACT_DRIFT`.
2. V4 calls candidate transfer a Docker archive/API stream into named volume. V9 requires deterministic candidate archive and full extraction equality. Integrated plan must declare one exact archive format/tool/BOM and prove both semantics; a generic `docker cp` or mutable bind is not equivalent.
3. V2 uses RFC 8785/JCS for locks; V1/V3/V4/V5/V6/V7/V8 use several prose canonicalization variants. Global plan must assign schema-specific canonicalizers and hashes. V9 cannot claim a single aggregate while canonicalization is ambiguous.
4. RC ranges in V1–V8 overlap and names differ. V9 scoped semantic states are normative for custody/evidence; final integrator must map child RC/status into one global envelope without changing child meaning. Unknown mapping blocks.
5. V4 plan A forbids root/SYS_ADMIN/privileged-equivalent O5 rows. V9 preserves honest `OFFLINE_BLOCKED_CAPABILITY`; it does not reinterpret them as skipped or pass.
6. V5 names one `gate-runner`, while V9 requires actual production runner plus two independent validators and trusted collector. Integrated topology must separate identities/processes and prove no validator output sharing; one service name cannot imply one implementation.
7. V8 backup evidence and V9 run evidence both propose envelopes. V9 owns outer exact-set run seal; V8 owns backup semantic records. V8 COMPLETE/RESTORE_VERIFIED must be a collector-validated child record inside V9 envelope, not a competing self-sealed truth.
8. Updating a checked-out source branch to a commit containing the 21 dirty paths would alter their Git status semantics even if bytes stay unchanged. V9 therefore permits only a new candidate ref while source remains dirty; branch promotion requires a later owner decision.

Stricter contract wins. Missing or conflicting interface yields `V9_BLOCKED_CONTRACT_DRIFT`; permissions are never unioned.

## 20. Future phase order and gates

All steps are future obligations after frozen full plan v2 and applicable owner approvals:

1. Freeze numbering, schema canonicalizers, global state/RC mapping and V1–V8 interface hashes.
2. Run read-only source/Vault/lab-root discovery; independently create `source_custody_manifest/v2`; prove discovery no-write.
3. Freeze exact private authoring touchset and write journal authority; preserve source HEAD/index/21 paths.
4. Materialize private base+dirty snapshot and implement corrections/local-lab artifacts only there.
5. Freeze candidate, actual runner and exact 66/34/8 row manifests; perform secret/PII and byte-policy gates.
6. Acquire/qualify exact validator/collector/image/tool locks through V2 and resources/roots/containment through V1/V3/V4.
7. Execute two clean runs, all fault/control/canary rows and independent reconciliation. Append scoped attempts without touching REMOTE budget.
8. Seal exact-set evidence and obtain independent review of the same candidate/evidence anchor.
9. Create private commit tree; verify tree equals candidate; generate and verify package from commit tree.
10. Only under a new exact integration authority optionally import objects and create a new candidate ref while source HEAD/index/worktree remain unchanged.
11. Owner/independent reviewer verifies delivery identity, package, runbook and residual blocked scopes.
12. Production/REMOTE remains a separate exact-candidate authorization and rerun; no local result grants it.

Manual gates relevant to V9:

| Gate | Exact decision | Blocks |
|---|---|---|
| `MG-V9-PLAN` | frozen full plan v2 hash, numbering and V9 scope | all V9 execution |
| `MG-V9-ROOTS` | exact private/temp/journal/evidence roots and residual trust | first host write |
| `MG-V9-REPO-WRITE` | exact authoring touchset in private copy, not source | authoring |
| `MG-V9-CANDIDATE` | candidate/runner/row contract hashes and attempt budget | validator/test start |
| `MG-V9-INTEGRATE` | exact private commit, source guard, new ref and `.git` write manifest | source object/ref write |
| `MG-V9-PUBLISH` | exact package/delivery anchor and destination create-new target | package publication |
| `MG-V9-REMOTE` | separate remote authority, fingerprint, retry budget and rollback | any REMOTE execution; not implied here |

## 21. STOP/BLOCKED conditions

Immediate STOP or BLOCKED before next mutation:

- source `HEAD`, ref, index, 21-path snapshot, ignored inventory, `.git`, Vault or physical root identity drift;
- custody builders disagree or count-only dirty inventory is supplied;
- authoring/candidate consumes mutable source bind or linked worktree;
- any write lacks exact manifest/journal/root identity;
- reparse/symlink/junction/hardlink/case/Unicode/8.3/ADS/TOCTOU ambiguity;
- candidate, runner, row manifest, validator, environment, commit tree, package or evidence hash mismatch;
- incomplete/duplicate/extra 66/34/8 row set;
- validators are not independent, one is missing, or their results disagree;
- stale/shared output/cache or two clean runs differ semantically;
- fault trigger, positive control, paired control or cleanup receipt absent;
- forged/missing/contradictory result/RC/evidence;
- local/offline attempt presented as remote or remote exhausted state changed without new authority;
- evidence source not allowlisted, redaction/scanner fails or secret/PII marker appears;
- Git integration would move current HEAD/branch, touch user index/worktree, invoke hooks/filters or include unrelated content;
- rollback meets concurrent drift; preserve conflict and stop;
- any requirement needs plan B, VPS or broader privileges without a new owner decision.

## 22. Residual risks

1. Windows kernel, SYSTEM, approved Administrators and Docker control-plane principals remain trusted and can bypass user-mode path/container controls.
2. Full source/Vault/`.git` manifests detect changes inside declared roots but do not prove that an unrestricted host process never wrote elsewhere. V9 therefore requires contained authoring/test processes with no host roots and exact wrapper writes; OS-level provenance beyond that boundary remains a residual.
3. Hashes prove byte identity, not semantic correctness. Independent validators, actual runner, fault controls and review are compensating layers.
4. A private commit and candidate ref preserve the dirty source worktree but do not finish branch integration. Promotion remains blocked until the owner chooses how to reconcile the original dirty state.
5. Git object import can add unreachable/extra objects if pack construction or verification is wrong. Exact pack/object manifest and post-import object-set proof limit but do not remove trusted Git implementation risk.
6. Deterministic archives depend on exact tool/version/format behavior. Unsupported metadata determinism is `BLOCKED_TOOL`, not acceptance of a new hash after every build.
7. Two clean runs on the same Docker Desktop fingerprint do not prove remote compatibility. REMOTE requires its own run.
8. Plan A may never satisfy O5 rows requiring forbidden root/SYS_ADMIN semantics. Honest `OFFLINE_BLOCKED_CAPABILITY` is an accepted scoped outcome, not full offline readiness.
9. Evidence redaction may remove useful diagnostics. Fail-closed source allowlisting favors privacy; incident-only raw diagnostics require a separate V7 owner gate and are not release evidence.

## 23. Definition of Done V9 design and future runtime

### Design DoD

V9 is design-ready for canonical integration review only when:

- all `R8-P1-001..010`, `R8-P2-011..012` and `R9-F01..F10` retain explicit contract + AT + NC + EV mappings;
- source HEAD `11974...`, user index and exact 21-path snapshot are protected by a full reproducible custody contract;
- no stash/reset/clean/checkout or linked-worktree mutation path exists;
- private authoring, source repo, `.git`, Vault and lab roots have separate authorities/manifests;
- path, write-journal, rollback and concurrency semantics are fail-closed;
- candidate, runner, row contracts, commit tree, package and evidence share one successor content identity;
- 66/34/8 are exact row sets, not counts;
- validators, runner, two clean runs, environment fingerprint and fault receipts are executable contracts;
- LAB/LOCAL/OFFLINE/REMOTE states and attempts cannot cross-promote;
- trusted collector alone seals evidence;
- private index/commit/package semantics preserve source worktree/index;
- EOL/mode/attributes and secret/temp safeguards are explicit;
- all V1–V8 dependencies/conflicts and residuals remain visible;
- no runtime PASS, repository commit, installation, Docker/network/VPS action or secret access is claimed.

### Future runtime DoD

`V9_OFFLINE_PASS` is possible only when exact frozen plan/authority/source custody/candidate/runner/row/validator/tool/environment identities exist, both clean runs and all required canaries pass, evidence exact-set verifies, independent review accepts the same anchor and attempt ledger records a valid terminal result. `V9_RELEASE_CANDIDATE_READY` additionally requires private commit tree equality and package-from-commit-tree equality. Neither state updates the source checked-out branch or grants REMOTE/production authority.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
