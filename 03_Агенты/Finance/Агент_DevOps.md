---
id: "agent-finance-devops"
тип: "агент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["агент", "finance", "devops", "infra"]
ссылки:
  - "[[MOC_Finance]]"
---

# Агент DevOps — Finance

## Зона ответственности

Инфраструктура и деплой: HexCore (45.10.110.42), nginx reverse proxy,
systemd services, PostgreSQL 16, backup/restore, deploy runbook.

## Стек

- Linux (Ubuntu), systemd, nginx
- PostgreSQL 16, pg_dump/pg_restore
- Shell scripts (deploy, backup)

## Права на решения

- Изменение `ops/` (scripts, configs, cron)
- Изменение `docs/deploy/` (runbook, procedures)

## Активные задачи

- [ ] Deploy runbook: step-by-step production
- [ ] Automated backup (daily pg_dump)
- [ ] Restore procedure verification

## Связанные заметки

- [[MOC_Finance]]
- [[Finance]]
