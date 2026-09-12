---
id: "n8nagents-plan-v2-v10-owner-operability"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V10 owner UX/runbook/recovery architect"
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
  - "08_V7_SECRETS_PRIVACY_INCIDENT.md"
  - "09_V8_BACKUP_COLD_RESTORE.md"
  - "10_V9_CANDIDATE_EVIDENCE_GIT_CUSTODY.md"
доказательства: []
теги: ["n8nagents", "plan-v2", "owner", "operability", "runbook", "recovery", "status", "design-only"]
---

# V10 — эксплуатация владельцем, runbook и recovery UX

## 0. Статус, границы и запрет на исполнение

Это implementation-ready design-секция будущего полного plan v2. Она не разрешает read-only host discovery, download, installation, UAC, Windows feature change, reboot, Docker/Windows/VPS mutation, provider API/UI, ввод или чтение секретов, repository write, запуск контейнеров, расходы, backup, restore или удаление данных.

Ни один launcher, status result, Docker component, n8n owner, 2FA, Telegram bot, backup, recovery key, screenshot workflow или acceptance test фактически не создан и не проверен. Все host/runtime/provider значения имеют состояние `UNKNOWN` до отдельных authorizations и evidence. Термины `PASS`, `READY`, `VERIFIED` ниже определяют будущие predicates, а не текущие факты.

V10 владеет только:

- единым owner-facing CLI и стабильным bootstrap из произвольного каталога;
- human/JSON diagnostic envelope и fail-closed aggregation;
- owner cards для license, Windows features, UAC и reboot/resume;
- ежедневным runbook Docker/n8n/mock/real-dev/backup/stop/sleep/reboot;
- owner-facing n8n owner/2FA onboarding и поддерживаемым recovery без SQL;
- redacted Telegram arming UX и emergency escalation;
- видимостью resources, drift, incident и последнего recoverable backup;
- black-box handoff и owner acceptance без подсказок агента;
- screenshot, clipboard и support-bundle UX policy.

V10 не владеет технической реализацией endpoint, Windows mutation, supply-chain, storage, network, Compose/SQL, Telegram correctness, secret transport, backup cryptography, candidate/evidence или Git. Он не может смягчить их статусы, объединить конфликтующие permissions либо объявить runtime `PASS` по тексту runbook.

План B, отдельный пользовательский WSL-дистрибутив, VM, VPS и production не являются fallback. Недоступная capability даёт scoped `BLOCKED`; V10 показывает причину и одно безопасное действие, но не выбирает другую платформу.

## 1. Целевой owner outcome и непереговорные UX-инварианты

После будущей реализации владелец из обычной неэскалированной PowerShell-сессии должен уметь без знания repository cwd и без помощи агента:

1. определить, установлен ли Docker Desktop и можно ли безопасно продолжать;
2. запустить только approved Docker Desktop и увидеть его readiness;
3. запустить локальный `mock`, открыть n8n только на loopback и выполнить синтетический сценарий;
4. вручную создать n8n owner, включить 2FA и проверить повторный вход;
5. при отдельной необходимости пройти фазовое Telegram arming, один bounded real test и disarm;
6. увидеть ресурсы, drift, текущий режим, arming, health и свежесть backup;
7. получить redacted logs и read-only diagnosis;
8. создать backup по отдельным gates и провести независимый cold restore drill;
9. выполнить emergency stop при healthy и unavailable Docker Engine;
10. безопасно завершить работу перед sleep/reboot и восстановить контекст после нового входа.

Инварианты:

- ежедневный CLI никогда не требует elevation;
- `status`, `install-status`, `doctor`, `logs --redacted`, preview и resume-preflight являются read-only;
- `doctor` не содержит скрытого `fix`, pull, start, repair, cleanup или provider probe;
- любое обязательное `UNKNOWN`, stale evidence, child schema error или contract drift остаётся `UNKNOWN/BLOCKED`, никогда зелёным `PASS`;
- human output и JSON выводятся из одного typed result object; human-текст не может улучшить JSON state/RC;
- каждая blocked/failed команда показывает ровно одно `next_safe_action_id`; дополнительные варианты доступны только по явному `details`, не маскируя основной шаг;
- status никогда не читает secret bytes, не вызывает Telegram/DeepSeek API и не запускает Docker ради диагностики;
- real-dev никогда не восстанавливает arm после stop, sleep, reboot, Docker daemon/session change, TTL, cap или drift;
- штатные stop/recovery операции не удаляют volumes, secrets, backups, evidence или LKG;
- raw token, key, password, 2FA QR/recovery code, user/chat/bot ID, message body, username/SID/raw path и unrestricted logs отсутствуют в stdout, history, JSON и evidence.

## 2. Реестр контрактов V10

| Contract | Обязательство |
|---|---|
| `V10-C01-BOOTSTRAP` | Один stable unelevated launcher работает из любого cwd, проверяет собственную/version-root identity и никогда не полагается на PATH, current Git checkout или global Docker context. |
| `V10-C02-DIAGNOSTIC-ENVELOPE` | `status`, `install-status`, `doctor` имеют один versioned human+JSON contract, tri-state observations, stable states/RC и одно безопасное действие. |
| `V10-C03-OWNER-CARDS` | License, feature, UAC и reboot являются отдельными owner cards с exact delta, abort semantics и hash-bound resume checkpoint. |
| `V10-C04-DAILY-OPERATIONS` | Одностраничный deterministic runbook охватывает Docker start, status, mock, real arm/disarm, logs, backup, stop, sleep и reboot. |
| `V10-C05-N8N-OWNER-2FA` | Exact-version owner/2FA onboarding и recovery выполняются только через supported interface, без SQL, raw screenshots или secret-bearing automation. |
| `V10-C06-TELEGRAM-ARM-UX` | Phase-specific TTL arming показывает redacted identities/caps/data/webhook effect; zero Telegram API до соответствующего V6 phase arm. |
| `V10-C07-EMERGENCY` | Host-first atomic disarm, bounded stop proof и Engine-unavailable/BotFather escalation не допускают ложного success и сохраняют данные. |
| `V10-C08-OPERABILITY-VISIBILITY` | В одном status видны resource reserve, project usage/trend, drift, current mode, arm/cap, health и last COMPLETE/RESTORE_VERIFIED backup. |
| `V10-C09-BLACKBOX-HANDOFF` | Владелец завершает acceptance из чистой PowerShell-сессии только по frozen runbook, без agent prompts/coaching. |
| `V10-C10-EVIDENCE-HYGIENE` | Structured evidence предпочтительно screenshots; clipboard и support bundle требуют отдельной безопасной церемонии. |
| `V10-C11-OWNER-RECOVERY` | Injected fault, emergency stop, backup и cold restore имеют owner-visible fail-closed acceptance и не используют live secret root/source volumes как скрытую зависимость. |
| `V10-C12-CONTRACT-DRIFT` | Несовместимые V4/V5/V6 topology/status interfaces блокируют real-dev и canonical freeze; V10 не разрешает их сам. |

## 3. `V10-C01-BOOTSTRAP` — один launcher из любого cwd

### 3.1. Единственная поддерживаемая точка входа

После будущей approved installation owner использует один command prefix:

```powershell
& "$env:LOCALAPPDATA\N8NAgents\control\lab.cmd" status
```

Это единственная bootstrap-команда. Последнее слово заменяется только documented subcommand/arguments, например `install-status`, `doctor`, `start --mode mock` или `telegram status`. Постоянная правка `PATH`, PowerShell profile, execution policy, aliases и Docker global current context запрещена. `lab.cmd` и все вызываемые scripts не запускаются elevated.

Stable control path определяется V1/V3 root qualification и хранится вне repository/Vault/cloud-sync. Это proposed logical location, не наблюдённый факт. Если фактический approved root иной, owner card показывает один exact абсолютный launcher path; `%LOCALAPPDATA%` не считается разрешением выбрать неqualified root.

### 3.2. Launcher/version-root contract

До dispatch launcher:

1. подтверждает standard non-elevated `INTENDED_DAILY_OWNER`; admin/elevation session даёт `V10_BLOCKED_ELEVATED_DAILY_SESSION`;
2. проверяет own file ID, SHA-256, signer/source lock, DACL, ancestors, reparse/case/Unicode/ADS и approved volume identity;
3. читает только MAC/hash-protected `current-version.json` из control root;
4. разрешает exact version root внутри qualified immutable versions root, проверяет plan/runtime/CLI/tool hashes и запрещает symlink/junction/path escape;
5. запускает exact locked PowerShell executable с `-NoLogo -NoProfile -File <exact-version-root>\lab.ps1`, explicit arguments и fixed working directory внутри version root;
6. очищает/отклоняет `DOCKER_HOST`, `DOCKER_CONTEXT`, `COMPOSE_*`, proxy и path-affecting overrides согласно operation class;
7. печатает CLI version, plan/runtime lock refs, resolved pseudonymous version-root ref и command ID;
8. выполняет V1 explicit local endpoint guard перед каждой Docker operation, не меняя global context.

`current-version.json` нельзя переписывать обычным start/status. Переключение version root — отдельная V2 update promotion с LKG, backup/restore, exact before/after и owner gate. Missing, changed, untrusted or multiple launcher/version roots дают nonzero до child process/Docker mutation.

## 4. `V10-C02-DIAGNOSTIC-ENVELOPE` — status/install-status/doctor

### 4.1. Команды и отсутствие side effects

| Команда | Назначение | Запрещённые side effects |
|---|---|---|
| `lab install-status [--json]` | Windows/WSL/license/existing-install/install transaction/reboot checkpoint | download, launch/repair/install, feature change, UAC, reboot, Docker start |
| `lab status [--json]` | Краткий operational snapshot всех scopes | secret read, provider API/DNS, container/file mutation, implicit refresh/fix |
| `lab doctor [--json]` | Расширенные read-only predicates и evidence freshness | любое `--fix`, pull, start, cleanup, config rewrite, support bundle |
| `lab logs --redacted --since <bounded>` | Только allowlisted structured logs с source-side redaction | raw Docker logs/inspect/env, message bodies, headers, identifiers |
| `lab details <result-id> [--json]` | Explain stable failed predicates/evidence refs | повтор операции, network probe, secret/provider access |

`--json` выдаёт ровно один UTF-8 JSON object в stdout. Human mode использует тот же object и не меняет решение.

### 4.2. Global result schema

```yaml
schema: n8nagents.owner-status/v2
result_id: <uuid>
operation_id: INSTALL_STATUS | STATUS | DOCTOR | LOGS_REDACTED | ...
observed_at_utc: <timestamp>
valid_until_utc: <timestamp>
plan_sha256: <exact-or-null>
authority_ref: <nonsecret-or-null>
cli: {version, launcher_sha256, version_root_ref, lock_state}
operator: {role: INTENDED_DAILY_OWNER | OTHER | UNKNOWN, elevated: true|false|UNKNOWN}
overall: {decision, state, rc}
platform: {windows, wsl, features, pending_reboot, policy}
install: {branch, stage, license, checkpoint, installed_identity}
docker: {desktop, endpoint, daemon, server_os, session_ref}
project: {requested_mode, observed_mode, compose_state, exposure_state}
health: {postgres, n8n, telegram_bridge, mocks}
onboarding: {owner_state, two_factor_state, recovery_lock_state}
telegram: {phase, arm_state, expires_in_seconds, bot_ref, tuple_set_ref,
           webhook_state, sends_consumed, sends_reserved, sends_remaining,
           deepseek_state}
resources: {host_volume_ref, free_bytes, reserve_bytes, projected_peak_bytes,
            vhdx_allocated_bytes, docker_total_bytes, lab_labelled_bytes,
            backup_bytes, db_cap_state, trend_state}
drift: {state, changed_field_ids, update_state, last_qualified_utc}
backup: {last_complete_ref, last_complete_age_seconds,
         last_restore_verified_ref, last_restore_age_seconds,
         freshness_state, custody_state, recovery_tier}
incident: {state, disarm_epoch_ref, provider_revoke_state}
scopes: {LAB, LOCAL, OFFLINE, REMOTE}
observations: {required, known, unknown, stale, contradictory}
child_results: [{domain, schema, state, rc, evidence_refs}]
failed_predicates: [<stable-id>]
manual_gate_id: <exact-or-null>
next_safe_action_id: <exactly-one>
evidence_refs: [<EV-V10-* and validated child refs>]
mutation_started: false
redaction_policy_sha256: <exact>
```

Raw child numeric RC сохраняется только рядом с child string state. Global aggregator использует frozen mapping по string state; совпавшие numeric RC разных domains не считаются эквивалентными. Unknown child schema/status/mapping даёт `V10_STOP_RESULT_INVALID`.

### 4.3. Human contract

Human output стабилен и короток:

```text
[BLOCKED] lab status — real-dev запрещён (RC 201)
Режим: STOPPED    Docker: READY    PostgreSQL/n8n: NOT_RUN
Telegram: DISARMED    Лимит: 0/20    TTL: —
Диск: 61 GiB free / 20 GiB reserve    Тренд: STABLE
Drift: CONTRACT_DRIFT    Backup: RESTORE_VERIFIED 3d ago
Проверено: 2026-...Z; действительно до: 2026-...Z
Следующий безопасный шаг: ACTION_REVIEW_V456_DRIFT
Result ID: ...
```

Поля со значением `UNKNOWN`, `STALE`, `CONTRADICTORY`, `NOT_RUN` не скрываются и не окрашиваются как healthy. Human mode не печатает raw paths/IDs/values; `details` объясняет только stable predicate IDs.

### 4.4. Stable overall states and RC

String state первичен. RC `0` относится только к exact requested read-only/operational scope, не к общему release/production readiness.

| RC | State | Meaning |
|---:|---|---|
| `0` | `V10_STATUS_HEALTHY`, `V10_OPERATION_VERIFIED`, `V10_HANDOFF_PASS` | Все обязательные predicates exact scope доказаны. |
| `10` | `V10_READY_OWNER_GATE` | Требуется один exact manual gate; следующая mutation не началась. |
| `200` | `V10_BLOCKED_UNKNOWN` | Обязательное наблюдение отсутствует, stale, unreadable или contradictory. |
| `201` | `V10_BLOCKED_CONTRACT_DRIFT` | Cross-domain schema/topology/RC interface не канонизирован. |
| `202` | `V10_BLOCKED_BOOTSTRAP` | Launcher/version root/operator identity не exact. |
| `203` | `V10_BLOCKED_INSTALL_STATE` | Windows/WSL/license/existing-install/checkpoint branch не допускает продолжение. |
| `204` | `V10_BLOCKED_DOCKER` | Desktop/endpoint/daemon/Server OS не qualified или stopped для requested operation. |
| `205` | `V10_BLOCKED_PROJECT` | Mode/Compose/port/health/object state не exact. |
| `206` | `V10_BLOCKED_OWNER_ONBOARDING` | n8n owner/2FA/recovery lock не соответствует стадии. |
| `207` | `V10_BLOCKED_TELEGRAM_NOT_ARMED` | Phase arm отсутствует/истёк/drifted; zero provider API. |
| `208` | `V10_BLOCKED_RESOURCE` | V3 reserve/cap/compute/retention predicate не проходит. |
| `209` | `V10_BLOCKED_DRIFT` | Version/config/image/settings/runtime inventory не `CURRENT`. |
| `210` | `V10_BLOCKED_BACKUP` | Backup stale/missing/not restore-verified/custody unknown для операции. |
| `211` | `V10_BLOCKED_RECOVERY` | Supported recovery/cold-restore precondition отсутствует. |
| `212` | `V10_BLOCKED_POLICY` | Execution/screenshot/clipboard/support/at-rest policy не допускает шаг. |
| `213` | `V10_EMERGENCY_UNVERIFIED` | Disarm intent сохранён, но running external effect не доказан stopped. |
| `214` | `V10_STOP_INCIDENT_OPEN` | Revoke/copy/residual/rotation incident не закрыт. |
| `215` | `V10_FAIL_ACCEPTANCE` | Owner black-box acceptance predicate выполнен и провалился. |
| `216` | `V10_STOP_RESULT_INVALID` | Schema/RC/evidence/child aggregation противоречивы. |
| `217` | `V10_BLOCKED_ELEVATED_DAILY_SESSION` | Daily command вызвана из elevated/wrong-owner session. |
| `218` | `V10_BLOCKED_EVIDENCE_HYGIENE` | Запрещённый capture/source/scanner/support artifact обнаружен. |

При нескольких проблемах приоритет: `STOP_RESULT_INVALID` → containment/incident/emergency → contract drift → policy/identity → resource/drift/backup → health/manual. JSON сохраняет все `failed_predicates`, human показывает одно действие для самого высокого приоритета.

### 4.5. `install-status` state machine

```text
UNKNOWN
  -> DISCOVERED_READ_ONLY
  -> ELIGIBLE_NOT_INSTALLED | ALREADY_QUALIFIED
  -> READY_LICENSE_CARD
  -> READY_FEATURE_CARD
  -> READY_UAC_CARD
  -> INSTALL_ACTION_RUNNING
  -> REBOOT_REQUIRED_STOPPED
  -> RESUME_REVALIDATING
  -> INSTALLED_NOT_QUALIFIED
  -> INSTALLED_QUALIFIED

any -> BLOCKED_EXISTING_STATE | BLOCKED_POLICY | BLOCKED_RESOURCE
    -> BLOCKED_POST_REBOOT_DRIFT | FAILED_PARTIAL_INSTALL | RECOVERY_GATE_REQUIRED
```

`ELIGIBLE_NOT_INSTALLED`, `READY_*`, `REBOOT_REQUIRED_STOPPED` не являются install PASS. `ALREADY_QUALIFIED/INSTALLED_QUALIFIED` требуют exact V1/V2 installed identity и endpoint evidence. `UNKNOWN` никогда не подразумевает fresh install.

## 5. `V10-C03-OWNER-CARDS` — license, features, UAC и reboot

Каждая card выводится из immutable proposed action record и имеет:

```text
card_schema, card_id, card_type, plan_sha256, observation_sha256,
source/revision refs, exact action/executable/arguments or UI action,
why_needed, owner/elevation role, expected files/features/services/WSL objects,
network/data/resource impact, downtime, reboot semantics,
rollback vs recovery limits, abort outcome, expiry_utc,
required_manual_gate_id, next_checkpoint_state, card_sha256.
```

Owner confirmation создаёт secret-free attestation, связанную с exact card hash; свободное «да» или прошлое plan approval не заменяет card.

### 5.1. License card

Показывает exact Docker/n8n/third-party terms revision/date/source refs, выбранную owner eligibility/subscription category, obligations, unknowns и какие операции будут запрещены при отказе. Automation не выбирает категорию, не принимает terms и не передаёт consent switch. Changed terms invalidates card. Gates: `MG-V1-LICENSE`, `MG-V2-LICENSE-DOCKER`, `MG-V2-LICENSE-N8N`, `MG-V2-LICENSE-THIRD-PARTY` в их фактическом scope.

### 5.2. Windows feature card

Показывает exact before-state и только один delta для необходимых plan-A компонентов WSL 2/Virtual Machine Platform, signed executable/hash/arguments, expected feature/package objects, возможный reboot и rollback limitations. BIOS/UEFI, Hyper-V VM, отдельный distro, pagefile/security exclusions не добавляются. Gate: `MG-V1-WINDOWS-DELTA`.

### 5.3. UAC card

Показывает одну narrow elevated action, почему elevation нужна, exact signer/hash/path/args, `INTENDED_DAILY_OWNER` и отдельный `ELEVATION_CREDENTIAL`, ожидаемый профиль назначения, data impact и cancel result. Full orchestration/first launch не elevated. Gate: `MG-V1-UAC` либо точный supply-chain install-UAC gate; cancellation возвращает blocked/manual без retry loop.

### 5.4. Reboot card и resume

Автоматический reboot запрещён. Card требует владельцу сохранить работу, проверить питание и вручную перезагрузить Windows. До reboot атомарно публикуется secret-free checkpoint:

```text
checkpoint_id, plan/authority/card/delta/action-result hashes,
owner_ref, host_before_ref, expected_next_state, nonce,
issued/expires_utc, checkpoint_mac.
```

После входа используется тот же launcher:

```powershell
& "$env:LOCALAPPDATA\N8NAgents\control\lab.cmd" resume <checkpoint-id>
```

`resume` сначала повторяет read-only identity, OS/features/WSL/policy/pending-reboot/existing-install/endpoint/resource checks. Он не повторяет installer и не продолжает mutation автоматически. Changed owner/plan/card/host state, stale checkpoint или дополнительный reboot дают nonzero и новую owner card.

## 6. `V10-C04-DAILY-OPERATIONS` — ежедневный runbook

### 6.1. Начало обычной mock-сессии

Из новой standard PowerShell session и любого cwd:

1. `lab install-status` — ожидается `INSTALLED_QUALIFIED`; иначе выполнить только показанный safe action.
2. `lab docker start` — запускает только exact qualified Docker Desktop under intended owner, без update/install; bounded wait. Если Engine уже ready, no-op.
3. `lab status` — проверить `drift=CURRENT`, resources, endpoint, backup freshness, incident closed и Telegram `DISARMED`.
4. `lab start --mode mock` — exact V5 convergence; не читает real secrets и не создаёт external route.
5. `lab status` — ожидается `MOCK_READY`, loopback exposure и PostgreSQL/n8n health.
6. Открыть URL, напечатанный wrapper (`127.0.0.1:5678` only); bookmark/alternate address не является authority.
7. Выполнить synthetic mock workflow/message по frozen case ID; реальные IDs, prompts и персональные данные запрещены.

### 6.2. Диагностика во время работы

- `lab status` — краткий snapshot;
- `lab doctor` — read-only полный predicate report;
- `lab logs --redacted --since 15m` — bounded allowlisted logs;
- `lab backup status` — last COMPLETE/RESTORE_VERIFIED, age, RPO/RTO and custody state;
- `lab resource status` — exact V3 reserve/caps/trend without cleanup;
- `lab drift status` — approved/observed inventory diff IDs, no auto-update.

Никакая команда не рекомендует broad prune, reset, factory reset, `down -v`, SQL repair или disabling security controls.

### 6.3. Real Telegram test

Real-dev никогда не является continuation mock «одной кнопкой». Последовательность:

1. `lab stop` и verification `STOPPED/DISARMED`;
2. phase-specific V6 owner workflow из §8;
3. `lab start --mode real-dev` только с current `REAL_ARMED`;
4. `lab telegram status` до и после bounded real exchange;
5. `lab telegram disarm` immediately after test;
6. `lab stop`; verify zero poller/uplink/secret mount and preserved volumes;
7. `lab backup status`; data-changing run может потребовать новый backup по V8 policy.

DeepSeek остаётся `DISARMED` без отдельного `MG-V6-DEEPSEEK`; Telegram arm не разрешает модель, стоимость или запрос.

### 6.4. Backup и завершение дня

1. `lab backup status`.
2. Если due и все V8 gates готовы: `lab backup create --preview`, owner key proof, затем exact approved create operation.
3. `lab stop` — disarm first, drain, remove ephemeral containers/networks only, preserve persistent volumes.
4. `lab status` — ожидается `STOPPED_VERIFIED`, `DISARMED`, no listener/poller/uplink.
5. Docker Desktop можно закрыть через `lab docker stop` только после verified project stop; команда не uninstall/update/reset.

### 6.5. Sleep и reboot

Перед sleep: `lab prepare-sleep`. Он disarm-first, требует stopped real services и записывает secret-free session boundary; он не отправляет Windows в sleep. Owner выполняет sleep вручную.

Перед reboot: `lab prepare-reboot`. Он выполняет те же проверки, сообщает stale/active backup operation и пишет checkpoint, но не reboot-ит Windows.

После wake/reboot: `lab status`. Любой prior arm истёк. Если Docker stopped, `lab docker start`; затем только mock может быть восстановлен по обычному start. Real-dev всегда требует новое phase arming. Unknown previous operation/lock даёт doctor/recovery action, не automatic resume.

## 7. `V10-C05-N8N-OWNER-2FA` — onboarding и recovery без SQL

### 7.1. Version-specific lock

До owner onboarding существует `n8n_owner_operability_lock/v2`:

```text
n8n exact child/config digest and version, official source revision,
readiness and loopback URL contract, observed owner-state interface,
2FA enrollment/login/recovery interface, supported recovery command/UI,
effects and prerequisites, backup requirement, session-revoke behavior,
negative SQL/undocumented-endpoint policy, lock sha256.
```

Если exact version не имеет проверенного supported recovery interface, состояние `V10_BLOCKED_OWNER_ONBOARDING`; план не изобретает SQL reset. Direct metadata DB query/write, undocumented endpoint, password/2FA automation и extraction recovery material запрещены.

### 7.2. Owner onboarding

```text
INSTANCE_EMPTY
 -> OWNER_CARD_READY
 -> OWNER_CREATED
 -> TWO_FACTOR_ENROLLMENT_REQUIRED
 -> TWO_FACTOR_ENABLED
 -> LOGOUT_LOGIN_2FA_VERIFIED
 -> OWNER_OPERABLE
```

Порядок:

1. `lab n8n onboarding-status` подтверждает exact `INSTANCE_EMPTY`, mock readiness, loopback exposure и current n8n lock.
2. `lab n8n owner-card` печатает только loopback URL, stage, prohibitions и gate `MG-V5-OWNER-ONBOARD`.
3. Владелец вручную создаёт ровно одного owner в n8n UI. Email/password не вводятся в CLI, chat, Vault или screenshot.
4. Владелец вручную включает 2FA. QR, seed и recovery codes не фотографируются, не копируются в evidence и не читаются агентом.
5. Recovery material сохраняется владельцем в independently controlled custody, не в live secret root/backup ciphertext как единственной копии. Evidence содержит только `CUSTODY_ATTESTED` и keyed owner ref.
6. Владелец выходит, входит снова и подтверждает 2FA. Wrapper наблюдает только supported redacted state.
7. Multiple owner, disabled 2FA, identity drift или unknown state дают `BLOCKED_OWNER_ONBOARDING`; no repair.

### 7.3. Account/2FA recovery

Путь 1: владелец использует сохранённый recovery code через exact supported UI и после входа отзывает старые sessions/codes согласно locked runbook.

Путь 2, если recovery code недоступен: `lab n8n recovery-plan` остаётся read-only, требует current COMPLETE+RESTORE_VERIFIED backup, exact-version official recovery lock, stopped/disarmed state и owner gate. Сначала процедура репетируется на isolated restore copy. Затем владелец запускает только locked supported n8n recovery interface. Никакого прямого SQL, DB editor, undocumented API или удаления metadata row.

После recovery обязательны owner login/2FA re-enrollment, session revocation, credential decryptability, inactive workflow inventory, mock regression и новый backup. Если supported interface отсутствует, перестал соответствовать version или затрагивает данные иначе lock, статус остаётся `V10_BLOCKED_RECOVERY`; destructive instance recreation — отдельный план/gate, не fallback.

## 8. `V10-C06-TELEGRAM-ARM-UX` — TTL arming с redacted preview

V10 следует более строгому V6: никакого `getMe`, `getWebhookInfo`, DNS или Bot API до соответствующего phase arm. Формулировка V0 про «preflight, затем arm» реализуется как offline preview → `PROBE_ARMED` → bounded provider probe, а не как unarmed API call.

### 8.1. Owner workflow

1. `lab telegram identity-bind` — offline masked input и expected dev-bot identity; production deny; API count `0`.
2. `lab telegram probe-arm` — preview и approval TTL ≤5 min для ровно одного `getMe` и одного `getWebhookInfo`.
3. `lab telegram webhook-plan` — redacted snapshot и backlog choices; no mutation.
4. `lab telegram webhook-apply` — только отдельный TTL ≤5 min transition arm и exact frozen action. Backlog DROP имеет отдельный irreversible gate.
5. `lab telegram tuple-bind` — owner reviews exact five-part tuple through keyed refs and synthetic data class.
6. `lab telegram arm` — preview and explicit owner confirmation for `REAL_ARMED` TTL ≤30 min.
7. `lab start --mode real-dev` — validates every binding before secret mount/container/API.
8. `lab telegram disarm` — atomic revoke, drain/stop and proof.

### 8.2. Redacted preview

Real arm preview обязательно показывает:

- `environment_ref`, dev bot keyed fingerprint и `PRODUCTION_DENY=PASS`;
- recipient tuple-set keyed fingerprint and count, never raw IDs;
- exact synthetic data class and forbidden classes;
- plan/candidate/Compose/workflow/network/destination policy hashes;
- webhook decision/postcondition state;
- TTL and exact expiry local+UTC;
- Telegram cap `20`, consumed/reserved/remaining across authorization scope;
- permitted API methods and max polling/message bounds;
- DeepSeek `DISARMED` либо separate authorization/model/cost/request/TTL refs;
- automatic disarm triggers: stop, sleep/reboot/session/daemon drift, TTL, cap, conflict, identity/config/workflow drift and incident;
- exact external effects and `MG-V6-REAL-ARM` ID.

Arm record хранится protected and MAC-bound; status показывает только refs/counters/TTL. Expired/missing/drifted record gives RC `207` before provider API. New arm never resets used cap for the same authorization.

## 9. `V10-C07-EMERGENCY` — stop, Engine unavailable и provider revoke

Печатная карточка emergency должна быть доступна локально и содержать stable launcher path. Основная команда:

```powershell
& "$env:LOCALAPPDATA\N8NAgents\control\lab.cmd" emergency-stop telegram
```

Порядок неизменяем:

1. Acquire protected incident lock и атомарно записать host-side `DISARM_REQUESTED` с monotonic epoch до Docker/DB calls.
2. Если canonical DB path reachable, revoke arm/lease и запретить новые reservations/dispatch transactionally.
3. Через V1 endpoint guard stop secret-bearing bridge/adapters first, затем secretless brokers; remove exact ephemeral real objects without volumes.
4. Bounded verification: no poll request, provider socket, outbox dispatch, real restart, secret mount, uplink member or host/public listener.
5. Preserve PostgreSQL/n8n volumes, secret files, backups, evidence and incident record. No prune, reset, key deletion or revoke automation.
6. Только полный proof даёт `V10_OPERATION_VERIFIED` + child `DISARMED_VERIFIED`.

### 9.1. Engine/DB unavailable

Host disarm marker остаётся authority для следующего governed start, но не доказывает прекращение already-running process. Результат `V10_EMERGENCY_UNVERIFIED`, nonzero, с одним immediate action: owner вручную выбирает видимый **Quit/Stop Docker Desktop** для exact installed product из V1 runbook. Automation не убивает неизвестный process/service и не заявляет успех.

После manual quit owner снова запускает `lab emergency-stop telegram` либо `lab status`; только observed zero-process/socket/listener/secret-mount closes stop. Следующий Docker start обязан consume host disarm epoch before any secret mount/API and leave real services stopped.

### 9.2. BotFather revoke escalation

Если token compromise, uncontrolled poller или external effect нельзя исключить, status показывает `ACTION_OWNER_REVOKE_DEV_BOT_TOKEN`. Owner из trusted Telegram session открывает verified BotFather account and uses its **revoke token** flow for the exact independently recognized dev/test bot; token не вставляется в chat/CLI. Exact UI/command labels must be refreshed from authoritative provider source and frozen in provider-recovery card before operational use; this offline draft does not claim them current.

Old token usability check, issuance/binding of a successor token, webhook/backlog/offset/identity requalification and rearm are separate incident steps. V10 никогда не вызывает BotFather автоматически, не читает new token и не rearm-ит. Если provider revoke не подтверждён, incident остаётся `OPEN`, RC `214`.

## 10. `V10-C08-OPERABILITY-VISIBILITY` — resources, drift и backup

`lab status` всегда показывает, даже при stopped Docker:

### Resources

- redacted Windows volume ref, capacity/free bytes;
- V3 non-consumable reserve `R`, current operation `G/M/Pfree` where applicable;
- physical allocated VHDX bytes, Docker total and laboratory-labelled usage;
- PostgreSQL/backup/evidence/quarantine caps and warn/block state;
- measured trend and observation age;
- service hard memory/CPU limits and current envelope state when observable.

No reclaim estimate is added to free space. Low reserve blocks growth operation; status does not cleanup automatically.

### Drift

- `CURRENT | DRIFTED | UPDATE_PENDING | ROLLBACK_REQUIRED | UNKNOWN`;
- changed field IDs across Desktop/Engine/Compose/WSL/settings/images/config/migrations/CLI;
- current/LKG refs, latest qualification time and exception expiry;
- exact next action `review-drift`, never implicit pull/update/repair.

### Backup/recovery

- last `COMPLETE` generation ref and age;
- last `RESTORE_VERIFIED` ref and age;
- freshness `CURRENT | WARN | STALE_BLOCK_REAL | UNKNOWN`;
- independent age/n8n key custody state without paths/values;
- `L1_COLD_LOGICAL_RESTORE`, `L2_VHDX_LOSS_READY` or explicit unqualified tier;
- last measured RPO/RTO result and next due reason.

Status must not call a backup healthy solely because ciphertext exists. Missing authentication, COMPLETE marker, restore evidence, key custody or compatible lock remains blocked/unknown.

## 11. `V10-C09/C11` — black-box handoff и owner acceptance

### 11.1. Правила handoff

- новая standard unelevated Windows login/PowerShell session;
- произвольный cwd, repository не открыт и не требуется;
- owner получает только frozen one-page runbook, stable bootstrap command, approved custody items and named owner cards;
- agent не диктует команды, не отвечает во время run и не исправляет ошибку; только versioned CLI may show its predefined prompts/next actions;
- все manual confirmations are explicit, logged by card hash and never contain raw values;
- screen/session recording and transcription disabled/qualified before secret/2FA steps;
- любой undocumented command, agent hint, SQL, Docker direct call or hidden cwd prerequisite makes `V10_HANDOFF_PASS` impossible.

### 11.2. Mandatory black-box script

| Phase | Owner action and success criterion |
|---|---|
| `H01 Bootstrap` | From arbitrary cwd run stable command; verify CLI/version-root refs and healthy read-only status. |
| `H02 Install diagnosis` | `install-status` and `doctor` correctly distinguish qualified/current state from injected pending reboot/unknown fixture without mutation. |
| `H03 Docker/mock` | Start exact Desktop, start mock, prove loopback-only UI, PostgreSQL/n8n health and synthetic mock exchange. |
| `H04 n8n owner` | On disposable instance create owner, enroll 2FA, logout/login; no raw material in capture/history/evidence. |
| `H05 Persistence` | Stop/start project and Docker Desktop; semantic DB/workflow/credential/file canaries remain accessible and Telegram remains disarmed. |
| `H06 Injected fault` | Approved fixture makes PostgreSQL unhealthy or port occupied; status becomes nonzero with one correct safe action; doctor does not repair; controlled recovery restores mock. |
| `H07 Real Telegram` | Phase-arm dev identity/webhook/tuple, start real-dev, perform minimum approved synthetic exchange within cap, inspect counters, disarm and verify zero polling/uplink. |
| `H08 Emergency healthy` | During active bounded poll run emergency command; host disarm first, verified stop, volumes unchanged, no automatic rearm. |
| `H09 Emergency Engine-down` | Inject Engine-unavailable boundary; result remains nonzero/unverified, owner follows visible Desktop stop and provider revoke card if required, then closes via observed status. |
| `H10 Backup` | Create one COMPLETE generation under key proof; interruption fixture never publishes partial as selectable. |
| `H11 Cold restore` | With source volumes and live secret root inaccessible, owner supplies independent age+n8n custody, restores into fresh no-egress/no-port target and passes semantic canaries. |
| `H12 Sleep/reboot` | Prepare boundary, manually sleep/reboot, run status/resume; no installer repeat, volume loss or real rearm. |
| `H13 Daily close` | Redacted logs/backup status, disarm/stop, Docker stop; final state has no app listener/poller/uplink and persistent data remains. |

Real-provider and reboot rows execute only under their exact manual gates. Before those gates the acceptance suite may report scoped `BLOCKED_MANUAL`, never fabricate PASS. `H09` uses a controlled Engine-down fixture and does not corrupt Docker. `H11` proves V8 L1 only; actual VHDX/host loss remains separately destructive.

## 12. `V10-C10-EVIDENCE-HYGIENE` — screenshots, clipboard и support

### 12.1. Structured evidence first

Owner uses JSON result ID/evidence refs instead of screenshot whenever possible. Safe screenshots may be created only from screens synthetic and non-sensitive **before capture**. Redaction after capturing a token/2FA/PII screen does not make the raw original acceptable.

Always forbidden in screenshot/video/remote recording:

- Telegram/DeepSeek tokens, DB/n8n/backup keys and secret-entry windows;
- n8n Credentials, owner password, 2FA QR/seed/recovery codes;
- raw bot/user/chat/thread IDs, message bodies, usernames, routes or provider responses;
- unrestricted Docker inspect/log/env/support output;
- Windows usernames/SIDs/raw paths, browser session/account data or provider billing identity.

Approved synthetic UI capture uses protected staging, strips metadata, passes field-aware OCR/content scan and manual preview, then publishes only sanitized derivative to evidence. A forbidden/raw capture is not retained for redaction; it opens incident/copy inventory. Secure erase is not claimed.

### 12.2. Clipboard

Clipboard is prohibited by default for secrets and 2FA. One secret slot may use `MG-V7-CLIPBOARD-PASTE-<slot>` only after owner card reports clipboard history/cloud sync/third-party manager/remote capture as `SAFE`; helper reads one masked paste, publishes one restricted file, clears current clipboard and requires owner-visible history clearing. `UNKNOWN/UNSAFE`, screenshot/recording or uncertain cleanup marks credential potentially contaminated and requires revoke/rotate before real use.

Non-secret command/result refs may use clipboard only if they contain no raw path/identity. Clipboard clearing is operational hygiene, not secure-erase evidence.

### 12.3. Support bundle

Ordinary `status/doctor/logs` never creates a Docker/vendor support bundle or dump. `MG-V7-SUPPORT-INCIDENT`/`MG-V3-SUPPORT-BUNDLE` is required **before creation**, binding incident, exact tool, classes, max bytes/time, encrypted quarantine, disarm and no-auto-upload. If tool creates uncontrolled plaintext, location is unknown or upload cannot be disabled, collection is blocked.

Bundle remains presumed secret-bearing ciphertext; it is not attached to Vault/repo/evidence and is never uploaded automatically. External transfer requires a second owner decision after relevant revocation/rotation. Failed/partial cleanup is exact-target and separately gated.

## 13. Acceptance tests, negative canaries и evidence

All rows are future obligations. Evidence is schema-valid, content-addressed, secret-minimal and bound to exact plan/CLI/runtime/owner-card/result identities. Child component output cannot self-promote global status.

| ID | Acceptance test | Negative canary | Evidence |
|---|---|---|---|
| `AT-V10-01` | Clean unelevated PowerShell from three arbitrary cwd resolves one approved launcher/version root and exact local endpoint without PATH/global-context dependence. | `NC-V10-01`: elevated/other user, changed current context, `DOCKER_HOST`, moved/reparse/stale launcher, alternate version pointer and repo-relative invocation all block before child/Docker mutation. | `EV-V10-01-BOOTSTRAP`: launcher/version/operator/endpoint hashes, cwd classes and zero-mutation results. |
| `AT-V10-02` | Golden `install-status/status/doctor` fixtures produce identical human/JSON semantics, stable RC and one next action for healthy, absent Docker, pending reboot, stopped Engine, occupied port, unhealthy PG, low disk, drift, stale backup and armed Telegram. | `NC-V10-02`: unknown field, stale evidence, invalid child schema, stdout PASS/nonzero child, zero RC with blocked component and doctor mutation are rejected. | `EV-V10-02-DIAGNOSTICS`: schemas, fixture hashes, state/RC matrix, human projection hashes and no-change ledger. |
| `AT-V10-03` | License/feature/UAC/reboot cards show exact bounded action; cancel/no-reboot/reboot-required/multi-reboot/resume cases follow state machine. | `NC-V10-03`: stale card/checkpoint, changed plan/owner/delta, hidden elevation, automatic reboot/resume or installer repeat blocks. | `EV-V10-03-OWNER-CARDS`: card/attestation/checkpoint hashes and before/action/post-state refs. |
| `AT-V10-04` | Owner follows daily mock start/status/UI/synthetic exchange/logs/backup-status/stop from clean session; stop preserves volumes and removes exposure. | `NC-V10-04`: direct Docker command, implicit pull/update, mixed profile, raw log, auto-cleanup or real secret in mock prevents PASS. | `EV-V10-04-DAILY-MOCK`: redacted black-box command/result chain and child health/exposure refs. |
| `AT-V10-05` | Exact-version disposable n8n creates one owner, enrolls 2FA, logout/login succeeds; supported recovery on separate restore copy restores access without SQL. | `NC-V10-05`: direct metadata SQL, undocumented endpoint, raw 2FA/recovery material in history/capture/evidence, multiple owner or wrong-version recovery blocks. | `EV-V10-05-N8N-OWNER`: operability-lock hash, redacted state transitions, custody attestations and mock regression refs. |
| `AT-V10-06` | Phase arms allow only exact V6 methods/TTL; redacted real preview binds dev bot/tuple/cap/workflow/network and bounded real exchange disarms cleanly. | `NC-V10-06`: unarmed `getMe`, expired/rebooted/drifted arm, production token, changed tuple/webhook/workflow, 21st send or DeepSeek without separate gate yields zero unauthorized call. | `EV-V10-06-TELEGRAM-ARM`: preview/decision/arm hashes, keyed refs, method/cap counters and disarm proof. |
| `AT-V10-07` | Healthy/hung/unhealthy/Engine-down emergency cases publish host disarm first, preserve volumes and report success only with process/network proof. | `NC-V10-07`: Engine unavailable while CLI says stopped, real restart policy, lingering poll/socket/secret mount or implicit rearm gives nonzero/open incident. | `EV-V10-07-EMERGENCY`: disarm epochs, bounded stop assertions, Engine state, provider-revoke state and next-action refs. |
| `AT-V10-08` | Boundary fixtures above/below V3 reserve/caps, one drifted digest and backup ages around warn/block thresholds are accurately visible and admission-controlled. | `NC-V10-08`: reclaimable bytes counted as free, ciphertext-only marked recoverable, missing custody marked healthy, auto-update/cleanup or hidden trend blocks. | `EV-V10-08-VISIBILITY`: resource equations, usage/trend, drift diff and backup/restore/custody refs. |
| `AT-V10-09` | Synthetic safe UI screenshot, non-secret clipboard and incident-only encrypted support workflow obey source/retention policy. | `NC-V10-09`: token/2FA/raw ID/path fixture, OCR/metadata/scanner failure, unsafe clipboard history, plaintext or auto-upload support artifact is rejected and opens incident where applicable. | `EV-V10-09-EVIDENCE-HYGIENE`: allowed source IDs, scan decisions, owner gates and ciphertext catalog refs; no raw capture. |
| `AT-V10-10` | Owner completes H01–H13 from clean standard session using frozen runbook only, with no agent message/hint and documented manual gates. | `NC-V10-10`: unknown cwd dependence, undocumented command, agent coaching, skipped fault/emergency/restore row or hidden destructive action leaves handoff incomplete. | `EV-V10-10-BLACKBOX`: ordered result refs, owner attestations, interaction/no-agent declaration and final state. |
| `AT-V10-11` | Backup interruption, wrong key, target collision and successful independent cold restore behave per V8; source/live secret root remain inaccessible and unchanged. | `NC-V10-11`: partial selectable backup, live-key/root access, source volume mount, egress/port/trigger, SQL recovery or in-place failed-target retry prevents recovery PASS. | `EV-V10-11-COLD-RESTORE`: V8 operation/generation/keys/isolation/fault evidence refs and owner timeline. |
| `AT-V10-12` | Prepare sleep/reboot, new login and resume preserve data, detect daemon/session drift and require fresh real arm without rerunning install. | `NC-V10-12`: stale arm survives, installer repeats, checkpoint silently accepted after drift or owner must know repo cwd. | `EV-V10-12-SESSION-RECOVERY`: boundary/checkpoint/boot refs, status transitions and no-rearm/no-install-repeat proofs. |

## 14. Traceability: relevant V0 finding → V10 contract / AT / NC / EV

`DESIGN_CLOSED` means only that V10 owner-facing design exists. Runtime and cross-domain closure remain pending. `XDEP` means V10 cannot close the finding alone.

### 14.1. Primary R10 findings

| Finding | V10 contract | AT / NC / EV | Disposition |
|---|---|---|---|
| `R10-F01` | `V10-C06` | `AT/NC/EV-V10-06` | `DESIGN_CLOSED_WITH_XDEP-V4/V5/V6`; phase arm precedes every API |
| `R10-F02` | `V10-C07` | `AT/NC/EV-V10-07` | `DESIGN_CLOSED_WITH_XDEP-V1/V4/V6/V7` |
| `R10-F03` | `V10-C11` | `AT/NC/EV-V10-11` | `DESIGN_CLOSED_WITH_XDEP-V3/V5/V7/V8` |
| `R10-F04` | `V10-C08` | `AT/NC/EV-V10-08` | `DESIGN_CLOSED_WITH_XDEP-V3/V5` |
| `R10-F05` | `V10-C02`, `V10-C08` | `AT/NC/EV-V10-02`, `08` | `DESIGN_CLOSED_WITH_XDEP-V1/V2/V5/V8` |
| `R10-F06` | `V10-C09`, `V10-C11` | `AT/NC/EV-V10-10`, `11` | `DESIGN_CLOSED`; runtime handoff pending all domains |
| `R10-F07` | `V10-C05` | `AT/NC/EV-V10-05` | `DESIGN_CLOSED_WITH_XDEP-V2/V5/V7/V8`; supported exact-version recovery pending |
| `R10-F08` | `V10-C02` | `AT/NC/EV-V10-02` | `DESIGN_CLOSED`; global child mapping unresolved |
| `R10-F09` | `V10-C03` | `AT/NC/EV-V10-03`, `12` | `DESIGN_CLOSED_WITH_XDEP-V1/V2` |
| `R10-F10` | `V10-C10` | `AT/NC/EV-V10-09` | `DESIGN_CLOSED_WITH_XDEP-V3/V7/V9` |
| `R10-F11` | `V10-C01`, `V10-C04` | `AT/NC/EV-V10-01`, `04`, `12` | `DESIGN_CLOSED`; runtime launcher/handoff pending |

### 14.2. Material cross-findings

| Finding | V10 contribution | AT / NC / EV | Remaining owner |
|---|---|---|---|
| `R1-WIN-002` | install-status renders support predicate and unknown fail-closed | `AT/NC/EV-V10-02`, `03` | V1/V2 authoritative requirements |
| `R1-WIN-003`, `R1-WIN-011` | exact feature/reboot cards and resume checkpoint | `AT/NC/EV-V10-03`, `12` | V1 Windows transaction |
| `R1-WIN-004` | daily owner/elevation role separation in launcher/cards | `AT/NC/EV-V10-01`, `03` | V1 identity/control plane |
| `R1-WIN-005` | fresh/upgrade/already-qualified/blocked discovery shown without repair | `AT/NC/EV-V10-02` | V1 existing install |
| `R1-WIN-009` | drift/current/update/LKG visibility and start block | `AT/NC/EV-V10-08` | V1/V2 update implementation |
| `R1-WIN-012` | occupied-port owner diagnosis without auto-port fallback | `AT/NC/EV-V10-02`, `04` | V1/V4 exposure |
| `R4-F07` | n8n owner/2FA/workflow lifecycle owner ceremony | `AT/NC/EV-V10-05` | V5 exact n8n interface |
| `R4-F10` | actionable deterministic component diagnostics | `AT/NC/EV-V10-02` | V5 child status |
| `R5-F16` | Telegram owner ceremony and emergency black-box flow | `AT/NC/EV-V10-06`, `07`, `10` | V6 correctness/provider state |
| `R6-P1-009` | revoke/rotate escalation and open-incident visibility | `AT/NC/EV-V10-07` | V7 incident lifecycle |
| `R6-P2-011` | owner secret/clipboard/screenshot ceremony | `AT/NC/EV-V10-09` | V7 secret transport |
| `R7-F10` | owner-independent cold restore handoff | `AT/NC/EV-V10-11` | V8 recovery implementation |
| `R7-F11` | backup freshness/RPO/RTO visibility | `AT/NC/EV-V10-08`, `11` | V8 owner policy |
| `R7-F12` | backup/restore fault rows in owner acceptance | `AT/NC/EV-V10-11` | V8 fault implementation |
| `R8-P1-006` | scoped global state/RC projection, no BLOCKED→SUCCESS | `AT/NC/EV-V10-02` | V9/global schema integrator |
| `R9-F10` | pre-secret bootstrap and evidence hygiene | `AT/NC/EV-V10-01`, `09` | V7/V9 source/temp safeguards |

## 15. Manual gates и owner decision routing

V10 не создаёт approvals, дублирующие domain authority. Owner card маршрутизует только exact existing gate; один gate не подразумевает следующий.

| Owner-facing moment | Required gate(s) | Что не включено |
|---|---|---|
| Full plan start | `MG-V1-PLAN`, `MG-V9-PLAN` и canonical full-plan authority | install/runtime/provider/destructive actions без их gates |
| License decision | `MG-V1-LICENSE`, `MG-V2-LICENSE-*` | automation acceptance, changed terms |
| Windows feature delta | `MG-V1-WINDOWS-DELTA` | BIOS, separate distro, plan B, security exclusion |
| UAC/install | `MG-V1-UAC`, `MG-V1-INSTALL`, `MG-V2-INSTALL-UAC` | full elevated orchestration, first launch as admin |
| Reboot/resume | `MG-V1-REBOOT`, затем `MG-V1-POST-REBOOT` | auto-reboot/auto-resume |
| Roots/resources/at-rest | `MG-V3-ROOTS`, `MG-V3-RESOURCE-THRESHOLDS`, applicable trust/at-rest gate | silent risk acceptance/cleanup |
| n8n key/owner/2FA | `MG-V5-N8N-KEY`, `MG-V5-OWNER-ONBOARD` | password/2FA capture or automation |
| n8n recovery | `MG-V5-UPDATE` or exact recovery gate plus verified backup; `MG-V8-OWNER-KEY-PROOF` as applicable | SQL reset, destructive recreation |
| Telegram identity/probe/webhook/tuple | `MG-V6-IDENTITY`, `MG-V6-PROBE`, `MG-V6-WEBHOOK`, optional `MG-V6-DROP-BACKLOG`, `MG-V6-TUPLE-DATA` | real send/start until real arm |
| Telegram real-dev | `MG-V6-REAL-ARM`, `MG-V4-REAL-ARM` | DeepSeek, new recipient/data class, cap reset |
| DeepSeek | `MG-V6-DEEPSEEK` | Telegram arm as cost authority |
| Incident/revoke/rotate | `MG-V6-INCIDENT` and applicable V7 issuer/custody decision | automated provider ownership action |
| Backup/cold restore | `MG-V8-BACKUP-ROOT`, `MG-V8-KEY-CUSTODY`, `MG-V8-RPO-RETENTION`, per-run `MG-V8-OWNER-KEY-PROOF` | live key/root dependency, target deletion |
| Clipboard exception | `MG-V7-CLIPBOARD-PASTE-<slot>` | unknown/unsafe clipboard state |
| Support bundle | `MG-V7-SUPPORT-INCIDENT`, `MG-V3-SUPPORT-BUNDLE`; separate transfer decision | auto-create/upload/plaintext artifact |
| Cleanup/destruction | exact V3/V4/V8/V9 target gate | prune, volume/VHDX/backup/key deletion by daily CLI |

## 16. Cross-domain dependencies и нерешённый interface drift

### 16.1. Required interfaces

| Owner section | V10 consumes | V10 provides |
|---|---|---|
| V1 Windows/control plane | intended owner, endpoint guard, eligibility/install/change/reboot states | owner cards, stable launcher UX and V1 child-state projection |
| V2 supply chain/license | launcher/tool/image/source/license/drift locks and LKG | license/update owner UX and drift visibility |
| V3 resources/storage | qualified roots, caps/reserve/trend, backup freshness/custody | concise owner visibility, warning/block and cleanup-free next action |
| V4 isolation/network | modes, exposure, no-egress, object and emergency network proof | global commands, owner manual LAN/emergency actions and status projection |
| V5 Compose/PostgreSQL/n8n | lifecycle, health, owner/2FA/recovery, workflow and DB states | daily start/stop/onboarding/recovery UX and black-box tests |
| V6 Telegram/DeepSeek | phase arms, identity/tuple/webhook/cap/cost/offset/emergency semantics | redacted owner preview, phase ceremony and provider escalation UX |
| V7 secrets/privacy/incident | masked input, screenshot/clipboard/support/incident rules | printable emergency/entry cards and no-secret owner output |
| V8 backup/cold restore | generation, keys, RPO/RTO, faults, restore isolation/results | backup/recovery status and owner cold-restore handoff |
| V9 candidate/evidence/Git | immutable CLI/version/evidence identities and global scoped truth | stable owner verification commands, black-box evidence and no-cwd requirement |

### 16.2. Blocking V4/V5/V6 drift — V10 does not resolve it

`DRIFT-V10-01-BRIDGE-DB-PATH`:

- V4 network graph gives `telegram-bridge` only `telegram_ingress` and `telegram_proxy`; PostgreSQL is only on `db`.
- V5 §6.3 and its roles require `bridge_runtime` to call PostgreSQL procedures directly and V5 residual explicitly asks to add a DB-only bridge path.
- V6 explicitly forbids bridge DB path/credential and routes authenticated envelope via `telegram_ingress` to n8n/application ingress, which calls PostgreSQL as `automation_runtime`.

These are mutually exclusive trust/topology contracts. Unioning both would broaden permissions and is forbidden. Until a separately integrated owner chooses one exact path, revises V4/V5/V6 service/network/role/secret/procedure/workflow hashes and re-reviews it:

- `real-dev`, Telegram emergency DB postcondition, bridge backup writer inventory and real black-box rows are `V10_BLOCKED_CONTRACT_DRIFT`;
- V10 status names all three conflicting hash refs and action `ACTION_REVIEW_V456_BRIDGE_PATH`;
- V10 does not invent a proxy, second credential, alias or temporary bypass.

`DRIFT-V10-02-SERVICE-KEY`:

- Current V4 and V6 use `egress-telegram` and V6 rejects alias `telegram-egress-proxy`.
- V5 residual text still records a conflict as if V6 used the alias. This stale interface statement must be removed/re-hashed in canonical integration; runtime manifest cannot proceed from contradictory prose even if intended service name appears inferable.

`DRIFT-V10-03-ARM-ORDER`:

- V0 `R10-F01` prose describes read-only provider preflight before `lab arm telegram`.
- V6 requires zero API including `getMe/getWebhookInfo` before phase-specific `PROBE_ARMED`.
- V10 owner flow exposes offline preview then phase arm, but canonical integrated plan must explicitly disposition the V0 wording and freeze one API-call state machine. Until then provider operations remain blocked.

`DRIFT-V10-04-GLOBAL-RESULT`:

- V1–V8 use overlapping numeric RC and different result schemas/state names.
- V9 requires scoped semantic aggregation and rejects BLOCKED promotion.
- V10 defines owner projection, but canonical global mapping/schema/canonicalization and child freshness rules are not yet frozen. Unknown mapping is RC `216`, not best-effort status.

`DRIFT-V10-05-SECTION-NUMBERING`:

- Some V4/V7 references call backup/evidence owners `V7/V8`, while assigned drafts are secrets `V7`, backup `V8`, custody/evidence `V9`.
- Canonical integrator must mechanically rewrite references and hashes; V10 links by contract IDs, not inferred section number.

No drift above is runtime-tested or resolved by this document.

## 17. Residual risks и STOP triggers

Residual risks:

1. A compromised Windows owner/admin/SYSTEM/Docker control principal can bypass CLI and extract runtime data; runbook cannot enforce behavior outside governed launcher.
2. Visible Docker Desktop quit and host disarm marker cannot prove an already-running external effect stopped when Engine/OS observation is unavailable; provider revoke may be required.
3. BotFather/provider UI labels and exact n8n recovery interface can drift; both must be refreshed from authoritative exact-version sources before use.
4. Browser extensions, screen/remote-session capture and clipboard managers remain outside Docker isolation. Policy reduces but does not eliminate exposure.
5. Sanitized screenshots can still reveal layout/timing correlations; structured evidence is preferred.
6. Backup and independently held keys on the same physical host do not prove host-loss DR; V8 L1/L2 labels remain exact.
7. Owner black-box success proves documented operability for one exact fingerprint, not unattended production operation or REMOTE readiness.
8. Daily `status` can only report what approved collectors observe. Unreadable control plane, firewall, provider or opaque support artifact remains blocked/unknown.
9. Docker Desktop auto-update behavior may not be suppressible; drift gate must block start until requalification.
10. Plan A may leave OFFLINE O5 rows blocked by capability while LAB remains independently useful; V10 must not call this full project success.

Immediate STOP/BLOCKED before next mutation:

- launcher/version root/operator/endpoint identity unknown or changed;
- elevated daily session or hidden global Docker/context/profile dependency;
- unknown child state/schema/RC mapping or stale evidence presented as healthy;
- unresolved V4/V5/V6 bridge path, service-key, arm-order or result mapping drift;
- license/terms/existing-install/feature/UAC/reboot card absent, changed or expired;
- automatic reboot, auto-resume, installer repeat or daily command asks elevation;
- n8n owner/2FA/recovery interface not exact-version supported or any SQL workaround;
- real arm absent/expired/drifted, production identity, changed tuple/workflow/network, cap/cost unknown;
- emergency stop without complete process/network proof reported as success;
- incident/revoke/contaminated-copy/residual state open;
- resource reserve, drift, backup freshness/custody or recovery tier unknown for requested operation;
- raw secret/PII/path in output/capture/clipboard/support/evidence or scanner failure;
- black-box run uses agent coaching, undocumented command, direct Docker/SQL or hidden cwd;
- any fallback to plan B, VPS, production, broader privilege or destructive cleanup without a new exact owner decision.

## 18. Future implementation order и Definition of Done V10

Sequential order after frozen full plan approval and applicable authorities:

1. Resolve and re-hash all drift in §16.2; freeze global result schema/RC/canonicalizers and section numbering.
2. Freeze V1/V2 owner/endpoint/license/install/update interfaces and V3 approved control/version/evidence roots.
3. Implement stable launcher/version-root dispatch and fixture-test it without Docker/host mutation.
4. Implement global typed result aggregator, human renderer and read-only `install-status/status/doctor/details/logs` adapters.
5. Implement owner cards/checkpoint/resume state machine and run fixture/disposable Windows acceptance under separate gates.
6. Implement V5 daily mock lifecycle and exact-version n8n owner/2FA/recovery locks; run synthetic/disposable tests.
7. Implement V6/V7 phase arming, redacted preview, disarm/emergency/provider-revoke cards after topology canonicalization.
8. Integrate V3/V8 resources, backup freshness, key custody and cold restore owner workflows.
9. Integrate V9 content-addressed CLI/result/evidence identity and seal AT/NC/EV-V10 records through trusted collector.
10. Run H01–H13 black-box handoff from clean standard session; any agent assistance invalidates run.
11. Obtain independent review of frozen plan, implementation, runbook and exact evidence anchor.

V10 design is ready for canonical integration review only when:

- all `R10-F01..F11` and material cross-findings map to named contract/AT/NC/EV;
- one stable unelevated bootstrap works conceptually without cwd/PATH/global-context dependence;
- human and JSON status share one fail-closed object and preserve `UNKNOWN/BLOCKED`;
- license/features/UAC/reboot are resumable separate owner cards;
- n8n owner/2FA/recovery has an exact-version supported, no-SQL contract;
- daily mock/real/disarm/logs/backup/stop/sleep/reboot procedures are complete;
- emergency Engine-down and BotFather escalation never false-PASS;
- resource/drift/backup/recovery truth is visible without mutation;
- screenshot/clipboard/support flows cannot silently publish sensitive artifacts;
- black-box acceptance contains injected fault, emergency and independent cold restore;
- V4/V5/V6 drift remains explicitly blocking until another integration decision resolves and re-hashes it;
- no runtime, installation, Docker, provider, repository, Vault-other-file, VPS, secret or production action is claimed;
- file is UTF-8 without BOM, LF only and exactly one final LF.

Future `V10_HANDOFF_PASS` requires all H01–H13 applicable rows, exact child domain PASS/manual attestations, zero undocumented assistance, schema-valid evidence and final stopped/disarmed/recoverable state. It does not grant REMOTE/production authority.

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
- [[09_V8_BACKUP_COLD_RESTORE]]
- [[10_V9_CANDIDATE_EVIDENCE_GIT_CUSTODY]]
