---
id: "moc-finance"
тип: "MOC"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["MOC", "finance", "навигация"]
источники:
  - "README.md"
  - "docs/product-mvp.md"
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
- [[OCR_Pipeline]] — конвейер распознавания (layout-aware парсер)
- [[OCR_Layout_Parser]] — layout-aware парсинг aggregate rows
- [[Capture_Draft_Lifecycle]] — жизненный цикл черновика захвата
- [[Auth_Model]] — модель аутентификации
- [[DB_Schema]] — схема базы данных
- [[Account]] — счёт (cash/card/savings/brokerage)
- [[Category]] — категория расходов/доходов
- [[Membership]] — членство в household
- [[Scope_Isolation]] — изоляция personal/shared scope
- [[Immutable_Scope]] — immutable scope triggers
- [[Capture_Category_Mapping]] — маппинг OCR-категорий
- [[Rate_Limiting]] — rate limiting auth endpoints
- [[Neutral_Response]] — нейтральные ответы при ошибках auth
- [[Session_Token]] — сессионные токены
- [[Screenshot_Source]] — screenshot OCR source
- [[Money]] — Money value object (decimal)
- [[Report]] — отчёты (spending by category, period summaries)
- [[Testing_Strategy]] — стратегия тестирования

## Источники

- [[Источник_README]]
- [[Источник_Продукт_MVP]]
- [[Источник_Текущий_Статус]]
- [[Источник_ADR_0001]]
- [[Источник_Security_Baseline]]
- [[Источник_OpenAPI]]
- [[Источник_Domain_Model]]
- [[Источник_Access_Model]]

## Пакеты контекста

- [[Пакет_Finance_Полный]] — агрегирующий пакет со всеми ссылками
- [[Кворум_Finance]] — кворум-саммари проекта
- [[Android_Architecture]] — архитектура Android-приложения
- [[PWA_Architecture]] — архитектура Web PWA + iOS/Capacitor

## Агенты

_(роли агентов проекта — см. `03_Агенты/Finance/`)_

## Решения

- [[ADR_0002_Auth_Model]] — двухплатформенная модель аутентификации
- [[ADR_0003_OCR_Architecture]] — OCR архитектура (ML Kit + Tesseract)
- [[ADR_0004_Capture_Drafts_Lifecycle]] — lifecycle capture drafts
- [[ADR_0005_Scope_Isolation]] — scope isolation через DB triggers

## Доказательства

_(доказательства верификации — см. `02_Знания/Доказательства/Finance/`)_

## Схемы

_(схемы проекта — см. `05_Система/Схемы/Finance/`)_

## Регламенты

_(регламенты проекта — см. `05_Система/Регламенты/Finance/`)_

## Промпты

_(промпты агентов — см. `05_Система/Промпты/Finance/`)_

## Навигация

- [[MOC_Все_Проекты]] — ← все проекты
