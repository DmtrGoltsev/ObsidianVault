---
id: "agent-qa"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/06-qa-strategy.md", "docs/33-current-state-summary.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md"]
теги: ["агент", "qa", "тестирование"]
---

# Агент QA

## Зона ответственности

- Backend unit tests (JUnit)
- Backend integration tests (Embedded PostgreSQL zonky)
- Web build verification (`npm run build`)
- Android Robolectric tests (4.12.2)
- Notification E2E smoke ([[FCM]] push-tap flow)
- Валидация API контрактов
- Proof-документирование результатов

## Инструменты

- JUnit 5 + Embedded PostgreSQL (zonky)
- Robolectric 4.12.2 для Android unit-тестов
- Скрипт smoke: `scripts/Start-NotificationSmokeBackend.ps1`

## Права на решения

- Определение критериев качества
- Блокировка релиза при падении тестов
- Требование доказательств от других агентов

## Активные задачи

- Staging notification certification
- Валидация MVP3 изменений
- Поддержание зелёных CI-воркфлоу

## Выполненные волны

- Wave A: backend API validation
- Wave B: scheduling validation
- Wave C: notification E2E proof

## Связанные заметки

- [[Источник_QA_Стратегия]] — стратегия тестирования
- [[Регламент_Нотификационного_Смока]] — smoke-процедура
- [[Источник_Нотификация_Пруф]] — результаты proof
- [[RocketFlow]] — проект
