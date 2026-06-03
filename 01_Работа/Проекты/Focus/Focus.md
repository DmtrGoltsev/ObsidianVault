---
id: "proj-focus-001"
тип: "проект"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-04"
уверенность: "высокая"
источники:
  - "[[Источник_Промпт]]"
  - "[[Источник_Архитектура]]"
  - "[[Источник_API]]"
теги:
  - "focus"
  - "планировщик"
  - "spring_boot"
  - "react"
  - "android"
---

# Focus

## Цель проекта

Приложение для планирования задач с приоритетами, напоминаниями и совместным доступом. Помогает пользователю фокусироваться на важном через систему зелёных/красных задач, автоснижения приоритета при прокрастинации и повторяющихся задач. Проект Focus — ответвление от [[RocketFlow]], выделяющее core-логику в независимый продукт.

## Стек технологий

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.5, Spring Security, Spring Data JPA, Flyway, PostgreSQL 16 |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6, lucide-react |
| Android | Kotlin 1.9.24, minSdk 26, targetSdk 34, WorkManager 2.9.1, FCM 24.1.0 |
| CI/CD | GitHub Actions (ubuntu-24.04) |
| Production | systemd + Nginx |
| Тестирование | JUnit + Embedded PostgreSQL (zonky), Robolectric 4.12.2 |

## Архитектура

[[Modular_Monolith]] — один бэкенд, одна БД, один фоновый планировщик, web SPA, Android клиент.

Решение: [[ADR_Modular_Monolith]]

## Модули бэкенда

- `auth` — аутентификация и управление токенами (JWT)
- `accounts` — профили пользователей, регистрация, управление аккаунтом
- `settings` — настройки пользователя (часовой пояс, язык, уведомления)
- `folders` — папки/проекты для группировки задач
- `goals` — цели пользователя с привязкой к задачам
- `tasks` — CRUD задач, зелёные/красные, приоритеты, drag-and-drop
- `sharing` — совместный доступ к папкам и задачам
- `calendar` — представление задач в календаре
- `recurrence` — правила повторения задач ([[Recurrence_Rule]])
- `reminders` — правила напоминаний ([[Reminder_Rule]])
- `prioritypolicy` — политика автоснижения приоритета ([[Priority_Decay]])
- `notifications` — push-уведомления через FCM
- `ideas` — идеи/входящие, инбокс
- `links` — ссылки, прикреплённые к задачам
- `notes` — заметки к задачам
- `health` — health-check эндпоинты и метрики
- `common` — общие утилиты, DTO, исключения
- `config` — конфигурация Spring, CORS, security

## Текущий статус

- Проект инициализирован: 2026-06-01
- Стадия: **MVP v2 — бэкенд + фронтенд + Android реализованы и протестированы**
- Ветка: `agent/opencode/focus-init`
- Структура Obsidian vault создана
- Backend: ✅ Spring Boot 3.4.1, компилируется, запускается, API проверен
- Frontend: ✅ React 18 + Vite 5, `npm run build` зелёный
- Android: ✅ Kotlin, `assembleDebug` зелёный, API контракты синхронизированы
- CI/CD: ✅ 4 workflow файла в `.github/workflows/`
- Тесты: ✅ 5 тестовых классов, `mvn test` зелёный

### Исправления (2026-06-04)

- Создан `.gitignore` в корне проекта
- ReminderScheduler: исправлена логика AT_START/BT_START, добавлен PostgreSQL advisory lock
- ReminderScheduler: исправлен LazyInitializationException через JOIN FETCH
- API контракты фронтенда/Android/бэкенда полностью синхронизированы
- PriorityPolicyService: реализован time-based decay (по дням/неделям/месяцам)
- ShareController: добавлены `GET /api/shares`, `GET /api/shares/accepted`
- Бэкенд проверен через curl: register → login → folders → goals → tasks — все CRUD работают
- Добавлен `docker-compose.yml` и `Dockerfile.backend` для деплоя

## Риски

- Отделение от [[RocketFlow]] может привести к дублированию кода
- Выбор модульного монолита требует строгой дисциплины границ модулей
- JWT-аутентификация требует безопасного хранения refresh-токенов на клиентах
- FCM push-уведомления — заглушка, нужна реальная интеграция Firebase
- Android testing — нужны инструментальные тесты (Espresso)

## Ссылки

- [[MOC_Focus]] — карта всех заметок проекта
- [[MOC_Все_Проекты]] — все проекты vault
- [[Источник_Промпт]] — промпт инициализации проекта
- [[Источник_Архитектура]] — архитектурные решения
- [[Источник_API]] — API-контракты
- [[Пакет_Focus_Полный]] — пакет контекста (агрегат)
