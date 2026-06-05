---
id: "task-finance-wave1-mvp"
тип: "задача"
проект: "Finance"
статус: "выполнено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["задача", "finance", "mvp", "wave1"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Доказательство_Production_GO]]"
---

# Задача: Wave 1 — реализация MVP

## Цель

Реализовать и вывести в production MVP личных финансов: backend API, PWA-клиент, Android-приложение, auth, accounts, categories, transactions, reports.

## Контекст

- **Commit**: `808f727`
- **Production GO**: 2026-05-19
- Стек: Python/FastAPI backend, React/Vite PWA, Kotlin/Jetpack Compose Android, PostgreSQL 16
- Ограничения: plain HTTP (PWA service worker ограничен без HTTPS), import/bank API/SMS/push вне scope
- См. `docs/current-status.md`

## Definition of Done

- [x] Backend API: auth, accounts, categories, transactions, reports
- [x] PWA-клиент: browser + iPhone
- [x] Android-приложение: базовый функционал
- [x] Functional checks passed (Android final GO, PWA/iPhone final GO)
- [x] Production deployment на HexCore

## Статус

**Выполнено** — 2026-05-19. Functional GO получен, MVP развернут в production.

## Доказательства

- [[Доказательство_Production_GO]] — финальный отчет
- `MVP_EVIDENCE/prod-qa-20260519-040640/android-final/`
- `MVP_EVIDENCE/prod-qa-20260519-040710/pwa-iphone-final/`

## Связанные заметки

- [[Задача_Production_Deploy]]
- [[Задача_Capture_Drafts_OCR]]
- [[Задача_Wave2_Backlog]]
