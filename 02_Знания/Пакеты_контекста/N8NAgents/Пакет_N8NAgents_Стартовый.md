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
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]] — A1: transport/authentication `PASS`, session channel `BLOCKED-EXTERNAL`; remote command/mutations отсутствуют.
- [[Журнал_Автономной_Работы_N8NAgents]] — статус ночной работы, риски и rollback.
- [[Очередь_Ручных_Действий_N8NAgents]] — внешний и владелецский input без секретов.
- [[MOC_N8NAgents]] — навигация по знаниям.

## Когда использовать

Перед любым действием по N8NAgents; после каждого существенного этапа пакет должен быть актуализирован evidence без секретов.

## Текущий безопасный режим

T1 local SSH-preflight завершён со статусом `PASS`. В A1 transport, pinned host key и public-key authentication также `PASS`, но server прекратил отвечать до `/usr/bin/id`; exit `255`. Поэтому SSH discovery — **`BLOCKED-EXTERNAL`**, A2 не начата, server mutations не начаты. Границы, rollback и ручная очередь: [[Журнал_Автономной_Работы_N8NAgents]] и [[Очередь_Ручных_Действий_N8NAgents]].

Не повторять SSH до provider-console diagnosis session-channel failure. Если требуется иной host/port, password, port scan, глобальный `known_hosts`, `StrictHostKeyChecking=no` либо mutation — Stop. Любые VPS changes требуют completed discovery, architecture, exact command/object list, downtime/rollback и fresh console check.

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
