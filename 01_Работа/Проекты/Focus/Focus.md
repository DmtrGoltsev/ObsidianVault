---
id: "proj-focus-001"
тип: "проект"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-06"
уверенность: "высокая"
источники:
  - "[[Источник_Промпт]]"
  - "[[Источник_Архитектура]]"
  - "[[Источник_API]]"
доказательства:
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
  - "[[QA_ТестКейсы_v2]]"
теги:
  - "focus"
  - "планировщик"
  - "spring_boot"
  - "react"
  - "android"
---

# Focus

## Цель продукта

Focus — планировщик задач, который помогает пользователю фокусироваться на важном. Ключевая механика: задачи делятся на два типа — **Green** (выполнение двигает к успеху) и **Red** (невыполнение создаёт негативные последствия). Пользователь организует работу в иерархии: **Папки → Цели → Задачи**. Цели и задачи можно шарить с другими пользователями по email-инвайту.

## Стек технологий

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.1, Spring Security, Spring Data JPA, Flyway, PostgreSQL 18 |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6 |
| Android | Kotlin, minSdk 26, targetSdk 34, Room, WorkManager 2.9.1, FCM |
| CI/CD | GitHub Actions |
| Production | systemd + Nginx |

## Архитектура

**Modular Monolith** — один бэкенд, одна БД, REST API с JWT (access + refresh). Soft delete для folders/goals/tasks. Optimistic locking через @Version. In-process scheduler для напоминаний.

Решение: [[ADR_Modular_Monolith]]

## Модули бэкенда

- `auth` — аутентификация, JWT access/refresh, логаут
- `accounts` — профиль пользователя, часовой пояс
- `settings` — язык интерфейса, политики priority decay
- `folders` — CRUD папок, порядок отображения
- `goals` — CRUD целей внутри папок
- `tasks` — CRUD задач, green/red, приоритет 1-10, статусы, теги, связи
- `sharing` — инвайты по email, goal/task sharing
- `calendar` — day/week/month проекции
- `recurrence` — правила повторения ([[Recurrence_Rule]])
- `reminders` — правила напоминаний ([[Reminder_Rule]])
- `prioritypolicy` — автоснижение приоритета ([[Priority_Decay]])
- `notifications` — push через FCM, регистрация устройств
- `health` — health-check

## Текущий статус

**Активная разработка + QA тестирование**

- Backend: функционально завершён, 18 фиксов применено (FIX-A — FIX-R)
- Frontend: ретро-стиль UI, SPA с роутингом
- Android: офлайн-first компаньон, Room + WorkManager

### QA прогресс (2026-06-06)

| Метрика | Значение |
|---|---|
| Всего тест-кейсов | 253 |
| Протестировано (Волны 1-3) | ~65 |
| PASS | ~63 |
| FAIL (открытые баги) | 1 (BE-101) |
| Фиксов применено | 18 |

См. подробности: [[QA_Результаты]], [[QA_Фиксы]], [[QA_ТестКейсы_v2]]

### Предыдущий аудит (2026-06-04)

Из 24 бизнес-требований: **9 работают полностью, 7 частично, 8 не реализованы**.
Ключевые проблемы: FCM мёртвый, Sharing не давал доступ (FIX-O), Decay settings не сохранялись (FIX-M),
Recurrence/Reminders/Links нет в UI, Offline sync только CREATE.

См. полный аудит: [[Аудит_Реальный_Статус]]
См. план исправлений: [[План_Исправлений_Focus]]

## Риски

- BE-101: Goal owner не может редактировать task созданный shared user → 404
- Android: ANR при холодном старте (FIX-E: lazy TokenManager)
- FCM push — заглушка, нужна реальная интеграция Firebase
- Offline sync — только CREATE, нет UPDATE/DELETE sync

## Ссылки

- [[MOC_Focus]] — карта всех заметок проекта
- [[MOC_Все_Проекты]] — все проекты vault
- [[Источник_Промпт]] — промпт инициализации проекта
- [[Источник_Архитектура]] — архитектурные решения
- [[Источник_API]] — API-контракты
- [[Пакет_Focus_Полный]] — пакет контекста (агрегат)
