---
id: "evidence-n8nagents-h6-third-stop-packaging-incident-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Доказательство_H5_Phase_A_Recovery_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "Отчёт исполнения, incident review и независимого review в текущем диалоге"
доказательства: []
теги: ["n8n", "phase-a", "third-stop", "packaging", "incident", "release", "reapproval"]
---

# H6 — третий STOP: packaging incident разрешён, состояние заморожено

## Частичный результат H5

По H5/`bae8c88f7a7d153ffc4a5ae28028045a0a27d319` созданы approval record, archive и non-current release. `current` остался на `f6e0`. Приложение, containers и volumes отсутствуют; `.env` не затронут.

## Третий STOP

Exact remote archive wrapper имеет CRLF, hash `8ec`, размер `1868` и `/bin/sh -n` `RC=2`. Это не соответствует canonical wrapper: hash `ffd5`, размер `1820`, LF и `PASS`. STOP произошёл до config/app start; state заморожен.

## Incident: mistaken target и его разрешение

- Ошибочный investigator использовал `45.10.110.42` и general `known_hosts`.
- Correct target использует literal `154.59.110.121`, `-F none` и project-scoped `known_hosts`; это подтвердило target `n8n-agents` и exact state.
- Identity reviewer подтвердил SSH-path. Mapping текущей provider live panel с target остаётся unavailable residual; public-edge работа отложена и этим не разблокируется.

Это не повышает G1 выше **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`** и не подтверждает fingerprint — [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].

## Root cause и исправление packaging

Root cause: уязвимый Windows-вызов `git archive <commit> .` из subtree. Локальный bad archive совпал с remote, поэтому расхождение не являлось transport-only проблемой.

Безопасное packaging исправлено commit `4e7737`; final independently reviewed commit: `9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b`.

Redacted deterministic archive evidence final release: SHA `4cbaa388…`, `83` entries, `68` regular, `0` blob mismatches; wrapper `ffd5` / `1820` / `0` CR.

## Новый approval gate

Независимое review имеет статус **`GO` только на запрос нового explicit approval** commit `9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b`. H5 approval immutable/historical для нового release и не разрешает server execution этого commit.

## Сохраняющиеся ограничения

State остаётся frozen. Не разрешены Caddy, public ports, firewall, IPv6, domains, SSH hardening, owner, 2FA, workflows и credentials. Public-edge остаётся deferred.

## Следующий gate

Получить новый явный approval final commit `9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b`. До этого packaging/release execution не выполнять.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
