---
id: "evidence-n8nagents-h5-phase-a-recovery-approval-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "Явное разрешение пользователя в текущем диалоге"
  - "[[Доказательство_H4_Phase_A_Wrapper_Stop_Recovery_Plan_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
доказательства: []
теги: ["n8n", "phase-a", "recovery", "approval", "constrained-resume", "swap"]
---

# H5 — отдельное разрешение на constrained Phase A recovery

## Решение пользователя

- Время фиксации: `2026-08-26`, `Europe/Moscow`.
- Пользователь явно одобрил exact commit `bae8c88f7a7d153ffc4a5ae28028045a0a27d319`.
- Точный scope: `phase-a-internal`.
- Выбранная настройка: `SWAP_OPTION=plaintext-2g`.
- H5 — новое distinct approval; H3/f6e0 остаётся историческим и не применяется к recovery release.

## Разрешённый constrained resume

Разрешены только следующие действия по exact commit:

1. partial-state revalidation;
2. новый versioned release и atomic переключение `current`;
3. точная проверка wrapper, hash, `sh -n` и config;
4. internal start, health, listeners и memory checks.

## Явно запрещено

- Не повторять host preparation.
- Не читать и не регенерировать `.env`.
- Не выполнять deletion или rollback.
- Не выходить за прежние exclusions: Caddy, public ports, firewall, IPv6, domains, SSH hardening, owner, 2FA, workflows и credentials.

## Состояние исполнения

H5 сделал частичный progress, но H6 зафиксировал третий `STOP` на archive wrapper до config/app start. Approval H5 immutable/historical для нового release; полный incident и frozen state: [[Доказательство_H6_Third_Stop_Packaging_Incident_N8NAgents_20260826]].

## Сохраняющиеся gates

- H4 `STOP` и partial state сохранены как историческое evidence — [[Доказательство_H4_Phase_A_Wrapper_Stop_Recovery_Plan_N8NAgents_20260826]].
- G1 остаётся **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`** — [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]. H5 не повышает его до `PASS`, не подтверждает fingerprint и не расширяет scope.

## Следующий gate

H6 зафиксировал третий `STOP`, root cause и final reviewed packaging fix. Требуется новый explicit approval final commit, прежде чем продолжать execution.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
