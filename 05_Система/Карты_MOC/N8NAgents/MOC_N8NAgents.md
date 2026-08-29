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
  - "[[Архитектура_AS_IS_и_API_Tools_N8NAgents]]"
  - "[[TARGET_Задачи_и_Напоминания_N8NAgents]]"
доказательства:
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
  - "[[Доказательство_Local_Compose_Render_N8NAgents_2026-08-29]]"
  - "[[Доказательство_MVP_Backup_Restore_Receipt_N8NAgents_2026-08-29]]"
теги: ["MOC", "n8n", "навигация"]
---

# MOC — N8NAgents

## Проект

- [[N8NAgents]] — цель, стек, статус и активные гейты.
- [[CURRENT_STATE_N8NAgents_2026-08-29]] — каноническая полная AS-IS сводка production, архитектуры, workflows, operations, incidents, scope и commit matrix.
- [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] — полный canonical human/agent-readable документ: verified production topology, каталог 8 workflows, runtime/data/memory flows, текущие ограничения и отдельно размеченная TARGET API-tools архитектура.
- [[TARGET_Задачи_и_Напоминания_N8NAgents]] — утверждённый **DESIGN_APPROVED / TARGET / NOT_DEPLOYED** дизайн задач и напоминаний: все расписания, `Europe/Moscow`, quiet `00:00–06:00`, подтверждаемый перенос с пользовательским cadence, UX/contracts, Task→Occurrence→Delivery, trust/policy, rollout и acceptance. Не является AS-IS.

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

## Импортированная source documentation

Полный human/agent-readable inventory из source final GO `09824a6e...` перенесён в canonical vault. `source_path`, commit/tree, дата импорта, point-in-time status и redaction review закреплены во frontmatter каждой заметки. Source hygiene predecessor `d163606a...` завершён финальным local review commit `dd9e10a9b9b51e33761971e517a61a6bd9fa899c`, tree `1d9dc11150e87846937b622748c95877f4823128`, parent `d163606a...`; два независимых `GO`, `P0=0`, `P1=0`. Source repository не имеет `origin`: `dd9e10a...` имеет статус `LOCAL_ONLY / NOT_DEPLOYED`, не upstream-published. Source paths — только provenance; current runtime facts определяют [[CURRENT_STATE_N8NAgents_2026-08-29]] и [[Архитектура_AS_IS_и_API_Tools_N8NAgents]].

### Repository и архитектурные snapshots

- [[Источник_Repository_Overview_N8NAgents_2026-08-29]]
- [[Источник_Architecture_and_Trust_Boundaries_N8NAgents_2026-08-29]] — historical source snapshot; не заменяет canonical architecture.
- [[Источник_AS_IS_and_API_Tools_N8NAgents_2026-08-29]] — полный historical source snapshot; не второй AS-IS канон.
- [[Источник_Compatibility_Matrix_Source_2026-08-29]]
- [[Источник_Credential_Binding_N8NAgents_2026-08-29]]
- [[Источник_Threat_Model_N8NAgents_2026-08-29]]
- [[Источник_Version_Digest_Inventory_N8NAgents_2026-08-29]] — production digests `UNKNOWN`; exact values только local/parity pins.

### Evidence, history и operations

- [[Доказательство_Local_Compose_Render_N8NAgents_2026-08-29]] — redacted loss-preserving local/parity Compose render; raw bytes bound by SHA-256.
- [[Доказательство_MVP_Backup_Restore_Receipt_N8NAgents_2026-08-29]] — redacted field-complete backup/isolated-restore receipt; raw bytes bound by SHA-256.
- [[Исторический_Манифест_Phase_A_Deploy_Rollback_N8NAgents]]
- [[Исторический_Full_Delivery_Scope_v1_N8NAgents]]
- [[Доказательство_Local_Verification_2026-08-27_N8NAgents]]
- [[Исторические_Manual_Inputs_N8NAgents]]
- [[Матрица_Верификации_N8NAgents_2026-08-29]]
- [[Регламент_Backup_Restore_N8NAgents]]
- [[Регламент_Operations_N8NAgents]]
- [[Регламент_Security_N8NAgents]]
- [[Лаборатория_Local_Docker_N8NAgents]]
- [[Регламент_Local_Secret_Leaves_N8NAgents]]

Production acceptance source полностью merged в [[Доказательство_Production_Acceptance_N8NAgents_20260829]], а source discovery — в [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]].

### Workflow specifications

- [[Workflow_Artifacts_and_Import_Gate]]
- [[00_Import_and_Compatibility_Gate]]
- [[01_Telegram_Assistant]]
- [[02_Tool_Subworkflows]]
- [[03_Reminder_Dispatcher]]
- [[04_Error_Handler]]

## Контекст

- [[Пакет_N8NAgents_Стартовый]] — актуальная точка входа следующего агента.
- [[Агент_Production_Handoff_N8NAgents]] — роль, стоп-условия и knowledge governance.

## Обязательные AS-IS artifacts

- [[Participants_and_Flows_N8NAgents]] — участники, trust boundaries и data flow.
- [[Runtime_Flows_N8NAgents]] — production topology, execution и containment flows.
- [[Change_History_N8NAgents]] — redacted change history и status deployed/source-only.
- [[Архитектура_AS_IS_и_API_Tools_N8NAgents]] — полный AS-IS catalogue/capabilities/limits и отдельный TARGET API-tools contract.

Все четыре artifacts обновлять только по цепочке `change → tests → rollout → production PASS → diagrams/descriptions → link/secret checks → Obsidian acceptance`. Planned state держать отдельно; failed rollout или rollback сохраняет last verified AS-IS до нового production verification `PASS`.

TARGET-схемы, включая утверждённый, но не развёрнутый [[TARGET_Задачи_и_Напоминания_N8NAgents]], не переносятся в обязательные AS-IS artifacts до production verification `PASS`. После PASS участники, потоки и их описания обновляются во всех четырёх обязательных artifacts одной согласованной KB-транзакцией.

Вся human/agent-readable документация N8NAgents канонична только в этом vault. Source repository предназначен для machine-consumed code/config/tests/contracts и не является запасным каноном документации.

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
