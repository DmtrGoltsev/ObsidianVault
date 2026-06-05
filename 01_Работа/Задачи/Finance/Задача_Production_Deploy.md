---
id: "task-finance-production-deploy"
тип: "задача"
проект: "Finance"
статус: "выполнено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["задача", "finance", "deploy", "production"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Доказательство_Production_GO]]"
---

# Задача: Production Deploy

## Цель

Развернуть MVP на production-сервере HexCore (45.10.110.42) с backend, frontend и PostgreSQL.

## Контекст

### Инфраструктура

| Компонент | Путь / Детали |
|---|---|
| Сервер | HexCore, `45.10.110.42` |
| Backend | `/opt/finance/current`, systemd service |
| Frontend | `/var/www/finance/current`, nginx |
| Database | PostgreSQL 16, database `finance` |
| Frontend URL | `http://<host>/finance/` |
| Backend API | `http://<host>/finance-api` |
| Commit | `808f727` |

### Ограничения

- Plain HTTP (нет HTTPS/domain) — PWA service worker ограничен
- Tag alignment: `v0.1.0-mvp` → требуется owner approval для retag

## Definition of Done

- [x] Backend развернут и работает через systemd
- [x] Frontend развернут и обслуживается nginx
- [x] PostgreSQL 16, база `finance` создана
- [x] API endpoint доступен: `/finance-api`
- [x] Frontend доступен: `/finance/`
- [x] Functional checks passed

## Статус

**Выполнено** — production развернут 2026-05-19.

## Доказательства

- [[Доказательство_Production_GO]]
- `MVP_EVIDENCE/prod-final-20260519/FINAL_PROD_MVP_REPORT.md`

## Связанные заметки

- [[Задача_Wave1_MVP]]
- [[Задача_Wave2_Backlog]]
