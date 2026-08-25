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

SSH discovery заблокирован на внешней стороне: transport, pinned host key и public-key authentication прошли, но session channel не ответил до `/usr/bin/id`. Server mutations не начаты. Локальная foundation прошла независимое ревью с `GO-LOCAL`; server deployment остаётся `NO-GO`: [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]].

## Окружения

- Локальное: SSH-preflight `PASS`; совместимость/локальная реализация в работе.
- VPS: TCP, pinned host key и public-key authentication подтверждены в A1; remote command не выполнена, discovery `BLOCKED-EXTERNAL`.
- Production: не начат.

## Активные гейты

1. A1 завершена только на transport/authentication; session channel требует provider-console diagnosis.
2. A2 не начинать до снятия внешнего блокера и свежей console-проверки.
3. Server mutations не начаты; hardening требует rollback и console-проверки.
4. Секреты не создаются и не сохраняются в vault, Git или отчетах.

## Известные риски

- Причина неответа session channel на VPS/provider стороне неизвестна.
- Независимая верификация фактического порта и host fingerprint не завершена.
- Неизвестны существующие сервисы, занятые порты и ресурсы VPS.
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
- [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]
- [[MOC_Все_Проекты]]
