---
id: "src-qa-strategy"
тип: "источник"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-01"
уверенность: "высокая"
источники: ["docs/06-qa-strategy.md"]
доказательства: []
теги: ["документация", "qa", "тестирование"]
---

# Источник: QA Стратегия

## Путь

`docs/06-qa-strategy.md`

## Роль в проекте

Определяет стратегию тестирования RocketFlow: уровни тестов (unit, интеграционные, smoke, E2E), инструменты (JUnit, Embedded PostgreSQL zonky, Robolectric), критерии качества.

## Краткое содержание

Пирамида тестирования: backend unit tests (JUnit), backend integration tests (Embedded PostgreSQL), web build verification, Android Robolectric tests, notification E2E smoke. CI-воркфлоу для каждого уровня. Proof-стандарт для доказательств. Добавлены требования MVP3 UI Tests и Android parity — проверка UI на соответствие между web и Android клиентами.

## Статус актуальности

Актуален. Все CI-воркфлоу следуют этой стратегии.

## Связанные заметки

- [[Агент_QA]] — роль QA в проекте
- [[Регламент_CI_CD]] — CI/CD воркфлоу
- [[Регламент_Нотификационного_Смока]] — smoke-тестирование нотификаций
