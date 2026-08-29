---
id: "schema-n8nagents-change-history-20260829"
тип: "схема"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[CURRENT_STATE_N8NAgents_2026-08-29]]"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
доказательства:
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "change-history", "production", "as-is"]
---

# Change History — N8NAgents

Журнал хранит только redacted изменения, которые дошли до проверенного runtime или явно помечены как source-only. Plans не выдаются за deployed state.

| Дата | Контур | Изменение | Evidence / commit | Статус |
|---|---|---|---|---|
| 2026-08-28 | Git/release | Подготовлен S2 IP-TLS candidate | `36e149374802263d644cc98e510f6113e1095dae`; manifest `a4d28773...` | Deployed current |
| 2026-08-29 | Production edge | Удален фиктивный ACME contact через immutable runtime override | Caddyfile SHA `ae54da45...` | Superseded v2 |
| 2026-08-29 | Production edge | Добавлен default SNI для IP-клиентов без SNI | Caddyfile SHA `a8af5429...`; Compose override `974a1106...` | Active, TLS PASS |
| 2026-08-29 | Production rollout | Durable atomic switch на S2, старый release сохранен | systemd one-shot/rollback evidence; current `36e149...` | PASS |
| 2026-08-29 | Production workflow | Первый live run обнаружил fan-out до 7 running executions и memory errors | QA/runtime redacted counts | Contained, historical |
| 2026-08-29 | PostgreSQL | Runtime memory-role получил минимальный `CREATE` только на schema `memory` | Grant checks + memory write | PASS |
| 2026-08-29 | n8n | Trusted Session Memory переведен на `customKey`, явный trusted session key и обязательный `ai_memory` edge | Node contract + A/B | PASS |
| 2026-08-29 | Production acceptance | Новая чистая A/B: one-in/one-execution/one-outbound, same-session continuity | [[Доказательство_Production_Acceptance_N8NAgents_20260829]] | PASS |
| 2026-08-29 | Git/source | Production memory/grant contract reconciled в исходниках и тестах | `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9` | Source-only; не новый release |
| 2026-08-29 | Obsidian | Первичная production acceptance зафиксирована | `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba` | Accepted predecessor |

## Правило новой записи

Добавлять AS-IS запись только после: `change → tests → rollout → production PASS`. Затем синхронно обновить [[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[CURRENT_STATE_N8NAgents_2026-08-29]], выполнить frontmatter/wikilink/secret checks и зафиксировать Obsidian acceptance commit.

Если change остановлен до production PASS, записывать его как `planned`, `blocked`, `rolled back` или `source-only`, но не менять AS-IS diagrams.

## Связанные заметки

- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Participants_and_Flows_N8NAgents]]
- [[Runtime_Flows_N8NAgents]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
