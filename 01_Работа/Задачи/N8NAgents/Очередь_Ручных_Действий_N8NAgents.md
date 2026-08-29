---
id: "manualqueue-n8nagents-20260826"
тип: "задача"
статус: "заменено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Журнал_Автономной_Работы_N8NAgents]]"
  - "[[Доказательство_H1_Phase_A_User_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_H2_Phase_A_Stop_Preflight_N8NAgents_20260826]]"
  - "[[Доказательство_H3_Phase_A_Reapproval_N8NAgents_20260826]]"
  - "[[Доказательство_H4_Phase_A_Wrapper_Stop_Recovery_Plan_N8NAgents_20260826]]"
  - "[[Доказательство_H5_Phase_A_Recovery_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_H6_Third_Stop_Packaging_Incident_N8NAgents_20260826]]"
  - "[[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]]"
  - "[[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]"
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
теги: ["n8n", "ручные-действия", "provider", "secrets", "blocked-external"]
---

# Очередь ручных действий N8NAgents

> Историческая pre-production очередь. Многие пункты ниже уже superseded фактическим rollout/acceptance и не должны исполняться как current backlog. Актуальная очередь: [[Открытые_Задачи_N8NAgents_2026-08-29]]; verified state: [[CURRENT_STATE_N8NAgents_2026-08-29]].

Записывать здесь только non-secret решения, статусы и подтверждения. Не помещать токены, API keys, passwords, private keys, encryption keys, chat IDs или другие персональные identifiers.

| Приоритет | Требуется от владельца / внешней стороны | Что подтвердить или выполнить | Статус |
|---|---|---|---|
| P0 | Владелец проекта | Выбрать один способ закрытия K4R локальной Linux boundary: включить Windows Sandbox **или** разрешить локальную HTTPS-загрузку exact hash-pinned Linux/v86 boot/runtime inputs для no-NIC sandbox | WAITING — `B2R_NETWORK_BOUNDARY`/RC45; Windows Sandbox является system feature и может потребовать reboot; не переустанавливать VPS OS |
| P0 | Владелец проекта | Явно авторизовать расширенный offline recovery budget и новый corrective cycle для K4; это **не** authorizes remote execution | WAITING — K4 retry cap исчерпан; сначала planning, corrective commit, fresh Linux QA и independent review |
| P0 | Provider / владелец | Подтвердить firewall policy провайдера и допустимые inbound ports (`22`, затем `80/443`); отдельно определить IPv6 policy | WAITING — provider live-panel mapping остаётся residual; public-edge deferred |
| P0 | Владелец / provider | Актуальная сверка VPS в Hexcore, provider firewall и IPv6 policy перед public edge | WAITING — H7 разрешает execution, но DNS/provider UI остаётся ручным gate |
| P1 | Владелец доменов | `EDITOR_DOMAIN`, `WEBHOOK_DOMAIN`, DNS provider, readiness DNS и ACME email | WAITING |
| P1 | Владелец проекта | Timezone | WAITING |
| P1 | Владелец Telegram | Наличие отдельных dev/prod bots, username(s) и allowed IDs; token вводить только напрямую в защищённый server-side credential flow, не в vault/чат | WAITING |
| P1 | Владелец DeepSeek | API key вводить только напрямую в защищённый server-side credential flow; подтвердить non-secret base URL/model отдельно | WAITING |
| P1 | Владелец n8n | Owner account, 2FA и server-side credential binding после доступного HTTPS editor | WAITING |
| P1 | Владелец backup | Destination, retention, RPO/RTO, encryption/key-custody policy; ключи не записывать здесь | WAITING |
| P2 | Владелец проекта | IPv6 policy | WAITING |
| P2 | Владелец / валидатор | Final E2E: Telegram → DeepSeek → Telegram, authorization before LLM/tools, persistence, backup/restore и external exposure checks | WAITING |

## Правило разблокировки

A2 read-only discovery завершён `PASS` после reboot VPS: [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]. H5/H6 сохраняются историей frozen state. K4R-OFFLINE-v2 `BLOCKED` до validator start, поэтому сначала требуется выбор владельца по локальной Linux boundary. B2r evidence сохраняет `REMOTE/VPS/VAULT/NETWORK=0`; это обновление документов сделано после run и не изменяет его измерение. Только после выбранного offline пути, success evidence, нового planning/review и отдельно named authorization может быть предложен remote gate с exact commit и attempt budget — [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]. Остальные пункты не предполагают передачу секретов через vault или чат.

Локальная проверка JSON Schema закрыта в [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]; Docker/Bash/runtime гейты этим не закрываются.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[MOC_N8NAgents]]
