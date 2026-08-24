---
id: "src-focus-api"
тип: "источник"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
источники:
  - "[[Focus]]"
  - "[[Источник_Архитектура]]"
теги:
  - "focus"
  - "источник"
  - "api"
---

# Источник: API-контракты Focus

## Тип источника

Спецификация REST API — документирует контракты между бэкендом и клиентами (Web SPA, Android).

## Базовый URL

`/api/v1`

## Аутентификация

Все запросы (кроме `/auth/**`) требуют заголовок:
```
Authorization: Bearer <access_token>
```

Токены: short-lived access (15 min) + long-lived refresh (30 days). См. [[ADR_JWT_Auth]].

## Основные эндпоинты

| Модуль | Метод | Путь | Описание |
|--------|-------|------|----------|
| `auth` | POST | `/auth/login` | Вход, возвращает токены |
| `auth` | POST | `/auth/register` | Регистрация |
| `auth` | POST | `/auth/refresh` | Обновление access-токена |
| `auth` | POST | `/auth/logout` | Отзыв refresh-токена |
| `tasks` | GET | `/tasks` | Список задач с фильтрацией |
| `tasks` | POST | `/tasks` | Создание задачи |
| `tasks` | PUT | `/tasks/{id}` | Обновление задачи |
| `tasks` | DELETE | `/tasks/{id}` | Удаление задачи |
| `tasks` | PATCH | `/tasks/{id}/priority` | Ручное изменение приоритета |
| `tasks` | PATCH | `/tasks/{id}/toggle-green` | Переключение зелёного флага |
| `folders` | GET | `/folders` | Список папок |
| `folders` | POST | `/folders` | Создание папки |
| `folders` | PUT | `/folders/{id}` | Обновление папки |
| `folders` | DELETE | `/folders/{id}` | Удаление папки |
| `goals` | GET | `/goals` | Список целей |
| `goals` | POST | `/goals` | Создание цели |
| `sharing` | POST | `/sharing/folders/{id}/share` | Поделиться папкой |
| `sharing` | DELETE | `/sharing/folders/{id}/members/{userId}` | Удалить доступ |
| `calendar` | GET | `/calendar` | Задачи в календарном представлении |
| `recurrence` | POST | `/tasks/{id}/recurrence` | Установить правило повторения |
| `recurrence` | DELETE | `/tasks/{id}/recurrence` | Удалить правило повторения |
| `reminders` | POST | `/tasks/{id}/reminders` | Добавить напоминание |
| `reminders` | DELETE | `/reminders/{id}` | Удалить напоминание |
| `notifications` | GET | `/notifications` | Список уведомлений |
| `notifications` | PATCH | `/notifications/{id}/read` | Пометить прочитанным |
| `accounts` | GET | `/accounts/me` | Профиль текущего пользователя |
| `accounts` | PUT | `/accounts/me` | Обновить профиль |
| `settings` | GET | `/settings` | Настройки пользователя |
| `settings` | PUT | `/settings` | Обновить настройки |
| `health` | GET | `/health` | Health-check |

## Форматы ответов

- Успех: `200 OK`, `201 Created`, `204 No Content`
- Ошибка валидации: `400 Bad Request` + `{ "error": "...", "details": [...] }`
- Не авторизован: `401 Unauthorized`
- Доступ запрещён: `403 Forbidden`
- Не найдено: `404 Not Found`
- Конфликт: `409 Conflict`

## Пагинация

Параметры запроса: `page` (0-based), `size` (default 20, max 100).
Ответ: `{ "content": [...], "page": 0, "size": 20, "totalElements": 150, "totalPages": 8 }`

## Связи

- [[Focus]] — главная заметка проекта
- [[Источник_Архитектура]] — архитектурные решения
- [[ADR_JWT_Auth]] — обоснование JWT
