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
доказательства: []
теги: ["MOC", "n8n", "навигация"]
---

# MOC — N8NAgents

## Проект

- [[N8NAgents]] — цель, стек, статус и активные гейты.

## Работа

- [[Доказательство_Production_Acceptance_N8NAgents_20260829]] — production A/B E2E `PASS`; redacted evidence, текущий `S2` и границы acceptance.
- [[Задача_Развертывание_N8NAgents]] — активная задача: безопасный старт развертывания.
- [[Журнал_Автономной_Работы_N8NAgents]] — статус этапов, evidence, риски и rollback ночной работы.
- [[Очередь_Ручных_Действий_N8NAgents]] — действия владельца и внешние блокеры без секретов.
- [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]] — независимое `GO-LOCAL` для foundation и отдельный `NO-GO` server deployment.
- [[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]] — plan-level authority Full Delivery v1; K4 outcome заменён R7 STOP.
- [[Доказательство_R7_K4_Recovery_Stop_N8NAgents_20260826]] — K4 STOP: retry cap исчерпан; новый recovery cycle ожидает отдельной авторизации.
- [[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]] — K4R-OFFLINE-v2 `BLOCKED` до validator start; нужен ручной выбор локального Linux sandbox path.

## Источники и промпты

- [[Источник_Мастер_Промпт_N8NAgents]] — происхождение и контрольная сумма исходного мастер-промпта.
- [[Промпт_N8NAgents_v1_2026-08-25]] — зафиксированная версия операционных ограничений.
- [[Матрица_Совместимости_N8NAgents_2026-08-26]] — baseline версий, runtime, proxy, node targets и гейтов совместимости.

## Контекст

- [[Пакет_N8NAgents_Стартовый]] — минимальный пакет для следующего агента.

## Текущее доказательство

- [[Доказательство_Production_Acceptance_N8NAgents_20260829]] — актуальное production evidence: A/B `PASS`, health/webhook clean; source reconciliation остаётся follow-up.
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]] — исторический A1 session-channel blocker до reboot VPS.
- [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]] — A2 read-only discovery `PASS`; server mutations не начаты.
- [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]] — статическое локальное evidence и незакрытые runtime/deployment гейты.

## Проектные разделы

- `02_Знания/Глоссарий/N8NAgents/` — термины.
- `02_Знания/Доказательства/N8NAgents/` — результаты проверок.
- `03_Агенты/N8NAgents/` — роли агентов.
- `04_Решения/N8NAgents/` — ADR.
- `05_Система/Регламенты/N8NAgents/` — проектные регламенты.
- `05_Система/Схемы/N8NAgents/` — схемы развертывания.

## Навигация

- [[MOC_Все_Проекты]]
