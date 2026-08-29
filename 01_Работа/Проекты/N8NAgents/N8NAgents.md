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

Production A/B E2E завершён с `PASS`: текущее фактическое состояние — `S2`, health clean, `1/8` workflow active, одна опубликованная версия active, webhook queue `pending=0` без ошибки, лимит `2/20`. Подтверждены «один update — один execution — один outbound» и continuity памяти в одной сессии: [[Доказательство_Production_Acceptance_N8NAgents_20260829]]. Reconciliation канонического источника истины продолжается; backup и replication заморожены и не входят в этот acceptance.

## Окружения

- Локальное: SSH-preflight `PASS`; совместимость/локальная реализация в работе.
- VPS: A2 read-only discovery `PASS`; подтверждены свободные порты и отсутствие целевого стека. RAM ниже предпочтительных 4 GiB, swap отсутствует; firewall/provider firewall и IPv6 policy требуют решения.
- Production: основной Telegram/memory E2E принят; состояние `S2`, health и webhook clean.

## Активные гейты

1. Завершить reconciliation канонического источника истины с фактическим production state; старые blockers сохранять как историю, а не как текущий статус.
2. Backup/restore и replication остаются замороженными и требуют отдельного scope, evidence и gate.
3. Секреты не создаются и не сохраняются в vault, Git или отчетах.

## Известные риски

- Независимая верификация фактического порта и host fingerprint не завершена.
- RAM ниже предпочтительных 4 GiB и swap отсутствует; ресурсный риск для пилота.
- Provider firewall и IPv6 policy не подтверждены.
- Не предоставлены обязательные non-secret параметры доменов, DNS, timezone, Telegram и backup-политики.

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
- [[MOC_Все_Проекты]]
