---
id: "ctx-n8nagents-start-001"
тип: "пакет_контекста"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Промпт_N8NAgents_v1_2026-08-25]]"
  - "[[CURRENT_STATE_N8NAgents_2026-08-29]]"
доказательства:
  - "[[Доказательство_T1_Local_SSH_Preflight_N8NAgents]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "пакет_контекста", "старт", "безопасность"]
---

# Стартовый пакет контекста N8NAgents

## Назначение

Минимальный безопасный контекст для агента, начинающего работу по проекту.

## Состав

- [[N8NAgents]] — цель, стек, статус и риски.
- [[CURRENT_STATE_N8NAgents_2026-08-29]] — открыть первым: full AS-IS production, architecture, workflow catalogue, operations, incidents, scope и commit matrix.
- [[Доказательство_Production_Acceptance_N8NAgents_20260829]] — final post-containment A/B `PASS`.
- [[Открытые_Задачи_N8NAgents_2026-08-29]] — актуальная незакрытая работа.
- [[Participants_and_Flows_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Change_History_N8NAgents]] — обязательные AS-IS artifacts.
- [[Агент_Production_Handoff_N8NAgents]] — роль, права и стоп-условия нового агента.
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]] — standalone recovery prompt для нового Codex chat.
- [[Задача_Развертывание_N8NAgents]] — исторический DoD раннего развертывания; не источник current state.
- [[Источник_Мастер_Промпт_N8NAgents]] — происхождение и SHA-256 исходного файла.
- [[Промпт_N8NAgents_v1_2026-08-25]] — зафиксированные ограничения и этапы.
- [[Журнал_Автономной_Работы_N8NAgents]] и [[Очередь_Ручных_Действий_N8NAgents]] — исторический pre-production контур.
- [[MOC_N8NAgents]] — навигация по знаниям.
- [[Матрица_Совместимости_N8NAgents_2026-08-26]] — предварительный compatibility baseline; `UNVERIFIED` пункты не разрешают deployment.

## Когда использовать

Перед любым действием по N8NAgents; после каждого существенного этапа пакет должен быть актуализирован evidence без секретов.

## Текущий безопасный режим

Production MVP принят и frozen на exact S2 `36e149374802263d644cc98e510f6113e1095dae` с verified Caddy runtime override и final A/B `PASS`. Все current facts и drift boundaries брать только из [[CURRENT_STATE_N8NAgents_2026-08-29]].

Без новой пользовательской задачи и planner разрешено только читать Git/Obsidian. Production read-only verification допустима, когда она входит в approved plan; mutations, traffic и provider actions — только в отдельном scope с rollback/stop conditions.

Code source reconciliation `aa087b59f0c8b44ee6ebe93ccbd9f996eca49ce9` локален и не равен deployed release. Нельзя автоматически переключать current или активировать остальные workflows.

## Вне контекста и запрещено

- Не читать и не передавать private key, token, credential value, `.env`, encryption key, secret header, chat ID или message content.
- Не выполнять password authentication, `StrictHostKeyChecking=no`, подключение к иному endpoint или принятие изменившегося host key.
- Не активировать семь inactive workflows, не добавлять recipients/tools/reminders и не отправлять traffic без отдельного scope.
- Не выполнять VPS/provider/firewall/SSH/backup/replication/destructive changes из этого пакета.

## Зависимости

- Новая production change требует planner, exact owner/scope/DoD, tests, rollback и fresh verification.
- Обязательная knowledge chain: `change → tests → rollout → production PASS → AS-IS diagrams/descriptions → frontmatter/wikilink/secret checks → Obsidian acceptance`.
- Backup automation, remote immutability и replication остаются отдельным scope.

## Связанные заметки

- [[MOC_N8NAgents]]
- [[CURRENT_STATE_N8NAgents_2026-08-29]]
- [[Промпт_Recovery_Handoff_N8NAgents_2026-08-29]]
- [[MOC_Все_Проекты]]
