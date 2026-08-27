---
id: "review-n8nagents-docker-desktop-plan-v1-quorum-20260827"
тип: "ревью"
статус: "выполнено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
доказательства:
  - "00_REVIEW_RECORDS_MANIFEST.json"
теги: ["review", "quorum", "docker-desktop", "plan-a", "stop"]
---

# Итог кворума десяти ревью плана Docker Desktop — N8NAgents v1

## Итог

**Кворумный результат: `STOP / PLAN_V1_NOT_APPROVABLE`.**

План v1 нельзя использовать как разрешение на установку или исполнение. Причины независимы друг от друга:

- `GO`: `0/10`, тогда как порог равен минимум `8/10`;
- `STOP`: `1`, тогда как допустимо `0`;
- подтверждённый `P0`: `1`, тогда как допустимо `0`;
- имеются consensus-P1, тогда как допустимо `0`.

Результат не изменяет frozen plan v1, не создаёт plan v2 и не разрешает загрузку, установку, Docker/Windows/VPS/Telegram/DeepSeek-действия. Рекомендуемое решение владельца — подготовить новую полную версию плана, сохранив v1 как неизменяемый вход ревью.

## Канонические идентификаторы

| Объект | Значение |
|---|---|
| План | `07_FULL_PLAN.md`, `46234` байта |
| SHA-256 плана | `a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79` |
| Bundle aggregate | `ac97cdacc140c7bcb186672aa63d002acc1658c767775a3d0718b406f17728e2` |
| Manifest SHA-256 | `7fbec135d522a5a79a50f7568c5d53a371f2c1b17b26664f3652e67e09f320d5` |
| Schema | `09_REVIEW_SCHEMA.json`, SHA-256 `de8935d9e2fe990bc41c70fdfb1dcc946b13942ee81064d028753a583b7c7b26` |
| Frozen bundle | `ReviewBundle_a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79` |

Повторная read-only проверка до сведения дала: все `11` bundle-файлов совпадают с manifest; canonical aggregate record имеет `1063` байта и ожидаемый SHA-256; canonical plan и bundle copy byte-identical.

## Валидация десяти записей

Каждый raw JSON сохранён рядом с этим отчётом. Все десять записей:

- валидны по `09_REVIEW_SCHEMA.json`;
- привязаны к одному plan hash/size и bundle hash;
- имеют уникальные `review_id` и `finding_id`;
- имеют `started_utc <= completed_utc`;
- имеют UTF-8 без BOM, только LF и ровно один финальный LF;
- не содержат намеренно сохранённых raw secrets, адреса VPS или raw allowlist IDs.

| Reviewer | Вердикт | Findings | P0 | P1 | P2 | P3 | Raw SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| R1 Windows/WSL | STOP | 12 | 1 | 7 | 3 | 1 | `df9c80bc7eb5067f0c293f1373221722ef64e983d520fa9c2ce5999f05449571` |
| R2 Supply chain/license | CHANGES_REQUIRED | 12 | 0 | 7 | 5 | 0 | `6e1956b5506f80cd0e803474556804d98023f569c96c60fac974f09e6cf4f397` |
| R3 Isolation/network/privileged | CHANGES_REQUIRED | 8 | 0 | 6 | 2 | 0 | `6406e4e72c6b09f677dc444ecad75f54caba4aae0bf2ea5785fc559f77e0d6ee` |
| R4 Compose+n8n+PostgreSQL | CHANGES_REQUIRED | 10 | 0 | 5 | 4 | 1 | `0742637f353d0faa830fa7d36e76322a3eeabff32d50cb0c00cf7bec37f4060b` |
| R5 Telegram | CHANGES_REQUIRED | 16 | 0 | 13 | 3 | 0 | `cb994f31ad9b93d4c5be24760bb8be6f489178047e46160d30b339a770269c6d` |
| R6 Secrets/PII/logs | CHANGES_REQUIRED | 11 | 0 | 10 | 1 | 0 | `622d437cf758c43690f7390dc48484762c27166a319189bd797b90c4d4fc217d` |
| R7 Persistence/backup | CHANGES_REQUIRED | 12 | 0 | 11 | 1 | 0 | `888d23387d76aa3e44d6f30fb88cd76fa1819614eeae5e6ed02c1754ce2d11e1` |
| R8 B2r/O5/evidence | CHANGES_REQUIRED | 12 | 0 | 10 | 2 | 0 | `3a67acc0a50b798bde557225898e4edb8566081528428a61a9844d7509b47a70` |
| R9 Dirty tree/touchset/rollback | CHANGES_REQUIRED | 10 | 0 | 8 | 2 | 0 | `b803a6e096e70cc807e417b7d679364b7e178c7c950958877694dc953cf7e234` |
| R10 Operability/resources/recovery | CHANGES_REQUIRED | 11 | 0 | 6 | 5 | 0 | `ce11263b855c4c0d40b6a6e14634b0cac5a720042fcb1cc231afe08996071373` |
| **Итого** | **0 GO / 9 CHANGES_REQUIRED / 1 STOP** | **114** | **1** | **83** | **28** | **2** | — |

`blocking=true`: `84`; `blocking=false`: `30`.

## Consensus blockers

Consensus ниже основан только на совпадении минимум двух независимых релевантных reviewers. Live internet и новые внешние источники при сведении не использовались; поэтому одиночный P1 не повышался до consensus по неподтверждённой ссылке.

| Кластер | Уровень | Независимые подтверждения | Общая критика и обязательное направление исправления |
|---|---|---|---|
| C01 Local Docker endpoint/control plane | P0 + P1 | R1, R3, R6 | Любая mutation может уйти в stale/remote Docker context или быть доступна более широкой Windows control-plane boundary. Каждая команда должна fail closed привязываться к локальному Docker Desktop endpoint, отклонять overrides/drift и доказывать субъектов доступа. |
| C03 Disk/resource enforcement | P1 | R1, R10 | `25 GiB` против `20 GiB + 5 GiB` не оставляет host/peak reserve; soft caps не исполнимы. Нужны budget equation, hard reserve, pre-growth checks, log/execution/backup retention и безопасный cleanup preview. |
| C04 Storage roots/at-rest remnants | P1 | R1, R6 | Не квалифицированы managed VHDX, Windows roots, staging, ACL/reparse/sync/drive/protection и pagefile/crash/support remnants. Нужна полная data map и fail-closed root qualification. |
| C06 Update/drift/migration/rollback | P1 | R2, R4, R7, R10 | Постоянная лаборатория не имеет детерминированного drift gate, migration-safe update и проверенного recovery; простой возврат к старому image опасен после schema/DB upgrade. |
| C07 Mount/write containment | P1 | R3, R9 | Allowlist mounts и защита Windows host writes не закрывают junction/reparse/symlink/hardlink/case/ADS/TOCTOU. Нужен exact canonical target policy и runtime sentinel/negative matrix. |
| C08 Network isolation and destinations | P1 | R3, R5, R6, R8 | Mock/gate no-egress и real-dev destination restriction остаются намерением. Нужны runtime-observed negative/positive matrices, отсутствие hidden proxies/routes и техническая destination allowlist для secret-bearing процессов. |
| C10 Telegram arming/dev identity/caps | P1 | R5, R10 | Нет TTL-bound fail-closed arming, доказуемой dev-bot identity и атомарных общих message/cost ceilings. `real-dev` должен отказываться до любого API-вызова без актуального owner arm record. |
| C12 Telegram authorization/envelope/routing | P1 | R5, R6 | Не определены conjunctive allowlist tuple, Update classification, authenticated anti-replay envelope, pre-storage rejection и единая trusted routing policy. |
| C14 Backup key/encryption/cold restore | P1 | R6, R7, R10 | Backup/key pair, authenticated encryption, plaintext staging и независимый cold restore не доказаны. Drill в том же failure domain с live secret root может дать ложный PASS. |
| C15 Emergency stop/revocation | P1 | R6, R10 | Нет единой fail-closed emergency procedure, atomic disarm, bounded stop verification, revoke/rotate protocol и escalation при недоступном Engine. |
| C17 Candidate/evidence chain of custody | P1 | R8, R9 | Exact candidate/runner/commit/package и dirty snapshot не связаны content-addressed identity; host-side TOCTOU и неполная write/evidence custody допускают ложный gate PASS. |

Любой один из этих кластеров блокирует GO. C01 дополнительно содержит подтверждённый P0 и сам по себе завершает кворум со `STOP`.

## Одиночные или спорные блокеры

Они не замалчиваются и не объявляются consensus-P1. Для plan v2 каждый должен быть либо исправлен, либо отклонён владельцем с конкретным evidence и residual-risk decision.

| Группа | Reviewer/IDs | Суть |
|---|---|---|
| S01 Windows eligibility/install transaction | R1 `WIN-002..006` | Нет исполнимого support predicate, exact change/resume state machine, разделения daily owner/UAC identity, безопасной ветки existing install и доказанного rollback. |
| S02 Supply-chain executable lock | R2 `001..005`, `007` | Нет exact execution lock до download, однозначного trust root/TOCTOU-safe verification, OCI leaf identity, hermetic build contract и полного license gate. |
| S03 Privileged blast radius | R3 `PRIV-001` | Unspecified privileged one-shot container делит Docker Desktop backend с постоянной лабораторией без достаточно узкой blast-radius boundary. |
| S04 Loopback acceptance | R3 `PORT-004` | Недостаточно runtime-проверок Windows/Docker IPv4/IPv6 forwarding для доказательства loopback-only n8n. |
| S05 Compose/service/data lifecycle | R4 `F01..F04` | Нет deterministic mode convergence, health/migration graph, PostgreSQL authority model и exact n8n DB/key/ownership/process contract. |
| S06 Telegram polling/idempotency | R5 `F02,F03,F05,F06,F07,F12` | Не заданы webhook transaction, poller exclusivity, highest-contiguous offset, durable acceptance/outbox и error-class state machine. |
| S07 Secret injection/PII/redaction | R6 `P1-002,P1-005,P1-006` | Не определены per-secret exposure channels, exact execution-data retention и fail-closed redaction/sink contract. |
| S08 Backup unit/atomicity/target/faults | R7 `F01,F02,F03,F06,F08,F12` | Нет единого backup epoch, полного recoverable set, cluster-scope dump, atomic publish, target identity и corruption/fault matrix. |
| S09 B2r/O5 executable truth | R8 `P1-001,P1-002,P1-004..007,P1-009` | Не hash-bound наборы `66/34/8`, независимость validators, clean-run protocol, proving canaries, state/attempt namespaces и exact execution fingerprint. |
| S10 Dirty worktree governance | R9 `F02,F04,F06,F07` | Touchset открыт; нет race-safe ownership, index/staging provenance и rollback частичной записи в dirty tree. |
| S11 Owner black-box handoff | R10 `F06` | Happy-path повторение не доказывает самостоятельные start/status/fault/emergency/backup/cold-restore действия владельца из чистой сессии. |

Некоторые элементы этих групп поддержаны P2/P3 других reviewers; это усиливает необходимость исправления, но не меняет строгую классификацию consensus.

## Неблокирующие улучшения

Все `28 P2` получают disposition `MITIGATE_V2`, а оба `P3` — `ACCEPT_CLARITY_TEST`. Основные темы:

- update inventory, last-known-good artifacts, SBOM/vulnerability/license/source evidence;
- cleanup/object custody и exclusive profile transitions;
- bridge offset backup, idempotent onboarding, image/project naming;
- dry-run без side effects, privacy retention и безопасная manual Telegram ceremony;
- secret entry hygiene и screenshot/support-bundle protocol;
- RPO/RTO, tool BOM и cleanup label schema;
- line endings, executable bits, `.gitattributes`, pre-secret `.gitignore`;
- owner 2FA recovery, stable `status/doctor`, reboot resume и daily runbook;
- immediate pre-bind port revalidation и actionable diagnostic states.

Это не разрешение автоматически расширять scope: v2 должен явно выбрать, какие меры входят до install/start, а какие являются post-foundation hardening без ослабления consensus blockers.

## Влияние на выбор владельца

Варианты решения без исполнения:

1. **Рекомендуется: создать полный plan v2.** Исправить все 11 consensus blocker clusters; дать explicit disposition каждому single P1 и каждому P2/P3; повторно заморозить новый plan/bundle и провести новое независимое ревью.
2. **Остановить plan A.** Сохранить v1, raw reviews и этот отчёт как evidence отказа; никаких локальных или VPS-действий.
3. **Сузить будущий plan v2.** Отделить read-only Windows discovery от install/runtime, но это должно быть новым планом и новым решением владельца. Текущий отчёт сам ничего не разрешает.

Варианта «исполнять v1 как есть» в рамках утверждённой quorum policy нет: это нарушит сразу четыре условия GO.

## Полная карта finding-ID → cluster → disposition

Disposition:

- `BLOCK_P0`: validated P0; безусловный STOP.
- `BLOCK_CONSENSUS_P1`: P1 входит в кластер с минимум двумя независимыми релевантными подтверждениями.
- `PRESENT_SINGLE_P1`: P1 остаётся отдельным/спорным и требует явного решения, не замалчивается.
- `MITIGATE_V2`: P2 принимается как мера качества/эксплуатации для проектирования v2.
- `ACCEPT_CLARITY_TEST`: P3 принимается как улучшение ясности/проверяемости.

### R1

| Finding | Cluster | Disposition |
|---|---|---|
| `R1-WIN-001` | C01 endpoint/control plane | `BLOCK_P0` |
| `R1-WIN-002`, `R1-WIN-003`, `R1-WIN-004`, `R1-WIN-005`, `R1-WIN-006` | C02 Windows qualification/install transaction | `PRESENT_SINGLE_P1` |
| `R1-WIN-007` | C03 resource enforcement | `BLOCK_CONSENSUS_P1` |
| `R1-WIN-008` | C04 storage roots/at-rest | `BLOCK_CONSENSUS_P1` |
| `R1-WIN-009` | C06 drift/update | `MITIGATE_V2` |
| `R1-WIN-010`, `R1-WIN-011` | C02 Windows policy/operator safety | `MITIGATE_V2` |
| `R1-WIN-012` | C08 exposure | `ACCEPT_CLARITY_TEST` |

### R2

| Finding | Cluster | Disposition |
|---|---|---|
| `R2-001`, `R2-002`, `R2-003`, `R2-004`, `R2-005`, `R2-007` | C05 supply chain/license | `PRESENT_SINGLE_P1` |
| `R2-006` | C06 drift/update/migration | `BLOCK_CONSENSUS_P1` |
| `R2-008`, `R2-011`, `R2-012` | C05 SBOM/installed identity/source evidence | `MITIGATE_V2` |
| `R2-009` | C06 last-known-good rollback set | `MITIGATE_V2` |
| `R2-010` | C09 n8n runtime extensions | `MITIGATE_V2` |

### R3

| Finding | Cluster | Disposition |
|---|---|---|
| `R3-PRIV-001` | C07 privileged blast radius | `PRESENT_SINGLE_P1` |
| `R3-NET-002`, `R3-NET-003` | C08 network isolation/destinations | `BLOCK_CONSENSUS_P1` |
| `R3-PORT-004` | C08 loopback exposure | `PRESENT_SINGLE_P1` |
| `R3-CTRL-005` | C01 endpoint/control plane | `BLOCK_CONSENSUS_P1` |
| `R3-MOUNT-006` | C07 mount/write containment | `BLOCK_CONSENSUS_P1` |
| `R3-CLEAN-007` | C18 cleanup custody | `MITIGATE_V2` |
| `R3-PROFILE-008` | C09 mode convergence | `MITIGATE_V2` |

### R4

| Finding | Cluster | Disposition |
|---|---|---|
| `R4-F01`, `R4-F02`, `R4-F03`, `R4-F04` | C09 Compose/service/data lifecycle | `PRESENT_SINGLE_P1` |
| `R4-F05` | C06 update/migration | `BLOCK_CONSENSUS_P1` |
| `R4-F06` | C14 backup boundary | `MITIGATE_V2` |
| `R4-F07`, `R4-F09` | C09 lifecycle/project ownership | `MITIGATE_V2` |
| `R4-F08` | C05 OCI/image identity | `MITIGATE_V2` |
| `R4-F10` | C19 diagnostics | `ACCEPT_CLARITY_TEST` |

### R5

| Finding | Cluster | Disposition |
|---|---|---|
| `R5-F01`, `R5-F11`, `R5-F13` | C10 Telegram arming/identity/caps | `BLOCK_CONSENSUS_P1` |
| `R5-F02`, `R5-F03`, `R5-F05`, `R5-F06`, `R5-F07`, `R5-F12` | C11 Telegram polling/idempotency/errors | `PRESENT_SINGLE_P1` |
| `R5-F04`, `R5-F08`, `R5-F09`, `R5-F10` | C12 Telegram auth/envelope/routing | `BLOCK_CONSENSUS_P1` |
| `R5-F14` | C09 mode/dry-run convergence | `MITIGATE_V2` |
| `R5-F15` | C13 PII/retention | `MITIGATE_V2` |
| `R5-F16` | C10 owner Telegram ceremony | `MITIGATE_V2` |

### R6

| Finding | Cluster | Disposition |
|---|---|---|
| `R6-P1-001` | C01 control-plane boundary | `BLOCK_CONSENSUS_P1` |
| `R6-P1-002`, `R6-P1-005`, `R6-P1-006` | C13 secret transport/PII/redaction | `PRESENT_SINGLE_P1` |
| `R6-P1-003`, `R6-P1-008` | C14 key/encryption/plaintext staging | `BLOCK_CONSENSUS_P1` |
| `R6-P1-004` | C12 pre-storage Telegram rejection | `BLOCK_CONSENSUS_P1` |
| `R6-P1-007` | C04 at-rest remnants | `BLOCK_CONSENSUS_P1` |
| `R6-P1-009` | C15 incident/revocation | `BLOCK_CONSENSUS_P1` |
| `R6-P1-010` | C08 destination allowlisting | `BLOCK_CONSENSUS_P1` |
| `R6-P2-011` | C13 manual secret entry hygiene | `MITIGATE_V2` |

### R7

| Finding | Cluster | Disposition |
|---|---|---|
| `R7-F01`, `R7-F02`, `R7-F03`, `R7-F06`, `R7-F08`, `R7-F12` | C14 backup scope/atomicity/target/faults | `PRESENT_SINGLE_P1` |
| `R7-F04`, `R7-F05`, `R7-F07`, `R7-F10` | C14 key/encryption/isolated cold restore | `BLOCK_CONSENSUS_P1` |
| `R7-F09` | C06 update/migration recovery | `BLOCK_CONSENSUS_P1` |
| `R7-F11` | C14 RPO/RTO | `MITIGATE_V2` |

### R8

| Finding | Cluster | Disposition |
|---|---|---|
| `R8-P1-001`, `R8-P1-002`, `R8-P1-004`, `R8-P1-005`, `R8-P1-006`, `R8-P1-007`, `R8-P1-009` | C16 B2r/O5 executable truth | `PRESENT_SINGLE_P1` |
| `R8-P1-003`, `R8-P1-010` | C17 candidate/evidence custody | `BLOCK_CONSENSUS_P1` |
| `R8-P1-008` | C08 no-network evidence | `BLOCK_CONSENSUS_P1` |
| `R8-P2-011` | C16 tool BOM/availability | `MITIGATE_V2` |
| `R8-P2-012` | C18 cleanup labels | `MITIGATE_V2` |

### R9

| Finding | Cluster | Disposition |
|---|---|---|
| `R9-F01`, `R9-F05`, `R9-F08` | C17 candidate/evidence custody | `BLOCK_CONSENSUS_P1` |
| `R9-F03` | C07 Windows mount/write containment | `BLOCK_CONSENSUS_P1` |
| `R9-F02`, `R9-F04`, `R9-F06`, `R9-F07` | C17 dirty tree governance | `PRESENT_SINGLE_P1` |
| `R9-F09` | C17 line endings/mode/attributes | `MITIGATE_V2` |
| `R9-F10` | C13 pre-secret safeguards | `MITIGATE_V2` |

### R10

| Finding | Cluster | Disposition |
|---|---|---|
| `R10-F01` | C10 Telegram arming | `BLOCK_CONSENSUS_P1` |
| `R10-F02` | C15 emergency stop | `BLOCK_CONSENSUS_P1` |
| `R10-F03` | C14 independent cold restore | `BLOCK_CONSENSUS_P1` |
| `R10-F04` | C03 resource enforcement | `BLOCK_CONSENSUS_P1` |
| `R10-F05` | C06 update/drift | `BLOCK_CONSENSUS_P1` |
| `R10-F06` | C19 black-box handoff | `PRESENT_SINGLE_P1` |
| `R10-F07`, `R10-F08`, `R10-F11` | C19 onboarding/diagnostics/daily operations | `MITIGATE_V2` |
| `R10-F09` | C02 owner change/reboot ceremony | `MITIGATE_V2` |
| `R10-F10` | C13 screenshot/support-bundle safety | `MITIGATE_V2` |

## Доказательства и ограничения сведения

Есть:

- exact raw records `R01.json`…`R10.json` и их manifest;
- schema/identity/uniqueness/encoding validation;
- повторная проверка frozen plan/bundle hashes;
- полная карта всех `114` finding IDs;
- неизменённый project baseline: HEAD `11974a33fa78bb72598059671cef9465402ab091`, `12M + 9U`, index `0` на момент сведения.

Отсутствует:

- plan v2;
- решение владельца по критике;
- post-review authorization на read-only preflight, download, install или runtime;
- live authoritative source refresh на момент будущего исполнения;
- любые новые Windows/Docker/VPS/Telegram/DeepSeek evidence.

Риск: принятие только части consensus clusters оставит v2 непригодным для GO. Уверенность в арифметике, schema binding и кворумном STOP — высокая; уверенность в окончательном дизайне исправлений не оценивается, потому что plan v2 в этом этапе запрещён.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
