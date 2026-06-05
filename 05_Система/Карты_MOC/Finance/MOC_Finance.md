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

- [[Агент_Бэкенд]] — Python/FastAPI backend API
- [[Агент_PWA]] — React/Vite PWA + iOS (Capacitor)
- [[Агент_Android]] — Kotlin/Compose Android
- [[Агент_QA]] — тестирование и верификация
- [[Агент_DevOps]] — инфраструктура и деплой

## Решения

- [[ADR_0002_Auth_Model]] — двухплатформенная модель аутентификации
- [[ADR_0003_OCR_Architecture]] — OCR архитектура (ML Kit + Tesseract)
- [[ADR_0004_Capture_Drafts_Lifecycle]] — lifecycle capture drafts
- [[ADR_0005_Scope_Isolation]] — scope isolation через DB triggers

## Доказательства

- [[Доказательство_Production_GO]] — Production MVP functional GO (2026-05-19)
- [[Доказательство_Android_QA]] — Android final QA
- [[Доказательство_PWA_iOS_QA]] — PWA/iiPhone final QA
- [[Доказательство_Privacy_Security]] — Privacy/Security baseline (10 инвариантов)
- [[Доказательство_MVP_Release]] — Release checklist + test matrix

## Схемы

- [[Схема_Архитектуры]] — архитектура системы (клиенты, backend, OCR, БД)
- [[Схема_Развертывания]] — деплой на HexCore (nginx, systemd, PostgreSQL)
- [[Схема_Data_Flow]] — поток данных OCR capture drafts

## Регламенты

_(регламенты проекта — см. `05_Система/Регламенты/Finance/`)_

## Промпты

- [[Промпт_Агента_Бэкенд]] — инструкция бэкенд-агенту
- [[Промпт_Агента_QA]] — инструкция QA-агенту
- [[Промпт_Деплоя]] — инструкция DevOps по деплою

## Задачи

- [[Задача_Wave1_MVP]] — Wave 1: MVP (выполнено)
- [[Задача_Capture_Drafts_OCR]] — OCR capture drafts (выполнено)
- [[Задача_Wave2_Backlog]] — Wave 2 backlog (черновик)
- [[Задача_Production_Deploy]] — деплой на HexCore (выполнено)

## Навигация

- [[MOC_Все_Проекты]] — ← все проекты
