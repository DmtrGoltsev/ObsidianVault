---
id: "context-package-finance-full"
тип: "пакет_контекста"
проект: "Finance"
название: "Пакет Finance — Полный контекст"
создано: "2026-06-01"
обновлено: "2026-06-08"
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
  - "[[Док_Release_Planning_MVP_20260607]]"
  - "[[Карта_Пользовательских_Путей_Finance]]"
  - "[[Единый_Документ_Критики_И_План_NewDis]]"
---

# Пакет Finance — Полный контекст

Агрегирующая заметка, собирающая все ключевые ссылки по проекту Finance.

## Проект

- [[Finance]] — главная заметка проекта

## Навигация

- [[MOC_Finance]] — MOC-карта проекта
- [[Карта_Пользовательских_Путей_Finance]] — UX journey map для дизайнеров
- [[Единый_Документ_Критики_И_План_NewDis]] — кворум-синтез дизайн-критики и план для `newDis`

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
| Project commit | `819b5815fed8c81bfa6a6e6131e790429454c2e8` |
| Current release scope | Planning iteration MVP production release; allocation-level progress clarification; web + backend current release sync |
| Backend/API | Alembic head `20260607_0013 (head)`; production backend current `/opt/finance/releases/20260607T225457Z-819b5815`; prod `COMMIT` -> `819b5815fed8c81bfa6a6e6131e790429454c2e8` |
| QA | OpenAPI parse OK; operationId duplicates `0/58`; backend `243 passed, 9 warnings`; Android unit PASS; Android assembleDebug PASS; APK SHA256 `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4` |
| Production deploy | SUCCESS: project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`; release `20260607T225457Z-819b5815`; backend `/opt/finance/releases/20260607T225457Z-819b5815`; web `/var/www/finance/releases/20260607T225457Z-819b5815` |
| Production evidence | `finance-backend.service` active; `127.0.0.1:8081/health` OK; `/finance-api/health` OK; `/finance/` 200; manifest scope/start_url `/finance/`; `/finance/sw.js` 200; authenticated login/OCR smoke NOT_RUN |
| Android APK final | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk`; size `54,235,660`; SHA256 `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4`; debug-signed |

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19). Текущая поставка 2026-06-07 — Planning iteration MVP — прошла QA gate и подтверждена в production release `20260607T225457Z-819b5815`.

## Release Planning iteration MVP (текущий контекст)

- Project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8` (`Release planning iteration MVP`), branch `codex/finance-planning-mvp-gpt5` запушен в `origin`.
- Backend current: `/opt/finance/releases/20260607T225457Z-819b5815`; web current: `/var/www/finance/releases/20260607T225457Z-819b5815`; оба prod `COMMIT` файла указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8`.
- Alembic head: `20260607_0013 (head)`.
- Production checks: service active, health direct/nginx OK, `/finance/` 200, manifest scope/start_url `/finance/`, `/finance/sw.js` 200.
- QA evidence: OpenAPI parse OK, operationId duplicates `0/58`, backend `243 passed, 9 warnings`, Android unit PASS, Android `assembleDebug` PASS.
- Acceptance clarification: planning progress является allocation-level (`PlanningAllocationDto.actualAmount`/`varianceAmount`/`status`/`attentionReason`), не `PlanningPlanDto.progress`; `previousMonthSurplus` находится в `PlanningSummaryDto`.
- Release evidence: [[Док_Release_Planning_MVP_20260607]].
- Residual risk: authenticated QA login/OCR smoke не запускался из-за отсутствия operator password/session token; APK debug-signed.

## Asset categories + Analytics/Planning polish (текущий контекст)

- Asset categories — source of truth: `manualAmount` для пустых категорий, `isInvestment`, `assetType`, связь `account.assetCategoryId`; удалённые счета не дают stale totals.
- Backend/API: `reportMode=personal`, asset-categories endpoints, миграция `20260607_0012`.
- Analytics: investments metric; capital structure отображается только в Analytics.
- Categories: создание учитывает scope `personal`/`household`; редактирование через edit icon.
- Planning: income day = день месяца; income form скрыта за Add; новые allocations выбирают expense category или investment asset category, без account target; history text уточнён.
- QA evidence: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`, APK SHA256 `C0AC9EC325482FF5ED4AE9D9B55CC35B16C4B509E66BCD99B5FCBD06156A9C26`.
- Release boundary: production deploy текущей поставки подтверждён; `/opt/finance/current` указывает на `/opt/finance/releases/20260607T163043Z-be9f8ab`.

## Planning MVP (текущий контекст)

- Вкладка Analytics получила Planning flow: personal/shared scope, income sources, allocations, history/copy, локальные Android reminders.
- Backend/API включает planning package, таблицы `planning_plans`, `planning_income_sources`, `planning_allocations`, OpenAPI planning endpoints и authz/validation правила.
- Allocation targets для новых allocations поддерживают expense categories и investment asset categories; account target больше не предлагается для новых allocations.
- Миграция release: `20260607_0011_planning_allocation_asset_target.py`.
- Android flow расширен выбором и созданием asset/investment из planning flow.
- QA evidence по Planning лежит в [[QA_Результаты#Волна 3 Аналитика - Планирование MVP (2026-06-06)]], [[QA_Фиксы#Волна 4 (2026-06-07)]] и [[QA_Фиксы#Волна 5 (2026-06-07)]]. Актуальные цифры текущей поставки: backend latest `238 passed, 8 warnings`, fixtures `8 passed`, Android build `BUILD SUCCESSFUL`.

## Риски

P1-B02, P1-B03, tag misalignment; production deploy текущей поставки подтверждён release agent.
