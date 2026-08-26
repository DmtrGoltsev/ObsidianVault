---
id: "evidence-n8nagents-r7-k4-recovery-stop-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "Отчёты исполнителя и независимого reviewer в текущем цикле K4"
  - "[[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
доказательства: []
теги: ["n8n", "k4", "incident", "recovery", "stop", "linux", "packaging", "governance"]
---

# R7 — K4 recovery: исчерпанный лимит попыток, без VPS mutation

## Итог

K4 остановлен. Лимит двух попыток этого gate исчерпан; третья попытка не разрешена. Текущий статус: **`WAITING-USER-AUTHORIZATION`** для будущего отдельно названного gate после нового планирования, corrective commit, fresh Linux QA и независимого review. Для какого-либо exact commit сейчас нет авторизации на remote execution.

## Хронология и факты

1. **K4 retry 1** остановлен до записи на VPS: неверный вызов `swapon` не прошёл на установленной версии util-linux. Это pre-write STOP; production state не менялся.
2. Linux R1 установил точную причину следующего сбоя: реальный symlink с mode `l777` был ошибочно выбран выражением `-perm/022`; такой результат не доказывает небезопасность целевых production paths.
3. Corrective commit `b3020ee` остановлен с P1-замечаниями и соответствующими evidence; он не получил допуск к remote execution.
4. Единственная локальная повторная проверка corrective цепочки, commit `11974a33`, завершилась **`STOP / CHANGES_REQUIRED`**. Reviewer зафиксировал блокеры; поэтому K4 retry 2 не получил успешного acceptance и retry cap исчерпан.

## Package evidence, ограниченное локальным контуром

Детерминированный package evidence для локальной проверки: archive SHA-256 `9c3b793…`, size `84246` bytes, `91` entries, `75` regular files, `0` symlinks. Сопоставляющие transcripts сохранены в execution/review evidence, но не являются доказательством передачи или распаковки на VPS.

## Что не доказано

- Не подтверждены никакие K4 remote write, transfer, extraction, immutable records, `current` switch или запуск приложения.
- Утверждение «VPS unchanged» — **только attestation исполнителя**, не независимое наблюдение в этом R7 evidence.
- Не выполнены и не закрыты runtime, containers, PostgreSQL, n8n, Caddy, public edge, firewall, SSH hardening, workflows, backup, monitoring, E2E и restore.
- Не изменены ручные gates: secrets, DNS/provider UI, owner/2FA, destructive/data-loss, новые получатели, дополнительные расходы и расширение scope.

## Следующее ручное действие

Сначала владелец должен явно авторизовать **расширенный offline recovery budget / новый corrective cycle**. Только после нового планирования, нового corrective commit, свежего Linux QA и независимого review может быть предложен новый, отдельно названный remote gate с exact reviewed commit и собственным attempt budget. Это не авторизация remote execution сейчас.

## TOFU и границы

`[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]` остаётся **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`**. R7 не подтверждает host fingerprint, не расширяет TOFU scope и не отменяет security gates.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Доказательство_H7_Full_Delivery_Plan_Approval_N8NAgents_20260826]]
- [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]
