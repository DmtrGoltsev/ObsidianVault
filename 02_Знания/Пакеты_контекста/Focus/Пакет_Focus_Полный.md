---
id: "ctx-focus-full"
тип: "пакет_контекста"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
источники:
  - "[[Focus]]"
  - "[[Источник_Промпт]]"
  - "[[Источник_Архитектура]]"
  - "[[Источник_API]]"
  - "[[MOC_Focus]]"
теги:
  - "focus"
  - "пакет_контекста"
  - "агрегат"
---

# Пакет контекста: Focus (Полный)

Агрегат всех знаний проекта Focus для быстрой загрузки в контекст агента.

## 1. Проект

[[Focus]] — планировщик задач. Модульный монолит на Spring Boot + React + Android.

## 2. Глоссарий

- [[Green_Task]] — зелёная задача (осознанный выбор пользователя)
- [[Red_Task]] — красная задача (индикатор прокрастинации, автоматически)
- [[Priority_Decay]] — механизм автоснижения приоритета с раздельными коэффициентами
- [[Recurrence_Rule]] — правило повторения задач (DAILY, WEEKLY, MONTHLY, YEARLY, CUSTOM)
- [[Reminder_Rule]] — правило напоминаний о задаче (BEFORE_DUE, AT_TIME, DAILY, WEEKLY)

## 3. Источники

- [[Источник_Промпт]] — промпт инициализации Focus (структура vault)
- [[Источник_Архитектура]] — архитектурный блюпринт (стиль, модули, решения)
- [[Источник_API]] — API-контракты (эндпоинты, аутентификация, пагинация)

## 4. Архитектурные решения (ADR)

- [[ADR_Modular_Monolith]] — почему модульный монолит, а не микросервисы
- [[ADR_JWT_Auth]] — почему JWT (access + refresh), а не сессии или OAuth2
- [[ADR_Priority_Decay]] — почему раздельные коэффициенты decay для зелёных/красных

## 5. Навигация

- [[MOC_Focus]] — MOC-карта всех заметок проекта
- [[MOC_Все_Проекты]] — все проекты vault

## 6. Структура vault (Focus)

```
01_Работа/Проекты/Focus/Focus.md
01_Работа/Задачи/Focus/
02_Знания/Глоссарий/Focus/Green_Task.md, Red_Task.md, Priority_Decay.md, Recurrence_Rule.md, Reminder_Rule.md
02_Знания/Источники/Focus/Источник_Промпт.md, Источник_Архитектура.md, Источник_API.md
02_Знания/Доказательства/Focus/
02_Знания/Пакеты_контекста/Focus/Пакет_Focus_Полный.md
03_Агенты/Focus/
04_Решения/Focus/ADR_Modular_Monolith.md, ADR_JWT_Auth.md, ADR_Priority_Decay.md
05_Система/Карты_MOC/Focus/MOC_Focus.md
05_Система/Регламенты/Focus/
05_Система/Схемы/Focus/
05_Система/Промпты/Focus/
```

## 7. Ключевые технические решения

- Java 21, Spring Boot 3.4.5, Spring Data JPA, Flyway
- PostgreSQL 16, JSONB для гибких настроек
- JWT: access 15 min, refresh 30 days
- Фоновый планировщик: Spring `@Scheduled` для decay, reminders, recurrence
- Тестирование: JUnit + Embedded PostgreSQL (zonky), Robolectric 4.12.2
- CI/CD: GitHub Actions

## 8. Родительский проект

[[RocketFlow]] — исходный проект, от которого ответвляется Focus.
