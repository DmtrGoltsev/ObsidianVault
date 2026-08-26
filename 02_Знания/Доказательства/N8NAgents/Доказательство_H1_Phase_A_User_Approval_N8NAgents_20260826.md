---
id: "evidence-n8nagents-h1-phase-a-user-approval-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "Явное разрешение пользователя в текущем диалоге"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
доказательства: []
теги: ["n8n", "phase-a", "approval", "swap", "scoped-mutation"]
---

# H1 — явное разрешение пользователя на Phase A

## Решение пользователя

- Время фиксации: `2026-08-26`, `Europe/Moscow`.
- Пользователь дословно подтвердил: `Разрешаю Phase A, plaintext-2g`.
- Утверждённый commit deployment plan: `d1703bdfbdb183836afe7d75c871938ca8a9f196`.
- Точный scope: `phase-a-internal`.
- Выбранная настройка: `SWAP_OPTION=plaintext-2g`.

## Разрешённый результат

Разрешено начать только внутренний Phase A из утверждённого commit: подготовить Docker/Compose и служебного пользователя, затем запустить PostgreSQL и n8n, доступные только через `127.0.0.1`.

## Явные исключения из разрешения

Не разрешены: Caddy, публичные порты, firewall, IPv6, domains, SSH hardening, owner account, 2FA, workflows и credentials. Эти темы сохраняют собственные gates и не могут считаться одобренными данным решением.

## Состояние исполнения и доказательства

- Console recovery уже был продемонстрирован до этого approval: A2 выполнен после reboot и завершил read-only discovery с `PASS` — [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]].
- Последующий preflight остановил Phase A до всех mutations; исходный approval не даёт права исполнять переработанный plan. Полный outcome: [[Доказательство_H2_Phase_A_Stop_Preflight_N8NAgents_20260826]].
- В эту заметку не копируются IP-адреса, host-key fingerprints, секреты или иные служебные идентификаторы.

## TOFU

[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]] остаётся статусом **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`**. H1 не повышает его до `PASS`, не подтверждает fingerprint и не расширяет его прежний узкий read-only scope на Phase A или любые новые SSH-операции.

## Следующий gate

H2 зафиксировал `STOP — PRE-MUTATION`; требуется новый явный approval финального reviewed commit, прежде чем вновь начинать execution. До этого нельзя заявлять, что PostgreSQL, n8n или swap успешно применены.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
