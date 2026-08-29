---
id: "moc-n8nagents-001"
тип: "MOC"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[N8NAgents]]"
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[CURRENT_STATE_N8NAgents_2026-08-29]]"
доказательства:
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["MOC", "n8n", "навигация"]
---

# MOC — N8NAgents

## Проект

- [[N8NAgents]] — цель, стек, статус и активные гейты.
- [[CURRENT_STATE_N8NAgents_2026-08-29]] — каноническая полная AS-IS сводка production, архитектуры, workflows, operations, incidents, scope и commit matrix.

## Работа

- [[Доказательство_Production_Acceptance_N8NAgents_20260829]] — final post-containment production A/B `PASS` без secrets/message content.
- [[Открытые_Задачи_N8NAgents_2026-08-29]] — актуальный backlog после принятого MVP.
- [[Задача_Развертывание_N8NAgents]] — историческая задача развертывания; superseded current state.
- [[Журнал_Автономной_Работы_N8NAgents]] — исторический pre-production execution journal.
- [[Очередь_Ручных_Действий_N8NAgents]] — историческая очередь pre-production blockers.

## Источники и промпты

- [[Источник_Мастер_Промпт_N8NAgents]] — происхождение и контрольная сумма исходного мастер-промпта.
- [[Промпт_N8NAgents_v1_2026-08-25]] — зафиксированная версия операционных ограничений.
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]] — standalone prompt для нового Codex chat.
- [[Матрица_Совместимости_N8NAgents_2026-08-26]] — baseline версий, runtime, proxy, node targets и гейтов совместимости.

## Контекст

- [[Пакет_N8NAgents_Стартовый]] — актуальная точка входа следующего агента.
- [[Агент_Production_Handoff_N8NAgents]] — роль, стоп-условия и knowledge governance.

## Обязательные AS-IS artifacts

- [[Participants_and_Flows_N8NAgents]] — участники, trust boundaries и data flow.
- [[Runtime_Flows_N8NAgents]] — production topology, execution и containment flows.
- [[Change_History_N8NAgents]] — redacted change history и status deployed/source-only.

Обновлять их только по цепочке `change → tests → rollout → production PASS → diagrams/descriptions → link/secret checks → Obsidian acceptance`.

## Текущее доказательство

- [[Доказательство_Production_Acceptance_N8NAgents_20260829]] — актуальное production evidence: final A/B `PASS`, health/TLS/webhook clean, duplicate loop отсутствует.
- [[CURRENT_STATE_N8NAgents_2026-08-29]] — commit/runtime hashes и verified current facts.
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]], [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]], [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]], [[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]], [[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]], [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]] — историческая цепочка до production acceptance.

## Проектные разделы

- `02_Знания/Глоссарий/N8NAgents/` — термины.
- `02_Знания/Доказательства/N8NAgents/` — результаты проверок.
- `03_Агенты/N8NAgents/` — роли агентов.
- `04_Решения/N8NAgents/` — ADR.
- `05_Система/Регламенты/N8NAgents/` — проектные регламенты.
- `05_Система/Схемы/N8NAgents/` — схемы развертывания.

## Навигация

- [[MOC_Все_Проекты]]
