---
id: "moc-finance"
тип: "MOC"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-08"
уверенность: "высокая"
теги: ["MOC", "finance", "навигация"]
источники:
  - "README.md"
  - "docs/product-mvp.md"
  - "docs/current-status.md"
ссылки:
  - "[[Finance]]"
  - "[[MOC_Все_Проекты]]"
---

# MOC — Finance

Навигационная карта проекта Finance. Все заметки проекта собраны здесь.

## Проект

- [[Finance]] — главная заметка проекта

## Под-MOC

_(под-MOC проекта будут добавляться по мере роста vault)_

## Глоссарий

- [[Household]] — семейное пространство
- [[Personal_Shared]] — personal vs shared данные
- [[Transaction]] — операция (income/expense/transfer/brokerage)
- [[Transfer]] — перевод между счетами
- [[Capture_Draft]] — OCR черновик
- Asset categories — source of truth для категорий активов: `manualAmount`, `isInvestment`, `assetType`, `account.assetCategoryId`, без stale totals от удалённых счетов
- Planning MVP — планирование доходов и распределений во вкладке Analytics; новые allocations выбирают expense category или investment asset category, account target для новых allocations не предлагается

## Источники

- [[Источник_README]]
- [[Источник_Продукт_MVP]]
- [[Источник_Текущий_Статус]]
- [[Источник_ADR_0001]]
- [[Источник_Security_Baseline]]

## Пакеты контекста

- [[Пакет_Finance_Полный]] — агрегирующий пакет со всеми ссылками
- [[Кворум_Finance]] — кворум-саммари проекта

## Агенты

_(роли агентов проекта — см. `03_Агенты/Finance/`)_

## Решения

_(архитектурные и проектные решения — см. `04_Решения/Finance/`)_

## Доказательства

- [[QA_Результаты]] — результаты прогонов тестирования
- [[QA_Фиксы]] — журнал фиксов багов
- [[Док_Release_Planning_MVP_20260607]] — concise evidence по production release `20260607T225457Z-819b5815`
- Planning evidence — см. [[QA_Фиксы#Волна 3 (2026-06-06)]], [[QA_Фиксы#Волна 4 (2026-06-07)]], [[QA_Фиксы#Волна 5 (2026-06-07)]] и [[QA_Фиксы#Волна 6 (2026-06-07)]]
- Release context — текущая поставка 2026-06-07: Planning iteration MVP; project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`; release `20260607T225457Z-819b5815`; backend `/opt/finance/releases/20260607T225457Z-819b5815`; web `/var/www/finance/releases/20260607T225457Z-819b5815`; Alembic `20260607_0013 (head)`; backend `243 passed, 9 warnings`; Android unit/assemble PASS; health/static checks OK

## Схемы

_(схемы проекта — см. `05_Система/Схемы/Finance/`)_

## Регламенты

_(регламенты проекта — см. `05_Система/Регламенты/Finance/`)_

## Промпты

_(промпты агентов — см. `05_Система/Промпты/Finance/`)_

## Навигация

- [[MOC_Все_Проекты]] — ← все проекты
