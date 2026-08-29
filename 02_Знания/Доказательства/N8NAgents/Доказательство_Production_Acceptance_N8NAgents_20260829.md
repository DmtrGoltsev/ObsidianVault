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
доказательства: []
теги: ["n8n", "production", "acceptance", "e2e", "telegram", "memory"]
---

# Production acceptance N8NAgents — 2026-08-29

## Что доказано

Основной production-сценарий Telegram → n8n → memory → LLM → Telegram прошёл новую двухшаговую приёмку A/B после containment первого retry incident. Финальное состояние production: exact S2 release `36e149374802263d644cc98e510f6113e1095dae`, mode `public`; Caddy/n8n/PostgreSQL healthy без restart/OOM; один из восьми workflow active и одна published active version; webhook queue `pending=0` без ошибки; running executions отсутствуют; расход лимита `2/20`.

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

- Telegram update `476688234` породил ровно один execution `16` со статусом `app completed`.
- Число строк памяти изменилось `0 → 2`.
- Создан ровно один outbound.

### Gate B — PASS

- Telegram update `476688235`, попытка `1`, завершён со статусом `app completed`.
- Execution `17` восстановлен по последовательности и состоянию; его подробная запись уже pruned, поэтому номер отмечен как inferred, а не как прямое наблюдение.
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
- Detailed execution `17` pruned; его идентификатор имеет уровень inferred, остальные перечисленные метрики подтверждены прямым gate evidence.
- Memory continuity доказана только для одной trusted session. Persistence после controlled restart и изоляция двух session keys в этом gate не тестировались и остаются follow-up.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Participants_and_Flows_N8NAgents]]
- [[Runtime_Flows_N8NAgents]]
- [[Change_History_N8NAgents]]
