---
id: "evidence-n8nagents-production-acceptance-20260829"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "production gate evidence 2026-08-29 (redacted)"
  - "user acceptance confirmation 2026-08-29"
  - "Git N8NAgents aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9"
  - "Git N8NAgents docs/production-memory-acceptance-2026-08-29.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/production-memory-acceptance-2026-08-29.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
проверка_редакции: "PASS — numeric update/execution identities removed; no secret/PII values or message content"
теги: ["n8n", "production", "acceptance", "e2e", "telegram", "memory"]
---

# Production acceptance N8NAgents — 2026-08-29

## Что доказано

Основной production-сценарий Telegram → n8n → memory → LLM → Telegram прошёл новую двухшаговую приёмку A/B после containment первого retry incident. Финальное состояние production: exact S2 release `36e149374802263d644cc98e510f6113e1095dae`, mode `public`; Caddy/n8n/PostgreSQL healthy без restart/OOM; один из восьми workflow active и одна published active version; webhook queue `pending=0` без ошибки; running executions отсутствуют. Acceptance checkpoint завершился на `2/20`; более поздний redacted cumulative snapshot показал `4/20`.

External edge доказан для strict IP TLS с SNI и без SNI. Единственный публичный application listener — `443` (management SSH `:22` остается отдельным), n8n доступен только на loopback `5678`, PostgreSQL host-port отсутствует. Полная redacted AS-IS сводка: [[CURRENT_STATE_N8NAgents_2026-08-29]].

## Инциденты, причины и исправления

| Этап | Причина | Исправление | Результат |
|---|---|---|---|
| TLS | В ACME был указан фиктивный email; запросы без SNI не получали подходящий сертификат. | Фиктивный contact удален; задан `default_sni` для production IP. | Strict IP TLS с SNI и без SNI `PASS`. |
| PostgreSQL memory | Runtime-роли не хватало права создания объектов в целевой схеме. | Выдано минимальное право `CREATE` только на схему `memory`; широкие права не выдавались. | Запись memory проходит. |
| Контракт memory node | Параметры `sessionIdType` и `customKey` не соответствовали контракту узла. | Контракт приведён к `sessionIdType=customKey` с явным ключом сессии. | Одна и та же сессия сохраняется между сообщениями. |
| Повторные попытки | Первый live run породил до 7 concurrent/running executions и memory errors. | Workflow/webhook contained; DB и node contract исправлены; новая A/B выполнялась по одному контролируемому входу. | Исторический incident закрыт; текущих running executions, duplicate loop и лишних outbound нет. |

## Redacted evidence

### Gate A — PASS

- Redacted update A породил ровно одно выполнение со статусом `app completed`.
- Число строк памяти изменилось `0 → 2`.
- Создан ровно один outbound.

### Gate B — PASS

- Redacted update B, попытка `1`, завершён со статусом `app completed`.
- Подробная success-запись второго выполнения уже pruned; последовательность подтверждена по состоянию без сохранения numeric execution identity.
- В той же сессии число строк памяти изменилось `2 → 4`.
- Совокупный outbound после A/B равен `2`.
- Пользователь подтвердил правильное извлечение ранее сохранённого значения; само значение и тексты сообщений намеренно не сохранены.

## Итог gate

- Статус: `PASS`.
- Update/execution/outbound соответствуют модели «один вход — одно выполнение — один ответ».
- Memory continuity подтверждена отдельным вторым сообщением и пользовательской проверкой результата.
- Token, chat id, содержимое сообщений, контрольное значение и прочие секреты/персональные данные в evidence отсутствуют.
- Success execution persistence настроена `none`; отсутствие сохраненной успешной строки после проверки ожидаемо и не отменяет bounded gate evidence.

## Source и runtime reconciliation

- Deployed immutable release остается `36e149374802263d644cc98e510f6113e1095dae`.
- Effective Caddy no-contact/default-SNI runtime override хранится отдельно от release manifest и связан exact hashes в [[CURRENT_STATE_N8NAgents_2026-08-29]].
- Production memory/grant correction reconciled в local source commit `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9`; этот commit не объявляется уже развернутым release.
- Первичная Obsidian acceptance зафиксирована commit `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba`; эта заметка уточнена final post-containment state в successor handoff branch.

## Rollback

При регрессии: деактивировать единственный production workflow, вернуть предыдущую опубликованную версию workflow и Caddy-конфигурации, отменить только точечное изменение контракта memory node; право `CREATE` на схему `memory` отозвать лишь после остановки записи, иначе memory снова перестанет работать. После отката повторить health, webhook queue и одиночный smoke test.

## Ограничения и follow-up

- Reconciliation канонического источника истины продолжается и не входит в этот acceptance; до завершения не считать старые статусные заметки эквивалентными фактическому production state.
- Backup и replication заморожены и не входят в эту приёмку; restore/replication gate здесь не заявлен и не закрыт.
- Detailed success execution pruned; последовательность второго выполнения имеет уровень inferred, остальные перечисленные метрики подтверждены прямым gate evidence.
- Memory continuity доказана только для одной trusted session. Persistence после controlled restart и изоляция двух session keys в этом gate не тестировались и остаются follow-up.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Participants_and_Flows_N8NAgents]]
- [[Runtime_Flows_N8NAgents]]
- [[Change_History_N8NAgents]]


## Импортированный source acceptance record

> [!note] Source provenance
> Полный sanitized source record сохранён ниже как provenance snapshot `09824a6e...`. Канонический итог и более новый cumulative counter остаются в верхней части этой заметки.

This durable record contains no chat IDs, user IDs, session IDs, message bodies, control word, credential IDs, tokens, headers, public addresses, or secrets.

### Bound production state

- Production S2 source commit: `36e149374802263d644cc98e510f6113e1095dae`.
- n8n version observed: `docker.n8n.io/n8nio/n8n:2.36.7`; production runtime digest **UNKNOWN — not independently reverified**.
- PostgreSQL version observed: `postgres:17.11-alpine3.24`; production runtime digest **UNKNOWN — not independently reverified**.
- Workflow catalogue at acceptance: one active workflow out of eight.

Repository local/parity pins are `sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c` for n8n 2.36.7 and `sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73` for PostgreSQL 17.11. These exact values identify local/test inputs only; they are not production `docker inspect` evidence and do not establish the production runtime digests.

### A/B evidence

| Step | Telegram update | n8n execution | Application state | Memory rows | Outbound evidence |
|---|---:|---:|---|---:|---|
| A | redacted update A | redacted execution identity | `completed` | `0 → 2` | one outbound attempt |
| B | redacted update B | inferred sequence; success record pruned by configured execution retention | `completed` | `2 → 4` | second outbound attempt; durable budget `2/20` |

The user confirmed that B recalled the value supplied in A correctly. Webhook inspection showed zero pending updates and no webhook error. No duplicate or retry loop was observed for these two acceptance updates.

### Exact scope of PASS

| Claim | Status | Evidence boundary |
|---|---|---|
| Single-session recall through the active production workflow | **PASS** | A/B sequence above plus user confirmation. |
| Direct PostgreSQL parity for n8n 2.36.7 LangChain initialization and add/get/clear SQL | **PASS** | Repository PostgreSQL 17.11 contract test logs in directly as `memory_runtime`, reruns the grants migration, checks exact privileges/search path, then exercises exact DDL, ordered read, and clear-by-session inside a transaction. |
| Persistence across an n8n or PostgreSQL restart | **UNKNOWN — not tested** | No controlled restart occurred during this acceptance. |
| Isolation between two distinct session keys | **UNKNOWN — not tested** | Only one sanitized session participated in A/B acceptance. |

The direct PostgreSQL parity result supports the least-privilege database contract; it is separate from and does not expand the production single-session recall PASS.
