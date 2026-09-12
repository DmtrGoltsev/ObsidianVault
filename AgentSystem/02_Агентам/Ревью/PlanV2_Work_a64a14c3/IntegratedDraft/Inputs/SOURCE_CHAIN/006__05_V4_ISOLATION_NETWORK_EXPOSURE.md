---
id: "n8nagents-plan-v2-v4-isolation-network-exposure-a64a14c3"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V4 container isolation/network architect"
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
доказательства: []
теги: ["n8nagents", "plan-v2", "docker-desktop", "изоляция", "network", "egress", "exposure", "design-only"]
---

# V4 — изоляция контейнеров, сеть и host exposure

## 0. Статус, область и запрет на исполнение

Это implementation-ready проект секции `V4` для будущего полного plan v2. Он не разрешает read/write preflight, сеть, download, Docker, Windows, VPS, Telegram, DeepSeek, секреты, изменение project repository или установку. Фактические свойства Docker Desktop/WSL kernel, internal networks, IPv6, host forwarding, VPN, firewall, mount semantics и capabilities имеют статус `UNKNOWN` до отдельно утверждённого runtime qualification.

Секция относится только к плану A: Docker Desktop с его штатным WSL 2 backend. Отдельный пользовательский WSL-дистрибутив, VM, plan B и VPS не являются fallback. Если Docker Desktop не даёт обязательную boundary, результат — scoped `V4_*_BLOCKED_CAPABILITY`; исполнитель не расширяет privileges, не включает plan B и не переносит тест на VPS.

`V4` владеет:

- per-container privilege envelope;
- exact mount allowlist и Windows-to-container containment;
- exact service/network graph для `mock`, `real-dev`, `restore` и `gate`;
- no-egress/no-external-route proof;
- narrow destination egress для Telegram и опционального DeepSeek;
- loopback-only Windows exposure;
- mode convergence, cleanup network custody и scoped LAB/LOCAL/OFFLINE status.

Секция не владеет supply-chain provenance, значениями секретов, Telegram authorization/routing, DeepSeek budget, backup cryptography, Compose health graph, repo commit или production deployment. Она потребляет только frozen hashes/IDs соответствующих контрактов.

## 1. Проверенные design inputs

| Вход | Bytes | SHA-256/status | Результат |
|---|---:|---|---|
| `00_FINDINGS_BASELINE.json` | `213739` | `934c449aa75ad157b1702afefcbaac4eab80b750801f172226d065b5a528c4aa` | `READ` |
| `01_BASELINE_AUDIT.json` | `7607` | internal status `PASS`, `114/114` | `READ` |
| frozen plan v1 | `46234` | `a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79` | `READ` |
| quorum report | `21742` | `08a59e4838d42102f94bb0bb826201d5edec704fcd90a6fe401f8e05f4eff5e7` | `READ` |
| `R03.json` identity | `18954` | `6406e4e72c6b09f677dc444ecad75f54caba4aae0bf2ea5785fc559f77e0d6ee` | accepted from V0 audit |
| Existing V1/V2/V3 drafts | design-only | uncommitted sibling drafts | `READ_ONLY` |

Ни один runtime факт из таблицы не выводится. `READ` означает только использование текста как design input.

## 2. Реестр контрактов V4

| Contract | Обязательство |
|---|---|
| `V4-C01-ENDPOINT-CHAIN` | Каждая Docker mutation проходит через V1 approved local endpoint guard; redirect variables и direct daemon access запрещены. |
| `V4-C02-PRIVILEGE-ENVELOPE` | `Privileged=false`, non-root, `CapDrop=ALL`, exact minimal `CapAdd`, no devices/socket/host PID/IPC, no privilege escalation. |
| `V4-C03-MOUNT-MANIFEST` | У каждого service/run есть исчерпывающий exact mount manifest; неизвестный/implicit mount блокирует create. |
| `V4-C04-HOST-PATH-CUSTODY` | Windows bind source проходит handle-based reparse/symlink/hardlink/case/Unicode/ADS/TOCTOU guard. |
| `V4-C05-NETWORK-GRAPH` | Для каждого режима определены exact services, network membership, internal/external class и отсутствие implicit `default`. |
| `V4-C06-NO-EGRESS` | Mock/restore не имеют внешнего маршрута; autonomous gate имеет `network_mode=none`; runtime matrix и positive control обязательны. |
| `V4-C07-DESTINATION-EGRESS` | Real-dev выходит только через secretless reviewed brokers к exact Telegram/DeepSeek origin policy; direct route/IP/redirect/rebind запрещены. |
| `V4-C08-HOST-EXPOSURE` | Единственный host listener — `127.0.0.1:5678/tcp` n8n; Windows IPv4/IPv6/portproxy/firewall/VPN matrix fail closed. |
| `V4-C09-MODE-CONVERGENCE` | `mock`, `real-dev`, `real-dev+deepseek`, `restore`, `gate` взаимоисключены и сходятся к exact desired state через drain/remove без volume deletion. |
| `V4-C10-O5-CAPABILITY` | O5 не получает privileged-equivalent права; недоступная строка даёт только `OFFLINE_BLOCKED_CAPABILITY`, не ослабляя LAB/LOCAL. |
| `V4-C11-OBJECT-CUSTODY` | Run-scoped networks/containers/temp volumes создаются и удаляются только по full identity tuple и exact object IDs. |
| `V4-C12-STATUS-RC` | Scope/state/RC schema не допускает общий SUCCESS при blocked OFFLINE и не принимает stdout вместо evidence. |

## 3. Базовые инварианты

1. Любое обязательное наблюдение имеет состояние `KNOWN_VALID | KNOWN_INVALID | UNKNOWN`. `UNKNOWN`, skipped, unreadable, stale или contradictory блокирует соответствующий scope.
2. Любой container create/start требует совпадения plan, authority, endpoint, supply/runtime lock, Compose render, privilege manifest, mount manifest, network manifest и operation manifest.
3. Прямые вызовы Docker/Compose/SDK/named pipe вне versioned V1 guard запрещены static policy. Глобальный Docker context не изменяется.
4. Никакой application, proxy, mock, restore или gate container не запускается как UID `0`, username `root` либо с пустым `Config.User`, разрешающим root default.
5. `HostConfig.Privileged` всегда `false`. `CapDrop` всегда содержит `ALL`. `CapAdd` пуст, кроме одного заранее утверждённого row-specific capability из §5.4.
6. `devices`, `device_cgroup_rules`, Docker socket, Windows Docker named pipe, `/var/run/docker.sock`, host root, Docker-managed root/VHDX, project/Vault roots и host PID/IPC namespace запрещены.
7. `network_mode: host`, `service:*`, `container:*`, unreviewed `extra_hosts`, `host-gateway`, `links`, implicit default network, external pre-existing network и `attachable:true` запрещены.
8. Runtime root filesystem read-only. Writable locations существуют только в exact named volume/tmpfs manifest; executable code не загружается в writable mount.
9. `security_opt` содержит `no-new-privileges:true`; `seccomp=unconfined` и `apparmor=unconfined` запрещены. Отсутствие ожидаемого security mode даёт capability block, не silent downgrade.
10. Container restart policy не может самовосстановить real external traffic после disarm/stop. Для bridge/adapters/brokers разрешено только `restart: no`.
11. Mock/dry/restore/gate никогда не читают Telegram/DeepSeek secrets и не содержат real proxy configuration.
12. Production VPS, provider UI, DNS и remote Docker endpoint остаются недоступны этому разделу.

## 4. `V4-C01-ENDPOINT-CHAIN` — daemon и project identity

Каждая операция получает immutable tuple:

```yaml
schema: n8nagents.v4-operation/v2
plan_sha256: <full-plan-v2>
authority_sha256: <exact>
approved_endpoint_record_sha256: <V1>
supply_runtime_lock_sha256: <V2>
approved_roots_record_sha256: <V3>
compose_render_sha256: <exact>
privilege_manifest_sha256: <exact>
mount_manifest_sha256: <exact>
network_manifest_sha256: <exact>
project_name: n8nagents-local | n8nagents-restore-<run-id> | n8nagents-k4r-<run-id>
mode: STOPPED | MOCK | REAL_TG | REAL_TG_DEEPSEEK | RESTORE | GATE
run_id: <nonce>
candidate_sha256: <hash|null>
```

Перед каждой first mutation wrapper:

- отклоняет `DOCKER_HOST`, `DOCKER_CONTEXT`, `DOCKER_TLS_VERIFY`, `DOCKER_CERT_PATH` и неутверждённые `COMPOSE_*` overrides;
- использует explicit approved local Docker Desktop context из `V1-001`;
- сверяет named-pipe endpoint, daemon ID, `Server.Os=linux`, `Architecture=amd64`, Engine/Desktop/Compose build и Docker root identity;
- сверяет project name с operation tuple;
- перечитывает tuple непосредственно перед API request без user callback между guard и request;
- после mutation повторно сверяет daemon identity.

TCP/SSH/HTTP endpoint, remote context, неизвестный pipe или endpoint drift дают `V4_BLOCKED_ENDPOINT`, mutation count `0`. V4 не дублирует V1 endpoint implementation, но ни один его PASS без `EV-V1-001` не действует.

## 5. `V4-C02-PRIVILEGE-ENVELOPE`

### 5.1. Общий runtime profile

Каждый container имеет:

```yaml
privileged: false
user: "<exact-numeric-uid>:<exact-numeric-gid>" # оба > 0
cap_drop: [ALL]
cap_add: []
read_only: true
security_opt: [no-new-privileges:true]
pid: private
ipc: private
devices: []
device_cgroup_rules: []
pids_limit: <positive-approved-limit>
init: true
```

`pid: private`/`ipc: private` здесь означает отсутствие `host`/shared external namespace; если Compose omits explicit private keyword, runtime inspect обязан доказать private/default container namespace. `userns_mode: host`, `cgroupns: host`, sysctls, kernel modules, `/proc`/`/sys` write, `SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE`, `BPF`, `PERFMON`, `SYS_MODULE`, `DAC_READ_SEARCH`, `MKNOD` и `SETFCAP` запрещены.

Runtime inspect считается источником истины: Compose intent без `docker inspect`, in-container UID/GID, `CapEff/CapBnd/NoNewPrivs`, mount namespace и device inventory не даёт PASS.

### 5.2. Per-service privilege matrix

| Service class | UID/GID | CapAdd | Writable objects | Дополнительные запреты |
|---|---|---|---|---|
| `postgres` | pinned image-declared nonzero PostgreSQL UID/GID | none | `local_postgres_data`, exact tmpfs | no host bind, no secret-root directory, no external network |
| `n8n` | pinned image-declared nonzero n8n UID/GID | none | `local_n8n_data`, optional `local_n8n_files`, tmpfs | no Telegram/DeepSeek uplink, no shell/device/socket |
| `bootstrap/migrate` | exact nonzero application UID/GID | none | only declared DB connection; no persistent filesystem except exact migration marker if service domain requires | no root ownership repair/chown fallback |
| `mock-telegram/mock-llm` | baked nonzero UID/GID | none | tmpfs only | no real secret, no uplink |
| `telegram-bridge` | baked nonzero UID/GID | none | `local_bridge_state`, tmpfs, exact token file RO | no Docker control, no DeepSeek network |
| `deepseek-adapter` | baked nonzero UID/GID | none | tmpfs, exact API-key file RO | no Telegram network, no arbitrary URL input |
| `egress-telegram/egress-deepseek` | baked nonzero UID/GID | none | tmpfs only | no secrets, no application/data volumes, no TLS interception CA |
| `restore-*` | pinned nonzero service UID/GID | none | new restore volumes only | no source/live volume, host port, trigger or uplink |
| `gate-runner/validator` | baked nonzero UID/GID | none by default | candidate RO, invocation output RW, tmpfs | network none, no secret/persistent-lab mount |

Если official image не запускается non-root или требует root init/chown, это `V4_LAB_BLOCKED_CAPABILITY`. Запуск root-helper в том же backend не является remediation. Допустим новый Docker-only image design через V2 build/review, но не privilege relaxation.

### 5.3. Запрещённый privileged-equivalent

Любой запрос `Privileged=true`, `CAP_SYS_ADMIN`, host PID/IPC/network, Docker socket/named pipe, device passthrough, host cgroup/proc/sys, bind Docker VHDX/root или sidecar с этими правами даёт `V4_STOP_SCOPE_EXPANSION`. Наличие пустого persistent backend не меняет запрет: текущий план A не создаёт отдельный disposable daemon/backend.

### 5.4. Единственное допустимое row-specific исключение

Для isolated O5 row, проверяющего inode immutable flag, может быть **предложен**, но не автоматически выдан, только `CAP_LINUX_IMMUTABLE` при всех условиях:

- process UID/GID nonzero и владеет единственным invocation-owned disposable named volume;
- rootfs RO, network none, no other mount/device/socket;
- separate row manifest и capability probe доказывают exact effective/bounding set = только `LINUX_IMMUTABLE` после `CapDrop=ALL`;
- before/after foreign/persistent sentinels unchanged;
- cleanup имеет exact object custody.

Если Docker/kernel/filesystem не поддерживает эту комбинацию, строка `OFFLINE_BLOCKED_CAPABILITY`; добавлять `SYS_ADMIN`, root или privileged запрещено.

## 6. `V4-C03-MOUNT-MANIFEST`

### 6.1. Schema

До container create существует canonical manifest:

```yaml
schema: n8nagents.v4-mount-manifest/v2
service_id: <allowlisted>
project_name: <exact>
mode: <exact>
image_child_digest: sha256:<exact>
mounts:
  - mount_id: <stable>
    source_kind: NAMED_VOLUME | TMPFS | WINDOWS_FILE_BIND
    source_logical_id: <V3-DM/root-or-run-object-id>
    source_identity_sha256: <object/path-custody-hash>
    target: <absolute-normalized-posix-path>
    access: RO | RW
    type: file | directory
    options: [<closed-list>]
    purpose: <closed-enum>
```

Canonical rendered Compose, Docker create request и post-create inspect `Mounts` должны совпасть byte/field-for-field после allowed daemon normalization. Extra, missing, reordered-with-semantic-drift, implicit integration mount или unknown option блокирует start.

### 6.2. Allowlist

| Consumer | Source | Target | Access/options |
|---|---|---|---|
| `postgres` | named volume `local_postgres_data` | exact path из pinned image contract | RW; no propagation |
| `n8n` | named volume `local_n8n_data` | `/home/node/.n8n` либо exact pinned-image path | RW; no propagation |
| `n8n` | named volume `local_n8n_files`, только если service contract = PRESENT | exact application files path | RW; no propagation |
| `telegram-bridge` | named volume `local_bridge_state` | `/state` | RW; no propagation |
| Secret consumer | один `WINDOWS_FILE_BIND` на один secret slot | `/run/secrets/<ASCII-slot>` | RO file; noexec/nosuid/nodev where effective |
| Stateless services | tmpfs | `/tmp`, optional `/run` | RW, size+mode bounded, noexec/nosuid/nodev where compatible |
| Gate runner | candidate named volume | `/candidate` | RO |
| Gate runner | invocation output named volume | `/output` | RW; empty-at-start |
| Restore service | new restore-generation named volumes | exact application paths | RW; unique run only |

Windows directory bind mounts отсутствуют. Repo, Vault и candidate не bind-mounted. Trusted wrapper передаёт frozen candidate/runner через Docker archive API в new labelled volume/container while stopped; затем сверяет manifest/hashes и монтирует volume read-only. Evidence export идёт source-allowlisted Docker archive/API stream в V3 approved evidence root, не через writable project bind.

### 6.3. Target-side deny policy

Container target обязан быть absolute, single-normalized POSIX path без `..`, duplicate separator, symlink ancestor или overlap. Запрещены `/`, `/proc`, `/sys`, `/dev`, `/etc`, `/boot`, `/usr`, `/bin`, `/sbin`, `/lib*`, `/var/run/docker.sock`, `/run/docker.sock`, home SSH/config executable directories и любой image code path. Target type и owner/mode проверяются до application exec. Mount propagation только `rprivate/private`; shared/slave propagation запрещена.

### 6.4. Named-volume identity

Named volume разрешён только если:

- actual name соответствует exact project/run manifest;
- full labels включают scope, authority, plan, project, run, candidate, resource class, persistent/disposable;
- volume ID/name, creation timestamp, driver/options и mountpoint fingerprint совпадают custody record;
- foreign, missing-label, stale, collision или pre-existing unexpected volume блокирует create;
- persistent volumes никогда не подаются gate/restore как source, кроме explicit backup contract, который V4 здесь не разрешает.

## 7. `V4-C04-HOST-PATH-CUSTODY`

### 7.1. Допустимый Windows bind

Единственный допустимый host bind — individual secret file для exact consumer, если V6 доказал version-specific file transport. Общий `LAB_SECRET_ROOT`, repo, Vault, backup/evidence/download/temp root, profile directory, drive root, UNC, mapped/subst/removable/network/sync path и Docker-managed root не монтируются.

Leaf name ограничен ASCII `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`. Raw paths хранятся только в local protected V3 inventory; долговременное evidence содержит logical root и keyed path/file fingerprints.

### 7.2. Pre-create algorithm

Trusted non-elevated wrapper для root, каждого ancestor и leaf:

1. Принимает только absolute local NT path из approved V3 record; environment expansion, wildcard, relative path, UNC, device namespace, `GLOBALROOT`, named pipe и colon вне drive separator запрещены.
2. Открывает handle без следования reparse point; сверяет fixed NTFS volume identity, exact file ID, type, owner/DACL и approved root containment.
3. Отклоняет любой reparse tag, junction, symlink, mount point, Cloud Files placeholder, recall/sync attribute и unknown filesystem.
4. Сравнивает ordinal-exact case и Unicode NFC round-trip каждого component; alternate normalization/case/8.3 alias ambiguity блокирует. NTFS ADS запрещены.
5. Для leaf требует regular file, link count `1`, no executable attribute, exact size ceiling и expected owner/ACL; directory bind запрещён.
6. Удерживает leaf и ancestor handles без delete/write sharing через Docker create, post-create inspect и pre-start validation. Если Docker Desktop не совместим с таким custody, file-bind capability = BLOCKED; sharing не ослабляется.
7. Непосредственно до API create и после create повторяет file/parent/volume IDs, timestamps, DACL hash и reparse state. Любое изменение — `V4_FAIL_CONTAINMENT`, container не стартует.
8. В stopped validation container либо daemon mount inspection проверяет target type и non-secret canary identity. Secret bytes/hash не попадают в evidence.
9. После start проверяет, что только exact consumer видит exact target RO; соседний container, child environment, `/proc`, inspect и logs не содержат canary.

### 7.3. TOCTOU threat boundary

Handle custody защищает от обычной rename/delete/substitution гонки для non-privileged concurrent writer. Windows kernel, SYSTEM, approved Administrator и Docker control-plane principals остаются trusted boundary и могут обойти user-mode protection; это residual risk из V1/V3/V6, а не абсолютная гарантия.

### 7.4. Negative fixture matrix

Обязательны junction parent наружу, symlink leaf, external hardlink, case-only collision, NFC/NFD collision, 8.3 alias, named ADS, writable/common parent, directory swap во время паузы, leaf replacement, broad root mount и extra Compose bind. Каждый case даёт zero container start и unchanged outside sentinel.

## 8. `V4-C05-NETWORK-GRAPH`

### 8.1. Network classes

Compose project `n8nagents-local` использует только эти logical network keys; actual object name по умолчанию `<project>_<key>`, и wrapper сверяет его с project labels:

| Key | Class | `internal` | Exact members по режиму | Назначение |
|---|---|---:|---|---|
| `db` | application-data | true | `postgres`, `n8n`, bounded `bootstrap/migrate` | DB only |
| `mock_tg` | synthetic | true | `n8n`, `mock-telegram` | mock Telegram |
| `mock_llm` | synthetic | true | `n8n`, `mock-llm` | mock LLM |
| `telegram_ingress` | application-adapter | true | `n8n`, `telegram-bridge` | authenticated internal update/reply contract |
| `telegram_proxy` | controlled-client | true | `telegram-bridge`, `egress-telegram` | bridge can reach only Telegram broker |
| `llm_ingress` | application-adapter | true | `n8n`, `deepseek-adapter` | constrained internal LLM contract |
| `llm_proxy` | controlled-client | true | `deepseek-adapter`, `egress-deepseek` | adapter can reach only DeepSeek broker |
| `uplink` | controlled-external | false | only active `egress-*` brokers | единственный Internet-capable container path |

`restore` использует отдельный project `n8nagents-restore-<run-id>` и только `restore_db` с `internal:true`. `gate` использует `network_mode:none` и не создаёт network object. Если multi-process validator требует связь, она реализуется одним container/IPC/filesystem contract; добавление сети — новый reviewed row, не implicit fallback.

### 8.2. Exact desired states

| Mode | Running service set | Network set | Host ports | Real secrets/egress |
|---|---|---|---|---|
| `STOPPED` | none | none | none | arm expired; none |
| `MOCK` | `postgres`, completed `bootstrap/migrate`, `n8n`, `mock-telegram`, `mock-llm` | `db`, `mock_tg`, `mock_llm` | `127.0.0.1:5678` | none |
| `REAL_TG` | `postgres`, completed `bootstrap/migrate`, `n8n`, `telegram-bridge`, `egress-telegram` | `db`, `telegram_ingress`, `telegram_proxy`, `uplink` | `127.0.0.1:5678` | Telegram bridge only |
| `REAL_TG_DEEPSEEK` | `REAL_TG` plus `deepseek-adapter`, `egress-deepseek` | `REAL_TG` networks plus `llm_ingress`, `llm_proxy` | `127.0.0.1:5678` | Telegram bridge + DeepSeek adapter |
| `RESTORE` | exact restore PostgreSQL + offline structural validator; n8n only with triggers disabled by V5 contract | `restore_db` only | none | only independently supplied instance key; no provider secret/egress |
| `GATE` | one exact runner/validator container at a time | none (`network_mode:none`) | none | none |

В strict plan A real Telegram path использует bridge как единственный Telegram API consumer и outbound adapter. n8n Telegram node с direct external connection запрещён. Если product owner позже требует exact n8n node, это новый cross-domain design: n8n всё равно не получает external network, а совместимость с narrow adapter/proxy должна быть отдельно доказана.

DeepSeek path аналогично проходит через narrow `deepseek-adapter`; n8n не присоединяется к `uplink`, `telegram_proxy` или `llm_proxy`. Adapter validation, model/budget/data-class contracts принадлежат V6.

### 8.3. Compose/network static rules

- Every service has an explicit `networks` list or exact `network_mode:none`.
- Rendered Compose must not contain/create `default`, external networks, `attachable:true`, aliases equal to provider/host names, `extra_hosts`, `links`, `network_mode:host/service/container` or static route/sysctl changes.
- `uplink` membership exact-set equals active `egress-*` brokers. Application/data/secret-bearing services never join `uplink`.
- PostgreSQL belongs only to `db`; mocks belong only to their synthetic network; egress brokers never join `db`.
- Docker embedded DNS may resolve peers only inside networks shared by the caller. External provider names are resolved only by their egress broker.
- Mock/restore/gate clear all case variants of `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY` and tool-specific proxy variables. Real adapter uses only a hash-bound explicit proxy client configuration; generic proxy inheritance is rejected.
- Runtime inspect service/network bipartite graph must equal manifest. An extra attachment is a containment failure even if probes currently fail.

## 9. `V4-C06-NO-EGRESS`

### 9.1. Exact meanings

- `NETWORK_NONE`: only loopback interface is present, no non-loopback route/default route/resolver/external peer. Used by autonomous `GATE`.
- `INTERNAL_ONLY`: exact non-loopback interfaces/routes may exist only for approved Docker internal networks and peers; no usable external/host path. Used by `MOCK` and `RESTORE`.
- `CONTROLLED_EGRESS`: secret-bearing adapter has only internal peers plus a named broker; only secretless broker has external route. Used by real-dev.

Фраза «без NIC» запрещена. Gate evidence заявляет `no non-loopback interface/default route`, если это наблюдено. Mock/restore evidence заявляет `internal-only exact peers`, а не no-NIC.

### 9.2. Trusted observation

Для каждого container collector связывает с execution fingerprint:

- Docker `NetworkMode`, endpoint IDs, network IDs, internal/attachable flags, aliases, IPAM, gateway and DNS fields;
- in-namespace `link`, addresses, routes, rules, resolver, `/etc/hosts`, proxy environment names без значений и listening/established socket classes;
- Desktop/Engine/kernel/storage/security identities из V1/V2/V8 dependencies;
- before/after host published ports/listeners.

Collector image/tool hash входит в V2 tool BOM. Missing `ip`, IPv6 support, socket probe, namespace field или collector error даёт `V4_BLOCKED_UNKNOWN`, не skipped PASS.

### 9.3. Required probe matrix

Из каждого applicable service выполняются bounded DNS/UDP/TCP/TLS probes:

| Destination class | GATE | MOCK/RESTORE | REAL secret consumer | Positive control |
|---|---|---|---|---|
| approved internal peer name/IP | N/A | PASS only exact peer | PASS only exact adapter/broker peer | PASS |
| unshared Docker sentinel name/IP | DENY | DENY | DENY | PASS after explicit control attachment |
| public DNS name via resolver | DENY/no resolver | DENY | consumer DENY direct; broker resolution policy only | controlled broker PASS |
| literal public IPv4/IPv6 | DENY | DENY | consumer DENY; CONNECT numeric literal DENY | exact control probe PASS where approved |
| Docker gateway/default gateway | absent/DENY | connection DENY except DNS machinery proven necessary | consumer host access DENY | separately instrumented sentinel PASS |
| `host.docker.internal`, `gateway.docker.internal`, host-gateway alias | absent/DENY | resolve/connect DENY | DENY | no production-like positive allow |
| loopback `127.0.0.0/8`, `::1` | only own controlled probe may PASS | no host escape; external target DENY | no broker bypass | local probe proves harness works |
| link-local/metadata `169.254.0.0/16`, `169.254.169.254`, `fe80::/10` | DENY | DENY | DENY | isolated sentinel only |
| LAN, WSL, VPN host interface IPs | DENY | DENY | DENY | LAN exposure harness outside target scope |
| alternate DNS server UDP/TCP 53 | DENY | DENY | consumer DENY; broker only approved resolver | resolver fixture PASS |

Probe timeout is bounded and a timeout is distinguished from policy denial. `connection refused` counts as denial only when route/path observation proves containment; it cannot alone prove no egress.

### 9.4. Positive control

Один hash-pinned, secret-free probe image uses the same executable/arguments/fixture IDs twice:

1. `CONTROL`: attached only to a run-scoped controlled sentinel network with DNS+IPv4 and, when supported, IPv6 endpoints; every canary must reach its sentinel.
2. `TARGET`: exact service namespace/manifest; every forbidden destination must fail with the expected containment class.

If positive control cannot reach a canary, target denial is `V4_BLOCKED_CANARY`, not PASS. Intentional second network/default gateway on target must change graph hash and yield `V4_FAIL_CONTAINMENT` before probe aggregation.

No public Internet positive control is required for mock/gate. Future real-provider positive operation belongs to real arming and destination proof, not offline containment qualification.

## 10. `V4-C07-DESTINATION-EGRESS`

### 10.1. Architecture

```text
n8n --internal--> telegram-bridge [Telegram token]
                          |
                    telegram_proxy (internal)
                          |
              egress-telegram [no secrets]
                          |
                       uplink
                          |
          proposed api.telegram.org:443 only

n8n --internal--> deepseek-adapter [DeepSeek key]
                          |
                       llm_proxy (internal)
                          |
              egress-deepseek [no secrets]
                          |
                       uplink
                          |
          proposed api.deepseek.com:443 only
```

Provider hostnames above are proposed logical origins, not current-source claims. Before acquisition/use, V2/V6 must bind each ASCII hostname, port, API base, TLS policy and official-source evidence into immutable `destination_policy_sha256`. If authoritative current source disagrees or metadata is unknown, real-dev remains `V4_BLOCKED_DESTINATION`.

### 10.2. Broker and client policy

Each provider has a separate broker/image/config/network. Broker:

- has no token, API key, DB credential, n8n key, data volume, project/Vault mount or Docker control;
- listens only on its internal client network and exact non-privileged proxy port;
- accepts only HTTP `CONNECT` authority in canonical lowercase ASCII exact hostname plus `:443`;
- rejects numeric IP literals, userinfo, wildcard/subdomain, trailing dot, alternate case after non-canonical input, Unicode/punycode not in policy, alternate port, plaintext forwarding, generic SOCKS and arbitrary proxy methods;
- does not terminate provider TLS and has no custom CA; secret-bearing client validates hostname/certificate end-to-end;
- disables response redirects in adapter/client. Any `3xx` is a blocked protocol result; redirects are not followed by broker or adapter;
- logs only run ID, destination class, decision, byte counters and error class; CONNECT URL/path/header/token never enters logs/evidence;
- has bounded connections/bytes/time and no administrative/listening port on host or application networks.

Adapter/bridge uses an explicit proxy setting in reviewed code/config, not inherited generic proxy variables. It cannot accept destination/base URL/host/port from workflow, LLM, Telegram payload or environment. n8n reaches only the adapter's authenticated internal schema; provider secret never reaches n8n in this strict topology.

### 10.3. DNS rebinding and address policy

Broker resolution is part of the locked implementation and must:

1. Query only approved resolver path; alternate DNS, search suffix and hosts-file override are rejected.
2. Canonicalize query to exact policy hostname and retain the hostname for TLS SNI/certificate validation by client.
3. Evaluate every returned A/AAAA address. Any loopback, private, CGNAT, link-local, multicast, unspecified, documentation, benchmark, reserved, host/WSL/VPN/LAN subnet or Docker subnet answer blocks the whole RRset.
4. Bind connection to one address from the just-validated RRset; no second resolver lookup by another layer before connect.
5. Revalidate on every new connection and after TTL; cap cache lifetime. Changed public RRset is logged as hash/counter and re-evaluated, not blindly trusted.
6. Reject CNAME chain to unapproved terminal name or excessive/looping chain. A required provider alias must be explicit in a new destination policy.
7. Treat DNS failure, mixed safe/unsafe answers, IPv6-unavailable ambiguity and TLS name failure as `BLOCKED`, never retry through literal IP.

TLS alone mitigates forged public DNS answers only while hostname verification and trusted CA validation remain intact. Broker compromise can create arbitrary secretless outbound traffic and remains a residual risk; it must not gain provider secrets. A secret-bearing adapter compromise can send arbitrary data to its single approved provider, so V6 application schema/data class/message/cost caps remain mandatory.

### 10.4. Real destination tests

For each secret-bearing adapter:

- approved minimal provider operation succeeds only after valid time-bounded arm record;
- unrelated public FQDN, sibling provider domain, control domain, subdomain, trailing-dot host, direct IPv4/IPv6, alternate port, redirect and DNS-rebind fixtures fail;
- raw socket to uplink/public IP fails because adapter has no uplink membership;
- malformed CONNECT/absolute URI cannot make broker connect elsewhere;
- DeepSeek-disabled mode has no adapter, broker, networks, key mount, DNS query or connection count for DeepSeek;
- workflow HTTP/Code/custom-node exfil canary cannot reach provider or arbitrary Internet because n8n has no provider/uplink network.

## 11. `V4-C08-HOST-EXPOSURE`

### 11.1. Allowed exposure

Only n8n publishes `127.0.0.1:5678:5678/tcp`. PostgreSQL, mocks, bridge, adapters, brokers, restore and gates publish zero TCP/UDP ports. `[::1]` is not published in v2; IPv6 loopback connection therefore must fail. `0.0.0.0`, `[::]`, LAN/Wi-Fi/VPN/WSL/Hyper-V interface addresses, host networking and diagnostic ports are forbidden.

Port change or optional diagnostic listener is not an automatic fallback. It requires a new reviewed configuration/owner gate; V4 does not approve it.

### 11.2. Immediate pre-bind guard

Immediately before create/start and without user callback:

- enumerate IPv4/IPv6 TCP/UDP listeners and owning process/service;
- enumerate Docker published ports and approved project/container identity;
- enumerate Windows `portproxy`, HNS/NAT/forwarding objects when readable, relevant firewall inbound rules/profile state, active routes/adapters and VPN/proxy/tunnel software state;
- bind classification must be `FREE` or exact idempotent approved lab listener;
- any unrelated listener, wildcard, non-loopback address, unknown owner, proxy/forward, unreadable required inventory or changed VPN/firewall state returns `V4_BLOCKED_EXPOSURE` before project mutation.

No firewall/portproxy/VPN remediation is executed. User need not disable security tooling; if the boundary cannot be proven, the mode remains blocked.

### 11.3. Post-bind matrix

After start, before reporting ready:

| Vantage | Destination | Expected |
|---|---|---|
| Windows host | `127.0.0.1:5678` | PASS, expected n8n health identity |
| Windows host | `localhost` resolved to IPv4 | PASS only same listener |
| Windows host | `::1:5678` | DENY under IPv4-only policy |
| Windows host | every active non-loopback IPv4 address | DENY |
| Windows host | every active non-loopback IPv6 address | DENY |
| Docker container | `host.docker.internal:5678`, gateway and host interface IPs | DENY |
| WSL/Hyper-V virtual adapter vantage | host port | DENY |
| Active VPN/tunnel address/vantage | host port | DENY |
| Separate LAN device on same network | host LAN IPv4/IPv6 port | DENY |

Authoritative listener/portproxy/firewall inventories are repeated after tests. Недоступность separate LAN vantage, required IPv6 probe, HNS/portproxy/firewall inventory or VPN classification gives `V4_BLOCKED_EXPOSURE`; self-connect refusal alone is insufficient. LAN test is owner-assisted manual evidence and never opens a port.

Host sleep/wake, Docker restart, Windows reboot, network profile change, adapter/VPN change and Docker/Desktop drift invalidate prior exposure evidence. Next start repeats the full guard.

## 12. `V4-C09-MODE-CONVERGENCE`

### 12.1. State machine

```text
STOPPED
  -> MOCK_PRECHECK -> MOCK_RUNNING
  -> REAL_PRECHECK -> ARMED_TG -> REAL_TG_RUNNING
  -> REAL_PRECHECK -> ARMED_TG_DS -> REAL_TG_DEEPSEEK_RUNNING
  -> RESTORE_PRECHECK -> RESTORE_RUNNING
  -> GATE_PRECHECK -> GATE_RUNNING

any RUNNING -> DRAINING -> EPHEMERAL_REMOVED -> STOPPED
any PRECHECK -> BLOCKED_* | STOP_*
any RUNNING -> EMERGENCY_DISARMED -> DRAINING | STOP_UNVERIFIED
```

Direct `MOCK_RUNNING -> REAL_*`, `REAL_TG_RUNNING -> REAL_TG_DEEPSEEK_RUNNING`, restore/gate overlap and mixed Compose profiles are forbidden. Transition first drains current mode, removes exact project containers and networks without `-v`, verifies no process/listener/network/secret mount/background connection, then creates target state.

`docker compose down` is permitted only through object custody, without `--volumes`, `--rmi`, orphan/foreign deletion or broad cleanup. Persistent named volumes remain unchanged.

### 12.2. Dry-run

`lab ... --dry-run` is read-only and must perform zero Docker/file mutation, secret read, container create/start, Telegram/DeepSeek API, webhook/offset/budget/arm change. Online `getMe` or provider probe is a separate armed command, never hidden in dry-run/status/doctor.

### 12.3. Real arming dependency

V4 consumes a valid V6 arm record bound to bot/recipient/data class/message cap, optional DeepSeek model/cost cap, destination policy, Compose/network/mount hashes, TTL and current host/endpoint fingerprint. Missing/stale/drifted arm blocks before starting any bridge/adapter/broker or provider DNS/API call.

Stop, emergency stop, timeout, cap exhaustion, reboot/session boundary or identity/config drift atomically disarms first. Real containers use `restart:no`; after stop they are removed so token/key mounts and uplink networks do not remain attached.

### 12.4. Emergency stop network contract

`lab emergency-stop telegram`:

1. Atomically expires arm record through V6 control path before Docker stop attempt.
2. Through V1 endpoint guard, stops adapters then brokers, removes exact real containers/networks without volumes, and checks zero polling/provider sockets/listeners/secret mounts.
3. Preserves persistent volumes, secrets and evidence; no revoke/delete/prune.
4. If Engine unavailable, returns nonzero `V4_STOP_UNVERIFIED` and prints exact owner action: stop/quit Docker Desktop through visible UI/service procedure, then rerun read-only verification. It does not claim outbound stopped until process/listener checks prove it.
5. Bot token revoke/rotate through BotFather belongs to V6 manual incident procedure and is never automated by V4.

## 13. `V4-C10-O5-CAPABILITY` — независимые scopes

Scopes are independent:

- `LAB`: local PostgreSQL+n8n+mock/real topology, exposure and persistence prerequisites.
- `LOCAL`: Docker-local static/runtime/capability tests that do not require privileged-equivalent access.
- `OFFLINE`: full B2r/O5 exact candidate gate, including required Linux filesystem/mount semantics.
- `REMOTE`: outside this plan; no status is produced by V4 execution.

Allowed O5 non-root rows include ordinary file/symlink/hardlink/mode/UID-visible behavior, signals to owned processes, rollback/cleanup and optionally §5.4 `LINUX_IMMUTABLE`. Mount namespace creation, bind/nested mounts or inode operations that require root/`CAP_SYS_ADMIN`/privileged-equivalent rights are not emulated and not silently skipped.

If any mandatory O5 row needs forbidden rights or Docker Desktop fingerprint lacks semantics:

```text
LAB = PASS or independent result
LOCAL = PASS or independent result
OFFLINE = BLOCKED_CAPABILITY
overall = PARTIAL_READY; never SUCCESS/OFFLINE_READY
rc = 88
```

Plan B, VPS and privilege escalation remain absent. Повторный design может искать другой Docker-only путь после решения владельца.

Gate input is a content-addressed candidate volume, not mutable host bind. Output starts empty. Gate runner has `network_mode:none`, no secrets, no persistent-lab volumes and no Docker control. Two clean runs and full candidate/environment evidence belong to V8; V4 supplies containment records.

## 14. `V4-C11-OBJECT-CUSTODY`

Every disposable object label tuple:

```yaml
io.n8nagents.scope: LAB | LOCAL | OFFLINE | RESTORE
io.n8nagents.plan_sha256: <exact>
io.n8nagents.authority_sha256: <exact>
io.n8nagents.project: <exact>
io.n8nagents.run_id: <nonce>
io.n8nagents.candidate_sha256: <hash-or-NONE>
io.n8nagents.resource_class: container | network | volume
io.n8nagents.disposable: "true" | "false"
```

Before create: zero name/label collision. Custody record also stores exact Docker object IDs, creation facts, endpoint/daemon hash and expected dependencies. Cleanup preview is immutable and TTL-bound. Apply rechecks endpoint, IDs, all labels, dependency graph and persistent=false. Missing/extra/foreign/changed object deletes `0` and returns nonzero.

Crash, signal, Docker restart and host reboot cases run a read-only residual scan. Idempotent recovery removes only exact current-run disposable containers/networks/temp volumes. Persistent laboratory volumes, current/LKG images, backup, secrets and foreign objects remain unchanged. Broad prune and orphan auto-delete are forbidden.

## 15. `V4-C12-STATUS-RC`

### 15.1. Result schema

```yaml
schema: n8nagents.v4-result/v2
run_id: <uuid>
operation_id: <allowlisted>
plan_sha256: <exact>
authority_ref: <nonsecret>
endpoint_record_sha256: <hash|null>
scope: LAB | LOCAL | OFFLINE | RESTORE
decision: PASS | READY_FOR_MANUAL_GATE | BLOCKED | FAIL | STOP | NOT_RUN
status: <stable-enum>
rc: <int>
mutation_started: <bool>
first_mutation_utc: <utc|null>
mode_before: <enum>
mode_after: <enum>
privilege_manifest_sha256: <hash|null>
mount_manifest_sha256: <hash|null>
network_manifest_sha256: <hash|null>
destination_policy_sha256: <hash|null>
execution_fingerprint_sha256: <hash|null>
assertions: {required: <int>, passed: <int>, failed: <int>, blocked: <int>, skipped: <int>}
evidence_refs: [EV-V4-*]
failed_predicates: [<stable-ids>]
next_safe_action: <one-stable-id>
```

RC `0` only when every mandatory assertion for the exact scope passes and `skipped=blocked=failed=0`. Human text/stdout cannot override schema/RC/evidence.

### 15.2. Local RC namespace

| RC | Status | Семантика |
|---:|---|---|
| `0` | `V4_<SCOPE>_PASS` | Exact scope PASS only. |
| `10` | `V4_READY_FOR_MANUAL_GATE` | No mutation; exact gate listed. |
| `80` | `V4_BLOCKED_UNKNOWN` | Missing/unreadable/stale observation or dependency. |
| `81` | `V4_BLOCKED_ENDPOINT` | V1 endpoint/daemon/project identity mismatch. |
| `82` | `V4_BLOCKED_PRIVILEGE` | Privilege manifest unsupported or exceeded. |
| `83` | `V4_BLOCKED_MOUNT` | Mount/path/volume manifest not qualified. |
| `84` | `V4_BLOCKED_NETWORK` | Network graph/no-egress predicate unavailable or invalid. |
| `85` | `V4_BLOCKED_DESTINATION` | Destination/DNS/TLS/redirect policy not qualified. |
| `86` | `V4_BLOCKED_EXPOSURE` | Windows loopback/LAN/IPv6/firewall/VPN proof incomplete. |
| `87` | `V4_BLOCKED_MODE_DRIFT` | Active services/networks/mounts differ from desired state. |
| `88` | `V4_OFFLINE_BLOCKED_CAPABILITY` | Mandatory OFFLINE row needs forbidden/unsupported capability; LAB/LOCAL retain own result. |
| `89` | `V4_FAIL_CONTAINMENT` | Unexpected mount/write/network/route/object observed. |
| `90` | `V4_BLOCKED_CANARY` | Positive control or required probe unavailable; no PASS. |
| `91` | `V4_STOP_SCOPE_EXPANSION` | Forbidden privilege/device/socket/host/VPS/plan-B request. |
| `92` | `V4_INTERNAL_ERROR` | Collector/schema/tool ambiguity; fail closed. |
| `93` | `V4_STOP_UNVERIFIED` | Emergency disarm recorded, but process/egress stop not proven. |

Глобальный интегратор может remap numeric codes, но обязан сохранять status semantics and nonzero behavior.

### 15.3. Aggregation

```text
LAB_PASS + LOCAL_PASS + OFFLINE_BLOCKED_CAPABILITY
  => PARTIAL_READY, rc 88
  != SUCCESS
  != OFFLINE_READY

Any FAIL_CONTAINMENT/STOP_SCOPE_EXPANSION
  => STOP for next mutation in all dependent scopes.
```

`status/doctor` read-only показывает independently: endpoint, privilege, mounts, network graph, exposure, mode, real arm, destinations, LAB/LOCAL/OFFLINE, timestamp, stale reason and one next safe action. `UNKNOWN` не отображается зелёным.

## 16. Manual gates

| Gate | Когда | Exact предмет |
|---|---|---|
| `MG-V4-FULL-PLAN` | До любого V4 runtime | frozen full plan v2 hash и A-only scope |
| `MG-V4-DESTINATION-POLICY` | До real provider DNS/API | exact Telegram/optional DeepSeek hostname:port, source refs, redirects=false, address policy, broker/adapters hashes |
| `MG-V4-REAL-ARM` | До real containers/DNS | V6 arm record, TTL, identities, message/cost/data limits, exact mode/network/mount/destination hashes |
| `MG-V4-LAN-CANARY` | Перед loopback exposure PASS | owner-assisted second-device negative probe, exact time/window, no host change |
| `MG-V4-HOST-NETWORK-CHANGE` | Только если потребуются firewall/portproxy/VPN changes | вне текущего разрешения; новый exact change plan, не remediation V4 |
| `MG-V4-PORT-CHANGE` | Если `5678` unavailable | new reviewed configuration; automatic port selection forbidden |
| `MG-V4-CLEANUP-<plan-id>` | Каждый material cleanup | exact object IDs/full labels; no volumes/foreign objects |
| `MG-V4-O5-SCOPE-CHANGE` | Если нужен root/SYS_ADMIN/privileged/device/backend | не gate внутри текущего A; STOP и новое решение владельца |

V1/V2/V3/V5/V6/V7/V8/V9/V10 gates не подразумеваются этими approvals. Любой hash/host/endpoint/mode/TTL drift инвалидирует gate.

## 17. Acceptance tests

| ID | Проверка |
|---|---|
| `AT-V4-01` | Every Docker operation uses explicit V1 local endpoint; current-context drift cannot redirect it. |
| `AT-V4-02` | Render+inspect all services: nonroot, Privileged=false, CapDrop ALL, exact CapAdd, no devices/socket/host PID/IPC, RO rootfs, no-new-privileges. |
| `AT-V4-03` | Compose/inspect mounts equal exact per-service manifest; only declared named volumes/tmpfs/file-scoped secrets visible. |
| `AT-V4-04` | Host file bind passes handle/volume/file-ID/ACL/reparse/link/case/Unicode/ADS custody through create/start; only consumer reads canary. |
| `AT-V4-05` | Fresh and repeated desired-state render for STOPPED/MOCK/REAL_TG/REAL_TG_DEEPSEEK/RESTORE/GATE has exact services/networks/ports/mount classes. |
| `AT-V4-06` | Gate namespace has only loopback/no default route; same probe positive-control reaches controlled sentinel. |
| `AT-V4-07` | Mock/restore can reach only exact internal peers; DNS/IPv4/IPv6/gateway/host-alias/link-local/external probes deny with positive controls green. |
| `AT-V4-08` | Real bridge/adapter has no uplink; reaches only its broker; broker allows exact provider origin and rejects all destination canaries. |
| `AT-V4-09` | DNS safe/public RRset and TLS hostname fixture passes; mixed/private/link-local/CNAME/re-resolution rebinding fixtures block whole connection. |
| `AT-V4-10` | Windows pre/post bind proves only `127.0.0.1:5678`; host loopback succeeds; ::1/non-loopback/WSL/VPN/separate-LAN attempts deny. |
| `AT-V4-11` | All mode transitions drain/remove forbidden services/networks/mounts before target create; stop leaves volumes only and no poller/uplink/secret mount. |
| `AT-V4-12` | Dry-run/status/doctor make zero mutation/secret read/provider call; online probes are separate armed operations. |
| `AT-V4-13` | O5 nonprivileged rows execute exact envelope; any SYS_ADMIN/root/privileged-equivalent row returns scoped OFFLINE_BLOCKED_CAPABILITY while LAB/LOCAL remain independent. |
| `AT-V4-14` | Cleanup normal/failure/signal/Desktop restart/host reboot removes only invocation disposable objects; persistent/foreign states unchanged. |
| `AT-V4-15` | Emergency stop disarms first; healthy/unhealthy/Engine-unavailable cases never claim stopped without process/network proof. |
| `AT-V4-16` | Execution fingerprint drift in kernel/Engine/network/mount/security invalidates previous containment PASS. |
| `AT-V4-17` | Scoped result table rejects forged PASS, missing assertions, skipped probes and OFFLINE blocked promoted to overall success. |

## 18. Negative canaries

| ID | Canary and expected result |
|---|---|
| `NC-V4-01` | `DOCKER_HOST/CONTEXT/TLS`, TCP/SSH/second daemon or project-name substitution -> RC 81, zero mutation. |
| `NC-V4-02` | Privileged/root/empty user, CAP_SYS_ADMIN/NET_ADMIN, extra cap, host PID/IPC, device/socket/proc/sys mount -> RC 82/91 before create. |
| `NC-V4-03` | Extra/missing/writable/broad/implicit bind or foreign named volume -> RC 83; target not started. |
| `NC-V4-04` | Junction, symlink, hardlink, case/NFC collision, ADS, 8.3 alias, ancestor/leaf swap -> RC 83/89; outside sentinel unchanged. |
| `NC-V4-05` | Implicit default/external/attachable/host/service/container network, extra_hosts/host-gateway, extra attachment -> RC 84/89. |
| `NC-V4-06` | Positive-control endpoint unavailable -> RC 90; target denial cannot become PASS. |
| `NC-V4-07` | DNS name, direct IPv4/IPv6, alternate DNS, gateway, host aliases, metadata/link-local/LAN/VPN from mock/gate/restore -> expected deny or RC 89. |
| `NC-V4-08` | Real arbitrary FQDN, sibling domain, subdomain, trailing dot, direct IP, port !=443, redirect, mixed/private DNS answer -> RC 85, no provider request. |
| `NC-V4-09` | Workflow/LLM/payload attempts to set host/base URL/proxy/destination -> ignored/rejected; n8n has no route and exfil marker absent. |
| `NC-V4-10` | Occupy 5678 after preflight, wildcard/IPv6/LAN bind, portproxy/firewall/VPN drift -> RC 86 and no project start/alternate port. |
| `NC-V4-11` | Mixed profiles/direct service target, hot-enable DeepSeek, stale real container/restart policy -> RC 87 until drain/remove. |
| `NC-V4-12` | Dry-run with provider/secret/offset/arm/container side effect -> FAIL, not degraded PASS. |
| `NC-V4-13` | O5 asks root/SYS_ADMIN/privileged/Docker socket -> OFFLINE RC 88/91; no retry with broader rights. |
| `NC-V4-14` | Same run label but different authority/candidate/class, missing label or changed object ID -> cleanup deletes zero. |
| `NC-V4-15` | Engine unavailable during emergency stop -> arm DISARMED but status STOP_UNVERIFIED RC 93; volumes unchanged. |
| `NC-V4-16` | Reuse evidence after kernel/storage/network/mount fingerprint change -> RC 80/84; rerun required. |
| `NC-V4-17` | stdout `PASS` with nonzero RC, zero RC with missing probe/row, OFFLINE blocked plus overall SUCCESS -> schema rejection RC 92. |

## 19. Evidence catalog

Evidence is schema-bound, content-addressed, source-allowlisted and secret-free. Raw secret values, Telegram/DeepSeek URLs with credentials, request paths/headers/bodies, user IDs, raw Windows paths/SIDs, unrestricted inspect/config/env or packet payloads are forbidden.

| ID | Artifact |
|---|---|
| `EV-V4-01-ENDPOINT` | V1 endpoint hash, pre/post daemon identity, explicit context/project and zero-mutation result. |
| `EV-V4-02-PRIVILEGE` | Render/inspect/in-container UID/GID, privilege/cap/security/device/PID/IPC assertions for every container. |
| `EV-V4-03-MOUNTS` | Exact mount manifest, rendered/inspect equality, named-volume identity and target validation. |
| `EV-V4-04-HOST-PATH` | Logical root, keyed volume/file/ancestor fingerprints, ACL/reparse/link/case/Unicode/ADS/handle timeline and outside-sentinel result. |
| `EV-V4-05-NETWORK-GRAPH` | Desired/observed service-network bipartite graph, network IDs/classes/IPAM/internal flags and drift diff. |
| `EV-V4-06-NO-EGRESS` | Per-service DNS/IPv4/IPv6/gateway/host/link-local probe rows plus namespace interface/route/resolver/socket hashes. |
| `EV-V4-07-POSITIVE-CONTROL` | Same probe/tool/args fixture IDs, reachable controlled sentinel rows and target comparison. |
| `EV-V4-08-DESTINATIONS` | Destination policy hash, broker/adapters/image/config hashes, canonical allow/deny classes, DNS/TLS/redirect results and byte counters. |
| `EV-V4-09-EXPOSURE` | Pre/post Windows listener owners, published ports, portproxy/HNS/firewall/VPN state hashes and all vantage results. |
| `EV-V4-10-MODE` | Mode transition ledger, exact service/network/mount deltas, arm/disarm refs and no-background result. |
| `EV-V4-11-O5` | Row privilege/mount/network manifest, capability result and scoped LAB/LOCAL/OFFLINE aggregation. |
| `EV-V4-12-CUSTODY` | Full labels, object IDs/creation facts, cleanup preview/apply/recovery and persistent/foreign invariance. |
| `EV-V4-13-FINGERPRINT` | Architecture/kernel/Desktop/Engine/Compose/storage/backing-fs/cgroup/security/network/mount fingerprint. |
| `EV-V4-14-STATUS` | Schema-valid scoped state/RC/assertion counts/timestamps/next-safe-action. |
| `EV-V4-15-NO-CHANGE` | Blocked/dry-run canaries: mutation/API/secret-read counts zero and source/persistent/outside sentinels unchanged. |

Packet capture, if a future approved tool needs it, stores only direction, protocol, destination class, bytes, decision and timestamps; payload/SNI token path/headers are not retained. If metadata cannot be safely redacted and validated, capture is discarded and evidence stage blocks.

## 20. Traceability к V0 baseline

`DESIGN_CLOSED` ниже означает только наличие design contract/test/canary/evidence. Runtime proof pending. `XDEP` означает, что V4 закрывает только свою часть, а общий finding остаётся заблокирован до owner section PASS.

| Source finding | V4 contract | Acceptance | Negative canary | Evidence | Disposition |
|---|---|---|---|---|---|
| `R1-WIN-001` | `V4-C01-ENDPOINT-CHAIN` | `AT-V4-01` | `NC-V4-01` | `EV-V4-01-ENDPOINT` | `XDEP-V1`; design mapped |
| `R1-WIN-008` | `V4-C03-MOUNT-MANIFEST`, `V4-C04-HOST-PATH-CUSTODY` | `AT-V4-03`, `AT-V4-04` | `NC-V4-03`, `NC-V4-04` | `EV-V4-03-MOUNTS`, `EV-V4-04-HOST-PATH` | `XDEP-V3`; design mapped |
| `R1-WIN-012` | `V4-C08-HOST-EXPOSURE` | `AT-V4-10` | `NC-V4-10` | `EV-V4-09-EXPOSURE` | `DESIGN_CLOSED`; runtime pending |
| `R3-PRIV-001` | `V4-C02-PRIVILEGE-ENVELOPE`, `V4-C10-O5-CAPABILITY` | `AT-V4-02`, `AT-V4-13` | `NC-V4-02`, `NC-V4-13` | `EV-V4-02-PRIVILEGE`, `EV-V4-11-O5` | `DESIGN_CLOSED_WITH_BLOCKED_PATH`; no privileged backend |
| `R3-NET-002` | `V4-C05-NETWORK-GRAPH`, `V4-C06-NO-EGRESS` | `AT-V4-06`, `AT-V4-07` | `NC-V4-05`, `NC-V4-06`, `NC-V4-07` | `EV-V4-05-NETWORK-GRAPH`, `EV-V4-06-NO-EGRESS`, `EV-V4-07-POSITIVE-CONTROL` | `DESIGN_CLOSED`; runtime pending |
| `R3-NET-003` | `V4-C07-DESTINATION-EGRESS` | `AT-V4-08`, `AT-V4-09` | `NC-V4-08`, `NC-V4-09` | `EV-V4-08-DESTINATIONS` | `DESIGN_CLOSED`; provider/source runtime pending |
| `R3-PORT-004` | `V4-C08-HOST-EXPOSURE` | `AT-V4-10` | `NC-V4-10` | `EV-V4-09-EXPOSURE` | `DESIGN_CLOSED`; LAN/manual runtime pending |
| `R3-CTRL-005` | `V4-C01-ENDPOINT-CHAIN` | `AT-V4-01` | `NC-V4-01` | `EV-V4-01-ENDPOINT` | `XDEP-V1`; design mapped |
| `R3-MOUNT-006` | `V4-C03-MOUNT-MANIFEST`, `V4-C04-HOST-PATH-CUSTODY` | `AT-V4-03`, `AT-V4-04` | `NC-V4-03`, `NC-V4-04` | `EV-V4-03-MOUNTS`, `EV-V4-04-HOST-PATH` | `DESIGN_CLOSED`; V3 roots pending |
| `R3-CLEAN-007` | `V4-C11-OBJECT-CUSTODY` | `AT-V4-14` | `NC-V4-14` | `EV-V4-12-CUSTODY` | `DESIGN_CLOSED`; runtime pending |
| `R3-PROFILE-008` | `V4-C05-NETWORK-GRAPH`, `V4-C09-MODE-CONVERGENCE` | `AT-V4-05`, `AT-V4-11`, `AT-V4-12` | `NC-V4-11`, `NC-V4-12` | `EV-V4-05-NETWORK-GRAPH`, `EV-V4-10-MODE`, `EV-V4-15-NO-CHANGE` | `DESIGN_CLOSED`; V5/V6 pending |
| `R4-F01` | `V4-C05-NETWORK-GRAPH`, `V4-C09-MODE-CONVERGENCE` | `AT-V4-05`, `AT-V4-11` | `NC-V4-11` | `EV-V4-05-NETWORK-GRAPH`, `EV-V4-10-MODE` | `XDEP-V5`; network portion mapped |
| `R5-F10` | `V4-C07-DESTINATION-EGRESS` | `AT-V4-08` | `NC-V4-09` | `EV-V4-08-DESTINATIONS` | `XDEP-V6`; network destination only |
| `R5-F14` | `V4-C09-MODE-CONVERGENCE` | `AT-V4-11`, `AT-V4-12` | `NC-V4-11`, `NC-V4-12` | `EV-V4-10-MODE`, `EV-V4-15-NO-CHANGE` | `XDEP-V6`; network/dry portion mapped |
| `R6-P1-001` | `V4-C01-ENDPOINT-CHAIN`, `V4-C02-PRIVILEGE-ENVELOPE` | `AT-V4-01`, `AT-V4-02` | `NC-V4-01`, `NC-V4-02` | `EV-V4-01-ENDPOINT`, `EV-V4-02-PRIVILEGE` | `XDEP-V1/V3/V6`; container portion mapped |
| `R6-P1-002` | `V4-C03-MOUNT-MANIFEST`, `V4-C04-HOST-PATH-CUSTODY` | `AT-V4-03`, `AT-V4-04` | `NC-V4-03`, `NC-V4-04` | `EV-V4-03-MOUNTS`, `EV-V4-04-HOST-PATH` | `XDEP-V6`; mount portion mapped |
| `R6-P1-010` | `V4-C05-NETWORK-GRAPH`, `V4-C07-DESTINATION-EGRESS` | `AT-V4-08`, `AT-V4-09` | `NC-V4-08`, `NC-V4-09` | `EV-V4-05-NETWORK-GRAPH`, `EV-V4-08-DESTINATIONS` | `DESIGN_CLOSED`; V6 app policy pending |
| `R7-F07` | `V4-C06-NO-EGRESS`, `V4-C08-HOST-EXPOSURE` | `AT-V4-07`, `AT-V4-10` | `NC-V4-05`, `NC-V4-07`, `NC-V4-10` | `EV-V4-05-NETWORK-GRAPH`, `EV-V4-06-NO-EGRESS`, `EV-V4-09-EXPOSURE` | `XDEP-V7`; isolation portion mapped |
| `R8-P1-003` | `V4-C03-MOUNT-MANIFEST`, `V4-C10-O5-CAPABILITY` | `AT-V4-03`, `AT-V4-13` | `NC-V4-03`, `NC-V4-16` | `EV-V4-03-MOUNTS`, `EV-V4-11-O5`, `EV-V4-13-FINGERPRINT` | `XDEP-V8`; no mutable host bind |
| `R8-P1-004` | `V4-C11-OBJECT-CUSTODY` | `AT-V4-14` | `NC-V4-14`, `NC-V4-16` | `EV-V4-12-CUSTODY`, `EV-V4-13-FINGERPRINT` | `XDEP-V8`; containment clean-run portion |
| `R8-P1-006` | `V4-C12-STATUS-RC` | `AT-V4-17` | `NC-V4-17` | `EV-V4-14-STATUS` | `DESIGN_CLOSED`; global mapping pending |
| `R8-P1-008` | `V4-C06-NO-EGRESS` | `AT-V4-06`, `AT-V4-07` | `NC-V4-05`, `NC-V4-06`, `NC-V4-07` | `EV-V4-06-NO-EGRESS`, `EV-V4-07-POSITIVE-CONTROL` | `DESIGN_CLOSED`; runtime pending |
| `R8-P1-009` | `V4-C10-O5-CAPABILITY`, `V4-C12-STATUS-RC` | `AT-V4-16`, `AT-V4-17` | `NC-V4-16`, `NC-V4-17` | `EV-V4-11-O5`, `EV-V4-13-FINGERPRINT`, `EV-V4-14-STATUS` | `DESIGN_CLOSED`; fingerprint observation pending |
| `R8-P2-012` | `V4-C11-OBJECT-CUSTODY` | `AT-V4-14` | `NC-V4-14` | `EV-V4-12-CUSTODY` | `DESIGN_CLOSED`; runtime pending |
| `R9-F03` | `V4-C04-HOST-PATH-CUSTODY` | `AT-V4-04` | `NC-V4-04` | `EV-V4-04-HOST-PATH`, `EV-V4-15-NO-CHANGE` | `DESIGN_CLOSED`; runtime pending |
| `R9-F08` | `V4-C03-MOUNT-MANIFEST`, `V4-C04-HOST-PATH-CUSTODY` | `AT-V4-03`, `AT-V4-04` | `NC-V4-03`, `NC-V4-04` | `EV-V4-03-MOUNTS`, `EV-V4-04-HOST-PATH`, `EV-V4-15-NO-CHANGE` | `XDEP-V9`; runtime no-write portion |
| `R10-F01` | `V4-C09-MODE-CONVERGENCE` | `AT-V4-11`, `AT-V4-15` | `NC-V4-11`, `NC-V4-15` | `EV-V4-10-MODE`, `EV-V4-14-STATUS` | `XDEP-V6`; arming consumed, not owned |
| `R10-F02` | `V4-C09-MODE-CONVERGENCE`, `V4-C12-STATUS-RC` | `AT-V4-15` | `NC-V4-15` | `EV-V4-10-MODE`, `EV-V4-14-STATUS`, `EV-V4-15-NO-CHANGE` | `XDEP-V6/V10`; network stop portion mapped |
| `R10-F08` | `V4-C12-STATUS-RC` | `AT-V4-17` | `NC-V4-17` | `EV-V4-14-STATUS` | `XDEP-V10`; V4 diagnostics substate mapped |

Coverage: `29` unique relevant baseline finding IDs; each has at least one named V4 contract, acceptance test, negative canary and evidence artifact. Other V0 findings are outside V4 ownership and are not claimed closed.

## 21. Cross-domain interfaces

| Owner section | V4 consumes | V4 provides |
|---|---|---|
| V1 Windows/control plane | approved endpoint, exact daemon/project guard, identities, immediate port inventory | endpoint-dependent operation IDs, exposure/containment result |
| V2 supply chain | exact image/tool/proxy/adapter digests, source locks, runtime fingerprint inputs | no-network build/runtime constraints, broker/adapters runtime identity |
| V3 storage/resources | approved roots, VHDX/data map, ACL/effective principals, volume/cap records | exact mounts, no directory binds, runtime writable-set and object custody |
| V5 Compose/n8n/PostgreSQL | exact service IDs, UID/GID, paths, health/migration graph, trigger-disable mechanism | exact desired-state service/network/mount/port/privilege matrix |
| V6 Telegram/DeepSeek/secrets | secret-file transport, authenticated adapter schemas, arm record, routing/budget/data policies | sole external consumers, destination policy, no n8n direct route, stop/disarm evidence |
| V7 backup/restore | restore generation/keys/target, disabled writers/triggers | restore internal-only/no-port/no-source-mount proof |
| V8 B2r/O5/evidence | candidate/runner/fingerprint/result schemas | network-none, nonprivileged capability and scoped block evidence |
| V9 repo custody | immutable candidate and touchset/Vault/Git boundaries | no repo/Vault bind/write and archive-to-volume path |
| V10 operability | global CLI/status/emergency UX and RC mapping | V4 stable substates, diagnostics and next-safe-action IDs |

Conflict rule: stricter contract wins. If two sections disagree on service name, mount, network, secret consumer, result state or privilege, integrated plan blocks until one new frozen interface is reviewed; no union of permissions.

## 22. Stop conditions

Immediate STOP/BLOCKED before next mutation:

- endpoint/project/daemon tuple not exact;
- any root/privileged/CAP_SYS_ADMIN/device/socket/host namespace request;
- unmanifested or unqualified mount/path/volume;
- any Windows directory bind, repo/Vault/backup/data-root bind or secret-root directory bind;
- implicit/external/default/extra network or application membership in uplink;
- mock/restore/gate external/host path or skipped positive control;
- provider origin/DNS/TLS/redirect policy unknown or changed;
- n8n/PostgreSQL direct external route;
- host bind not strictly `127.0.0.1:5678`, unknown LAN/IPv6/VPN/firewall/portproxy result;
- stale/mixed mode, real credential mount outside active arm or broker/adapter after disarm;
- O5 requires forbidden capability;
- cleanup identity/labels drift;
- result/evidence schema invalid or fingerprint drift.

## 23. Residual risks

1. Docker Desktop daemon/control principals remain root-equivalent to all backend data; container controls do not isolate secrets from approved daemon administrators.
2. Host-path handle custody does not defend against compromised Windows kernel/SYSTEM/approved Administrator. This is explicit trusted boundary.
3. Secretless egress broker compromise can send arbitrary outbound traffic and probe its client network. Separate broker networks, no secrets/data mounts and nonroot envelope limit impact but do not eliminate it.
4. A compromised secret-bearing adapter can exfiltrate permitted data to its single provider. V6 schema, data classification, arming and caps are mandatory compensating controls.
5. Docker `internal` semantics, host-gateway reachability and Desktop port forwarding must be proved on exact fingerprint. Documentation/version is not evidence.
6. Dynamic provider IPs prevent fixed-IP allowlisting; DNS RRset filtering plus end-to-end TLS binds hostname, but DNS/CA compromise remains in trusted Internet boundary.
7. Separate LAN/VPN exposure proof may require owner-assisted vantage. Its absence blocks exposure PASS rather than being waived.
8. O5 rows requiring mount namespace/root/SYS_ADMIN remain honestly blocked under plan A. This does not imply LAB failure, but prevents OFFLINE_READY.
9. IPv6 may be unavailable in Docker Desktop configuration. Unavailable required canary is BLOCKED; IPv6 is not silently ignored.
10. No root container may make official image initialization impossible. A reviewed Docker-only nonroot image/design may solve it; privilege relaxation does not.

## 24. Порядок будущей реализации

1. Integrate V1–V10 logical IDs and freeze full plan v2; no runtime action.
2. Read-only Windows/Docker preflight and endpoint/storage/resource/manual gates.
3. Supply-lock exact images/tools/adapters/brokers; no containers before runtime lock.
4. Static render policy tests for privilege/mount/network/ports/modes with mutation canaries.
5. Synthetic runtime qualification without secrets: positive controls, no-egress, host exposure, path/mount, nonroot capabilities and cleanup/reboot recovery.
6. If LAB/LOCAL capability qualified, build/start mock stack and repeat containment/persistence checks.
7. Only after V6 arm/secret/data/budget gates start real Telegram; optional DeepSeek is a separate exact mode.
8. Run restore isolation and B2r/O5 scopes independently; preserve scoped BLOCKED where applicable.
9. Owner repeats loopback start/status/mock/real stop/emergency and LAN negative canary from runbook.
10. Independent review validates exact manifests/evidence before any release/deployment gate.

## 25. Definition of Done V4 design

V4 is design-ready for integration review only if:

- all `29` mapped baseline IDs exist in V0 and have contract/AT/NC/EV coverage;
- privilege policy is nonroot, nonprivileged, CapDrop ALL and forbids privileged-equivalent fallback;
- mount manifest and Windows path algorithm cover reparse/symlink/hardlink/case/Unicode/ADS/TOCTOU;
- service/network matrix has no implicit default/proxy and no n8n/PostgreSQL external route;
- mock/gate/restore canary matrix contains DNS, IPv4, IPv6, gateway, host aliases, link-local and positive control;
- real egress has separate provider brokers, exact destination/redirect/DNS-rebind denial and no secrets in broker;
- loopback matrix covers Windows listener, IPv4/IPv6, portproxy/firewall/VPN/WSL and separate LAN vantage;
- LAB/LOCAL/OFFLINE statuses cannot produce false overall SUCCESS;
- cross-domain conflicts, manual gates and residual risks remain explicit;
- no runtime PASS, installation, network access, secret use, repo/VPS/Windows/Docker change is claimed.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
