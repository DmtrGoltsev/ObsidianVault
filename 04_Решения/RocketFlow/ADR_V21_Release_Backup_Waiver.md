---
id: "adr-v21-release-backup-waiver-2026-08-22"
тип: "решение"
статус: "утверждено"
проект: "RocketFlow"
владелец: "пользователь"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["пользовательское решение 2026-08-22", "docs/production/rocketflow-cicd-runbook.md"]
доказательства: []
теги: ["adr", "v21", "production", "backup", "waiver", "risk-acceptance"]
---

# ADR: V21 Release Backup Waiver

## Контекст

Стандартный production rollout должен иметь свежую и проверенную DB recovery point до promotion. Для текущего V21 release candidate такой recovery point отсутствует.

Application rollback artifact V20 существует и может вернуть приложение на совместимый V20 binary, но application rollback не восстанавливает состояние базы данных и не заменяет DB backup.

## Решение

Пользователь 2026-08-22 явно разрешил провести текущий rollout без fresh backup исключительно для exact source SHA:

`50a63270ae094fe08ee57b945be0930cb1115dfe`

Риск отсутствия DB recovery point принят осознанно. Доступный V20 artifact является только application rollback path; DB recovery для этого rollout не гарантирован.

## Ограничения решения

- Waiver одноразовый и не является precedent или общей политикой RocketFlow.
- Решение действительно только для exact SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`.
- При любом изменении SHA решение автоматически недействительно, даже если функциональный diff считается эквивалентным.
- Новый SHA требует fresh backup по стандартному gate либо нового явного решения пользователя.
- Решение не разрешает DB downgrade, repair, restore или расширение production-привилегий.
- Этот ADR фиксирует разрешение и принятый риск, но не является доказательством выполненного deploy.

## Последствия

- При необратимой проблеме данных после promotion восстановление к состоянию непосредственно перед rollout может быть невозможно.
- Application rollback может вернуть V20 binary на forward-compatible V21 schema, но не откатывает миграции или данные.
- Постоянный backup/rollback gate остаётся открытой задачей: [[Задача_Production_Deploy_Backup_Rollback]].

## Связанные заметки

- [[RocketFlow]]
- [[Задача_Production_Deploy_Backup_Rollback]]
- [[Док_Prod_Deploy_State]]
- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
