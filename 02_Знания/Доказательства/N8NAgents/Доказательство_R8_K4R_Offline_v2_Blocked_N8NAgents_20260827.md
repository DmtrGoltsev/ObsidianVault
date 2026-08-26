---
id: "evidence-n8nagents-r8-k4r-offline-v2-blocked-20260827"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "Локальный B2r blocked evidence bundle, 2026-08-27"
  - "[[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
доказательства: []
теги: ["n8n", "k4r", "offline", "b2r", "blocked", "windows", "linux", "sandbox", "governance"]
---

# R8 — K4R-OFFLINE-v2: блокировка локальной Linux boundary

## Итоговый статус

Текущий K4R-OFFLINE-v2 gate: **`BLOCKED`**. Terminal label: `B2R_NETWORK_BOUNDARY`; exit code: `45`. Это произошло **до запуска валидатора**: `VALIDATOR_PROCESS_START_COUNT=0` и `VALIDATOR_PACKAGE_LOAD_COUNT=0`. Candidate не заморожен, commit не создан, corrective attempt 1 не израсходован.

Эта запись в Obsidian создана после B2r run и вне его контекста. Она не относится к измеренному запуску и не меняет его evidence: `REMOTE=0`, `VPS=0`, `VAULT=0`, `NETWORK=0`.

## Контекст K4R-OFFLINE-v2

- Quorum-v2 plan sealed; dirty draft содержит ровно `21` разрешённый allowlist path. Commit отсутствует.
- B2 semantic two-engine initial run дал `PASS`, затем три независимых reviewer дали `3/3 CHANGES_REQUIRED`.
- B2r contract и replay bundle подготовлены, но не стали evidence успешного Linux execution.
- Canonical Ajv `8.18` недоступен; после B2r corrections quorum принял связку Ajv `8.17` + SchemaSafe. Это не отменяет необходимость требуемой Linux boundary.

## Причина блокировки

Для no-NIC Linux sandbox отсутствуют hash-pinned boot/runtime inputs v86. Автоматический поиск boundary также не нашёл доступного исполнения: Windows Sandbox, Hyper-V, WSL, host-native Linux network namespace и локальный v86/QEMU runtime недоступны. Поэтому gate остановился fail-closed до валидатора; это не является `PASS`, `OFFLINE_READY`, VPS check или remote authority.

## Локальные evidence и привязки

Evidence root:

`C:\Users\style\AppData\Local\Temp\n8nagents-b2r-blocked-03f4a5d18ab74f379d5c44dd387b34e8`

| Артефакт | SHA-256 |
|---|---|
| `evidence.anchor.txt` | `5960d0ebce383bdf4b71f5f0a583d415e7b09a9303fe8ea4ad19ae72e8110a06` |
| `evidence/EVIDENCE_MANIFEST.tsv` | `3b56d0491f8c156c2e3c7e21e6b93e895b52757c4212b168d9f364a3a88a0d35` |
| `evidence/BLOCKED_REPORT.kv` | `0cce74079a1b6a8cd934dbf45f660216d7ccfac90dfa504a7e90f95813093992` |
| `replay-bundle/BUNDLE_MANIFEST.tsv` | `8b7c65ff1a67934db42765c64c6613eaf95920c9f134784ce6bd273aad51cd0c` |

`BLOCKED_REPORT.kv` дополнительно связывает baseline `11974a33fa78bb72598059671cef9465402ab091`, contract SHA-256 `c5e9f41798b8f0ff32ba464ea45986a2b829d389d428293f55a14a1acba4165a` и quorum SHA-256 `593531ed42a68621bd02da9bd9f02a844b5903c2b32ed649bcecb3eb7c2adc6f`.

## Не выполнено и не доказано

- Нет VPS, SSH, SCP, provider, firewall, DNS, Caddy, Docker, PostgreSQL, n8n, workflow или иных network actions.
- Linux validator, package load, actual-runner matrix, canaries, Linux capability/containment record и `OFFLINE_READY` не выполнены.
- Нет candidate commit, package, independent acceptance или authority для `K4R-REMOTE-1`.
- Не следует переустанавливать VPS OS: это не является средством закрытия локальной boundary.

## Ручной выбор владельца

Приоритетные варианты, требующие явного решения владельца:

1. Разрешить включение Windows Sandbox. Это системное/потенциально destructive изменение host feature и может потребовать reboot.
2. Разрешить локальную HTTPS-загрузку **только** exact hash-pinned Linux/v86 boot и runtime inputs, затем использовать no-NIC sandbox.

До выбора не пытаться обходить boundary, не начинать remote gate и не переустанавливать VPS OS.

## TOFU и границы

`[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]` остаётся **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`**. K4R-OFFLINE-v2 не подтверждает fingerprint, не использует SSH и не расширяет TOFU scope.

## Связанные заметки

- [[N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]]
- [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]
