---
id: "context-package-finance-full"
тип: "пакет_контекста"
проект: "Finance"
название: "Пакет Finance — Полный контекст"
создано: "2026-06-01"
обновлено: "2026-06-07"
уверенность: "высокая"
теги: ["пакет_контекста", "finance", "агрегация"]
источники:
  - "[[Источник_README]]"
  - "[[Источник_Продукт_MVP]]"
  - "[[Источник_Текущий_Статус]]"
  - "[[Источник_ADR_0001]]"
  - "[[Источник_Security_Baseline]]"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
  - "[[Кворум_Finance]]"
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
---

# Пакет Finance — Полный контекст

Агрегирующая заметка, собирающая все ключевые ссылки по проекту Finance.

## Проект

- [[Finance]] — главная заметка проекта

## Навигация

- [[MOC_Finance]] — MOC-карта проекта

## Источники

| Источник | Файл |
|----------|------|
| [[Источник_README]] | `README.md` |
| [[Источник_Продукт_MVP]] | `docs/product-mvp.md` |
| [[Источник_Текущий_Статус]] | `docs/current-status.md` |
| [[Источник_ADR_0001]] | `docs/architecture/decision-records/adr-0001-stack-repo-layout.md` |
| [[Источник_Security_Baseline]] | `docs/security/security-baseline.md` |

## Глоссарий

| Термин | Определение |
|--------|------------|
| [[Household]] | Семейное пространство |
| [[Personal_Shared]] | Личное vs совместное |
| [[Transaction]] | Финансовая операция |
| [[Transfer]] | Перевод между счетами |
| [[Capture_Draft]] | OCR черновик |

## Кворум

- [[Кворум_Finance]] — кворум-саммари с высокой уверенностью

## Release context (2026-06-07)

| Область | Статус |
|---------|--------|
| KB branch | `codex/finance-kb-planning-mvp-gpt5` |
| KB previous commit | `b7729f9` |
| Code branch | `codex/finance-planning-mvp-gpt5` |
| Project commit | `5bb7ab493d7c3faa323d711ffa1febb2d94b4f7c` — `fix(planning): support asset allocation targets` |
| Backend release | backend-only `20260607T121851Z-5bb7ab4` в `/opt/finance/releases/20260607T121851Z-5bb7ab4`; `/opt/finance/current` указывает на новый release |
| QA | backend full pytest `228 passed, 4 warnings`; OpenAPI `AllocationTargetType` = `expense_category`, `account`, `asset`; Android gate `BUILD SUCCESSFUL` |
| Backup/migrations | backup SHA256 `adbed3574f02a4fad94c41ac0fa2e18b4abe3e3cd21d527c3bf08cab04c1a8ae`; migrations `20260531_0009 -> 20260606_0010 -> 20260607_0011`, after `20260607_0011 (head)` |
| Delivery boundary | web frontend не деплоился; Android APK delivered locally |

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19). Planning MVP asset-target release `5bb7ab4` развернут backend-only в production 2026-06-07; web frontend не деплоился, Android APK доставлен локально.

## Planning MVP (текущий контекст)

- Вкладка Analytics получила Planning flow: personal/shared scope, income sources, allocations, history/copy, локальные Android reminders.
- Backend/API включает planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, OpenAPI planning endpoints и authz/validation правила.
- Allocation targets поддерживают expense categories, accounts и явный asset target; OpenAPI `AllocationTargetType` enum = `expense_category`, `account`, `asset`.
- Миграция release: `20260607_0011_planning_allocation_asset_target.py`.
- Android flow расширен выбором и созданием asset/investment из planning flow.
- QA evidence по Planning лежит в [[QA_Результаты#Волна 3 Аналитика - Планирование MVP (2026-06-06)]] и [[QA_Фиксы#Волна 4 (2026-06-07)]]. Финальные цифры по asset-target release зафиксированы: backend full pytest `228 passed, 4 warnings`, Android gate `BUILD SUCCESSFUL`, production smoke OK.

## Риски

P1-B02, P1-B03, tag misalignment; asset-target backend release зафиксирован, web frontend не деплоился.
