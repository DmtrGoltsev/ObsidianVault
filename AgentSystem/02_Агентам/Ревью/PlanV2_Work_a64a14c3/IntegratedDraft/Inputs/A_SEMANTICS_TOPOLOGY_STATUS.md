---
тип: corrective-specification
проект: N8NAgents
версия: R2-A-draft-1
статус: DRAFT_NOT_FROZEN
дата: 2026-08-27
область: [AT-NC-EV, topology, telegram-egress, backup-verifier, child-status]
runtime_claims: none
теги: [n8nagents, correction-r2, semantics, topology, status]
---

# Correction R2/A — semantic catalogs, topology and child-status replacement

## 0. Назначение и запреты

Этот документ — **replacement specification**, а не исправленный canonical artifact и не свидетельство исполнения. Он задаёт единственный допустимый способ пересобрать `09/10/11/12/18` и связанные topology fragments после final prefreeze audit. Никакие Windows, Docker, VPS, provider, secret, repo или Vault runtime actions здесь не выполнялись. Состояние остаётся `DRAFT_NOT_FROZEN / RUNTIME_NOT_RUN`.

Запрещено при реализации этой спецификации:

- сохранять `SYNTHETIC_EXACT_POSITIVE`, `SYNTHETIC_EXACT_INTEGRATION`, «execute source procedure», «positive boundary» или иной placeholder как semantic fixture/procedure;
- выводить outcome, status, RC или `mutation_started` из имени finding/status, regex, числового `max()` или domain-wide default;
- считать механическую cardinality/hash проверку semantic review;
- ослаблять A-only, подменять Plan B, обращаться к VPS/provider, читать реальные secrets или объявлять runtime PASS;
- добавлять service/network/mount/secret membership вне exact sets этого документа.

## 1. Зафиксированные входы

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `07_FINDING_DISPOSITIONS_V2.json` | 192796 | `2c108d75b5046446249108894f96f46a8e0186996f518ebf026d7128e56343ba` |
| `09_ACCEPTANCE_TEST_CATALOG.json` | 209236 | `b6fe861c53965bd55c2181033d3cc6b17a216000656eecb6476393df53feaf16` |
| `10_NEGATIVE_CANARY_CATALOG.json` | 229800 | `4fcc66c473185309b42012e0170d79a16b78d24714ca58ae08285e7039ea5df7` |
| `11_EVIDENCE_CATALOG.json` | 205401 | `573c9ea526bbd16ccaebb38e58cd2bc33b3b9a1316599cb59dcf02fb7688edd9` |
| `12_CANONICAL_ALIAS_MAP_V2.json` | 378224 | `b95476448328ccb1385a2e2aa39a63a61054adfd5ff17f545e4d5f9f510b27b2` |
| `18_CHILD_STATUS_MAPPING_V2.json` | 180751 | `6c3c279ca3a836db7cb3e26259672938ff7dfcf2422bea71ee95b63397da8f04` |
| `12_CROSS_DOMAIN_INTEGRATION_DECISIONS.md` | 54686 | `885843a253c67c81d658d60414a9ca4f699843518a7ce67daa6ccaa6a5ab8e64` |

Исходная exact cardinality: `114 findings + 15 XD = 129` AT, 129 NC, 129 EV; `306` native child-status keys. Canonical 306-key set hash is `afd05d828c22c9132b7e00612781c776ddc922ea089c2a61cf14f1921e589c06`, computed by requiring ASCII keys, sorting the unique strings with ordinal/code-point order (which equals UTF-8 byte order for ASCII), joining with byte `0x0A`, and appending exactly one final `0x0A`. Culture-aware collation is forbidden.

## 2. Replacement data model для всех 129 AT/NC/EV

### 2.1. Одна typed semantic record на source ID

Каждая строка реестра §3 обязана развернуться в один объект следующей формы; ссылки на prose без этих полей недостаточны.

```yaml
schema: n8nagents.semantic-test-contract/v3
source_id: <one of exact 129>
semantic_key: <exact key from §3>
source_binding:
  source_hash: <existing exact finding/XD hash>
  source_refs: [<file:line>]
acceptance:
  id: AT-F-<finding> | AT-<XD>
  fixture:
    fixture_type: <semantic_key>.positive/v1
    case_ids: [<closed nonempty set>]
    input_schema_sha256: <sha256>
    setup_state_sha256: <sha256>
    locks: {plan, integration, runtime, image, policy}
    secret_class: NONE | SYNTHETIC_MARKER | OWNER_SUPPLIED_REAL_GATE
  procedure:
    procedure_id: PROC-<semantic_key>-v1
    executor_identity: <exact role/image/tool>
    entrypoint_argv_sha256: <sha256>
    ordered_steps: [{step_id, verb, target, input_ref, timeout_ms, effect_class}]
    positive_control: <exact expected observation>
    cleanup: <exact object-custody action or NONE>
  outcome:
    decision: PASS
    status: G_PASS_EXACT_REQUESTED_SCOPES
    rc: 0
    mutation_rule: ZERO | ONE_OR_MORE | CASE_COUNTER
    success_scope: <exact requested child scope only>
negative:
  id: NC-F-<finding> | NC-<XD>
  fixture_type: <semantic_key>.single-field-negative/v1
  base_fixture_sha256: <AT fixture hash>
  mutation: {json_pointer, from_sha256, to_sha256, count: 1}
  injection_phase: BEFORE_FIRST_EFFECT | AFTER_FIRST_EFFECT
  outcome: {decision, status, rc, mutation_rule}
  forbidden_effect_profile: <F0..F8>
evidence:
  id: EV-F-<finding> | EV-<XD>
  schema: n8nagents.evidence.<semantic_key>/v3
  producer: trusted-evidence-collector
  typed_payload: <closed schema, not free-form text>
  predicates: [<field-addressed boolean predicates>]
  forbidden_fields: <E-FORBID-BASE plus semantic additions>
```

### 2.2. Outcome codes и effect rules

| Code | Exact tuple |
|---|---|
| `P0` | `PASS / G_PASS_EXACT_REQUESTED_SCOPES / 0` |
| `O10` | `READY_OWNER_GATE / G_READY_OWNER_GATE / 10` |
| `B30` | `BLOCKED / G_BLOCKED_UNKNOWN / 30` |
| `B31` | `BLOCKED / G_BLOCKED_CAPABILITY / 31` |
| `B32` | `BLOCKED / G_BLOCKED_CONTRACT_DRIFT / 32` |
| `B33` | `BLOCKED / G_BLOCKED_POLICY / 33` |
| `B34` | `BLOCKED / G_BLOCKED_RESOURCE / 34` |
| `B35` | `BLOCKED / G_BLOCKED_IDENTITY / 35` |
| `B36` | `BLOCKED / G_BLOCKED_DEPENDENCY / 36` |
| `B37` | `BLOCKED / G_BLOCKED_MANUAL / 37` |
| `F40` | `FAIL / G_FAIL_VALIDATION / 40` |
| `F41` | `FAIL / G_FAIL_OPERATION / 41` |
| `F42` | `FAIL / G_FAIL_CONTAINMENT / 42` |
| `F43` | `FAIL / G_FAIL_INTEGRITY / 43` |
| `S50` | `STOP / G_STOP_SCOPE_EXPANSION / 50` |
| `S51` | `STOP / G_STOP_SECURITY / 51` |
| `S52` | `STOP / G_STOP_RESULT_INVALID / 52` |
| `S53` | `STOP / G_EMERGENCY_UNVERIFIED / 53` |
| `S54` | `STOP / G_INCIDENT_OPEN / 54` |

`READY_OWNER_GATE/G_BLOCKED_MANUAL/37` запрещён как internally contradictory tuple. `O10` означает, что exact artifact уже подготовлен и единственная следующая операция — именованный owner gate. Невалидное/просроченное owner решение после gate — `B37`, а не `O10`.

Mutation rules:

- `Z` = `ZERO`: `first_effect_counter == 0`, `mutation_started=false`;
- `M` = `ONE_OR_MORE`: `first_effect_counter >= 1`, `mutation_started=true`;
- `C` = `CASE_COUNTER`: каждый `case_id` заранее объявляет `Z` или `M`; aggregate `mutation_started = OR(case.mutation_started)`. Необъявленный case запрещён;
- для NC `B` = injection `BEFORE_FIRST_EFFECT`, rule `Z`; `A` = injection `AFTER_FIRST_EFFECT`, rule `M`; `D` = exact value берётся из child `first_effect_counter`, но только если NC fixture содержит два заранее хешированных subcase `before` и `after`. Missing counter даёт `S52`.

### 2.3. Forbidden-effect profiles

Каждый профиль — exact named counters, не текстовый список:

| Profile | Все counters, которые обязаны быть `0` |
|---|---|
| `F0` | `provider_requests`, `external_sockets`, `host_mutations`, `docker_mutations`, `secret_reads`, `source_writes`, `vault_writes`, `vps_effects`, `destructive_effects`, `pass_publications` |
| `F1-HOST` | `unexpected_uac`, `reboot_requests`, `security_control_changes`, `foreign_install_changes`, `nonlocal_daemon_calls`, плюс `F0` вне exact host target |
| `F2-SUPPLY` | `unlocked_downloads`, `mutable_tag_uses`, `unknown_origin_requests`, `unverified_execs`, `license_acceptance`, плюс `F0` |
| `F3-CONTAIN` | `host_socket_mounts`, `privileged_containers`, `extra_caps`, `extra_devices`, `host_pid_ipc`, `outside_root_writes`, `unexpected_network_edges`, `unexpected_listeners` |
| `F4-DATA` | `foreign_volume_writes`, `source_volume_writes`, `plaintext_persistent_writes`, `unapproved_schema_writes`, `extra_db_writers`, `complete_markers` |
| `F5-PROVIDER` | `unarmed_calls`, `wrong_bot_calls`, `wrong_recipient_calls`, `unreserved_sends`, `unreserved_cost`, `redirect_follows`, `direct_ip_calls`, `provider_payload_persistence` |
| `F6-SECRET` | `argv_secret_occurrences`, `env_secret_occurrences`, `log_secret_occurrences`, `evidence_secret_occurrences`, `unapproved_consumer_reads`, `plaintext_backup_occurrences` |
| `F7-GATE` | `nic_interfaces`, `provider_calls`, `secret_mounts`, `source_mounts`, `candidate_seals`, `validator_identity_overlap`, `stale_evidence_accepts` |
| `F8-CUSTODY` | `out_of_touchset_writes`, `foreign_repo_writes`, `source_commits`, `vault_writes`, `unreviewed_publications`, `raw_identity_disclosures` |

All profiles also require the source-specific sentinel counter and `unexpected_effect_total == 0`. A negative test that intentionally proves a forbidden effect after it occurs records that exact canary counter in `observed_fault_effect`; it must still keep every *other* forbidden counter zero and cannot PASS.

### 2.4. Evidence base fields

Every EV contains typed base fields:

```text
schema, evidence_id, source_id, semantic_key, run_id, case_id,
plan_sha256, integration_lock_sha256, source_binding_sha256,
fixture_schema_sha256, fixture_instance_sha256, procedure_sha256,
executor_identity_sha256, pre_state_sha256, post_state_sha256,
first_effect_counter_before, first_effect_counter_after,
mutation_started, decision, status, rc,
forbidden_effect_counters, typed_payload_sha256,
collector_image_digest, collector_entrypoint_sha256,
observed_at_utc, validity_window, artifact_refs, evidence_record_sha256
```

`mutation_started` must equal `(first_effect_counter_after > first_effect_counter_before)` except `Z`, which additionally requires both counters `0`. Forbidden in every EV: raw token/password/private key, message/prompt content, raw Telegram/user/chat/thread tuple, raw SID/username/path/volume serial, VPS/IP/fingerprint, headers/cookies, clipboard, dumps, unrestricted stdout/stderr, unredacted exception text.

## 3. Exact 129-entry semantic registry

Machine interpretation of each row:

- `semantic_key` fixes `fixture_type`, `procedure_id` and EV schema suffix exactly as in §2.1;
- `AT operation` is the typed stimulus and oracle; it replaces the generic procedure array;
- `ATm` is the acceptance mutation rule from §2.2;
- `NC pointer` is the only mutated JSON pointer; `NC result/effect` fixes tuple and injection rule;
- `FP` is the forbidden profile. The generated EV payload must include the before/after typed object named by `semantic_key` and every oracle field named in `AT operation`.

### 3.1. R1 — Windows/control plane (12)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R1-WIN-001 | `host.endpoint-pin` | Resolve explicit approved Desktop context; compare canonical endpoint and daemon identity before every operation; harmless local daemon positive control only. | Z | `/docker/endpoint_uri` | B35/B | F1-HOST |
| R1-WIN-002 | `host.support-matrix` | Evaluate supported/unsupported/below-threshold/unreadable/contradictory fixtures; only exact supported tuple validates. | Z | `/windows/support_predicate` | B30/B | F1-HOST |
| R1-WIN-003 | `host.feature-delta-gate` | Hash exact optional-feature delta and reboot expectation; produce preview and owner-gate record without applying it. | Z | `/windows/feature_delta_sha256` | O10/B | F1-HOST |
| R1-WIN-004 | `host.principal-boundary` | Correlate non-elevated operator, UAC principal, Docker access and owner-only roots; prove approved/denied canaries. | Z | `/operator/elevation_principal` | O10/B | F1-HOST |
| R1-WIN-005 | `host.existing-install-disposition` | Classify clean/partial/old/owned/unknown/alternate/conflicting install inventory into one exact branch. | Z | `/docker/existing_install_branch` | B30/B | F1-HOST |
| R1-WIN-006 | `host.install-rollback` | In disposable Windows fixture apply exact install, first launch, controlled stop/uninstall and compare accounted before/after state. | C | `/install/rollback_equivalence` | F41/D | F1-HOST |
| R1-WIN-007 | `host.resource-admission` | Evaluate byte-exact disk/RAM/commit/CPU reserve on both threshold sides for each operation; below side performs no mutation. | Z | `/resource/host_reserve_bytes` | B34/B | F1-HOST |
| R1-WIN-008 | `host.storage-root-qualification` | Open-by-handle qualify local ACL-capable nonsync non-reparse root and managed-data location; compare parent/leaf identity. | Z | `/storage/root_reparse_tag` | B33/B | F1-HOST |
| R1-WIN-009 | `host.runtime-drift-lock` | Compare every observed Desktop/Engine/Compose/setting field to runtime lock; exact equality is the oracle. | Z | `/runtime/lock_sha256` | B32/B | F1-HOST |
| R1-WIN-010 | `host.security-policy-observation` | Read policy/quarantine/block state without exclusions or retries; classify unreadable or blocked executable fail-closed. | Z | `/security_policy/readable` | B33/B | F1-HOST |
| R1-WIN-011 | `host.reboot-checkpoint` | Generate pre-reboot checkpoint, reject boot-id drift/cancelled UAC and require fresh post-reboot revalidation. | Z | `/reboot/checkpoint_boot_id` | O10/B | F1-HOST |
| R1-WIN-012 | `host.loopback-port-custody` | Prove 5678 owner/listener tuple and successful `127.0.0.1` control while wildcard/LAN/WSL/VPN/portproxy sets are empty. | Z | `/n8n/loopback_port_owner` | B36/B | F3-CONTAIN |

### 3.2. R2 — supply chain (12)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R2-001 | `supply.origin-lock` | Validate final origin, redirect chain, artifact hash and evidence binding against one approved source lock. | Z | `/supply/final_origin` | F43/B | F2-SUPPLY |
| R2-002 | `supply.signer-chain` | Verify file hash, publisher thumbprint, trust chain, timestamp, revocation and expected product tuple. | Z | `/installer/signer_thumbprint` | F43/B | F2-SUPPLY |
| R2-003 | `supply.acquire-open-handle` | Verify downloaded file through stable handle; recheck file/parent identity and hash immediately before exec. | Z | `/acquisition/sha256` | F43/B | F2-SUPPLY |
| R2-004 | `supply.oci-platform-leaf` | Resolve registry/index/amd64 child/config/layers by digest and compare rendered/loaded image identity. | Z | `/oci/platform_leaf_digest` | F43/B | F2-SUPPLY |
| R2-005 | `supply.reproducible-build` | Build clean-cache from exact materials and compare material graph/final digest under declared reproducibility policy. | M | `/build/materials_sha256` | F43/B | F2-SUPPLY |
| R2-006 | `supply.runtime-current-lkg` | Compare current and LKG runtime tuples; staged failure retains verified prior lock and blocks unqualified run. | Z | `/runtime/previous_lock_sha256` | B32/B | F2-SUPPLY |
| R2-007 | `supply.license-owner-record` | Validate exact terms revision and owner attestation; prove no silent acceptance switch or download before acceptance. | Z | `/license/exact_revision` | B33/B | F2-SUPPLY |
| R2-008 | `supply.scan-sbom-policy` | Bind scanner DB freshness, SBOM subject digest, threshold and waiver tuple; clean fixture alone passes. | Z | `/scan/policy_result` | B33/B | F2-SUPPLY |
| R2-009 | `supply.lkg-offline-import` | Import retained exact amd64 OCI objects into disposable clean data root and prove isolated start without registry. | C | `/lkg/offline_import_verified` | B31/B | F2-SUPPLY |
| R2-010 | `supply.extension-allowlist` | Deny runtime/UI package install; prove allowed node exists only in pinned reviewed image and inventory. | Z | `/n8n/extension_allowlist` | B33/B | F2-SUPPLY |
| R2-011 | `supply.installed-identity` | Complete exact installer fixture then bind observed installed build/channel/update state to installer and lock. | C | `/installed/identity_sha256` | F43/B | F2-SUPPLY |
| R2-012 | `supply.source-evidence-replay` | Independent offline auditor reconstructs each lock claim from retained exact source bytes and redirects. | Z | `/evidence/source_set_sha256` | S52/D | F2-SUPPLY |

### 3.3. R3 — containment/topology (8)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R3-CLEAN-007 | `contain.object-custody-cleanup` | Drain invocation-owned objects, compare exact label+ID+creation tuple, delete only approved disposable set and preserve foreign/persistent objects. | M | `/cleanup/object_id` | F41/D | F3-CONTAIN |
| R3-CTRL-005 | `contain.endpoint-guard` | Clear redirect env, use explicit context, compare daemon identity immediately before API call and deny nonlocal endpoint. | Z | `/docker/endpoint_uri` | B35/B | F3-CONTAIN |
| R3-MOUNT-006 | `contain.mount-manifest` | Compare rendered and inspect mount tuples with exact manifest; handle-qualify every parent/leaf and access mode. | Z | `/mount/source_handle_identity` | F42/B | F3-CONTAIN |
| R3-NET-002 | `contain.no-egress-graph` | Start disposable MOCK/GATE canaries and prove DNS/TCP/HTTP IPv4/IPv6/gateway/alias/link-local denial plus one internal positive control. | M | `/network/mock_egress_route` | F42/D | F3-CONTAIN |
| R3-NET-003 | `contain.real-destination-egress` | Through sole brokers exercise allowed provider operation and deny sibling host, direct IP, alternate port, redirect and DNS rebind. | M | `/egress/destination_sni` | F42/D | F5-PROVIDER |
| R3-PORT-004 | `contain.loopback-exposure` | Start n8n loopback publication; compare Windows/WSL/VPN listener matrix and positive host-loopback request. | M | `/host/port5678_owner` | B36/B | F3-CONTAIN |
| R3-PRIV-001 | `contain.privilege-envelope` | Inspect exact services: privileged false, CapDrop ALL, allowed CapAdd, no devices/socket/host PID/IPC, nonroot, no-new-privileges. | Z | `/container/capabilities` | B31/B | F3-CONTAIN |
| R3-PROFILE-008 | `contain.mode-convergence` | Render and transition every exact mode via STOPPED; compare service/network/mount/port sets and absence of stale real objects. | C | `/mode/exact_service_set` | F40/B | F3-CONTAIN |

### 3.4. R4 — Compose/PostgreSQL/n8n lifecycle (10)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R4-F01 | `lifecycle.mode-state-machine` | Execute fresh/repeated MOCK and REAL transitions through STOPPED; assert exact running/one-shot sets, health order and persistent-volume invariance. | C | `/compose/render_sha256` | F40/B | F3-CONTAIN |
| R4-F02 | `lifecycle.health-deadline` | Inject slow/failing DB, migration and n8n readiness; bounded supervisor reaches READY only after exact dependency predicates. | C | `/service/health_deadline` | F41/D | F4-DATA |
| R4-F03 | `db.role-grant-boundary` | From every DB identity test exact role attributes, procedure EXECUTE allowlist and denied table/DDL/cross-boundary operations. | C | `/postgres/role_grants` | S51/B | F4-DATA |
| R4-F04 | `n8n.backend-key-transport` | Assert PostgreSQL-only backend and exact execution mode; create/decrypt synthetic credential and workflow across restart with one-file key transport. | M | `/n8n/secret_transport` | B33/B | F6-SECRET |
| R4-F05 | `lifecycle.migration-rollback` | Upgrade isolated clone, fault after first migration, restore old image+preupgrade schema and verify credential decryptability. | M | `/migration/schema_version` | F41/D | F4-DATA |
| R4-F06 | `lifecycle.bridge-durability` | Fault bridge before/after n8n ACK and DB commit; verify contiguous offset, bounded duplicate window and one authoritative generation. | M | `/backup/writer_set` | F41/D | F4-DATA |
| R4-F07 | `n8n.owner-bootstrap-idempotency` | Run supported owner/workflow bootstrap twice on fresh and persistent instances; counts/hashes stay exact and unsupported interface blocks. | C | `/n8n/owner_interface_capability` | B31/B | F4-DATA |
| R4-F08 | `lifecycle.image-lock-render` | Parse every service/build stage, then compare loaded amd64 child/config digest; reject tags/latest/missing platform. | Z | `/oci/platform_leaf_digest` | F43/B | F2-SUPPLY |
| R4-F09 | `lifecycle.project-volume-separation` | Run local/gate/restore projects concurrently; compare project labels, names, mounts and disjoint volume identity sets. | M | `/compose/project_labels` | B36/B | F4-DATA |
| R4-F10 | `lifecycle.result-envelope` | Execute closed failure/gate case matrix and validate deterministic native/global envelope, redaction and next-safe-action. | C | `/result/envelope_schema` | S52/D | F4-DATA |

### 3.5. R5 — Telegram/DeepSeek correctness (16)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R5-F01 | `telegram.dev-bot-binding` | Under PREARM issue exactly one getMe/getWebhookInfo through broker; bind observed bot fingerprint to offline expected-dev/production-deny record. | M | `/telegram/dev_bot_fingerprint` | B35/B | F5-PROVIDER |
| R5-F02 | `telegram.webhook-owner-action` | Evaluate webhook snapshot and exact keep/delete/drop-backlog owner action; one bounded mutation only in WEBHOOK_APPLY. | C | `/telegram/webhook_action_gate` | O10/B | F5-PROVIDER |
| R5-F03 | `telegram.single-poller-fence` | Start competing bridge/project consumers and trigger sentinel; only lease/fence holder may poll or commit offset. | M | `/telegram/poller_fence` | S51/B | F5-PROVIDER |
| R5-F04 | `telegram.inbound-allowlist` | Feed typed Telegram update variants; only exact bot/chat/thread/user/content/time tuple enters authorized inbox. | M | `/telegram/allowlist_tuple` | S51/B | F5-PROVIDER |
| R5-F05 | `telegram.contiguous-ack-offset` | Fault each batch item before/after durable write and ACK; offset advances only through contiguous terminal outcomes. | M | `/bridge/request_mac` | S51/B | F5-PROVIDER |
| R5-F06 | `telegram.offset-bot-epoch` | Restart/corrupt/swap bot-state fixtures; exact bot+arm+epoch state resumes and all cross-bot/corrupt state blocks. | C | `/bridge/contiguous_offset` | F43/B | F4-DATA |
| R5-F07 | `telegram.idempotent-outbox` | Fault before/after dedup, ACK, provider acceptance and completion; one idempotency key prevents duplicate durable/send outcomes. | M | `/bridge/idempotency_key` | F43/B | F5-PROVIDER |
| R5-F08 | `telegram.immutable-reply-route` | Derive route once from authorized inbound tuple; test private/group/topic/forwarded/anonymous variants and forbid payload-selected route. | M | `/bridge/reply_route` | S51/B | F5-PROVIDER |
| R5-F09 | `telegram.ingress-mac-replay` | Validate MAC, timestamp, nonce, bot/arm/fence/tuple and schema before DB/LLM/tool effect; commit returns independent MACed ACK. | M | `/bridge/ack_mac` | S51/B | F5-PROVIDER |
| R5-F10 | `telegram.closed-http-client` | Exercise only locked client method/path/body to broker and immutable route; split response/retry never changes destination. | M | `/telegram/client_path_policy` | F42/D | F5-PROVIDER |
| R5-F11 | `telegram.send-cap-reservation` | At count 19 race ten requests; exactly one durable reservation may reach provider and retries reuse the reservation. | M | `/telegram/send_reservation_count` | B34/B | F5-PROVIDER |
| R5-F12 | `telegram.error-taxonomy` | Feed success, malformed 2xx, auth, forbidden, 409, 429, 5xx, reset and ambiguous-send outcomes; apply exact retry/disarm/offset policy. | M | `/telegram/error_class` | F41/D | F5-PROVIDER |
| R5-F13 | `deepseek.cost-reservation` | Race calls at remaining budget; exact pricing/model/request bound reservations alone may reach DeepSeek; reconcile actual cost. | M | `/deepseek/remaining_worst_case_usd` | B34/B | F5-PROVIDER |
| R5-F14 | `provider.dryrun-zero-effect` | Capture network/state for every dry-run and mode stop; dry-run reads no secret and emits no provider/state effect; stop drains real graph. | C | `/mode/provider_config_class` | F40/B | F5-PROVIDER |
| R5-F15 | `provider.payload-retention` | Inject unique typed sentinels, execute success/error/retry/crash/backup/expiry cases and scan every allowed sink for bounded/absent data. | M | `/payload/expiry_utc` | S54/D | F6-SECRET |
| R5-F16 | `telegram.owner-real-exchange` | Owner performs preview, PREARM, ACTIVE_ARM and one allowlisted real exchange under cap 20/TTL; status and disarm are exact. | M | `/telegram/owner_arm_decision` | O10/B | F5-PROVIDER |

### 3.6. R6 — secrets/privacy/incident (11)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R6-P1-001 | `secret.effective-principal-acl` | Build canary ACL inventory for secret root and Docker control plane; approved operator reads, unapproved user fails, every daemon principal is trusted. | Z | `/control/effective_principal_set` | B35/B | F6-SECRET |
| R6-P1-002 | `secret.one-file-transport` | Project one synthetic marker per consumer via exact one-file channel; scan argv/env/config/inspect/log/process metadata for absence. | M | `/secret/transport_channel` | B33/B | F6-SECRET |
| R6-P1-003 | `secret.consumer-allowlist` | For every secret slot prove one intended consumer can read and every sibling/one-shot/broker/gate/backup producer cannot. | C | `/secret/consumer_set` | B33/B | F6-SECRET |
| R6-P1-004 | `privacy.prestorage-auth` | Submit valid and forged envelopes; only MAC/arm/tuple/replay-verified data reaches authorized DB procedure and storage. | M | `/telegram/prestorage_authorized` | S51/B | F6-SECRET |
| R6-P1-005 | `privacy.n8n-payload-minimization` | Execute typed updates and inspect execution tables/binary/log/error/LLM sinks; only allowlisted transient/minimal fields survive TTL. | M | `/n8n/execution_payload_sink` | S54/D | F6-SECRET |
| R6-P1-006 | `privacy.evidence-redaction` | Pass source-allowlisted typed records through collector; nested/encoded/header/path/UI/support secret canaries reject whole artifact. | C | `/evidence/redaction_source_allowlist` | S54/D | F6-SECRET |
| R6-P1-007 | `secret.atrest-remnant-policy` | Qualify NTFS/encryption/pagefile/hiberfil/dump/sync/support classes using redacted facts; UNKNOWN/OFF blocks real secrets. | Z | `/storage/at_rest_class` | B33/B | F6-SECRET |
| R6-P1-008 | `secret.backup-no-plaintext` | Stream synthetic DB/files through encryptor, interrupt each phase and prove plaintext marker count zero in persistent/temp/log/evidence sinks. | M | `/backup/plaintext_stage_count` | S54/D | F6-SECRET |
| R6-P1-009 | `incident.revoke-rotate-close` | Execute synthetic incident state machine through containment, inventory, rotation, restore/regression and owner residual decision. | M | `/incident/revocation_state` | S54/D | F6-SECRET |
| R6-P1-010 | `secret.destination-confinement` | For each secret-bearing client prove only its broker/internal peer is reachable; direct/sibling/IP/redirect/rebind targets fail. | M | `/egress/secret_client_destination` | F42/D | F5-PROVIDER |
| R6-P2-011 | `secret.owner-entry-ceremony` | Owner-only non-echo one-file entry creates exact ACL/size/newline payload without agent value access; teardown preserves no copy claim. | C | `/secret/entry_channel` | B33/B | F6-SECRET |

### 3.7. R7 — backup/cold restore (12)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R7-F01 | `backup.recoverable-inventory` | Enumerate DB/n8n/files/bridge truth, exclusions, image/tool/key IDs and generation relation; every required class has one authority. | Z | `/backup/recoverable_inventory` | F40/B | F4-DATA |
| R7-F02 | `backup.epoch-consistency` | Quiesce writers, bind DB/files/offset/BOM to one epoch and reject mixed-generation component set. | M | `/backup/epoch_id` | F40/B | F4-DATA |
| R7-F03 | `backup.single-writer-session` | Race capture sessions and prove one lock/session writer; source resumes only after verified terminal transition. | M | `/backup/writer_session_count` | F41/D | F4-DATA |
| R7-F04 | `backup.age-recipient-binding` | Encrypt with exact public recipient, verify header/manifest key ID and authenticate with independently supplied matching private identity. | M | `/backup/age_recipient_id` | F43/B | F4-DATA |
| R7-F05 | `backup.streaming-no-plaintext` | Stream unique plaintext sentinels through pipes into ciphertext, fault every edge and scan all persistent/log/evidence sinks. | M | `/backup/plaintext_file_count` | S54/D | F6-SECRET |
| R7-F06 | `backup.publication-state-machine` | Enforce partial→sealed→verified→complete order; tamper/missing/extra/wrong-key artifacts never receive COMPLETE. | M | `/backup/publication_state` | F41/D | F4-DATA |
| R7-F07 | `restore.source-inaccessibility` | Authenticate before write in isolated project; source/live-secret mounts, networks, host ports and provider credentials are exact empty sets. | C | `/restore/source_mount_count` | F42/B | F4-DATA |
| R7-F08 | `restore.empty-target-custody` | Qualify unique target project/volume/path/labels/emptiness by identity before first extraction/DB write. | Z | `/restore/target_empty` | B35/B | F4-DATA |
| R7-F09 | `update.preupgrade-restore-first` | Create COMPLETE+RESTORE_VERIFIED preupgrade generation, migrate clone, fault and recover LKG without old-image/new-schema pairing. | M | `/update/preupgrade_generation` | F41/D | F4-DATA |
| R7-F10 | `restore.n8n-key-custody` | Independently enter matching n8n key ID into isolated restore and prove credential decryptability without exporting plaintext. | C | `/restore/n8n_key_id` | B35/B | F6-SECRET |
| R7-F11 | `backup.rpo-rto-owner-objectives` | Measure technical/custody intervals and compare immutable owner-approved RPO/RTO/retention values without revising targets. | Z | `/backup/rpo_seconds` | O10/B | F4-DATA |
| R7-F12 | `backup.restore-fault-matrix` | Trigger every declared capture/auth/publish/restore fault at exact receipt; source/last-good invariant and failed target isolation hold. | M | `/fault/trigger_receipt` | F41/D | F4-DATA |

### 3.8. R8 — B2r/O5 gates (12)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R8-P1-001 | `gate.row-manifest-exactset` | Load exact required row set, predicates and fixture hashes; reject missing/extra/duplicate/reordered semantic rows. | Z | `/gate/row_manifest_sha256` | F40/B | F7-GATE |
| R8-P1-002 | `gate.runner-identity` | Bind runner image/config/binary/entrypoint to lock and prove candidate cannot select or replace runner. | Z | `/gate/runner_sha256` | F43/B | F7-GATE |
| R8-P1-003 | `gate.candidate-aggregate` | Recompute candidate tree/artifact aggregate in trusted loader and both validators; all three digests must equal. | Z | `/candidate/aggregate_sha256` | F43/B | F7-GATE |
| R8-P1-004 | `gate.independent-validator-pair` | Execute two implementation-diverse validators in separate processes/images; compare closed result schema, not stdout labels. | C | `/validator/implementation_pair` | F40/B | F7-GATE |
| R8-P1-005 | `gate.clean-run-isolation` | Run twice from empty output/cache/tmp state; environment fingerprint exact, output hashes normalized equal, stale evidence rejected. | C | `/clean_run/environment_fingerprint` | F40/B | F7-GATE |
| R8-P1-006 | `gate.child-status-normalization` | Feed all 306 semantic status fixtures plus unknown/contradictory/stale cases into collector; compare §8 mapping exactly. | Z | `/child/status_mapping` | S52/D | F7-GATE |
| R8-P1-007 | `gate.fault-trigger-proof` | For every required negative row prove trigger receipt precedes oracle and missing trigger cannot count as tested. | C | `/fault/trigger_receipt` | F40/B | F7-GATE |
| R8-P1-008 | `gate.nic-zero` | Inspect namespace/interface/route/DNS/socket sets of every GATE process; all external NIC/routes absent and positive local fixture access remains. | C | `/gate/network_interface_set` | F42/D | F7-GATE |
| R8-P1-009 | `gate.o5-capability-boundary` | Compare each O5 row capability with A-only envelope; unsupported privileged-equivalent row returns OFFLINE_BLOCKED_CAPABILITY. | Z | `/o5/required_capability` | B31/B | F7-GATE |
| R8-P1-010 | `gate.evidence-exactset` | Trusted collector accepts exactly one EV per required row with valid hashes/predicates; missing/extra/stale/duplicate set is invalid. | C | `/evidence/exact_set_sha256` | S52/D | F7-GATE |
| R8-P2-011 | `gate.tool-closure-bom` | Resolve pinned Linux/Node/tool closure and compare BOM/hash/platform/signature; missing closure blocks capability. | Z | `/tool/bom_sha256` | B31/B | F2-SUPPLY |
| R8-P2-012 | `gate.disposable-cleanup` | Delete only gate-run exact labeled objects after evidence seal; local persistent/source objects and other runs remain byte-identical. | M | `/cleanup/object_label` | F41/D | F7-GATE |

### 3.9. R9 — candidate/Git/evidence custody (10)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R9-F01 | `custody.source-snapshot` | Capture read-only source tree/index/worktree/untracked/submodule hashes and bind candidate derivation to immutable snapshot. | Z | `/source/custody_sha256` | F43/B | F8-CUSTODY |
| R9-F02 | `custody.private-touchset` | Compute exact private worktree write allowlist; every proposed path and parent handle must be inside it before write. | Z | `/private/write_touchset_sha256` | B32/B | F8-CUSTODY |
| R9-F03 | `custody.host-path-boundary` | Open host target/parents by handle and reject repo/Vault/outside roots, reparse/hardlink/case/Unicode/ADS ambiguity. | Z | `/host/target_handle_identity` | F42/B | F8-CUSTODY |
| R9-F04 | `custody.write-toctou` | Compare parent/leaf/file identity before open, after open and after atomic replace; outside sentinel remains unchanged. | C | `/write/toctou_identity` | F42/B | F8-CUSTODY |
| R9-F05 | `custody.candidate-tree` | Recompute candidate bytes/mode/path/tree/aggregate from private output and compare review/package identities. | Z | `/candidate/commit_tree_sha256` | F43/B | F8-CUSTODY |
| R9-F06 | `custody.owner-integration-gate` | Produce exact reviewed commit/package/touchset evidence and pause at named owner integration decision. | Z | `/repo/integration_owner_decision` | O10/B | F8-CUSTODY |
| R9-F07 | `custody.write-journal-recovery` | Fault each journal/atomic-rename phase; recover to one terminal state without replaying foreign or ambiguous write. | M | `/write/journal_terminal` | F41/D | F8-CUSTODY |
| R9-F08 | `custody.delivery-identity-chain` | Prove source snapshot→candidate→review→package→owner-selected delivery identities are exact and non-aliased. | Z | `/delivery/identity_sha256` | F43/B | F8-CUSTODY |
| R9-F09 | `custody.git-byte-mode-policy` | Validate raw path bytes, case/Unicode aliases, executable bits, symlink/submodule/filter/EOL attributes and archive representation. | Z | `/git/byte_mode_policy` | F43/B | F8-CUSTODY |
| R9-F10 | `custody.prestage-secret-scan` | Scan staged/private/package bytes with typed secret canaries; any finding opens incident and prevents commit/publication. | C | `/secret/pre_stage_scan_count` | S54/D | F8-CUSTODY |

### 3.10. R10 — owner operations/handoff (11)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| R10-F01 | `owner.real-start-gate` | From clean state show real start stops before bridge/API; after exact owner arms start only approved bot/recipient within TTL/caps. | M | `/telegram/active_arm_decision` | O10/B | F5-PROVIDER |
| R10-F02 | `owner.emergency-disarm` | During polling and each health failure set host disarm marker, stop real services, prove no process/socket/arm; unavailable Engine remains unverified. | C | `/emergency/effect_stopped` | S53/D | F5-PROVIDER |
| R10-F03 | `owner.independent-restore` | With source volumes/live key inaccessible, owner supplies independent custody and completes isolated semantic restore. | M | `/restore/independent_target` | F41/D | F4-DATA |
| R10-F04 | `owner.resource-status` | Render warning/block thresholds and inspect limits/log rotation; no auto-prune/global tuning or hidden reserve crossing. | Z | `/resource/host_reserve_bytes` | B34/B | F1-HOST |
| R10-F05 | `owner.update-lkg-flow` | Detect one-field drift; backup+clone+test+owner decision precede update, and failure returns exact LKG. | C | `/runtime/lock_sha256` | B32/B | F2-SUPPLY |
| R10-F06 | `owner.runbook-clean-session` | Owner executes exact acceptance script from new standard PowerShell session/arbitrary cwd using runbook only; every checkpoint observed. | C | `/handoff/step_set` | F40/B | F1-HOST |
| R10-F07 | `owner.n8n-account-recovery` | Use supported UI/setup/2FA and documented recovery on disposable restore; no SQL/unsupported account bypass. | M | `/n8n/owner_recovery_interface` | O10/B | F4-DATA |
| R10-F08 | `owner.status-doctor` | Table-test native/global mappings, golden states and safe action; human/JSON outputs agree and doctor is read-only. | Z | `/status/child_mapping` | S52/D | F0 |
| R10-F09 | `owner.elevation-reboot-resume` | Dry-run exact elevated deltas; cancelled gate and reboot checkpoint cannot auto-resume; fresh validation required. | Z | `/reboot/resume_checkpoint` | O10/B | F1-HOST |
| R10-F10 | `owner.support-evidence-privacy` | Process synthetic UI/log/support artifacts through reject/redact/quarantine flow; no auto-upload or raw identifier leaves source. | C | `/support/secret_scan_count` | S54/D | F6-SECRET |
| R10-F11 | `owner.daily-operation` | New unelevated arbitrary-cwd session performs status/start/check/stop and post-reboot status using stable entrypoint; terminal state exact. | M | `/daily/operation_terminal` | F41/D | F1-HOST |

### 3.11. XD — cross-domain integration (15)

| Source ID | semantic_key | AT operation and oracle | ATm | NC pointer | NC result/effect | FP |
|---|---|---|---|---|---|---|
| XD-01 | `xd.integration-lock` | Canonicalize all input hashes/interfaces into one integration lock; every consumer references the same hash. | Z | `/integration/lock_sha256` | B32/B | F0 |
| XD-02 | `xd.section-alias-exactset` | Recompute section and alias key sets; every source reference resolves once and no placeholder remains. | Z | `/section_map/alias_key_set` | S52/D | F0 |
| XD-03 | `xd.canonical-byte-contract` | Apply UTF-8/no-BOM/LF/final-LF/path-byte canonicalizer twice; normalized bytes and hashes remain identical. | Z | `/canonicalizer/raw_bytes` | F43/B | F8-CUSTODY |
| XD-04 | `xd.global-result-aggregation` | Table-test semantic child classes, freshness, required scopes and precedence; exact global tuple follows without numeric max. | Z | `/child/global_rc` | S52/D | F0 |
| XD-05 | `xd.independent-scope-result` | Evaluate LAB/LOCAL/OFFLINE requirement combinations; optional blocked scope cannot improve or poison a different requested scope. | Z | `/scope/required_child_state` | B31/B | F7-GATE |
| XD-06 | `xd.canonical-topology` | Render every phase/mode twice and compare exact service/network/volume/port/mount/secret graph from §6. | Z | `/topology/service_network_edge` | F40/B | F3-CONTAIN |
| XD-07 | `xd.bridge-ingress-authority` | Valid bridge HTTP operation relays unchanged through n8n to exact SECURITY DEFINER procedure; bridge DB route/credential set remains empty. | M | `/bridge/db_route_count` | S51/B | F4-DATA |
| XD-08 | `xd.telegram-sole-egress` | One armed Telegram operation traverses bridge→egress-telegram→locked origin; every direct/alias/redirect/IP/rebind alternative is denied. | M | `/egress/destination_sni` | F42/D | F5-PROVIDER |
| XD-09 | `xd.telegram-two-arm` | Execute PREARM then ACTIVE_ARM ordered substates; allowed method counts and auto-disarm conditions equal §5. | M | `/telegram/arm_phase` | B33/B | F5-PROVIDER |
| XD-10 | `xd.secret-consumer-matrix` | Compare exact secret slot→consumer projection across every mode/one-shot; all nonmembers fail before read. | C | `/secret/consumer_set` | B33/B | F6-SECRET |
| XD-11 | `xd.privacy-retention-envelope` | Propagate typed sentinels through ingress/DB/n8n/LLM/log/backup/evidence and verify allowlist, TTL and incident boundary. | M | `/payload/expiry_utc` | S54/D | F6-SECRET |
| XD-12 | `xd.backup-verifier-separation` | Capture with public recipient, verify with isolated private identity, collect without key; exact phase/key/network sets match §7. | M | `/backup/verifier_key_visibility` | F43/B | F4-DATA |
| XD-13 | `xd.gate-process-separation` | Loader, runner, validator-a, validator-b and collector execute as distinct locked identities with no NIC/source/secret overlap. | C | `/gate/process_identity` | F42/D | F7-GATE |
| XD-14 | `xd.delivery-identity-chain` | Recompute source→candidate→review→package→delivery hashes and reviewer independence constraints. | Z | `/delivery/identity_sha256` | F43/B | F8-CUSTODY |
| XD-15 | `xd.owner-decision-effect-set` | For each owner gate prove decision binds exact hash/TTL/effect set and cannot authorize another operation. | Z | `/owner/decision_effect_set` | O10/B | F0 |

The registry above is the exact source set. A generator must reject any source ID not present once, any missing ID, duplicate `semantic_key`, absent procedure atom, empty typed payload, or a shared semantic-contract hash between different `semantic_key` values.

## 4. `EV-V3-ACL` is a real evidence alias, not a placeholder

Current `REJECTED_TEMPLATE_PLACEHOLDER` disposition is invalid because V3 §4.3/§14.3 defines concrete evidence. Replace it with:

```yaml
alias_id: EV-V3-ACL
alias_type: EV
disposition: CANONICAL_MULTI_BINDING
canonical_target_ids:
  - EV-F-R6-P1-001
  - EV-F-R3-CTRL-005
  - EV-F-R1-WIN-004
join_semantics: ALL_TARGETS_REQUIRED_SAME_RUN
typed_schema: n8nagents.evidence.acl-control-plane/v3
source_references:
  - 04_V3_RESOURCE_STORAGE_BOUNDARY.md:135-156
  - 04_V3_RESOURCE_STORAGE_BOUNDARY.md:444-445
  - 04_V3_RESOURCE_STORAGE_BOUNDARY.md:467
  - 04_V3_RESOURCE_STORAGE_BOUNDARY.md:484-490
```

Exact typed payload:

```yaml
logical_roots: [{root_id, parent_identity_hmac, leaf_identity_hmac, filesystem_class, reparse_state}]
root_acl: [{root_id, owner_principal_hmac, dacl_protected, ace_set_sha256, inherited_ace_count}]
effective_access: [{root_id, principal_hmac, read, write, delete, change_acl, take_ownership, canary_result}]
docker_control_plane: [{endpoint_class, daemon_identity_hmac, principal_hmac, rights_class}]
approved_trust: [{principal_hmac, authority_ref, role_class, expiry_or_null}]
correlation: [{principal_hmac, root_access, daemon_access, approved, residual_class}]
vhdx_vendor_acl: {observed_hash, rewritten: false}
owner_residual_gate: MG-V3-TRUST-BOUNDARY
```

Acceptance predicates are exact: operator owns protected project secret/backup/quarantine roots; only approved operator/SYSTEM or an explicitly justified service principal has required root access; broad/unknown/inherited principals are empty; every Docker control-plane principal appears in `approved_trust`; VHDX vendor ACL is observed but not rewritten; effective-access canaries agree with DACL-derived rights; all three canonical targets bind the same `run_id`, daemon identity, principal-set hash and trust-list hash. Raw SID/user/path/volume serial are forbidden. Any unknown/foreign daemon principal is `B35`, any broad root ACL is `B33`, and contradiction between ACL text and effective canary is `S52`; all occur before secret write (`Z`).

## 5. Telegram client canaries and same-bridge proof

### 5.1. Closed client RPC and provider construction

`telegram-bridge` is the only token holder and Telegram client. Its internal calls to `egress-telegram` use HTTP/1.1 over `telegram_proxy`; the broker does not terminate provider TLS or possess the token. The bridge sends an exact CONNECT-style destination request to the locked broker, then establishes TLS end-to-end to the exact Telegram origin. Application code never accepts a URL, host, port, path or redirect target from inbound update/LLM/tool data.

Allowed provider calls use `POST`, an exact method name selected by state, UTF-8 JSON, `Content-Type: application/json`, no query string, and `redirect: error/maximum_redirects=0`:

| Arm/substate | Logical provider path | Exact body key set | Count bound |
|---|---|---|---:|
| PREARM | `/bot{TOKEN}/getMe` | `{}` | 1 |
| PREARM | `/bot{TOKEN}/getWebhookInfo` | `{}` | 1 |
| ACTIVE_ARM/WEBHOOK_APPLY | `/bot{TOKEN}/getWebhookInfo` | `{}` | bounded locked count |
| ACTIVE_ARM/WEBHOOK_APPLY | `/bot{TOKEN}/deleteWebhook` | `drop_pending_updates` | 0 or 1 owner-bound |
| ACTIVE_ARM/POLL_SEND | `/bot{TOKEN}/getUpdates` | `offset,limit,timeout,allowed_updates` | lease/TTL-bound |
| ACTIVE_ARM/POLL_SEND | `/bot{TOKEN}/sendMessage` | `chat_id,text` plus `message_thread_id` iff bound tuple has topic | cap/reservation-bound |

`{TOKEN}` is inserted only inside bridge memory after route validation and is forbidden in logs/evidence. The broker sees only locked destination metadata and encrypted TLS bytes. Telegram response redirects are never followed, including same-origin 301/302/303/307/308.

### 5.2. Four independent client HTTP canaries

These are four separate NC records/subcases with separate evidence IDs; combining them into one generic destination canary is forbidden.

| Canary | Single mutation | Expected result | Required observation |
|---|---|---|---|
| `NC-HTTP-METHOD-01` | allowed `POST` → `GET`, `HEAD`, `PUT`, `CONNECT` or method with case/OWS ambiguity | `S51`, `Z` | bridge rejects before broker socket; provider request count `0` |
| `NC-HTTP-PATH-01` | exact state-bound method path → sibling method, raw absolute URL, encoded separator/dot, query, fragment or token-independent arbitrary path | `S51`, `Z` | constructed provider request count `0`; token interpolation count `0` |
| `NC-HTTP-BODY-01` | exact closed body → missing required key, unknown key, duplicate JSON key, alternate `chat_id/thread_id`, oversize/non-UTF-8/NaN or route selected from content | `S51`, `Z` | reservation/DB/provider counters `0`; immutable route hash unchanged |
| `NC-HTTP-REDIRECT-01` | locked direct `200` fixture → each 301/302/303/307/308 with same-origin, sibling-origin, literal-IP and alternate-port Location | `F42`, `M` | exactly one request reached original endpoint; follow count `0`; disarm/ambiguous outcome recorded; no second socket |

Positive control `AT-HTTP-DIRECT-01` uses the same bridge client and broker with direct nonredirect `200`, exact response schema and a synthetic route; it must be executed adjacent to every negative run. A failure of the positive control invalidates the canary (`S52`), it does not turn denial into PASS.

### 5.3. Same bridge binary, entrypoint and real-lock contamination

MOCK, PREARM and REAL use exactly the same tuple:

```text
bridge_image_amd64_digest
bridge_binary_sha256
bridge_entrypoint_path
bridge_entrypoint_argv_prefix_sha256
bridge_config_schema_sha256
bridge_http_client_library_lock_sha256
bridge_ingress_envelope_schema_sha256
```

The only allowed differences are typed config values `provider_profile=MOCK|TELEGRAM`, the destination service, arm-state projection and the mode-specific mounts/networks in §6. A mock-only bridge build, mock entrypoint, bypass client or alternate token-loading code is `B32`.

Required canaries:

| ID | Mutation | Exact denial |
|---|---|---|
| `NC-BRIDGE-BINARY-01` | MOCK image/binary/entrypoint differs from REAL locked tuple | `B32/Z`; no container start |
| `NC-MOCK-REAL-LOCK-01` | add real token file, real secret root, PREARM/ACTIVE arm, real broker endpoint or `telegram_proxy/uplink` to MOCK | `S51/Z`; secret-read/socket counters `0` |
| `NC-REAL-MOCK-LOCK-01` | REAL references mock endpoint, synthetic token, mock network or mock provider profile | `B32/Z`; provider/socket counters `0` |
| `NC-BRIDGE-DIRECT-01` | bridge receives `uplink`, default network, host alias, direct origin/IP route or proxy env | `F42/Z` when render catches it; any observed external socket is `F42/M` and run cannot continue |

Evidence `EV-BRIDGE-SAME-BINARY-v3` contains only digests, config classes, exact network/mount sets, arm-state hashes and counters; token/path/body values are forbidden.

## 6. Canonical executable topology

### 6.1. Names and global invariants

Long-running service keys are exactly:

```text
postgres n8n mock-telegram mock-llm telegram-bridge egress-telegram
deepseek-adapter egress-deepseek
```

One-shot keys are exactly:

```text
db-bootstrap db-migrate n8n-volume-init db-secret-apply bridge-key-seed
real-arm-guard backup-runner backup-verifier restore-postgres
restore-validator gate-loader gate-runner validator-a validator-b
evidence-collector
```

`backup-verifier` is mandatory and new; aliases, implicit/default services and a generic privileged helper are forbidden. Every container has `Privileged=false`, `CapDrop=[ALL]`, empty `Devices`, private PID/IPC, no Docker socket, nonroot UID/GID, read-only rootfs except exact tmpfs/writable volume, `no-new-privileges`, and no host namespace. `n8n-volume-init` is nonroot verify/seed-by-image semantics only; inability to initialize without privileged/root helper is `B31`.

All different-mode transitions are `current -> STOPPED -> target`, removing invocation-owned containers and networks without volumes. `--remove-orphans`, prune, factory reset and deletion by name/label alone are forbidden.

### 6.2. Exact network eligibility

| Network | `internal` | Exact eligible members across all phases |
|---|---:|---|
| `db` | true | `postgres`, `n8n`, and only active bounded DB one-shots `db-bootstrap`, `db-migrate`, `db-secret-apply`, `bridge-key-seed`, `real-arm-guard` |
| `mock_tg` | true | exactly `telegram-bridge`, `mock-telegram` |
| `mock_llm` | true | exactly `n8n`, `mock-llm` |
| `telegram_ingress` | true | exactly `telegram-bridge`, `n8n` |
| `telegram_proxy` | true | exactly `telegram-bridge`, `egress-telegram` |
| `llm_ingress` | true | exactly `n8n`, `deepseek-adapter` |
| `llm_proxy` | true | exactly `deepseek-adapter`, `egress-deepseek` |
| `uplink` | false | only the active `egress-telegram` and/or `egress-deepseek` |
| `backup_db` | true | exactly `postgres`, `backup-runner` during BACKUP/CAPTURE |
| `restore_db` | true | exactly active `restore-postgres`, `restore-validator`, and restored `n8n` semantic-check instance |

No service receives an implicit default network. `telegram-bridge` never receives `db`; `n8n` never receives `uplink`, `telegram_proxy` or `llm_proxy`; brokers never receive DB/application/secret/source networks or mounts. GATE and BACKUP/VERIFY/COLLECT use `network_mode:none` as specified below and create no Compose network for those phases.

### 6.3. Exact running-mode desired sets

The notation `s@n` is a service-to-network edge. One-shots exist only in the named phase row and must be absent after terminal completion.

| Mode/phase | Exact active service set | Exact network edge set | Exact host ports |
|---|---|---|---|
| `STOPPED` | `{}` | `{}` | `{}` |
| `MOCK/INIT` | `{postgres,db-bootstrap,db-migrate,n8n-volume-init,db-secret-apply,bridge-key-seed}` in dependency order, never concurrently unless declared | active DB one-shot and `postgres` on `db` only | `{}` |
| `MOCK/RUN` | `{postgres,n8n,mock-telegram,mock-llm,telegram-bridge}` | `{postgres@db,n8n@db,n8n@telegram_ingress,telegram-bridge@telegram_ingress,telegram-bridge@mock_tg,mock-telegram@mock_tg,n8n@mock_llm,mock-llm@mock_llm}` | `{n8n:127.0.0.1:5678/tcp}` |
| `PREARM_TG` | `{telegram-bridge,egress-telegram}` | `{telegram-bridge@telegram_proxy,egress-telegram@telegram_proxy,egress-telegram@uplink}` | `{}` |
| `REAL_TG/INIT` | `{postgres,db-bootstrap,db-migrate,n8n-volume-init,db-secret-apply,bridge-key-seed,real-arm-guard}` in dependency order | active DB one-shot and `postgres` on `db` only | `{}` |
| `REAL_TG/RUN` | `{postgres,n8n,telegram-bridge,egress-telegram}` | `{postgres@db,n8n@db,n8n@telegram_ingress,telegram-bridge@telegram_ingress,telegram-bridge@telegram_proxy,egress-telegram@telegram_proxy,egress-telegram@uplink}` | `{n8n:127.0.0.1:5678/tcp}` |
| `REAL_TG_DEEPSEEK/RUN` | `{postgres,n8n,telegram-bridge,egress-telegram,deepseek-adapter,egress-deepseek}` | REAL_TG/RUN edges plus `{n8n@llm_ingress,deepseek-adapter@llm_ingress,deepseek-adapter@llm_proxy,egress-deepseek@llm_proxy,egress-deepseek@uplink}` | `{n8n:127.0.0.1:5678/tcp}` |

MOCK is therefore internally coherent: the **same** `telegram-bridge` polls `mock-telegram` on `mock_tg`, relays to n8n on `telegram_ingress`, and receives synthetic ACKs. It has no `telegram_proxy`, `uplink`, real broker, real token, PREARM/ACTIVE arm or real provider lock. `mock-telegram` has no other network. MOCK secret projection may contain only a public synthetic marker generated inside the fixture; `LAB_SECRET_ROOT` is not mounted.

### 6.4. Exact one-shot phase topology

| Operation/phase | Exact active set | Networks | Forbidden co-members |
|---|---|---|---|
| `BACKUP/CAPTURE` | `{postgres,backup-runner}` | both on `backup_db` | `n8n`, bridge, mocks, brokers, verifier, restore, gate |
| `BACKUP/VERIFY` | `{backup-verifier}` | `network_mode:none` | all other containers |
| `BACKUP/COLLECT` | `{evidence-collector}` | `network_mode:none` | all other containers |
| `RESTORE/PREFLIGHT_DB` | `{restore-postgres}` | `restore_db` only | source postgres/n8n, bridge, mocks, brokers, gate |
| `RESTORE/VALIDATE` | `{restore-postgres,restore-validator,n8n}` with restored n8n `restart:no` | `restore_db` only | source services, provider credentials, mocks, bridge, brokers |
| `RESTORE/COLLECT` | `{evidence-collector}` | `network_mode:none` | restore key, restored services |
| `GATE/LOAD` | `{gate-loader}` | `network_mode:none` | runner/validators/collector |
| `GATE/RUN` | `{gate-runner}` | `network_mode:none` | loader/validators/collector |
| `GATE/VALIDATE-A` | `{validator-a}` | `network_mode:none` | all other gate identities |
| `GATE/VALIDATE-B` | `{validator-b}` | `network_mode:none` | all other gate identities |
| `GATE/COLLECT` | `{evidence-collector}` | `network_mode:none` | candidate writer, loader, runner, validators |

## 7. `backup-verifier` and key isolation

### 7.1. Exact mount/secret matrix

| Service | Allowed read-only inputs | Allowed writable target | Key material | Network |
|---|---|---|---|---|
| `backup-runner` | selected source n8n/file volumes RO; public age recipient; exact capture manifest; one-file DB backup credential | ciphertext staging generation only; bounded tmpfs | public recipient and capture-only DB credential; **never private age identity or n8n key** | `backup_db` |
| `backup-verifier` | sealed ciphertext generation RO; encrypted manifest RO; exact verifier binary/spec RO; private age identity one-file RO | bounded tmpfs plaintext-to-hash/null only; typed verifier result in dedicated output | private age identity only; **no DB credential, n8n key, provider key/token or live secret root** | `none` |
| `evidence-collector` | typed verifier result RO; public manifest/hash inventory RO | dedicated evidence output only | **none** | `none` |
| `restore-postgres` | authenticated restore component stream; restore-specific DB credential | new empty restore volumes only | restore DB credential only; no age identity after authentication handoff | `restore_db` |
| `restore-validator` | restored volumes RO where possible; typed manifest; independently supplied n8n key one-file only for decryptability check | typed validation result and bounded tmpfs | n8n key only; no age identity/provider credentials/live secret root | `restore_db` |

Host/Vault/repo roots, Docker socket, source DB volume in verifier/restore, backup destination in restored n8n, and any unrestricted directory bind are forbidden. Private identity is mounted only after `backup-runner` has exited and `backup_db` has been removed; it is unmounted before collector start. Process teardown is asserted, but no physical secure-erase claim is made.

### 7.2. State machine and publication authority

```text
CAPTURE_OPEN
  -> CIPHERTEXT_SEALED_PENDING_VERIFIER
  -> VERIFIED_PENDING_COLLECTOR
  -> COMPLETE

any capture failure      -> QUARANTINED_INCOMPLETE
any verifier/auth failure -> QUARANTINED_AUTH_FAILED
any collector/schema failure -> VERIFIED_NOT_COMPLETE
```

Only `backup-verifier` may create the signed/hashed `VERIFIED_PENDING_COLLECTOR` result; only `evidence-collector` may publish `COMPLETE`, and it does so only after verifying the verifier identity, closed result schema, ciphertext/manifest hashes, component exact set and zero forbidden counters. Neither producer nor owner text can self-assert COMPLETE. A prior verifier result, changed ciphertext, missing component, mixed run/generation or absent current authentication produces `F43/Z` before COMPLETE.

### 7.3. Key-isolation canaries

| ID | Single mutation | Outcome |
|---|---|---|
| `NC-BACKUP-KEY-01` | private age identity visible to `backup-runner` | `S51/Z`; capture does not start |
| `NC-BACKUP-KEY-02` | private age identity visible to collector, restore validator or any long-running service | `S51/Z`; no consuming process starts |
| `NC-BACKUP-KEY-03` | public recipient missing/changed after capture lock | `F43/Z`; no COMPLETE |
| `NC-BACKUP-KEY-04` | verifier has `backup_db`, `db`, default network or any NIC | `F42/Z`; verifier does not start |
| `NC-BACKUP-KEY-05` | collector receives ciphertext plaintext stream/private identity or verifier output from another generation | `S52/Z`; no COMPLETE |
| `NC-BACKUP-KEY-06` | backup producer attempts to write verifier result/COMPLETE | `S51/Z`; publication counter `0` |

Positive controls prove capture succeeds with the public recipient alone, verification succeeds with network none and the correct independently supplied identity, and collection succeeds after the identity mount is absent.

## 8. Semantic rebuild of all 306 child-status mappings

### 8.1. Replacement schema

The existing `default_mutation_started` field is removed. Every one of the exact 306 keys must have a reviewed record:

```yaml
native_status_key: <V01..V10:native_status>
domain: <V01..V10>
native_status: <exact>
source_semantics:
  references: [{source_relpath, line_start, line_end}]
  excerpt_sha256: <hash of exact UTF-8 LF source bytes>
  assertion: <closed semantic assertion, not copied status name>
semantic_class: PASS_SCOPED | OWNER_READY | NOT_RUN |
  BLOCK_UNKNOWN | BLOCK_CAPABILITY | BLOCK_DRIFT | BLOCK_POLICY |
  BLOCK_RESOURCE | BLOCK_IDENTITY | BLOCK_DEPENDENCY | BLOCK_MANUAL |
  FAIL_VALIDATION | FAIL_OPERATION | FAIL_CONTAINMENT | FAIL_INTEGRITY |
  STOP_SCOPE | STOP_SECURITY | STOP_INVALID | STOP_EMERGENCY | INCIDENT_OPEN
global_tuple: {decision, status, rc}
success_scope: <exact child operation or null>
effect_semantics:
  operation_phase: PREFLIGHT | READ_ONLY | PRE_FIRST_EFFECT | POST_FIRST_EFFECT | MULTIPHASE
  first_effect_definition: <typed counter name and boundary>
  mutation_policy: CONST_FALSE | CONST_TRUE | COUNTER_REQUIRED
  allowed_counter_range: <exact>
  missing_counter_result: S52
owner_gate_semantics: {gate_id, artifact_ready, decision_missing} | null
incident_semantics: {incident_open, closure_scope, residual_gate} | null
source_refs: <existing refs retained>
```

### 8.2. Semantic class → global tuple

| semantic_class | Exact global tuple |
|---|---|
| `PASS_SCOPED` | `PASS/G_PASS_EXACT_REQUESTED_SCOPES/0` |
| `OWNER_READY` | `READY_OWNER_GATE/G_READY_OWNER_GATE/10` |
| `NOT_RUN` | `NOT_RUN/G_NOT_RUN/20` |
| `BLOCK_UNKNOWN` | `BLOCKED/G_BLOCKED_UNKNOWN/30` |
| `BLOCK_CAPABILITY` | `BLOCKED/G_BLOCKED_CAPABILITY/31` |
| `BLOCK_DRIFT` | `BLOCKED/G_BLOCKED_CONTRACT_DRIFT/32` |
| `BLOCK_POLICY` | `BLOCKED/G_BLOCKED_POLICY/33` |
| `BLOCK_RESOURCE` | `BLOCKED/G_BLOCKED_RESOURCE/34` |
| `BLOCK_IDENTITY` | `BLOCKED/G_BLOCKED_IDENTITY/35` |
| `BLOCK_DEPENDENCY` | `BLOCKED/G_BLOCKED_DEPENDENCY/36` |
| `BLOCK_MANUAL` | `BLOCKED/G_BLOCKED_MANUAL/37` |
| `FAIL_VALIDATION` | `FAIL/G_FAIL_VALIDATION/40` |
| `FAIL_OPERATION` | `FAIL/G_FAIL_OPERATION/41` |
| `FAIL_CONTAINMENT` | `FAIL/G_FAIL_CONTAINMENT/42` |
| `FAIL_INTEGRITY` | `FAIL/G_FAIL_INTEGRITY/43` |
| `STOP_SCOPE` | `STOP/G_STOP_SCOPE_EXPANSION/50` |
| `STOP_SECURITY` | `STOP/G_STOP_SECURITY/51` |
| `STOP_INVALID` | `STOP/G_STOP_RESULT_INVALID/52` |
| `STOP_EMERGENCY` | `STOP/G_EMERGENCY_UNVERIFIED/53` |
| `INCIDENT_OPEN` | `STOP/G_INCIDENT_OPEN/54` |

`BLOCK_MANUAL` and `OWNER_READY` are intentionally distinct. The former means a prerequisite/decision is absent or invalid and the operation is blocked; the latter means a complete exact artifact is staged and the only permitted next effect is one named owner decision.

### 8.3. Mandatory build algorithm

```text
1. Read the ten domain source files by exact hash; extract native-status keys and source ranges.
2. Sort unique keys by UTF-8 byte order. Require count=306 and
   sha256(join(keys,"\n")+"\n") =
   afd05d828c22c9132b7e00612781c776ddc922ea089c2a61cf14f1921e589c06.
3. Join by exact native_status_key to a reviewer-authored semantic annotation table.
   Regex, prefix/suffix, numeric native RC and current global tuple are forbidden inputs.
4. Reject absent/duplicate annotation, empty assertion, status-name-only assertion,
   missing source excerpt hash, or unresolved contradiction.
5. Map semantic_class through §8.2. No other tuple is valid.
6. Apply the exact override table §8.5; disagreement is a build failure.
7. Evaluate mutation policy from effect semantics §8.4, never from domain or status class.
8. Emit 306 records, then independently reparse and compare key/source/global/effect exact sets.
9. Unknown runtime child status, missing counter, stale child, impossible tuple or zero RC with
   failed predicate normalizes to STOP/G_STOP_RESULT_INVALID/52; it is not added as key 307.
```

The current mapping may supply the exact key set and source references only. Its current tuple and `default_mutation_started` values are untrusted and cannot seed semantic annotations.

### 8.4. Phase-aware `mutation_started`

`mutation_started` reports whether the **requested governed operation** crossed its first-effect boundary, not whether the checker wrote evidence, allocated memory, opened a read-only handle or observed an already-existing condition.

| Policy | Required rule |
|---|---|
| `CONST_FALSE` | Status can be emitted only in `PREFLIGHT/READ_ONLY/PRE_FIRST_EFFECT`; named governed effect counter is exactly unchanged and actual boolean is false. |
| `CONST_TRUE` | Native semantics prove first effect necessarily occurred (for example restore target write began); counter increased and actual boolean is true. |
| `COUNTER_REQUIRED` | A multiphase status may arise before or after effect. Child must emit typed before/after counter and phase; actual boolean is comparison result. Missing/ambiguous counter is `S52`. |

Read-only commands and results (`status`, `doctor`, `dry-run`, inventory, hash/ACL/topology render, policy/RPO measurement, source replay, authentication-to-null when invoked standalone) are always `CONST_FALSE`. Evidence sealing is not the governed effect. An already-existing leak/foreign socket/incident may cause STOP/FAIL while the current read-only detection operation remains `mutation_started=false`; the incident/containment evidence separately records the pre-existing effect. Conversely, a canary that deliberately crosses the boundary is `CONST_TRUE` even if rollback succeeds.

### 8.5. Exact mandatory overrides

| native_status_key | semantic_class / tuple | mutation policy | Exact rationale/scope |
|---|---|---|---|
| `V04:V4_STOP_UNVERIFIED` | `STOP_EMERGENCY` = `STOP/G_EMERGENCY_UNVERIFIED/53` | `CONST_TRUE` | Host disarm record was written, but process/egress stop was not proved; never PASS. |
| `V07:INCIDENT_CLOSED` | `PASS_SCOPED` = `PASS/G_PASS_EXACT_REQUESTED_SCOPES/0` | `CONST_TRUE` | PASS only for requested incident-close operation after complete lifecycle and owner residual decision; it cannot clear any other blocked scope or historical incident evidence. |
| `V08:RESTORE_FAILED_ISOLATED` | `FAIL_OPERATION` = `FAIL/G_FAIL_OPERATION/41` | `CONST_TRUE` | V8 says failed/partial DB target exists and is isolated; target write began, no retry in place. |
| `V08:V8_FAIL_BACKUP` | `FAIL_OPERATION` = `FAIL/G_FAIL_OPERATION/41` | `COUNTER_REQUIRED` | Capture/publish failed; pre-capture problems must use `V8_BLOCKED_*`; counter distinguishes failure before/after ciphertext effect. |
| `V08:V8_FAIL_AUTH` | `FAIL_INTEGRITY` = `FAIL/G_FAIL_INTEGRITY/43` | `COUNTER_REQUIRED` | Wrong key/tamper/truncation authentication failure; standalone verify is read-only, full backup may already have captured ciphertext. |
| `V08:V8_FAIL_PLAINTEXT` | `INCIDENT_OPEN` = `STOP/G_INCIDENT_OPEN/54` | `COUNTER_REQUIRED` | Prohibited plaintext occurrence opens incident; current operation counter is reported separately from detected existing occurrence. |
| `V08:V8_FAIL_RESTORE` | `FAIL_OPERATION` = `FAIL/G_FAIL_OPERATION/41` | `CONST_TRUE` | Native definition explicitly says target write began and semantic restore failed. |
| `V08:V8_FAIL_CONTAINMENT` | `FAIL_CONTAINMENT` = `FAIL/G_FAIL_CONTAINMENT/42` | `COUNTER_REQUIRED` | Observed source/live-root/egress/port/trigger/path violation; preflight-only missing proof must be a `V8_BLOCKED_*` status. |
| `V08:V8_FAIL_RPO` | `FAIL_VALIDATION` = `FAIL/G_FAIL_VALIDATION/40` | `CONST_FALSE` | Measurement shows recoverable point exceeds frozen target; measuring it is read-only. |
| `V08:V8_FAIL_RTO` | `FAIL_VALIDATION` = `FAIL/G_FAIL_VALIDATION/40` | `CONST_TRUE` | Measured technical restore exceeded target after restore operation crossed first effect. |

The following current contradictory mappings are also replaced exactly:

| Native key set | Required semantic handling |
|---|---|
| `V01:BLOCKED_MANUAL`, `V01:BLOCKED_PENDING_REBOOT`, `V01:BLOCKED_POST_REBOOT_DRIFT`, `V01:REBOOT_REQUIRED_STOPPED`, `V02:BLOCKED-MANUAL`, `V03:V3_BLOCKED_MANUAL`, `V05:BLOCKED_MANUAL`, `V10:BLOCKED_MANUAL`, `V10:REBOOT_REQUIRED_STOPPED` | `BLOCK_MANUAL` = `BLOCKED/G_BLOCKED_MANUAL/37`; normally `CONST_FALSE`. |
| `V01:READY_FOR_MANUAL_GATE`, `V04:V4_READY_FOR_MANUAL_GATE`, `V05:READY_FOR_MANUAL_GATE` | `OWNER_READY` = `READY_OWNER_GATE/G_READY_OWNER_GATE/10`; `CONST_FALSE`. |
| `V01:MG-V1-POST-REBOOT`, `V01:MG-V1-REBOOT`, `V10:MG-V1-POST-REBOOT`, `V10:MG-V1-REBOOT` | These are gate IDs, not free-standing result statuses. If artifact-ready state is explicitly emitted, `OWNER_READY/10`; otherwise reject mapping as `S52`. |
| `V02:UPDATE_PENDING`, `V08:UPDATE_PENDING` | `OWNER_READY/10` only after exact staged update/preupgrade evidence exists; otherwise `BLOCK_MANUAL/37`. Therefore `COUNTER_REQUIRED` is forbidden; child must emit distinct staged/not-staged native state or mapping build stops. |
| `V09:MANUAL_PASS` | Never PASS. Treat as `OWNER_READY/10` only when it means pending owner integration of a complete reviewed artifact; otherwise remove/rename source status before freeze. |

### 8.6. Semantic mapping acceptance

The rebuild passes only if:

- key cardinality is 306, key-set hash is exact, and every key has one source excerpt hash and nonempty semantic assertion;
- every tuple is a row of §8.2 and all `READY_OWNER_GATE` records use RC 10/status `G_READY_OWNER_GATE`;
- every `PASS_SCOPED` names the exact successful requested scope; no PASS is inferred from `COMPLETE`, `CLOSED`, `HEALTHY` or numeric zero alone;
- all read-only statuses have `CONST_FALSE`; all `CONST_TRUE` have an unavoidable first-effect statement; all multiphase statuses use `COUNTER_REQUIRED`;
- mutation canaries flip each of decision/status/RC/effect policy/source excerpt and both independent checkers reject them;
- the overrides above match byte-for-byte after canonical serialization.

## 9. Rendered-topology exact-set tests

### 9.1. Canonical normalized graph

For each §6 row, render Compose with exact lock and mode/phase. Normalize into this closed object; sorting is UTF-8 byte order and arrays are sets unless `ordered=true`:

```yaml
schema: n8nagents.rendered-topology/v3
mode: <exact>
phase: <exact>
project_name: <n8nagents-local | n8nagents-k4r-${run_id} | restore exact id>
services:
  <service>:
    image_digest: <sha256>
    platform: linux/amd64
    command_argv_sha256: <sha256>
    entrypoint_argv_sha256: <sha256>
    networks: [<exact>]
    mounts: [{type,source_logical_id,target,read_only,propagation}]
    secrets: [{slot_id,target,consumer}]
    ports: [{host_ip,host_port,container_port,protocol}]
    privileged: false
    cap_drop: [ALL]
    cap_add: [<exact per-service set, normally empty>]
    devices: []
    pid: private
    ipc: private
    user: <nonzero uid:gid>
    read_only_rootfs: true
    restart: "no" | <exact MOCK local policy only>
    security_opt: [no-new-privileges:true]
networks:
  <network>: {internal, members:[<exact>]}
volumes: [{key,external:false,project_label,purpose}]
implicit_default_network: false
```

Exact comparison, not subset comparison:

```text
actual.services.keys                 == expected.services
actual.networks.keys                 == expected.networks
set(service,network)                 == expected.edges
set(service,mount tuple)             == expected.mounts
set(service,secret slot)             == expected.secrets
set(service,port tuple)              == expected.ports
set(service,image,entrypoint,command)== expected.runtime_identities
set(volume key/label/purpose)         == expected.volumes
unexpected = actual - expected       == empty
missing    = expected - actual       == empty
```

Compose-generated default networks, aliases not in the manifest, `extra_hosts`, `host.docker.internal`, proxy variables, DNS overrides, links, network namespace sharing, bind propagation other than exact locked value and unnamed/anonymous volumes are unexpected elements, even if not currently used.

### 9.2. Required test matrix

| Test | Procedure | Pass oracle |
|---|---|---|
| `RT-01-RENDER-DETERMINISM` | Render every mode/phase twice from clean env and normalized path-independent inputs. | normalized bytes/hash equal for each pair |
| `RT-02-SERVICE-EXACTSET` | Compare service keys to §6.3/§6.4 row. | no missing/extra/alias service |
| `RT-03-NETWORK-EXACTSET` | Compare network keys, `internal` flags and bipartite edges. | exact set; no default network |
| `RT-04-MOCK-BRIDGE` | Render MOCK/RUN and inspect graph. | bridge is on `mock_tg`+`telegram_ingress`; no real token/broker/proxy/uplink/arm |
| `RT-05-SAME-BRIDGE` | Compare bridge identity tuple across MOCK/PREARM/REAL. | image, binary, entrypoint, schema/client hashes equal |
| `RT-06-PORT-EXACTSET` | Render/inspect ports, then Windows listener inventory. | only n8n `127.0.0.1:5678/tcp` in RUN rows; no wildcard/IPv6/LAN/WSL/VPN/portproxy |
| `RT-07-MOUNT-EXACTSET` | Compare mount manifest and handle-qualified host paths. | exact targets/modes; no workspace/repo/Vault/broad secret root/socket |
| `RT-08-SECRET-EXACTSET` | Compare per-phase secret slots/consumers. | MOCK has no real secret; broker/backup producer/verifier/collector isolation exact |
| `RT-09-PRIVILEGE-EXACTSET` | Compare rendered security fields and runtime inspect. | privileged/devices/host PID/IPC/socket empty; CapDrop ALL/nonroot/no-new-privileges |
| `RT-10-MODE-DRAIN` | Run every directed transition through STOPPED and inspect after drain/start. | no stale old-mode container/network/process/socket; volumes unchanged |
| `RT-11-EGRESS-CANARIES` | Run DNS, IPv4/IPv6, gateway, host alias, link-local, direct IP, redirect and rebind canaries plus internal/provider positive controls. | only exact internal or active broker path works |
| `RT-12-HTTP-CANARIES` | Run §5.2 method/path/body/redirect canaries separately. | exact tuple/counters and no redirect follow |
| `RT-13-BACKUP-PHASES` | Render CAPTURE, VERIFY, COLLECT independently and compare process/network/mount/key sets. | producer/verifier/collector never overlap; verifier/collector NIC empty |
| `RT-14-RESTORE-GATE` | Render every RESTORE/GATE phase. | source/live secrets/provider paths absent; exact process separation |
| `RT-15-RUNTIME-CONVERGENCE` | After start compare `docker ps/inspect/network inspect/volume inspect` normalized graph to rendered graph. | rendered expected = observed exact set |

### 9.3. Mutation canaries for the checker itself

Independent checker A and checker B must each reject at least these one-field mutations with nonzero checker RC and the named mismatch class:

```text
add service; remove service; add default network; add/remove edge; add host alias;
add wildcard port; change image digest; change bridge entrypoint; add real token to MOCK;
add bridge@db; add n8n@uplink; add broker@db; add verifier NIC;
expose private key to producer/collector; add Docker socket; set privileged;
remove CapDrop ALL; add device; set host PID/IPC; add broad bind; add anonymous volume;
retain stale real container after MOCK transition; merge validator identities.
```

The checker must compare structured sets, not search rendered YAML text. Every mismatch evidence contains only logical service/network/mount/slot IDs and hashes.

## 10. Mechanical generation and validation gates

### 10.1. Catalog generator pseudocode

```text
registry = parse_markdown_table_sections(3.1..3.11)
assert unique(registry.SourceID) and count == 129
assert finding IDs == exact 114 keys from 07_FINDING_DISPOSITIONS_V2
assert XD IDs == {XD-01..XD-15}

for row in registry:
    at = expand_typed_acceptance(row, source_binding[row.SourceID])
    nc = expand_single_field_negative(row, at.fixture_hash)
    ev = expand_typed_evidence(row, at, nc)
    assert at.procedure.ordered_steps not in GENERIC_PROCEDURES
    assert at.fixture.fixture_type == row.semantic_key + ".positive/v1"
    assert nc.mutation.count == 1 and nc.json_pointer == row.NC_pointer
    assert tuple(nc.outcome) == OUTCOME[row.NC_result]
    assert effect(nc) == row.NC_effect
    assert ev.schema == "n8nagents.evidence." + row.semantic_key + "/v3"
    assert ev.typed_payload is closed and nonempty
    hash canonical JSON with UTF-8/no-BOM/LF/final-LF

assert exact IDs/counts: AT=129, NC=129, EV=129
assert every disposition links exactly one of each
assert alias EV-V3-ACL resolves to exact three targets and same-run join
```

The actual generator must inline typed fixtures/procedures/payload schemas into the catalogs. It may not leave `semantic_key` as an unimplemented promise. A compile-time schema registry may reduce duplication only when field sets and oracles are truly identical; different targets must still have distinct source bindings, case sets and semantic hashes.

### 10.2. Explicit acceptance / Definition of Done

Correction R2/A is acceptable for integration only when all conditions are true:

1. **129 semantics:** exact 114 finding and 15 XD source sets; every AT has typed fixture, ordered executable procedure, positive control, exact outcome/scope and effect rule; every NC has one typed mutation, injection phase, exact tuple, counters and forbidden profile; every EV has a closed semantic payload/predicates.
2. **No placeholders:** zero occurrences in generated catalogs of generic fixture/procedure/evidence forms identified in §0; no empty or prose-only oracle; no duplicate semantic-contract hash across unrelated keys.
3. **ACL closure:** `EV-V3-ACL` is the exact three-target same-run alias in §4 and its effective-principal/VHDX/control-plane predicates are implemented and independently mutation-tested.
4. **HTTP/bridge closure:** four separate HTTP canaries plus positive control pass; same bridge image/binary/entrypoint/config/client tuple is proved in MOCK and REAL; real-lock contamination canaries fail before secret/socket effect.
5. **Topology closure:** canonical service/one-shot/network/mode/phase membership equals §6, including bridge in MOCK `mock_tg`, no MOCK real uplink/secret, no bridge DB route, and no stale mode objects.
6. **Backup closure:** `backup-verifier` exists as a separate one-shot; capture/verify/collect process, network, mount and key sets are disjoint; only collector can publish COMPLETE after current verifier result.
7. **Status closure:** exact 306 key-set hash; reviewer-authored semantic annotation per key; no name/regex/RC heuristic; §8.5 overrides exact; all read-only effects false and all multiphase effects counter-derived.
8. **Rendered exact sets:** `RT-01..RT-15` and checker mutation matrix are present in the generated acceptance catalog and both independent implementations agree.
9. **Custody:** all replacement artifacts are UTF-8 without BOM, LF only, exactly one final LF; manifest hashes/counts are recomputed; independent reviewers receive immutable inputs and do not share authorship.
10. **Claims:** result remains `DESIGN_READY_FOR_INDEPENDENT_REVIEW / RUNTIME_NOT_RUN`; no host/Docker/provider/Telegram/DeepSeek/backup/restore success is claimed until separately authorized execution produces current evidence.

Any failed condition is `CHANGES_REQUIRED`. A mechanical 129/306 count alone is insufficient for GO.

## 11. Coverage index

| Audit requirement | Replacement sections | Required proof |
|---|---|---|
| Typed AT/NC/EV for all 129; priority 114 findings | §2, §3, §10 | exact 129 registry/generator/schema checks |
| `EV-V3-ACL` | §4 | three-target alias, ACL/control-plane typed evidence |
| HTTP method/path/body/redirect | §5.1–§5.2 | four independent NC + positive control |
| Same bridge binary/entrypoint and real-lock contamination | §5.3, §6.3 | identity tuple and four bridge canaries |
| Coherent MOCK with bridge in `mock_tg`, no real route/secret | §6.2–§6.3 | exact graph and `RT-04/05/08/11` |
| Canonical services/one-shots and backup verifier | §6.1, §6.4, §7 | exact keys, phase graph, key matrix/state machine |
| Semantic 306 status mappings | §8 | exact-set algorithm, class map, annotations, overrides |
| `V4_STOP_UNVERIFIED`, `INCIDENT_CLOSED`, V08 FAIL_* | §8.5 | byte-exact override validation |
| Phase-aware/read-only `mutation_started` | §2.2, §8.4 | counter-bound policy and missing-counter canary |
| Rendered topology exact sets | §9 | `RT-01..RT-15` plus checker mutation matrix |

This document deliberately contains no freeze instruction, commit instruction or runtime authority.
