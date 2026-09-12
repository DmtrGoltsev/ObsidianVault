---
id: "n8nagents-plan-v2-v1-windows-control-plane"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V1 Windows/Docker platform architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
доказательства:
  - "00_FINDINGS_BASELINE.json"
  - "01_BASELINE_AUDIT.json"
теги: ["n8nagents", "plan-v2", "windows", "docker-desktop", "control-plane", "design-only"]
---

# V1 — Windows и Docker Desktop control plane для plan v2

## 0. Статус, область и запрет на исполнение

Этот документ — implementation-ready проект секции `V1` для будущего полного plan v2. Он не является разрешением на read/write preflight, download, установку, UAC, включение Windows features, reboot, запуск Docker, изменение Docker context, доступ к VPS или ввод секретов.

В область `V1` входят только:

- квалификация Windows и существующего Docker-состояния;
- транзакция WSL 2 / Virtual Machine Platform / reboot;
- модель Windows identities и Docker control plane;
- локальный Docker endpoint invariant;
- storage/resource eligibility на уровне Windows;
- install/upgrade/uninstall/rollback semantics;
- policy/drift/port guards, result schema, canaries и evidence contracts.

План B, отдельный пользовательский WSL-дистрибутив, Hyper-V VM, Windows Sandbox, VPS и production остаются запрещёнными fallback. Никаких runtime-утверждений здесь нет: текущие Windows, WSL, Docker, политики, ресурсы, identities и порт `5678` имеют статус `UNKNOWN` до отдельно разрешённого read-only discovery.

## 1. Проверенные входы и граница findings

| Вход | Bytes | SHA-256 | Результат |
|---|---:|---|---|
| `00_FINDINGS_BASELINE.json` | `213739` | `934c449aa75ad157b1702afefcbaac4eab80b750801f172226d065b5a528c4aa` | `MATCH` |
| `01_BASELINE_AUDIT.json` | источник V0 | статус внутри файла `PASS` | `READ` |
| frozen plan v1 | `46234` | `a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79` | `IDENTITY_ACCEPTED_FROM_AUDIT` |
| quorum report | `21742` | `08a59e4838d42102f94bb0bb826201d5edec704fcd90a6fe401f8e05f4eff5e7` | `IDENTITY_ACCEPTED_FROM_AUDIT` |
| `R01.json` | `26209` | `df9c80bc7eb5067f0c293f1373221722ef64e983d520fa9c2ce5999f05449571` | `MATCH` |

Повторно реконструирован canonical hash каждого `R1-WIN-001`…`R1-WIN-012` из raw `R01.json` по правилам baseline. Все `12/12` совпали:

| Finding | Canonical SHA-256 |
|---|---|
| `R1-WIN-001` | `231e0951f7f6551550e947996e0a3942ba3b09ac4a090b9c4bd9262eb5b3efc3` |
| `R1-WIN-002` | `14742c1355f2cb047548945995720d3c0529b8669531259b3736b22987f02052` |
| `R1-WIN-003` | `9064f58591d47ed1571aa1bf4f916aac3b605a7a8afd16c6253985b8e1878281` |
| `R1-WIN-004` | `1f3ef4d0115cdfa32034e827334a63dbf4674e93ca49dbc04546b6c9b5b8529c` |
| `R1-WIN-005` | `8f0f36a4a668857d6638b5c4d792172cc50eee8b08d61454a3a6698c032e302c` |
| `R1-WIN-006` | `7850b7593b4a1dec2708c4e36f8ce509b383d0122b102888284bb529f8363047` |
| `R1-WIN-007` | `acefd7f25a251e01866e70af2b4c1cb8e6080f5ed15d515ba17ce2210c4e3e4a` |
| `R1-WIN-008` | `3a8dcb141ccb0bb1c3640a4fd4369046464f0a7a52f31d9023d8be6a591e75e4` |
| `R1-WIN-009` | `576fd4544dbbce3fc37f46e91a805d4efe6f6fdf928fea650dec032074b1b582` |
| `R1-WIN-010` | `7a2d28a1c3c1608375592cefabf20338a9451a9feba47801ab7ade1b9ce23850` |
| `R1-WIN-011` | `d6cc7193e831766dadb24a4515bb3466d4ae7e8d01ecb22953c5f5105ac14958` |
| `R1-WIN-012` | `1fdc076c9aafd9cbaa7d1b16d090c36bacc205538fc5d208b1927d6079b4cf4c` |

Секция обязана закрыть именно эти 12 source findings. Cross-domain findings перечислены как зависимости, но не объявляются закрытыми `V1`.

## 2. Общие инварианты

### V1-000 — fail-closed и zero-assumption

1. Любое требуемое поле имеет трёхзначное состояние `KNOWN_VALID | KNOWN_INVALID | UNKNOWN`.
2. `UNKNOWN`, unreadable, contradictory, stale или не связанное с frozen rules/plan поле никогда не трактуется как допустимое.
3. Только `KNOWN_VALID` по всем обязательным predicates даёт `PASS` конкретной read-only стадии.
4. Любой mutation требует: актуальный plan hash, authorization hash, guard tuple, precondition snapshot, exact touchset и новый непосредственный guard перед первой mutation.
5. Никакой child stdout, слово `PASS` или exit code сами по себе не достаточны: результат должен соответствовать schema из раздела 12.
6. Оркестратор не меняет глобальный Docker context, Windows security policy, BIOS/UEFI, pagefile, power policy, update policy, firewall, Docker data root или пользовательские группы как скрытую remediation.
7. Все имена пользователей, SID, пути профиля и machine identifiers в долговременном evidence заменяются role labels и keyed pseudonyms. Exact значения находятся только в локальном защищённом control record вне Git/Vault.

### V1-000A — immutable execution identity

До любого mutation создаётся `execution_lock`:

```text
execution_lock_sha256 = SHA256(canonical-json(
  plan_sha256,
  authorization_id + authorization_sha256,
  rules_snapshot_sha256,
  acquisition_lock_sha256,
  branch_kind,
  intended_owner_ref,
  approved_endpoint_record_sha256,
  approved_roots_record_sha256,
  resource_policy_sha256,
  exact_operation_manifest_sha256
))
```

Если применимое поле ещё не существует, mutation запрещён; read-only discovery может выдать только `READY_FOR_MANUAL_GATE` или `BLOCKED_*`.

## 3. V1-001 — invariant локального Docker endpoint

### 3.1. Approved endpoint record

После успешной установки/квалификации, но до pull/build/start, один раз создаётся защищённый `approved_endpoint_record`:

```yaml
schema: n8nagents.local-docker-endpoint/v2
endpoint_class: WINDOWS_LOCAL_NAMED_PIPE_DOCKER_DESKTOP_LINUX
context_name: <exact locally resolved name>
endpoint_uri: <exact canonical local npipe URI>
transport: npipe
server_os: linux
architecture: amd64
desktop_product_ref: <installed-product evidence ref>
desktop_build: <exact>
engine_version: <exact>
compose_version: <exact>
daemon_id: <exact local value, stored only in protected control record>
daemon_name: <exact local value, stored only in protected control record>
docker_root_identity: <redacted physical-volume/object identity>
settings_sha256: <canonical approved settings hash>
owner_ref: <keyed pseudonym>
authorized_control_principals: [<keyed pseudonyms>]
qualified_at_utc: <timestamp>
record_sha256: <self-excluding canonical hash>
```

Допустим только локальный Windows named pipe, который одновременно доказан как Docker Desktop Linux engine. TCP/HTTP/HTTPS/SSH, WSL-distribution socket, remote daemon, rootless engine другого продукта, unknown pipe и любой endpoint через proxy запрещены. Имя context само по себе не является доказательством.

### 3.2. Guard каждой операции

Все Docker/Compose API-вызовы лаборатории проходят через один versioned wrapper `local-daemon-guard`; прямой вызов `docker`, `docker compose`, SDK или named pipe из lab scripts запрещён static policy.

Перед **каждой** read-write операцией (`pull`, `build`, `create`, `start`, `stop`, `restart`, `exec` с write-effect, `cp` в container/volume, network/volume/image create/remove, backup, restore, cleanup, update) wrapper обязан:

1. Сверить `execution_lock`, intended owner и operation manifest.
2. Отклонить непустые `DOCKER_HOST`, `DOCKER_CONTEXT`, `DOCKER_TLS_VERIFY`, `DOCKER_CERT_PATH`; отклонить `COMPOSE_FILE`, `COMPOSE_PROJECT_NAME`, `COMPOSE_PROFILES`, `COMPOSE_ENV_FILES`, если они не являются exact значениями operation manifest.
3. Отклонить CLI config с proxy/credential-helper/plugin/context drift, если drift входит в identity/settings policy; не редактировать пользовательский config.
4. Выполнить только read-only handshake с явным `--context <approved-context>`; никогда не использовать current/global context неявно.
5. Сравнить endpoint URI/transport, Desktop product/build, `Server.Os=linux`, `Architecture=amd64`, Engine/Compose, daemon ID/name, root identity и settings hash с approved record.
6. Сверить exact Compose project name с allowlist: `n8nagents-local`, `n8nagents-k4r-<authorized-run-id>` или `n8nagents-restore-<authorized-run-id>`. Произвольное имя запрещено.
7. Перечитать environment и daemon tuple непосредственно перед первым mutating request. Между последним guard и mutation не допускается отдельный shell step, callback или user prompt.
8. Передать child process явный context/project/files/profile из immutable operation manifest; сохранить hash аргументов после secret-field removal.
9. После операции повторно прочитать daemon identity. Drift после mutation даёт `STOP_DAEMON_DRIFT`, запрещает следующую mutation и запускает только redacted evidence capture.

Global current context может изменяться пользователем между командами: wrapper всё равно использует explicit approved context. Но наличие env override является отдельным fail-closed сигналом и блокирует выполнение, даже если CLI precedence технически позволило бы `--context`.

### 3.3. Control-plane boundary

Доступ к approved named pipe рассматривается как root-equivalent доступ ко всем данным Docker backend. `V1` не обещает изоляцию секретов от authorized Docker control principals. Множество таких principals должно быть точным, минимальным и зафиксированным; неизвестный principal или широкая группа даёт `BLOCKED_CONTROL_PLANE`.

## 4. V1-002 — machine-readable Windows eligibility predicate

### 4.1. Frozen rules snapshot

До preflight, без скачивания installer, supply-chain owner формирует и хеширует `windows_eligibility_rules/v2` из датированных официальных требований Docker/Microsoft и принятой resource/data-classification policy. Snapshot содержит source evidence IDs, revision/time, exact comparisons и не может использовать слова «актуальная версия» без значения.

### 4.2. Обязательная запись наблюдений

`windows_eligibility_observation/v2` содержит минимум:

```yaml
identity:
  plan_sha256: <exact>
  rules_snapshot_sha256: <exact>
  collector_sha256: <exact>
  collected_at_utc: <exact>
  intended_owner_ref: <keyed pseudonym>
os:
  edition: {state: <tri-state>, value: <redacted exact>}
  build: {state: <tri-state>, value: <exact>}
  architecture: {state: <tri-state>, value: <exact>}
  servicing_channel: {state: <tri-state>, value: <exact>}
  servicing_stack_or_revision: {state: <tri-state>, value: <exact>}
  pending_reboot: {state: <tri-state>, value: <bool>}
hardware:
  cpu_architecture: {state: <tri-state>, value: <exact>}
  logical_cpu_count: {state: <tri-state>, value: <int>}
  virtualization_capable: {state: <tri-state>, value: <bool>}
  virtualization_firmware_enabled: {state: <tri-state>, value: <bool>}
  required_cpu_features: {state: <tri-state>, value: <set>}
memory:
  physical_total_bytes: {state: <tri-state>, value: <int>}
  available_bytes_at_observation: {state: <tri-state>, value: <int>}
features:
  wsl_optional_feature: {state: <tri-state>, value: <exact enum>}
  virtual_machine_platform: {state: <tri-state>, value: <exact enum>}
  hypervisor_boot_state: {state: <tri-state>, value: <exact enum>}
wsl:
  command_present: {state: <tri-state>, value: <bool>}
  component_version: {state: <tri-state>, value: <exact|null>}
  kernel_version: {state: <tri-state>, value: <exact|null>}
  default_version: {state: <tri-state>, value: <exact|null>}
  update_required_by_rules: {state: <tri-state>, value: <bool>}
  update_source_available_and_permitted: {state: <tri-state>, value: <bool>}
policy:
  device_management_state: {state: <tri-state>, value: <redacted enum>}
  app_control_readable: {state: <tri-state>, value: <bool>}
  antivirus_state_readable: {state: <tri-state>, value: <bool>}
  installer_execution_permitted: {state: <tri-state>, value: <bool>}
  wsl_feature_change_permitted: {state: <tri-state>, value: <bool>}
license:
  owner_decision_record: {state: <tri-state>, value: <evidence-ref|null>}
existing_install:
  discovery_record_sha256: {state: <tri-state>, value: <hash|null>}
storage:
  roots_record_sha256: {state: <tri-state>, value: <hash|null>}
  resource_evaluation_sha256: {state: <tri-state>, value: <hash|null>}
```

Serial numbers, product keys, usernames, raw SID, MAC/IP и device IDs не сохраняются.

### 4.3. Predicate

```text
ELIGIBLE =
  all required fields KNOWN_VALID
  AND OS tuple is in rules.supported_os_tuples
  AND CPU/virtualization predicates satisfy rules
  AND RAM/resource equation passes
  AND feature/WSL state is either already sufficient
      OR has one exact separately approvable transition path
  AND no unknown pending reboot
  AND policy is readable and permits the exact path
  AND license decision record is valid for the exact terms revision
  AND existing-install branch is FRESH_APPROVABLE or UPGRADE_APPROVABLE
  AND every storage root passes qualification.
```

`UNKNOWN` никогда не равен `false` и никогда не даёт default. Итоги:

- все predicates true: `PASS_ELIGIBLE`, RC `0`, без host changes;
- любой unknown/unreadable/conflict: `BLOCKED_UNKNOWN`, RC `31`;
- известное несоответствие требованиям: `BLOCKED_UNSUPPORTED`, RC `32`;
- policy/security restriction: `BLOCKED_POLICY`, RC `34`;
- resources/storage fail: `BLOCKED_RESOURCE`/`BLOCKED_STORAGE`, RC `35/45`;
- требуется владелец, license, feature delta или upgrade choice: `READY_FOR_MANUAL_GATE`, RC `10`; это не разрешение на mutation.

## 5. V1-005 — existing-install discovery и взаимоисключающие ветки

Read-only discovery не запускает, не repair-ит и не обновляет Docker. Оно инвентаризирует:

- installed-application/MSI/installer records, publisher, version, channel и install location;
- найденные Docker/Desktop/Compose/BuildKit executables, file IDs, signatures, versions и PATH precedence;
- services, drivers, scheduled tasks, startup entries, processes и named pipes;
- process/user/machine environment overrides и Docker CLI config/contexts/plugins;
- WSL distributions, state, owner, registered base/data locations и `docker-desktop*` objects;
- Docker Desktop settings/policies, configured managed-data location и update state;
- user config/data/cache roots, ACL owner, physical volume, reparse/sync status;
- при уже доступном approved local daemon — только read-only object counts/labels/volume ownership; daemon не запускается ради discovery;
- conflicting engines (Rancher/Podman/Colima/remote contexts или неизвестные services) без их изменения.

Классификатор выдаёт ровно одну ветку:

| Ветка | Условия | Следующий шаг |
|---|---|---|
| `FRESH_APPROVABLE` | отсутствуют app/executables/services/contexts/managed WSL objects/user data/conflicting engines; каждый probe `KNOWN` | предложить exact fresh-install delta |
| `UPGRADE_APPROVABLE` | один полностью идентифицированный vendor install; intended owner/данные/roots/version/settings известны; backup+cold-restore и vendor-supported migration path подготовлены; exact upgrade отдельно разрешён | перейти только через `MG-V1-UPGRADE` |
| `ALREADY_QUALIFIED` | установленная версия и вся identity/config уже совпадают с approved locks; endpoint guard проходит | install не выполняется, начать qualification/drift gate |
| `BLOCKED_EXISTING_STATE` | partial/old/stopped/foreign install, неизвестный owner/data, alternate root, migration ambiguity, conflicting engine, unreadable object или необходимость запуска/repair для выяснения | STOP без launch/repair/uninstall |

Запрещено автоматически выбирать fresh-install по отсутствию одного executable или пустому `docker ps`.

## 6. V1-003/V1-011 — WSL/features/reboot как plan-hash state machine

### 6.1. Состояния

```text
S0 DISCOVERED_READ_ONLY
  -> S1 DELTA_PROPOSED
  -> S2 DELTA_OWNER_APPROVED
  -> S3 PRE_MUTATION_REVALIDATED
  -> S4 NARROW_ELEVATED_ACTION_RUNNING
  -> S5 ACTION_RESULT_CAPTURED
  -> S6 REBOOT_REQUIRED | S8 POST_ACTION_REVALIDATED
S6 -> S7 OWNER_REBOOT_CONFIRMED -> STOP_FOR_REBOOT
NEW SESSION -> S7R RESUME_CHECKED -> S8 POST_ACTION_REVALIDATED
S8 -> S9 NEXT_EXACT_DELTA_PROPOSED | S10 WINDOWS_PREREQUISITES_QUALIFIED
ANY -> BLOCKED_* | STOP_* | FAILED_OPERATION
```

Никакого обещания «одна перезагрузка» нет. Каждая новая feature/package/update mutation — отдельный `delta_id`, owner approval и state transition.

### 6.2. Exact delta record

`windows_change_delta/v2` включает plan/rules/observation hashes, before-state, exact executable absolute path+hash+signer, exact arguments, required elevation identity role, projected files/features/services/WSL objects, reboot semantics, vendor rollback limits и timestamp expiry. Допустимы только необходимые для plan A штатные WSL 2/Virtual Machine Platform изменения. BIOS/UEFI, отдельный distro, Hyper-V VM, pagefile, security exclusions и plan B не входят.

### 6.3. UAC boundary

- Полная orchestration никогда не работает elevated.
- Неэскалированный intended owner готовит record и выполняет guard.
- UAC запускает только один exact signed executable с exact hash/arguments из approved delta.
- Over-the-shoulder admin credential не становится owner лаборатории.
- Cancelled UAC даёт `BLOCKED_MANUAL`, повтор только после нового immediate confirmation.
- Непредвиденный helper/download/payload/delta даёт `STOP_SCOPE_EXPANSION` до нового supply-chain/change review.

### 6.4. Reboot ceremony и checkpoint

Автоматический reboot и auto-resume запрещены. Перед каждой перезагрузкой владелец видит exact delta/result, ожидаемое прерывание, rollback limits, подтверждает сохранение своей работы, питание и готовность вручную перезагрузить систему.

Checkpoint не содержит секретов и включает:

```text
checkpoint_sha256 = SHA256(plan_sha256 + authorization_sha256 +
  delta_sha256 + before_state_sha256 + action_result_sha256 +
  intended_owner_ref + expected_next_state + nonce + expiry_utc)
```

После boot никакая mutation не продолжается автоматически. В новой неэскалированной сессии заново проверяются owner, plan/authorization/checkpoint, OS/build/servicing, pending reboot, features, WSL version/update, policies, existing-install inventory и Docker endpoint (если существует). Любое расхождение делает checkpoint stale и даёт `BLOCKED_POST_REBOOT_DRIFT`. Продолжение требует нового owner gate.

## 7. V1-004 — identities, ownership и control-plane principals

Роли различаются обязательно:

| Роль | Право | Запрет |
|---|---|---|
| `INTENDED_DAILY_OWNER` | неэскалированный запуск Desktop/lab CLI, владение user-only control root | не считается admin автоматически |
| `ELEVATION_CREDENTIAL` | только UAC для exact approved installer/feature action | не запускает orchestration, first launch и lab workload |
| `SYSTEM_COMPONENT` | только vendor-documented service/files с observed ACL | не получает lab secrets сверх необходимого approved channel |
| `DOCKER_CONTROL_PRINCIPAL` | доступ к approved local daemon; root-equivalent trust | список не расширяется автоматически |
| `UNAUTHORIZED_LOCAL_USER` | никакого lab/secret/control-plane доступа | не наследует broad ACL/group access |

Exact SID и account names хранятся в локальном user-only control record. Evidence содержит `role`, HMAC-pseudonym, membership/ACL summary и before/after diff, но не raw identity.

Обязательные условия:

1. Intended owner определяется до download и остаётся тем же до first launch/endpoint qualification.
2. Install под другим elevation credential не может создавать lab config/data в его profile; после UAC проверяются все profile roots.
3. First launch выполняет intended owner неэскалированно.
4. Любое изменение local groups/ACL inheritance/sign-out requirement заранее входит в exact delta; скрытое добавление в группу запрещено.
5. Если vendor semantics требуют более широкого control-plane доступа, чем owner одобрил, результат `BLOCKED_CONTROL_PLANE`.
6. User-only roots имеют explicit ACL intended owner + только доказанно необходимый SYSTEM access; inherited broad ACE, unknown SID или reparse ancestor блокирует.
7. Проверка unauthorized local user выполняется fixture/simulated ACL evaluation; создание реального дополнительного Windows пользователя в plan A не разрешено.

## 8. V1-006 — install/uninstall и rollback semantics

### 8.1. Fresh install transaction

До запуска installer должны существовать `FRESH_APPROVABLE`, exact supply-chain lock, license gate, roots/resource PASS, intended-owner/control-plane model, exact delta и before-state manifest. Installer запускается один раз по verified absolute file identity. Первый launch и создание data выполняются отдельной стадией; install success ещё не означает endpoint qualification.

### 8.2. Upgrade transaction

Upgrade запрещён по умолчанию. Он разрешается только при `UPGRADE_APPROVABLE`, cold-restore-ready backup, migration compatibility, retained last-known-good artifacts и `MG-V1-UPGRADE`. In-place downgrade не обещается. Неудачный upgrade даёт restore-first recovery plan и STOP; никакого автоматического repair/uninstall.

### 8.3. Три разных понятия

- `APPLICATION_REMOVAL`: vendor uninstall exact version.
- `FEATURE_ROLLBACK`: выключение WSL/VMP или удаление WSL update. По умолчанию запрещено, потому что может затронуть другие приложения.
- `DATA_RECOVERY`: восстановление лабораторных данных из проверенного backup; не является uninstall.

Ни одно из них не называется «недеструктивным rollback» без отдельного доказательства.

### 8.4. Стадии отказа

| Стадия | Разрешённое автоматическое действие | Требуемое решение |
|---|---|---|
| Download до запуска | удалить exact acquired file только после повторной проверки file/parent identity; иначе quarantine-in-place | integrity evidence |
| Feature/action partial | прекратить дальнейшие actions, сохранить state/delta evidence | `MG-V1-RECOVERY`; не выключать features автоматически |
| Installer partial | остановить дальнейший launch/retry/repair | vendor recovery review |
| Installed, first launch не выполнен | controlled stop, before/after inventory | uninstall только `MG-V1-UNINSTALL` |
| Data/backend создан | сохранить данные и endpoint offline | backup/recovery gate; uninstall не считается data rollback |
| Upgrade failure | не downgrade/uninstall автоматически | isolated restore-first gate |

В текущем plan A нет disposable Windows VM/Sandbox, поэтому byte-identical доказательство install→uninstall на disposable host недоступно. Следствие fail-closed: `V1` **не обещает** восстановление Windows в исходное состояние и не предлагает uninstall как automatic rollback. Если владелец потребует доказанный restorative uninstall, потребуется новый scope для disposable Windows environment; до этого residual status `ROLLBACK_EQUIVALENCE_UNVERIFIED`.

Pre-existing sentinel WSL distributions, Docker configs/data roots, services, contexts и user files фиксируются до mutation и должны остаться byte/identity-equivalent; любое изменение вне approved delta даёт `STOP_OUTSIDE_TOUCHSET`.

## 9. V1-007/V1-008 — resources и Windows storage roots

### 9.1. Root qualification

До install разрешаются только canonical physical roots, перечисленные в `approved_roots_record`:

- installer staging;
- vendor application location;
- Docker-managed data/VHDX location;
- user-only control/secret root;
- redacted evidence root;
- encrypted backup destination;
- transient backup/build staging.

Для каждого root/каждого ancestor проверяются resolved final path, volume GUID/serial pseudonym, fixed-local drive, filesystem, owner/ACL, reparse/junction/symlink absence, cloud-sync/redirect/network/removable status, encryption/data-protection class, free-space policy и overlap с repo/Vault/другими roots. Vault, project repo, cloud-sync, shared, removable, network paths и reparse targets запрещены без нового owner data-location gate.

Secrets должны использовать отдельный secret-domain design `V6`; backup plaintext не записывается в Windows staging. Разрешён поток container/tmpfs/pipe → authenticated encrypted artifact → approved backup root. Если tool требует plaintext host staging, backup блокируется.

Перенос managed data root после qualification считается destructive migration и требует нового plan/delta/backup/restore gate.

### 9.2. Исполнимый resource budget

Все значения хранятся в bytes, а не в отображаемых GiB. Перед install утверждается `resource_policy/v2`:

```text
host_reserve = max(20 GiB, ceil(15% * capacity_of_each_affected_volume))
projected_peak =
  vendor_application_peak
  + managed_backend_bootstrap_peak
  + steady_image_and_volume_cap
  + worst_case_pull_build_transient
  + encrypted_backup_output_cap
  + backup_encryption_transient
  + isolated_restore_duplicate_cap
  + logs_and_evidence_cap
  + operation_specific_growth
  + 10% forecast_error_margin

ALLOW_GROWTH iff
  every component KNOWN
  AND free_before - projected_peak >= host_reserve
  AND current_managed_usage + operation_growth <= approved_managed_cap.
```

Exact component values поступают из supply-chain sizes, measured existing-state inventory и owner-approved quotas; неизвестный размер блокирует growth. Проверка выполняется перед install, pull/build, start with migration, backup и restore, затем ещё раз непосредственно перед first write.

Hard high-water mark: при достижении `min(approved_managed_cap, free-host_reserve)` новые growth operations прекращаются. Cleanup только preview + exact labelled object list + owner approval. `system prune`, broad VHDX deletion и automatic data-root compaction запрещены. VHDX reclaim/compact — отдельная остановка Docker, backup и manual change gate.

## 10. V1-009/V1-010/V1-012 — drift, security policy и port guard

### 10.1. Drift/update

Qualified inventory включает Desktop build/channel/update settings, Engine/CLI/Compose/BuildKit, WSL component/kernel, endpoint identity, settings hash, data-root identity и rules/supply-chain hashes. `lab start`, `verify`, `backup`, `restore` и cleanup сначала сравнивают этот tuple. Любой drift даёт `BLOCKED_DRIFT` до workload mutation.

Controlled update — новый acquisition lock, owner approval, quiesced backup+cold restore readiness, exact update delta, после чего повторяются endpoint/capability/exposure/resource/backup regressions. Auto-update либо технически выключен утверждённой setting, либо его возможный drift всегда обнаруживается до start. Если vendor не позволяет безопасно отключить update, это фиксируется как residual risk, но fail-closed start остаётся обязательным.

### 10.2. App Control/antivirus

Policy unreadable/contradictory даёт `BLOCKED_POLICY_UNKNOWN`. Quarantine, execution block или tamper event даёт `STOP_SECURITY_POLICY` после первой попытки; тот же файл не запускается повторно. Automation никогда не отключает защиту и не создаёт exclusions. Исключение возможно лишь через отдельное организационное/owner решение вне этого плана, затем artifact заново получается из official source и повторяет все integrity/identity checks. Evidence содержит только redacted policy state и релевантный event class, без support bundle с PII/secrets.

### 10.3. Port `5678`

Read-only preflight не резервирует порт. Непосредственно перед container create/start guard проверяет IPv4 и IPv6 listeners/owners, Docker published ports, portproxy и approved project labels. Возможны только:

- порт свободен → разрешить exact `127.0.0.1:5678` bind;
- listener принадлежит тому же approved daemon/project/service/container identity → idempotent status/start;
- любой другой/неопределённый owner, `[::]`, `0.0.0.0`, LAN/VPN/WSL address или portproxy → `BLOCKED_PORT`, RC `44` до container start.

Автовыбор другого порта, IPv6 wildcard и firewall remediation запрещены. Изменение порта — новый reviewed configuration lock и owner decision.

## 11. Manual gates

| Gate | Когда | Exact предмет подтверждения |
|---|---|---|
| `MG-V1-PLAN` | до любых действий plan v2 | frozen full-plan hash и scope A-only |
| `MG-V1-LICENSE` | до acquisition/install | exact Docker terms revision, eligibility basis; automation не принимает terms |
| `MG-V1-EXISTING-UPGRADE` | только upgrade branch | exact owned install/data, backup/restore, migration/downgrade limits |
| `MG-V1-WINDOWS-DELTA` | перед каждой feature/WSL mutation | exact delta bytes/hash, executable/args, touchset, rollback limits |
| `MG-V1-UAC` | непосредственно перед UAC | одна narrow elevated action, intended/elevation role split |
| `MG-V1-REBOOT` | перед каждой перезагрузкой | saved work/power/readiness, checkpoint hash; owner перезагружает вручную |
| `MG-V1-POST-REBOOT` | после нового read-only resume check | revalidated tuple и next exact delta |
| `MG-V1-INSTALL` | перед installer execution | fresh/upgrade branch, supply lock, resource/root PASS, exact switches |
| `MG-V1-UNINSTALL` | перед vendor uninstall | data preservation, known leftovers, destructive limits; не automatic rollback |
| `MG-V1-RECOVERY` | partial install/action | exact current state и vendor-supported next step |
| `MG-V1-STORAGE-RISK` | при отличии data protection от approved class | конкретный root/class/residual; не разрешает reparse/shared/network root автоматически |
| `MG-V1-UPDATE` | любой version/settings update | new locks, backup/restore, regression matrix |
| `MG-V1-PORT-CHANGE` | если `5678` нельзя использовать | новый explicit port/config plan; auto-fallback запрещён |

Gate истекает при изменении plan/delta/lock/owner/host observation/endpoint hash или времени expiry. Подтверждение одного gate не включает следующий.

## 12. Result schema, статусы и RC

Каждая команда выдаёт один JSON object в stdout после redaction; human text идёт отдельно и не определяет результат:

```yaml
schema: n8nagents.v1-result/v2
run_id: <uuid>
operation_id: <allowlisted id>
plan_sha256: <exact>
authorization_ref: <redacted ref|null>
execution_lock_sha256: <hash|null>
decision: PASS | READY_FOR_MANUAL_GATE | BLOCKED | STOP | FAIL
status: <enum below>
rc: <integer below>
mutation_started: <bool>
first_mutation_utc: <timestamp|null>
observations_sha256: <hash>
pre_guard_sha256: <hash|null>
post_guard_sha256: <hash|null>
evidence_refs: [<EV IDs/artifact hashes>]
failed_predicates: [<stable IDs>]
next_safe_action: <one stable action ID>
redaction_policy_sha256: <hash>
```

| RC | Status | Семантика |
|---:|---|---|
| `0` | `PASS_READ_ONLY`, `PASS_MUTATION_VERIFIED` | только schema-valid и все обязательные postconditions |
| `10` | `READY_FOR_MANUAL_GATE` | mutation не разрешена |
| `31` | `BLOCKED_UNKNOWN` | обязательное поле unknown/unreadable/contradictory |
| `32` | `BLOCKED_UNSUPPORTED` | известное несоответствие rules |
| `33` | `BLOCKED_EXISTING_STATE` | fresh/upgrade нельзя доказать |
| `34` | `BLOCKED_POLICY`, `BLOCKED_POLICY_UNKNOWN` | policy запрещает или не читается |
| `35` | `BLOCKED_RESOURCE` | budget equation не проходит |
| `36` | `BLOCKED_MANUAL` | нет exact gate/owner action |
| `37` | `BLOCKED_PENDING_REBOOT`, `BLOCKED_POST_REBOOT_DRIFT` | продолжение запрещено |
| `38` | `BLOCKED_IDENTITY`, `BLOCKED_CONTROL_PLANE` | identity/ACL boundary не доказана |
| `41` | `BLOCKED_ENDPOINT` | endpoint/context/env invariant нарушен |
| `42` | `BLOCKED_DAEMON_DRIFT`, `BLOCKED_DRIFT` | qualified tuple изменился |
| `43` | `BLOCKED_PROJECT_IDENTITY` | project/profile/operation не allowlisted |
| `44` | `BLOCKED_PORT` | bind/owner/exposure не допустим |
| `45` | `BLOCKED_STORAGE` | root/data protection не прошли |
| `46` | `BLOCKED_ROLLBACK_EQUIVALENCE` | restorative rollback не доказан |
| `51` | `STOP_INTEGRITY`, `STOP_TOCTOU` | artifact/object identity нарушена |
| `52` | `STOP_SCOPE_EXPANSION`, `STOP_OUTSIDE_TOUCHSET` | действие вышло за authority |
| `53` | `STOP_SECURITY_POLICY` | block/quarantine/tamper; без retry |
| `61` | `FAILED_OPERATION` | разрешённая операция началась, postcondition не достигнута |
| `70` | `REBOOT_REQUIRED_STOPPED` | действие завершено, нужен ручной reboot; это не PASS всей стадии |

Любой ненулевой RC блокирует следующую mutation. Unknown status/RC, schema error, missing evidence или несовпадение decision/status/RC трактуется как `STOP_RESULT_INVALID` вызывающей стороной.

## 13. Acceptance tests, negative canaries и evidence

Tests до реального host execution работают на immutable fixtures/fake adapters и не создают Windows/Docker state. Host acceptance выполняется только после соответствующих manual gates.

### 13.1. Test/canary catalog

| ID | Положительный acceptance | Negative canary |
|---|---|---|
| `AT-V1-001` | start/stop/backup/restore/image/cleanup используют один approved explicit local context; global current-context drift не перенаправляет | `NC-V1-001`: injected `DOCKER_HOST`, `DOCKER_CONTEXT`, remote/TCP/SSH/unknown context и daemon tuple drift дают RC `41/42` до первого mutating API request |
| `AT-V1-002` | полностью supported fixture даёт `PASS_ELIGIBLE` и no-change attestation | `NC-V1-002`: unsupported, below-threshold, unreadable и contradictory поля дают RC `31/32/35` до network/installer |
| `AT-V1-003` | table cases already-enabled/disabled/update-required/reboot resume следуют exact state machine | `NC-V1-003`: stale plan hash, unapproved delta, second reboot need, policy block или changed post-boot state запрещают resume |
| `AT-V1-004` | intended owner после first launch владеет только approved roots/endpoint; no elevation-profile state | `NC-V1-004`: alternate UAC account, broad ACL/group, unknown principal и unauthorized-user access дают RC `38` |
| `AT-V1-005` | clean, known approved upgrade и already-qualified fixtures попадают ровно в свои branches | `NC-V1-005`: partial/stopped-old/unknown-owned/alternate-root/conflicting-engine fixture всегда `BLOCKED_EXISTING_STATE`, без launch/repair |
| `AT-V1-006` | static/state tests подтверждают раздельные application/feature/data recovery semantics и отсутствие automatic rollback claim | `NC-V1-006`: sentinel existing WSL/config/data + partial install запрещают uninstall/feature disable без gate; external sentinel unchanged; restorative equivalence остаётся RC `46` без disposable evidence |
| `AT-V1-007` | boundary values выше high-water сохраняют measured host reserve на install/pull/start/backup/restore | `NC-V1-007`: каждое значение на 1 byte ниже reserve/cap блокирует до write; unknown forecast тоже блокирует |
| `AT-V1-008` | approved canonical fixed-local non-reparse roots дают PASS и no-plaintext-backup-staging proof | `NC-V1-008`: broad ACL, junction/reparse ancestor, sync/shared/removable/network root, overlap repo/Vault или unapproved protection дают RC `45` |
| `AT-V1-009` | exact qualified Desktop/Engine/Compose/WSL/settings tuple разрешает start | `NC-V1-009`: изменение каждого version/channel/settings/root field блокирует start; update не снимает block без requalification |
| `AT-V1-010` | readable policy/no-block fixture проходит без protection changes | `NC-V1-010`: unreadable policy, quarantine, runtime block и exclusion request дают RC `34/53`, без exclusion/retry |
| `AT-V1-011` | no-reboot/reboot-required/cancelled-UAC cases имеют детерминированные stop/resume states | `NC-V1-011`: auto-reboot/auto-resume, stale checkpoint, changed owner/plan/prerequisite всегда отвергаются |
| `AT-V1-012` | free `5678` или exact already-running approved listener имеют корректный result; loopback binding проверен после start | `NC-V1-012`: unrelated IPv4/IPv6 listener после preflight даёт RC `44`, не выбирает другой port и не создаёт project |

### 13.2. Evidence catalog

| ID | Artifact | Обязательные поля |
|---|---|---|
| `EV-V1-001` | endpoint guard ledger | approved endpoint hash, pre/post daemon tuple hashes, env/context predicate results, operation/project hash, first-mutation marker |
| `EV-V1-002` | eligibility evaluation | rules/source refs, redacted observations, per-predicate tri-state, decision/RC, no-change attestation |
| `EV-V1-003` | Windows change ledger | before/delta/approval/action/checkpoint/post-state hashes, reboot count observed, resume result |
| `EV-V1-004` | identity/ACL ledger | role pseudonyms, owner/elevation/SYSTEM/control-plane separation, before/after membership+ACL diff, profile-root checks |
| `EV-V1-005` | existing-install inventory | all discovery categories, object identity/provenance/ownership state, exclusive branch and reason |
| `EV-V1-006` | install/removal/recovery ledger | stage, before/after touchset, sentinel results, vendor limits, explicit `ROLLBACK_EQUIVALENCE_UNVERIFIED` where applicable |
| `EV-V1-007` | resource evaluation ledger | resolved volumes, free/cap/reserve/component/peak bytes, operation, before/after usage, decision |
| `EV-V1-008` | approved roots/data map | redacted canonical path refs, volume identity, ACL/reparse/sync/drive/protection checks, plaintext-staging scan result |
| `EV-V1-009` | qualified runtime/drift inventory | version/channel/settings/WSL/endpoint/root tuple, baseline hash, changed fields, update qualification ref |
| `EV-V1-010` | security policy ledger | readability, policy class, redacted block/quarantine event class, no-control-change attestation |
| `EV-V1-011` | UAC/reboot ceremony | immediate command/delta hash, owner confirmations, checkpoint, no-auto-reboot/no-auto-resume proof |
| `EV-V1-012` | port/exposure ledger | immediate pre-bind IPv4/IPv6 owners, published-port/portproxy state, project identity, post-bind result |

Все evidence artifacts имеют schema/version, bytes, SHA-256, UTF-8/LF policy, UTC, tool hash и redaction policy. Raw secrets, usernames, SID, IP/MAC, Docker credentials, environment values и unrestricted command output не сохраняются.

## 14. Полная coverage map source finding → contract/test/canary/evidence

| Source finding | Contract | Acceptance | Negative canary | Evidence | Disposition в V1 |
|---|---|---|---|---|---|
| `R1-WIN-001` | `V1-001` | `AT-V1-001` | `NC-V1-001` | `EV-V1-001` | `DESIGN_CLOSED`; runtime proof pending |
| `R1-WIN-002` | `V1-002` | `AT-V1-002` | `NC-V1-002` | `EV-V1-002` | `DESIGN_CLOSED`; observation pending |
| `R1-WIN-003` | `V1-003` | `AT-V1-003` | `NC-V1-003` | `EV-V1-003` | `DESIGN_CLOSED`; mutation prohibited now |
| `R1-WIN-004` | `V1-004` | `AT-V1-004` | `NC-V1-004` | `EV-V1-004` | `DESIGN_CLOSED`; exact identities pending |
| `R1-WIN-005` | `V1-005` | `AT-V1-005` | `NC-V1-005` | `EV-V1-005` | `DESIGN_CLOSED`; branch pending |
| `R1-WIN-006` | `V1-006` | `AT-V1-006` | `NC-V1-006` | `EV-V1-006` | `DESIGN_CLOSED_WITH_RESIDUAL`; no restorative rollback claim |
| `R1-WIN-007` | `V1-007` | `AT-V1-007` | `NC-V1-007` | `EV-V1-007` | `DESIGN_CLOSED`; exact measured budget pending |
| `R1-WIN-008` | `V1-008` | `AT-V1-008` | `NC-V1-008` | `EV-V1-008` | `DESIGN_CLOSED`; roots pending |
| `R1-WIN-009` | `V1-009` | `AT-V1-009` | `NC-V1-009` | `EV-V1-009` | `DESIGN_CLOSED`; runtime inventory pending |
| `R1-WIN-010` | `V1-010` | `AT-V1-010` | `NC-V1-010` | `EV-V1-010` | `DESIGN_CLOSED`; policy observation pending |
| `R1-WIN-011` | `V1-011` | `AT-V1-011` | `NC-V1-011` | `EV-V1-011` | `DESIGN_CLOSED`; ceremony pending |
| `R1-WIN-012` | `V1-012` | `AT-V1-012` | `NC-V1-012` | `EV-V1-012` | `DESIGN_CLOSED`; immediate runtime check pending |

Покрытие: `12/12` source findings имеют минимум один contract, acceptance test, negative canary и evidence artifact. `DESIGN_CLOSED` не означает runtime `PASS` и не отменяет независимое ревью полного frozen plan v2.

## 15. Cross-domain зависимости

| Domain | Findings/contracts, от которых зависит V1 | Что V1 требует, но не владеет |
|---|---|---|
| V2 supply chain/license | `R2-001..007`, `R2-009`, `R2-011`, `R2-012` | exact installer/WSL payload locks, official source/trust roots, license record, installed-product identity, last-known-good artifacts |
| V3 isolation/network | `R3-CTRL-005`, `R3-PORT-004`, `R3-MOUNT-006`, `R3-NET-002`, `R3-NET-003` | control-plane subject audit, loopback/LAN canaries, mount containment и runtime network proof |
| V4 Compose/runtime | `R4-F01..F05`, `R4-F07`, `R4-F09`, `R4-F10` | exact project/profile convergence, health/migration state и stable status/doctor |
| V5 Telegram | `R5-F14`, `R5-F16` | zero-effect dry-run и owner ceremony поверх V1 endpoint guard |
| V6 secrets/PII | `R6-P1-001`, `R6-P1-002`, `R6-P1-005..008`, `R6-P2-011` | secret transport, authorized control-plane risk, data classification, redaction, no-plaintext staging |
| V7 backup/recovery | `R7-F01..F10`, `R7-F12` | cold-restore-ready backup до upgrade/update, encryption/key split, restore target identity |
| V8 evidence/K4R | `R8-P1-003`, `R8-P1-008`, `R8-P1-010`, `R8-P2-012` | immutable candidate/evidence binding и no-network/cleanup evidence |
| V9 repo custody | `R9-F01..F10` | wrapper/source touchset, immutable operation manifests, no writes в project/Vault вне разрешённой документации |
| V10 operability | `R10-F02`, `R10-F04..F09`, `R10-F11` | emergency stop, resource UX, drift/update UX, black-box handover и reboot ceremony |

Если cross-domain lock/evidence отсутствует, V1 выдаёт `BLOCKED_UNKNOWN` или `READY_FOR_MANUAL_GATE`, а не локально изобретает замену.

## 16. Residual risks и unresolved conflicts

1. `ROLLBACK_EQUIVALENCE_UNVERIFIED`: plan A запрещает disposable Windows VM/Sandbox, поэтому exact install→uninstall equivalence для выбранного installer нельзя безопасно доказать на текущем host до установки. Разрешение: uninstall не является rollback и требует отдельного destructive/manual gate. Полное снятие риска требует нового scope, который пользователь пока не подтвердил.
2. Docker control-plane principal имеет root-equivalent доступ к backend. ACL не изолирует secrets от уже authorized control principal; минимизация principals и secret-domain controls лишь уменьшают риск.
3. Vendor installer может иметь system-wide компоненты даже при per-user ownership UI/data. V1 не обещает «чисто per-user install»: фактический touchset должен совпасть с supply-chain/vendor evidence и exact delta, иначе STOP.
4. Windows/Docker/WSL security updates могут сделать qualified tuple stale. Fail-closed drift gate сохраняет безопасность, но может временно блокировать лабораторию.
5. Docker-managed VHDX и vendor support artifacts могут оставлять данные вне user-selected lab paths. Data map должна явно классифицировать такие remnants; невозможность доказать защиту блокирует sensitive real-dev mode.
6. Security policy может быть организационно скрыта. В этом случае автоматического обхода нет, установка остаётся `BLOCKED_POLICY_UNKNOWN`.
7. Resource forecast до pull/build основан на supply metadata и cap; реальный VHDX growth может отличаться. Повторный непосредственный high-water guard и hard host reserve обязательны, но не гарантируют отсутствие vendor-side temporary growth между измерениями.
8. Port `5678` имеет TOCTOU между Windows listener check и Docker bind. Guard минимизирует окно, post-bind проверка обнаруживает ошибку, но атомарной Windows reservation через Docker API нет; collision всегда fail-closed.

## 17. Definition of Done для V1 design и будущего runtime gate

### Design DoD

- `R1-WIN-001..012` имеют полную 4-way coverage contract/test/canary/evidence;
- есть explicit endpoint invariant для каждой Docker mutation;
- eligibility predicate машинно читаем и fail-closed на unknown/conflict;
- fresh/upgrade/already-qualified/ambiguous branches взаимоисключающие;
- WSL/features/reboot оформлены plan-hash-bound state machine без обещания числа reboot;
- owner/elevation/SYSTEM/control-plane identities разделены;
- install/uninstall/feature rollback/data recovery не смешаны;
- статусы/RC и manual gates однозначны;
- residual risks и cross-domain dependencies не скрыты;
- нет runtime claims и host mutations.

### Future runtime DoD

`V1_RUNTIME_PASS` возможен только после отдельно утверждённого frozen full plan v2 и соответствующих gates, когда schema-valid evidence докажет exact host eligibility, выбранную install branch, root/resource PASS, identity boundary, endpoint qualification, port exposure, drift baseline и отсутствие outside-touchset change. До этого статус этой секции только `DESIGN_READY_FOR_INTEGRATION_REVIEW`.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
