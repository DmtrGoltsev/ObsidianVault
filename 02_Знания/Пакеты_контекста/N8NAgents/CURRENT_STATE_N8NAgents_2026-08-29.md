---
id: "ctx-n8nagents-current-state-20260829"
тип: "пакет_контекста"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents commit 36e149374802263d644cc98e510f6113e1095dae"
  - "Git N8NAgents commit aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9"
  - "Obsidian commit b037cd23690b35ded8e2a0c5c9e2473a53f4fbba"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
доказательства:
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "production", "current-state", "handoff", "as-is"]
---

# CURRENT STATE — N8NAgents — 2026-08-29

Это каноническая AS-IS-сводка проекта после финальной production-проверки. Более старые документы про `deployment not started`, `server NO-GO`, K4/K4R blockers и отсутствие контейнеров остаются историей и не описывают текущее production-состояние.

## Приоритет источников истины

1. Свежая production-проверка и redacted runtime evidence.
2. Фактически развернутый immutable release, runtime-конфигурация и состояние n8n/PostgreSQL.
3. Git-код и тесты.
4. Эта сводка, схемы и acceptance evidence.
5. Исторические планы, журналы и чат.

При конфликте документ не повышает статус сам: сначала read-only сверка production, затем корректировка KB.

## Зафиксированное production-состояние

| Объект | Подтвержденный факт |
|---|---|
| Production host | `154.59.110.121`; SSH endpoint `:22`; webhook base использует IP TLS |
| Current release | `/opt/n8n-stack/releases/20260828T141500Z-36e149374802263d644cc98e510f6113e1095dae` |
| Release commit | `36e149374802263d644cc98e510f6113e1095dae` |
| Release manifest SHA-256 | `a4d28773f99e8b51d6d8516654e4277bc68e0940e610a83249f6ff399f2b7bde` |
| Runtime mode | `public` |
| Services | Caddy, n8n и PostgreSQL healthy; `RestartCount=0`, `OOMKilled=false` на финальной проверке |
| External listeners | единственный публичный application listener — `154.59.110.121:443`; management SSH остается на `:22`; n8n доступен только на `127.0.0.1:5678`; PostgreSQL host-port отсутствует |
| TLS | Let's Encrypt IP certificate; strict verify по IP, TLS с SNI и без SNI — `PASS` |
| Webhook | `POST https://154.59.110.121/webhook/telegram-assistant`; queue `pending=0`, error отсутствует |
| Workflows | всего 8; ровно 1 active и 1 published active version; после acceptance running executions отсутствуют |
| Acceptance | новая двухшаговая A/B-проверка после containment — `PASS`: на каждый вход одно выполнение и один outbound; память одной сессии сохранила continuity |
| Test budget | использовано 2 из разрешенных 20 Telegram test messages; дополнительный расход не подразумевается |
| Secrets/PII | значения secrets, chat ID и содержимое сообщений в KB не сохраняются |

Success execution rows могут отсутствовать, потому что production настроен на `save-on-success=none`; это ожидаемая privacy-настройка, а не доказательство отсутствия выполнения.

Memory acceptance доказывает recall/continuity только в одной trusted session в рамках A/B. Persistence после n8n/PostgreSQL restart и изоляция двух одновременных session keys в этой production acceptance **не тестировались**; не повышать их до `PASS`.

## Архитектура AS-IS

| Слой | Компонент | Текущая граница |
|---|---|---|
| Public edge | Caddy `2.11.4-alpine` с pinned digest `sha256:98eb57d882ccd5213d1688764db10c1ca2c58a1ca3a6717a3411ad798f7a423a` | Только `443`; exact webhook route; все лишние/неавторизованные routes дают `404`; IP certificate является default для no-SNI |
| Orchestration | n8n `2.36.7` с pinned digest `sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c` | Host bind только `127.0.0.1:5678`; credentials хранятся server-side; один production workflow active |
| Data | PostgreSQL `17.11-alpine3.24` с pinned digest `sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73` | Нет host-port; отдельные metadata/app/memory boundaries; `CREATE` для runtime memory-role ограничен схемой `memory` |
| Telegram | Bot API webhook | Exact POST path, server-side secret header, единственный allowlisted test recipient; identifiers не документируются |
| LLM | DeepSeek | Вызывается только после trust/allowlist gate; тестовый budget ограничен; ключ не хранится в Git/Obsidian |
| Memory | Postgres Chat Memory v1.4 | `sessionIdType=customKey`, явный trusted `sessionKey`, таблица `n8n_chat_histories`, `ai_memory` edge к agent |

Полные схемы: [[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]].

## Runtime override вне immutable release

Public edge использует root-owned immutable override, потому что исходный S2 package содержал нерабочий ACME contact и не обслуживал no-SNI TLS как default:

| Artifact | Path | SHA-256 | Mode |
|---|---|---|---|
| Effective Caddyfile | `/opt/n8n-stack/shared/runtime-overrides/36e149374802263d644cc98e510f6113e1095dae/Caddyfile.no-contact-default-sni` | `a8af5429ad7b5be6b8e26c6c51f3f5b8baccd0e51ec2d4f0a0214d9a82f2dc79` | `root:root 0400`, immutable |
| Compose override | `/opt/n8n-stack/shared/runtime-overrides/36e149374802263d644cc98e510f6113e1095dae/compose.caddy-no-contact-default-sni.yaml` | `974a11063d30bc7b5c5a0770e1c41a7ac572176ce75f31b82d29889785086b93` | `root:root 0400`, immutable |
| Shared config snapshot | `/opt/n8n-stack/shared/config.env` | `c760e7c30a31cc26c3306a365466b730048ed2a04535fd3f954743d444758a68` на rollout gate | secret-bearing; не читать и не копировать |

Старый release сохранен для rollback: `/opt/n8n-stack/releases/20260828T072000Z-15e14e3735d195e38d9c3d90a77976d1b0e1ad25`.

## Каталог workflows

| Каноническое имя | Назначение | Production state, доказанный на 2026-08-29 |
|---|---|---|
| `01_telegram_assistant` | Telegram → trust gate → memory → DeepSeek → Telegram | Единственный active/published workflow; A/B `PASS` |
| `tool_save_note` | Сохранение заметки с trusted actor/chat и idempotency | В каноническом каталоге; отдельная production-активация не доказана |
| `tool_search_notes` | Поиск заметок в trusted scope | В каноническом каталоге; отдельная production-активация не доказана |
| `tool_list_notes` | Список заметок в trusted scope | В каноническом каталоге; отдельная production-активация не доказана |
| `tool_create_reminder` | Создание напоминания без внешней отправки в транзакции | В каноническом каталоге; отдельная production-активация не доказана |
| `tool_list_reminders` | Список напоминаний в trusted scope | В каноническом каталоге; отдельная production-активация не доказана |
| `reminder_dispatcher` | Bounded delivery напоминаний | Не считать active без fresh production evidence |
| `error_handler` | Sanitized internal error handling | Не считать active без fresh production evidence |

Production evidence подтверждает счетчик `8` и только один active workflow, но не является secret-free export всех семи остальных объектов. До отдельной сверки не утверждать, что каждый inactive production object полностью совпадает с каноническим spec.

## Инциденты и принятые решения

| Инцидент | Решение | Финальный статус |
|---|---|---|
| ACME `invalidContact` из-за фиктивного email | Не передавать фиктивный ACME contact; применен минимальный immutable Caddy override | Resolved |
| TLS без SNI завершался `alert internal_error` | Добавлен `default_sni` для public IP; доказаны strict SNI и no-SNI handshakes | Resolved |
| SSH-bound rollout прерывался при disconnect/HUP | Финальный rollout выполнен durable systemd one-shot с независимым rollback timer | Resolved |
| Memory node не мог создать требуемую таблицу | Выдано минимальное `CREATE` только на схему `memory` | Resolved |
| Legacy memory node contract делал workflow stateless/ошибочным | Зафиксированы `sessionIdType=customKey`, trusted `sessionKey` и обязательный `ai_memory` edge; source reconciled в `aa087b59...` | Resolved |
| Начальный retry loop породил 7 concurrent/running executions | Workflow/webhook были contained, ошибки исправлены, затем выполнена новая чистая A/B acceptance | Historical; текущих running executions и duplicate loop нет |

Подробная хронология: [[Change_History_N8NAgents]].

## Матрица Git ↔ Obsidian ↔ production

| Контур | Commit / artifact | Значение | Отношение к production |
|---|---|---|---|
| Git, deployed package | `36e149374802263d644cc98e510f6113e1095dae` | S2 IP-TLS release | Именно этот immutable release является `/opt/n8n-stack/current` |
| Runtime config | Caddyfile `a8af5429...`, Compose override `974a1106...` | no-contact + default no-SNI certificate | Активно поверх S2; вне release manifest, но hash/mode/owner проверены |
| n8n/PostgreSQL runtime | Финальные UI/DB corrections | Trusted memory contract и минимальный grant | Доказаны A/B, но runtime state не равен чистому checkout `36e149` |
| Git, reconciled source | `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9` | Memory contract, tests, grant и docs reconciled с production | Локальный source-of-next-release; не объявлять уже развернутым release |
| Obsidian acceptance | `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba` | Production acceptance A/B | Утвержденный predecessor этой CURRENT_STATE-сводки |
| Obsidian handoff | ветка `agent/codex/n8nagents-prod-handoff-20260829` | Полная AS-IS документация и recovery prompt | Commit фиксируется в отчете исполнителя |

У code repository нет настроенного `origin`; `aa087b59...` локален. Нельзя считать его опубликованным или интегрированным в remote. В vault `b037cd236...` присутствует в `origin/agent/codex/n8nagents-prod-acceptance`.

## Операционные правила

- Для обычной проверки собирать только health/restart/OOM, current release/mode, listeners, bounded execution counts и redacted webhook status.
- Не печатать `.env`, Docker environment, credential values, Telegram identifiers, headers, message bodies, prompts или provider responses.
- При ingress-инциденте сначала остановить или деактивировать только webhook/main workflow либо Caddy; PostgreSQL и данные сохранять.
- Не использовать `down -v`, не удалять volumes/releases/backup artifacts и не менять encryption key без отдельного destructive approval.
- Rollback должен быть конкретным, обратимым и сопровождаться health/listener проверкой. Старый release и runtime artifacts сохранять.
- Paid/provider traffic и Telegram сообщения запускать только в явном лимите и только на подтвержденного allowlisted recipient.

## Открытые задачи

Канонический список: [[Открытые_Задачи_N8NAgents_2026-08-29]]. Критично не путать их с уже закрытым MVP acceptance:

1. Подготовить отдельный reviewed release, который интегрирует `aa087b59...` и Caddy no-contact/default-SNI fix, вместо постоянной зависимости от runtime drift.
2. Выполнить secret-free export/catalog reconciliation всех восьми production workflows; семь inactive объектов не активировать автоматически.
3. Обновить устаревшие repo docs, где deployment все еще указан как `not started`, только в отдельной code-задаче и чистом worktree.
4. Backup automation, remote immutability, replication и formal restore lifecycle держать в отдельном scope; MVP acceptance их не закрывает.
5. Сохранить regression gate против retry fan-out, stateless memory edge и no-SNI TLS regression.
6. Отдельно проверить memory persistence после controlled restart и изоляцию двух session keys; до этого их статус `NOT TESTED`.

## Scope boundaries

Текущий принятый scope — персональный Telegram → DeepSeek → Telegram MVP с одной trusted memory session и одним active workflow. Не входят автоматически: новые recipients/chats/groups, новые tool capabilities, reminders, backup automation, replication, migration, provider/firewall/SSH changes, дополнительный spend, destructive cleanup и новая архитектура.

Любое такое расширение требует отдельной пользовательской задачи, планировщика, named owner, проверяемого DoD и свежего acceptance.

## Обязательный инвариант knowledge governance

[[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]] и [[Change_History_N8NAgents]] — обязательные поддерживаемые KB artifacts.

Порядок обновления неизменен:

`change → tests → rollout → production PASS → AS-IS diagrams/descriptions → wikilink/frontmatter/secret checks → Obsidian acceptance`.

Планы и будущая архитектура документируются отдельно от AS-IS. Нельзя обновлять AS-IS схемы по намерению до production verification `PASS`.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Доказательство_Production_Acceptance_N8NAgents_20260829]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]]
