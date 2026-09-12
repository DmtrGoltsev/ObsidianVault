---
id: "proj-focus-report-001"
тип: "доказательство"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-02"
обновлено: "2026-06-04"
уверенность: "высокая"
источники:
  - "[[Источник_Промпт]]"
  - "[[Focus]]"
теги:
  - "focus"
  - "mvp"
  - "результаты"
  - "доказательство"
---

# Результаты MVP Focus

> Обновлено: 2026-06-04 — этап исправления критических багов и синхронизации API

## Статус сборки

| Компонент | Статус | Проверка |
|-----------|--------|----------|
| Backend (Spring Boot 3.4.1) | ✅ Работает | `mvn compile`, `mvn test` зелёный |
| Frontend (React 18 + Vite 5) | ✅ Работает | `npm run build` зелёный |
| Android (Kotlin) | ✅ Собирается | `./gradlew assembleDebug` зелёный |
| База данных (PostgreSQL 18) | ✅ Таблицы созданы | Flyway V1 + V2 миграции применены |
| CI/CD (GitHub Actions) | ✅ Определены | 4 workflow файла |
| Docker | ✅ Готов | `docker-compose.yml` + `Dockerfile.backend` |

## Модули бэкенда

| # | Модуль | Статус | Примечание |
|---|--------|--------|------------|
| 1 | auth | ✅ | JWT access/refresh, BCrypt, логаут |
| 2 | accounts | ✅ | Профиль, часовой пояс, язык |
| 3 | settings | ✅ | Язык, decay config (green/red раздельно), сохранение в БД |
| 4 | folders | ✅ | CRUD + soft delete, description, color |
| 5 | goals | ✅ | CRUD + soft delete, status, priority |
| 6 | tasks | ✅ | GREEN/RED, статусы, теги, связи, reschedule с decay |
| 7 | sharing | ✅ | Инвайты по email, share goal/task, accept/decline |
| 8 | calendar | ✅ | day/week/month, `GET /api/calendar?from=...&to=...` |
| 9 | recurrence | ✅ | DAILY/WEEKLY/MONTHLY, auto-create next occurrence |
| 10 | reminders | ✅ | AT_START/BEFORE_START/BEFORE_DEADLINE, advisory lock |
| 11 | prioritypolicy | ✅ | Decay при reschedule + time-based decay (cron) |
| 12 | notifications | ✅ | FCM + логирование (заглушка отправки) |

## API эндпоинты — проверены

Все эндпоинты протестированы через curl/Invoke-RestMethod:

| Эндпоинт | Метод | Результат |
|----------|-------|-----------|
| `/api/auth/register` | POST | ✅ 200, возвращает JWT |
| `/api/auth/login` | POST | ✅ 200, возвращает JWT |
| `/api/me` | GET | ✅ 200, профиль пользователя |
| `/api/me/settings` | PATCH | ✅ 200, настройки обновлены |
| `/api/folders` | GET/POST | ✅ 200/201, CRUD работает |
| `/api/folders/{id}` | PATCH/DELETE | ✅ 200/204 |
| `/api/folders/{id}/goals` | GET/POST | ✅ 200/201 |
| `/api/goals/{id}` | GET/PATCH/DELETE | ✅ 200/204 |
| `/api/goals/{id}/tasks` | GET/POST | ✅ 200/201 |
| `/api/tasks/{id}` | GET/PATCH/DELETE | ✅ 200/204 |
| `/api/tasks/{id}/complete` | POST | ✅ 200 |
| `/api/tasks/{id}/cancel` | POST | ✅ 200 |
| `/api/tasks/{id}/reschedule` | POST | ✅ 200, priority decay применяется |
| `/api/tasks/{id}/tags` | PUT | ✅ 200 |
| `/api/tasks/{id}/links` | POST | ✅ 200 |
| `/api/tasks/{id}/recurrence` | PUT | ✅ 200 |
| `/api/tasks/{id}/reminders` | PUT | ✅ 200 |
| `/api/goals/{id}/share` | POST | ✅ 201 |
| `/api/tasks/{id}/share` | POST | ✅ 201 |
| `/api/shares` | GET | ✅ 200, список моих шарингов |
| `/api/shares/accepted` | GET | ✅ 200, принятые шаринги |
| `/api/shares/invitations` | GET | ✅ 200, входящие приглашения |
| `/api/shares/{id}/accept` | POST | ✅ 200 |
| `/api/shares/{id}/decline` | POST | ✅ 200 |
| `/api/calendar` | GET | ✅ 200 |
| `/api/devices` | POST | ✅ 201 |
| `/api/health` | GET | ✅ 200, status: UP |

## Фронтенд

- Ретро-стиль (Press Start 2P, моноширинный шрифт)
- 7 страниц: Auth, Folders, Goals, Tasks, Calendar, Settings, Sharing
- i18n: русский / английский
- Protected routes (JWT)
- Service Worker (PWA ready)
- API контракты синхронизированы с бэкендом

## Android

- Kotlin, minSdk 26, targetSdk 34
- Room (SQLite) для офлайн-first
- WorkManager для фоновой синхронизации
- Retrofit + OkHttp для API
- EncryptedSharedPreferences для токенов
- Navigation Component, ViewModel + LiveData
- API контракты синхронизированы с бэкендом
- APK собирается (`assembleDebug`)

## Исправления (2026-06-04)

### Критические (P0)
- ✅ Создан `.gitignore` — секреты и артефакты исключены из git
- ✅ ReminderScheduler: исправлена логика AT_START (было идентично BEFORE_START)
- ✅ ReminderScheduler: добавлен PostgreSQL advisory lock для безопасности
- ✅ ReminderScheduler: исправлен LazyInitializationException (JOIN FETCH)
- ✅ API контракты фронтенда полностью синхронизированы с бэкендом
- ✅ API контракты Android полностью синхронизированы с бэкендом

### Высокие (P1)
- ✅ PriorityPolicyService: реализован time-based decay (по дням/неделям/месяцам)
- ✅ ShareController: добавлены `GET /api/shares`, `GET /api/shares/accepted`
- ✅ UserController.updateSettings: сохраняет decay config в БД

## Известные ограничения

1. FCM push-уведомления — заглушка (нужна реальная интеграция Firebase)
2. Нужны инструментальные тесты Android (Espresso)
3. Нужна реальная Firebase-интеграция для push на устройство
4. ProGuard для Android release не настроен

## Следующие шаги

1. Подключить реальный Firebase проект для push-уведомлений
2. Покрытие Android инструментальными тестами (Espresso)
3. Production деплой на self-hosted Linux (docker-compose)
4. Подключить реальное Android устройство к локальному бэкенду
5. End-to-end тестирование полного флоу

## Ссылки

- [[Focus]] — главная заметка проекта
- [[MOC_Focus]] — карта содержимого
- [[ADR_Modular_Monolith]] | [[ADR_JWT_Auth]] | [[ADR_Priority_Decay]]
- [[Пакет_Focus_Полный]] — пакет контекста