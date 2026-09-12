---
id: "plan-n8nagents-docker-desktop-lab-v2-20260827"
тип: "задача"
статус: "черновик"
проект: "AgentSystem"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[00_FINDINGS_BASELINE]]"
  - "[[12_CROSS_DOMAIN_INTEGRATION_DECISIONS]]"
доказательства: []
теги: ["n8nagents", "docker-desktop", "plan-v2", "draft-prefreeze", "a-only"]
---

# Полный план локальной лаборатории Docker Desktop для N8NAgents — v2

## P00 — статус, назначение и запрет на исполнение

Состояние документа: `DRAFT_PREFREEZE`. Это design-only план для повторного независимого ревью. Он не является разрешением на загрузку, установку, включение Windows features, UAC, reboot, запуск Docker, изменение project repository, ввод секретов, Telegram/DeepSeek traffic, расходы, backup, удаление данных или доступ к VPS/provider UI.

Runtime status всех описанных проверок: `NOT_RUN`. Слова `PASS`, `COMPLETE`, `RESTORE_VERIFIED`, `READY` ниже обозначают только будущие критерии; они не утверждают фактический результат.

План исправляет все `114` findings frozen review v1 и все `20` известных cross-domain конфликтов. Нормативная трассировка находится в `07_FINDING_DISPOSITIONS_V2.json`; acceptance, canary и evidence ID определены ровно по одному разу в каталогах `09`–`11`. До freeze все эти файлы являются черновиками и должны изменяться как один набор.

## P01 — исходная задача и целевой результат

Единственный разрешённый путь — **plan A: Docker Desktop на текущем Windows host, Linux containers, штатный WSL 2 backend Docker Desktop, без отдельной Ubuntu/WSL distro**.

После отдельного owner approval и успешного исполнения владелец получает постоянную локальную лабораторию, в которой:

- реальные PostgreSQL и n8n Community запускаются локально в Docker;
- editor n8n доступен только через `127.0.0.1:5678`;
- default `MOCK` работает без внешней сети и реальных секретов;
- отдельный Telegram dev/test bot может работать через локальный long-polling bridge без публичного endpoint;
- `REAL_TG` и опциональный `REAL_TG_DEEPSEEK` включаются только краткоживущими owner arms, имеют allowlisted recipient/data class и атомарные пределы сообщений/расходов;
- агент и владелец используют один versioned PowerShell launcher и одинаковые команды;
- данные PostgreSQL/n8n переживают stop/reboot; backup шифруется, а cold restore проверяется без live volumes и live secret root;
- B2r/O5 запускаются из immutable candidate с двумя независимыми validators и trusted collector;
- владелец способен самостоятельно выполнить start/status/mock/real/disarm/backup/restore/emergency-stop из чистой unelevated PowerShell-сессии.

Production VPS остаётся отдельной целью и не получает ни одной mutation по этому плану.

## P02 — scope, exclusions и authority

### P02-C01 — входит

- read-only Windows/Docker eligibility discovery после отдельного approval;
- установка или квалификация существующего Docker Desktop только после exact source/license/delta gates;
- только Docker Desktop WSL 2 backend и Linux `amd64` containers;
- project-scoped Compose, volumes, networks, images, controls, evidence и encrypted backups;
- mock Telegram/LLM, реальные n8n/PostgreSQL, ограниченный dev Telegram и отдельно разрешённый DeepSeek spike;
- owner onboarding/2FA, workflow import inactive-by-default, backup/cold restore, monitoring/status/doctor, B2r/O5 и black-box handoff.

### P02-C02 — явно исключено

- отдельная Ubuntu/WSL distro, plan B, Hyper-V VM, Windows Sandbox, v86/QEMU;
- VPS/production/remote Docker/provider UI как fallback;
- public Caddy/TLS/DNS/tunnel/webhook exposure;
- Kubernetes, Swarm, Windows containers, Docker socket в project containers;
- production Telegram bot локально;
- broad host mounts, repository/Vault binds, global Docker context changes, implicit `latest`;
- automatic license acceptance, reboot, UAC escalation, firewall/security-policy exclusions;
- автоматическое удаление volumes/backups/keys/VHDX или очистка через broad prune;
- secret/PII в Git, Vault, plan/review/evidence/log/screenshot/clipboard history.

Любая необходимость исключённого пути даёт `G_STOP_SCOPE_EXPANSION`/RC `50` либо scoped `G_BLOCKED_CAPABILITY`/RC `31`; она не создаёт fallback.

## P03 — источники истины и canonicalization

### XD-C01 — integration lock

Каждая future authority, команда, result и evidence bind один `n8nagents.integration-lock/v2`: policy `A_ONLY_DOCKER_DESKTOP_WSL2_BACKEND`, frozen plan hash, section map, canonicalizer registry, global result schema, topology lock и owner-decision policy. Изменение любого компонента требует нового freeze/review; self-update запрещён.

### XD-C02 — единая canonicalization registry

- JSON: RFC 8785 JCS, UTF-8, no BOM;
- YAML: duplicate-rejecting parse, затем JSON/JCS;
- text: UTF-8 no BOM, LF, ровно один final LF;
- binary: opaque bytes;
- file set: length-prefixed `path + bytes + size + SHA-256` с ordinal case-sensitive NFC IDs;
- raw executable/text bytes дополнительно имеют raw SHA-256;
- unknown schema fields rejected, если schema явно не разрешает их.

Две независимые реализации обязаны согласиться на Unicode/numeric/order/EOL/duplicate-key fixtures. Tool identities являются runtime unknown до supply lock.

### XD-C03 — frozen input chain

Design input chain включает immutable v1 bundle целиком, v1 quorum и десять raw review records, baseline/audit `114/114`, domain drafts V1–V10, нормализованный V9 и cross-domain decision record. Каждый файл имеет exact path/bytes/SHA-256 в `13_PRIMARY_SOURCE_LOCK.md`; aggregate строится length-framed из ordinal-отсортированных записей. Silent замена одного input запрещена.

Review subject использует нециклическую двухслойную схему. `content_set_sha256` считается по plan и substantive artifacts, но исключает review schema, run record и manifest. Review schema содержит `const content_set_sha256`. После этого `subject_envelope_sha256` считается по content-set record + review-schema hash + checker-source hashes. Schema требует поле envelope формата SHA-256, а quorum validator сравнивает его с frozen manifest — schema не содержит собственный будущий hash и круг отсутствует. Любое замораживание детерминированно подставляет только документированные `<FREEZE_*>` placeholders, пересчитывает content set один раз, создаёт schema один раз и затем envelope; повторная подстановка запрещена.

Future frozen bundle содержит exact manifest, external anchor, byte-identical plan copy, hash-bound checker sources, команды и полные structured transcripts. Review начинается только после двух независимых mechanical PASS и успешных structural/semantic mutation canaries; это не runtime PASS продукта.

## V01 — Windows и Docker Desktop control plane

### V01-C01 — local endpoint identity

Каждая Docker read или mutation проходит единственный trusted wrapper. Wrapper:

1. очищает/отклоняет `DOCKER_HOST`, `DOCKER_CONTEXT`, TLS/SSH/TCP overrides;
2. указывает explicit approved local Docker Desktop context, не меняя global context;
3. сверяет endpoint class, daemon identity, `Server OS=linux`, Engine/Compose/Desktop/settings tuple, boot/session и project name;
4. повторяет guard непосредственно перед первой mutating API call и после операции;
5. допускает только project `n8nagents-local-v2` и operation allowlist.

Remote/unknown endpoint, drift или unreadable identity блокирует до mutation. Ни одна инструкция не предлагает `docker context use`.

### V01-C02 — eligibility и existing-install branch

Read-only preflight создаёт tri-state record (`KNOWN_SUPPORTED | KNOWN_UNSUPPORTED | UNKNOWN`) для Windows edition/build/architecture, hardware virtualization, WSL/Virtual Machine Platform, WSL kernel/status, policy/App Control/AV, RAM/CPU/disk, filesystem/protection, port 5678, admin/UAC/reboot need и existing Docker/WSL/data/config state.

Ровно одна branch:

- `FRESH_INSTALL_ELIGIBLE`;
- `EXISTING_QUALIFIED_NO_CHANGE`;
- `EXISTING_UPGRADE_REVIEW_REQUIRED`;
- `BLOCKED_EXISTING_OR_UNKNOWN`.

Partial install, alternate engine/root, unknown ownership, stopped legacy state или contradictory inventory никогда не ремонтируются автоматически.

### V01-C03 — Windows delta, UAC и reboot

Каждая feature/install change имеет отдельный hash-bound delta record: executable, args, touchset, expected before/after, vendor rollback limits, elevation principal и exact owner gate. UAC относится к одной immediate action. Reboot выполняет владелец вручную после checkpoint; новый boot/session требует read-only resume и нового gate. Cancel/no answer оставляет zero mutation. Автоматический reboot/resume запрещён.

Обычные lab-команды работают только от intended unelevated owner. Elevated daily session блокируется.

### V01-C04 — install/upgrade/recovery semantics

Application uninstall, Windows feature rollback и data recovery — три разные операции. План не обещает byte-identical rollback Docker Desktop. До upgrade обязательны current/LKG locks, backup и restore proof; schema/data migration запрещает image-only downgrade. Vendor uninstall/feature disable/data deletion всегда отдельные owner/destructive gates.

## V02 — supply chain, лицензии и drift

### V02-C01 — discovery lock, acquisition lock, runtime lock

Supply chain имеет три фазы:

1. metadata-only discovery с owner-approved origins/redirect/byte ceilings;
2. acquisition lock: exact version/platform/origin/final URL/hash/signature chain/timestamp/revocation result/bytes;
3. runtime lock: installed identity, OCI manifest-list + `linux/amd64` leaf digests, config/layers, Compose/tool hashes, SBOM, scan DB age/policy, licenses and obligations.

Downloaded installer помещается в private non-reparse staging, открывается handle-safe, проверяется SHA-256 и Authenticode publisher/chain/EKU/timestamp/revocation до execution и повторно через тот же file identity. Mismatch/unknown revocation blocks; suspect bytes quarantine/delete only via exact gate.

### V02-C02 — OCI/build provenance

Все images referenced by digest; platform leaf identity обязательно совпадает. Custom bridge/mock/egress/collector images строятся hermetically из exact context/BOM/base leaf, без network after fetch, без floating package indexes. Build output должен воспроизводиться двумя независимыми builds либо иметь documented deterministic exception that blocks release claims.

### V02-C03 — license, SBOM, vulnerability and source evidence

Docker Desktop, n8n и third-party licenses принимаются владельцем по exact revision/applicability. Automation terms не принимает. SBOM покрывает image config/layers и custom artifacts. Critical/high scanner results, stale/unavailable DB или unresolved license требуют explicit disposition; неизвестность не становится PASS.

### V02-C04 — drift/update/LKG

Перед каждым start wrapper сравнивает qualified tuple с runtime lock. Drift даёт block, не auto-update. Update — отдельная transaction: metadata/acquisition/runtime locks, backup/cold restore, migration rehearsal, rollback decision. Сохраняются current и last-known-good artifacts до отдельного retirement gate; offline import proof не равен runtime compatibility.

## V03 — ресурсы, storage roots и data boundary

### V03-C01 — roots, path and ACL qualification

Логические roots: `LAB_CONTROL_ROOT`, `LAB_SECRET_ROOT`, `LAB_EVIDENCE_ROOT`, `LAB_BACKUP_ROOT`, `LAB_DOWNLOAD_STAGE_ROOT`, `LAB_CIPHERTEXT_STAGE_ROOT`, `LAB_QUARANTINE_ROOT`, `LAB_TEMP_ROOT`, Docker managed root/VHDX и owner key custody. Exact paths определяются только preflight, не захардкожены в plan.

Каждый host root должен быть fixed local volume, canonical handle-resolved path без junction/reparse/symlink/hardlink/ADS/case/NFC alias, sync/share/network/removable semantics и overlap с repository/Vault/другими roots. DACL допускает только intended owner, SYSTEM и отдельно owner-approved Docker principals; inheritance/effective principals фиксируются. Identity повторно проверяется перед/после write для защиты от TOCTOU.

### V03-C02 — data map and at-rest limits

Authoritative persistent classes: project-scoped named volumes `local_postgres_data`, `local_n8n_data`, optional `local_n8n_files`; PostgreSQL bridge schema — единственный durable bridge authority. `local_bridge_state` только recreatable cache без payload. Docker VHDX не является backup. Secret leaves, n8n instance key и age private identity имеют независимую owner custody и не входят в runtime evidence.

Windows/VHDX/pagefile/hiberfil/dumps могут сохранять remnants; secure erase не обещается. Если фактическая protection class не соответствует owner policy, real modes блокируются до informed exact gate. Security control автоматически не изменяется.

### V03-C03 — enforceable resource budget

До install/pull/build/start/backup/restore/update/cleanup рассчитывается per-volume peak: current allocated + non-reclaimable growth + temporary duplicate + rollback/LKG + backup/ciphertext + safety margin. Reclaimable bytes не считаются free. После операции должен сохраняться owner-approved host reserve; unknown forecast blocks.

Compose enforces per-service CPU/RAM/PIDs; PostgreSQL shared memory и Docker Desktop resource envelope измеряются. Docker log rotation: `10 MiB × 3` на container как начальный ceiling. n8n execution payload retention — zero; metadata/log/evidence/cache/backup TTL/caps фиксируются owner policy. Cap pressure предупреждает/блокирует, но не удаляет данные автоматически.

### V03-C04 — cleanup/VHDX

Cleanup двухфазен: read-only exact preview по object IDs/labels/generation → отдельный destructive owner gate → revalidation → exact removal. `docker system prune`, broad volume/image prune и glob deletion запрещены. VHDX compact/relocate/reset — отдельные действия, не repair. Failed/quarantine artifacts не загружаются и не удаляются молча.

## V04 — isolation, network и host exposure

### V04-C01 — privilege envelope and mounts

По умолчанию все containers: nonroot, nonprivileged, `cap_drop: ALL`, no-new-privileges, read-only rootfs, bounded tmpfs, no Docker socket/devices/host PID/IPC/network, exact project-scoped volumes only. Root/SYS_ADMIN/privileged/backend access запрещены.

Каждый mount присутствует в immutable manifest: source type/exact ID, target, RO/RW, expected owner/mode/filesystem, service/mode/purpose. Windows binds разрешены только из qualified roots. Candidate переносится deterministic pax stream в empty run-scoped named volume через `gate-loader`; `docker cp`, repository/Vault bind и mutable candidate bind запрещены.

Если O5 row требует запрещённую capability, только эта required OFFLINE row получает `OFFLINE_BLOCKED_CAPABILITY`; privilege не расширяется и LAB/LOCAL не объявляются failed автоматически.

### V04-C02 — canonical modes

Machine enum: `STOPPED | MOCK | PREARM_TG | REAL_TG | REAL_TG_DEEPSEEK | BACKUP | RESTORE | GATE`. Любая смена running mode сначала drains to `STOPPED` без удаления volumes. Mixed/stale service set блокирует. `real-dev` допустимо только как human description.

### V04-C03 — canonical services

Long-running: `postgres`, `n8n`, `mock-telegram`, `mock-llm`, `telegram-bridge`, `egress-telegram`, `deepseek-adapter`, `egress-deepseek`.

One-shot/QA: `db-bootstrap`, `db-migrate`, `n8n-volume-init`, `db-secret-apply`, `bridge-key-seed`, `real-arm-guard`, `backup-runner`, `restore-postgres`, `restore-validator`, `gate-loader`, `gate-runner`, `validator-a`, `validator-b`, `evidence-collector`.

Alias `telegram-egress-proxy`, default network и undeclared service запрещены.

### V04-C04 — canonical networks and exact membership

| Network | Class | Eligible members |
|---|---|---|
| `db` | internal data | `postgres`, `n8n`, bounded DB one-shots |
| `mock_tg` | internal synthetic | `n8n`, `mock-telegram` |
| `mock_llm` | internal synthetic | `n8n`, `mock-llm` |
| `telegram_ingress` | internal app ingress | `telegram-bridge`, `n8n` |
| `telegram_proxy` | internal controlled client | `telegram-bridge`, `egress-telegram` |
| `llm_ingress` | internal app ingress | `n8n`, `deepseek-adapter` |
| `llm_proxy` | internal controlled client | `deepseek-adapter`, `egress-deepseek` |
| `uplink` | external | active `egress-telegram` and/or `egress-deepseek` only |
| `backup_db` | internal backup | exactly `postgres`, `backup-runner` during `BACKUP` |
| `restore_db` | internal restore | exact restore services only |

`telegram-bridge` never joins `db`; egress services never join application/data networks. `GATE` uses `network_mode:none` and creates no network. Mock internal networks are internal and have runtime no-egress proof.

### V04-C05 — destination egress and loopback exposure

Only egress brokers join `uplink`. Secret-bearing clients reach brokers on internal proxy networks. The broker **does not terminate provider TLS** and holds no application secrets/volumes. Its enforceable boundary is limited to exact destination class: CONNECT/SNI hostname, DNS RRset/address policy, destination IP/port `443`, connection limits and prohibition of generic proxy/redirect destinations. It cannot inspect or attest encrypted HTTP method/path/body.

The narrow secret-bearing client (`telegram-bridge` or `deepseek-adapter`) independently enforces exact HTTPS method/path, closed request schema/body ceiling, response schema/ceiling and `redirect=error` before it opens the broker connection. Telegram and DeepSeek use separate brokers, client policies and tests. Acceptance is split: broker tests destination/SNI/DNS/IP/port bypass; client tests method/path/body/redirect mutation. No TLS interception, substitute CA or decrypted-content logging is permitted. Positive control proves observer ability; negative tests cover DNS/IPv4/IPv6/proxy/redirect/direct-IP/host-gateway paths.

Only `n8n` may publish `127.0.0.1:5678/tcp`. Immediate IPv4+IPv6 pre-bind owner check and post-bind connect/listener/portproxy/firewall observation are mandatory. Conflict blocks; no automatic alternate port.

### V04-C06 — MOCK parity and real-lock separation

`MOCK` runs the **same immutable `telegram-bridge` binary, entrypoint and authenticated envelope implementation** as `REAL_TG`; only a hash-bound provider configuration selects internal `mock-telegram`. It has no uplink and mounts only synthetic non-secret keys/identities. The mock provider implements bounded Telegram response/error fixtures, never accepts a real token and is addressable only on `mock_tg`.

The mandatory matrix covers authorized/unauthorized classification, forged/replayed envelope, crash before/after DB commit, contiguous offset, duplicate/idempotency, immutable route/outbox, atomic 21st-send denial, 409/429/transient/auth errors and disarm. A separate negative canary tries to insert mock endpoint, synthetic key ID, mock bot identity or mock image/config hash into `PREARM_TG`, `ACTIVE_ARM` or `REAL_TG` lock and must stop before provider call/container convergence. Passing MOCK proves functional parity only; it never proves real destination identity.

## V05 — Compose, PostgreSQL и n8n lifecycle

### V05-C01 — deterministic Compose identity

Every invocation uses explicit context, project `n8nagents-local-v2`, exact immutable compose files, mode fragments, env-name allowlist and config hash. Render twice; reject interpolation secrets, unpinned images, defaults, unnamed networks/volumes, extra ports/mounts/services, mixed profiles. No direct `docker compose` is a supported owner path.

### V05-C02 — convergence, health and readiness

From any known state, wrapper inventories objects, drains wrong mode to `STOPPED`, converges exact desired graph, then proves health. Startup order: `postgres` health → `db-bootstrap/db-migrate` → `n8n-volume-init` → `n8n` readiness → mode-specific mocks/bridge/adapters/brokers. Bounds and retries are fixed in runtime lock; exhaustion is FAIL/BLOCKED, never infinite wait.

Stop removes containers/networks/exposure but preserves named volumes. Restart/reboot must not rearm real traffic.

### V05-C03 — PostgreSQL authority and least privilege

Logical areas separate n8n metadata and `n8nagents_app.bridge`. Roles: cluster bootstrap/migrator exact one-shots; n8n metadata runtime limited to its DB; `automation_runtime` has EXECUTE only on enumerated SECURITY DEFINER procedures, no table read/DML/DDL; backup/restore roles exact one-shots. Long-running `bridge_runtime` role is forbidden.

PostgreSQL procedure verifies authenticated bridge envelope and atomically owns lease/fence, terminal observation, contiguous offset, authorized inbox, immutable route, idempotency, outbox, message/cost cap reservations, replay and request/ACK keyring. Every migration is ordered, checksum-bound, idempotent or explicitly one-shot, and separately rehearsed on restored copy.

### V05-C04 — n8n configuration and persistence

n8n image/platform/digest/config keys are runtime-locked. Process runs documented nonroot UID/GID with `local_n8n_data` and optional files volume. `N8N_ENCRYPTION_KEY` is persistent and independently recoverable. DB password/key file support must be proven for exact version; otherwise only reviewed pinned nonroot entrypoint fallback with owner-accepted process-memory residual is allowed.

n8n execution success/error/manual/progress payload retention is zero. Internal workflow relays authenticated envelope transiently, maps exact method/path to exact procedure, and returns MACed ACK unchanged. If exact version cannot prove no raw persistence, bounded relay or supported owner/credential/import behavior, affected real mode is `G_BLOCKED_CAPABILITY`.

### V05-C05 — owner, 2FA, workflows and updates

Owner/2FA setup occurs only through supported loopback UI/CLI for exact n8n version, never SQL/undocumented endpoint. Workflows import inactive, hashes verified; credentials bind through owner ceremony; activation requires exact mode gates. Update begins from `STOPPED`, fresh backup + cold restore, migration rehearsal and new runtime lock; PostgreSQL major upgrade restores into new volume. Old volumes remain untouched until separate destructive decision.

## V06 — Telegram, DeepSeek и message correctness

### V06-C01 — dev identity and two-phase arming

Only separate dev bot is eligible; production deny fingerprint is bound offline. Exactly two Telegram arms exist:

1. `PREARM_TG`, TTL ≤ 5 minutes: permits one `getMe` and one `getWebhookInfo`; no poll/send/delete/start/retry. It produces redacted bot/webhook snapshot and auto-closes.
2. `ACTIVE_ARM`, TTL ≤ 30 minutes: binds successful snapshot, dev bot, five-part tuple `(bot, chat, user, topic, environment)`, synthetic data class, webhook/backlog action, topology/workflow/runtime/secret fingerprints and global cap ≤ 20 Telegram sends. Ordered substates: webhook apply, then poll/send.

No current matching arm means zero provider API calls. Expiry, stop, reboot/session/daemon/config/tuple/token/workflow drift, cap exhaustion, 409 conflict or incident disarms. DeepSeek is never implied by Telegram arm.

### V06-C02 — polling/webhook and single poller

PREARM snapshot informs an explicit owner choice: preserve-and-block or exact one-time `deleteWebhook` with selected backlog disposition. Irreversible backlog drop is a separate gate. Polling begins only after webhook postcondition. A PostgreSQL fenced lease permits one poller across project instances; 409 conflict stops and disarms.

### V06-C03 — classification, authorization and authenticated ingress

Bridge classifies Update before storage. Unsupported/unauthorized input exists only in bounded memory and becomes terminal metadata without raw body/tuple. Authorized input is normalized to closed schema after conjunctive five-part tuple check.

Path: `telegram-bridge -> telegram_ingress -> exact n8n internal workflow -> exact PostgreSQL procedure -> MACed ACK`. Bridge has no DB route/credential; n8n has no MAC keys; arbitrary procedure/parameter map is forbidden. Request and ACK use independent 256-bit keys, timestamp, nonce, fence, bot/arm/tuple and replay verification. ACK occurs only after commit.

### V06-C04 — durable offset, idempotency, route and outbox

Highest contiguous terminal offset advances only transactionally. Crash-before/after-commit, duplicate update and retry cannot create duplicate accepted work. Reply route is immutable from authorized input; LLM/workflow cannot choose recipient. All Telegram sends pass one durable outbox/reservation/cap ledger and one `telegram-bridge -> egress-telegram` path. 21st send is denied atomically.

Provider errors are classified: transient bounded backoff with Retry-After; auth/identity/config/cap/409 are terminal stop/disarm classes. Exactly-once is not claimed; bounded effectively-once cases are demonstrated.

### V06-C05 — DeepSeek

DeepSeek requires separate owner decision for exact model/version alias resolution, official pricing revision/time/currency, input/output token worst-case unit prices, request cap, USD cap, data class, identity/config hashes and TTL. Only `deepseek-adapter -> egress-deepseek` can call it. Telegram mode without DeepSeek never creates these services. Tool access remains enumerated procedures only; no generic SQL/shell/filesystem/HTTP/Docker/admin.

PostgreSQL is the sole durable cost authority. Before every request, one transaction locks the active DeepSeek ledger, validates arm/model/price/currency/data class, computes worst-case cost from maximum input + maximum output tokens plus provider rounding, and reserves that amount atomically against both request and USD ceilings. No reservation means no network request. Concurrent callers serialize on the ledger; retries reuse the same pseudonymous correlation/idempotency key and cannot reserve twice.

Success settles actual metered usage and releases only the unused reserve. Timeout/disconnect/ambiguous provider result remains `AMBIGUOUS_CONSUMED`: the worst-case reserve stays consumed and automatic retry is forbidden. A bounded owner-visible reconcile may use only valid provider usage evidence bound to the same pseudonymous correlation; absent/contradictory evidence never releases reserve. Price/model/currency drift expires the arm. Near-ceiling concurrent tests prove exactly one admissible request, exact deny beyond either cap, retry idempotency and ambiguous-consumed behavior without exposing prompt, key or raw recipient.

### V06-C06 — privacy retention

Authorized protected inbox/outbox payload expires no later than terminal + 24 h; shorter owner policy wins. Unauthorized raw never persists. Logs/evidence/status exclude content and raw IDs. Backup default is zero payload rows; nonterminal/unexpired payload blocks backup and does not auto-delete.

## V07 — secrets, privacy и incident response

### V07-C01 — control-plane trust and secret registry

Before secret creation, actual Windows/Docker effective principals, ACLs, root identity, process exposure and at-rest class must be owner-approved. Authoritative registry contains slot ID, independent key ID/fingerprint, producer, exact consumers, source leaf, container target, transport, rotation/revocation, backup disposition and leak canaries — never the value.

No shared `.env`, Compose interpolation secret, argv secret, shared directory mount or generic `_FILE` assumption.

### V07-C02 — exact transport matrix

| Slot | Consumer | Transport |
|---|---|---|
| Telegram dev token | `telegram-bridge` | owner-only leaf → RO `/run/secrets/telegram_token`, direct file API |
| DeepSeek API key | `deepseek-adapter` only | owner-only leaf → RO `/run/secrets/deepseek_api_key`, direct file API; never n8n/bridge/broker |
| request MAC key | bridge + `bridge-key-seed` | independent leaf/file; seed to protected PG keyring |
| ACK MAC key | bridge + `bridge-key-seed` | different independent leaf/file; no reuse/implicit derivation |
| `automation_runtime` password | n8n encrypted Credential | password-manager + masked DB set/rotate + loopback UI binding; no runtime file/env mount |
| n8n metadata DB password | n8n | exact native file option if proven, else reviewed nonroot entrypoint fallback |
| `N8N_ENCRYPTION_KEY` | n8n | separate persistent leaf + independent owner recovery custody |
| admin/migrator/backup/restore secrets | exact one-shots | individual time-bounded leaves, absent afterward |
| n8n owner/2FA/recovery | owner/browser | no lab file, agent, script, SQL, screenshot or evidence |
| age X25519 private identity | owner/verifier/restore only | per-operation file; never application/capture staging |

Secret files are created atomically with restrictive ACL before value write, mounted as exact leaves, removed from consumer after operation where applicable, and scanned via synthetic markers. Clipboard is prohibited unless separately owner-approved after history/residual review.

### V07-C03 — PII/log/evidence/support policy

Source-side structured allowlist precedes sinks. Redaction-after-log is insufficient. Ordinary evidence contains hashes, counts, enums, keyed pseudonyms and result refs only. Screenshots are exceptional, source allowlisted and scanned; support bundle is incident-only, encrypted at creation, never automatically uploaded, with explicit retention/deletion gate.

### V07-C04 — incident state machine

Leak suspicion or unverified emergency opens incident: host-first disarm marker → stop external effect if possible → preserve evidence safely → inventory contaminated copies → revoke provider tokens → rotate request/ACK/DB/n8n/backup identities in dependency order → rebuild affected runtime/ciphertext → revalidate → owner-authorized resume. Unknown copies or incomplete revoke keep `G_INCIDENT_OPEN`/RC `54`.

## V08 — encrypted backup and independent cold restore

### V08-C01 — recoverable inventory and one epoch

Backup starts only from `STOPPED`, with exact source object identities and exclusive lock. Only `postgres` and nonroot `backup-runner` join `backup_db`; n8n/bridge/mocks/adapters/brokers/migrations/retention/UI writers are absent. Writer/session/generation markers are watched throughout.

Inventory includes all PostgreSQL DBs/globals/roles/grants/extensions/schema history, n8n metadata/workflows/encrypted Credentials, n8n data/files volume or proven ABSENT, and full bridge authoritative schema. Login password verifiers are reseeded; source secret leaves, Telegram/DeepSeek tokens, `N8N_ENCRYPTION_KEY`, automation raw password, age private identity and recreatable cache are excluded. Authorized payload is excluded by default and requires a separate data-backup gate.

### V08-C02 — authenticated streaming capture and publication

PostgreSQL logical capture and normalized read-only volume archives stream directly into authenticated age X25519 encryption; persistent plaintext staging is forbidden. Capture gets only public recipient. Private identity is available only to separately trusted COMPLETE verifier/restore reader. Partial/corrupt/wrong-key artifacts never become selectable.

Publication is same-filesystem atomic rename from unique ciphertext stage to content-addressed generation. Internal manifest binds operation lock, source census, component hashes/sizes, key IDs, tool/runtime/image locks and zero-payload decision. Producer stops at `SEALED_PENDING_COLLECTOR`; only V09 collector may publish `COMPLETE`.

### V08-C03 — cold restore

Restore uses a new run, new empty target volumes/project, `restore_db`, no uplink/host ports/provider secrets/source volumes/live secret root/VHDX. Before first write: authenticate ciphertext+manifest, verify exact key ID, BOM, space, target emptiness/identity and no source reachability. Archive extraction rejects absolute/traversal/link/device/ownership/mode violations.

Restore order: cluster globals/roles without password verifiers → DB/schema/data → reseed logins → n8n volumes → force arms/leases inactive → validate migrations, decrypt representative synthetic Credential with separately supplied n8n key, workflow hashes and bridge invariants. A different collector-sealed run emits `RESTORE_VERIFIED`; failed targets are quarantined and never retried in place.

Mandatory fault matrix covers interrupted stream, writer/session drift, disk full, target collision, wrong/truncated/tampered ciphertext, wrong key, malicious archive, migration failure and source-mount canary. RPO/RTO/retention/backup root/key custody are owner policy. At least two restore-verified generations plus current pre-upgrade generation remain until separate retirement gate.

### V08-C04 — exact backup verifier identity

`backup-verifier` is a pinned one-shot service distinct from `backup-runner`, restore services and `evidence-collector`. It runs documented nonroot UID/GID, `cap_drop: ALL`, no-new-privileges, read-only rootfs, bounded private tmpfs, `network_mode:none`, no host port, Docker socket, device, application/source volume or live secret-root directory. Inputs are exact sealed ciphertext and internal manifest mounted RO plus one per-operation age X25519 private-key leaf mounted RO. Its only writable target is a run-scoped closed result volume.

Verifier authenticates/decrypts to bounded tmpfs or streaming null/manifest parser, checks key ID, AEAD/authentication, component hashes/sizes/BOM and zero forbidden plaintext, then deletes tmpfs/key mount and exits. It emits `backup-verifier-result/v2` containing run/generation/key pseudonym, input hashes, predicate booleans, decision/native status/RC and result hash — never key or plaintext. Collector never sees/mounts the private key and accepts only a closed verifier result whose process/image/input/result identities match the operation lock. Wrong key, tamper, forged result, reused run result, lingering key mount/tmpfs or collector key access prevents `COMPLETE`; teardown is independently observed.

## V09 — candidate, B2r/O5, evidence and Git custody

### V09-C01 — source and private authoring custody

Known source worktree remains dirty and user-owned. Before any future authoring, two independent readers bind HEAD, index, full no-ignore worktree, exact 21-path snapshot, modes/types and `.git` identity. Repository, `.git`, Vault and lab roots are separate physical/write scopes.

Base tree + frozen dirty overlay materialize in a private non-source copy; authoring occurs only there under exact write manifest and transactional journal. Handle-safe writes resist reparse/link/case/NFC/ADS/TOCTOU. Rollback never overwrites concurrent change. Source/Vault invariance is required.

### V09-C02 — immutable candidate and row manifests

Candidate binds base, dirty overlay, authorized edits, file modes/EOL/attributes and actual production runner. Deterministic pax transport and file-set aggregate are separate identities. Sets `66/34/8` are row-by-row immutable manifests with stable row ID, fixture hash, expected status/RC/evidence and requirement scope; set equality is exact.

### V09-C03 — distinct no-network gate processes

Sequential pinned processes: `gate-loader`, `gate-runner`, `validator-a`, `validator-b`, `evidence-collector`. Candidate and inputs are RO except each role's isolated output. All are nonroot/nonprivileged/cap-drop/no-new-privileges/read-only-rootfs, no Docker socket/device/host namespace and `network_mode:none`. Validators have distinct implementation/BOM/process/output identities and cannot cross-read before close. Collector alone emits final result/evidence.

Two independently provisioned clean runs use empty volumes/caches and exact environment/tool/image/kernel fingerprint. Fault tests require external trigger receipt, expected failure and paired positive control. Forged stdout `PASS`, stale output, deleted/duplicate row, validator copy/disagreement, network availability or cleanup failure cannot produce PASS.

Required O5 privileged-equivalent row remains `OFFLINE_BLOCKED_CAPABILITY` under A-only. It is not skipped or manual PASS. B2r and supported O5 rows may still produce their exact scoped results.

### V09-C04 — evidence authority, attempt ledger and delivery

One trusted collector creates exact-set manifest, global result, redaction audit, append-only hash-linked attempt ledger and external anchor. Child/domain status cannot self-seal or improve. LOCAL/OFFLINE records never rewrite exhausted historical REMOTE attempts.

Private isolated Git object DB/index creates exact commit from verified candidate without source hooks/filters/index. Optional integration may create a new dedicated ref by compare-and-swap while leaving checked-out HEAD/index/worktree and 21 dirty paths byte-identical. Branch reconciliation is a later owner gate. Package is generated from verified commit tree and projection-equal to candidate; no worktree packaging.

## V10 — owner CLI, daily operations and recovery UX

### V10-C01 — one launcher and command contract

One signed/hash-locked unelevated launcher `n8na.ps1` resolves approved version root from any cwd and uses the trusted wrapper. It never depends on PATH, current Git checkout, global Docker context or agent chat. Planned stable grammar:

```powershell
n8na.ps1 install-status --json
n8na.ps1 status --json
n8na.ps1 doctor --json
n8na.ps1 plan --operation <id> --json
n8na.ps1 apply --decision <owner-decision-file>
n8na.ps1 start --mode MOCK
n8na.ps1 stop
n8na.ps1 n8n-open
n8na.ps1 secret set --slot telegram-dev-token --stdin --decision <file>
n8na.ps1 secret set --slot deepseek-api-key --stdin --decision <file>
n8na.ps1 secret status --slot <slot> --json
n8na.ps1 secret rotate --slot <slot> --stdin --decision <file>
n8na.ps1 secret revoke --slot <slot> --decision <file>
n8na.ps1 telegram identity-bind --dev-fingerprint <keyed-ref> --prod-deny-fingerprint <keyed-ref> --decision <file>
n8na.ps1 telegram tuple-bind --tuple-file <owner-private-file> --decision <file>
n8na.ps1 telegram webhook-plan --action preserve|delete --backlog preserve|drop --json
n8na.ps1 telegram webhook-apply --decision <file>
n8na.ps1 telegram prearm --decision <file>
n8na.ps1 telegram arm --decision <file>
n8na.ps1 deepseek key-status --json
n8na.ps1 deepseek arm --decision <file>
n8na.ps1 deepseek disarm
n8na.ps1 deepseek reconcile --correlation <keyed-ref> --decision <file>
n8na.ps1 start --mode REAL_TG
n8na.ps1 start --mode REAL_TG_DEEPSEEK --decision <file>
n8na.ps1 disarm
n8na.ps1 emergency-stop
n8na.ps1 backup --decision <file>
n8na.ps1 restore-drill --generation <id> --decision <file>
n8na.ps1 gate --scope B2R|O5 --candidate <id>
n8na.ps1 handoff-check
```

Exact filenames/options may only change before freeze; after freeze they are compatibility API. `install-status`, `status`, `doctor`, `plan` are read-only and side-effect-free, expose tri-state predicates and exactly one `next_safe_action`.

Secret input is accepted only from an owner-opened masked prompt or bounded stdin pipe attached to the intended process; never argv, environment, PowerShell history, transcript, clipboard by default or JSON result. `status` returns presence/keyed fingerprint/consumer/rotation state only. `set`, `rotate` and `revoke` are separate exact owner decisions per slot and atomically disarm dependent real modes before changing the leaf. Offline dev/prod bot fingerprint binding, five-part tuple binding, webhook plan/apply, Telegram PREARM/ACTIVE_ARM, DeepSeek key and DeepSeek arm are distinct decisions; none inherits another.

### V10-C02 — daily owner flow

Mock: start Docker Desktop manually if needed → `status` → `start --mode MOCK` → open loopback n8n → synthetic exchange → structured logs/status → stop. Stop preserves volumes and proves zero host exposure except while approved n8n listener is active.

Real Telegram: complete exact-version owner/2FA and inactive workflow/credential binding → PREARM redacted preview → ACTIVE_ARM → `REAL_TG` bounded test → disarm/stop → inspect counters. The owner can execute identical commands without the agent. DeepSeek requires a separate decision.

Sleep/reboot preparation always disarms/stops real mode. New session detects boot/daemon drift and never repeats installer or restores arm implicitly.

### V10-C03 — emergency stop

Emergency sequence is host-first: atomically publish disarm epoch outside Docker → revoke DB arm/lease via bounded control one-shot if reachable → stop bridge then broker → prove no poll/send/socket/secret mount → preserve volumes/secrets. If Engine/process/network effect cannot be observed stopped, report `G_EMERGENCY_UNVERIFIED`/RC `53` and show BotFather/provider revoke instructions; never claim success from CLI alone.

### V10-C04 — black-box handoff

Owner acceptance occurs from a clean unelevated PowerShell session using only frozen runbook: arbitrary cwd bootstrap, status/doctor, masked secret set/status/rotate/revoke canary, offline dev/prod bot identity binding, tuple binding, webhook plan/apply, mock parity matrix, persistence restart, injected safe fault, emergency stop, Telegram bounded test, separate DeepSeek key/arm/near-cap test when approved, backup, wrong-key/forged-verifier rejection, cold restore and post-reboot resume. No agent coaching during recorded run. Structured evidence precedes screenshots.

## XD — global result, scopes and owner gates

### XD-C04 — global result envelope and RC

Only trusted collector emits numeric RC in `n8nagents.global-operation-result/v2`. Child codes remain namespaced strings (`V06:100`) with schema/status/lock/freshness/evidence. Decisions: `PASS | READY_OWNER_GATE | BLOCKED | FAIL | STOP | NOT_RUN`. Project summary: `READY | PARTIAL_READY | BLOCKED | STOPPED | NOT_EVALUATED`.

| RC | Global status |
|---:|---|
| 0 | `G_PASS_EXACT_REQUESTED_SCOPES` |
| 10 | `G_READY_OWNER_GATE` |
| 20 | `G_NOT_RUN` |
| 30 | `G_BLOCKED_UNKNOWN` |
| 31 | `G_BLOCKED_CAPABILITY` / `G_PARTIAL_READY_OFFLINE_BLOCKED` |
| 32 | `G_BLOCKED_CONTRACT_DRIFT` |
| 33 | `G_BLOCKED_POLICY` |
| 34 | `G_BLOCKED_RESOURCE` |
| 35 | `G_BLOCKED_IDENTITY` |
| 36 | `G_BLOCKED_DEPENDENCY` |
| 37 | `G_BLOCKED_MANUAL` |
| 40 | `G_FAIL_VALIDATION` |
| 41 | `G_FAIL_OPERATION` |
| 42 | `G_FAIL_CONTAINMENT` |
| 43 | `G_FAIL_INTEGRITY` |
| 50 | `G_STOP_SCOPE_EXPANSION` |
| 51 | `G_STOP_SECURITY` |
| 52 | `G_STOP_RESULT_INVALID` |
| 53 | `G_EMERGENCY_UNVERIFIED` |
| 54 | `G_INCIDENT_OPEN` |

Aggregation semantic, never `max(rc)`. Precedence: invalid/stale required child → security → scope expansion → incident → emergency-unverified → containment/integrity/operation/validation → contract/identity/policy/resource/dependency/capability/unknown/manual block → ready gate → not run → PASS. Parent cannot improve child.

### XD-C05 — independent scopes

`LAB`, `LOCAL`, `OFFLINE`, `RESTORE`, `DELIVERY`, `OWNER_HANDOFF` are independently requested/resulted. LAB/LOCAL operation may return RC 0 when exact requested predicates pass while overall project is `PARTIAL_READY`; all-scope/OFFLINE-required claim remains RC 31 if mandatory O5 row is blocked. Нельзя писать общий `SUCCESS` без перечисления requested scopes.

### XD-C06 — owner decision records

`n8nagents.owner-decision-record/v2` binds owner pseudonym, integration lock, exact domain gate IDs, one action, effect classes, artifact/config/identity hashes, TTL/bytes/messages/USD/retries, excluded effects and expiry. One record may satisfy several gates только для одного exact action/effect/hash/expiry; omitted gate never implied. Drift expires decision.

Mandatory distinct owner moments:

1. frozen v2 review outcome and implementation scope;
2. metadata discovery, then acquisition/runtime locks;
3. exact licenses and eligibility;
4. Windows feature/UAC/install delta, each reboot and resume;
5. roots/principals/resources/at-rest residuals;
6. each secret class, n8n key, owner/2FA/workflow reconciliation;
7. Telegram PREARM, ACTIVE_ARM, webhook backlog drop, recipient/data class, optional payload backup;
8. DeepSeek model/price/USD/request decision;
9. backup root/key/RPO/retention and per-run key proof;
10. incident revoke/rotate/resume and support bundle;
11. every material cleanup/key retirement/failed-target deletion/VHDX action;
12. candidate start, optional new-ref integration and package publication;
13. any remote/production action under a new plan.

Plan-wide approval cannot supply secret values, accept unknown license terms, perform UAC/reboot, arm traffic, spend, delete, publish or touch remote systems.

### XD-C07 — immutable child-status mapping

`18_CHILD_STATUS_MAPPING_V2.json` is the only child→global normalization authority. Every domain-native status maps to exactly one global decision/status/RC and semantic class; unknown/duplicate mapping is `G_STOP_RESULT_INVALID`/RC `52`. Each operation declares required and optional child IDs per requested scope. Required `NOT_RUN`, stale or missing child blocks/invalidates per mapping; optional `NOT_RUN` cannot worsen an otherwise exact requested-scope PASS and remains visible.

Owner cancel/no-answer is `READY_OWNER_GATE` + `G_BLOCKED_MANUAL`/RC `37`, `mutation_started=false`, unless no effect was requested and operation is a pure status projection. Multiple failures aggregate by the immutable semantic precedence in XD-C04 and retain every failed predicate. `LAB=PASS, LOCAL=PASS, OFFLINE=BLOCKED_CAPABILITY` gives LAB/LOCAL-only RC `0`, but all-scope/OFFLINE-required RC `31` and `PARTIAL_READY`. Child numeric RC never escapes its namespace.

## P80 — execution sequence after future approval

1. **D0 freeze/re-review:** finalize this integrated set, two mechanical checks/canaries, immutable bundle, independent critical review and owner decision.
2. **D1 read-only preflight:** Windows/Docker/license/resource/root/policy/port/existing-install facts only. Any unknown affecting safety blocks.
3. **D2 supply and install transaction:** official metadata lock → owner license/delta gates → bounded acquisition → verify → UAC install/feature action → manual reboot if needed → read-only resume. No containers/secrets.
4. **D3 Docker qualification:** endpoint, identity, root/ACL/resource, loopback, network, mount, nonroot, volume, signal/cleanup and capability matrix with synthetic data. Unsupported mandatory capability is scoped block.
5. **D4 private implementation/candidate:** source custody, private authoring, schemas/Compose/wrapper/bridge/mocks/migrations/runbook, static tests, candidate and two-validator review. Repository remains unchanged unless later gate.
6. **D5 MOCK:** pull/build from runtime lock; render/topology/no-egress; create project objects; start real PostgreSQL+n8n plus mocks; health, persistence and workflow regression.
7. **D6 owner onboarding:** owner creates n8n account/2FA and binds inactive dev credentials/workflows manually; recovery rehearsed on disposable restore copy.
8. **D7 REAL_TG:** secret ceremony, PREARM, owner webhook decision, ACTIVE_ARM, bounded real dev bot test, atomic cap/disarm/emergency checks. No production token.
9. **D8 optional DeepSeek:** separate source/price/data/cost lock and owner gate; otherwise remains `NOT_RUN` without blocking REAL_TG.
10. **D9 backup/restore:** quiesced encrypted generation, collector COMPLETE, independent cold restore, wrong-key/fault matrix, collector RESTORE_VERIFIED.
11. **D10 B2r/O5:** immutable candidate, 66/34/8 manifests, loader/runner/A/B/collector, two clean no-network runs; honest scoped O5 capability result.
12. **D11 owner black-box handoff:** owner runs frozen runbook from clean session; final result lists each scope separately.

At every phase: `plan` first, exact owner gate where required, revalidation immediately before mutation, evidence seal, bounded retries (no repeated failing branch more than twice), and fail-closed stop.

## P81 — rollback and recovery boundaries

- Preflight/review: no mutation, rollback not applicable.
- Download: exact staged file can be quarantined/removed under exact gate; no broad cleanup.
- Feature/install: vendor-supported recovery only; no false equivalence; data/config preserved.
- Compose start: stop/remove exact containers/networks/exposure, preserve volumes.
- Migration/update: restore into new volumes from verified generation; never overwrite old source/failed target.
- Telegram/DeepSeek: disarm first, stop clients/brokers, revoke/rotate owner-controlled provider secrets when incident requires.
- Backup: partial remains unselectable quarantine; source unchanged.
- Candidate/private authoring: transaction rollback only exact private write set; concurrent/user source work untouched.
- Git: optional new-ref CAS only; no checked-out branch/index/worktree movement.

Automatic rollback is allowed only when exact inverse is preverified, non-destructive, within authority and conflict-free. Otherwise `BLOCKED/INCIDENT` plus owner next action.

## P82 — stop conditions

Stop before next effect on: endpoint/context/daemon/plan/artifact/boot/owner/root/object drift; unknown support/license/revocation/policy/resource; signature/hash/SBOM/license failure; reparse/ACL/TOCTOU/path overlap; unplanned service/network/port/mount/secret/egress; production identity; missing/expired arm; cap/cost mismatch; raw secret/PII in sink; writer/backup generation drift; restore source reachability; validator disagreement/copy; result/evidence/schema inconsistency; outside write set; attempt budget exhaustion; any need for plan B/VPS/privilege expansion/destructive cleanup.

## R2-C01 — typed semantic contracts and evidence

The authoritative correction registry is the exact `114 findings + 15 XD` table in `CorrectionR2/A_SEMANTICS_TOPOLOGY_STATUS.md`. Each source ID expands to one typed acceptance contract, one single-field negative contract and one closed evidence contract. A fixture names a semantic type, closed case set, input/setup hashes, plan/integration/runtime/image/policy locks and secret class. A procedure names an executor, entrypoint hash, ordered bounded steps, positive control, first-effect boundary and cleanup. Free-form “execute source procedure”, generic positive boundaries, prose-only evidence and shared boilerplate contract hashes are invalid.

Every negative contract fixes one JSON pointer, before/after hashes, mutation count `1`, injection phase, exact global decision/status/RC, phase-aware mutation rule and a named forbidden-counter profile. Every evidence object has a closed typed payload, field-addressed predicates, before/after effect counters and an exact forbidden-field set. `mutation_started` is derived from the governed operation counter, never from evidence collection.

`EV-V3-ACL` is `CANONICAL_MULTI_BINDING` to `EV-F-R6-P1-001`, `EV-F-R3-CTRL-005` and `EV-F-R1-WIN-004`, all in the same run. Its payload binds pseudonymous root/ACL/effective-access, Docker-control principals, approved trust and VHDX vendor ACL observation. Unknown daemon principal is `B35`, broad root ACL is `B33`, ACL/effective-access contradiction is `S52`; raw SID/user/path/volume identity is forbidden.

## R2-C02 — closed Telegram HTTP client and same bridge

`telegram-bridge` is the only Telegram token holder and application HTTP client. The non-terminating `egress-telegram` broker enforces only locked destination/CONNECT/SNI/DNS/IP/port; bridge code enforces `POST`, exact state-bound path, closed UTF-8 JSON body, no query/fragment and redirect count zero. Four independent canaries mutate only method, path, body or redirect behavior. Method/path/body mutation is rejected before broker socket and token interpolation; redirect mutation permits exactly the original request, follows no second socket and records the bounded ambiguous/disarm outcome. Every denial is paired with a direct-200 positive control.

MOCK, PREARM and REAL use the same immutable bridge image digest, binary hash, entrypoint path/argv prefix, config schema, HTTP-client lock and ingress-envelope schema. MOCK changes only typed provider profile and mode graph: the bridge joins `mock_tg` and `telegram_ingress`, has no real token, arm, `telegram_proxy` or `uplink`. Any mock-only binary, real-lock contamination, real-to-mock contamination or direct bridge uplink is fail-closed before secret/socket effect where render detects it.

## R2-C03 — executable exact topology

Long-running keys are exactly `postgres`, `n8n`, `mock-telegram`, `mock-llm`, `telegram-bridge`, `egress-telegram`, `deepseek-adapter`, `egress-deepseek`. One-shot keys are exactly `db-bootstrap`, `db-migrate`, `n8n-volume-init`, `db-secret-apply`, `bridge-key-seed`, `real-arm-guard`, `backup-runner`, `backup-verifier`, `restore-postgres`, `restore-validator`, `gate-loader`, `gate-runner`, `validator-a`, `validator-b`, `evidence-collector`. No default service/network, alias helper or privileged initializer exists.

Exact networks and eligible members are: `db` internal for PostgreSQL/n8n and active bounded DB one-shots; `mock_tg` internal for bridge/mock Telegram; `mock_llm` internal for n8n/mock LLM; `telegram_ingress` internal for bridge/n8n; `telegram_proxy` internal for bridge/Telegram broker; `llm_ingress` internal for n8n/DeepSeek adapter; `llm_proxy` internal for adapter/DeepSeek broker; non-internal `uplink` only for active brokers; `backup_db` internal only for PostgreSQL/backup runner during capture; `restore_db` internal only for restore PostgreSQL/validator/restored semantic-check n8n. Bridge never joins `db`; n8n never joins uplink or proxy networks; brokers receive no DB/application/secret/source mounts or networks.

Modes are exact sets: `STOPPED={}`; MOCK/RUN is `{postgres,n8n,mock-telegram,mock-llm,telegram-bridge}`; PREARM is `{telegram-bridge,egress-telegram}`; REAL_TG/RUN is `{postgres,n8n,telegram-bridge,egress-telegram}`; REAL_TG_DEEPSEEK adds `{deepseek-adapter,egress-deepseek}`. Only n8n publishes `127.0.0.1:5678/tcp` in RUN modes. All transitions pass through STOPPED and preserve persistent volumes.

Capture, verify and collect are disjoint one-shot phases. `BACKUP/CAPTURE={postgres,backup-runner}` on `backup_db`; `BACKUP/VERIFY={backup-verifier}` with `network_mode:none`; `BACKUP/COLLECT={evidence-collector}` with `network_mode:none`. RESTORE and GATE phase sets are likewise exact and process-separated. Rendered and observed service/network/edge/mount/secret/port/runtime/volume sets must equal their manifests; subset checks are invalid.

## R2-C04 — backup verifier authority

`backup-runner` receives source volumes read-only, public age recipient and capture-only DB credential; it writes ciphertext staging and never sees the private identity or n8n key. `backup-verifier` receives sealed ciphertext/manifest and a one-file private age identity read-only, has only bounded tmpfs plus a dedicated typed-result output and no network. `evidence-collector` receives only the closed verifier result and public inventory, has no key/network, and alone may publish `COMPLETE` after current identity/hash/exact-set checks.

The state machine is `CAPTURE_OPEN -> CIPHERTEXT_SEALED_PENDING_VERIFIER -> VERIFIED_PENDING_COLLECTOR -> COMPLETE`; failures become `QUARANTINED_INCOMPLETE`, `QUARANTINED_AUTH_FAILED` or `VERIFIED_NOT_COMPLETE`. Wrong key, tamper, mixed generation, stale/forged verifier result, key visibility to producer/collector, verifier NIC, or producer publication authority prevents COMPLETE. No physical secure-erase claim is made.

## R2-C05 — semantic child-status projection

The immutable key set contains exactly 306 ASCII `domain:native_status` entries with ordinal/code-point sorting (identical to UTF-8 byte order for ASCII), `0x0A` separators and one final `0x0A`; culture-aware collation is forbidden. Its set hash is `afd05d828c22c9132b7e00612781c776ddc922ea089c2a61cf14f1921e589c06`. Each record binds source range/excerpt hash, a nonempty semantic assertion, reviewed semantic class, exact global tuple, requested success scope and effect semantics. `default_mutation_started` is removed. Name/regex/numeric-RC inference is forbidden; an unknown or impossible runtime child is `STOP/G_STOP_RESULT_INVALID/52` and never becomes key 307.

Effect policy is `CONST_FALSE`, `CONST_TRUE` or `COUNTER_REQUIRED`. Read-only/status/doctor/dry-run/inventory/render/policy/measurement operations are false. A necessarily crossed first-effect boundary is true. Multiphase outcomes carry a typed before/after counter; missing or contradictory counters are `S52`. `READY_OWNER_GATE/G_READY_OWNER_GATE/10` is distinct from `BLOCKED/G_BLOCKED_MANUAL/37`.

Mandatory overrides include `V04:V4_STOP_UNVERIFIED -> S53/CONST_TRUE`, `V07:INCIDENT_CLOSED -> scoped P0/CONST_TRUE`, and exact V08 failure tuples/effect policies for backup, authentication, plaintext incident, restore, containment, RPO and RTO. `MANUAL_PASS` is never PASS. Required/optional scope, NOT_RUN, owner cancel/no-answer, multi-failure precedence and partial OFFLINE use `18_CHILD_STATUS_MAPPING_V2.json` only.

## R2-C06 — raw review batch, false-GO and custody

Future review input is exactly ten isolated raw files `R1.json`…`R10.json`. Duplicate-key-rejecting parsers validate raw bytes, UTF-8/LF, exact role/review ID, plan/content/subject/manifest identities and exact assessment maps `114/11/15/13`. Caller-supplied `schema_valid`, `go_semantics_valid`, counters, record hashes or aggregate verdict are not authority; validators derive them from raw records. Missing/extra/invalid record invalidates the batch rather than shrinking the denominator.

Aggregate GO requires ten valid records, at least eight GO, zero STOP, zero BLOCKED, zero validated P0, zero consensus P1, zero contradictory GO, exact bindings and unique review IDs/raw hashes. Five or more independently demonstrated false-GO variants must be rejected, including BLOCKED-compatible GO, duplicate ID, duplicate raw hash, role mismatch, foreign subject/manifest, supplied counter mismatch and GO with open/inadequate legacy closure.

Paths are relative NFC `/` paths with no drive/UNC/root/dot/backslash/NUL/colon/ADS/trailing-dot-space/reserved basename. Exact path uniqueness includes NFC/NFD/casefold/Windows comparisons. Actual file set equals allowlist; unexpected files/directories, reparse/symlink/junction, ADS, hardlink, unstable handle identity or out-of-root final path stop validation. Two independent implementations bind plan, input chain, manifest, content set, subject envelope, encoding, checker source and complete transcripts. A/B disagreement is STOP, not quorum input.

The owner-designated master prompt is bound as exact `27410` bytes and SHA-256 `7b271daf6c3952aff905d2358e2e1a3c36ca789e5be784968311e133d1758da3`. Any changed bytes require a new visible owner input decision. The lost original nine-item audit is represented only by the permanent immutable source-loss incident; it is `SOURCE_ASSERTED_NOT_REPLAYED` and a correction summary cannot manufacture its missing claim/evidence bytes. The prospective successor baseline contains exactly thirteen independently reviewable items (`P1-01..P1-08`, `P2-01`, `NEW-P1-01..NEW-P1-04`).

## R2-C07 — non-circular subject and R2 gate

Content identity is a domain-separated, ordinal path-framed SHA-256 over exact plan, input/source records and substantive artifacts. Review/quorum schemas, validator sources, run transcripts, manifest and anchor are excluded from content. Subject envelope is a separate domain-separated hash over content digest plus exact schema/validator source frames. Manifest excludes its own bytes; its external digest belongs only in detached dispatch/anchor metadata. No required self-hash loop is permitted.

R2 prefreeze requires two independent validator PASS results and at least thirty distinct mutation canaries. Required mutations cover typed semantics, `EV-V3-ACL`, HTTP method/path/body/redirect, same bridge/MOCK locks, exact topology, backup key isolation, all status tuple/effect/source fields, plan/input/content/subject/manifest/transcript identities, encoding, raw review exact sets, false GO, path collision/ADS/reparse/hardlink and unexpected files. This remains `DRAFT_PREFREEZE / RUNTIME_NOT_RUN`; freeze, read-only, commit and execution require separate authority.

## R2-C08 — prospective audit supersession, pending owner

The original audit source cannot be reproduced byte-for-byte. `C1_LEGACY_SOURCE_LOSS_INCIDENT.json` is permanent, immutable and remains part of every successor subject. `C2_PREFREEZE_AUDIT_R2_RAW.md` plus its exact attestation define a prospective thirteen-item baseline with exact source spans, per-item hashes and an aggregate hash; they do not retroactively prove the lost nine-item source. `19_PREFREEZE_CORRECTION_R1.json` is a nonauthoritative remediation cross-reference only.

Three isolated reviewers conditionally approved this prospective supersession. Their raw records and attestations are exact inputs, but review approval alone does not activate authority. The candidate state is `PENDING_OWNER_SUPERSESSION`: owner activation must bind the final plan, input set, content set, subject envelope, manifest and decision-set hashes and may change only the audit-authority pointer from the unavailable predecessor to C2. It does not freeze, execute, commit, erase C1, convert runtime `NOT_RUN` into PASS, or authorize Docker/VPS/provider/secrets. Owner rejection or no-answer leaves the predecessor unavailable and the successor pending; it never creates GO.

## P90 — Definition of Done

### P90-C01 — design/freeze DoD

- exactly `114/114` findings bound to immutable source hash/severity/blocking and `DESIGN_RESOLVED` disposition;
- all `84` blocking and `30` nonblocking findings have existing section, acceptance, canary, evidence and semantic reviewer roles;
- consensus clusters `11/11` closed and cross-domain conflicts `20/20` resolved with no union-of-permissions;
- all referenced section/test/canary/evidence IDs unique and catalogued exactly once;
- A-only scope, exact topology/names/modes/global RC/gates/CLI/backup/secrets/supply/evidence/DoD are internally consistent;
- exact local AT/NC/EV alias map covers every token from all domain/XD inputs; unmapped/duplicate/wrong-type alias is rejected;
- immutable child-status map covers every declared native status once, with required/optional scope rules and no RC/status ambiguity;
- two hash-bound independent mechanical validators PASS; at least 30 distinct structural/semantic/custody canaries, including delete/duplicate/severity/blocking/source-hash/missing-section/test/evidence/cluster-omission/wrong-RC/wrong-status/wrong-mutation-started/unmapped-alias/status-duplicate, typed-contract boilerplate, HTTP method/path/body/redirect, topology membership, backup-key exposure, raw-review false-GO, GO-contradiction, path collision/ADS/reparse/hardlink/unexpected-file and transcript/subject drift, all return nonzero;
- raw review schema and both standalone batch validators enforce exact `114/11/15/13` assessment sets and exact isolated R1–R10 slots; all thirteen audit assessments must be `CLOSED/ADEQUATE`, and aggregate GO additionally requires `BLOCKED=0` and derived, not asserted, counters;
- frozen plan/bundle bytes/hashes/manifest/anchor verified before reviewers;
- critical independent review meets its future quorum; owner explicitly decides whether to authorize execution.

### P90-C02 — future LAB/LOCAL DoD

- qualified local Docker Desktop endpoint and resource/storage/control boundary;
- real local PostgreSQL+n8n durable across restart/reboot, loopback-only editor;
- reproducible MOCK with observed no-egress and synthetic end-to-end exchange;
- owner onboarding/2FA and recovery through supported exact-version interfaces;
- bounded dev Telegram PREARM/ACTIVE_ARM test, five-part allowlist, global cap, clean disarm/emergency proof;
- optional DeepSeek only if separately authorized and within ledger;
- encrypted COMPLETE backup and independent RESTORE_VERIFIED cold restore;
- owner black-box run from clean unelevated session;
- no secret/PII leakage and no source/Vault/VPS mutation outside exact later gates.

### P90-C03 — future OFFLINE/delivery DoD

- exact candidate/runner/66-34-8 manifests, distinct validators, two clean runs and trusted evidence seal;
- every required row terminal with no false PASS;
- under current A-only design, privileged-equivalent O5 row is expected to remain honest `OFFLINE_BLOCKED_CAPABILITY` unless a new owner-reviewed architecture is approved;
- therefore this plan does not promise `OFFLINE_READY`, production readiness or VPS deployment.

## P99 — known unknowns and residual risk

Live values intentionally unknown until future gates: Windows/virtualization/WSL/Docker state; exact current official versions/hashes/signers/licenses/prices; host RAM/disk/policy/port; Docker Desktop filesystem/network behavior; exact n8n file-input/relay/owner/2FA/import semantics; PostgreSQL crypto/tool closure; Telegram dev identity/webhook/recipient; DeepSeek model/price; backup destination/retention/key custody; privileged O5 capability.

Trusted Windows/Docker principals can access local container data/secrets. WSL/VHDX/pagefile/SSD may retain remnants. Public DNS/CA/provider APIs remain external dependencies. Hash equality proves bytes, not semantic correctness. A-only intentionally leaves some OFFLINE claims blocked. Все residuals должны быть видимы в owner decision и final scoped result.

## Связи

- [[MOC_N8NAgents]]
- [[N8NAgents]]
- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[12_CROSS_DOMAIN_INTEGRATION_DECISIONS]]
