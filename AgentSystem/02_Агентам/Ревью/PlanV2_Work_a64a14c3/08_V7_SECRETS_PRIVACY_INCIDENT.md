---
id: "n8nagents-plan-v2-v7-secrets-privacy-incident"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V7 secrets/privacy/incident architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "00_FINDINGS_BASELINE.json"
  - "01_BASELINE_AUDIT.json"
  - "02_V1_WINDOWS_CONTROL_PLANE.md"
  - "03_V2_SUPPLY_CHAIN_LICENSE_DRIFT.md"
  - "04_V3_RESOURCE_STORAGE_BOUNDARY.md"
  - "05_V4_ISOLATION_NETWORK_EXPOSURE.md"
  - "06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE.md"
  - "07_V6_TELEGRAM_CORRECTNESS_SECURITY.md"
доказательства: []
теги: ["n8nagents", "plan-v2", "secrets", "privacy", "incident", "n8n", "docker-desktop", "design-only"]
---

# V7 — секреты, privacy и incident response

## 0. Статус, область и запрет на исполнение

Это implementation-ready design-секция будущего полного plan v2. Она не разрешает download, installation, Windows/Docker/VPS mutation, чтение или ввод реальных секретов, Telegram/DeepSeek API, provider UI, изменение project repository, запуск контейнеров, сбор support bundle или расходы. Все фактические principals, ACL, пути, secret-file capabilities, n8n settings, provider credentials, retention jobs и incident actions имеют статус `UNKNOWN` до соответствующих gates и runtime evidence.

V7 владеет:

- фактической Windows/Docker control-plane threat model применительно к секретам;
- реестром secret classes и per-secret lifecycle/transport;
- правилом «один secret — один restricted source file — только named consumers», без общего secret-root mount;
- exact-version `_FILE` qualification и отдельным informed gate для runtime environment fallback;
- идентичностью, custody и restore-связкой постоянного `N8N_ENCRYPTION_KEY`;
- privacy/retention политикой n8n, application data, logs, telemetry и UI artifacts;
- source-side evidence allowlist и fail-closed scanner policy;
- secret-entry ceremony для browser/clipboard/PowerShell/screenshots;
- host-first disarm, emergency stop, incident inventory, revoke/rotate и contaminated-copy handling;
- at-rest residual-risk disclosure.

V7 не владеет Windows endpoint implementation, OCI acquisition, физическим network enforcement, Compose/SQL delivery, Telegram offset/routing/cap semantics, backup writer/restore implementation, repo integration или global owner CLI. Он задаёт обязательные secret/privacy interfaces для этих владельцев. Отсутствующий либо противоречивый внешний interface блокирует real-dev; V7 не объединяет конфликтующие permissions.

## 1. Design inputs, граница findings и выявленный drift

V0 содержит `114/114` findings и audit `PASS`; это доказательство полноты baseline, а не runtime readiness. V7 принимает первичное design-владение всеми `R6-P1-001..010` и `R6-P2-011`. Cross-findings перечислены в §18 и не объявляются закрытыми V7 единолично.

До canonical integration обнаружены следующие конфликты:

| ID | Конфликт | V7 disposition |
|---|---|---|
| `DRIFT-V7-01` | V4 cross-table относит secrets к V6, backup к V7, evidence к V8, repo к V9 и operability к V10. Текущая decomposition выделяет V7 как secrets/privacy/incident. | Старые номера downstream owners не являются authority. Интегратор связывает sections по contract IDs, а не по устаревшему номеру. V7 не принимает backup implementation. |
| `DRIFT-V7-02` | V5 §6.2/§6.3 даёт `telegram-bridge` роль `bridge_runtime` и прямой DB-only path; V6 §§1,5,18 запрещает bridge DB path/credential и требует authenticated internal n8n ingress. | `BLOCKED_CONTRACT_DRIFT`. Никакой union permissions. До выбора одного reviewed path secret `V7-S08` и verifier consumer имеют `UNRESOLVED_CONSUMER`; real bridge не стартует. |
| `DRIFT-V7-03` | V5 residual text считает V6 service key `telegram-egress-proxy`, тогда как V4/V6 закрепляют `egress-telegram` и V6 прямо запрещает alias. | V7 не владеет service key. Secret mount и destination records блокируются до одного canonical V4/V5/V6 service identity. |
| `DRIFT-V7-04` | V5 допускает preferred `_FILE` либо entrypoint export, но не задаёт доказательство поддержки или exposure gate. | Внутри V7 это разрешено §6: никакой generic `_FILE` assumption; env fallback только по `MG-V7-ENV-FALLBACK-<slot>` и с явным `/proc`/process-memory residual. |
| `DRIFT-V7-05` | V3 говорит, что real-dev raw message body не хранится, а V6 разрешает protected inbox/outbox до 24 h. | Privacy authority V7 принимает более точную модель: authorized raw text может существовать только в protected inbox/outbox максимум 24 h; в n8n execution payload — никогда. V3 data map должен быть скорректирован до freeze. |
| `DRIFT-V7-06` | V6 matrix называет `automation_runtime` password одновременно n8n Credential/entrypoint secret. Это разные transport/exposure paths. | До binding выбирается ровно один path. UI-bound encrypted n8n Credential предпочтителен; file/entrypoint path требует отдельного slot и V7-C03 gate. |

Пока `DRIFT-V7-02/03/05/06` не устранены новыми hash-bound interfaces, статус — `BLOCKED_V7_CONTRACT_DRIFT`, RC `132`; runtime secret provisioning запрещён.

## 2. Реестр контрактов V7

| Contract | Обязательство |
|---|---|
| `V7-C01-CONTROL-PLANE-TRUST` | Инвентаризировать реальные Windows/Docker principals и считать Docker Engine control root-equivalent для всех container secrets/data. |
| `V7-C02-PER-SECRET-LIFECYCLE` | У каждого секрета есть issuer, custodian, sole/named consumers, отдельный source, transport, lifetime, rotation и forbidden sinks. |
| `V7-C03-FILE-TRANSPORT` | Один restricted file на secret slot; exact consumer file bind; `_FILE` только после version canary; env fallback — отдельный accepted risk. |
| `V7-C04-N8N-INSTANCE-KEY` | Постоянный `N8N_ENCRYPTION_KEY` генерируется до first boot, имеет non-secret ID, independent custody и DB/backup binding. |
| `V7-C05-N8N-PII-RETENTION` | Exact-version n8n persistence/log/telemetry settings и field-level PII retention доказаны canaries; unknown блокирует real-dev. |
| `V7-C06-SOURCE-ALLOWLIST-EVIDENCE` | Evidence строится source-side только из closed safe schemas; unknown field/artifact/scanner error блокирует публикацию. |
| `V7-C07-DIAGNOSTIC-ATREST` | Raw support/dump не является обычным evidence; support bundle возможен только по incident gate в encrypted quarantine; residual remnants явны. |
| `V7-C08-SECRET-ENTRY-CEREMONY` | Owner вводит secret без argv/chat/Vault/screenshot/history; clipboard path либо запрещён, либо отдельно gated и очищается с contamination accounting. |
| `V7-C09-ATOMIC-DISARM` | Emergency всегда сначала атомарно disarm на host; verified stop требует process/network postconditions; Engine-down никогда не даёт success. |
| `V7-C10-INCIDENT-LIFECYCLE` | Для каждой secret class существуют revoke/rotate/rebind steps и полный contaminated-copy inventory; unknown copy остаётся contaminated. |
| `V7-C11-PRESTORAGE-DESTINATION` | Raw unauthorized data отклоняется до application storage; secret-bearing egress ограничен exact provider path; V4/V6 evidence обязательно. |
| `V7-C12-BACKUP-SECRET-EDGE` | Backup всегда sensitive, без plaintext staging; DB generation связана с n8n key ID и независимым backup-key ID, но raw keys не входят в payload/BOM. |
| `V7-C13-STATUS-GATES` | Stable states/RC/manual gates не допускают общий PASS при secret/privacy/incident unknown или unverified emergency. |

## 3. `V7-C01-CONTROL-PLANE-TRUST` — фактические principals и threat model

### 3.1. Principal classes

Read-only preflight до первого secret write строит `v7_control_plane_principals/v2` по фактическому host:

| Principal class | Потенциальная способность | Требуемое решение |
|---|---|---|
| `OPERATOR_SID` | Читать owner files, запускать Docker client, управлять собственной UI/session | Exact intended daily owner; единственный обычный interactive principal. |
| `ELEVATION_PRINCIPAL` | UAC/admin actions, ownership/ACL takeover | Не является daily owner; если отличается от operator, его profile не получает lab state. Compromise остаётся trusted-boundary risk. |
| `SYSTEM` и approved local Administrators | Читать/перехватывать memory/files, менять ACL, управлять services/WSL | Root-equivalent residual; owner принимает exact redacted trust list. |
| Фактические члены `docker-users` и principals с effective Docker named-pipe/context access | Inspect/exec/copy/create container, mount source files/volumes, извлечь process/file secrets | Каждый обязан быть известен и owner-approved; неизвестный или broad unexpected member блокирует secret-bearing stages. |
| Docker Desktop/WSL service identities и backend processes | Обрабатывают mounts, VHDX, network и container state | Фактические services/process/signers и endpoint ACL связываются с V1/V2 lock; unknown identity блокирует. |
| Approved backup/AV/EDR/index/dump agents | Могут копировать или quarantine sensitive bytes | Policy disposition обязателен; unknown automatic upload/sync/dump coverage блокирует real-dev. |
| Container consumer UID/GID | Читать только exact mounted file и process memory своего service | Nonzero UID/GID, one-file RO mount, no sibling secret, no Docker socket/host root. |
| Неутверждённый standard Windows user/container | Не должен читать source file, использовать Engine или видеть canary | Negative access must fail. |
| Browser/extensions/clipboard/screen-capture tools в operator session | Могут получить provider token/PII до file custody | Не считаются технически изолированными; owner ceremony минимизирует, но compromise session остаётся residual. |

`authorized Docker control principal` означает доверие ко всем secrets/data внутри backend, а не ограниченный доступ к одному project. ACL source files не защищает от principal, способного управлять Engine. Evidence хранит только purpose-keyed SID/service fingerprints, role labels, effective-right classes и approved/blocked decision; raw usernames/SID/paths отсутствуют.

### 3.2. Gate predicate

`V7_CONTROL_PLANE_QUALIFIED` требует одновременно:

1. V1 endpoint record и actual named-pipe effective access inventory совпадают;
2. operator/elevation/SYSTEM/service/group identities не `UNKNOWN`;
3. secret/control roots имеют protected DACL, expected owner, exact ACE и safe ancestors из V3;
4. нет reparse/sync/shared/removable/network root;
5. каждый Engine principal присутствует в `MG-V7-TRUST-BOUNDARY`;
6. owner видит residual: approved admin/SYSTEM/Engine principal может извлечь все runtime secrets.

Unknown, unreadable, conflicting или changed principal даёт RC `121`, mutation count `0` до secret write/mount.

## 4. `V7-C02-PER-SECRET-LIFECYCLE` — authoritative secret registry

Raw values никогда не входят в registry. `key_id`/fingerprint — purpose-separated HMAC через отдельный local control key; plain SHA-256 токена, пароля или малопространственного ID запрещён.

| Slot | Issuer / custodian | Named consumer | Source и transport | Lifetime / rotation owner / forbidden sinks |
|---|---|---|---|---|
| `V7-S01 telegram-dev-token` | BotFather/provider; owner | Только canonical `telegram-bridge` | Один owner-only file; RO mount только `/run/secrets/telegram_token`; bridge читает file API напрямую | До revoke/expiry/identity drift; owner revokes/rotates через trusted provider session. Запрещены n8n Credential, broker, DB, env, URL evidence, CLI. |
| `V7-S02 deepseek-api-key` | Provider portal; owner | Только canonical `deepseek-adapter` | Один owner-only file; RO mount только adapter; direct file read | До revoke/expiry/budget/model drift; owner/provider rotation. Запрещены n8n, bridge, broker, env/render/log. |
| `V7-S03 n8n-instance-key` | Local CSPRNG; owner | Только n8n process | Один persistent restricted file; native exact `_FILE` либо gated n8n entrypoint fallback | Lifetime всей local n8n credential DB; rotation только supported migration либо controlled credential recreation. Запрещены DB raw field, backup payload, logs, evidence. |
| `V7-S04 postgres-cluster-admin-password` | Local CSPRNG; owner | PostgreSQL init и exact admin backup/bootstrap one-shot only | Отдельный file; exact pinned PostgreSQL native password-file contract обязателен; не монтируется runtime services | Rotate after initialization and on incident; admin one-shots get time-scoped mount. Запрещён n8n/bridge/mocks/env. |
| `V7-S05 n8n-runtime-db-password` | Local CSPRNG; DB owner | n8n process | Отдельный file; native n8n file support либо gated n8n entrypoint fallback | Rotate через coordinated DB+n8n credential transaction; old login revoked before close. |
| `V7-S06 app-migrator-password` | Local CSPRNG; DB owner | Exact migration one-shot | Отдельный file, mounted только during migration, then unmounted | Time-bounded; rotate/revoke after migration or incident. Never long-running container. |
| `V7-S07 application-runtime-credentials` | Local CSPRNG; DB owner | Exact n8n credential slots for `app_runtime`, `memory_runtime`, `automation_runtime` | Preferred: owner masked n8n UI -> encrypted credential DB, no host source file. If file/entrypoint path chosen, each role is a separate slot/gate | Rotate per DB role and rebind inactive workflows. Запрещены workflow export, shared env, bridge unless canonical interface explicitly requires it. |
| `V7-S08 bridge-envelope-key` | Local CSPRNG; security owner | Bridge plus exactly one approved verifier provisioning path | Один source file; RO mount only to bridge and time-bounded verifier-seed consumer; never common root. Final consumer unresolved by `DRIFT-V7-02` | Rotate with dual-key bounded transition or full stop/reseed; old verifier disabled after drain. No evidence/n8n workflow node/runtime-role read. |
| `V7-S09 pseudonym-keys` | Local CSPRNG; evidence/privacy owner | Host trusted collector only, one key per purpose (`bot`, `actor`, `route`, `path`, `evidence`) | Каждый purpose — отдельный file; never mounted to application/provider containers | Rotate per evidence epoch; old evidence remains intentionally unlinkable or requires retained key per owner policy. No shared universal pseudonym key. |
| `V7-S10 control-record-MAC-key` | Local CSPRNG; control owner | Host wrapper only | Отдельный file under control-secret root; no container mount | Persistent for current lab-control generation; rotation invalidates arms/checkpoints and requires rebind. |
| `V7-S11 backup-AEAD-key` | Owner/offline custody | Exact backup or restore one-shot | Independently supplied per operation through one restricted ephemeral file; not live secret root; never persistent plaintext stage | Owner-controlled generation/rotation. Old key retained only while corresponding backup generations retained; compromised key contaminates all dependent ciphertext. |
| `V7-S12 owner-password-2FA-recovery` | Owner through n8n UI/authenticator | Owner/browser and upstream-supported n8n auth only | `NO_LAB_FILE`; masked loopback UI/manual authenticator ceremony | Lifetime owner account; recovery/rotation only supported exact-version flow after backup. Запрещены chat, scripts, SQL reset, screenshots/evidence. |

Дополнительный secret class или consumer — scope change. Empty placeholder files не создаются для `NO_LAB_FILE`. Directory bind `LAB_SECRET_ROOT -> container` запрещён; каждый Compose secret source должен ссылаться на один qualified leaf и каждый runtime inspect mount должен совпасть с exact slot/consumer manifest.

## 5. File creation, ACL и mount invariants

Для каждого file slot:

1. V3-qualified fixed local NTFS root, safe ancestors и approved volume identity проверяются до input.
2. Parent создаётся с protected DACL до появления value. Leaf создаётся exclusive под случайным staging name внутри того же parent, с owner-only/SYSTEM policy, link count `1`, no reparse/ADS/sync attributes и bounded expected size.
3. Input записывается один раз, handle flush выполняется до same-volume atomic publish; status никогда не читает/показывает value.
4. Перед Docker create и после inspect повторно сверяются volume/file ID, owner/DACL, link count, size class и unchanged keyed fingerprint. Handle/TOCTOU semantics следуют V4/V3; directory mount и alternate path запрещены.
5. Container target — exact `/run/secrets/<ASCII-slot>`, read-only, non-executable, только named consumer. Sibling service canary access должен завершаться отказом.
6. Absence, zero-length, extra newline where unsupported, owner/mode mismatch, file substitution или fingerprint drift блокирует before application process.
7. Abort до atomic publish удаляет только unpublished exact staging identity. Если cleanup identity не доказана, файл помещается в incident inventory как `POTENTIALLY_CONTAMINATED`; broad delete запрещён.

## 6. `V7-C03-FILE-TRANSPORT` — exact-version `_FILE` и env fallback

Никакой convention `${NAME}_FILE` не считается поддерживаемой по аналогии. Для каждого `(exact child image digest, platform, application version, config key, entrypoint digest)` существует одна запись:

```text
UNQUALIFIED
  -> NATIVE_FILE_VERIFIED
  -> ENTRYPOINT_ENV_RISK_ACCEPTED
  -> BLOCKED_UNSUPPORTED
```

### 6.1. Native-file qualification

V2 предоставляет exact official source/config-schema evidence и immutable image. Canary запускается без real secret:

- уникальный marker существует только в individual source file;
- application достигает semantically verified connection/decryption behavior;
- Compose render и Engine `Config.Env` не содержат marker;
- main/child process environment не содержит marker, а содержит максимум approved file path name;
- marker отсутствует в sibling filesystems, writable layers, `/proc/*/environ`, logs, errors, diagnostics и evidence;
- missing file, wrong owner/mode, extra newline/encoding, changed file after precheck и unsupported key дают nonzero before serving.

Для exact PostgreSQL `17.11-alpine3.24` проверяется только документированный password-file key pinned source; для n8n `2.36.7` отдельно проверяются DB-password и encryption-key file semantics. Эти версии — target inputs, не доказательство поддержки. До source+runtime canary status `UNQUALIFIED`, RC `123`.

### 6.2. Gated environment fallback

Fallback допустим только для `V7-S03` и `V7-S05`, если exact n8n version не имеет verified native file input, а reviewed minimal non-root entrypoint:

1. читает только два named files после permission/size/format checks;
2. не принимает secret через Compose interpolation, CLI, parent host environment или reusable temp;
3. устанавливает exact process environment только внутри container непосредственно перед `exec` n8n;
4. не печатает env и не порождает shell/debug child;
5. имеет V2-pinned source/image digest и negative tests.

Fallback **не устраняет** exposure: secret будет в process memory и `/proc/<n8n-pid>/environ` для sufficiently privileged same-container/Engine principals. До его применения нужен `MG-V7-ENV-FALLBACK-<slot>` с exact version/digest, доказательством native-file failure, named consumer, `/proc` canary, trust-list hash, TTL и owner acceptance. Docker Engine config/Compose render всё равно не может содержать value. Telegram/DeepSeek/bridge/backup/PostgreSQL admin secrets не получают generic env fallback; unsupported native/custom direct-file path блокирует их consumer.

## 7. `V7-C04-N8N-INSTANCE-KEY` — identity, custody и restore

1. До первого n8n boot owner-approved local generator создаёт CSPRNG material не менее `256` bits entropy. Допустимый textual format и exact length подтверждаются source/image canary для n8n `2.36.7`; до этого генерация real key запрещена.
2. `instance_key_id = HMAC-SHA256(V7-S10-or-dedicated-identity-key, purpose || raw-key)`; raw key и plain hash нигде не сохраняются. Смена identity key не меняет n8n key, но требует controlled remapping.
3. Live key file `V7-S03` и independent owner recovery copy находятся в разных custody domains. Agent проверяет только matching keyed ID/presence; raw recovery copy не читает.
4. Empty instance с missing key не запускает n8n: никакой implicit application-generated key. Existing volume/DB требует exact recorded `instance_key_id`; mismatch останавливает до serving.
5. Volume-set identity, n8n image/config lock, credential-store generation и `instance_key_id` образуют один `n8n_key_binding/v2`. Два normal restart обязаны сохранить binding.
6. Backup external catalog и encrypted internal BOM хранят только `instance_key_id`; backup payload не содержит raw `V7-S03`. Cold restore получает DB/volumes, n8n key и backup key независимо. Key ID сверяется до n8n start, затем supported credential decryptability canary проходит без plaintext export/direct metadata SQL.
7. Missing/wrong key, DB/key generation mismatch и corrupt binding дают RC `124`. Rotation raw bytes + restart запрещена. Разрешены только exact-version supported migration с clone/rollback либо остановка, provider/DB credential revocation и controlled recreation всех n8n Credentials.

## 8. `V7-C05-N8N-PII-RETENTION` — exact n8n и application data policy

### 8.1. Exact-version n8n policy

Следующий semantic target из V5 не считается effective до official-source check и runtime fixtures на exact image digest:

| Surface | Required semantic state |
|---|---|
| Diagnostics/telemetry | `N8N_DIAGNOSTICS_ENABLED=false`; version notifications, templates и personalization disabled; все дополнительные outbound telemetry/defaults exact version inventoried. Unknown destination/default blocks. |
| Community/custom packages | Disabled; writable package/node install directories absent/empty. |
| Environment access from nodes | `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`; Code/Execute Command/arbitrary HTTP/custom/community nodes forbidden in real-dev independently. |
| Execution payload success/error | Persistent payload `0`; settings proposed by V5 (`SAVE_ON_SUCCESS=none`, `SAVE_ON_ERROR=none`) must be recognized and effective. |
| Progress/manual/pin data | Progress persistence false; real-data manual execution and pinned/sample data forbidden; manual mock uses synthetic markers only. |
| Execution metadata | Only allowlisted status/timestamps/opaque workflow+work refs; maximum 24 h and 1000 rows unless a stricter exact-version mechanism is required. No raw input/output/error stack. |
| Binary/files data | Real Telegram path accepts no binary/media; binary marker count remains zero. Synthetic mock files expire within 24 h and are separately labelled. |
| Logging | `warn`, console only, Docker cap `10 MiB x 3`; real-dev containers are removed after verified disarm. Raw text/IDs/token URL/header/prompt/error payload are forbidden, not merely time-limited. |
| Browser/UI | No export, download, pin, screenshot or autofill artifact containing real message/identity/credential. |

Unknown/ignored setting, an unexpected outbound telemetry attempt, raw marker in any execution/error/manual path or an unclassified DB/volume field gives `BLOCKED_V7_PRIVACY`, RC `125`. Redaction after collection cannot cure prohibited source persistence.

### 8.2. Field-level retention

| Data class | Allowed protected authority | Maximum retention / deletion rule |
|---|---|---|
| Unauthorized/unsupported raw Update | Process memory only until classifier terminal decision | Request lifetime; no n8n/application DB/LLM/tool/log/evidence. Minimal keyed terminal counter/control offset only. |
| Authorized synthetic incoming text | V6/V5 protected inbox/work rows only | Maximum 24 h after terminal work state; explicit verified purge. |
| Outgoing synthetic reply/chunks | Protected outbox only | Maximum 24 h after terminal send/ambiguous state. |
| Raw bot/chat/user/thread IDs | Protected identity/reply-route authority only | Authorization lifetime plus exact owner-approved recovery window; evidence receives purpose-keyed refs. |
| Offset, update IDs, reason enums | Bridge control authority | Through bot decommission/offset reconciliation and applicable verified backup window; no raw body. |
| Cap/cost/send attempt ledger | Bridge control authority, pseudonymous | 30 days after authorization reconciliation unless owner approves a stricter auditable period; never delete before incident/billing reconcile. |
| n8n execution payload | None | Zero. |
| n8n safe execution metadata | Dedicated n8n DB rows | Maximum 24 h/1000 rows after exact-version qualification. |
| Mock execution/data | Labelled synthetic stores | Maximum 24 h/1000; never mixed with real authority. |
| Docker/application logs | VHDX logging driver only | Current container lifetime, max `10 MiB x 3`; real containers removed after verified disarm; raw PII remains prohibited. |
| Backups containing protected data | Encrypted complete generations only | Governed by V8/V3; a live purge is not full erasure while such generations remain. Residual copies listed. |

Retention operation is content/identity scoped and owner visible. It verifies marker absence across declared DB tables, n8n/binary volumes, logs, browser export roots and selectable backups. It never promises secure erase from SSD/VHDX/pagefile/journal.

## 9. `V7-C06-SOURCE-ALLOWLIST-EVIDENCE`

### 9.1. Source-side collection

Evidence producers never pipe unrestricted output through a regex redactor. Each producer emits one schema-versioned closed object assembled from exact safe fields at the source. Examples: boolean predicate, enum, count, byte size, hash, keyed ref, timestamp, version/digest and stable error class. Raw environment, full `docker inspect`, full `compose config`, provider response, HTTP request/response, DB row, log tail, exception object, URL, path, ID or body is not a permissible source.

Rules:

1. Unknown field, schema version, artifact type, encoding, archive member or binary format rejects the whole artifact; it is never copied to evidence for later inspection.
2. Collector, schema, redaction/allowlist policy and scanner versions/digests are bound to run/plan/runtime identity.
3. Pseudonyms use purpose- and run-scoped HMAC keys. Stable cross-run identity is emitted only when a contract requires it and owner approved that linkage.
4. Scanner is defense-in-depth after source allowlisting. Scanner unavailable, stale, self-test failure, unsupported archive/binary or I/O error yields RC `126`, not PASS.
5. Before real secrets, unique canaries cover file/env, URL path/query, header, nested JSON, text/ID, multiline/base64, CLIXML/PowerShell transcript, Docker JSON log and a synthetic archive. Collector must block every prohibited canary and deliberately unknown schema.
6. Raw streams are not written to stdout/stderr, PowerShell transcript, temp, evidence, browser or clipboard. Safe child output is parsed in memory with strict byte/field bounds and discarded on schema failure; pagefile/memory remnants remain residual.

### 9.2. Sink inventory

Before real-dev every potential sink has `ABSENT | SOURCE_ALLOWLISTED | PROTECTED_AUTHORITY | INCIDENT_ONLY | BLOCKED_UNKNOWN`: console/stdout/stderr, PowerShell history/transcript/CLIXML, Docker logs, container writable layer, `/proc`, PostgreSQL/n8n tables, binary volumes, Windows temp, VHDX, pagefile/hiberfil, WER/crash dumps, antivirus quarantine, search/sync/backup agents, browser download/autofill, clipboard/history, screenshots, evidence, encrypted backup/quarantine and provider-side data. A discovered sink without disposition blocks real-dev.

## 10. `V7-C07-DIAGNOSTIC-ATREST`

### 10.1. Ordinary diagnostics

`status`, `doctor`, `logs --redacted` and routine failure collection may emit only V7-C06 allowlisted artifacts. Raw Docker support bundle, dump, packet payload, unrestricted inspect/config/env, browser export and DB dump are forbidden. The ordinary scanner is not authorized to claim a support bundle safe.

### 10.2. Incident-only support bundle

`MG-V7-SUPPORT-INCIDENT` is required **before creation**, not only before upload. It binds exact incident ID, vendor tool/version, requested artifact classes, source/target identity, at-rest protection, quarantine key ID, maximum bytes/time, disarm state, no-auto-upload policy, retention and owner decision.

Allowed flow:

1. Atomic disarm/emergency containment precedes collection.
2. Vendor tool may write only to an approved encrypted fixed-volume quarantine boundary. If it necessarily creates raw plaintext elsewhere, location/policy is unknown, or automatic upload cannot be disabled, result is RC `130` and bundle is not collected.
3. Artifact is presumed secret/PII-bearing; no ordinary redaction or `SAFE` label. Catalog stores only ciphertext/hash/size/tool/incident refs.
4. External transfer requires a second explicit owner decision after provider secrets are revoked/rotated as applicable. V7 never uploads automatically.
5. Failed/partial artifacts remain exact-target quarantine entries; deletion is a separate V3 custody gate.

### 10.3. At-rest qualification и residuals

Real secrets require V3-qualified encryption/protection for volumes containing secret root, Docker VHDX, backup/quarantine, pagefile/hiberfil and dumps, or an exact expiring owner exception. ACL does not protect offline plaintext media. Even with full-volume encryption, V7 does not promise protection against logged-in compromised operator/admin/SYSTEM, Engine principal, kernel/EDR, browser extension, DMA/session capture or provider-side retention.

Deletion does not prove secure erase from SSD wear-leveling, NTFS journal, VHDX/overlay layers, pagefile, hibernation, crash dumps, antivirus quarantine or external backup/sync. These copies remain `POTENTIALLY_CONTAMINATED` until positively accounted for; an owner may close an incident only with explicit residual acceptance, never by relabelling unknown as clean.

## 11. `V7-C08-SECRET-ENTRY-CEREMONY`

### 11.1. Default owner-only flow

1. Start a clean non-elevated owner session; fixed launcher contains no value/ID. Precheck records only whether transcription/terminal recording, PSReadLine persistence, clipboard history/cloud sync, browser autofill/download and screen capture policies are `SAFE | UNSAFE | UNKNOWN`.
2. Local-generated secrets are written directly by pinned CSPRNG helper into unpublished restricted file; they never traverse clipboard or PowerShell variables.
3. Provider-generated secrets use a pinned masked/non-echo helper that accepts direct keyboard input. The helper displays only slot, present/missing, age and keyed fingerprint after atomic publish.
4. Secret is never supplied in command argument, environment assignment, here-string, pipeline, chat, Vault, editor, Notepad, screenshot or reusable temp file. No `Get-Content`, `echo`, `type`, `docker inspect env` or copy-back confirmation.
5. Abort before publish removes only exact staging identity and emits secret-free status. Ambiguous cleanup opens an incident record and blocks use.
6. Owner separately confirms provider identity and named consumer. Binding occurs only while application workflows are inactive.

PowerShell transcription or terminal recording that cannot be proven safe yields RC `131`. A fixed launcher recorded in history is harmless; secret input must occur in child masked UI and exact canary must prove the raw marker absent from history/transcript/output/process command line/temp.

### 11.2. Clipboard exception

Clipboard is not the default. If provider UI makes manual typing impractical, `MG-V7-CLIPBOARD-PASTE-<slot>` may allow one masked paste after owner sees the exposure: Windows clipboard history/cloud sync, third-party clipboard manager, browser/extensions and remote-session capture may retain it. The helper reads once, publishes the restricted file, zeroes its buffer best-effort, clears the current clipboard and requires owner-visible clearing of clipboard history. If history/sync state is `UNKNOWN`, cannot be cleared, or a screenshot/recording may exist, the slot is marked `POTENTIALLY_CONTAMINATED`; owner must immediately revoke/rotate it before any real use. Clearing clipboard is not evidence of secure erase.

Screenshots are prohibited from token display, masked entry, raw IDs, n8n credential/2FA screens and support artifacts. UI evidence is recreated after values are closed and may show only keyed refs, state enums and counts.

## 12. `V7-C09-ATOMIC-DISARM` — emergency semantics

`lab emergency-stop telegram` and global emergency use one host-first protocol:

1. Acquire the protected single-writer incident lock.
2. Before any Docker/DB call, publish same-volume atomic, MAC-protected `DISARM_REQUESTED` with monotonic epoch, reason class, plan/runtime/arm refs and UTC. A real start/entrypoint rejects any arm whose epoch is not newer than the current disarm record.
3. If canonical DB path is reachable, atomically revoke arm/lease and prevent new send reservations/dispatch. In-flight ambiguous sends remain consumed and recorded.
4. Through V1 guard stop secret-bearing adapters/bridge first, then secretless brokers; remove exact real containers/networks without volumes; verify no poll request, provider socket, outbox dispatch, secret mount, uplink member or real restart policy.
5. Only after all postconditions publish `DISARMED_VERIFIED`, RC `0`. Volumes, secret files, backups and evidence are preserved; no prune/delete/factory reset.

If Docker Engine or DB is unavailable, host marker still blocks future governed starts, but it cannot prove an already-running process stopped or received the marker. Result is `EMERGENCY_V7_UNVERIFIED`, RC `142`, never PASS. Owner follows exact V1 visible quit/stop procedure. If external effect or credential compromise cannot be excluded, owner manually revokes Telegram token and DeepSeek key from a trusted provider session; automation does not need/read the provider value. On next Engine start, real services remain `restart:no`, entrypoint checks disarm epoch before secret mount/API, and read-only verification either closes stop or remains nonzero.

## 13. `V7-C10-INCIDENT-LIFECYCLE`

### 13.1. State machine

```text
DETECTED
  -> DISARM_REQUESTED
  -> EXTERNAL_EFFECT_CONTAINED | EMERGENCY_UNVERIFIED
  -> CREDENTIALS_REVOKED_OR_BLOCKED
  -> COPIES_INVENTORIED
  -> INTERNAL_ROTATION_AND_REBIND
  -> RESTORE_AND_REGRESSION_VERIFIED
  -> OWNER_RESIDUAL_DECISION
  -> INCIDENT_CLOSED
```

No rearm while any prior state is missing, `UNKNOWN` or failed. Incident record contains no raw value: secret slot/key ID, first/last suspected exposure, systems/sinks, provider revoke status, replacement binding, affected backup generations, evidence/quarantine refs and residual decision.

### 13.2. Contaminated-copy inventory

For every affected slot, enumerate: Windows source/staging/temp, clipboard/history/sync, PowerShell/terminal/CLIXML, browser/autofill/download/screenshots, process environment/memory, `/proc`, Docker config/container layer/log/VHDX, PostgreSQL/n8n/binary volumes, backup generations/keys, evidence, WER/dumps/AV quarantine, repository/Vault, provider account and support artifacts.

Each copy is exactly `NOT_APPLICABLE | CONFIRMED_CLEAN | CONFIRMED_CONTAMINATED | POTENTIALLY_CONTAMINATED | UNKNOWN`. `UNKNOWN` is handled as contaminated for containment and blocks `INCIDENT_CLOSED` unless owner accepts a named non-removable residual. Rotation does not sanitize old backups/dumps/pagefile/provider logs.

### 13.3. Revoke/rotate order by class

| Class | Mandatory order |
|---|---|
| Telegram token | Disarm/stop; owner revokes through BotFather/trusted provider path; prove old token unusable under separately armed zero-send check if safe; issue/bind new dev identity; webhook/offset/backlog requalification before real arm. |
| DeepSeek key | Disarm adapter; owner revokes provider key; reconcile cost/request ledger; issue new key; destination/model/pricing/budget re-arm. |
| DB runtime/migrator/admin passwords | Stop consumers/writers; create new credential/role secret; update named consumer while inactive; revoke old login; permission/connection negative canary; backup new generation. |
| Bridge envelope key | Stop bridge and ingress; choose canonical V5/V6 verifier path; bounded dual-key transition only if explicitly designed, otherwise drain and replace both ends atomically; replay/old-key negative canary. |
| Pseudonym/control MAC keys | Freeze evidence/arms; issue purpose-separated replacements; invalidate prior arm/checkpoint records; keep old evidence key only per approved audit policy or accept unlinkability. |
| Backup AEAD key | Stop new backup; revoke future use; classify every generation encrypted under old key; retain old key only for explicitly retained quarantined/recovery generation or destroy generation by exact owner gate. |
| `N8N_ENCRYPTION_KEY` | Never blind-rotate. Use exact-version supported credential migration on clone with rollback, or revoke external/DB credentials and recreate all n8n Credentials under a new instance key/generation. Old DB/backups remain contaminated until retired. |
| Owner password/2FA | Upstream-supported account recovery only after backup; revoke sessions/recovery codes; no SQL shortcut. |

Failed/unknown issuer, revoke, old-credential negative test, binding or restore check gives RC `141/128`. Incident close requires a cold-restore-compatible backup after rotation, full mock regression, minimum approved live test only under a new arm, and owner residual decision.

## 14. `V7-C11-PRESTORAGE-DESTINATION`

V7 consumes, but does not reimplement:

- V6 strict classifier and exact five-part authorization tuple before n8n/application persistence;
- terminal unauthorized/unsupported drop with no raw payload and only keyed aggregate/control state;
- authenticated bounded envelope and durable ACK;
- V4 secret-bearing consumer -> secretless `egress-*` broker -> exact provider origin, with no n8n/PostgreSQL uplink;
- V6 synthetic-data class, Telegram cap 20 and separate DeepSeek gate.

Privacy PASS requires source-side canary proving an unauthorized marker is absent from n8n/PostgreSQL application data, logs, memory/tool/LLM calls, backups and evidence after offset terminal handling. Arbitrary FQDN, direct IP, alternate DNS/port, redirect, sibling origin and workflow/LLM-selected destination must fail through V4. A secret-bearing component with broad egress, unknown canonical service, direct n8n provider route or unresolved V5/V6 bridge path gives RC `129/132`.

## 15. `V7-C12-BACKUP-SECRET-EDGE`

V7 defines only the secret/privacy edge consumed by the backup owner:

1. Every n8n/PostgreSQL backup is sensitive. Authenticated encryption begins before persistent storage; persistent plaintext dump/archive/temp count is zero.
2. `V7-S11` is independently supplied and never stored in ciphertext, live secret root, arguments, environment, logs or catalog.
3. External catalog and encrypted BOM bind backup generation, data/config/image identities, `instance_key_id`, backup recipient/key ID and consistency epoch, never raw keys/token/IDs.
4. `V7-S03` is not included in backup payload. Cold restore obtains it from independent owner custody; live secret root and source VHDX/volumes are inaccessible.
5. Wrong key, bit flip, truncation, BOM/key-ID mismatch fail before target write. Restore starts disarmed, without provider secrets/egress/ports.
6. Backup key rotation does not make prior ciphertext safe after key compromise. Affected generations are quarantined/retired by exact owner gates or remain incident residuals.

Backup algorithm/tool, writer consistency, atomic publication, retention and restore object custody belong to downstream backup owner. Until its contract/hash exists, V7 reports `XDEP_BACKUP_BLOCKED`, not backup PASS.

## 16. `V7-C13-STATUS-GATES` — states, RC и manual decisions

### 16.1. Runtime states

| RC | State | Meaning |
|---:|---|---|
| `0` | `V7_SECRETLESS_CANARY_PASS`, `V7_SECRET_BOUND`, `V7_PRIVACY_QUALIFIED`, `V7_DISARMED_VERIFIED` | Exact scoped postconditions only; never overall project success. |
| `10` | `V7_READY_OWNER_GATE` | Exact owner decision needed; no unauthorized secret/provider mutation. |
| `121` | `BLOCKED_V7_CONTROL_PLANE` | Principal/Engine trust boundary unknown or unapproved. |
| `122` | `BLOCKED_V7_SECRET_PATH` | Path/ACL/file/mount identity invalid or drifted. |
| `123` | `BLOCKED_V7_SECRET_TRANSPORT` | Exact native file support not proven and no valid fallback gate. |
| `124` | `BLOCKED_V7_N8N_KEY` | Missing/wrong/unbound instance key or restore pair. |
| `125` | `BLOCKED_V7_PRIVACY` | n8n setting/data/retention/sink contract unknown or violated. |
| `126` | `BLOCKED_V7_EVIDENCE` | Unknown field/artifact/schema or scanner/collector failure. |
| `127` | `BLOCKED_V7_AT_REST` | Required protection/remnant policy absent and no valid exception. |
| `128` | `BLOCKED_V7_INCIDENT_OPEN` | Contaminated/unknown copy, revoke or residual decision unresolved. |
| `129` | `BLOCKED_V7_DESTINATION` | V4/V6 destination/pre-storage proof absent. |
| `130` | `BLOCKED_V7_SUPPORT_ARTIFACT` | Support/dump collection not safely incident-gated. |
| `131` | `BLOCKED_V7_ENTRY_CEREMONY` | Recording/history/clipboard/screenshot/abort safety not qualified. |
| `132` | `BLOCKED_V7_CONTRACT_DRIFT` | Cross-section consumer/service/retention contract conflicts. |
| `140` | `FAIL_V7_SECRET_OR_PII_LEAK` | Canary/real marker detected in forbidden sink; incident opens automatically. |
| `141` | `FAIL_V7_REVOKE_ROTATE` | Issuer/revoke/old-credential/rebind validation failed. |
| `142` | `EMERGENCY_V7_UNVERIFIED` | Host disarmed but running external effect cannot be proven stopped. |
| `143` | `FAIL_V7_SECRET_IDENTITY_DRIFT` | Secret/key ID changed unexpectedly after binding. |
| `144` | `BLOCKED_V7_EXACT_VERSION` | Exact n8n/PostgreSQL/helper semantics unavailable or changed. |

Unknown status, schema error, missing EV, zero RC with failed/skipped row, child stdout `PASS` or stale plan/runtime/secret identity is `STOP_RESULT_INVALID` in the global caller.

### 16.2. Manual gates

| Gate | Exact owner decision |
|---|---|
| `MG-V7-PLAN` | Frozen full plan/hash and V7 contracts before implementation/runtime. |
| `MG-V7-TRUST-BOUNDARY` | Exact redacted Windows/admin/SYSTEM/Docker control principals and root-equivalent residual. |
| `MG-V7-SECRET-CREATE-<slot>` | Issuer, named consumer, source/transport, lifetime and forbidden sinks; no value. |
| `MG-V7-ENV-FALLBACK-<slot>` | Exact n8n version/image/entrypoint, native-file failure evidence and `/proc` exposure acceptance. |
| `MG-V7-N8N-KEY` | First boot/restore key ID, independent custody and volume/backup binding. |
| `MG-V7-PII-RETENTION` | Exact data class, fields, TTL/caps, backups and non-secure-erase residual. |
| `MG-V7-CLIPBOARD-PASTE-<slot>` | One provider secret paste, clipboard/history/sync residual and immediate cleanup/revoke rule. |
| `MG-V7-ATREST-EXCEPTION` | Exact unprotected volumes/classes, principals/remnants, expiry; synthetic mock only unless real risk explicitly accepted. |
| `MG-V7-SUPPORT-INCIDENT` | One incident artifact before creation; quarantine/no-upload/retention. |
| `MG-V7-INCIDENT-ROTATE-<slot>` | Issuer action, old/new ID, downstream copies, rollback and validation. |
| `MG-V7-INCIDENT-RESUME` | All revoke/rotation/restore/regression evidence and named accepted residuals before new arm. |

Plan approval cannot supply values, accept provider/2FA action, rotate credentials, drop data, collect support bundle, accept at-rest/clipboard residual or resume an open incident implicitly.

## 17. Acceptance tests, negative canaries и evidence catalog

All tests are future obligations. Canary fixtures contain no real credentials/PII. Runtime rows require approved locks/gates. EV artifacts are source-allowlisted, schema-valid and secret-free.

Canonical short ID каждого contract/evidence record — префикс `V7-CNN`/`EV-V7-NN`; descriptive suffix в §2/таблице ниже является его единственным полным label, а не отдельным объектом. Поэтому ссылки `V7-C03` и `V7-C03-FILE-TRANSPORT`, как и `EV-V7-03` и `EV-V7-03-TRANSPORT`, обозначают одну запись.

| Contract | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `V7-C01` | `AT-V7-01`: operator/root/Engine effective-principal inventory matches exact owner trust list; standard user denied. | `NC-V7-01`: unknown group member, broad ACE, alternate endpoint or Engine principal blocks before secret write. | `EV-V7-01-CONTROL-PLANE`: keyed principal refs, rights classes, endpoint/root hashes, decision. |
| `V7-C02` | `AT-V7-02`: every slot has complete issuer/consumer/source/lifetime/rotation graph and only named consumers observe its unique canary. | `NC-V7-02`: extra consumer, shared root mount, common env file, missing issuer/expiry or neighbor canary access blocks. | `EV-V7-02-SECRET-REGISTRY`: slot IDs, keyed fingerprints, lifecycle states and mount refs only. |
| `V7-C03` | `AT-V7-03`: exact native-file canaries for pinned n8n/PostgreSQL/custom images; gated n8n fallback shows only documented process-env exposure. | `NC-V7-03`: unsupported `_FILE`, wrong newline/mode, canary in Compose/Engine env, child/sibling process or ungated fallback -> RC 123/140. | `EV-V7-03-TRANSPORT`: version/image/entrypoint/source refs, visibility matrix, fallback gate ID. |
| `V7-C04` | `AT-V7-04`: first boot, two restarts and cold restore match key/volume/DB/BOM IDs and decrypt canary via supported operation. | `NC-V7-04`: missing/wrong/substituted key, changed identity-key mapping or blind rotation blocks before serving. | `EV-V7-04-N8N-KEY`: key IDs, binding hashes, restart/restore/decryptability outcomes. |
| `V7-C05` | `AT-V7-05`: authorized/unauthorized/success/error/retry/manual/pin/telemetry fixtures match exact DB/volume/log/network retention matrix before/after purge. | `NC-V7-05`: unique raw markers in execution/error/log/binary/browser/backup or unexpected telemetry -> RC 125/140. | `EV-V7-05-PRIVACY`: setting-source/runtime hashes, table/sink counts, TTL/cap/purge outcomes. |
| `V7-C06` | `AT-V7-06`: source producers emit only closed safe schemas; all canary encodings rejected and scanner self-test passes. | `NC-V7-06`: unknown field/schema/archive/binary, disabled scanner, nested/base64/CLIXML marker or raw stdout blocks publication. | `EV-V7-06-EVIDENCE`: producer/schema/scanner hashes, case IDs/counts, no raw excerpts. |
| `V7-C07` | `AT-V7-07`: at-rest/sink policy is complete; ordinary doctor creates no bundle/dump; incident fixture goes only to approved encrypted quarantine. | `NC-V7-07`: unapproved support command, plaintext temp, auto-upload, unknown dump/sync/pagefile state blocks. | `EV-V7-07-DIAGNOSTIC`: protection classes, policy refs, incident gate/quarantine ciphertext refs. |
| `V7-C08` | `AT-V7-08`: owner completes create/bind/abort flows with canary absent from argv/history/transcript/temp/clipboard/browser/evidence. | `NC-V7-08`: active recorder, clipboard history unknown, screenshot fixture, command-line secret or partial readable file blocks and opens incident. | `EV-V7-08-CEREMONY`: safe/unsafe enums, slot/keyed ref, atomic publish/abort result. |
| `V7-C09` | `AT-V7-09`: healthy/hung/unhealthy/DB-down/Engine-down cases disarm host first; only full process/network proof gives RC 0. | `NC-V7-09`: stop fails or Engine unavailable while command claims success; schema rejects and RC 142 remains. | `EV-V7-09-EMERGENCY`: disarm epoch/hash, DB/Docker actions, socket/mount/process postconditions, next action. |
| `V7-C10` | `AT-V7-10`: tabletop for every secret class revokes old canary, binds new, inventories all copies and completes mock/restore regression. | `NC-V7-10`: unknown issuer/copy, usable old credential, blind n8n-key rotation or forgotten backup/support artifact blocks close. | `EV-V7-10-INCIDENT`: slot IDs, state transitions, copy dispositions, revoke/rebind/restore refs, residual decision. |
| `V7-C11` | `AT-V7-11`: unauthorized marker terminal-drops once before storage; allowed provider path passes under arm while every alternate destination fails. | `NC-V7-11`: mixed tuple, forged envelope, direct n8n egress, arbitrary host/IP/redirect or unresolved bridge path blocks. | `EV-V7-11-PRESTORAGE-DEST`: V4/V6 policy hashes, keyed counters, destination class results. |
| `V7-C12` | `AT-V7-12`: interrupted/successful encrypted stream contains marker only in authenticated ciphertext; cold restore receives keys independently. | `NC-V7-12`: plaintext stage, key in BOM/payload/env, wrong key/tamper or live secret-root visibility blocks before target write. | `EV-V7-12-BACKUP-EDGE`: generation/ciphertext/BOM/key IDs and source-inaccessibility refs. |
| `V7-C13` | `AT-V7-13`: golden status fixtures produce deterministic scoped state/RC/gate/one next action. | `NC-V7-13`: zero RC with unknown sink/open incident/unverified emergency/missing EV or stale key ID is rejected. | `EV-V7-13-STATUS`: schema/result hashes, failed predicates, manual gate and next-action IDs. |

## 18. Traceability к V0 findings

`DESIGN_CLOSED` означает только полноту design contract/AT/NC/EV. `XDEP` означает обязательную совместную реализацию и runtime evidence другого owner.

### 18.1. Primary R6 findings

| Finding | V7 contract | AT | NC | EV | Disposition |
|---|---|---|---|---|---|
| `R6-P1-001` | `V7-C01` | `AT-V7-01` | `NC-V7-01` | `EV-V7-01` | `DESIGN_CLOSED`; XDEP V1/V3 runtime principals |
| `R6-P1-002` | `V7-C02`, `V7-C03` | `AT-V7-02/03` | `NC-V7-02/03` | `EV-V7-02/03` | `DESIGN_CLOSED`; exact-version tests pending |
| `R6-P1-003` | `V7-C04` | `AT-V7-04` | `NC-V7-04` | `EV-V7-04` | `DESIGN_CLOSED`; XDEP V5/backup owner |
| `R6-P1-004` | `V7-C11` | `AT-V7-11` | `NC-V7-11` | `EV-V7-11` | `DESIGN_CLOSED_V7_EDGE`; XDEP V6/V5 |
| `R6-P1-005` | `V7-C05` | `AT-V7-05` | `NC-V7-05` | `EV-V7-05` | `DESIGN_CLOSED`; exact n8n runtime pending |
| `R6-P1-006` | `V7-C06`, `V7-C07` | `AT-V7-06/07` | `NC-V7-06/07` | `EV-V7-06/07` | `DESIGN_CLOSED`; evidence owner integration pending |
| `R6-P1-007` | `V7-C07` | `AT-V7-07` | `NC-V7-07` | `EV-V7-07` | `DESIGN_CLOSED_WITH_RESIDUAL`; XDEP V3/V1 observation |
| `R6-P1-008` | `V7-C12` | `AT-V7-12` | `NC-V7-12` | `EV-V7-12` | `DESIGN_CLOSED_V7_EDGE`; backup implementation pending |
| `R6-P1-009` | `V7-C09`, `V7-C10` | `AT-V7-09/10` | `NC-V7-09/10` | `EV-V7-09/10` | `DESIGN_CLOSED`; provider/manual drills pending |
| `R6-P1-010` | `V7-C11` | `AT-V7-11` | `NC-V7-11` | `EV-V7-11` | `DESIGN_CLOSED_V7_EDGE`; XDEP V4/V6 destination proof |
| `R6-P2-011` | `V7-C08` | `AT-V7-08` | `NC-V7-08` | `EV-V7-08` | `DESIGN_CLOSED`; owner canary pending |

### 18.2. Cross-findings materially supported by V7

| Finding | V7 contract | AT | NC | EV | Disposition |
|---|---|---|---|---|---|
| `R1-WIN-004` | `V7-C01` | `AT-V7-01` | `NC-V7-01` | `EV-V7-01` | XDEP V1; secret trust portion |
| `R1-WIN-008` | `V7-C02`, `V7-C07` | `AT-V7-02/07` | `NC-V7-02/07` | `EV-V7-02/07` | XDEP V3; sensitive-root/residual portion |
| `R3-MOUNT-006` | `V7-C02`, `V7-C03` | `AT-V7-02/03` | `NC-V7-02/03` | `EV-V7-02/03` | XDEP V4; individual secret-file mount portion |
| `R3-NET-003` | `V7-C11` | `AT-V7-11` | `NC-V7-11` | `EV-V7-11` | XDEP V4; secret-to-egress portion |
| `R4-F04` | `V7-C03`, `V7-C04`, `V7-C05` | `AT-V7-03/04/05` | `NC-V7-03/04/05` | `EV-V7-03/04/05` | XDEP V5; n8n secret/config portion |
| `R5-F08` | `V7-C11` | `AT-V7-11` | `NC-V7-11` | `EV-V7-11` | XDEP V6; pre-storage privacy only |
| `R5-F15` | `V7-C05` | `AT-V7-05` | `NC-V7-05` | `EV-V7-05` | XDEP V6/V3; privacy authority |
| `R5-F16` | `V7-C08`, `V7-C09`, `V7-C10` | `AT-V7-08/09/10` | `NC-V7-08/09/10` | `EV-V7-08/09/10` | XDEP V6/operability |
| `R7-F04` | `V7-C04`, `V7-C12` | `AT-V7-04/12` | `NC-V7-04/12` | `EV-V7-04/12` | XDEP backup owner; key identity/custody |
| `R7-F05` | `V7-C12` | `AT-V7-12` | `NC-V7-12` | `EV-V7-12` | XDEP backup/supply owners; secret edge |
| `R7-F10` | `V7-C04`, `V7-C12` | `AT-V7-04/12` | `NC-V7-04/12` | `EV-V7-04/12` | XDEP backup owner; independent-key cold restore |
| `R8-P1-010` | `V7-C06` | `AT-V7-06` | `NC-V7-06` | `EV-V7-06` | XDEP evidence owner; privacy schema portion |
| `R9-F10` | `V7-C02`, `V7-C06`, `V7-C08` | `AT-V7-02/06/08` | `NC-V7-02/06/08` | `EV-V7-02/06/08` | XDEP repo owner; pre-secret safeguards |
| `R10-F02` | `V7-C09`, `V7-C10` | `AT-V7-09/10` | `NC-V7-09/10` | `EV-V7-09/10` | XDEP operability; emergency semantics |
| `R10-F03` | `V7-C04`, `V7-C12` | `AT-V7-04/12` | `NC-V7-04/12` | `EV-V7-04/12` | XDEP backup/operability |
| `R10-F06` | `V7-C08`, `V7-C09`, `V7-C10` | `AT-V7-08/09/10` | `NC-V7-08/09/10` | `EV-V7-08/09/10` | XDEP operability; incident handoff |
| `R10-F08` | `V7-C06`, `V7-C13` | `AT-V7-06/13` | `NC-V7-06/13` | `EV-V7-06/13` | XDEP operability; safe diagnostics |
| `R10-F10` | `V7-C06`, `V7-C07`, `V7-C08` | `AT-V7-06/07/08` | `NC-V7-06/07/08` | `EV-V7-06/07/08` | XDEP operability; screenshot/support safety |

## 19. Cross-domain interfaces

| Owner | V7 consumes | V7 provides |
|---|---|---|
| V1 Windows/control plane | Approved local endpoint, exact operator/elevation/SYSTEM/service/group inventory, no global-context drift | Secret-bearing trust-list gate and root-equivalent risk decision |
| V2 supply chain | Exact n8n/PostgreSQL/bridge/adapter/entrypoint/tool digests and official config/source evidence | Required `_FILE`/env canary matrix and secret-free key IDs |
| V3 resources/storage | Qualified roots/ACL/effective principals/at-rest/sink/data-map/retention boundary | Per-secret files/classes, PII TTL and incident/residual inventory requirements |
| V4 isolation/network | Exact file mounts, service identities, no broad bind/socket, destination brokers and emergency process/network proof | Secret-to-consumer and secret-to-egress matrices, disarm prerequisites |
| V5 Compose/PostgreSQL/n8n | Exact service/UID/config/DB-role/credential/migration/key-binding implementation | Required secret slots, n8n settings, fallback gates and privacy canaries |
| V6 Telegram/security | Exact classifier/tuple/envelope/arm/cap/route/offset/egress semantics | Secret custody, provider-key lifecycle, PII/evidence and incident requirements |
| Future backup/recovery owner | Authenticated streaming, cold restore, generation/target/retention contracts | `instance_key_id`, backup-key ID, no-plaintext/no-live-secret-root edge |
| Future evidence/candidate owner | Content-addressed run/candidate/environment manifest and independent collector custody | Source-safe schemas, scanner policy and forbidden artifact classes |
| Future repo/integration owner | Pre-secret `.gitignore`/touchset/ADS/archive scanning and no Vault/repo writes | Secret roots outside repo/Vault and complete slot inventory |
| Future operability owner | Versioned safe CLI, black-box owner runbook and global RC mapping | Entry/disarm/incident ceremonies and stable V7 states |

Stricter contract wins only when permissions are comparable. Для конфликтующих service/consumer/path contracts применяется `BLOCKED_V7_CONTRACT_DRIFT`, а не объединение allowlists.

## 20. Stop conditions

Immediate STOP/BLOCKED before next secret/provider/application mutation:

- unknown/unapproved Docker/Windows control principal or changed endpoint/root/ACL;
- общий secret-root mount, соседний secret visible, secret в Compose/Engine env/argv/log/evidence;
- `_FILE` support assumed without exact source+runtime canary;
- env fallback without exact owner risk gate;
- missing/wrong/drifted n8n instance key or absent independent custody;
- n8n setting ignored/unknown, unexpected telemetry, raw execution/error/manual/binary marker;
- unknown sink, evidence schema/artifact/scanner failure;
- unencrypted/unqualified at-rest path without current exact exception;
- support/dump command without incident gate or with auto-upload/plaintext temp;
- active transcript/recording, unsafe clipboard/screenshot or ambiguous partial secret file;
- emergency stop without verified process/network effect;
- open incident, usable old credential, unknown issuer/copy or blind n8n-key rotation;
- unauthorized raw Update reaches storage/LLM/tools;
- secret-bearing consumer has broad/different egress or cross-contract consumer/service conflict;
- backup contains raw key/plaintext stage or restore sees live secret root;
- any plan B/VPS/production/provider action outside an exact manual gate.

## 21. Residual risks

1. Approved Administrator, SYSTEM, Windows kernel, Docker control principal and compromised operator session can extract runtime secrets despite ACL/file mounts.
2. Gated n8n env fallback exposes `V7-S03/S05` in process memory and `/proc` to sufficiently privileged principals; it is never equivalent to native file use.
3. Full-volume encryption does not protect a logged-in compromised host and does not guarantee deletion from SSD/VHDX/pagefile/journal/dump/quarantine.
4. Browser/extensions, clipboard managers, screen/remote-session capture and provider portals are outside Docker isolation. Ceremony reduces but cannot eliminate this exposure.
5. Provider-side Telegram/DeepSeek request/message/account logs cannot be purged or proven absent by the local plan.
6. A secret-bearing adapter compromised inside its exact provider route can exfiltrate allowed data to that provider; schema, cap and synthetic-only test data limit impact.
7. HMAC verifier key has at least two named consumers if current V6 design is retained. Compromise of either permits envelope forgery until rotation; V5/V6 topology conflict must be resolved first.
8. Backup/key compromise remains transitive to all retained generations. Rotation alone does not repair old ciphertext or copies.
9. `N8N_ENCRYPTION_KEY` loss can make all stored n8n Credentials unrecoverable; blind rotation is prohibited and independent custody remains an owner responsibility.
10. Emergency host marker cannot stop an already-running process when Engine/DB paths are unavailable; manual Docker stop and provider revocation are required.
11. Evidence scanner cannot establish absence in unsupported/opaque artifacts; unknown is blocked, not redacted into PASS.
12. Current design cannot claim runtime compatibility of n8n `2.36.7`, PostgreSQL `17.11-alpine3.24`, `_FILE`, telemetry or retention semantics without future exact-source and runtime evidence.

## 22. Порядок будущей реализации и Definition of Done V7

Sequential order after frozen full plan approval:

1. Resolve `DRIFT-V7-01..06`, freeze service/consumer/DB/retention interfaces and global RC namespace.
2. Implement secret-free schemas, source-side evidence producers, canary registry and incident state machines under repo-write authority.
3. Read-only principal/root/at-rest/sink inventory; owner decides trust/at-rest gates.
4. Acquire exact images/sources/tools via V2 and run secretless `_FILE`, execution, telemetry, evidence and entry-ceremony canaries.
5. Create protected roots and empty slot metadata; no provider secret until every applicable canary PASS.
6. Generate DB/n8n internal secrets, establish n8n key independent custody and prove mock first boot/restarts.
7. Configure n8n owner/2FA and inactive credentials/workflows through owner-only ceremony.
8. Run privacy/retention/error/backup/restore canaries using synthetic values.
9. Only after V4/V5/V6 and all V7 gates bind dev Telegram/optional DeepSeek credentials, execute minimum bounded real test, disarm and purge.
10. Perform emergency/Engine-down and per-secret incident tabletop with canaries, then owner black-box handoff.

V7 design is ready for integration review when:

- all 11 primary R6 findings have contract/AT/NC/EV mapping;
- every file secret has one restricted source and exact named consumers; no directory/common-root mount;
- exact-version `_FILE` tests precede any fallback, and fallback residual is owner-gated;
- n8n key/DB/backup identity and independent custody are unambiguous;
- exact n8n persistence/log/telemetry semantics and PII retention have fail-closed tests;
- evidence is source-allowlisted and scanner/unknown behavior cannot false-PASS;
- support bundle is incident-only before creation;
- secret entry, emergency, engine-unavailable and revoke/rotate procedures are executable without raw values;
- contaminated-copy inventory and at-rest residuals cannot be silently marked clean;
- V4/V5/V6 drift remains blocking until canonical hashes replace it;
- UTF-8 without BOM, LF only and exactly one final LF are verified;
- no runtime, secret, provider, install, repo, VPS or production action is claimed by this document.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[02_V1_WINDOWS_CONTROL_PLANE]]
- [[03_V2_SUPPLY_CHAIN_LICENSE_DRIFT]]
- [[04_V3_RESOURCE_STORAGE_BOUNDARY]]
- [[05_V4_ISOLATION_NETWORK_EXPOSURE]]
- [[06_V5_COMPOSE_POSTGRES_N8N_LIFECYCLE]]
- [[07_V6_TELEGRAM_CORRECTNESS_SECURITY]]
