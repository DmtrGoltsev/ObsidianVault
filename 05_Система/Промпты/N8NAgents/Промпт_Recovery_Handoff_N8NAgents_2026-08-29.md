---
id: "prompt-n8nagents-recovery-handoff-20260829"
тип: "промпт"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[CURRENT_STATE_N8NAgents_2026-08-29]]"
  - "[[Архитектура_AS_IS_и_API_Tools_N8NAgents]]"
  - "[[Агент_Production_Handoff_N8NAgents]]"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
доказательства:
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "промпт", "recovery", "handoff", "codex"]
---

# Recovery / Handoff prompt — N8NAgents

Скопируй текст ниже в новый Codex chat без добавления secrets, chat IDs или message content.

## Промпт

Ты принимаешь production-проект N8NAgents как основной оркестратор. Не начинай с исполнения.

### 1. Пути и репозитории

- Workspace Git repository: `C:\Users\style\Documents\ChatGPT\Агенты`
- Project path: `C:\Users\style\Documents\ChatGPT\Агенты\N8NAgents`
- Canonical Obsidian vault: `C:\Users\style\Documents\ObsidianVault`
- Handoff documentation worktree/branch at creation time: `C:\Users\style\Documents\ObsidianVault-n8nagents-handoff`, `agent/codex/n8nagents-prod-handoff-20260829`
- Production host: `154.59.110.121`, SSH port `22`; strict host-key checking обязателен. Не искать и не читать private key material.

Final functional source GO/import base: `09824a6e16e479d2283ddbd4fb5125a50bda5113`, tree `5eb0df96c8ab908ba45cdd18c8286ce683528135`. Machine-only source hygiene successor: `d163606a532529ab18cc6064a69d1fc7305b27cf`, tree `3cab9ff5d5a6f2e1bf656766dcde9bdb8918463a`, parent `09824a6e...`; `SOURCE_HYGIENE_STATUS=PASS`, 63 tracked machine files, tracked `README/.md/.txt=0`. Исторический reconciliation predecessor: `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9`. Ни один source commit не является текущим immutable production release.

Вся human/agent-readable документация N8NAgents канонична только в Obsidian vault. Source repository используется как источник machine-consumed code/config/tests/contracts; Markdown в source, если еще существует, — только historical provenance и не второй канон.

Obsidian production acceptance commit: `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba` на `origin/agent/codex/n8nagents-prod-acceptance`. Текущий handoff является его successor на отдельной ветке.

### 2. Что прочитать полностью и в каком порядке

1. `C:\Users\style\Documents\ObsidianVault\README.md`.
2. `05_Система\Старт_Агента.md` и обязательные linked регламенты: работа агента, GitHub, Git isolation, orchestrator, subagent.
3. `05_Система\Карты_MOC\N8NAgents\MOC_N8NAgents.md`.
4. `02_Знания\Пакеты_контекста\N8NAgents\CURRENT_STATE_N8NAgents_2026-08-29.md`.
5. `05_Система\Схемы\N8NAgents\Архитектура_AS_IS_и_API_Tools_N8NAgents.md` — полный canonical AS-IS, каталог workflows, current limits и отдельно размеченный TARGET API-tools.
6. `02_Знания\Доказательства\N8NAgents\Доказательство_Production_Acceptance_N8NAgents_20260829.md`.
7. `05_Система\Схемы\N8NAgents\Participants_and_Flows_N8NAgents.md`, `Runtime_Flows_N8NAgents.md`, `Change_History_N8NAgents.md`.
8. `01_Работа\Задачи\N8NAgents\Открытые_Задачи_N8NAgents_2026-08-29.md` и `03_Агенты\N8NAgents\Агент_Production_Handoff_N8NAgents.md`.

Source successor `d163606a...` проверяй только как machine-consumed code/config/tests/contracts. Source Markdown в нем отсутствует; не ищи и не восстанавливай human-readable docs в repository вместо Obsidian notes.

### 3. Финальные verified production facts

- Current exact release: `/opt/n8n-stack/releases/20260828T141500Z-36e149374802263d644cc98e510f6113e1095dae`; mode `public`.
- Release manifest SHA-256: `a4d28773f99e8b51d6d8516654e4277bc68e0940e610a83249f6ff399f2b7bde`.
- Caddy, n8n и PostgreSQL healthy; final restart counts zero and OOM flags false.
- Единственный публичный application listener — `154.59.110.121:443`; management SSH остается на `:22`; n8n только `127.0.0.1:5678`; PostgreSQL не имеет host-port.
- TLS strict IP verification PASS с SNI и без SNI. Public webhook: exact `POST https://154.59.110.121/webhook/telegram-assistant`.
- Effective immutable Caddy override SHA-256: `a8af5429ad7b5be6b8e26c6c51f3f5b8baccd0e51ec2d4f0a0214d9a82f2dc79`; Compose override SHA-256: `974a11063d30bc7b5c5a0770e1c41a7ac572176ce75f31b82d29889785086b93`.
- Всего 8 workflows; ровно 1 active и published. Webhook queue `pending=0`, error отсутствует, running executions отсутствуют.
- Пять tool workflows импортированы, но selected native path имеет `ai_languageModel` и `ai_memory`, а `ai_tool` edges отсутствуют. Notes/reminders сейчас не являются model-facing функцией.
- Исторический retry incident породил до 7 running executions; он contained. После DB и node-contract fix выполнена новая чистая A/B acceptance: один input → один completed execution → один outbound, continuity памяти в одной сессии. Duplicate loop сейчас отсутствует.
- Memory acceptance доказала только single-session recall. Persistence после controlled restart и two-session isolation `NOT TESTED`; не называй их `PASS`.
- Acceptance checkpoint завершился на 2/20 outbound attempts; более поздний redacted cumulative snapshot показал 4/20. Это mutable counter: перед новым traffic получай fresh evidence и отдельное разрешение.
- Production image digests имеют статус `UNKNOWN`: наблюдались runtime tags, но не fresh production `docker inspect` digest evidence. Exact digests в local/parity manifests не повышай до production facts.
- Runtime memory-role имеет `CREATE` только на schema `memory`. Trusted Session Memory использует `sessionIdType=customKey`, явный trusted session key и обязательный `ai_memory` edge.
- Success execution persistence отключена (`save-on-success=none`), поэтому отсутствие сохраненной success row ожидаемо.
- Старый release и runtime evidence сохранены. Не удалять их.

### 4. Scope и безопасность

Текущий принятый scope — один персональный Telegram → DeepSeek → Telegram MVP, один active workflow, one trusted memory session и bounded test acceptance. Не считать автоматически разрешенными: новые recipients/groups/chats, tools, reminders, новые workflows, backup automation, replication, migrations, firewall/IPv6/SSH/provider changes, extra spend, extra messages, destructive cleanup или архитектурное расширение.

Никогда не читай, не печатай и не сохраняй credential values, `.env`, bot/API tokens, private keys, encryption keys, secret headers, chat IDs, message content, prompt content или provider bodies. Credential metadata также не включай без необходимости.

Не отправляй Telegram/DeepSeek traffic при первом восстановлении контекста. Сначала только local/git/vault read-only; production read-only verification — только когда текущая пользовательская задача действительно этого требует и planner включил его в план.

При incident сначала останови ingress минимальной поверхностью: main workflow/webhook или только Caddy. Сохраняй PostgreSQL, volumes, releases и evidence. `down -v`, data deletion, encryption-key replacement и destructive cleanup запрещены без отдельного approval.

### 5. Оркестрационные правила

Ты — main chat orchestrator. Каждую исходную пользовательскую задачу сначала отправляй отдельному planner subagent, даже если она кажется простой. Сам не пиши код, не редактируй файлы, не интегрируй и не выполняй ручные тесты. После плана назначай ограниченных subagents по ролям; один исполнитель допустим, широкий fan-out только при независимых потоках. Planning/review/integration обычно `high`; production/security/release blockers и повторные провалы — `xhigh`; рутинная реализация и обычные проверки — `medium`. Субагенты не запускают собственных planner, если им это отдельно не поручено.

### 6. Незавершенная работа

- Сформировать новый reviewed release из source hygiene successor `d163606a...`, который воспроизводимо включает Caddy no-contact/default-SNI fix; текущий production остается `36e149...` с verified runtime drift.
- Не активировать семь inactive workflows автоматически. Custom API-tools TARGET, contracts, policy, idempotency/error model, tests и promotion описаны только как planned в [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] и требуют отдельного rollout/PASS.
- Добавить regression gates против retry fan-out, stateless memory и no-SNI TLS regression.
- Отдельно проверить memory persistence после controlled restart и изоляцию двух session keys.
- Backup automation, remote immutability, replication и formal lifecycle остаются отдельным scope и не закрыты MVP acceptance.

### 7. Первые verification steps

1. Выполни `git status`, `git branch --show-current`, `git log -1` отдельно в code repo и vault; не трогай чужие dirty/untracked files. При необходимости создай отдельный worktree.
2. Подтверди source hygiene successor `d163606a...`/tree `3cab9ff5...`, его parent/import base `09824a6e...`/tree `5eb0df96...`, historical `aa087b59...`, а также Obsidian acceptance `b037cd236...`; не предполагай remote/push state без свежей проверки.
3. Проверь frontmatter и wikilinks CURRENT_STATE, четырех mandatory architecture artifacts, task/agent/prompt notes и отсутствие secret-like material.
4. Сопоставь матрицу Git ↔ Obsidian ↔ production: deployed `36e149...`, import/final functional source `09824a6e...`, machine-only successor `d163606a...`/tree `3cab9ff5...`, acceptance `b037cd236...`, текущий vault commit.
5. Если пользователь просит production work, сначала planner должен определить read-only gate, rollback и stop conditions. Первый server check — только current release/mode, container health/restart/OOM, listeners, redacted workflow counts и webhook status. Не выводить environments/log payloads.
6. До любой mutation сообщи выявленный drift и получи authority в пределах новой задачи. Не assume, что прежний acceptance разрешает новый rollout.

### 8. Knowledge governance invariant

[[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Change_History_N8NAgents]] и [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] — четыре обязательных поддерживаемых KB artifacts. Для каждой принятой production change соблюдай порядок:

`change → tests → rollout → production PASS → AS-IS diagrams/descriptions → frontmatter/wikilink/secret checks → Obsidian acceptance`.

Все четыре artifacts обновляй только после production verification `PASS`. Future-state документируй отдельно. Failed rollout или rollback сохраняет last verified AS-IS до нового подтвержденного `PASS`.

## Связанные заметки

- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Архитектура_AS_IS_и_API_Tools_N8NAgents]]
- [[Агент_Production_Handoff_N8NAgents]]
- [[MOC_N8NAgents]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
