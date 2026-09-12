---
id: "n8nagents-plan-v2-v6-telegram-correctness-security"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V6 Telegram/auth/security architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[02_V1_WINDOWS_CONTROL_PLANE]]"
  - "[[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]"
  - "[[04_V3_RESOURCE_STORAGE_BOUNDARY]]"
  - "[[05_V4_ISOLATION_NETWORK_EXPOSURE]]"
  - "[[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]"
доказательства:
  - "00_FINDINGS_BASELINE.json"
  - "01_BASELINE_AUDIT.json"
теги: ["n8nagents", "plan-v2", "telegram", "authorization", "idempotency", "security", "deepseek", "design-only"]
---

# V6 — Telegram correctness, authorization и security

## 0. Статус, область и запрет на runtime-утверждения

Это implementation-ready design-секция будущего полного plan v2. Она не разрешает network probe, Telegram/DeepSeek API, ввод или чтение секретов, Docker/Windows/VPS mutation, изменение project repo, создание бота, изменение webhook, запуск контейнеров или расходование бюджета. Все внешние identities, endpoints, цены, secrets, recipient tuples, offsets и runtime capabilities остаются `UNKNOWN` до соответствующего owner gate и исполнения.

V6 владеет:

- доказуемой отдельной dev/test bot identity и production deny;
- arming/disarming и webhook-to-polling transaction;
- single-poller lease, Update classification, authorization и pre-storage drop;
- authenticated bridge envelope, durable ACK, offset, inbox, idempotency, reply route, outbox и send ledger;
- единым Telegram outbound path и глобальным cap `20`;
- Telegram error/retry/conflict semantics;
- отдельным DeepSeek cost/request authorization;
- Telegram/LLM PII policy, owner ceremony и emergency stop.

V6 не владеет official artifact acquisition, Windows/Docker endpoint, физическими ACL/at-rest controls, Compose/SQL delivery, network enforcement, backup encryption, dirty-worktree integration или production deployment. Эти области — fail-closed cross-dependencies.

## 1. Принятые design-решения и реестр contracts

### 1.1. Непереговорные решения

1. Real-dev использует только отдельного owner-approved dev/test bot. Token или `bot_id`, не совпавший с заранее утверждённой dev identity, не получает ни одного state-changing Telegram API call. Известные production identities дополнительно находятся в denylist.
2. Никакой Telegram API call, включая `getMe` и `getWebhookInfo`, не разрешён без актуального arm record соответствующей фазы. «Read-only probe до arm» запрещён.
3. n8n не получает Telegram token, Telegram Credential, прямой Bot API route или активный Telegram Trigger. Все реальные ответы идут через один `telegram-bridge`; это устраняет обход cap через n8n node или fallback adapter.
4. `telegram-bridge` — единственный secret-bearing Telegram component. Внешний HTTPS доступен ему только через V4-controlled `egress-telegram`; broker не получает token и не расшифровывает TLS. n8n и PostgreSQL external route не имеют. Alias `telegram-egress-proxy` не является допустимым service key.
5. `telegram-bridge` не получает PostgreSQL network path/credential. Все durable control operations проходят через authenticated internal n8n/app ingress на V4 `telegram_ingress`; ingress вызывает exact PostgreSQL procedures ролью `automation_runtime`. n8n не знает envelope HMAC key и не может создать валидный control message.
6. `allowed_updates` не считается authorization. Bridge классифицирует Update и проверяет точный conjunctive tuple в памяти до передачи payload в n8n/application PostgreSQL.
7. Unauthorized/unsupported Update получает terminal drop: разрешены только минимальный durable control-state для contiguous offset и keyed aggregate counter. Raw payload, text, username и raw IDs не попадают в n8n, application DB, LLM, tools, logs или evidence.
8. Offset означает следующий Telegram offset после максимального непрерывного префикса наблюдённых Updates, достигших durable terminal state. «Непрерывный» относится к порядку полученного batch, а не требует арифметически соседних `update_id`.
9. External exactly-once для `sendMessage` не обещается. Timeout после возможной передачи запроса — `AMBIGUOUS_CONSUMED`, расходует cap и никогда не ретраится вслепую.
10. Telegram cap равен ровно `20` реальным outbound send attempts на один owner authorization scope. Каждый chunk, retry и ambiguous attempt считается отдельно; restart/rearm cap не сбрасывает.
11. DeepSeek authorization и ledger отделены от Telegram cap. Telegram arm сам по себе не разрешает LLM network/cost.
12. `mock` может менять только изолированное mock state, но имеет zero external API/egress и не меняет real webhook/offset/cap/cost. `dry-run` дополнительно имеет zero local mutation и не читает secrets.

### 1.2. Contracts

| Contract | Обязательство |
|---|---|
| `V6-C01-BOT-IDENTITY` | Offline owner binding exact dev bot; expected identity match; production deny; keyed evidence only. |
| `V6-C02-ARM` | Phase-specific TTL arm bound to plan/config/runtime/bot/tuple/caps/boot/endpoint; zero API without arm. |
| `V6-C03-WEBHOOK` | Snapshot, explicit backlog policy, exact `deleteWebhook` option, postcondition and no implicit restore. |
| `V6-C04-POLLER-LEASE` | Cross-project PostgreSQL lease with monotonic fencing; stale holder cannot poll or commit. |
| `V6-C05-UPDATE-CLASSIFIER` | Strict bounded Update/Message schema and terminal unsupported states before persistence. |
| `V6-C06-PRESTORAGE-AUTHZ` | Exact conjunctive tuple; unauthorized terminal drop before n8n/application DB/LLM/tools. |
| `V6-C07-BRIDGE-ENVELOPE` | Versioned HMAC-authenticated bounded envelope and durable anti-replay verifier. |
| `V6-C08-OFFSET-CAS` | Durable highest-contiguous prefix and monotonic CAS, bot/auth/fence namespaced. |
| `V6-C09-INBOX-ACK` | Structured authenticated ACK only after durable authorized inbox transaction. |
| `V6-C10-IDEMPOTENCY-OUTBOX` | Claim leases, idempotent completion/enqueue and transactional outbox with bounded crash semantics. |
| `V6-C11-REPLY-ROUTE` | Immutable server-side route derived only from authorized tuple; workflow/LLM cannot choose destination. |
| `V6-C12-TELEGRAM-CAP20` | One persistent atomic reserve-before-send ledger across every real outbound path/attempt. |
| `V6-C13-TELEGRAM-ERRORS` | Exact HTTP/Bot API classification, `retry_after`, conflict disarm and no blind retry. |
| `V6-C14-DEEPSEEK-BUDGET` | Separate exact model/pricing/currency/token/request/cost authorization and atomic ledger. |
| `V6-C15-MODE-ZERO-EFFECT` | Dry-run zero mutation/API/secret read; mock zero external state; fail-closed mode convergence. |
| `V6-C16-PII-RETENTION` | Field-level data map, synthetic default, keyed pseudonyms, bounded stores and deletion verification. |
| `V6-C17-OWNER-CEREMONY` | Short interactive identity/webhook/arm/status/reconcile/revoke runbook without raw values in CLI/history. |
| `V6-C18-EMERGENCY` | Atomic host-side disarm first, bounded stop proof, no false success, explicit Engine-down escalation. |
| `V6-C19-BACKUP-STATE` | Bridge authority belongs to the same quiesced generation as application state; restore starts disarmed/no-egress. |
| `V6-C20-DESTINATION` | Secret-bearing Telegram/DeepSeek processes have only reviewed provider operations through V4 control points. |

## 2. Protected records and identity rules

Raw tokens, raw bot/user/chat/thread IDs, webhook URL, message bodies and pricing credentials exist only in V3-qualified protected runtime stores. Vault/evidence receives stable contract IDs, hashes, counts, enums and purpose-separated keyed pseudonyms. Plain `SHA256(raw_id)` is forbidden because small identifier spaces are enumerable.

### 2.1. `bot_identity_authorization/v2`

Owner creates this record offline through secret-safe interactive input before any API call:

```yaml
schema: n8nagents.bot-identity-authorization/v2
authorization_id: <uuid>
plan_sha256: <exact full plan v2>
environment_ref: <keyed pseudonym>
purpose: LOCAL_REAL_DEV_ONLY
expected_dev_bot_id: <raw only in protected record>
expected_dev_bot_ref: <HMAC-SHA256 purpose=bot-evidence>
token_key_id: <non-secret key reference>
token_fingerprint: <HMAC-SHA256 purpose=token-binding; never plain token hash>
production_bot_deny_refs: [<keyed refs>]
production_token_deny_fingerprints: [<keyed refs where known>]
exclusive_use: true
owner_decision_ref: <exact gate record>
issued_at_utc: <timestamp>
expires_at_utc: <timestamp>
record_mac: <keyed integrity>
```

Rules:

- `expected_dev_bot_id` is obtained by the owner independently, not inferred as sufficient proof from the presented token.
- Dev identity must differ from every production deny entry. Missing registry, overlap, unknown purpose, expired record or token fingerprint change gives `BLOCKED_V6_IDENTITY` before network.
- A phase-scoped `getMe` response is accepted only when `ok=true`, schema is exact enough for locked client, returned bot ID equals `expected_dev_bot_id`, bot account predicate is true and token fingerprint is unchanged immediately before and after the call.
- Evidence stores only bot ref, predicate results and record hashes. Username/name/photo are neither required nor retained.

### 2.2. Conjunctive recipient authorization

Each owner-approved tuple is one exact record:

```text
(verified_bot_id, chat_id, from_user_id, chat_type, message_thread_id|null)
```

The predicate is logical `AND` over all five components. `message_thread_id=null` is itself an exact value; it is not wildcard. Supported initial chat types are `private`, `group`, `supergroup`. A forum tuple requires the exact thread ID. The initial design rejects bots as senders, missing `from`, `sender_chat`, anonymous admin/channel identity, forwarded origin, automatic forward and chat migration. Any later support is scope expansion plus new fixture/review.

Raw tuple values live only in the protected authorization store and immutable reply route. Evidence uses distinct HMAC purposes for bot, actor, conversation and route so records cannot be correlated across unrelated evidence sets.

## 3. Arm state machine: zero API before arm

### 3.1. States

```text
MOCK_OR_STOPPED
  -> IDENTITY_BOUND_OFFLINE
  -> PROBE_ARMED
  -> PROBE_COMPLETE
  -> WEBHOOK_DECISION_REQUIRED
  -> WEBHOOK_TRANSITION_ARMED
  -> WEBHOOK_QUALIFIED
  -> REAL_ARMED
  -> REAL_ACTIVE
  -> DRAINING
  -> DISARMED

any armed/active state
  -> DISARMED_DRIFT | DISARMED_EXPIRED | DISARMED_CAP
  -> DISARMED_CONFLICT | DISARMED_INCIDENT
```

Every Telegram API request carries a local authorization decision for one allowed phase/method. The egress path rejects a request unless the current arm record and method match. There is no implicit `getMe` exception.

### 3.2. Phase arms

| Phase | Maximum TTL | Permitted methods | Mutation |
|---|---:|---|---|
| `PROBE_ARMED` | 5 minutes | exactly one `getMe`, one `getWebhookInfo`; no automatic retry | none at provider |
| `WEBHOOK_TRANSITION_ARMED` | 5 minutes | identity recheck, bounded `getWebhookInfo`; optionally exactly one `deleteWebhook` with frozen boolean | only exact owner-approved webhook action |
| `REAL_ARMED` | 30 minutes | bounded `getWebhookInfo`, `getUpdates`, ledger-authorized `sendMessage` | polling and capped sends |
| `DEEPSEEK_ARMED` | 15 minutes | exact provider/model request through separate adapter | separate cost authorization |

Owner may choose a shorter TTL, never a longer one without changing the plan. Each phase auto-invalidates after its postcondition or expiry.

### 3.3. `telegram_arm_record/v2`

The record binds at least:

```text
arm_id, phase, authorization_id, plan_sha256, project_candidate_sha256,
compose_lock_sha256, workflow_inventory_sha256, bridge_schema_lock_sha256,
runtime/image lock hashes, V1 endpoint hash, V4 network-policy hash,
environment_ref, host_boot_ref, Docker daemon/session ref, operator_ref,
bot identity record hash, token key ID/fingerprint, tuple-set hash,
data-class policy hash, webhook decision/postcondition hash,
Telegram cap scope+ceiling(20)+current ledger hash,
allowed methods+exact request bounds, issued/expires UTC, owner decision ref,
record sequence, previous arm hash, record MAC.
```

`real-dev start` must validate every field before secret mount, container start or API. Missing/expired/corrupt/unknown, config or workflow drift, host reboot, Docker daemon identity change, tuple/token/webhook/cap/price change, lease loss, stop, cap exhaustion or emergency request atomically revokes the arm. Restart/reboot never re-arms.

## 4. Webhook and backlog transaction

### 4.1. Snapshot

After `PROBE_ARMED`, bridge obtains and schema-validates `getMe` and `getWebhookInfo`. Protected snapshot includes exact response hash, `url` only in protected memory/record, a keyed URL-origin ref, `has_custom_certificate`, `pending_update_count`, `allowed_updates`, redacted error class/time and acquisition UTC. Evidence contains no URL or provider payload.

Unknown URL ownership, non-dev identity, malformed response, custom certificate custody, snapshot drift or an unrecognized field needed for decision results in `BLOCKED_V6_WEBHOOK`.

### 4.2. Exact owner decision

Owner selects exactly one enum:

| Decision | Exact provider action | Preconditions |
|---|---|---|
| `REQUIRE_EMPTY_NO_DELETE` | no `deleteWebhook` | snapshot URL empty; owner separately selects backlog disposition |
| `DELETE_KEEP_BACKLOG` | `deleteWebhook(drop_pending_updates=false)` | dedicated dev bot, owner accepts removal and preserving pending updates |
| `DELETE_DROP_BACKLOG` | `deleteWebhook(drop_pending_updates=true)` | separate irreversible/data-loss confirmation names pending count and exact bot ref |
| `ABORT` | none | state returns disarmed |

Parameter omission is forbidden: when `deleteWebhook` is called, `drop_pending_updates` is explicit boolean. No other argument is allowed by the locked client schema.

Backlog disposition is separately exact: `PROCESS_EXISTING_AUTHORIZED_BACKLOG`, `DROP_ALL_PENDING` or `REQUIRE_ZERO_PENDING`. `PROCESS_EXISTING_AUTHORIZED_BACKLOG` still applies current classifier/tuple/data policy to every Update. It does not bypass TTL or privacy constraints.

### 4.3. Postcondition and restore policy

Within `WEBHOOK_TRANSITION_ARMED`, the bridge may perform one immediate post-read and at most two additional reads within a total 15-second deadline. Required postcondition:

- verified dev identity unchanged;
- webhook URL empty;
- exact backlog condition matches decision (`pending_update_count=0` for drop/require-zero; preservation decision records observed count but never promises exact delivery count);
- no custom-certificate state requiring retained material;
- response hash/time is bound into final `REAL_ARMED` record.

Failure or a webhook that reappears blocks polling and disarms. The dev bot is required to be exclusive to this local laboratory. Automatic webhook restoration is deliberately `NEVER`: retained webhook URL/certificate would expand secret/data custody and could recreate a foreign integration. If restoration is required, real-dev is `BLOCKED_SCOPE` pending a separate plan and owner gate.

## 5. Fenced single poller across projects

`bridge.poller_lease` in the canonical `n8nagents_app.bridge` authority is global for `(environment_ref, verified_bot_ref)`, not Compose project-scoped. Bridge reaches it only through the authenticated canonical internal ingress. A second Compose project cannot substitute its own DB/ingress because arm binds the canonical ingress/workflow/DB lock hashes; lack of reachability or mismatch blocks before polling.

### 5.1. Lease semantics

- Acquire is one PostgreSQL transaction under advisory lock. It rejects a non-expired holder; takeover after expiry increments a monotonic `fence_epoch` and records arm/project/run/container refs.
- Initial lease TTL is 30 seconds; owner renews every 10 seconds. Bounds are lock fields, not runtime defaults.
- Immediately before every `getUpdates` request, after every response and on every offset/inbox/outbox/send transition, the bridge sends a fresh authenticated control envelope; internal ingress relays it to a SECURITY DEFINER procedure with fixed `search_path`, which proves current `(lease_id, fence_epoch, arm_id)`.
- A stale epoch cannot renew, commit terminal state, advance offset, reserve cap or dispatch outbox. Lease loss cancels/drains the in-flight long poll and disarms.
- Compose replica count one is defense-in-depth, not the exclusivity proof.
- Pre-start workflow inventory rejects Telegram Trigger and any n8n Telegram credential/node on the real path. Static/config tests reject direct Bot API clients outside bridge.
- Telegram polling conflict (`409` or locked equivalent) is treated as evidence of an uncontrolled consumer: no retry, atomic `DISARMED_CONFLICT`, lease invalidation and owner reconciliation.

An external/manual poller that ignores this protocol cannot be prevented by local cooperation. The Telegram conflict response and mandatory disarm are the final detector; this remains an explicit residual risk.

## 6. Strict Update classification and pre-storage authorization

### 6.1. Retrieval contract

Locked initial `getUpdates` request uses `allowed_updates=["message"]`, positive offset from durable state when present, nonnegative offsets only, bounded `limit=20`, `timeout=20 seconds`, and an HTTP client deadline greater than the long-poll timeout but no more than 30 seconds. Missing initial offset is allowed only by the approved first-run/backlog branch. Negative offset and provider-side «tail skip» are forbidden.

Response processing first validates HTTP/Bot API envelope, then a bounded JSON body, then sorts unique Updates by ascending `update_id`. Duplicate `update_id` with byte-identical canonical payload is one observed record; different payload for the same ID is integrity failure and disarm.

### 6.2. Classifier

Before any payload persistence or n8n/application DB call, bridge requires:

- one integer `update_id` in the locked numeric range;
- exactly supported top-level Update kind `message`; other kinds are terminal `DROP_UNSUPPORTED_KIND` when `update_id` is trustworthy;
- `message.text` string with `1..4096` Unicode scalar values, valid UTF-8 representation, maximum `16384` UTF-8 bytes and no NUL;
- integer `message_id`, integer `chat.id`, exact supported `chat.type`, integer `from.id`, `from.is_bot=false`;
- exact nullable `message_thread_id` semantics;
- absence of `sender_chat`, forward-origin fields, automatic forward and service-message fields;
- timestamp/backlog class compatible with arm policy; date never replaces `update_id` ordering.

Unknown/additional fields are tolerated only outside the security decision set and never copied by generic object spread. A versioned projector constructs an allowlisted normalized object. Missing/unparseable `update_id` is not droppable safely: polling stops with `FAIL_V6_PROTOCOL` because no safe checkpoint can be formed.

### 6.3. Authorization and terminal drop

After classification, bridge compares the exact five-part tuple with the active tuple set. No wildcard, OR match, username, forwarded identity, chat migration or LLM-provided identifier participates.

For unauthorized or unsupported valid-ID Update:

1. raw object remains in process memory only and is zero-referenced after classification;
2. no request reaches n8n, application/runtime roles, memory, LLM or tools;
3. bridge authority stores only `update_id`, terminal reason enum, arm/bot/fence refs, canonical classifier version and no raw tuple/body;
4. one purpose-keyed pseudonymous counter is incremented by reason and coarse time bucket; raw ID and reversible hash are forbidden;
5. terminal record participates in highest-contiguous checkpoint.

Raw payload logging, exception serialization, request tracing and dead-letter body storage are forbidden. An unauthorized poison Update must not block later authorized Updates.

## 7. Authenticated bridge envelope and durable acceptance

Every bridge-to-ingress operation uses its own closed schema in family `n8nagents.telegram.control/v2`: `lease-acquire`, `lease-renew`, `terminal-drop`, `authorized-inbox`, `outbox-claim`, `send-attempt-reserve`, `send-attempt-finish` and `status`. There is no generic operation name, arbitrary procedure selector or free-form parameters map. Method/path/schema are one-to-one with one allowlisted procedure and are covered by the MAC. Only `authorized-inbox` contains message text/raw authorization tuple; other schemas reject those fields.

Authorized normalized Updates входят в durable authority по точному пути `telegram-bridge -> V4 telegram_ingress -> n8n internal control workflow -> bridge.accept_authorized_inbox`. Bridge не подключён к DB. n8n получает envelope только в памяти, не имеет HMAC key и может лишь передать exact value в procedure под `automation_runtime`. Аргумент процедуры — `n8nagents.telegram.ingress/v2`, а не произвольный набор SQL parameters:

```yaml
schema: n8nagents.telegram.ingress/v2
authorization_id: <uuid>
arm_id: <uuid>
bot_ref: <keyed ref>
fence_epoch: <integer>
update_id: <integer>
work_id: <UUIDv7 derived once and durably bound>
actor_ref: <purpose-keyed pseudonym>
conversation_ref: <purpose-keyed pseudonym>
authorization_tuple: <raw five-part tuple; protected transport/DB only>
received_at_utc: <timestamp>
text: <validated authorized text>
classifier_version: <exact>
```

Unknown fields are rejected (`additionalProperties=false`). Content type is exactly JSON UTF-8; canonical envelope maximum is `24 KiB`. Raw tuple is MAC-covered. It is transiently relayed by n8n but exact V5 execution settings/body-limit qualification must prove no execution/payload persistence before real-dev. Procedure compares it with owner authorization and atomically creates/reuses an opaque immutable route. Durable/result surfaces expose only `work_id`, purpose-keyed actor/conversation refs and `reply_route_ref`.

### 7.1. Authentication and anti-replay

Internal HTTP request includes method/path/content type, schema version, key ID, timestamp, 128-bit random nonce and HMAC-SHA-256 over canonical method, path, schema version, authorization/arm/fence refs, timestamp, nonce and canonical-envelope SHA-256. n8n passes the envelope/MAC fields unchanged to PostgreSQL. Canonical JSON serialization and key rotation overlap are hash-locked before implementation. Exact verifier primitive is a V2-locked PostgreSQL cryptographic extension/function; if authenticated verification or nonpersistent bounded relay cannot be supply/version-locked and negative-tested, real-dev is `BLOCKED_V6_ENVELOPE_CAPABILITY` with no weaker fallback.

HMAC material is generated in the owner secret ceremony. Bridge reads its one-file secret; verifier reads the matching key from protected `bridge.envelope_keyring`, writable only by one-shot migration/rotation authority and unreadable to runtime roles. n8n and `automation_runtime` cannot select the key table or obtain key bytes. Encrypted backup/restore and rotation treat it as a secret. PostgreSQL server/approved DB owner is therefore an explicit verifier consumer and trust-boundary member.

Verifier order:

1. n8n internal endpoint enforces method/path/content-type/body limit and exact inactive/active workflow hash without logging/persisting body;
2. it calls one allowlisted procedure as exact `automation_runtime`; arbitrary SQL/parameters are impossible;
3. procedure enforces canonical envelope length/schema without emitting the value;
4. locate exact key ID and bot principal binding;
5. verify MAC in constant-time and timestamp within ±30 seconds;
6. atomically insert `(key_id, nonce)` into durable replay ledger with unique constraint;
7. compare arm/bot/fence/update/tuple fields against server authority;
8. in the same transaction create/reuse inbox and immutable reply route and advance only the highest-contiguous terminal prefix;
9. return a structured signed ACK after commit; n8n relays bytes unchanged.

Missing/wrong internal caller/workflow hash/DB principal/MAC, expired/replayed nonce, envelope mutation, wrong bot/fence/arm, oversized value or call from mock role is rejected before inbox/application/memory/LLM/tools. Only keyed aggregate auth counter in the protected bridge authority is permitted. If exact n8n version persists a forged/raw envelope before procedure verification, real-dev remains blocked.

### 7.2. ACK

HTTP `2xx` alone never advances offset. Required ACK schema includes:

```text
schema, authorization_id, arm_id, bot_ref, fence_epoch, update_id,
work_id, inbox_state=DURABLE_ACCEPTED, canonical_body_sha256,
accepted_at_utc, ack_nonce, ack_mac
```

Bridge verifies ACK MAC, freshness and equality to request. Wrong/missing/duplicate-conflicting ACK is nonterminal; offset remains unchanged. A valid duplicate request returns the same durable `work_id` and equivalent ACK identity. The verifier and ACK signer may share one rotation family only if domain-separated keys are derived and exact derivation is locked; otherwise two keys are mandatory.

## 8. Durable offset, inbox, idempotency and outbox

### 8.1. PostgreSQL procedure boundary

V5 delivers checksummed SQL in `n8nagents_app.bridge`; V6 defines semantics. Runtime roles have no raw table access.

Minimum procedures invoked only through exact authenticated internal control workflows:

```text
bridge.acquire_poller_lease(...)
bridge.renew_poller_lease(...)
bridge.revoke_arm(...)
bridge.record_terminal_drop(...)
bridge.accept_authorized_inbox(envelope_json, key_id, timestamp, nonce, envelope_mac)
bridge.claim_work(...)
bridge.complete_work(...)
bridge.enqueue_reply(work_id, idempotency_key, body)
bridge.claim_outbox(...)
bridge.reserve_send_attempt(...)
bridge.finish_send_attempt(...)
bridge.status_redacted(...)
```

Every SECURITY DEFINER function has fixed owner/search path, explicit parameter types, revokes PUBLIC, validates caller role plus HMAC/nonce/current arm/fence as applicable, and returns a versioned result. Dynamic SQL and caller-selected schema/route are forbidden. `telegram-bridge` has no DB role/network; `automation_runtime` cannot call raw tables and internal workflows cannot construct unsigned operations.

`advance_contiguous_offset` is an internal non-granted function invoked only inside terminal-drop/inbox transactions; no runtime role or HTTP workflow can call it directly. Owner/emergency revocation uses a distinct local control-plane authorization, not a bridge envelope, and remains idempotent/fail-closed.

### 8.2. Offset authority

State namespace is `(environment_ref, verified_bot_ref, authorization_id, classifier_version)`. It includes schema version, checksum/MAC, highest terminal observed record, `next_offset`, current fence and monotonic revision. There is exactly one authority: PostgreSQL `bridge` schema; an additional file offset is forbidden.

For each ordered response batch:

1. create observations in increasing `update_id` without advancing checkpoint;
2. reach durable terminal state `DROPPED_UNSUPPORTED`, `DROPPED_UNAUTHORIZED` or `DURABLE_ACCEPTED` for the first nonterminal item;
3. continue sequentially or through durable queue, but never advance past a lower nonterminal observed item;
4. each terminal procedure invokes the same internal CAS in its transaction; it advances only to the last terminal prefix and sets `next_offset=last_update_id+1`;
5. fsync durability is PostgreSQL commit durability as qualified by V5/V3; only after commit may the next `getUpdates` use new offset.

Missing/corrupt/ahead/rollback state, token/bot/auth mismatch or observation gap gives `BLOCKED_V6_OFFSET`; no automatic reset. Reset/backlog reconciliation is a manual gate.

### 8.3. Work and outbox state machines

Authorized inbox:

```text
DURABLE_ACCEPTED -> CLAIMED -> PROCESSING
  -> COMPLETED_NO_REPLY
  -> OUTBOX_ENQUEUED
  -> FAILED_RETRYABLE (bounded internal processing)
  -> FAILED_TERMINAL
```

Claim uses a lease and generation. Expired processing lease may be reclaimed; stale generation cannot complete or enqueue. `bridge.enqueue_reply` is idempotent by `(work_id, owner-approved logical_reply_id)` and performs one transaction that validates active route, deterministically splits text into chunks, assigns immutable ordinals, creates outbox rows and reserves one initial Telegram cap slot per chunk. If the whole chunk set cannot fit, the transaction creates neither reply nor reservation. n8n can call this procedure but cannot supply/override raw destination, bot, chat or thread.

Outbox:

```text
QUEUED -> RESERVED -> DISPATCHING
  -> SENT_CONFIRMED
  -> FAILED_TERMINAL
  -> AMBIGUOUS_CONSUMED
```

Exactly-once is guaranteed only for local inbox/outbox state transitions under DB constraints. Provider side effect remains at-most-one automatic attempt after `DISPATCHING`; ambiguous completion is never silently marked success or retried.

## 9. Immutable reply route and global Telegram cap 20

### 9.1. Route

`reply_route` is constructed only by the authorization gateway from the verified five-part tuple and stored immutably with authorization ID, bot/token key ID, route version and active/revoked state. n8n/LLM/tools see only opaque `reply_route_ref` and pseudonymous conversation ref.

Both private and forum replies resolve server-side to exact `chat_id` and nullable `message_thread_id`. Alternative IDs in user text, LLM output, tool result, workflow JSON or adapter request are ignored/rejected. Chat migration response never rewrites the route automatically; it disarms and requires new owner binding.

### 9.2. One outbound path

- n8n Telegram Credential, Telegram node/Trigger and arbitrary HTTP/Code/Execute Command outbound path are forbidden in real-dev workflow inventory.
- Only `telegram-bridge` holds token and may invoke Telegram methods through V4 proxy.
- Sender claims only DB outbox rows. No manual `sendMessage` helper bypass exists; owner test sends also enqueue through the same stored procedure/ledger.
- Static workflow/image scan, runtime egress test and secret-mount inventory must independently prove this property.

### 9.3. Cap accounting

The owner authorization fixes `telegram_send_ceiling=20`. Counted unit is every real outbound `sendMessage` network attempt after a reservation reaches `DISPATCHING`, including:

- every response chunk;
- first attempts and retries;
- parallel workflows/projects;
- owner/manual test messages;
- adapter/bridge internal retries;
- timeout/reset/unknown outcome after request transmission may have begun.

Inbound `getUpdates` and read-only webhook/identity calls do not consume this send cap; they have separate method/TTL bounds. A provider response definitively received before any `sendMessage` transmission is not a send attempt, but its reservation is either safely released before `DISPATCHING` or, if transmission boundary is uncertain, becomes counted ambiguous.

Initial reservations are created atomically by `bridge.enqueue_reply`. Sender changes that exact reservation to `DISPATCHING` immediately before the network call. `bridge.reserve_send_attempt` is used only for an explicitly permitted retry and serializes on the same ledger row. No more than 20 reservations can exist across initial/retry paths. A reservation cancelled with proof that it never reached `DISPATCHING` may be released; any uncertain boundary is `AMBIGUOUS_CONSUMED`. Restart/rearm preserves consumed/reserved/ambiguous rows. Counter corruption, unknown reservation or `consumed+reserved >= 20` disarms real-dev; 21st reservation fails before network.

New authorization ID may create a new ledger only after an explicit owner gate. Reusing a new arm under the same authorization never resets it.

## 10. Telegram HTTP/Bot API error policy

The locked client evaluates transport state, HTTP status, JSON parse, top-level `ok`, result/error schema and method-specific fields. Generic «retry on failure» is forbidden.

| Class | Required action |
|---|---|
| Valid method success | Commit exact method postcondition; for send store only protected/pseudonymous message result fields. |
| Malformed `2xx`, schema conflict | `FAIL_V6_PROTOCOL`; no offset/send success; disarm if identity/state is uncertain. |
| `401`/invalid token | terminal identity incident; disarm, stop polling/sending, owner revoke/replace flow. |
| `403`/blocked or forbidden recipient | terminal route failure; revoke route and disarm; no retry. |
| Polling `409` conflict | `DISARMED_CONFLICT`; invalidate lease/arm; no automatic retry. |
| `429` with valid bounded `retry_after` | current API attempt is accounted; schedule at most one new attempt only if new reservation, arm TTL, operation deadline and cap all remain valid. |
| Missing/invalid/excessive `retry_after` | block/manual; no guessed delay. |
| Definitive pre-transmission DNS/connect/TLS failure | method policy may allow at most one retry under a new request/send reservation; all bounds still apply. |
| `5xx`, connection reset or timeout after transmission may begin | send becomes `AMBIGUOUS_CONSUMED`; no blind retry. Poll request may retry only after lease/arm/offset revalidation because it has no provider-side send effect. |
| `migrate_to_chat_id` or equivalent route mutation | no automatic migration; disarm and require owner rebind. |
| Unknown error code/parameter | fail closed and preserve redacted diagnostic class only. |

No backoff may outlive arm TTL, lease or owner deadline. Circuit state is durable enough to survive restart and cannot be reset by container recreation.

## 11. Separate DeepSeek authorization and ledger

n8n has no DeepSeek key or direct external route. Only a reviewed local LLM adapter/proxy may receive the key and reach the exact V4-approved provider destination. Telegram arm and Telegram cap do not imply DeepSeek permission.

`deepseek_authorization/v2` must contain non-placeholder exact values before any call:

```text
authorization_id, plan/config/workflow/runtime lock hashes,
provider=DeepSeek, exact base origin and API operation, exact model ID,
pricing source evidence hash+revision+retrieved/effective UTC,
currency=USD, owner-approved amount ceiling (never above USD 5.00 in this plan),
request ceiling, per-request max input/output tokens,
exact input/output/cache pricing units and decimal rates,
timeout, retry policy, TTL<=15m, key ID/fingerprint,
allowed pseudonymous work scopes, owner decision ref, record MAC.
```

The `USD 5.00` value is a plan maximum, not a claim that local spending is already authorized. Missing/changed/unknown pricing, model, currency, usage semantics or key blocks all provider calls.

Before each attempt, one serializable transaction reserves conservative worst-case cost using decimal/fixed-point arithmetic and the maximum token parameters. Concurrent attempts cannot overbook. After a valid signed/schema-checked usage record, ledger reconciles actual cost without ever increasing available amount beyond the original scope. Timeout, invalid/missing usage or ambiguous billing consumes the full reservation. A retry is a new request and reservation; request count and money both apply.

Ledger correlates `authorization_ref -> work_ref -> n8n_execution_ref -> provider_attempt_ref -> Telegram outbox/send refs` using purpose-keyed pseudonyms and hashes, never message/prompt contents or raw provider payload. Telegram cap and DeepSeek cost status are shown separately.

## 12. Mock, dry-run and mode convergence

### 12.1. `dry-run`

Dry-run:

- performs no Docker/file/DB/provider mutation;
- reads no Telegram/DeepSeek/DB/n8n secret;
- issues no DNS, HTTP, Telegram, DeepSeek or webhook request;
- does not create/renew arm, lease, nonce, offset, cap, inbox, route, outbox or cost row;
- only renders secret-free desired state, validates offline fixtures and emits a no-change record.

An online read-only provider probe is never called dry-run; it is `PROBE_ARMED` with owner-visible external traffic.

### 12.2. `mock`

Mock uses distinct mock credentials/identities/stores and internal endpoints only. Real token/key secret mounts are absent, V4 shows no uplink/default external route, and real bridge ledger is read-only/unmounted. Mock may mutate only isolated local test DB/state. It cannot change provider webhook, offset, send cap or DeepSeek cost.

Mode transition follows V5: stop forbidden prior-mode services, verify no poller/egress/secret mount, then start target graph. `real-dev -> mock/stop` always disarms first. Mixed mock+real services, direct profiled service target or restart-induced real polling is failure.

## 13. Secrets, PII and retention

### 13.1. Secret-to-consumer matrix

| Secret | Sole consumer | Prohibited consumers/sinks |
|---|---|---|
| Telegram dev token | `telegram-bridge` | n8n, PostgreSQL, `egress-telegram`, mocks, CLI args, env render, logs/evidence |
| Bridge envelope key | bridge file + PostgreSQL protected verifier keyring | n8n workflow nodes, runtime DB roles, mocks, broker, evidence |
| PostgreSQL `automation_runtime` password | n8n protected Credential/entrypoint only | bridge, brokers, mocks, host process list/logs |
| DeepSeek key | exact LLM adapter only | n8n, Telegram bridge, mocks, logs/evidence |
| Pseudonym/evidence keys | trusted control/evidence components by purpose | application workflows and provider adapters |

V3 determines one-file secret mounts/ACL/at-rest eligibility. Secret entry is interactive hidden input or owner UI; never command argument, clipboard transcript, reusable temp file, screenshot or Vault. Token-bearing Telegram URL must be field-aware redacted before any error/log; support bundles and HTTP debug tracing are disabled.

### 13.2. Data map

| Data class | Allowed storage | Maximum retention before owner-approved change |
|---|---|---:|
| Raw unauthorized/unsupported Update | none; process memory only | request lifetime |
| Raw authorized incoming text | protected inbox/work state only | 24 hours after terminal work state |
| Outgoing reply/chunk body | protected outbox only | 24 hours after terminal send state |
| Raw bot/chat/user/thread IDs | protected identity/route authority only | authorization lifetime + recovery window fixed by V3 |
| Offset/update IDs and terminal reason | bridge control state | current authorization + verified backup/RPO window |
| Cap/cost/send attempt ledger | bridge control state, pseudonymous | authorization + audit window; cannot expire before reconciliation |
| n8n execution payload | forbidden; exact V5 settings disable success/error/manual/progress payload retention | zero |
| Evidence/logs | hashes, counts, enums, keyed pseudonyms only | V3 evidence policy |

Initial real-dev data class is `SYNTHETIC_TEST_TEXT_ONLY`: no credentials, financial/medical/legal/private third-party data, documents, media, contact cards or location. Owner must approve any expansion. Browser exports, pinned/manual n8n data and screenshots with message content or identifiers are forbidden.

Purge is an explicit owner-visible operation covering inbox/outbox, allowed memory rows, n8n data surfaces and backup generations according to V3. It verifies canary absence but does not promise secure erase of SSD/VHDX/pagefile. Backup containing retained data follows the longer V3 retention and remains an explicit residual copy.

## 14. Owner workflows and emergency stop

All commands are versioned wrappers with no raw secret/ID in argv and have human plus schema-valid JSON output.

### 14.1. Owner ceremony

1. `lab telegram identity-bind` — offline hidden input; shows only dev/production keyed refs and purpose.
2. `lab telegram probe-arm` — previews exact read-only methods, bot ref, TTL and zero-send state; owner approves one probe record.
3. `lab telegram webhook-plan` — shows redacted webhook/backlog snapshot; owner selects exact decision. `DROP` requires separate irreversible confirmation.
4. `lab telegram webhook-apply` — executes only frozen action, verifies postcondition, auto-closes transition arm.
5. `lab telegram tuple-bind` — owner reviews redacted five-part tuple and synthetic data class.
6. `lab telegram arm` — shows plan/config/workflow/bot/tuple hashes, TTL, cap `20`, current consumed count and DeepSeek=`DISARMED`; explicit confirmation creates real arm.
7. `lab start --mode real-dev` — V5 convergence; no arm means nonzero before secret mount/API.
8. `lab telegram status`, `budget-status`, `offset-status` — read-only redacted state and one next safe action.
9. `lab telegram disarm` — atomically revokes arm, drains/stops and verifies no polling/send/secret mount.
10. `lab telegram offset-reconcile` — only after corruption/conflict/backlog decision; shows consequences, never guesses/reset silently.
11. `lab telegram revoke-guide` — owner-only BotFather/token rotation instructions; tooling does not automate account ownership action.

### 14.2. Emergency stop

`lab emergency-stop telegram` performs in this order:

1. host-side protected control record is atomically set `DISARM_REQUESTED` before Docker calls;
2. if DB reachable, revoke arm and lease in one transaction; sender can no longer reserve/dispatch;
3. cancel poll, stop bridge, verify no active poll request/outbox dispatch/real secret mount/uplink service;
4. preserve volumes/secrets and write redacted diagnostics; no prune/delete/factory reset;
5. report `DISARMED_VERIFIED` only after all observable postconditions.

If Engine/DB is unavailable, host state remains disarmed and auto-restart is blocked, but absence of a still-running remote effect cannot be proven. Result is `EMERGENCY_UNVERIFIED`, nonzero. Owner is instructed to exit/stop Docker Desktop using the exact V1 runbook and, when uncertainty includes token compromise or uncontrolled poller, revoke token through BotFather from a trusted session. On next Engine start, entrypoint consumes host disarm marker and exits before API; status must then close the incident or remain nonzero. Reboot/session boundary always invalidates arm.

## 15. Statuses, RC and manual gates

String status is authoritative; global integrator may remap numeric RC but must preserve nonzero/fail-closed meaning.

| RC | Status | Meaning |
|---:|---|---|
| `0` | `V6_MOCK_SAFE`, `V6_REAL_ARMED_READY`, `V6_DISARMED_VERIFIED` | Exact scoped postconditions only; never overall project PASS. |
| `10` | `V6_READY_OWNER_GATE` | Exact owner decision required; no unauthorized API/mutation. |
| `100` | `BLOCKED_V6_NOT_ARMED` | Missing/expired/wrong-phase arm; zero external API. |
| `101` | `BLOCKED_V6_IDENTITY` | Dev identity/production deny/token binding unknown or mismatch. |
| `102` | `BLOCKED_V6_WEBHOOK` | Snapshot/action/backlog/postcondition not safe. |
| `103` | `BLOCKED_V6_AUTHORIZATION` | Tuple/data class/route not exact or revoked. |
| `104` | `BLOCKED_V6_LEASE` | Current fenced poller lease unavailable/lost. |
| `105` | `BLOCKED_V6_OFFSET` | Offset/control state missing, corrupt, cross-bot or ambiguous. |
| `106` | `BLOCKED_V6_CAP` | Telegram cap exhausted/unknown/inconsistent. |
| `107` | `BLOCKED_V6_DEEPSEEK` | Exact model/pricing/currency/request/cost gate absent/drifted. |
| `108` | `BLOCKED_V6_PRIVACY` | Data class, retention, at-rest or secret boundary not accepted. |
| `109` | `BLOCKED_V6_DESTINATION` | V4 exact provider-route enforcement not PASS. |
| `110` | `BLOCKED_V6_ENVELOPE_CAPABILITY` | Locked authenticated verifier primitive unavailable; no weaker fallback. |
| `111` | `FAIL_V6_PROTOCOL` | Malformed/contradictory Telegram or internal protocol state. |
| `112` | `FAIL_V6_ENVELOPE_AUTH` | MAC/principal binding invalid. |
| `113` | `FAIL_V6_REPLAY` | Replay/nonce/timestamp contract violated. |
| `114` | `FAIL_V6_DURABILITY` | ACK/offset/inbox/outbox transaction not proven. |
| `115` | `AMBIGUOUS_V6_SEND_CONSUMED` | Possible external send; cap consumed; no blind retry. |
| `116` | `FAIL_V6_TELEGRAM_TERMINAL` | Auth/forbidden/migration or other terminal provider error. |
| `117` | `DISARMED_V6_CONFLICT` | Polling conflict/uncontrolled consumer detected. |
| `118` | `BLOCKED_V6_RETRY_WINDOW` | `retry_after`/TTL/deadline/cap cannot be safely satisfied. |
| `119` | `EMERGENCY_V6_UNVERIFIED` | Disarm intent recorded, but running-state stop not fully proven. |
| `120` | `FAIL_V6_INTEGRITY_INTERNAL` | Ledger/schema/collector/internal invariant failure. |

Manual gates:

| Gate | Exact decision | Blocks |
|---|---|---|
| `MG-V6-IDENTITY` | separate dev bot identity, purpose, production deny and exclusive use | any Telegram arm/API |
| `MG-V6-PROBE` | bot ref, exact read-only methods and TTL | `getMe/getWebhookInfo` |
| `MG-V6-WEBHOOK` | snapshot hash, backlog enum, exact delete boolean, no-restore policy | webhook mutation/polling |
| `MG-V6-DROP-BACKLOG` | irreversible drop and observed pending count | `drop_pending_updates=true` |
| `MG-V6-TUPLE-DATA` | exact five-part tuple and data class | authorized delivery/send |
| `MG-V6-REAL-ARM` | all hashes, TTL<=30m, cap=20/current count, stop rule | real-dev secret mount/start/API |
| `MG-V6-DEEPSEEK` | exact model/origin/pricing/currency/USD ceiling/request/tokens/TTL | any DeepSeek call/cost |
| `MG-V6-OFFSET-RECONCILE` | exact old/new checkpoint and backlog consequence | reset/recovery polling |
| `MG-V6-PII-RETENTION` | retention/backup/residual-copy policy | real data beyond synthetic fixtures |
| `MG-V6-INCIDENT` | revoke/rotate/rebind or accepted residual | resume after terminal incident |

Plan approval may authorize implementation and offline/mock tests, but cannot manufacture missing secrets, recipient identity, owner account action, irreversible backlog drop or new monetary authorization.

## 16. Acceptance tests, negative canaries and evidence

All tests are future obligations. Telegram/DeepSeek live cases run only under their exact arms and ceilings; most cases use locked mocks. Evidence is schema-valid, redacted and hash-bound to plan/config/runtime/arm/run.

Canonical evidence ID is the `EV-V6-NN` prefix. The descriptive suffix shown below is its artifact label; for example, `EV-V6-01` and `EV-V6-01-IDENTITY` identify the same sole catalog record, not two artifacts.

| ID | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `AT-V6-01` | Correct dev token under `PROBE_ARMED` matches owner record; five identity cases isolate exact dev bot. | `NC-V6-01`: production/other/missing/swapped token reaches zero webhook/poll/send calls. | `EV-V6-01-IDENTITY` record hashes, keyed refs, method counters. |
| `AT-V6-02` | No-arm, expired, rebooted, drifted and cap-exhausted states reject before secret mount/API; valid phase allows only exact methods. | `NC-V6-02`: call `getMe` from unarmed dry-run or `sendMessage` under probe arm. | `EV-V6-02-ARM` transition ledger and zero-API trace. |
| `AT-V6-03` | Empty/keep/drop/unknown/delete-failure/reappearing webhook matrix reaches polling only on exact postcondition. | `NC-V6-03`: flip `drop_pending_updates` or snapshot hash after approval. | `EV-V6-03-WEBHOOK` redacted snapshot/action/postcondition. |
| `AT-V6-04` | Two projects/replicas compete; exactly one fence polls and commits; expiry takeover increments epoch. | `NC-V6-04`: stale holder tries offset/cap/outbox mutation; all denied. | `EV-V6-04-LEASE` epochs, holders refs and API-call counts. |
| `AT-V6-05` | Fixture matrix text/photo/document/service/edited/channel/callback/sender_chat/missing-from/oversize/stale behaves per classifier. | `NC-V6-05`: poison unsupported Update followed by valid text; later Update is not blocked. | `EV-V6-05-CLASSIFIER` fixture hashes/reason counts only. |
| `AT-V6-06` | Private and exact group/topic tuples pass conjunctively; all mixed components terminal-drop pre-storage. | `NC-V6-06`: same user/wrong chat, same chat/wrong user, wrong thread, anonymous/forward/migration. | `EV-V6-06-AUTHZ` tuple-policy hash and keyed counters. |
| `AT-V6-07` | Valid envelope accepted once and receives matching durable ACK. | `NC-V6-07`: missing/wrong MAC, replay, expired timestamp, body/bot/update/route mutation, oversize/unknown field/mock caller. | `EV-V6-07-ENVELOPE` schema/key refs, nonce outcomes, no-payload trace. |
| `AT-V6-08` | Three-update batch with middle failure plus crash at each write never checkpoints past nonterminal prefix. | `NC-V6-08`: cross-bot/corrupt/truncated/rolled-back offset state. | `EV-V6-08-OFFSET` revisions, terminal enums, checkpoint sequence. |
| `AT-V6-09` | Crash before/after inbox commit/ACK/claim/complete yields no lost accepted Update and bounded reclaim. | `NC-V6-09`: bare/malformed 2xx or stale claim generation tries completion. | `EV-V6-09-INBOX` work-state/ACK hashes and crash matrix. |
| `AT-V6-10` | Repeated workflow execution/enqueue produces one logical reply set and immutable chunk ordinals. | `NC-V6-10`: LLM/workflow supplies alternate chat/thread/route or duplicate idempotency key with changed body. | `EV-V6-10-OUTBOX` work/reply/chunk hashes and route refs. |
| `AT-V6-11` | At counter 19, at least ten parallel n8n/owner/adapter requests cause at most one dispatch; restart/retry/split/ambiguous never exceed 20. | `NC-V6-11`: bypass procedure/direct Telegram node/direct HTTP/manual sender. | `EV-V6-11-CAP20` atomic reservation/attempt states and total. |
| `AT-V6-12` | Mock Telegram returns success, malformed 2xx, 401, 403, 409, 429, invalid retry_after, 5xx, reset, timeout-after-accept and migration. | `NC-V6-12`: generic retry loop or ambiguous send retry. | `EV-V6-12-ERRORS` class/action/delay/cap/circuit ledger. |
| `AT-V6-13` | Nearly exhausted DeepSeek budget under parallel requests/retries never overbooks money or request ceiling. | `NC-V6-13`: changed/unknown pricing/model/currency, missing usage or timeout. | `EV-V6-13-DEEPSEEK` exact authorization/pricing hash and cost ledger. |
| `AT-V6-14` | Dry-run state diff is empty and external call count zero; mock has local-only effects and real ledgers unchanged. | `NC-V6-14`: secret read, provider DNS/HTTPS, webhook/offset/cap/cost mutation or mixed profiles. | `EV-V6-14-ZERO-EFFECT` before/after snapshots and V4 network proof ref. |
| `AT-V6-15` | Sentinels in token/header/IDs/text/prompt across success/error/retry/crash/backup/purge appear only in approved protected stores and expire as specified. | `NC-V6-15`: raw URL/body in log, n8n execution, evidence, support bundle or screenshot fixture. | `EV-V6-15-PII` field-level scan counts, never sentinel values. |
| `AT-V6-16` | Healthy/hung/unhealthy/Engine-down emergency cases disarm first, never auto-resume and preserve volumes. | `NC-V6-16`: command claims success without polling/egress stop proof. | `EV-V6-16-EMERGENCY` host/DB state transitions and next-action ID. |
| `AT-V6-17` | Owner from clean non-elevated session completes identity/probe/webhook/tuple/arm/one real exchange/status/disarm and injected conflict recovery using runbook only. | `NC-V6-17`: raw ID/token in argv/history/output or hidden implicit confirmation. | `EV-V6-17-OWNER` redacted black-box transcript and decision refs. |
| `AT-V6-18` | Quiesced backup/restore preserves arm/cap/offset/inbox/route/outbox consistency but restore starts disarmed, without secrets/egress. | `NC-V6-18`: restored stale arm polls or sends automatically; generation mismatch accepted. | `EV-V6-18-RESTORE` consistency marker and no-egress/disarmed proof refs. |

## 17. Traceability to V0 findings

`DESIGN_CLOSED` below means the required design is specified; it does not claim implementation or runtime PASS. Cross-domain findings remain jointly owned.

| Finding | V6 contract | Acceptance | Canary | Evidence | Disposition |
|---|---|---|---|---|---|
| `R3-NET-003` | `V6-C20` | `AT-V6-14` | `NC-V6-14` | `EV-V6-14` | cross-dependency V4, design specified |
| `R3-PROFILE-008` | `V6-C15` | `AT-V6-14` | `NC-V6-14` | `EV-V6-14` | cross-dependency V5, design specified |
| `R4-F01` | `V6-C02`, `V6-C15` | `AT-V6-02`, `AT-V6-14` | `NC-V6-02`, `NC-V6-14` | `EV-V6-02`, `EV-V6-14` | cross-dependency V5 |
| `R4-F02` | `V6-C02`, `V6-C04` | `AT-V6-02`, `AT-V6-04` | `NC-V6-04` | `EV-V6-02`, `EV-V6-04` | cross-dependency V5 |
| `R4-F06` | `V6-C08`, `V6-C19` | `AT-V6-08`, `AT-V6-18` | `NC-V6-08`, `NC-V6-18` | `EV-V6-08`, `EV-V6-18` | `DESIGN_CLOSED` with V3/V5 |
| `R4-F07` | `V6-C17` | `AT-V6-17` | `NC-V6-17` | `EV-V6-17` | cross-dependency V5 |
| `R5-F01` | `V6-C01`, `V6-C02` | `AT-V6-01` | `NC-V6-01` | `EV-V6-01` | `DESIGN_CLOSED` |
| `R5-F02` | `V6-C03` | `AT-V6-03` | `NC-V6-03` | `EV-V6-03` | `DESIGN_CLOSED` |
| `R5-F03` | `V6-C04` | `AT-V6-04` | `NC-V6-04` | `EV-V6-04` | `DESIGN_CLOSED` |
| `R5-F04` | `V6-C05` | `AT-V6-05` | `NC-V6-05` | `EV-V6-05` | `DESIGN_CLOSED` |
| `R5-F05` | `V6-C08` | `AT-V6-08` | `NC-V6-08` | `EV-V6-08` | `DESIGN_CLOSED` |
| `R5-F06` | `V6-C08`, `V6-C19` | `AT-V6-08`, `AT-V6-18` | `NC-V6-08` | `EV-V6-08`, `EV-V6-18` | `DESIGN_CLOSED` |
| `R5-F07` | `V6-C09`, `V6-C10` | `AT-V6-09`, `AT-V6-10` | `NC-V6-09`, `NC-V6-10` | `EV-V6-09`, `EV-V6-10` | `DESIGN_CLOSED` |
| `R5-F08` | `V6-C06` | `AT-V6-06` | `NC-V6-06` | `EV-V6-06` | `DESIGN_CLOSED` |
| `R5-F09` | `V6-C07` | `AT-V6-07` | `NC-V6-07` | `EV-V6-07` | `DESIGN_CLOSED` |
| `R5-F10` | `V6-C10`, `V6-C11` | `AT-V6-10` | `NC-V6-10` | `EV-V6-10` | `DESIGN_CLOSED` |
| `R5-F11` | `V6-C12` | `AT-V6-11` | `NC-V6-11` | `EV-V6-11` | `DESIGN_CLOSED` |
| `R5-F12` | `V6-C13` | `AT-V6-12` | `NC-V6-12` | `EV-V6-12` | `DESIGN_CLOSED` |
| `R5-F13` | `V6-C14` | `AT-V6-13` | `NC-V6-13` | `EV-V6-13` | `DESIGN_CLOSED` |
| `R5-F14` | `V6-C15` | `AT-V6-14` | `NC-V6-14` | `EV-V6-14` | `DESIGN_CLOSED` |
| `R5-F15` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | `DESIGN_CLOSED` |
| `R5-F16` | `V6-C17`, `V6-C18` | `AT-V6-17` | `NC-V6-17` | `EV-V6-17` | `DESIGN_CLOSED` |
| `R6-P1-002` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | cross-dependency secrets/V3/V5 |
| `R6-P1-004` | `V6-C05`, `V6-C06` | `AT-V6-05`, `AT-V6-06` | `NC-V6-05`, `NC-V6-06` | `EV-V6-05`, `EV-V6-06` | `DESIGN_CLOSED` |
| `R6-P1-005` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | cross-dependency V5/V3 |
| `R6-P1-006` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | cross-dependency evidence domain |
| `R6-P1-007` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | cross-dependency V3; real-dev blocked if unknown |
| `R6-P1-009` | `V6-C18` | `AT-V6-16` | `NC-V6-16` | `EV-V6-16` | `DESIGN_CLOSED` with secret issuer runbooks |
| `R6-P1-010` | `V6-C20` | `AT-V6-14` | `NC-V6-14` | `EV-V6-14` | cross-dependency V4 |
| `R6-P2-011` | `V6-C16`, `V6-C17` | `AT-V6-15`, `AT-V6-17` | `NC-V6-17` | `EV-V6-15`, `EV-V6-17` | `DESIGN_CLOSED` |
| `R7-F01` | `V6-C19` | `AT-V6-18` | `NC-V6-18` | `EV-V6-18` | cross-dependency V3/V5 |
| `R7-F02` | `V6-C08`, `V6-C19` | `AT-V6-18` | `NC-V6-18` | `EV-V6-18` | cross-dependency V3/V5 |
| `R10-F01` | `V6-C02`, `V6-C12` | `AT-V6-02`, `AT-V6-11` | `NC-V6-02`, `NC-V6-11` | `EV-V6-02`, `EV-V6-11` | `DESIGN_CLOSED` |
| `R10-F02` | `V6-C18` | `AT-V6-16` | `NC-V6-16` | `EV-V6-16` | `DESIGN_CLOSED` |
| `R10-F06` | `V6-C17`, `V6-C18` | `AT-V6-17` | `NC-V6-17` | `EV-V6-17` | cross-dependency operability |
| `R10-F10` | `V6-C16` | `AT-V6-15` | `NC-V6-15` | `EV-V6-15` | cross-dependency operability/evidence |
| `R10-F11` | `V6-C17` | `AT-V6-17` | `NC-V6-17` | `EV-V6-17` | cross-dependency operability |

## 18. Cross-domain dependencies and conflict resolution

1. **V1 endpoint/control plane:** every Docker/Compose mutation and status uses the approved local Desktop context. Arm binds endpoint/daemon/boot identity; drift disarms. V6 never changes global context.
2. **V2 supply chain:** Telegram/LLM bridge, canonical serializer, crypto library, CA trust, exact API client, pricing source and image digests must be acquired and locked there. Unknown algorithm/library support blocks implementation.
3. **V3 storage/secrets/backup:** protected roots, ACL, at-rest decision, one-file secret mounts, PostgreSQL durability, encrypted backup and retention are prerequisites. V6 supplies data classes and writer/state inventory.
4. **V4 isolation/network:** exact network names, secret-bearing bridge → secretless proxy path, proxy-only uplink, destination/SNI/redirect/DNS policy and zero-egress mock/dry evidence must be hash-bound into arm. Direct n8n/PostgreSQL internet is forbidden.
5. **V5 Compose/PostgreSQL/n8n:** required real services are `postgres`, `n8n`, `telegram-bridge`, `egress-telegram`; optional DeepSeek adds `deepseek-adapter`, `egress-deepseek`. No separate ingress-verifier service exists: exact n8n internal control workflows relay HMAC envelopes to checksummed PostgreSQL procedures. `automation_runtime` is EXECUTE-only; bridge has no DB credential/path. Current V5 direct-bridge-DB draft conflicts with frozen V4 and this resolution; integrated plan is `BLOCKED_CONTRACT_DRIFT` until V5 roles/procedure invocation, workflow hashes and tests are revised and re-hashed. No V6 runtime/start may proceed against the conflicting V5 hash.
6. **Workflow/application contract:** n8n obtains work only through narrow claim procedure, stores no execution payload and enqueues only by opaque work/idempotency key. Arbitrary HTTP/Code/custom/community nodes and active Telegram Trigger are forbidden in real-dev.
7. **Evidence/repository:** implementation/tests/evidence must bind exact plan, candidate, SQL, bridge source/image, fixture set, arm and environment. This draft neither writes the project repo nor claims a runtime result.
8. **Operability:** global `lab` grammar may rename wrappers but cannot weaken phase arms, RC meaning, cap or emergency postconditions.

Conflict resolution with plan v1:

- v1 preference for n8n Telegram node is rejected for real-dev because it bypasses one cap/route/error ledger. Only bridge/outbox sender is allowed.
- v1 `2xx` acknowledgement is replaced by authenticated durable structured ACK.
- v1 per-update offset becomes highest-contiguous terminal prefix.
- v1 generic exponential backoff becomes the method/error matrix in §10.
- v1 «allowlisted user/chat IDs» becomes exact five-part tuple.
- v1 «budget meter before/after» becomes atomic Telegram and separate DeepSeek ledgers.

## 19. Residual risks and STOP triggers

Residual risks:

1. Telegram provides no general idempotency key for `sendMessage`; an ambiguous timeout cannot be resolved deterministically. V6 counts it and does not retry.
2. A poller outside the governed local environment can ignore the lease. Provider conflict detection disarms but cannot prevent the first conflict.
3. Destination control ultimately depends on V4/Docker Desktop networking and current provider address behavior. If exact enforcement cannot be proved, real-dev remains `BLOCKED_V6_DESTINATION`; broad Internet egress is not silently accepted.
4. PostgreSQL commit durability, Windows/VHDX at-rest remnants and crash semantics depend on V3/V5 runtime qualification.
5. HMAC keys and control-plane principals are inside the approved local Docker/Windows trust boundary; an approved Docker administrator can extract runtime data.
6. Provider schema/pricing/API behavior may drift. Drift invalidates source/runtime/arm locks and blocks calls; this document does not assert current provider facts.
7. Retention purge cannot guarantee secure erase from SSD/VHDX/pagefile/backups. Owner receives residual-copy inventory.
8. Real owner tests may disclose test text to Telegram/DeepSeek providers. Default remains synthetic and DeepSeek is separately disarmed.

Immediate STOP/disarm triggers include: identity mismatch; production deny match; arm missing/expired/drifted; host reboot/daemon drift; webhook postcondition drift; lease/fence loss; polling conflict; malformed identity/offset/ledger; unauthorized route; cap exhausted/unknown; unknown Telegram error; ambiguous send; secret/PII in prohibited sink; direct n8n Telegram/DeepSeek path; destination-control failure; backup generation mismatch; emergency stop not fully verified; any requested plan B/VPS action.

## 20. Implementation order and Definition of Done V6

Sequential implementation after full plan v2 owner approval and relevant repo-write/acquisition gates:

1. freeze V1–V6 hashes, global status/RC schema and exact V4/V5 interfaces;
2. implement pure offline schemas, canonicalization, state machines, classifier and mocks; run negative fixture matrices with no secrets/network;
3. implement checksummed `bridge` schema/procedures, grants and transactional fault tests on synthetic data;
4. implement bridge/proxy images through V2 supply lock; prove no direct n8n provider route and zero external mock/dry state;
5. execute owner identity/probe/webhook ceremony only after V1–V5 readiness and exact arms;
6. run bounded real Telegram test with cap 20, including restart/conflict/rate-limit/ambiguous fixtures primarily against mocks and only minimal approved live messages;
7. optionally execute separate DeepSeek spike only under `MG-V6-DEEPSEEK`;
8. quiesce/backup/cold restore and prove restored real state starts disarmed/no-egress;
9. owner performs black-box normal and emergency workflows;
10. publish redacted EV-V6 records and obtain independent review of exact implementation.

V6 is design-ready for integration only when:

- every finding in §17 retains at least one contract, AT, NC and EV mapping;
- V4/V5 exact interfaces are integrated by hash without weakening one outbound path, cap or role boundary;
- no API exists before a matching arm phase;
- production bot, unknown identity, mixed tuple and untrusted route fail closed;
- highest-contiguous offset, durable ACK, idempotent inbox/outbox and ambiguous send semantics are unambiguous;
- all real sends share one persistent atomic cap of 20;
- DeepSeek uses a separate exact cost authorization;
- dry-run/mock external-effect claims have future executable evidence obligations;
- emergency behavior never reports verified stop without proof;
- formatting is UTF-8 without BOM, LF only, exactly one final LF;
- no line in this document is interpreted as runtime PASS or execution authorization.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[02_V1_WINDOWS_CONTROL_PLANE]]
- [[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]
- [[04_V3_RESOURCE_STORAGE_BOUNDARY]]
- [[05_V4_ISOLATION_NETWORK_EXPOSURE]]
- [[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]
