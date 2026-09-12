---
id: "n8nagents-plan-v2-v3-resource-storage-boundary-a64a14c3"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "V3 Windows storage/data-protection architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники: ["[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]", "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]", "00_FINDINGS_BASELINE.json", "01_BASELINE_AUDIT.json"]
доказательства: []
теги: ["n8nagents", "plan-v2", "docker-desktop", "windows", "storage", "resources", "backup", "recovery"]
---

# V3 — граница ресурсов, хранения и защиты данных Windows

## 1. Назначение и статус

Этот рабочий раздел задаёт исполнимый контракт хранения и ресурсов для локальной постоянной лаборатории N8NAgents по плану A: Docker Desktop с WSL 2 backend, без отдельного пользовательского дистрибутива Ubuntu и без VPS fallback.

Документ не является утверждением о фактическом состоянии компьютера. Windows, Docker Desktop, VHDX, свободный диск, RAM, ACL, BitLocker/Device Encryption, pagefile, crash dumps и пути хранения пока не исследованы в рамках исполнения. Все значения, обозначенные `MEASURED` или `OWNER_APPROVED`, должны быть получены позднее отдельным read-only preflight и ручными gates. До этого состояние соответствующего этапа — `V3_BLOCKED_UNKNOWN`.

Никакое утверждение `PASS`, успешном backup, cold restore, очистке или защите at rest этим документом не делается.

## 2. Область ответственности и непереговорные инварианты

V3 владеет:

- картой всех persistent/transient/diagnostic данных на Windows и внутри Docker-managed VHDX;
- квалификацией Windows roots, volumes, ACL, effective principals, reparse/sync/drive/encryption свойств;
- расчётом host reserve и пикового роста до `download/install/pull/build/start/backup/restore/update`;
- hard limits CPU/RAM и политиками роста DB, logs, evidence, cache и backup;
- Windows-частью backup/restore, ciphertext custody и storage fault domains;
- точным preview и custody для cleanup без broad prune;
- явными residual risks и ручными owner gates.

### 2.1. Реестр contracts

| Contract | Обязательство |
|---|---|
| `V3-C01-ROOT-PATH` | Все Windows roots разрешаются handle-based до volume/file identity; reparse/sync/network/removable/ADS/TOCTOU fail closed. |
| `V3-C02-ACL-TRUST` | Protected DACL, effective principals и Docker control-plane trust list известны и owner-approved до secret/data write. |
| `V3-C03-DATA-MAP` | Каждый discovered persistent/transient/diagnostic class имеет единственный authority, backup и retention disposition. |
| `V3-C04-ATREST-REMNANTS` | VHDX/roots/pagefile/hiberfil/dumps/support boundary доказана либо real-dev блокируется до informed exception. |
| `V3-C05-DISK-PEAK` | Каждая growth operation сохраняет per-volume host reserve по измеряемой peak equation. |
| `V3-C06-COMPUTE-ENVELOPE` | Profile запускается только внутри hard CPU/RAM/commit limits, доказанных runtime inspection. |
| `V3-C07-RETENTION` | Logs/DB/executions/evidence/cache/backup имеют enforceable caps/TTL; cap pressure не вызывает auto-delete. |
| `V3-C08-BACKUP-UNIT` | Recoverable unit исчерпывающая, writers quiesced, generation/key identities связаны единым BOM. |
| `V3-C09-BACKUP-ATOMIC-AEAD` | Backup шифруется authenticated stream без persistent plaintext, публикуется атомарно и fault-safe. |
| `V3-C10-RESTORE-COLD` | Restore проверяет auth/BOM/space/target до write, не видит source/live root и честно различает L1/L2/L3. |
| `V3-C11-CLEANUP-CUSTODY` | Только exact-labelled/object-ID-bound preview может стать отдельным manual cleanup; broad prune отсутствует. |
| `V3-C12-VHDX-LIFECYCLE` | VHDX physical growth измеряется; relocation/compact/reset — отдельные gates, не repair по умолчанию. |
| `V3-C13-EVIDENCE-CUSTODY` | Trusted collector, clean output и content-addressed records не допускают stale/raw secret-bearing evidence. |
| `V3-C14-STATUS-RC` | Stable V3 states/RC показывают resources, drift, retention, backup и exact next safe action без mutation. |
| `V3-C15-TEMP-DIAGNOSTICS` | Download/temp/quarantine/dump/support/browser sinks учтены; raw diagnostic artifact не публикуется и не загружается автоматически. |
| `V3-C16-LKG-UPGRADE` | Current+LKG artifacts и pre-upgrade backup сохраняются; schema/major rollback выполняется новыми volumes, не image-only downgrade. |
| `V3-C17-KEY-CUSTODY` | n8n instance key и backup decrypt/auth material имеют разные non-secret IDs и независимую owner custody. |

Инварианты:

1. Ни один sensitive root не находится в Git repository, Obsidian Vault, `Documents`, известном sync root, UNC/mapped/network path, removable media или Docker-managed VHDX, если его назначение — пережить потерю VHDX.
2. Никакой общий Windows parent root не монтируется в контейнер. Secret projection — только отдельный файл конкретному consumer, read-only.
3. PostgreSQL/n8n backup всегда считается sensitive. На persistent Windows storage не создаётся plaintext dump/archive.
4. Свободное место Windows volume, а не логический размер Docker objects, является последней истиной для защиты host.
5. Перед любой операцией роста рассчитывается peak budget. Если хотя бы одно значение неизвестно или после пика не сохраняется host reserve — операция не начинается.
6. `docker system prune`, `docker builder prune`, `docker volume prune`, `compose down -v`, factory reset, WSL unregister и recursive delete общей data root отсутствуют во всех штатных командах.
7. Cleanup никогда не является скрытым побочным эффектом `start`, `stop`, `backup`, `restore`, `verify` или `update`.
8. Перемещение Docker data root/VHDX, изменение pagefile/hibernation/dump policy, compact/reclaim VHDX и удаление persistent volume — отдельные owner-approved изменения; этот раздел их автоматически не разрешает.
9. Потеря всего host disk не считается покрытой, пока нет независимо проверенной off-host пары backup + key custody.

## 3. Состояния и return codes V3

Строковое состояние первично; числовой RC применяется CLI. Интегратор обязан сохранить эту семантику при сведении с глобальным RC namespace.

| RC | Состояние | Семантика |
|---:|---|---|
| 0 | `V3_PASS` | Все обязательные predicates текущей операции доказаны; это не общий project PASS. |
| 10 | `V3_WARN` | Read-only status завершён, есть неблокирующая тенденция; mutation допускается только если её собственный gate = PASS. |
| 20 | `V3_BLOCKED_MANUAL` | Требуется перечисленный owner gate; mutation не началась. |
| 21 | `V3_BLOCKED_UNKNOWN` | Обязательное измерение/identity/policy неизвестно или противоречиво. |
| 22 | `V3_BLOCKED_PATH` | Root/path/volume не прошёл canonical containment. |
| 23 | `V3_BLOCKED_ACL` | Owner/DACL/effective-principal boundary не прошла. |
| 24 | `V3_BLOCKED_AT_REST` | Encryption/dump/pagefile/support-remnant policy не доказана. |
| 25 | `V3_BLOCKED_DISK` | Peak equation не сохраняет host reserve либо cap превышен. |
| 26 | `V3_BLOCKED_COMPUTE` | RAM/commit/CPU envelope не поддерживает выбранный profile. |
| 27 | `V3_BLOCKED_RETENTION` | Retention/custody не позволяет безопасно расти, а auto-delete запрещён. |
| 28 | `V3_BLOCKED_DRIFT` | Storage/resource/data-layout inventory расходится с approved lock. |
| 40 | `V3_FAIL_INTEGRITY` | Hash/authentication/BOM/identity нарушены. |
| 41 | `V3_FAIL_CONTAINMENT` | Обнаружена запись/ссылка/mount за утверждённой boundary. |
| 42 | `V3_FAIL_BACKUP` | Backup не достиг `COMPLETE`; source сохраняется, output уходит в quarantine. |
| 43 | `V3_FAIL_RESTORE` | Restore target или semantic validation не прошли; общий успех запрещён. |
| 44 | `V3_FAIL_CLEANUP_CUSTODY` | Target labels/IDs/plan hash изменились; удаление не выполняется. |
| 50 | `V3_INTERNAL_ERROR` | Scanner/collector/measurement недоступен или завершился неоднозначно; fail closed. |

`UNKNOWN`, `MANUAL_REQUIRED`, warning из другого gate и отсутствие evidence никогда не нормализуются в `PASS`.

## 4. Идентичности хранения и локальная конфигурация

### 4.1. Логические roots

Фактические пути не зашиваются в план и не публикуются в Vault/evidence. Read-only preflight предлагает кандидаты, владелец утверждает их в `MG-V3-ROOTS`, после чего локальный protected inventory хранит:

- `APP_BIN_ROOT` — vendor-managed Docker Desktop binaries;
- `DOCKER_USER_CONFIG_ROOT` — per-user Docker settings/context, не secret store;
- `DOCKER_MANAGED_ROOT` — vendor-managed WSL/data root;
- `DOCKER_VHDX` — точный managed virtual disk file/volume identity;
- `LAB_CONTROL_ROOT` — versioned local configuration/inventory без secret values;
- `LAB_SECRET_ROOT` — один файл на secret, без общего mount;
- `LAB_EVIDENCE_ROOT` — только source-allowlisted redacted evidence;
- `LAB_BACKUP_ROOT` — только complete encrypted backup generations и catalog;
- `LAB_CIPHERTEXT_STAGE_ROOT` — incomplete encrypted stream на том же filesystem, что `LAB_BACKUP_ROOT`;
- `LAB_QUARANTINE_ROOT` — failed ciphertext/support artifacts, никогда не selectable как backup;
- `LAB_DOWNLOAD_STAGE_ROOT` — verified installer/tool bytes до запуска;
- `LAB_TEMP_ROOT` — non-secret disposable files; secret-bearing generators сюда писать не вправе;
- `OWNER_KEY_CUSTODY` — владелец подтверждает наличие независимо от local secret root; путь и secret material не фиксируются.

`LAB_SECRET_ROOT` не может быть дочерним каталогом root, который когда-либо bind-mounted целиком. `LAB_BACKUP_ROOT` и `OWNER_KEY_CUSTODY` не могут находиться внутри `DOCKER_MANAGED_ROOT`/`DOCKER_VHDX`. Для заявленного VHDX-loss recovery backup root обязан быть на Windows filesystem вне VHDX. Отдельный physical disk/off-host storage не предполагается; его отсутствие фиксируется как residual risk.

### 4.2. Canonical path/volume predicate `V3-PATH-QUALIFIED`

Каждый Windows root до первой записи и перед каждой security-sensitive записью проходит один алгоритм:

1. Путь абсолютный; environment variables полностью разрешены; UNC, device share, mapped drive, `SUBST`, network mount и removable drive отклоняются.
2. Root и каждый существующий ancestor открываются handle-based без следования ссылке; фиксируются redacted fingerprints volume GUID и file ID. String-only `Resolve-Path` недостаточен.
3. Все ancestors и leaf проверяются на reparse tag. Junction, symlink, mount-point reparse, Cloud Files placeholder и неизвестный tag дают `V3_BLOCKED_PATH`.
4. Windows volume имеет `DriveType=Fixed`, локальный filesystem с ACL; для создаваемых lab roots требуется NTFS. Неизвестный filesystem блокирует.
5. Путь не лежит под известным OneDrive/Dropbox/другим sync root; cloud/offline/recall attributes отсутствуют. Неопределимая sync policy блокирует sensitive roots.
6. Имя round-trip совпадает по ожидаемому case и Unicode representation; colon разрешён только после drive letter; NTFS ADS запрещены.
7. Для файла проверяется link count `1`; существующий leaf не перезаписывается без exact identity. Новые файлы создаются exclusive, затем публикуются same-volume atomic replace.
8. Перед open, после open и после atomic replace повторно сравниваются volume/file identity и parent identities. Расхождение означает TOCTOU и `V3_FAIL_CONTAINMENT`.
9. Raw canonical path хранится только в локальном protected inventory; evidence содержит logical root ID и run-scoped keyed fingerprint.

Изменение любого approved root/volume identity переводит inventory в `DRIFTED`; relocation — не автоматический repair, а отдельный destructive migration gate.

### 4.3. ACL и effective principals

Роли различаются:

- `OPERATOR_SID` — ежедневный non-elevated владелец;
- `ELEVATION_PRINCIPAL` — только UAC installer action, не owner lab data;
- `SYSTEM` и vendor service identities;
- локальные Administrators, `docker-users`, Backup Operators и все principals с Docker named-pipe/control-plane access;
- неутверждённые standard users.

Для `LAB_SECRET_ROOT`, `LAB_BACKUP_ROOT`, `LAB_CIPHERTEXT_STAGE_ROOT`, `LAB_QUARANTINE_ROOT`:

- owner = `OPERATOR_SID`;
- DACL protected, inheritance disabled;
- allow ACE только `OPERATOR_SID` и `SYSTEM`, если отдельный contract не докажет необходимый service principal;
- broad groups (`Users`, `Authenticated Users`, `Everyone`, неизвестные SID), Backup Operators или write/read через ancestor блокируют;
- child ACL/mode проверяется после atomic creation;
- effective access проверяется машинно canary-файлом, а не только чтением ACL text.

`LAB_CONTROL_ROOT` и `LAB_EVIDENCE_ROOT` также не допускают broad write. Evidence может стать read-only после sealing.

Docker Desktop VHDX имеет vendor ACL; его не переписывают. Вместо этого `EV-V3-ACL` связывает его owner/effective principals с control-plane trust list. Любой principal, управляющий Docker daemon, считается способным извлечь container secrets/volumes даже без NTFS read. Компрометация approved Administrator/SYSTEM остаётся residual risk и должна быть принята владельцем в `MG-V3-TRUST-BOUNDARY`.

## 5. Полная data map

| ID | Класс и authority | Физическая/логическая граница | Чувствительность | Backup/retention | Разрешённые writers и удаление |
|---|---|---|---|---|---|
| `DM-V3-01` | Docker Desktop application binaries | `APP_BIN_ROOT`, Windows | executable | Не входит в data backup; exact installer/current+LKG определяется supply-chain lock | Только signed installer/update gate; uninstall отдельный gate |
| `DM-V3-02` | Docker per-user config/context | `DOCKER_USER_CONFIG_ROOT`, Windows | control-plane metadata, потенциально endpoints | Versioned secret-free inventory; raw config не попадает в evidence | Docker Desktop/operator; не чистится lab cleanup |
| `DM-V3-03` | Docker managed data/VHDX | `DOCKER_MANAGED_ROOT`/`DOCKER_VHDX` | sensitive: volumes, layers, writable layers, logs, remnants | Сам VHDX не считается backup; relocation/compact/reset отдельно | Только Docker Desktop; ручное destructive управление |
| `DM-V3-04` | PostgreSQL authoritative data | project-scoped named volume `local_postgres_data` | sensitive/high | Обязательный logical encrypted backup; DB-specific retention ниже | PostgreSQL UID; routine cleanup запрещён |
| `DM-V3-05` | n8n user directory | project-scoped `local_n8n_data` | sensitive/high | Обязательный consistent encrypted backup | n8n documented UID/GID; routine cleanup запрещён |
| `DM-V3-06` | n8n binary/files backend | project-scoped `local_n8n_files` либо явно `ABSENT` | sensitive/high | Обязательный backup, если существует; `ABSENT` доказан config/runtime | Только n8n; routine cleanup запрещён |
| `DM-V3-07` | Bridge offset/state | project-scoped `local_bridge_state` или PostgreSQL authority, ровно один | pseudonymous operational state | Backup в том же generation, bot/environment/key binding | Bridge/DB transaction; reset только owner gate |
| `DM-V3-08` | Custom/community nodes | Baked pinned image либо `ABSENT`; не mutable volume по умолчанию | executable | Версия в supply-chain lock, не data backup | Только reviewed image build/update |
| `DM-V3-09` | Image layers/build cache | VHDX, Docker content store | executable/cache | Current+LKG policy; cache не является recovery source | Pull/build gate; cleanup только exact preview |
| `DM-V3-10` | Container writable layers | VHDX | transient, может содержать sensitive remnants | Не backup authority | Compose lifecycle; deletion только object custody |
| `DM-V3-11` | Docker JSON/container logs | VHDX | secret/PII risk | rotation `10 MiB × 3` на container; raw logs не evidence | Docker logging driver; exact object cleanup |
| `DM-V3-12` | Secret source files | `LAB_SECRET_ROOT`, Windows | secret/critical | Не включаются в backup payload; independent custody required by class | Owner-only ceremony; one file/consumer, no broad mount |
| `DM-V3-13` | n8n instance key recovery copy | `OWNER_KEY_CUSTODY`, вне live secret root | secret/critical | Сохраняется независимо; BOM содержит только keyed ID | Только owner; agent не читает |
| `DM-V3-14` | Backup decrypt/auth key custody | `OWNER_KEY_CUSTODY`, отдельно от ciphertext | secret/critical | Отдельно от backup и live root | Только owner; agent не читает |
| `DM-V3-15` | Control inventory/status | `LAB_CONTROL_ROOT`, Windows | internal, secret-free | Current+previous approved inventory | Trusted wrapper; atomic write |
| `DM-V3-16` | Evidence | `LAB_EVIDENCE_ROOT`, Windows | allowlisted/redacted only | 90 days proposal; accepted anchors protected until release decision | Trusted collector only; candidate cannot seal |
| `DM-V3-17` | Complete backups | `LAB_BACKUP_ROOT`, Windows, вне VHDX | encrypted sensitive | Минимум две restore-verified generations после их появления + current pre-upgrade; actual count/bytes owner-approved | Single backup writer; deletion only exact manual gate |
| `DM-V3-18` | Backup ciphertext staging | `LAB_CIPHERTEXT_STAGE_ROOT`, same filesystem as final | encrypted incomplete | До завершения run; failure -> quarantine, никогда `COMPLETE` | Single writer, exclusive ID, atomic rename |
| `DM-V3-19` | Failed artifacts/quarantine | `LAB_QUARANTINE_ROOT` | potentially sensitive/encrypted | Max age/bytes owner-approved; no auto-delete/upload | Manual inspected exact cleanup only |
| `DM-V3-20` | Installer/tool download staging | `LAB_DOWNLOAD_STAGE_ROOT` | executable | До verified install + required LKG set | Supply-chain wrapper; identity-safe deletion only |
| `DM-V3-21` | Generic temporary data | `LAB_TEMP_ROOT`, Windows | non-secret only | Invocation-scoped; lingering item blocks next clean run | Trusted wrapper; exact manual cleanup |
| `DM-V3-22` | Gate output volumes/cache | run-scoped disposable named volume | untrusted until collector validates | Empty at start; selected evidence exported source-allowlisted | Candidate writes output only; manual exact cleanup |
| `DM-V3-23` | Windows pagefile/hiberfil | Windows system-managed volume | possible secret/PII remnants | Не backup; secure erase не обещается | OS only; policy read-only inventory, no auto-change |
| `DM-V3-24` | WER/process/kernel dumps | configured Windows dump locations | secret/PII risk | Raw dump запрещён в evidence; incident quarantine only | OS/vendor; collection/upload policy gate |
| `DM-V3-25` | Docker support bundle/diagnostics | vendor-selected temp/support location | presumed secret-bearing | Не создаётся штатно; encrypted quarantine only after owner incident gate | Owner-visible vendor workflow; no auto-upload |
| `DM-V3-26` | Browser downloads/exports/screenshots/clipboard | Windows user/UI stores | secret/PII risk | Не authoritative; raw captures forbidden; clipboard cleared by owner ceremony | Owner only; evidence runbook governs |
| `DM-V3-27` | Project repository and Vault | отдельные Windows roots | source/docs; secret values forbidden | Git/Vault governance independently | Read-only для runtime; никогда backup/temp/secret root |

Каждый data class имеет ровно один `authority` либо явное `ABSENT`. Startup/backup получает `V3_BLOCKED_UNKNOWN`, если discovered persistent class отсутствует в map или обязательный class не сопоставлен BOM.

## 6. At-rest, pagefile, dumps и support boundary

### 6.1. Gate `V3-ATREST-QUALIFIED`

Read-only preflight для каждого volume, содержащего `DM-V3-03..25`, фиксирует:

- local/fixed/removable/network classification;
- filesystem и volume fingerprint;
- BitLocker/Device Encryption state и protection state без recovery key/serial;
- root ancestry, reparse/sync/cloud attributes;
- location и protection volume для pagefile/hiberfil;
- WER/application dump policy и automatic upload/diagnostic settings;
- search indexing attribute для lab roots;
- known backup/sync agent coverage только как redacted policy result.

Нормальный `real-dev` требует шифрование device/full volume со статусом protection `ON` для Windows volume с VHDX, secret root, backup root, pagefile/hiberfil и dumps. `UNKNOWN`, suspended protection или plaintext volume даёт `V3_BLOCKED_AT_REST`.

Если включение шифрования не разрешено планом A или владелец сознательно выбирает риск, допускается только отдельный `MG-V3-ATREST-EXCEPTION`: показывает, какие exact classes могут остаться на диске, что ACL не защищает offline access/Administrator/SYSTEM, что SSD/VHDX/pagefile secure erase не обещается, и срок действия решения. Без этого real secrets и real Telegram profile не запускаются; synthetic mock может работать только без persistent secret/PII canaries.

Raw dump/support bundle не создаётся, не сканируется обычным redactor и не прикладывается к evidence. `MG-V3-SUPPORT-BUNDLE` разрешает один exact incident artifact в encrypted quarantine, без automatic upload, с owner review и отдельным решением о передаче.

## 7. Измеряемый бюджет диска и host reserve

### 7.1. Базовые величины

Для каждого затрагиваемого Windows volume `v`:

- `C(v)` — capacity bytes;
- `F(v,t)` — реально свободные bytes непосредственно перед операцией;
- `A(v,t)` — allocated physical bytes файлов/данных в scope; для sparse VHDX учитывается физически выделенное место, а не virtual maximum;
- `R(v)` — непотребляемый host reserve;
- `G(op,v)` — верхняя оценка дополнительного allocated growth до пика операции;
- `M(op,v) = max(2 GiB, ceil(0.10 × G(op,v)))` — measurement/error margin;
- `Pfree(op,v) = F(v,t0) - G(op,v) - M(op,v)`.

Значение по умолчанию до owner adjustment:

```text
R(v) = max(20 GiB, ceil(0.15 × C(v)))  для system volume либо volume с Docker VHDX
R(v) = max(10 GiB, ceil(0.10 × C(v)))  для отдельного approved fixed local data volume
```

Владелец может увеличить reserve обычным решением. Уменьшение — только `MG-V3-RESOURCE-RISK`, с exact old/new values, причиной и сроком; ниже 10 GiB на system/VHDX volume plan не разрешает снижать.

Операция разрешена, только если для каждого volume одновременно:

```text
Pfree(op,v) >= R(v)
A_lab_after_peak(v) <= OWNER_APPROVED_LAB_CAP(v)
A_backup_after_peak(v) <= OWNER_APPROVED_BACKUP_CAP(v)
all inputs measured or deterministically bounded
```

Если roots находятся на одном volume, все growth components суммируются, а reserve вычитается ровно один раз. Logical Docker size, `docker system df` reclaimable и sparse unallocated VHDX space не считаются свободным Windows disk.

### 7.2. Определение `G(op,v)`

`G` хранится с operation plan hash. Для уже квалифицированной exact operation используется максимум из deterministic bound и `1.25 ×` наибольшего измеренного peak delta для того же digest/config/profile. Новый digest/config не наследует меньшую оценку.

| Операция | Обязательная верхняя оценка роста до первого write |
|---|---|
| `download` | Declared Content-Length всех файлов + `256 MiB`; download идёт прямо в unique staging file без второй plaintext копии. Unknown length блокирует. |
| `install` | `max(10 GiB, 4 × installer bytes)` до появления измеренного exact-version install delta; уже существующая Docker data добавляется отдельно. |
| `pull` | `4 × sum(missing compressed OCI layers) + 2 GiB`; existing shared layer dedup учитывается только после exact digest inspection. |
| `build` | `G_pull(base) + 3 × build-context bytes + declared output bound + 4 GiB`; unknown/unbounded generator блокирует. |
| `start` | Sum per-service declared session growth budgets + writable-layer budget + max rotated logs; никакой implicit pull/build. |
| `backup` | На backup volume: authenticated BOM upper bound `1.05 × total logical source bytes + 256 MiB`; на Windows temp volume plaintext growth = `0`; source changes quiesced. |
| `restore` | На Docker/VHDX volume: `1.35 × BOM uncompressed component bytes + missing-image pull bound + 2 GiB`; на Windows temp volume plaintext growth = `0`. |
| `update` | Preserve current+LKG + pull/build bound + полный cloned restore/upgrade target + backup bound; in-place data reuse не уменьшает расчёт. |
| `cleanup` | Рост `0`; reclaimable bytes показываются только как preview и никогда заранее не прибавляются к `F`. |

Во время квалификационного выполнения collector с интервалом не более 2 секунд записывает только byte counters: host free, VHDX allocated, Docker total/lab-labelled, backup/stage/quarantine. Если фактический peak выходит за bound или приближается к `R(v)+M`, новые jobs блокируются, writers orderly quiesce, состояние `V3_FAIL_BUDGET`; автоматическое удаление или kill PostgreSQL запрещены.

### 7.3. Hard pre-growth gates

Каждая команда `pull`, `build`, `start`, `backup`, `restore-drill`, `update` обязана в одном read-only preview вывести:

- operation ID/hash и exact Docker endpoint dependency;
- logical roots и redacted volume fingerprints;
- `F`, `R`, `G`, `M`, `Pfree`, lab/backup caps до и после;
- current VHDX allocated bytes, Docker total/lab-labelled bytes и trend;
- какие images/volumes/files будут созданы;
- status/RC и одно безопасное следующее действие.

После preview identities и measurements повторяются непосредственно перед первым mutation. Изменение делает preview stale и возвращает `V3_BLOCKED_DRIFT`; silently recalculate-and-run запрещено.

## 8. CPU/RAM/runtime limits

### 8.1. Host envelope

До первого container start фиксируются installed RAM, available physical RAM, Windows commit limit/charge и logical CPU count. Host reserve:

```text
RAM_RESERVE = max(4 GiB, ceil(0.25 × installed_RAM))
CPU_LAB_BUDGET = min(4.0, max(1.5, 0.50 × logical_CPU_count))
```

Start profile проходит только если и available physical, и available commit не меньше `RAM_RESERVE + sum(profile hard memory limits)`. Если CPU budget меньше суммы hard CPU limits, profile блокируется; автоматического изменения pagefile, `.wslconfig`, BIOS, power policy или Docker global resource setting нет.

### 8.2. Начальный enforceable service envelope

| Profile/service | Hard RAM | Hard CPU | Дополнительный предел |
|---|---:|---:|---|
| PostgreSQL | 768 MiB | 0.75 | DB cache/work memory настраиваются так, чтобы поместиться; OOM = FAIL, не auto-restart loop |
| n8n regular single-process | 1536 MiB | 1.50 | Node heap не более 1024 MiB; queue/worker topology не допускается этим envelope |
| Telegram bridge | 256 MiB | 0.25 | Один poller; bounded buffers |
| Mock Telegram | 128 MiB | 0.25 | Только mock profile |
| Mock LLM | 256 MiB | 0.25 | Только mock profile |
| Backup one-shot | 768 MiB | 0.50 | Все application writers остановлены |
| Gate runner | 2048 MiB | 1.50 | Application stack остановлен; один gate одновременно |
| Isolated restore PostgreSQL+n8n | 2304 MiB total | 2.00 total | Source stack остановлен; no egress/ports — cross-domain gate |

Compose implementation должна использовать реально действующие для выбранного Docker Compose режима limits; acceptance сверяет `docker inspect`, а не только YAML. Если exact n8n/PostgreSQL конфигурация не помещается, это новый reviewed change, а не silent increase.

## 9. Retention и growth policy

| Класс | Политика v2 | Enforcement |
|---|---|---|
| Container logs | `max-size=10 MiB`, `max-file=3` для каждого container | Compose render + runtime inspect; отсутствие rotation блокирует start |
| n8n execution payload | Для `real-dev`: persistent success/error/manual payload = 0; raw Telegram/LLM body не является допустимым execution record | Exact-version n8n settings + DB/volume canaries; если невозможно доказать — real-dev BLOCKED |
| Synthetic mock executions | TTL 24 h, maximum 1000 records; только synthetic markers | Size/count status; owner-triggered exact purge |
| Dedup/outbox operational metadata | TTL 30 days после terminal state, без raw text/IDs | DB job/status; deletion test cross-domain |
| Bridge offset | До decommission/rotation конкретного dev bot; не time-pruned | Bound to bot/environment/schema/checksum; reset owner-gated |
| Application memory/test data | По умолчанию synthetic; real-dev raw message body не хранится; допустимые derived records/TTL определяет privacy contract | Unknown fields block real-dev; backup inherits shortest applicable data expiry classification |
| PostgreSQL logical growth | `OWNER_APPROVED_DB_CAP`; warn at 70%, block new real-dev/manual runs at 85%, hard stop new writes at 95% с orderly quiesce | `status` показывает bytes/table trend; no auto-delete |
| Evidence | Proposal: 90 days; последний accepted gate anchor и текущий investigation сохраняются независимо от TTL | Expired помечается; удаление только preview/apply owner gate |
| Backup | После начального периода минимум 2 `COMPLETE+RESTORE_VERIFIED` generations и 1 pre-upgrade generation; byte cap не меньше `2 × largest verified generation + margin` | Expired/cap-exceeded блокирует следующий backup; last verified никогда не удаляется автоматически |
| Current/LKG artifacts | Current и один last-known-good installer/image set до прохождения нового restore/update drill | Supply-chain inventory; deletion owner-gated |
| Ciphertext stage/quarantine | Stage только текущего run; quarantine age/bytes owner-approved, не selectable | Cap превышен = `V3_BLOCKED_RETENTION`; manual exact cleanup |

RPO/RTO proposal для owner gate: backup после каждого credential/workflow/schema change и перед update, плюс не реже одного раза в 7 календарных дней активного использования; stale warning 7 дней, real-dev start block 14 дней. Целевые RPO/RTO и покрываемые data classes утверждаются `MG-V3-BACKUP-POLICY` после первого measured restore; до этого нельзя писать «disaster recovery complete».

## 10. Backup contract

### 10.1. Recoverable unit

Generation BOM обязан перечислять `PRESENT/ABSENT/NOT_APPLICABLE` для:

- всех PostgreSQL databases, globals, roles/memberships/grants/ownership, encodings/collations/extensions и migration history;
- `local_n8n_data`;
- configured binary/files backend;
- single bridge offset authority;
- approved custom/community-node state либо доказанное `ABSENT`;
- exact Compose/config/schema/image/tool digests;
- n8n instance-key identifier и backup-recipient/auth identifier без key material;
- consistency generation ID во всех captured components;
- logical/uncompressed sizes для restore budgeting.

Cache, container logs и evidence не являются recoverable application unit и перечисляются как excluded. `COMPLETE` запрещён при неизвестном обязательном class.

### 10.2. State machine

```text
IDLE -> LOCKED -> QUIESCING -> QUIESCED -> CAPTURING
     -> SEALED -> VERIFIED -> COMPLETE -> RESTORE_VERIFIED
any pre-COMPLETE failure -> QUARANTINED
```

1. `LOCKED`: Windows single-writer lock + DB advisory lock; существующий run/backup ID блокирует.
2. `QUIESCING`: disarm/stop bridge; stop n8n main/task runners/workers; stop migrations, retention and mutation jobs; block UI/API writes.
3. `QUIESCED`: PostgreSQL остаётся только для backup; проверяется исчерпывающий session inventory и отсутствие writer sessions. Пишется generation marker.
4. `CAPTURING`: pinned same-major PostgreSQL client получает globals и каждую declared DB; volumes/files читаются при остановленных writers. Потоки сразу входят в authenticated encrypted stream.
5. `SEALED`: внутренний BOM находится внутри ciphertext; внешний secret-free catalog содержит backup ID, ciphertext SHA-256, size, recipient/key IDs, plan/config/digest identities и state `SEALED`.
6. `VERIFIED`: ciphertext полностью аутентифицируется; второй no-write pass расшифровывает поток только в validator и проверяет archive paths, hashes, BOM и declared sizes. Persistent plaintext отсутствует.
7. `COMPLETE`: same-filesystem atomic rename из ciphertext stage; catalog state публикуется атомарно. Только теперь generation selectable.
8. `RESTORE_VERIFIED`: выставляется отдельным successful isolated restore evidence, не самим backup writer.

Fail-safe resume всегда освобождает application write lock только после явной проверки состояний. Failure оставляет source volumes неизменными и создаёт только `QUARANTINED` ciphertext metadata; auto-delete failed artifact запрещён.

Конкретный AEAD/tool/version, key generation и acquisition hash закрепляет supply-chain/secrets contract. Минимальные свойства V3: authenticated streaming, random nonce/salt, no secret in arguments/environment/logs, authentication before target writes, independent owner custody и deterministic wrong-key/tamper failure. Пока tool lock не утверждён, backup = `V3_BLOCKED_UNKNOWN`.

## 11. Restore и recovery tiers

### 11.1. Restore preconditions

`restore-drill` до любого target write проверяет:

- backup ID входит в local allowlist catalog и имеет `COMPLETE`;
- ciphertext hash, authentication, внутренний BOM и expected key IDs;
- exact version/platform compatibility и source/LKG artifact availability;
- `G(restore)` и host reserve;
- unique cryptographic run/project nonce;
- отсутствие target containers/networks/volumes и name/label collision;
- отсутствие mounts к source volumes, live secret root, backup root или repo/Vault;
- no-egress/no-host-port/disabled trigger contract из network/service domains.

Owner вводит backup key и n8n key через отдельную non-echo ceremony; live secret root удалён из environment и не монтируется. Первый decrypt pass только валидирует stream. После этого создаются новые project-scoped volumes. Extractor отклоняет absolute/parent traversal, escaping symlink/hardlink, devices, ADS и unexpected UID/GID/mode. Старые images никогда не запускаются против migrated live volumes.

### 11.2. Recovery tiers

| Tier | Что доказывается | Условие статуса |
|---|---|---|
| `L1 logical restore` | Новый Compose project и volumes при существующем Docker Desktop | Полный isolated restore + semantic/permission/key canaries |
| `L2 VHDX-loss readiness` | Backup/custody не зависят от source VHDX; config/images можно восстановить из approved sources/LKG | Backup физически вне VHDX, keys independently supplied, source mounts/live root запрещены; реальная утрата VHDX не симулируется без отдельного destructive gate |
| `L3 host-loss DR` | Потеря Windows disk/machine | Вне текущего утверждения; только после independent off-host artifact+key custody и clean-host drill |

Нельзя называть L1 «полной disaster recovery». `MG-V3-HOSTLOSS-DRILL` требуется для destructive clean-Docker/VHDX-loss rehearsal. До него residual risk: Docker Desktop reinstall/host loss может быть непроверен.

## 12. Cleanup и VHDX growth

### 12.1. Двухфазный manual cleanup

`lab cleanup preview` — read-only и создаёт immutable cleanup plan:

- plan ID/hash, TTL и owner-visible reason;
- Docker endpoint/project dependency;
- exact object IDs, creation timestamps и полный label tuple: scope, authority, run, candidate, resource class, disposable;
- Windows logical root, volume/file fingerprints, size и retention/backup dependencies;
- доказательство, что target не persistent lab volume, current/LKG, last verified backup, secret/key source или foreign object;
- expected reclaimed bytes, которые не прибавляются к budget до фактического удаления.

`lab cleanup apply <plan-id>` требует интерактивного owner confirmation и повторяет endpoint/path/object/label/identity checks. Missing/extra/changed target возвращает RC 44 и удаляет `0` объектов. Каждый target удаляется индивидуально; partial result честно перечисляется. Никакие globs, parent-recursive deletion или broad Docker prune не допускаются.

Persistent volumes, backup generations, secret files, Docker data/VHDX и LKG artifacts имеют отдельные named destructive gates. Routine cleanup может только предложить expired disposable targets; автоматического применения нет.

### 12.2. VHDX

`status` различает virtual maximum, logical Docker usage и physical allocated VHDX bytes. Shrink/compact не считается гарантированным после удаления объектов. Compact/reclaim разрешается только `MG-V3-VHDX-RECLAIM`: Docker полностью остановлен, backup `RESTORE_VERIFIED`, exact vendor procedure/source, before/after disk identities, rollback limitations и owner approval. Factory reset/WSL unregister не является reclaim.

## 13. Owner gates и residual risks

| Gate | Момент | Что владелец видит и принимает |
|---|---|---|
| `MG-V3-ROOTS` | До download/install/data creation | Exact local paths, volume fingerprints, drive/filesystem/sync/reparse facts; data-root relocation в будущем destructive |
| `MG-V3-TRUST-BOUNDARY` | До secret write | Effective principals для roots и Docker control plane; Administrator/SYSTEM способны извлекать data |
| `MG-V3-ATREST-EXCEPTION` | Только если encryption/remnant policy не PASS | Конкретные unprotected classes, pagefile/VHDX/dump risks, срок и profiles; без gate real-dev blocked |
| `MG-V3-RESOURCE-THRESHOLDS` | После read-only measurement | `R`, lab/DB/backup/evidence/quarantine caps, RAM/CPU envelope, expected peak операций |
| `MG-V3-RESOURCE-RISK` | При снижении reserve/caps | Exact delta и риск host exhaustion; ниже absolute floor запрещено |
| `MG-V3-KEY-CUSTODY` | До first credential/backup | Независимое наличие n8n key и backup decrypt/auth material; значения не читает агент |
| `MG-V3-BACKUP-POLICY` | До D10/active use | Destination, minimum generations, byte cap, RPO/RTO, stale behavior, L1/L2/L3 boundary |
| `MG-V3-CLEANUP-<plan-id>` | Каждое material deletion | Exact targets/hashes/labels, size, rollback limits; никакого prune |
| `MG-V3-SUPPORT-BUNDLE` | Только incident | Exact vendor artifact, encrypted quarantine, отсутствие auto-upload, owner review/transmission decision |
| `MG-V3-VHDX-RECLAIM` | Перед compact/relocate/reset | Downtime, verified backup, exact vendor procedure, destructive limits |
| `MG-V3-HOSTLOSS-DRILL` | Перед реальной недоступностью VHDX/clean Docker | Destructive scope, recoverability prerequisites, rollback |
| `MG-V3-UPDATE-DATA` | Перед schema/major/data-layout update | Pre-upgrade restore-verified backup, clone, peak space, no in-place downgrade |

Непокрытые residual risks до соответствующих gates:

- approved Administrators/SYSTEM/Docker control-plane могут извлечь secrets;
- удаление файла не гарантирует secure erase SSD/VHDX/pagefile;
- ACL не защищает offline plaintext volume;
- backup вне VHDX, но на том же physical Windows disk, не покрывает host-disk loss;
- corporate dump/sync/backup agents с неизвестной policy блокируют real-dev;
- Docker Desktop/WSL storage implementation может изменить path/layout при update;
- no-prune/manual retention может остановить новые операции до решения владельца — это намеренный fail-safe.

## 14. Acceptance tests, negative canaries и evidence

### 14.1. Acceptance tests

| ID | Проверка |
|---|---|
| `AT-V3-01` | Table-driven path qualification: local NTFS PASS; UNC/mapped/removable/ReFS-or-unknown/sync/reparse/ADS/case-Unicode ambiguity BLOCKED до write. |
| `AT-V3-02` | ACL/effective principals: owner canary читается operator; чужой standard user не читает root/Engine; каждый Engine principal присутствует в approved trust list. |
| `AT-V3-03` | At-rest/remnants: redacted volume encryption, pagefile/hiberfil/dump/support policy; UNKNOWN/OFF блокирует real-dev либо требует exact exception. |
| `AT-V3-04` | Data-map completeness: discovered persistent/mount/log/temp class без `DM-V3-*` и BOM disposition блокирует start/backup. |
| `AT-V3-05` | Disk boundary fixtures по обе стороны `R+G+M` для download/install/pull/build/start/backup/restore/update; below case делает zero mutation. |
| `AT-V3-06` | Compose/inspect подтверждает hard RAM/CPU/log limits; малый host envelope блокирует profile; никакого pagefile/global auto-tuning. |
| `AT-V3-07` | DB/log/evidence/backup retention fixtures: 70/85/95% states, expired generation, cap exceeded; last verified и persistent volumes не предлагаются routine cleanup. |
| `AT-V3-08` | Backup writer matrix: UI/API/n8n/bridge/migration/retention writes блокированы; generation marker совпадает в DB/files/offset/BOM. |
| `AT-V3-09` | Streaming encryption: plaintext marker отсутствует в Windows roots/temp/log/evidence при success и interruption; wrong key/bit flip/truncation отклонены до target write. |
| `AT-V3-10` | Backup fault matrix: concurrent run, reused ID, disk-full, permission failure, termination каждой фазы; только verified artifact получает COMPLETE, source/last-good неизменны. |
| `AT-V3-11` | Restore target containment: collision, foreign labels, hostile paths, UID/GID/mode; zero writes при preflight failure, source volumes unchanged. |
| `AT-V3-12` | Cold logical restore: source volumes/live secret root inaccessible; keys supplied independently; credential/DB/file/offset canaries восстановлены без egress/ports. |
| `AT-V3-13` | Cleanup: foreign same-label/changed tuple/missing label/stale plan не удаляются; exact current disposable inventory удаляется только после manual gate. |
| `AT-V3-14` | Evidence/support: nested/encoded/path/header/UI/support fixtures не публикуются; unknown schema/scanner error = RC 50. |
| `AT-V3-15` | Update/data migration: clone uses full peak budget; failure after migration restores pre-upgrade generation in new volumes; old image + migrated volume rejected. |
| `AT-V3-16` | Status/doctor golden states: low disk, cap, VHDX growth, stale backup, drift, Docker stopped; JSON/human output согласованы, doctor read-only. |
| `AT-V3-17` | Two clean runs begin with empty output volume and no lingering temp; normalized result hashes equal; stale evidence cannot satisfy current run. |

### 14.2. Negative canaries

| ID | Canary и ожидаемый результат |
|---|---|
| `NC-V3-01` | Junction parent, symlink leaf, external hardlink, ADS, directory swap, case/Unicode alias -> RC 22/41, outside sentinel unchanged. |
| `NC-V3-02` | Broad inherited ACL/unknown SID/foreign Engine principal -> RC 23 до secret/data write. |
| `NC-V3-03` | Sync/cloud placeholder, removable/UNC path, unknown volume encryption -> RC 22/24. |
| `NC-V3-04` | Free-space fixture на 1 byte ниже required peak -> RC 25 и zero new Docker/file object. |
| `NC-V3-05` | Available RAM/commit на 1 byte ниже envelope или CPU budget ниже profile -> RC 26 до container start. |
| `NC-V3-06` | Unbounded log/DB growth и cap boundary -> admission stop без prune/delete; orderly quiesce evidence. |
| `NC-V3-07` | Unique plaintext marker в DB/files при success/abort backup -> marker только внутри authenticated ciphertext; иначе RC 42. |
| `NC-V3-08` | Duplicate backup ID, concurrent lock, partial catalog, changed ciphertext/BOM -> не selectable, quarantine only. |
| `NC-V3-09` | Existing restore volume/project, foreign label, archive traversal/device/symlink escape -> RC 43 до target mutation. |
| `NC-V3-10` | Live secret root/source volume made visible to restore -> containment validator blocks; no false cold-restore PASS. |
| `NC-V3-11` | Synthetic dump/support bundle with secret marker -> ordinary evidence pipeline rejects whole artifact; no auto-upload. |
| `NC-V3-12` | Foreign/stale cleanup label tuple and stale plan hash -> RC 44, zero deletes. |
| `NC-V3-13` | Missing/wrong n8n key or backup key -> restore/start blocked before n8n serves; raw key never emitted. |
| `NC-V3-14` | Old n8n/PostgreSQL image against upgraded state -> hard pre-start rejection, no volume mutation. |
| `NC-V3-15` | Evidence from previous run preloaded in cache/output -> clean-run gate rejects before validator. |

### 14.3. Evidence records

Evidence source-allowlisted, secret-free, с schema и hashes. Raw paths, usernames, SID, volume serials, Telegram IDs, keys, dumps и support bundles не входят.

| ID | Содержимое |
|---|---|
| `EV-V3-01-ROOT-INVENTORY` | Logical root IDs, run-scoped path/volume fingerprints, drive/filesystem/reparse/sync result, inventory hash. |
| `EV-V3-02-ACL-PRINCIPALS` | Redacted SID fingerprints, owner/protected DACL/effective rights, Engine trust-list correlation. |
| `EV-V3-03-ATREST-REMNANTS` | Encryption/protection state classes, pagefile/hiberfil/dump/support policy result, owner exception ID if any. |
| `EV-V3-04-DATA-MAP-BOM` | Every `DM-V3-*` disposition, authority, mount/backup/retention mapping; no values/content. |
| `EV-V3-05-RESOURCE-BASELINE` | Capacity/free/allocated/VHDX/Docker/lab/backup measurements, trend, owner threshold record. |
| `EV-V3-06-OPERATION-BUDGET` | Per-operation `F/R/G/M/Pfree`, exact input digests, preview hash, before/peak/after counters, RC. |
| `EV-V3-07-RUNTIME-LIMITS` | Rendered safe fields + inspect CPU/RAM/log limits and host envelope result. |
| `EV-V3-08-RETENTION-STATUS` | Counts/bytes/ages by class, stale/cap states, no-delete attestation. |
| `EV-V3-09-BACKUP-GENERATION` | State transitions, writer/session assertions, ciphertext/BOM hashes, key IDs, COMPLETE/QUARANTINED state. |
| `EV-V3-10-BACKUP-FAULT-MATRIX` | Case IDs, exact fixture/ciphertext/image hashes, RC/assertions, source/last-good invariance. |
| `EV-V3-11-RESTORE-DRILL` | Target nonce/object IDs, source-inaccessibility proof, preflight/semantic/permissions/key results, no-egress dependency. |
| `EV-V3-12-CLEANUP-CUSTODY` | Preview/apply plan hash, exact labels/IDs, owner gate, per-target result, persistent-object invariance. |
| `EV-V3-13-EVIDENCE-CUSTODY` | Manifest path-bytes-hashes, run/candidate/collector IDs, anchor and scanner self-test. |
| `EV-V3-14-UPDATE-RECOVERY` | Pre-upgrade generation, clone/peak budget, from/to locks, migration/failure/rollback result. |
| `EV-V3-15-OWNER-RISK` | Gate IDs, exact non-secret decision fields, expiry and residual-risk text hash. |
| `EV-V3-16-NO-CHANGE` | Для blocked/dry-run cases: no new file/Docker object, source/last-good invariance, RC. |

## 15. Traceability к baseline findings

Ниже перечислены все findings, которые V3 принимает во владение. Для каждого есть минимум один contract, acceptance test, negative canary и evidence record. Другие findings остаются cross-domain dependencies, а не молча считаются закрытыми.

| Finding | V3 contract | Acceptance | Canary | Evidence |
|---|---|---|---|---|
| `R1-WIN-002` | `V3-C05-DISK-PEAK`, `V3-C06-COMPUTE-ENVELOPE` | `AT-V3-05`, `AT-V3-06` | `NC-V3-04`, `NC-V3-05` | `EV-V3-05`, `EV-V3-16` |
| `R1-WIN-004` | `V3-C02-ACL-TRUST` | `AT-V3-02` | `NC-V3-02` | `EV-V3-02`, `EV-V3-15` |
| `R1-WIN-005` | `V3-C03-DATA-MAP`, `V3-C12-VHDX-LIFECYCLE` | `AT-V3-04` | `NC-V3-03` | `EV-V3-01`, `EV-V3-04` |
| `R1-WIN-006` | `V3-C11-CLEANUP-CUSTODY`, `V3-C12-VHDX-LIFECYCLE` | `AT-V3-13` | `NC-V3-12` | `EV-V3-12`, `EV-V3-16` |
| `R1-WIN-007` | `V3-C05-DISK-PEAK` | `AT-V3-05` | `NC-V3-04` | `EV-V3-05`, `EV-V3-06` |
| `R1-WIN-008` | `V3-C01-ROOT-PATH`, `V3-C02-ACL-TRUST`, `V3-C04-ATREST-REMNANTS` | `AT-V3-01`, `AT-V3-03` | `NC-V3-01`, `NC-V3-03` | `EV-V3-01..03` |
| `R1-WIN-009` | `V3-C12-VHDX-LIFECYCLE`, `V3-C16-LKG-UPGRADE` | `AT-V3-15`, `AT-V3-16` | `NC-V3-14` | `EV-V3-14` |
| `R2-003` | `V3-C01-ROOT-PATH`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-01` | `NC-V3-01` | `EV-V3-01`, `EV-V3-16` |
| `R2-009` | `V3-C07-RETENTION`, `V3-C16-LKG-UPGRADE` | `AT-V3-15` | `NC-V3-14` | `EV-V3-08`, `EV-V3-14` |
| `R3-MOUNT-006` | `V3-C01-ROOT-PATH`, `V3-C03-DATA-MAP` | `AT-V3-04`, `AT-V3-11` | `NC-V3-01`, `NC-V3-10` | `EV-V3-01`, `EV-V3-04` |
| `R3-CLEAN-007` | `V3-C11-CLEANUP-CUSTODY` | `AT-V3-13` | `NC-V3-12` | `EV-V3-12` |
| `R4-F03` | `V3-C08-BACKUP-UNIT` | `AT-V3-12` | `NC-V3-09` | `EV-V3-09`, `EV-V3-11` |
| `R4-F04` | `V3-C03-DATA-MAP`, `V3-C06-COMPUTE-ENVELOPE`, `V3-C17-KEY-CUSTODY` | `AT-V3-04`, `AT-V3-06` | `NC-V3-13` | `EV-V3-04`, `EV-V3-07` |
| `R4-F05` | `V3-C10-RESTORE-COLD`, `V3-C16-LKG-UPGRADE` | `AT-V3-15` | `NC-V3-14` | `EV-V3-14` |
| `R4-F06` | `V3-C03-DATA-MAP`, `V3-C08-BACKUP-UNIT` | `AT-V3-08`, `AT-V3-12` | `NC-V3-08` | `EV-V3-04`, `EV-V3-09` |
| `R4-F09` | `V3-C03-DATA-MAP`, `V3-C10-RESTORE-COLD` | `AT-V3-11` | `NC-V3-09` | `EV-V3-04`, `EV-V3-11` |
| `R5-F06` | `V3-C03-DATA-MAP`, `V3-C08-BACKUP-UNIT` | `AT-V3-08`, `AT-V3-12` | `NC-V3-08` | `EV-V3-04`, `EV-V3-11` |
| `R5-F15` | `V3-C03-DATA-MAP`, `V3-C07-RETENTION` | `AT-V3-07`, `AT-V3-14` | `NC-V3-06`, `NC-V3-11` | `EV-V3-04`, `EV-V3-08` |
| `R6-P1-001` | `V3-C02-ACL-TRUST` | `AT-V3-02` | `NC-V3-02` | `EV-V3-02`, `EV-V3-15` |
| `R6-P1-002` | `V3-C02-ACL-TRUST`, `V3-C03-DATA-MAP` | `AT-V3-04`, `AT-V3-14` | `NC-V3-02`, `NC-V3-11` | `EV-V3-02`, `EV-V3-04` |
| `R6-P1-003` | `V3-C08-BACKUP-UNIT`, `V3-C17-KEY-CUSTODY` | `AT-V3-12` | `NC-V3-13` | `EV-V3-09`, `EV-V3-11` |
| `R6-P1-005` | `V3-C03-DATA-MAP`, `V3-C07-RETENTION` | `AT-V3-07`, `AT-V3-14` | `NC-V3-06`, `NC-V3-11` | `EV-V3-08`, `EV-V3-13` |
| `R6-P1-006` | `V3-C13-EVIDENCE-CUSTODY`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-14` | `NC-V3-11` | `EV-V3-03`, `EV-V3-13` |
| `R6-P1-007` | `V3-C04-ATREST-REMNANTS`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-03` | `NC-V3-03`, `NC-V3-11` | `EV-V3-03`, `EV-V3-15` |
| `R6-P1-008` | `V3-C09-BACKUP-ATOMIC-AEAD` | `AT-V3-09`, `AT-V3-10` | `NC-V3-07`, `NC-V3-08` | `EV-V3-09`, `EV-V3-10` |
| `R6-P1-009` | `V3-C03-DATA-MAP`, `V3-C15-TEMP-DIAGNOSTICS`, `V3-C17-KEY-CUSTODY` | `AT-V3-14` | `NC-V3-11`, `NC-V3-13` | `EV-V3-03`, `EV-V3-15` |
| `R6-P2-011` | `V3-C01-ROOT-PATH`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-14` | `NC-V3-11` | `EV-V3-03`, `EV-V3-16` |
| `R7-F01` | `V3-C08-BACKUP-UNIT` | `AT-V3-08` | `NC-V3-08` | `EV-V3-09` |
| `R7-F02` | `V3-C03-DATA-MAP`, `V3-C08-BACKUP-UNIT` | `AT-V3-04`, `AT-V3-12` | `NC-V3-10` | `EV-V3-04`, `EV-V3-11` |
| `R7-F03` | `V3-C08-BACKUP-UNIT` | `AT-V3-12` | `NC-V3-09` | `EV-V3-09`, `EV-V3-11` |
| `R7-F04` | `V3-C08-BACKUP-UNIT`, `V3-C17-KEY-CUSTODY` | `AT-V3-12` | `NC-V3-13` | `EV-V3-09`, `EV-V3-15` |
| `R7-F05` | `V3-C09-BACKUP-ATOMIC-AEAD` | `AT-V3-09` | `NC-V3-07` | `EV-V3-09`, `EV-V3-10` |
| `R7-F06` | `V3-C07-RETENTION`, `V3-C09-BACKUP-ATOMIC-AEAD` | `AT-V3-10` | `NC-V3-08` | `EV-V3-08..10` |
| `R7-F07` | `V3-C10-RESTORE-COLD` | `AT-V3-12` | `NC-V3-10` | `EV-V3-11` |
| `R7-F08` | `V3-C01-ROOT-PATH`, `V3-C10-RESTORE-COLD`, `V3-C11-CLEANUP-CUSTODY` | `AT-V3-11`, `AT-V3-13` | `NC-V3-09`, `NC-V3-12` | `EV-V3-11`, `EV-V3-12` |
| `R7-F09` | `V3-C10-RESTORE-COLD`, `V3-C16-LKG-UPGRADE` | `AT-V3-15` | `NC-V3-14` | `EV-V3-14` |
| `R7-F10` | `V3-C10-RESTORE-COLD`, `V3-C17-KEY-CUSTODY` | `AT-V3-12` | `NC-V3-10` | `EV-V3-11`, `EV-V3-15` |
| `R7-F11` | `V3-C07-RETENTION`, `V3-C10-RESTORE-COLD` | `AT-V3-07`, `AT-V3-12` | `NC-V3-06` | `EV-V3-08`, `EV-V3-15` |
| `R7-F12` | `V3-C09-BACKUP-ATOMIC-AEAD`, `V3-C10-RESTORE-COLD` | `AT-V3-10` | `NC-V3-07..09`, `NC-V3-13/14` | `EV-V3-10`, `EV-V3-16` |
| `R8-P1-003` | `V3-C13-EVIDENCE-CUSTODY` | `AT-V3-17` | `NC-V3-15` | `EV-V3-13` |
| `R8-P1-004` | `V3-C13-EVIDENCE-CUSTODY`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-17` | `NC-V3-15` | `EV-V3-13`, `EV-V3-16` |
| `R8-P1-010` | `V3-C13-EVIDENCE-CUSTODY` | `AT-V3-14`, `AT-V3-17` | `NC-V3-11`, `NC-V3-15` | `EV-V3-13` |
| `R8-P2-012` | `V3-C11-CLEANUP-CUSTODY` | `AT-V3-13` | `NC-V3-12` | `EV-V3-12` |
| `R9-F03` | `V3-C01-ROOT-PATH` | `AT-V3-01` | `NC-V3-01` | `EV-V3-01`, `EV-V3-16` |
| `R9-F08` | `V3-C01-ROOT-PATH`, `V3-C13-EVIDENCE-CUSTODY` | `AT-V3-01`, `AT-V3-17` | `NC-V3-01`, `NC-V3-15` | `EV-V3-01`, `EV-V3-13` |
| `R9-F10` | `V3-C03-DATA-MAP`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-04`, `AT-V3-14` | `NC-V3-01`, `NC-V3-11` | `EV-V3-04`, `EV-V3-16` |
| `R10-F03` | `V3-C10-RESTORE-COLD`, `V3-C17-KEY-CUSTODY` | `AT-V3-12` | `NC-V3-10`, `NC-V3-13` | `EV-V3-11`, `EV-V3-15` |
| `R10-F04` | `V3-C05-DISK-PEAK`, `V3-C06-COMPUTE-ENVELOPE`, `V3-C07-RETENTION`, `V3-C11-CLEANUP-CUSTODY` | `AT-V3-05..07`, `AT-V3-13` | `NC-V3-04..06`, `NC-V3-12` | `EV-V3-05..08`, `EV-V3-12` |
| `R10-F05` | `V3-C12-VHDX-LIFECYCLE`, `V3-C16-LKG-UPGRADE` | `AT-V3-15`, `AT-V3-16` | `NC-V3-14` | `EV-V3-14` |
| `R10-F08` | `V3-C14-STATUS-RC` | `AT-V3-16` | `NC-V3-04..06` | `EV-V3-05`, `EV-V3-08`, `EV-V3-16` |
| `R10-F10` | `V3-C13-EVIDENCE-CUSTODY`, `V3-C15-TEMP-DIAGNOSTICS` | `AT-V3-14` | `NC-V3-11` | `EV-V3-03`, `EV-V3-13` |
| `R10-F11` | `V3-C07-RETENTION`, `V3-C14-STATUS-RC` | `AT-V3-07`, `AT-V3-16` | `NC-V3-06` | `EV-V3-08`, `EV-V3-16` |

## 16. Cross-domain dependencies

V3 не объявляет эти области закрытыми:

1. **Windows/Docker endpoint:** daemon/context identity и Docker control-plane principals должны поступить из endpoint/Windows domain (`R1-WIN-001`, `R3-CTRL-005`, `R6-P1-001`). Без них ACL gate не PASS.
2. **Supply chain:** exact Docker installer, OCI/tool digests, AEAD/backup tools, current/LKG acquisition и licensing принадлежат supply-chain domain (`R2-001..012`). V3 использует их sizes/digests, но не подтверждает provenance.
3. **Compose/n8n/PostgreSQL:** exact roles, UID/GID, writable paths, execution settings, migrations и health graph принадлежат service domain (`R4-F01..05`). V3 задаёт storage envelope и BOM.
4. **Isolation/network:** per-service mount manifest, no-egress restore/gate и privileged blast radius принадлежат isolation domain (`R3-PRIV-001`, `R3-NET-002/003`, `R3-MOUNT-006`). V3 проверяет Windows roots и object custody.
5. **Telegram/privacy:** допустимые fields, offset semantics, PII TTL и deletion semantics принадлежат Telegram/secrets domains (`R5-F04..15`, `R6-P1-004/005`). V3 реализует storage mapping/caps только после их freeze.
6. **Candidate/evidence:** trusted collector, candidate/runner digests и canonical evidence envelope принадлежат B2r/O5/evidence domain (`R8-P1-003/010`). V3 предоставляет resource/path records.
7. **Dirty worktree:** repo/Vault no-write and touchset governance принадлежат repo domain (`R9-F01..10`). V3 runtime считает оба roots запрещёнными.
8. **Operability/emergency:** глобальная JSON schema/RC mapping, owner CLI и emergency stop принадлежат operability domain (`R10-F02/06/08/11`). V3 выдаёт стабильные resource/backup substates.

Если cross-domain contract не frozen или расходится с V3 data map, следующий mutation получает `V3_BLOCKED_UNKNOWN/DRIFT`, а не локальное предположение.

## 17. Порядок реализации и Definition of Done V3

Последовательно:

1. Свести cross-domain logical IDs/RC/CLI schema без runtime action.
2. Выполнить read-only Windows storage/resource/effective-principal inventory.
3. Получить `MG-V3-ROOTS`, `MG-V3-TRUST-BOUNDARY`, `MG-V3-RESOURCE-THRESHOLDS` и при необходимости at-rest exception.
4. Только после install gate создать roots с protected DACL и локальный inventory; до secret values провести canary tests.
5. Квалифицировать Docker managed VHDX, measured peak и Compose limits на synthetic data.
6. Проверить data map, retention и cleanup preview без удаления.
7. После secret/Telegram gates провести backup/fault/isolated restore tests.
8. Владелец по runbook читает status, понимает cap/stale/restore tiers и выполняет отдельный cleanup preview без подсказок агента.

V3 готов только если:

- все `DM-V3-*` имеют observed disposition и authority;
- roots/volumes/ACL/effective principals/at-rest policy имеют evidence;
- operation peak fixtures доказали zero-mutation below threshold;
- runtime CPU/RAM/log limits подтверждены inspect;
- backup `COMPLETE` и отдельный `RESTORE_VERIFIED` связаны exact generation, keys IDs и source-inaccessibility;
- cleanup canaries доказали zero foreign deletes;
- все owned findings из §15 имеют PASS либо явно owner-accepted residual risk, разрешённый самим contract;
- ни один `BLOCKED/UNKNOWN/FAIL` не переименован в PASS.

## 18. Разрешение конфликтов v1

| v1 формулировка | Решение v2 V3 |
|---|---|
| Не менее `25 GiB` свободно до установки | Заменено на per-volume `F >= R + G + M`; для первого install `G=max(10 GiB,4×installer)`, reserve остаётся непотребляемым. |
| Persistent Docker laboratory storage soft cap `20 GiB` | Не safety reserve. Превращается в owner-approved hard lab cap после measurement; операции также обязаны сохранить host reserve. |
| Backup quota `5 GiB` | Отменена как неподтверждённая. Cap должен вмещать минимум две крупнейшие verified generations + margin и утверждается владельцем. |
| Host RAM reserve `4 GiB` | Усилено до `max(4 GiB,25% installed RAM)` и отдельно проверяется Windows commit. |
| Containers ориентир `3 GiB`, `2–4 vCPU` | Заменено exact per-service hard limits и profile sum; CPU budget зависит от 50% logical CPUs, максимум 4. |
| PostgreSQL `512–768 MiB`, n8n `1–1.5 GiB`, mocks/bridge `≤256 MiB` | Верхние границы превращены в enforceable limits: PostgreSQL 768 MiB, n8n 1536 MiB, bridge 256 MiB, mocks 128/256 MiB; inspect обязателен. |
| Backup сначала dump/archive, потом «если содержит data — зашифровать» | Отменено. Backup всегда sensitive; encryption/authentication streaming до persistent storage, plaintext stage = 0. |
| Restore в новом project | Недостаточно. Добавлены unique nonce, zero-collision, source/live-secret inaccessible, exact labels, path safety, peak budget и recovery tiers. |
| Cleanup по run labels | Недостаточно. Добавлены full label tuple + object IDs/creation facts + immutable preview + manual apply; prune запрещён. |

Эти значения — design defaults и gates, а не сведения о текущем host. Любая будущая корректировка после measurements создаёт новый versioned decision; v1 не переписывается.
