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
  - "Git N8NAgents commit 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
  - "Git N8NAgents source-hygiene commit d163606a532529ab18cc6064a69d1fc7305b27cf; tree 3cab9ff5d5a6f2e1bf656766dcde9bdb8918463a"
  - "Git N8NAgents final local review commit dd9e10a9b9b51e33761971e517a61a6bd9fa899c; tree 1d9dc11150e87846937b622748c95877f4823128; parent d163606a532529ab18cc6064a69d1fc7305b27cf"
  - "Obsidian commit b037cd23690b35ded8e2a0c5c9e2473a53f4fbba"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
  - "[[Архитектура_AS_IS_и_API_Tools_N8NAgents]]"
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
| Test budget | acceptance checkpoint завершился на 2/20; более поздний redacted cumulative snapshot показал 4/20; это mutable counter, а не постоянный configuration fact |
| Secrets/PII | значения secrets, chat ID и содержимое сообщений в KB не сохраняются |

Success execution rows могут отсутствовать, потому что production настроен на `save-on-success=none`; это ожидаемая privacy-настройка, а не доказательство отсутствия выполнения.

Memory acceptance доказывает recall/continuity только в одной trusted session в рамках A/B. Persistence после n8n/PostgreSQL restart и изоляция двух одновременных session keys в этой production acceptance **не тестировались**; не повышать их до `PASS`.

## Архитектура AS-IS

| Слой | Компонент | Текущая граница |
|---|---|---|
| Public edge | Caddy `2.11.4-alpine`; production digest `UNKNOWN` | Только `443`; exact webhook route; все лишние/неавторизованные routes дают `404`; IP certificate является default для no-SNI |
| Orchestration | n8n `2.36.7`; production digest `UNKNOWN` | Host bind только `127.0.0.1:5678`; credentials хранятся server-side; один production workflow active |
| Data | PostgreSQL `17.11-alpine3.24`; production digest `UNKNOWN` | Нет host-port; отдельные metadata/app/memory boundaries; `CREATE` для runtime memory-role ограничен схемой `memory` |
| Telegram | Bot API webhook | Exact POST path, server-side secret header, единственный allowlisted test recipient; identifiers не документируются |
| LLM | DeepSeek | Вызывается только после trust/allowlist gate; тестовый budget ограничен; ключ не хранится в Git/Obsidian |
| Memory | Postgres Chat Memory v1.4 | `sessionIdType=customKey`, явный trusted `sessionKey`, таблица `n8n_chat_histories`, `ai_memory` edge к agent |

Runtime tags наблюдались, но immutable production image digests не были подтверждены независимым `docker inspect` evidence. Любые exact digests в local/parity manifests — только **LOCAL/PARITY PINS**, не production facts.

Полная каноническая архитектура: [[Архитектура_AS_IS_и_API_Tools_N8NAgents]]. Связанные схемы: [[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]].

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
| `tool_save_note` | Сохранение заметки с trusted actor/chat и idempotency | Imported, inactive; не reachable из selected native agent path |
| `tool_search_notes` | Поиск заметок в trusted scope | Imported, inactive; не reachable из selected native agent path |
| `tool_list_notes` | Список заметок в trusted scope | Imported, inactive; не reachable из selected native agent path |
| `tool_create_reminder` | Создание напоминания без внешней отправки в транзакции | Imported, inactive; не reachable из selected native agent path |
| `tool_list_reminders` | Список напоминаний в trusted scope | Imported, inactive; не reachable из selected native agent path |
| `reminder_dispatcher` | Bounded delivery напоминаний | Imported, inactive |
| `error_handler` | Sanitized internal error handling | Imported, inactive |

Production inventory подтверждает ровно 8 workflow records и ровно один active/published workflow. Пять tool workflows импортированы, но `Native AI Agent` имеет только `ai_languageModel` и `ai_memory` edges — ни одного `ai_tool` edge. Поэтому notes/reminders сейчас не являются model-facing функциональностью; unselected fallback wiring не меняет этот AS-IS limitation.

## Инциденты и принятые решения

| Инцидент | Решение | Финальный статус |
|---|---|---|
| ACME `invalidContact` из-за фиктивного email | Не передавать фиктивный ACME contact; применен минимальный immutable Caddy override | Resolved |
| TLS без SNI завершался `alert internal_error` | Добавлен `default_sni` для public IP; доказаны strict SNI и no-SNI handshakes | Resolved |
| SSH-bound rollout прерывался при disconnect/HUP | Финальный rollout выполнен durable systemd one-shot с независимым rollback timer | Resolved |
| Memory node не мог создать требуемую таблицу | Выдано минимальное `CREATE` только на схему `memory` | Resolved |
| Legacy memory node contract делал workflow stateless/ошибочным | Зафиксированы `sessionIdType=customKey`, trusted `sessionKey` и обязательный `ai_memory` edge; source final GO `09824a6e...` | Resolved |
| Начальный retry loop породил 7 concurrent/running executions | Workflow/webhook были contained, ошибки исправлены, затем выполнена новая чистая A/B acceptance | Historical; текущих running executions и duplicate loop нет |

Подробная хронология: [[Change_History_N8NAgents]].

## Матрица Git ↔ Obsidian ↔ production

| Контур | Commit / artifact | Значение | Отношение к production |
|---|---|---|---|
| Git, deployed package | `36e149374802263d644cc98e510f6113e1095dae` | S2 IP-TLS release | Именно этот immutable release является `/opt/n8n-stack/current` |
| Runtime config | Caddyfile `a8af5429...`, Compose override `974a1106...` | no-contact + default no-SNI certificate | Активно поверх S2; вне release manifest, но hash/mode/owner проверены |
| n8n/PostgreSQL runtime | Финальные UI/DB corrections | Trusted memory contract и минимальный grant | Доказаны A/B, но runtime state не равен чистому checkout `36e149` |
| Git, final source GO | `09824a6e16e479d2283ddbd4fb5125a50bda5113`; tree `5eb0df96c8ab908ba45cdd18c8286ce683528135` | Machine-consumed code/config/tests/contracts reconciled с принятым состоянием | Successor source candidate; не объявлять уже развернутым release |
| Git, source hygiene predecessor | `d163606a532529ab18cc6064a69d1fc7305b27cf`; tree `3cab9ff5d5a6f2e1bf656766dcde9bdb8918463a`; parent `09824a6e...` | 63 tracked machine files; tracked `README/.md/.txt=0`; human docs перенесены в Obsidian; machine contracts заменили prose dependencies | `SOURCE_HYGIENE_STATUS=PASS`; локальный predecessor финального review commit; не deployed и не upstream-published |
| Git, final local reviewed source | `dd9e10a9b9b51e33761971e517a61a6bd9fa899c`; tree `1d9dc11150e87846937b622748c95877f4823128`; parent `d163606a...` | Exact-tree K4R release-gate corrections поверх source hygiene; два независимых `GO` — source hygiene и security; `P0=0`, `P1=0` | **LOCAL_ONLY / NOT_DEPLOYED**; source repository не имеет `origin`; commit не upstream-published; production/VPS не менялись и fresh VPS revalidation не выполнялась |
| Obsidian acceptance | `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba` | Production acceptance A/B | Утвержденный predecessor этой CURRENT_STATE-сводки |
| Obsidian handoff | ветка `agent/codex/n8nagents-prod-handoff-20260829` | Полная AS-IS документация и recovery prompt | Commit фиксируется в отчете исполнителя |

Final reviewed source `dd9e10a...` (parent `d163606a...`, source hygiene parent-chain от `09824a6e...`) — локальный exact commit и не является текущим production release: deployed immutable release остается строго `36e149...` с verified runtime corrections. Source repository не имеет настроенного `origin`; `dd9e10a...` имеет статус `LOCAL_ONLY / NOT_DEPLOYED`, не upstream-published, и документация не должна утверждать обратное. Human/agent-readable documentation канонична только в Obsidian; source repository содержит tracked machine-consumed code/config/tests/contracts. В vault `b037cd236...` присутствует в `origin/agent/codex/n8nagents-prod-acceptance`.

Residual `P2`: fresh VPS revalidation после `dd9e10a...` не выполнялась. Leader-only signal delivery полностью протестирована. Для `dash` process-group delivery допустимо отсутствие текстового `SIGNAL` label, но fail-closed поведение доказано через `RC79`, rollback и cleanup. Это ограничение source/test evidence, а не изменение production AS-IS.

## Операционные правила

- Для обычной проверки собирать только health/restart/OOM, current release/mode, listeners, bounded execution counts и redacted webhook status.
- Не печатать `.env`, Docker environment, credential values, Telegram identifiers, headers, message bodies, prompts или provider responses.
- При ingress-инциденте сначала остановить или деактивировать только webhook/main workflow либо Caddy; PostgreSQL и данные сохранять.
- Не использовать `down -v`, не удалять volumes/releases/backup artifacts и не менять encryption key без отдельного destructive approval.
- Rollback должен быть конкретным, обратимым и сопровождаться health/listener проверкой. Старый release и runtime artifacts сохранять.
- Paid/provider traffic и Telegram сообщения запускать только в явном лимите и только на подтвержденного allowlisted recipient.

## Открытые задачи

Канонический список: [[Открытые_Задачи_N8NAgents_2026-08-29]]. Критично не путать их с уже закрытым MVP acceptance:

1. Подготовить отдельный reviewed release из final local reviewed source `dd9e10a...`, который воспроизводимо включает Caddy no-contact/default-SNI fix, вместо постоянной зависимости от runtime drift.
2. Не активировать семь inactive workflow автоматически; отдельное добавление model-facing `ai_tool` edges проходит самостоятельный TARGET rollout.
3. Backup automation, remote immutability, replication и formal restore lifecycle держать в отдельном scope; MVP acceptance их не закрывает.
4. Сохранить regression gate против retry fan-out, stateless memory edge и no-SNI TLS regression.
5. Отдельно проверить memory persistence после controlled restart и изоляцию двух session keys; до этого их статус `NOT TESTED`.

## Scope boundaries

Текущий принятый scope — персональный Telegram → DeepSeek → Telegram MVP с одной trusted memory session и одним active workflow. Не входят автоматически: новые recipients/chats/groups, новые tool capabilities, reminders, backup automation, replication, migration, provider/firewall/SSH changes, дополнительный spend, destructive cleanup и новая архитектура.

Любое такое расширение требует отдельной пользовательской задачи, планировщика, named owner, проверяемого DoD и свежего acceptance.

## Обязательный инвариант knowledge governance

[[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Change_History_N8NAgents]] и [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] — обязательные поддерживаемые KB artifacts.

Порядок обновления неизменен:

`change → tests → rollout → production PASS → AS-IS diagrams/descriptions → wikilink/frontmatter/secret checks → Obsidian acceptance`.

Все четыре artifacts обновляются только после production verification `PASS`. Планы и будущая архитектура документируются отдельно от AS-IS. Failed rollout или rollback сохраняет last verified AS-IS до нового подтвержденного `PASS`.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Доказательство_Production_Acceptance_N8NAgents_20260829]]
- [[Архитектура_AS_IS_и_API_Tools_N8NAgents]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]]
