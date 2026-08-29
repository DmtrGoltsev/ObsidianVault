---
id: "proj-n8nagents-001"
тип: "проект"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[CURRENT_STATE_N8NAgents_2026-08-29]]"
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]"
  - "[[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]]"
  - "[[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "ai-ассистент", "self-hosted", "vps", "безопасность"]
---

# N8NAgents

## Цель

Безопасно спроектировать и развернуть self-hosted персонального AI-помощника на базе n8n Community Edition на VPS. Интерфейс — Telegram; LLM — DeepSeek; хранилище metadata, памяти и прикладных данных — PostgreSQL.

## Стек

| Слой | Планируемые технологии |
|---|---|
| Оркестрация | n8n Community Edition |
| Развертывание | Docker Compose |
| Reverse proxy | Caddy |
| Данные | PostgreSQL |
| Интерфейс | Telegram Bot |
| LLM | DeepSeek API |

## Текущий статус

Production MVP принят после containment первого retry incident и новой A/B-проверки. Current exact S2 release — `36e149374802263d644cc98e510f6113e1095dae`, mode `public`; Caddy/n8n/PostgreSQL healthy; strict IP TLS с SNI и без SNI `PASS`; единственный публичный application listener — `443`, management SSH — `22`, n8n только loopback `5678`; `1/8` workflow active/published; webhook queue `pending=0` без ошибки; running executions отсутствуют; лимит `2/20`. Подтверждены «один update — один execution — один outbound» и continuity памяти в одной сессии: [[Доказательство_Production_Acceptance_N8NAgents_20260829]]. Каноническая полная сводка: [[CURRENT_STATE_N8NAgents_2026-08-29]].

## Окружения

- Code workspace: local repository `C:\Users\style\Documents\ChatGPT\Агенты`, project `N8NAgents`; reconciled source commit `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9`; remote `origin` не настроен.
- Obsidian: production acceptance predecessor `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba`; текущая AS-IS документация ведется в отдельной handoff branch.
- Production: основной Telegram/memory E2E принят; current S2 и runtime override hashes приведены в [[CURRENT_STATE_N8NAgents_2026-08-29]].

## Активные гейты

1. Интегрировать verified runtime drift в новый reviewed immutable release; `aa087b59...` не объявлять deployed до отдельного rollout/acceptance.
2. Выполнить secret-free reconciliation всех 8 production workflows; семь inactive не активировать автоматически.
3. Backup automation/remote immutability/replication остаются отдельным scope и не входят в MVP acceptance.
4. Секреты, chat IDs и message content не сохраняются в vault, Git или отчетах.
5. Для любой принятой production change соблюдать обязательную цепочку KB governance.

## Известные риски

- Deployed release `36e149...` имеет verified runtime drift: Caddy override и production memory/grant corrections; source reconciliation `aa087b59...` еще не новый release.
- Полное соответствие семи inactive production objects каноническому workflow catalogue не доказано secret-free export.
- Ресурсный запас небольшого VPS требует наблюдения; любые tuning/resource changes — отдельная задача.
- Provider firewall/IPv6 и independent SSH host-key provenance остаются отдельными operational risks, а не основанием переписывать прошедший acceptance.

## Knowledge governance

[[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]] и [[Change_History_N8NAgents]] — обязательные поддерживаемые artifacts. Порядок для каждой change: `change → tests → rollout → production PASS → AS-IS diagrams/descriptions → frontmatter/wikilink/secret checks → Obsidian acceptance`. Planned state хранить отдельно от AS-IS.

## Связанные заметки

- [[MOC_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Источник_Мастер_Промпт_N8NAgents]]
- [[Промпт_N8NAgents_v1_2026-08-25]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]
- [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]
- [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]
- [[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]]
- [[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]]
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]
- [[Доказательство_Production_Acceptance_N8NAgents_20260829]]
- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
- [[Participants_and_Flows_N8NAgents]]
- [[Runtime_Flows_N8NAgents]]
- [[Change_History_N8NAgents]]
- [[Агент_Production_Handoff_N8NAgents]]
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]]
- [[MOC_Все_Проекты]]
