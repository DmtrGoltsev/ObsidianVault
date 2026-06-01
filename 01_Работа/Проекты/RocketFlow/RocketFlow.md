---
id: "proj-rocketflow"
тип: "проект"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "README.md", "docs/04-architecture-blueprint.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md"]
теги: ["проект", "rocketflow", "mvp"]
---

# RocketFlow

## Цель

Приложение для планирования задач с приоритетами, напоминаниями и совместным доступом. Помогает пользователю фокусироваться на важном через систему зелёных/красных задач, автоснижения приоритета при прокрастинации и повторяющихся задач.

## Стек

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.5, Spring Security, Spring Data JPA, Flyway, PostgreSQL 16 |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6, lucide-react |
| Android | Kotlin 1.9.24, minSdk 26, targetSdk 34, WorkManager 2.9.1, FCM 24.1.0 |
| CI/CD | GitHub Actions (ubuntu-24.04) |
| Production | [[HexCore]] (45.10.110.42), systemd + Nginx |
| Тестирование | JUnit + Embedded PostgreSQL (zonky), Robolectric 4.12.2 |

## Архитектура

[[Modular_Monolith]] — один бэкенд, одна БД, один фоновый планировщик, web SPA, Android клиент.

Модули бэкенда: `auth`, `accounts`, `settings`, `folders`, `goals`, `tasks`, `sharing`, `calendar`, `recurrence`, `reminders`, `prioritypolicy`, `notifications`.

## Текущий статус

- Три волны (A, B, C) завершены
- Wave C.1 завершён (web scheduling authoring)
- Текущая стадия: [[MVP3_Упрощение]]
- Backend тесты зелёные
- Web build зелёный
- Android build зелёный
- Notification E2E доказан локально
- Production развёрнут на [[HexCore]]

Источник: [[Источник_Текущее_Состояние]]

## Команда

Роли агентов: [[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_QA]], [[Агент_DevOps]]

## Окружения

- Production: [[HexCore]] (45.10.110.42)
- Staging: через CI (GitHub Actions)
- Локально: dev-профиль Spring Boot, Embedded PostgreSQL

## Активные гейты

- GHCR publish (`backend-image-publish`)
- Staging notification certification

## Известные риски

- Notification smoke на staging ещё не сертифицирован
- GHCR интеграция требует проверки credentials (предположение)
- Android push-tap flow требует staging-валидации

## Документация

- [[Источник_MVP_План]] — план MVP
- [[Источник_Спецификация_Домена]] — доменная модель
- [[Источник_Архитектура]] — архитектурный блюпринт
- [[Источник_API_Контракты]] — API
- [[Источник_Текущее_Состояние]] — текущий статус
- [[Источник_CI_CD_Политика]] — CI/CD
- [[Источник_Продакшен_Runbook]] — production runbook

## Связанные заметки

- [[Wave_A]], [[Wave_B]], [[Wave_C]] — завершённые волны
- [[MVP3_Упрощение]] — текущая стадия
- [[Схема_Развертывания]] — схема деплоймента
- [[Схема_Базы_Данных]] — схема БД
