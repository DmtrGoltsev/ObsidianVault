---
id: "src-prod-runbook"
тип: "источник"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["docs/60-hexcore-prod-runbook.md"]
доказательства: ["Док_Prod_Deploy_State", "Док_Production_Rollout_20260810"]
теги: ["документация", "production", "runbook"]
---

# Источник: Продакшен Runbook

## Путь

`docs/60-hexcore-prod-runbook.md`

## Роль в проекте

Инструкция по эксплуатации production-окружения на [[HexCore]]: развёртывание, мониторинг, откат, диагностика.

## Краткое содержание

Процедуры деплоя бэкенда на HexCore (Java jar под systemd), обновления web-статики (Nginx), проверки состояния БД (текущий production: PostgreSQL 18.4 по [[Док_Production_Rollout_20260810]]). Команды для перезапуска, просмотра логов, отката. Фактический workflow: `backend-hexcore-prod-deploy.yml`. Docker/GHCR deploy не закрыт и остаётся open gate. Добавлена ссылка на [[Источник_Бэкап_Runbook|backup runbook]] для процедур резервного копирования.

## Статус актуальности

Актуализирован на 2026-08-10 после production rollout и проверки версии БД.

## Связанные заметки

- [[Регламент_Деплоя]] — регламент на основе runbook
- [[HexCore]] — целевой сервер
- [[Док_Prod_Deploy_State]] — фактический deploy state
- [[Агент_DevOps]] — ответственный
