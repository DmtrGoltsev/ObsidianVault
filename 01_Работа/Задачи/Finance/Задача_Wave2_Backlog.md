---
id: "task-finance-wave2-backlog"
тип: "задача"
проект: "Finance"
статус: "черновик"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["задача", "finance", "wave2", "planning"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Задача_Wave1_MVP]]"
---

# Задача: Wave 2 Backlog

## Цель

Расширение MVP до полноценного продукта: auth/sessions, households, privacy flows, reports, transfers, export/delete, клиентские приложения (PWA + Android), backup/restore, security evidence.

## Контекст

- **Источник**: `docs/planning/wave-2-backlog.md` — 20 тикетов (W2-00..W2-19)
- **Service slice**: `docs/planning/wave-2-service-slice-plan.md` — ближайший slice: accounts/categories
- ADR-0001 принят: contract-first monorepo, FastAPI, React/Vite, Kotlin/Compose
- MVP release: **Hold** до закрытия всех P0/P1 gate

### Открытые вопросы

- **P1-B02**: rate-limit значения, export file TTL — требует Product/Security approval
- **P1-B03**: public launch, retention SLA, backup deletion promise, jurisdiction — вне engineering authority
- HTTPS/domain: PWA service worker требует HTTPS для полной работы
- Security GO: CVE scans, log redaction, dependency audit
- CI/CD: pipeline для тестов, evidence, деплоя
- Backup/restore: runbook + restore drill evidence

## Definition of Done

- [ ] Все W2-00..W2-19 тикеты реализованы с evidence
- [ ] P1-B02 и P1-B03 закрыты или имеют owner
- [ ] MVP release GO получен

## Статус

**Черновик** — планирование завершено, ближайший шаг: accounts/categories service slice.

## Доказательства

- `docs/planning/wave-2-backlog.md`
- `docs/planning/wave-2-service-slice-plan.md`

## Связанные заметки

- [[Задача_Wave1_MVP]]
- [[Задача_Production_Deploy]]
