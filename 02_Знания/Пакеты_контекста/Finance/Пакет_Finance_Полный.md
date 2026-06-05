---
id: "context-package-finance-full"
тип: "пакет_контекста"
проект: "Finance"
название: "Пакет Finance — Полный контекст"
создано: "2026-06-01"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["пакет_контекста", "finance", "агрегация"]
источники:
  - "[[Источник_README]]"
  - "[[Источник_Продукт_MVP]]"
  - "[[Источник_Текущий_Статус]]"
  - "[[Источник_ADR_0001]]"
  - "[[Источник_Security_Baseline]]"
  - "[[Источник_OpenAPI]]"
  - "[[Источник_Domain_Model]]"
  - "[[Источник_Access_Model]]"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
  - "[[Кворум_Finance]]"
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
| [[OCR_Pipeline]] | Конвейер распознавания (layout-aware) |
| [[OCR_Layout_Parser]] | Layout-aware парсинг aggregate rows |
| [[Capture_Draft_Lifecycle]] | Жизненный цикл черновика |
| [[Auth_Model]] | Модель аутентификации |
| [[DB_Schema]] | Схема базы данных |
| [[Account]] | Счёт |
| [[Category]] | Категория |
| [[Membership]] | Членство в household |
| [[Scope_Isolation]] | Изоляция scope |
| [[Immutable_Scope]] | Immutable scope triggers |
| [[Capture_Category_Mapping]] | Маппинг OCR-категорий |
| [[Rate_Limiting]] | Rate limiting |
| [[Neutral_Response]] | Нейтральный ответ |
| [[Session_Token]] | Сессионный токен |
| [[Screenshot_Source]] | Screenshot OCR source |
| [[Money]] | Money value object |
| [[Report]] | Отчёт |
| [[Testing_Strategy]] | Стратегия тестирования |

## Решения (ADR)

| ADR | Тема |
|-----|------|
| [[ADR_0002_Auth_Model]] | Двухплатформенная модель аутентификации |
| [[ADR_0003_OCR_Architecture]] | OCR архитектура |
| [[ADR_0004_Capture_Drafts_Lifecycle]] | Lifecycle capture drafts |
| [[ADR_0005_Scope_Isolation]] | Scope isolation через DB triggers |

## Пакеты контекста

| Пакет | Описание |
|-------|----------|
| [[Кворум_Finance]] | Кворум-саммари |
| [[Android_Architecture]] | Архитектура Android |
| [[PWA_Architecture]] | Архитектура Web PWA + iOS |

## Кворум

- [[Кворум_Finance]] — кворум-саммари с высокой уверенностью

## Стек (кратко)

Python 3.12 / FastAPI / PostgreSQL 16 / React 19 + Vite 7 PWA / Kotlin Jetpack Compose Android / OpenAPI 3.1 contract-first / Self-hosted Linux nginx

## Стадия

Production MVP functional GO (2026-05-19)

## Риски

P1-B02, P1-B03, tag misalignment
