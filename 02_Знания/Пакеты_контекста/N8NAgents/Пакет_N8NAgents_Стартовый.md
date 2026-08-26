---
id: "ctx-n8nagents-start-001"
тип: "пакет_контекста"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Промпт_N8NAgents_v1_2026-08-25]]"
доказательства:
  - "[[Доказательство_T1_Local_SSH_Preflight_N8NAgents]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]"
теги: ["n8n", "пакет_контекста", "старт", "безопасность"]
---

# Стартовый пакет контекста N8NAgents

## Назначение

Минимальный безопасный контекст для агента, начинающего работу по проекту.

## Состав

- [[N8NAgents]] — цель, стек, статус и риски.
- [[Задача_Развертывание_N8NAgents]] — DoD, стоп-условия и следующий шаг.
- [[Источник_Мастер_Промпт_N8NAgents]] — происхождение и SHA-256 исходного файла.
- [[Промпт_N8NAgents_v1_2026-08-25]] — зафиксированные ограничения и этапы.
- [[Доказательство_T1_Local_SSH_Preflight_N8NAgents]] — redacted evidence успешного локального SSH-preflight.
- [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]] — дословно зафиксированное принятие пользователем ограниченного риска TOFU; не `PASS` fingerprint gate.
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]] — исторический A1 session-channel blocker до reboot VPS.
- [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]] — A2: закреплённый SSH minimal test и полный read-only discovery `PASS`; mutations отсутствуют.
- [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]] — local foundation получила `GO-LOCAL`; server deployment сохраняет `NO-GO`.
- [[Журнал_Автономной_Работы_N8NAgents]] — статус ночной работы, риски и rollback.
- [[Очередь_Ручных_Действий_N8NAgents]] — внешний и владелецский input без секретов.
- [[MOC_N8NAgents]] — навигация по знаниям.
- [[Матрица_Совместимости_N8NAgents_2026-08-26]] — предварительный compatibility baseline; `UNVERIFIED` пункты не разрешают deployment.

## Когда использовать

Перед любым действием по N8NAgents; после каждого существенного этапа пакет должен быть актуализирован evidence без секретов.

## Текущий безопасный режим

T1 local SSH-preflight и A2 read-only discovery завершены `PASS`; A2 прошла после reboot VPS и не внесла mutations. VPS пригоден только как ограниченный пилот: 1.6 GiB RAM ниже предпочтительных 4 GiB, swap отсутствует; provider firewall и IPv6 policy не подтверждены. Server mutations не начаты. Следующий gate — review exact deployment plan с архитектурой, командами/объектами, downtime/rollback и отдельным approval. Границы и ручная очередь: [[Журнал_Автономной_Работы_N8NAgents]] и [[Очередь_Ручных_Действий_N8NAgents]].

Не выходить за подтверждённый SSH scope: иной host/port, password, port scan, глобальный `known_hosts`, `StrictHostKeyChecking=no` или изменившийся/reinstalled host key — Stop. Любые VPS changes требуют completed discovery, architecture, exact command/object list, downtime/rollback, firewall/IPv6 решения и отдельного approval.

Временная official-PyPI проверка закрыла `jsonschema` semantic/metaschema и fixture gates: Draft 2020-12 metaschemas/refs, 6+/3− DeepSeek и 5+/5− tool fixtures — `PASS`; окружение удалено, project tree не изменялся. Это не закрывает Bash (WSL без Linux distribution), Docker/Caddy/PostgreSQL/Compose runtime, import, E2E или restore: см. [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]].

## Вне контекста и запрещено

- Не читать и не передавать содержимое private key.
- Не хранить токены, API keys, пароли, `.env`, ключи шифрования или персональные данные.
- Не выполнять port scan, password authentication, `StrictHostKeyChecking=no`, подключение к другому host/port или принятие изменившегося/reinstalled host key.
- Не выполнять изменения на VPS без отдельного approval gate.

## Зависимости

- Для разрешённого исключения: только точный scope из [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]] и redacted evidence результата; независимая проверка fingerprint и порта остаётся незакрытой.
- Non-secret параметры доменов, DNS, timezone, Telegram и backup-политики — после discovery и в одном согласованном пакете.

## Связанные заметки

- [[MOC_N8NAgents]]
- [[MOC_Все_Проекты]]
