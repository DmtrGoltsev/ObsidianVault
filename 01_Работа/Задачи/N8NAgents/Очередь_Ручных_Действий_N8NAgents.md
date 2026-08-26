---
id: "manualqueue-n8nagents-20260826"
тип: "задача"
статус: "заблокировано"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Журнал_Автономной_Работы_N8NAgents]]"
  - "[[Доказательство_H1_Phase_A_User_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_H2_Phase_A_Stop_Preflight_N8NAgents_20260826]]"
  - "[[Доказательство_H3_Phase_A_Reapproval_N8NAgents_20260826]]"
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
теги: ["n8n", "ручные-действия", "provider", "secrets", "blocked-external"]
---

# Очередь ручных действий N8NAgents

Записывать здесь только non-secret решения, статусы и подтверждения. Не помещать токены, API keys, passwords, private keys, encryption keys, chat IDs или другие персональные identifiers.

| Приоритет | Требуется от владельца / внешней стороны | Что подтвердить или выполнить | Статус |
|---|---|---|---|
| P0 | Provider / владелец | Подтвердить firewall policy провайдера и допустимые inbound ports (`22`, затем `80/443`); отдельно определить IPv6 policy | WAITING |
| P0 | Владелец | Явно повторно одобрил финальный reviewed commit `f6e0c745ab889c11df1ab83ccf7957534be600cd` для `phase-a-internal` | CLOSED FOR RETRY — `SWAP_OPTION=plaintext-2g`; retry начат, outcome pending |
| P1 | Владелец доменов | `EDITOR_DOMAIN`, `WEBHOOK_DOMAIN`, DNS provider, readiness DNS и ACME email | WAITING |
| P1 | Владелец проекта | Timezone | WAITING |
| P1 | Владелец Telegram | Наличие отдельных dev/prod bots, username(s) и allowed IDs; token вводить только напрямую в защищённый server-side credential flow, не в vault/чат | WAITING |
| P1 | Владелец DeepSeek | API key вводить только напрямую в защищённый server-side credential flow; подтвердить non-secret base URL/model отдельно | WAITING |
| P1 | Владелец n8n | Owner account, 2FA и server-side credential binding после доступного HTTPS editor | WAITING |
| P1 | Владелец backup | Destination, retention, RPO/RTO, encryption/key-custody policy; ключи не записывать здесь | WAITING |
| P2 | Владелец проекта | IPv6 policy | WAITING |
| P2 | Владелец / валидатор | Final E2E: Telegram → DeepSeek → Telegram, authorization before LLM/tools, persistence, backup/restore и external exposure checks | WAITING |

## Правило разблокировки

A2 read-only discovery завершён `PASS` после reboot VPS: [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]. Исходный approval `d1703bdfbdb183836afe7d75c871938ca8a9f196` с `SWAP_OPTION=plaintext-2g` остановлен на H2 до mutations; policy redesign `7998020` завершён reviewed commit `f6e0c745ab889c11df1ab83ccf7957534be600cd`. Пользователь явно повторно одобрил этот финальный commit для `phase-a-internal`; retry начат, outcome pending — [[Доказательство_H3_Phase_A_Reapproval_N8NAgents_20260826]]. Provider firewall/IPv6 и все прочие пункты остаются `WAITING` и не входят в внутренний scope. Остальные пункты не предполагают передачу секретов через vault или чат.

Локальная проверка JSON Schema закрыта в [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]; Docker/Bash/runtime гейты этим не закрываются.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[MOC_N8NAgents]]
