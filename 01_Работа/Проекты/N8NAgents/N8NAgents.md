---
id: "proj-n8nagents-001"
тип: "проект"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]"
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

SSH discovery завершён с `PASS` после reboot VPS: минимальная проверка и полный read-only discovery завершились clean, без mutations. Server mutations не начаты. Локальная foundation прошла независимое ревью с `GO-LOCAL`; server deployment остаётся `NO-GO` до review точного deployment plan и отдельного approval: [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]], [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]].

## Окружения

- Локальное: SSH-preflight `PASS`; совместимость/локальная реализация в работе.
- VPS: A2 read-only discovery `PASS`; подтверждены свободные порты и отсутствие целевого стека. RAM ниже предпочтительных 4 GiB, swap отсутствует; firewall/provider firewall и IPv6 policy требуют решения.
- Production: не начат.

## Активные гейты

1. A2 read-only discovery завершён `PASS` после reboot VPS.
2. Перед mutations обязателен review exact deployment plan: команды/объекты, архитектура, downtime и rollback.
3. Server mutations не начаты; firewall/provider firewall и IPv6 policy — обязательные гейты.
4. Секреты не создаются и не сохраняются в vault, Git или отчетах.

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
- [[MOC_Все_Проекты]]
