---
id: "plan-n8nagents-docker-desktop-lab-v1-20260827"
тип: "задача"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Задача_Развертывание_N8NAgents]]"
  - "[[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]"
доказательства: []
теги: ["n8n", "docker-desktop", "локальная-лаборатория", "план", "telegram", "на-ревью"]
---

# Полный план локальной лаборатории Docker Desktop для N8NAgents — v1

## 0. Статус документа и запрет на преждевременное исполнение

Это **проект плана для критического независимого ревью**, а не разрешение на установку или выполнение.

- Выбран только **план A: Docker Desktop на текущем Windows-компьютере**.
- Отдельная Ubuntu в WSL, план B, Hyper-V VM, Windows Sandbox, v86/QEMU и тестирование на production VPS **не входят**.
- Docker Desktop вправе использовать собственный штатный WSL 2 backend. Это часть плана A и не означает установку отдельной пользовательской Ubuntu.
- До завершения десяти независимых ревью, сведения критики по кворуму и нового решения владельца запрещены: загрузки, установка Docker Desktop, включение Windows-компонентов, reboot, изменение проекта, запуск контейнеров, использование секретов, обращения к Telegram/DeepSeek, SSH/VPS/provider/DNS и любые расходы.
- Этот документ после заморозки не исправляется задним числом. Если критика принята, создаётся `v2`, а `v1` остаётся evidence входа ревью.

Статус этапов на момент заморозки:

| Этап | Статус |
|---|---|
| Полный план v1 | `FROZEN_FOR_REVIEW` после фиксации hash |
| Десять независимых ревью | `PENDING` |
| Кворум и общая критика владельцу | `PENDING` |
| Решение принять/переделать план | `MANUAL-GATE` |
| Реальные локальные изменения | `PROHIBITED` до нового решения |

## 1. Исходная задача и целевой результат

Владелец выбрал Docker Desktop как единственную локальную платформу и запретил автоматически переходить к плану B. Локальная среда должна быть постоянной, пригодной для повторных тестов агентом и владельцем вручную.

Итог, который должен дать утверждённый и исполненный план:

1. На Windows работает поддерживаемый Docker Desktop с Linux containers и WSL 2 backend.
2. Локально запускаются реальные PostgreSQL и n8n в закреплённых Docker-образах `linux/amd64`.
3. n8n editor доступен владельцу только через loopback Windows.
4. Локально можно запустить реального отдельного Telegram dev/test bot без публичного webhook: входящие updates получает ограниченный long-polling bridge.
5. Есть два явно различимых режима: `mock` без внешнего трафика и `real-dev` с ограниченным Telegram/DeepSeek-трафиком.
6. Агент и владелец используют одинаковые versioned PowerShell-команды `start`, `stop`, `status`, `logs`, `verify`, `backup`, `restore-drill`.
7. Постоянные данные и кэш сохраняются между задачами; одноразовые test containers удаляются после каждого прогона.
8. Текущий dirty draft проекта защищён от случайного изменения, packaging и commit до прохождения уже существующих gates.
9. Linux-only B2r/O5 проверки могут выполняться локально в Docker с доказанными capability и containment; недоступная capability даёт `BLOCKED`, а не ложный `PASS`.
10. Production VPS не меняется и не используется для локального плана.

## 2. Непереговорные ограничения

### 2.1. Входит

- Read-only preflight Windows и лицензии.
- После отдельного post-review approval: официальная загрузка и установка Docker Desktop.
- Только необходимые для Docker Desktop штатные компоненты WSL 2 / Virtual Machine Platform, если preflight покажет их отсутствие.
- Постоянная Docker-лаборатория N8NAgents.
- Реальные локальные PostgreSQL, n8n и отдельный Telegram dev/test bot.
- Локальный long-polling bridge для Telegram Bot API.
- Mock Telegram и mock LLM/DeepSeek endpoints без внешнего трафика.
- Docker-only Linux gates, static/runtime/integration tests, evidence, backup и isolated restore drill.
- Понятный ручной runbook для владельца.

### 2.2. Не входит

- Отдельный пользовательский Linux-дистрибутив WSL.
- План B или автоматический fallback на него.
- Hyper-V VM, Windows Sandbox, v86/QEMU, dual boot.
- Kubernetes, Docker Swarm, Windows containers.
- Production Caddy/TLS, публичные порты, DNS и provider UI.
- Использование production Telegram bot token для локальной разработки.
- Автоматическое создание Telegram bot через BotFather.
- Production VPS, SSH, firewall, server volumes или remote deployment.
- Автоматическое удаление Docker volumes, production данных, пользовательских файлов или общей Docker data root.
- Секреты в Git, Vault, чате, screenshots, command line, process list или review bundle.

### 2.3. Правило «никакого скрытого fallback»

Если Docker Desktop не обеспечивает обязательную capability, этап получает `BLOCKED-CAPABILITY`. Исполнитель не устанавливает отдельную Ubuntu/VM и не переносит тест на VPS. Он предъявляет evidence и предлагает владельцу только варианты внутри Docker Desktop либо новый план на отдельное решение.

## 3. Источники истины и фиксация baseline

Приоритет:

1. Exact Git tree/commit, тесты, Compose config, migrations, workflow exports и исполняемые scripts.
2. Immutable evidence с SHA-256, environment inventory и command transcripts после redaction.
3. Утверждённые ADR/планы и Obsidian.
4. Чат.

Перед любым будущим исполнением фиксируются:

- canonical plan SHA-256 и byte size;
- review-bundle SHA-256;
- решение кворума;
- exact project HEAD и hash dirty touchset;
- Windows build/edition/architecture без серийных номеров и учётных данных;
- Docker Desktop installer version, URL, publisher signature и SHA-256;
- exact image tags, registry digests и `linux/amd64` platform;
- выбранные limits на диск, память, трафик и сообщения;
- отдельный authorization ID для реальных изменений.

## 4. Известный baseline без секретов

### 4.1. Локальный проект

- Репозиторий: ветка `codex/n8nagents-foundation`.
- HEAD: `11974a33fa78bb72598059671cef9465402ab091`.
- Worktree содержит ровно 21 ранее разрешённый draft path: 12 tracked modifications и 9 untracked paths; index пуст; outside allowlist `0` по последнему зафиксированному evidence.
- Candidate и новый commit отсутствуют; corrective attempt 1 не израсходован.
- Host-level parse/unit/package/YAML/migration/canary checks ранее прошли в заявленном объёме.
- Linux capability, B2r actual-runner matrix и O5 не прошли из-за отсутствия подходящей локальной Linux boundary.
- Проектный `.env` с секретами не читается и не создаётся на этапе планирования/ревью.

### 4.2. Windows host

Надёжно известно только, что работа идёт на Windows и Docker/WSL Linux runtime ранее не был доступен для gate. Версия/edition/build, активность аппаратной виртуализации, текущие optional features, RAM, свободный диск, App Control/антивирус, наличие старой установки Docker и лицензионная категория являются `UNKNOWN` до read-only preflight.

### 4.3. VPS — только redacted context, не цель действий

По последнему известному контексту:

- Ubuntu 26.04 `amd64`, 2 vCPU, около 1.6 GiB RAM, root disk около 39 GiB.
- Plaintext swap 2 GiB активирован ранее.
- Docker Engine 29.7.2 и Compose 5.5.0 установлены.
- Точные tags: n8n 2.36.7 и PostgreSQL 17.11-alpine3.24 для `linux/amd64`.
- Приложение не запущено: containers `0`, application volumes `0`, application networks/listeners `0`; Caddy отсутствует.
- `.env` существует с mode `0600`; содержимое не читалось и не должно читаться этим планом.
- G1 остаётся `NOT VERIFIED — USER-ACCEPTED-EXCEPTION`; remote K4 retry budget исчерпан.

Все адреса, fingerprints, токены, allowlist IDs и другие идентификаторы из review bundle исключаются.

## 5. Целевая локальная архитектура

```text
Windows browser / PowerShell
        │ 127.0.0.1 only
        ▼
Docker Desktop, Linux containers, WSL 2 backend
  ├─ n8nagents-local-postgres      [internal data network, no host port]
  ├─ n8nagents-local-n8n           [127.0.0.1:5678 only]
  ├─ n8nagents-local-telegram-bridge [real-dev profile, outbound HTTPS only]
  ├─ n8nagents-local-mock-telegram [mock profile, internal only]
  ├─ n8nagents-local-mock-llm      [mock profile, internal only]
  └─ one-shot qa containers        [--network none or internal-only]

Persistent named volumes
  ├─ local_postgres_data
  ├─ local_n8n_data
  ├─ local_n8n_files
  └─ local_evidence_cache

Windows user-only data root
  ├─ secrets/          [not Git/Vault, restricted ACL]
  ├─ inventory/        [no secrets]
  ├─ evidence/         [redacted]
  └─ backups/          [encrypted where credentials/data are included]
```

Production Compose и local Compose не должны делить project name, volumes, secrets, ports или state. Предлагаемые имена:

- production: `n8nagents`;
- local: `n8nagents-local`;
- disposable gate: `n8nagents-k4r-<run-id>`;
- isolated restore: `n8nagents-restore-<run-id>`.

## 6. Режимы лаборатории

### 6.1. `mock` — режим по умолчанию

- Реальные PostgreSQL и n8n.
- Mock Telegram и mock LLM endpoints внутри Docker internal network.
- Нет production credentials и Telegram token.
- Внешний egress должен быть технически запрещён и проверен, а не только обещан.
- n8n editor доступен только на `127.0.0.1`.
- Используется для schema, migrations, workflow import, authorization-order, idempotency, retries, memory isolation и UI smoke.

### 6.2. `real-dev` — только после manual secret/recipient gate

- Реальные PostgreSQL и n8n.
- Только отдельный dev/test Telegram bot.
- Входящие updates через long polling; публичного webhook и Caddy нет.
- Только явно указанные numeric user/chat IDs, хранящиеся локально вне Git/Vault.
- DeepSeek по умолчанию выключен; включается отдельным profile/flag после budget gate.
- Лимиты сообщений и расходов проверяются preflight и post-run counters.
- Любой новый recipient, тип данных, bot token или бюджет требует нового решения владельца.

### 6.3. `gate`

- Одноразовые Linux test containers.
- Входной candidate read-only.
- Output/evidence — отдельный writable volume.
- Для B2r/O5: `--network none`, если тесту не нужна межконтейнерная сеть.
- Привилегии выдаются только конкретному one-shot контейнеру после capability review; Docker socket не монтируется.
- Cleanup удаляет только run-labelled контейнеры/networks/volumes, но не persistent laboratory volumes.

## 7. Локальный Telegram long-polling bridge

### 7.1. Назначение

Telegram webhook требует публичного HTTPS endpoint. Для локального теста используется Telegram Bot API `getUpdates`, поэтому публичный inbound, tunnel и Caddy не нужны.

### 7.2. Контракт bridge

Bridge должен:

1. Стартовать только в profile `real-dev` и в единственном экземпляре.
2. Читать bot token только из user-only secret source; не принимать token как CLI argument.
3. Выполнить `getMe`, зафиксировать только redacted bot identity status и numeric hash, не raw username/ID в evidence.
4. Проверить, что используется dev/test bot. Production bot запрещён policy flag и ручным подтверждением.
5. Перед polling проверить состояние webhook. Изменение webhook разрешается только для dev bot; `deleteWebhook` не выполняется для неизвестного/production bot.
6. Вызывать `getUpdates` с bounded timeout, `allowed_updates` только для согласованных text messages и сохранённым offset.
7. Отправлять update во внутренний n8n ingress с отдельным bridge-auth secret.
8. Считать update принятым только после ожидаемого 2xx от n8n; offset продвигать на `update_id + 1`.
9. Допускать повторную доставку; дедупликация остаётся в n8n/PostgreSQL по `(bot_id, update_id)`.
10. Иметь exponential backoff с jitter, bounded retry и circuit-breaker на auth/rate-limit failures.
11. Не логировать token, headers, raw message text, user/chat IDs или полный Telegram response.
12. На SIGTERM завершать текущий long poll, сохранять offset атомарно и останавливаться без потери уже подтверждённого update.

### 7.3. Исходящие ответы

Предпочтительный compatibility path:

- входящие updates доставляет bridge;
- ответ отправляет n8n Telegram node с локальной n8n Credential;
- destination берётся только из trusted normalized input и allowlist.

Если точная версия n8n/Telegram node не проходит import/live gate, разрешён только документированный local adapter, который отправляет `sendMessage` через bridge по узкому internal contract. Это не переносится в production без отдельного ADR/review.

### 7.4. Важное ограничение Telegram

Один token не должен одновременно использовать webhook и `getUpdates`. Поэтому отдельный dev bot — обязательное условие `real-dev`. Отсутствие отдельного dev bot означает `BLOCKED-MANUAL`, а не использование production token.

## 8. Секреты, персональные данные и журналы

### 8.1. Классы секретов

- Telegram dev token.
- DeepSeek API key.
- `N8N_ENCRYPTION_KEY` локальной instance.
- PostgreSQL passwords.
- Bridge-auth secret.
- При необходимости ключ шифрования backup.

### 8.2. Хранение

- Secrets не входят в repository, Vault, review bundle, screenshots или transcripts.
- Локальный secret root находится вне проекта и Vault, с ACL только текущему Windows user и `SYSTEM`; inherited broad ACL удаляется после отдельной проверки exact path.
- Docker Desktop administrator и текущий Windows user считаются доверенной boundary: обладатель Docker control plane способен получить container secrets.
- Telegram и DeepSeek credentials создаются владельцем через local n8n UI или интерактивный stdin/file flow.
- Заполненный `.env` не читается агентом и не печатается. Для Compose используется отдельный local env path вне repository.
- Любая команда `docker inspect`, `compose config`, logs и support bundle проходит field-aware redaction; raw output с environment не сохраняется.

### 8.3. Логи и retention

- Application logs: metadata/status only, без message bodies, prompts, provider payloads и headers.
- n8n success/error execution persistence выключена либо минимизирована до доказанного безопасного набора.
- Evidence хранит hashes, counts, labels и redacted excerpts.
- Локальные test chat данные удаляются только отдельной явной командой владельца; автоматического destructive cleanup нет.

## 9. Сетевые границы

### 9.1. Host exposure

- Только `127.0.0.1:5678` для local n8n editor.
- PostgreSQL `5432` не публикуется.
- Bridge и mocks не имеют host ports, кроме отдельного loopback diagnostic port при review-approved необходимости.
- `0.0.0.0`, `[::]`, host networking и published Docker API запрещены.
- Caddy profile не запускается локально по умолчанию.

### 9.2. Container egress

- `mock`: internal networks, подтверждённый отказ DNS/HTTPS наружу.
- `real-dev`: egress только тем сервисам, которым нужны Telegram/DeepSeek; Postgres остаётся internal-only.
- `gate`: `--network none` или internal-only network по тестовому контракту.
- Docker socket, Windows named pipe Docker Engine и host filesystem root не монтируются в containers.

### 9.3. Проверки

- `docker compose config` после redaction.
- `docker ps` published bindings.
- `docker network inspect` без environment.
- Connect tests на loopback/LAN/IPv4/IPv6.
- Внешний egress canary для mock/gate должен завершиться ожидаемым отказом.
- Успех теста не выводится только из configuration intent; нужен runtime evidence.

## 10. Persistent data, backup и recovery

### 10.1. Что сохраняется

- Docker Desktop и его managed Linux data disk.
- Закреплённые image layers и build cache в пределах квоты.
- Named volumes PostgreSQL/n8n.
- Version/digest inventory и redacted evidence.
- Runbooks и scripts в Git после отдельного repo-write gate.

### 10.2. Что одноразовое

- B2r/O5 test containers.
- Restore drill project и его volumes.
- Temporary build contexts, unredacted transient logs и failure injection shims.
- Network namespaces/privileged mounts конкретного run.

### 10.3. Backup plan

1. Quiesce local writes или остановить n8n.
2. Сделать PostgreSQL logical dump через pinned image.
3. Снять согласованный archive n8n data volume.
4. Создать BOM с exact image digests, schema version, file hashes и timestamps.
5. Если backup содержит credentials/data, зашифровать до помещения в persistent backup root.
6. Хранить `N8N_ENCRYPTION_KEY` и backup decryption material отдельно.
7. Применить предложенную квоту и retention только после решения владельца.
8. Проверить restore в новом Compose project с новыми volumes, без Telegram/DeepSeek egress.

### 10.4. Recovery

- Docker Desktop не запускается: сохранить logs/redacted diagnostics, не factory-reset автоматически.
- Data disk повреждён: STOP; не удалять `%LOCALAPPDATA%`/WSL distributions автоматически.
- Контейнер unhealthy: остановить local project, сохранить volumes, вернуться к последнему pinned compose/image inventory.
- Workflow regression: импортировать secret-free export в isolated project; production metadata DB напрямую не редактировать.
- Любое действие `down -v`, prune, factory reset или unregister WSL — отдельный destructive gate.

## 11. Ресурсы и квоты

Точные thresholds утверждаются после preflight, но план предлагает:

- свободное место до установки: не менее 25 GiB;
- резерв host RAM: не менее 4 GiB после запуска лаборатории;
- суммарный рабочий лимит containers: ориентир 3 GiB RAM и 2–4 vCPU;
- PostgreSQL: 512–768 MiB;
- n8n: 1–1.5 GiB, `NODE_OPTIONS` bounded;
- mocks/bridge: до 256 MiB каждый;
- persistent Docker laboratory storage soft cap: 20 GiB;
- backup quota: 5 GiB до отдельного решения;
- не более одного B2r/O5 privileged run одновременно.

Если host не выдерживает thresholds, установка не начинается до нового решения. Автоматическое изменение pagefile, BIOS, power policy или security tooling запрещено.

## 12. Этапы исполнения после успешного ревью и отдельного approval

### D0. Заморозка плана и десять ревью — текущий этап

Действия:

- зафиксировать canonical plan и byte-identical `07_FULL_PLAN.md`;
- создать secret-free bundle и manifest;
- дать один frozen bundle десяти независимым reviewer roles;
- собрать structured findings;
- применить quorum policy без исправления v1.

Gate: владелец видит общую критику до решения.

DoD:

- plan hash и size совпадают во всех copies;
- bundle manifest проверен дважды;
- десять outputs привязаны к тем же plan/bundle hashes;
- нет исполнения и секретов.

### D1. Read-only Windows/Docker/licensing preflight

Проверить без изменения:

- Windows edition/build/architecture;
- virtualization capability и текущий статус, не меняя BIOS;
- состояние WSL/Virtual Machine Platform;
- наличие Docker Desktop/Engine/CLI и конфликтующих daemons;
- CPU/RAM/free disk;
- App Control/antivirus policy;
- текущие user groups и необходимость admin/UAC;
- Docker Desktop license eligibility/terms — решение владельца;
- доступность loopback port 5678;
- отсутствие unexpected `docker-desktop` data, которую можно перезаписать.

Stop: неизвестная существующая Docker data, недостаток ресурсов, неподдерживаемая Windows, license ambiguity, требование plan B или destructive migration.

### D2. Supply-chain lock и установка Docker Desktop

До download сформировать acquisition record:

- official source URL;
- exact version/build/channel;
- published checksum/signature source;
- expected Authenticode publisher;
- installer bytes cap;
- UTC timestamp.

После download до запуска:

- SHA-256 совпадает;
- Authenticode status valid и publisher exact-match;
- файл не переадресован на неофициальный origin;
- mismatch: STOP, удалить только downloaded installer, сохранить redacted evidence.

Установка:

- Linux containers и WSL 2 backend;
- не включать Kubernetes/Windows containers/experimental features;
- не создавать отдельную Ubuntu distro;
- если нужны штатные Windows features, показать exact change set и ожидаемый reboot; выполнить только в post-review authority;
- после reboot заново проверить Windows build, WSL backend и Docker context.

### D3. Docker capability and containment qualification

До работы с dirty repo:

- проверить `linux/amd64` containers;
- UID 0 внутри container без трактовки как Windows administrator;
- `--network none`, internal network и loopback publication;
- named volumes и bind mounts;
- read-only bind source;
- symlink/hardlink/mode/UID/GID behavior;
- private mount namespace;
- nested/same-device bind mounts;
- immutable flag (`chattr/lsattr`) на overlay и volume;
- signal delivery и cleanup;
- resource limits;
- отсутствие Docker socket/host root mounts;
- outside sentinel unchanged.

Capability не считается доказанной по версии/документации. Нужен disposable runtime test. Неподдерживаемый immutable/mount сценарий — `BLOCKED-CAPABILITY`; план B не запускается.

### D4. Создание local lab artifacts

Только после отдельного repo-write gate и сохранения 21-path custody:

- local Compose overrides/profiles;
- PowerShell CLI wrappers;
- mock services;
- minimal long-polling bridge;
- secret inventory template без значений;
- local backup/restore scripts;
- tests и operator runbook.

Любое изменение существующего dirty path требует ownership check и diff review. Предпочтение — новые изолированные local paths. Нельзя commit/package текущий draft до K4R acceptance.

### D5. Image supply-chain lock

- Pull только с официальных registries.
- Resolve exact registry digest для `linux/amd64`.
- Записать tag, digest, platform, size, source и UTC без registry credentials.
- Не использовать `latest` и mutable tag без digest.
- Proposed baseline: n8n `2.36.7`, PostgreSQL `17.11-alpine3.24`; окончательная совместимость проверяется по официальным источникам на дату исполнения.
- Bridge/mocks собираются из reviewed source с pinned base digest и dependency lock; либо dependency-free standard runtime.
- Secret scan, SBOM и vulnerability review являются gate; severity policy утверждается до GO.

### D6. Mock mode

Последовательно:

1. Создать local secrets только для DB/encryption, без внешних credentials.
2. Запустить PostgreSQL и migrations.
3. Запустить n8n на `127.0.0.1:5678`.
4. Владелец создаёт local owner и 2FA.
5. Запустить mock Telegram/LLM.
6. Импортировать exact-version workflow drafts/exports без credentials.
7. Проверить ingress auth, normalize, allowlist order, deduplication, memory isolation, tools и response splitting.
8. Проверить отсутствие внешнего egress и secret/log leakage.
9. Перезапустить Docker Desktop/project и доказать persistence.

### D7. Real Telegram dev/test mode

Manual prerequisites одним пакетом:

- отдельный dev/test bot;
- прямой secret input вне чата/Vault;
- allowlisted test user/chat;
- допустимый test data class;
- message ceiling;
- подтверждение, что webhook этого dev bot можно отключить;
- stop/rollback rule.

Затем:

1. Проверить mock mode green.
2. Запустить bridge single-replica.
3. Подтвердить long polling и offset persistence.
4. Проверить unauthorized update rejection до DB/LLM/tools, кроме минимальной dedup/auth telemetry.
5. Отправить bounded Telegram messages только в allowlisted test chat.
6. Проверить duplicate/retry/rate-limit/restart cases.
7. Остановить profile и проверить отсутствие background polling.

### D8. DeepSeek real spike

По умолчанию `BLOCKED-MANUAL` до secret/budget approval.

- API key только через local n8n Credential.
- Exact base URL/model проверяется по официальному API на дату исполнения.
- Сначала один deterministic request, затем native tool-calling spike с двумя последовательными tool calls.
- Проверить timeout, malformed response, reasoning/thinking compatibility и tool result.
- Budget meter до и после; hard ceiling не превышается.
- Failure приводит к documented fallback decision, а не к самодельному agent loop.

### D9. K4R B2r/O5 gates в Docker

- Сверить frozen authority, contract, candidate и 21-path custody.
- Входной repo bind read-only; Git object store не меняется.
- Выполнить Linux validator engines и exact fixtures.
- Выполнить B2r actual runner matrix, fault shims, TOCTOU, rollback/signals/cleanup и mount-boundary checks.
- Выполнить O5 в disposable container/volumes без NIC.
- Каждый result связан с image digest, kernel, Docker Desktop/Engine versions и command hash.
- Никакой skipped row/count-only PASS.
- После success — independent review exact candidate; только затем commit/package в отдельном gate.

### D10. Backup, isolated restore и пользовательский handover

- Создать зашифрованный local backup.
- Restore в новом project name/volumes без real egress.
- Проверить DB state, n8n start и credential decryptability поддерживаемым способом без decrypted export.
- Подготовить owner runbook: start/stop/status/logs/mock/real/backup/restore/update/emergency.
- Владелец своими руками повторяет start, UI login, mock message, real dev-bot message, stop и restart.
- Зафиксировать только redacted evidence.

### D11. Production readiness — за пределами этого плана

Локальный `PASS` не разрешает VPS execution. Для production нужен новый exact-commit remote gate, актуальный provider-console/DNS/firewall/IPv6/manual-secret state и отдельное deployment evidence.

## 13. Пользовательский CLI и runbook contract

Предусмотреть versioned команды без секретов в arguments:

```text
lab preflight
lab install-status
lab start --mode mock
lab start --mode real-dev
lab stop
lab status
lab logs --redacted
lab verify --scope static|runtime|telegram|all
lab backup
lab restore-drill <backup-id>
lab inventory
lab doctor
```

Требования:

- every command поддерживает `--dry-run`, где есть mutations;
- exact target/data root выводится до изменения;
- destructive команды отсутствуют в обычном CLI;
- nonzero exit на любом failed assertion;
- слова `PASS` в child stdout не заменяют exit/schema validation;
- logs redacted по полям, не regex-only;
- start идемпотентен; stop не удаляет volumes;
- owner может выполнить основной сценарий без ручного ввода длинных shell-команд.

## 14. Планируемый touchset после отдельного repo-write gate

Предпочтительные новые пути; окончательные имена подтверждает review:

```text
N8NAgents/local/
  compose.local.yaml
  compose.mock.yaml
  compose.real-dev.yaml
  README.md
  telegram-bridge/
  mocks/
N8NAgents/scripts/local/
  lab.ps1
  preflight.ps1
  verify-runtime.ps1
  backup-local.ps1
  restore-local.ps1
N8NAgents/docs/
  runbook-local-docker.md
  local-threat-model.md
  local-verification-matrix.md
```

Дополнительно допустимы точечные изменения `.gitignore`, `.env.example`, root README и CI/static scripts только после collision check. Существующие 21 dirty paths не изменяются без отдельного ownership review.

Windows/runtime touchset после approval:

- Docker Desktop application files.
- Docker-managed WSL backend/data disk и virtual network.
- User Docker config/context.
- User-only N8NAgents lab data root.
- При необходимости штатные WSL/Virtual Machine Platform features и один reboot.

Точные paths фиксируются read-only preflight и installer evidence; broad directory deletion запрещён.

## 15. Rollback по этапам

| Этап | Недеструктивный rollback |
|---|---|
| Download | удалить только hash-mismatched installer по exact path |
| Install before data | штатно остановить/uninstall Docker Desktop; WSL features не отключать автоматически |
| Lab config | revert только reviewed local commit/branch; чужой dirty worktree не трогать |
| Image pull/build | оставить cache либо удалить только exact labelled image после отдельного подтверждения |
| Runtime failure | `compose stop`; сохранить volumes/evidence |
| Telegram failure | остановить bridge/profile; revoke/rotate token выполняет владелец напрямую |
| DeepSeek failure | отключить real profile/credential; сохранить redacted counters |
| Backup failure | сохранить исходные volumes; failed backup quarantine, не удалять good copies |
| Restore failure | удалить только exact disposable restore project после проверки target labels |

Никогда автоматически не выполнять `docker system prune -a`, `compose down -v`, Docker factory reset, WSL unregister, recursive delete общей data root или очистку пользовательского профиля.

## 16. Gates и stop conditions

### Manual gates

- Принятие критики и утверждение plan version.
- Docker Desktop license eligibility/terms.
- Exact Windows feature changes/reboot, если нужны.
- Admin/UAC action.
- Все secrets и credential binding.
- Telegram bot creation, webhook state и allowlist.
- DeepSeek budget/real traffic.
- Destructive cleanup, factory reset, volume deletion.
- Любой переход за Docker-only план A.

### Автоматические stop conditions

- Bundle/plan hash mismatch.
- Неожиданно dirty Vault или repo outside allowlist.
- Installer checksum/signature/publisher mismatch.
- Unsupported Windows/virtualization/resource state.
- Existing Docker data с неизвестным владельцем или migration risk.
- Host port bind не loopback-only.
- PostgreSQL опубликован на host.
- Container получает Docker socket/host root.
- Mock/gate имеет внешний egress.
- Secret/PII найден в Git/Vault/log/evidence.
- Production bot token или неизвестный recipient.
- Capability test skipped, смоделирован или выдан за `PASS`.
- Test modifies source repo, Git object store или outside sentinel.
- Backup/restore integrity mismatch.
- Требуется plan B, VPS или scope expansion.

## 17. Verification matrix верхнего уровня

| Область | Обязательное доказательство |
|---|---|
| Windows preflight | redacted inventory, no-change attestation |
| Installer | URL, version, size, SHA-256, valid publisher signature |
| Docker | versions, context, `linux/amd64`, resource/config inventory |
| Exposure | loopback-only n8n, no 5432/public bridge, IPv4+IPv6 checks |
| Isolation | runtime no-egress evidence mock/gate; no socket/host-root mounts |
| Persistence | restart Docker/project, DB/n8n state survives |
| Supply chain | image digests/platform, SBOM/scan disposition |
| PostgreSQL | migrations, roles/grants, fault atomicity, persistence |
| n8n | owner/2FA manual pass, import/export roundtrip exact version |
| Telegram | dev bot, polling offsets, allowlist, dedup, bounded real messages |
| DeepSeek | budgeted compatibility spike or explicit blocked status |
| Secrets | file ACL, Git/Vault/log scans, redacted output |
| B2r/O5 | exact matrices, canaries, containment, candidate binding |
| Backup | encrypted artifact, BOM/hash, isolated restore |
| Operability | owner repeats runbook start/test/stop/restart |

## 18. Definition of Done

План A считается полностью реализованным только когда:

- десять независимых reviews сведены по утверждённому quorum и итоговый plan принят владельцем;
- Docker Desktop установлен из проверенного official artifact и работает с Linux `amd64` containers;
- отдельная Ubuntu/VM не установлена;
- local n8n/PostgreSQL запускаются одной documented командой, доступны безопасно и переживают restart;
- mock mode доказан без внешнего egress;
- отдельный real dev/test Telegram bot работает через long polling только с allowlist;
- владелец вручную повторил основной сценарий;
- DeepSeek real spike либо прошёл в утверждённом бюджете, либо честно отмечен `BLOCKED-MANUAL/FAIL` без ложного общего успеха;
- B2r/O5 прошли в Docker или получили точный `BLOCKED-CAPABILITY`; fallback B/VPS не выполнялся;
- secrets/PII отсутствуют в Git, Vault, evidence и logs;
- backup создан и восстановлен в изолированном project;
- текущий dirty draft не потерян, не смешан и не закоммичен преждевременно;
- CLI/runbooks позволяют агенту и владельцу воспроизводить действия;
- production VPS не изменён;
- residual risks и следующий exact remote gate документированы.

Общий `SUCCESS` запрещён, если real Telegram path, persistence, secret controls, backup/restore или owner handover не доказаны. Linux gates могут иметь отдельный `BLOCKED-CAPABILITY`, но это должно явно ограничивать готовность проекта.

## 19. Риски, которые обязаны атаковать reviewer

1. Реальные Windows/WSL changes и rollback Docker Desktop.
2. Лицензия, official source, подпись, hash и mutable supply chain.
3. Docker Desktop как security boundary; privilege/mount/network escape.
4. Достаточность ресурсов Windows и рост VHDX/cache.
5. Совместимость n8n 2.36.7/PostgreSQL 17.11 и local overrides.
6. Корректность long polling, webhook conflict, offset/crash window и rate limits.
7. Неутечка Telegram/DeepSeek/DB/encryption secrets и PII.
8. Реальная, а не декларативная network isolation mock/gate.
9. B2r/O5 capability на Docker overlay/WSL kernel и риск ложного `PASS`.
10. Dirty 21-path custody, package integrity, rollback и evidence binding.
11. Backup пары DB + n8n encryption key и restore без production egress.
12. Удобство ручного запуска владельцем и recovery при поломке Docker Desktop.

## 20. Кворум для решения после десяти ревью

- Любой подтверждённый `P0` блокирует исполнение.
- Совпадающий `P1` у минимум двух независимых релевантных reviewers либо `P1`, подтверждённый authoritative source, требует исправления до GO.
- Для принятия v1: минимум `8/10 GO`, `0 STOP`, `0 P0`, `0 consensus-P1`.
- `BLOCKED` из-за дефекта bundle требует исправить bundle и повторить все десять reviews на новой frozen версии.
- Один disputed `P1` не замалчивается: оркестратор даёт владельцу evidence и аргументированное disposition.
- Все `P2/P3` получают явный `accept`, `mitigate`, `defer` или `reject` с обоснованием.
- Reviewer outputs не редактируют frozen v1. После сведения кворума владелец решает: принять v1, создать v2 или остановить план.

## 21. Открытые вопросы до исполнения

- Точная Windows version/edition/build и активные optional features.
- Hardware virtualization и policy ограничения.
- RAM/free disk и приемлемая storage quota.
- Есть ли существующая Docker Desktop data, которую нельзя затронуть.
- Лицензионная категория владельца.
- Exact Docker Desktop version/build после проверки official current channel.
- Отдельный dev/test Telegram bot и допустимость `deleteWebhook` для него.
- Local test allowlist и data class без записи raw IDs в Vault.
- Применимость прежнего Telegram/DeepSeek budget к local real-dev; до подтверждения считать новым manual gate.
- Backup destination/retention и custody local encryption material.
- Поддержка обязательных mount/immutable capabilities Docker Desktop.

## 22. Следующее решение владельца

До десяти reviews — никаких действий. После кворума оркестратор показывает владельцу:

- общие P0/P1/P2/P3 findings;
- совпадения и расхождения reviewers;
- проверенное disposition каждой критики;
- влияние на безопасность, удобство, сроки и disk/resource budget;
- рекомендацию: принять v1, подготовить v2 или остановить.

Только затем владелец выдаёт или не выдаёт новый authorization на D1–D10.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
