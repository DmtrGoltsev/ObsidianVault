---
id: "evidence-n8nagents-h4-phase-a-wrapper-stop-recovery-plan-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Доказательство_H3_Phase_A_Reapproval_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "Отчёт исполнения и независимого review в текущем диалоге"
доказательства: []
теги: ["n8n", "phase-a", "wrapper", "stop", "recovery-plan", "reapproval"]
---

# H4 — Phase A остановлен wrapper-валидацией; recovery plan ожидает approval

## Результат одобренного f6e0 retry

Для ранее одобренного commit `f6e0c745ab889c11df1ab83ccf7957534be600cd` успешно пройдены `PASS`: approval, preflight, swap, Docker, deploy-user, release, images и secret-safety gate.

Wrapper остановился на `/bin/sh -n` с `RC=2` **до** config/app start. Поэтому конфигурация приложения, запуск приложения и public exposure не выполнялись.

## Секреты и runtime-состояние

- `.env` остался root-owned с mode `0600`; его содержимое не читалось и не копировалось в vault.
- Не созданы containers и volumes; app listeners и public listeners отсутствуют.
- OOM=`0`, PSI=`0`.
- Частичное безопасное состояние (swap, Docker, deploy-user, release и images) сохранено для recovery; оно не является готовым application deployment.

## Новый release approval gate

Локальный wrapper fix: commit `2240c47`; финальный independently reviewed commit: `bae8c88f7a7d153ffc4a5ae28028045a0a27d319`.

Независимое review имеет статус **`GO` только на запрос нового пользовательского approval**. Это не разрешение на server execution. Approval H3/f6e0 остаётся неизменяемым историческим evidence и не применяется к новому release.

## Сохраняющиеся gates и scope

- G1 остаётся **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`** — [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]. H4 не повышает его до `PASS`, не подтверждает fingerprint и не расширяет scope.
- Не разрешены: Caddy, public ports, firewall, IPv6, domains, SSH hardening, owner, 2FA, workflows и credentials.

## Следующий gate

Пользователь дал отдельный H5 approval commit `bae8c88f7a7d153ffc4a5ae28028045a0a27d319`; constrained resume начат с outcome pending — [[Доказательство_H5_Phase_A_Recovery_Approval_N8NAgents_20260826]]. H4 остаётся историческим wrapper `STOP`, partial state сохраняется.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
