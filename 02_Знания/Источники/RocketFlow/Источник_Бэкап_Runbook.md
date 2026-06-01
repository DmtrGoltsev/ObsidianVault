---
id: "src-backup-runbook"
тип: "источник"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
источники: ["docs/65-prod-db-backup-local-runbook.md"]
доказательства: []
теги: ["документация", "production", "backup", "runbook"]
---

# Источник: Бэкап Runbook

## Путь

`docs/65-prod-db-backup-local-runbook.md`

## Роль в проекте

Runbook скачивания production backup базы данных через SSH/SCP на локальную машину для диагностики и восстановления.

## Краткое содержание

Пошаговая инструкция по созданию и скачиванию дампа production БД PostgreSQL 16 с [[HexCore]] через SSH/SCP. Включает команды для дампа, сжатия, передачи и восстановления локально. Связанный скрипт: `Invoke-ProdPostgresBackupDownload.ps1`.

## Статус актуальности

Актуален.

## Связанные заметки

- [[Источник_Продакшен_Runbook]] — основной production runbook
- [[HexCore]] — production-сервер
- [[Агент_DevOps]] — ответственный
