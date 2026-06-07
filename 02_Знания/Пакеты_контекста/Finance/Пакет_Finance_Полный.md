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
| Previous project commit | `5bb7ab493d7c3faa323d711ffa1febb2d94b4f7c` — `fix(planning): support asset allocation targets` |
| Current release scope | asset categories source of truth; Analytics investments/capital structure; Categories scope/edit icon; Planning income/allocation polish; backend `reportMode=personal` |
| Backend/API | asset-categories endpoints; migration `20260607_0012`; no stale totals from deleted accounts |
| QA | backend latest `238 passed, 8 warnings`; fixtures `8 passed`; Android build `BUILD SUCCESSFUL`; APK SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26` |
| Delivery boundary | current production deploy `PENDING` until release agent completes; не утверждать production deploy текущей поставки |

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19). Текущая поставка 2026-06-07 по asset categories + Analytics/Planning polish прошла QA evidence, но production deploy остаётся `PENDING` до завершения release agent.

## Asset categories + Analytics/Planning polish (текущий контекст)

- Asset categories — source of truth: `manualAmount` для пустых категорий, `isInvestment`, `assetType`, связь `account.assetCategoryId`; удалённые счета не дают stale totals.
- Backend/API: `reportMode=personal`, asset-categories endpoints, миграция `20260607_0012`.
- Analytics: investments metric; capital structure отображается только в Analytics.
- Categories: создание учитывает scope `personal`/`household`; редактирование через edit icon.
- Planning: income day = день месяца; income form скрыта за Add; новые allocations выбирают expense category или investment asset category, без account target; history text уточнён.
- QA evidence: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`, APK SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26`.
- Release boundary: production deploy текущей поставки pending, пока release agent не завершит деплой.

## Planning MVP (текущий контекст)

- Вкладка Analytics получила Planning flow: personal/shared scope, income sources, allocations, history/copy, локальные Android reminders.
- Backend/API включает planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, OpenAPI planning endpoints и authz/validation правила.
- Allocation targets для новых allocations поддерживают expense categories и investment asset categories; account target больше не предлагается для новых allocations.
- Миграция release: `20260607_0011_planning_allocation_asset_target.py`.
- Android flow расширен выбором и созданием asset/investment из planning flow.
- QA evidence по Planning лежит в [[QA_Результаты#Волна 3 Аналитика - Планирование MVP (2026-06-06)]], [[QA_Фиксы#Волна 4 (2026-06-07)]] и [[QA_Фиксы#Волна 5 (2026-06-07)]]. Актуальные цифры текущей поставки: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`.

## Риски

P1-B02, P1-B03, tag misalignment; текущий production deploy pending до release agent.
