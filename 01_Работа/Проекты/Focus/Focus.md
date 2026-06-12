---
id: "proj-focus-001"
тип: "проект"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-12"
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

**Production GO (2026-06-07)** — развёрнут на [[HexCore]] (`45.10.110.42`)

- Backend: systemd `focus.service`, порт 8082, JVM 256 MB
- Frontend: `/var/www/focus/`, nginx location `/focus/`
- API: nginx location `/focus-api/` → proxy на 8082
- БД: PostgreSQL 18, БД `focus_db`, пользователь `focus_user`
- URL: `http://45.10.110.42/focus/`

### Статус кода

- Backend: 21 фикс применён (FIX-A — FIX-U), BE-101 исправлен
- Frontend: ретро-стиль UI, 18/18 Playwright E2E PASS
- Android: офлайн-first компаньон, Room + WorkManager
- Все сборки: mvn test 21/21 PASS, npm run build OK, assembleDebug OK

### QA прогресс (2026-06-12)

| Метрика | Значение |
|---|---|
| Всего тест-кейсов | 253 (v2) + 47 (v3 quorum) + 13 (QA3 backend E2E) + 2 (QA3 Android E2E) = 315 |
| Протестировано (Волны 1-9) | ~155 (61% от v2) |
| Протестировано QE v3 backend | 29/47 (62%) |
| PASS v3 backend | 29 |
| Протестировано QA3 backend E2E | 13/13 (100%) |
| PASS QA3 backend E2E | 13 |
| Протестировано QA3 Android E2E | 2/2 (1 FAIL, 1 SKIP) |
| FAIL (открытые баги) | 2 (BE-101, AND-101) |
| Playwright E2E | 18/18 PASS |
| Android E2E | 9 PASS, 2 MANUAL (color-only) |
| MANUAL | 2 (AND-040, AND-012) |
| Фиксов применено | 21 (FIX-A — FIX-U) |
| FCM интеграция | Реализована (backend+android), верифицирована сборка, ожидает тестирования (disabled по умолчанию) |

См. подробности: [[QA_Результаты]], [[QA_Фиксы]], [[QA_ТестКейсы_v2]]

### Предыдущий аудит (2026-06-04)

Из 24 бизнес-требований: **9 работают полностью, 7 частично, 8 не реализованы**.
Ключевые проблемы: FCM мёртвый, Sharing не давал доступ (FIX-O), Decay settings не сохранялись (FIX-M),
Recurrence/Reminders/Links нет в UI, Offline sync только CREATE.

См. полный аудит: [[Аудит_Реальный_Статус]]
См. план исправлений: [[План_Исправлений_Focus]]

## Риски

- ~~BE-101: Goal owner не может редактировать task созданный shared user → пофикшен~~
- **AND-101: Android — токен не сохраняется в EncryptedSharedPreferences. После force-stop/restart — экран авторизации. Требуется расследование TokenManager/EncryptedSharedPreferences.**
- FCM push — реализована (backend+android, FIX-U wave), disabled по умолчанию. Для активации нужен Firebase project + credentials (Phase 3 nice-to-have)
- ReminderScheduler advisory lock — H2 fallback в тестах (noise, не блокер)

## Ссылки

- [[MOC_Focus]] — карта всех заметок проекта
- [[MOC_Все_Проекты]] — все проекты vault
- [[HexCore]] — production-сервер
- [[Регламент_Деплоя_Focus]] — процедура деплоя
- [[Источник_Промпт]] — промпт инициализации проекта
- [[Источник_Архитектура]] — архитектурные решения
- [[Источник_API]] — API-контракты
- [[Пакет_Focus_Полный]] — пакет контекста (агрегат)
