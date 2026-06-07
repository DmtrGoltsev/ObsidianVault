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
| KB baseline | `56fc7e3` — Planning MVP delivery записан, но найден недосинхрон MOC/package/QA fixes |
| Code branch | `codex/finance-planning-mvp-gpt5` |
| Code HEAD | `0780944` — `feat(finance): add planning MVP` |
| Code WIP поверх HEAD | незакоммиченные изменения: явный Planning `targetType=asset`, OpenAPI/backend/Android sync, миграция `20260607_0011_planning_allocation_asset_target.py`, `.gitignore` hygiene для raw QA artifacts |
| Deploy/финальный QA | не утверждено в KB; ожидается финальная QA/deploy-сводка от оркестратора/QA |

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19). Planning MVP расширяется на ветке `codex/finance-planning-mvp-gpt5`; текущий asset-target WIP документируется без заявления о production deploy success.

## Planning MVP (текущий контекст)

- Вкладка Analytics получила Planning flow: personal/shared scope, income sources, allocations, history/copy, локальные Android reminders.
- Backend/API включает planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, OpenAPI planning endpoints и authz/validation правила.
- Allocation targets поддерживают expense categories, accounts, assets, investments; текущий WIP синхронизирует явный `targetType=asset` для asset/investment целей на backend/OpenAPI/Android.
- Новая миграция WIP: `20260607_0011_planning_allocation_asset_target.py`.
- Android flow расширен выбором и созданием asset/investment из planning flow.
- QA evidence по Planning лежит в [[QA_Результаты#Волна 3 Аналитика - Планирование MVP (2026-06-06)]] и [[QA_Фиксы#Волна 4 (2026-06-07)]]. Финальные цифры по расширенному asset-target WIP пока не зафиксированы.

## Риски

P1-B02, P1-B03, tag misalignment; Planning asset-target WIP требует финальной QA/deploy фиксации после завершения оркестратором/QA.
