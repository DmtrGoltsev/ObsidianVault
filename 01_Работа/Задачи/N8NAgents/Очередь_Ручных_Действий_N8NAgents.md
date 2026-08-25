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
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
теги: ["n8n", "ручные-действия", "provider", "secrets", "blocked-external"]
---

# Очередь ручных действий N8NAgents

Записывать здесь только non-secret решения, статусы и подтверждения. Не помещать токены, API keys, passwords, private keys, encryption keys, chat IDs или другие персональные identifiers.

| Приоритет | Требуется от владельца / внешней стороны | Что подтвердить или выполнить | Статус |
|---|---|---|---|
| P0 | Provider console | Диагностировать SSH session-channel: transport/auth проходят, но сервер не отвечает после channel request; подтвердить состояние SSH daemon, account/session limits и console access без изменения конфигурации | BLOCKED-EXTERNAL |
| P0 | Provider console | Свежая console-проверка перед любым SSH hardening или server mutation | WAITING |
| P1 | Владелец доменов | `EDITOR_DOMAIN`, `WEBHOOK_DOMAIN`, DNS provider, readiness DNS и ACME email | WAITING |
| P1 | Владелец проекта | Timezone | WAITING |
| P1 | Владелец Telegram | Наличие отдельных dev/prod bots, username(s) и allowed IDs; token вводить только напрямую в защищённый server-side credential flow, не в vault/чат | WAITING |
| P1 | Владелец DeepSeek | API key вводить только напрямую в защищённый server-side credential flow; подтвердить non-secret base URL/model отдельно | WAITING |
| P1 | Владелец n8n | Owner account, 2FA и server-side credential binding после доступного HTTPS editor | WAITING |
| P1 | Владелец backup | Destination, retention, RPO/RTO, encryption/key-custody policy; ключи не записывать здесь | WAITING |
| P2 | Владелец проекта | IPv6 policy | WAITING |
| P2 | Владелец / валидатор | Final E2E: Telegram → DeepSeek → Telegram, authorization before LLM/tools, persistence, backup/restore и external exposure checks | WAITING |

## Правило разблокировки

Первым снимается только P0 provider-console diagnosis. До него `A2` не запускать; изменения VPS, SSH hardening и deployment не начинать. Остальные пункты не предполагают передачу секретов через vault или чат.

Локальная проверка JSON Schema закрыта в [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]; Docker/Bash/runtime гейты этим не закрываются.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[MOC_N8NAgents]]
