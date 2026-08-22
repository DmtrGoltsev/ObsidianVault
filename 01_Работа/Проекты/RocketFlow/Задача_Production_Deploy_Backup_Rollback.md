---
id: "task-rocketflow-production-deploy-backup-rollback"
тип: "задача"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["docs/65-prod-db-backup-local-runbook.md", "docs/production/rocketflow-cicd-runbook.md", ".github/workflows/rocketflow-prod-rollback.yml"]
доказательства: []
теги: ["задача", "production", "backup", "rollback", "release-gate"]
---

# Задача: Production Deploy Backup и Rollback

## Цель

Закрыть постоянный production release gate: каждый будущий promotion должен иметь проверенный свежий backup и доказанный application rollback без расширения production-привилегий deploy identity.

## Статус

- [ ] Выделена dedicated backup identity с минимально необходимыми правами
- [ ] Fresh backup выполняется и проверяется до любого promotion
- [ ] Application rollback протестирован на staged release artifact
- [ ] Автоматические contract tests backup/rollback gates проходят
- [ ] Sanitized evidence приложен к release record

## Контекст

Для exact SHA из [[ADR_V21_Release_Backup_Waiver]] пользователь принял одноразовый риск rollout без fresh backup. Waiver не распространяется на последующие SHA и не закрывает эту задачу.

Backup-доступ должен принадлежать отдельной identity. Реализация не должна расширять `sudo`-полномочия `rocketdeploy` или превращать deploy identity в владельца DB recovery операций.

## Критерии приёмки

- [ ] Dedicated backup identity создана отдельно от deploy identity и имеет только необходимые backup/read capabilities
- [ ] Workflow создаёт fresh backup до шага promotion
- [ ] До promotion зафиксированы UTC timestamp, размер backup и SHA-256; локальная/удалённая checksum parity подтверждена
- [ ] `pg_restore -l` успешно читает созданный backup
- [ ] Любая ошибка создания, передачи, checksum parity или `pg_restore -l` завершает workflow до promotion
- [ ] Evidence не содержит secrets, credentials, connection strings, production rows или иных production data
- [ ] Application rollback на заранее подготовленный artifact протестирован, включая health/readiness и неизменность Flyway history
- [ ] Contract tests покрывают положительный путь и fail-closed отрицательные сценарии backup/rollback gates
- [ ] Подтверждено отсутствие расширения `rocketdeploy` sudo policy для backup/DB recovery
- [ ] Результат связан с production release record и [[Док_Prod_Deploy_State]]

## Stop / Go

**Stop если:**

- fresh backup нельзя создать или проверить до promotion;
- checksum parity или `pg_restore -l` не подтверждены;
- решение требует расширения `rocketdeploy` sudo privileges;
- sanitized evidence невозможно отделить от secrets или production data.

**Go если:** все критерии приёмки закрыты воспроизводимым evidence и application rollback test прошёл.

## Связанные заметки

- [[RocketFlow]]
- [[ADR_V21_Release_Backup_Waiver]]
- [[Док_Prod_Deploy_State]]
- [[Источник_Бэкап_Runbook]]
- [[Регламент_Деплоя]]
- [[Регламент_CI_CD]]
