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
  - "[[Архитектура_AS_IS_и_API_Tools_N8NAgents]]"
  - "[[Источник_Repository_Overview_N8NAgents_2026-08-29]]"
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

Production MVP принят после containment первого retry incident и новой A/B-проверки. Current exact S2 release — `36e149374802263d644cc98e510f6113e1095dae`, mode `public`; Caddy/n8n/PostgreSQL healthy; strict IP TLS с SNI и без SNI `PASS`; единственный публичный application listener — `443`, management SSH — `22`, n8n только loopback `5678`; `1/8` workflow active/published; webhook queue `pending=0` без ошибки; running executions отсутствуют. Acceptance checkpoint завершился на `2/20`, более поздний redacted cumulative snapshot показал `4/20`. Подтверждены «один update — один execution — один outbound» и continuity памяти в одной сессии: [[Доказательство_Production_Acceptance_N8NAgents_20260829]]. Каноническая полная сводка: [[CURRENT_STATE_N8NAgents_2026-08-29]], полная архитектура: [[Архитектура_AS_IS_и_API_Tools_N8NAgents]].

## Окружения

- Code workspace: local repository `C:\Users\style\Documents\ChatGPT\Агенты`, project `N8NAgents`; final local reviewed source `dd9e10a9b9b51e33761971e517a61a6bd9fa899c`, tree `1d9dc11150e87846937b622748c95877f4823128`, parent `d163606a...`. Source repository не имеет `origin`; commit `LOCAL_ONLY / NOT_DEPLOYED`, не upstream-published. Human/agent-readable документация канонична только в Obsidian; source содержит machine-consumed code/config/tests/contracts и zero tracked human-readable docs.
- Obsidian: production acceptance predecessor `b037cd23690b35ded8e2a0c5c9e2473a53f4fbba`; текущая AS-IS документация ведется в отдельной handoff branch.
- Production: основной Telegram/memory E2E принят; current S2 и runtime override hashes приведены в [[CURRENT_STATE_N8NAgents_2026-08-29]].

## Активные гейты

1. Интегрировать verified runtime drift в новый reviewed immutable release; `aa087b59...` не объявлять deployed до отдельного rollout/acceptance.
2. Выполнить secret-free reconciliation всех 8 production workflows; семь inactive не активировать автоматически.
3. Backup automation/remote immutability/replication остаются отдельным scope и не входят в MVP acceptance.
4. Секреты, chat IDs и message content не сохраняются в vault, Git или отчетах.
5. Для любой принятой production change соблюдать обязательную цепочку KB governance.

## Известные риски

- Deployed release `36e149...` имеет verified runtime drift: Caddy override и production memory/grant corrections; final local reviewed source `dd9e10a...` не deployed. Fresh VPS revalidation после source review не выполнялась; residual `P2` по `dash` signal label остается fail-closed через `RC79`/rollback/cleanup.
- Полное соответствие семи inactive production objects каноническому workflow catalogue не доказано secret-free export.
- Ресурсный запас небольшого VPS требует наблюдения; любые tuning/resource changes — отдельная задача.
- Provider firewall/IPv6 и independent SSH host-key provenance остаются отдельными operational risks, а не основанием переписывать прошедший acceptance.

## Knowledge governance

[[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Change_History_N8NAgents]] и [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] — обязательные поддерживаемые artifacts. Порядок для каждой change: `change → tests → rollout → production PASS → AS-IS diagrams/descriptions → frontmatter/wikilink/secret checks → Obsidian acceptance`. Planned state хранить отдельно; failed rollout или rollback сохраняет last verified AS-IS до нового production `PASS`.

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
- [[Архитектура_AS_IS_и_API_Tools_N8NAgents]]
- [[Источник_Repository_Overview_N8NAgents_2026-08-29]]
- [[Открытые_Задачи_N8NAgents_2026-08-29]]
- [[Participants_and_Flows_N8NAgents]]
- [[Runtime_Flows_N8NAgents]]
- [[Change_History_N8NAgents]]
- [[Агент_Production_Handoff_N8NAgents]]
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]]
- [[MOC_Все_Проекты]]
