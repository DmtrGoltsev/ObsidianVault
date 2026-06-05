---
id: "term-auth-model"
тип: "термин"
проект: "Finance"
термин: "Auth Model"
термин_en: "Auth Model"
создано: "2026-06-05"
обновлено: "2026-06-05"
уровень_достоверности: "высокая"
теги: ["глоссарий", "finance", "auth", "security", "backend"]
источник: "apps/backend/src/app/auth/router.py"
ссылки:
  - "[[MOC_Finance]]"
---

# Auth Model (Модель аутентификации)

## Определение

Модель аутентификации проекта Finance — двухплатформенная система, обеспечивающая регистрацию, логин, управление сессиями и восстановление пароля с единым набором бизнес-правил. Каждая платформа (PWA и Android) использует собственный транспортный механизм доставки токенов, но разделяет общую логику верификации учётных данных, rate limiting и neutral responses.

## Двухплатформенная модель

### PWA (Progressive Web App) — cookie-based

- Сессия доставляется через **HttpOnly + Secure + SameSite** cookie, устанавливаемую сервером
- CSRF-защита: парный CSRF-token выставляется в отдельную читаемую cookie; клиент обязан отправлять значение в заголовке `X-CSRF-Token` при небезопасных методах (POST, PUT, PATCH, DELETE)
- CSRF-токен привязан к сессии и ротируется при login, logout и password reset
- Транспортный контракт: `PwaCookieCsrfContract` в `schemas.py`

### Android — Bearer token

- Аутентификация через заголовок `Authorization: Bearer <opaque_access_token>`
- Access token — непрозрачный opaque-токен с ограниченным TTL
- Refresh token — rotatable-токен с серверной ротацией при каждом использовании; рекомендуемое хранение — Android Keystore / EncryptedSharedPreferences
- Серверная поддержка инвалидации: каждая сессия хранит `session_version`, который сравнивается с версией пользователя; при несовпадении сессия отклоняется
- Транспортный контракт: `AndroidBearerRefreshContract` в `schemas.py`

## Registration flow

1. **Owner** отправляет запрос на регистрацию → система создаёт пользователя с `auth_status=active` и генерирует household
2. Owner приглашает участников через **invite tokens** — одноразовые токены с хешированным хранением и TTL
3. **Member** принимает приглашение → создаётся membership-связь с household
4. При дублировании email сервер возвращает **202 Accepted** с neutral-сообщением, не подтверждая и не отрицая существование аккаунта

## Neutral responses

Ключевой инвариант безопасности: сервер **никогда не раскрывает** существование аккаунта при ошибках аутентификации. Одинаковые по структуре ответы возвращаются для:

- «Аккаунт не существует» и «Неверный пароль» — при логине
- «Email существует» и «Email свободен» — при регистрации (conflict case → 202)
- «Email зарегистрирован» и «Email не найден» — при password reset
- «Инвайт существует» и «Инвайт не найден» — при invite request

Каждый neutral response содержит `flow`, `message`, `status` и `request_id`. Типы потоков: `login_failure`, `password_reset_request`, `invite_request`.

## Rate limiting

Sensitive endpoints защищены **in-memory sliding-window rate limiter**:

- Каждое правило определяется ключом (`RateLimitKey`), лимитом, временным окном и областью действия (IP / email / account / actor / household)
- Конфигурация через runtime settings с возможностью переопределения лимитов при деплое (`with_overrides`)
- Правила требуют отдельного утверждения Product/Security перед релизом
- Rate limit identity для email использует одностороннее хеширование (сервер не хранит IP в открытом виде для ключей на основе email)
- При срабатывании лимита: HTTP 429 + заголовок `Retry-After`

Покрываемые области: registration, login, password reset (request + confirm), invite (create / resend / token), экспорт данных, screenshot OCR.

## Сессии

### Cookie-based (PWA)

- HttpOnly Secure SameSite=Lax cookie с серверным TTL
- При логине/регистрации сервер устанавливает session cookie + CSRF cookie
- При logout — обе cookie удаляются, сессия помечается `revoked`
- Проверка: сервер хеширует plaintext token из cookie → ищет по хешу в хранилище → проверяет `status`, `expires_at`, `session_version`

### Bearer + Refresh (Android)

- Access token: короткоживущий opaque-токен, передаётся в `Authorization`
- Refresh token: длинноживущий, rotatable-токен
- При каждом refresh-обмене старый refresh-токен инвалидируется (rotation)
- `session_version` позволяет массовую инвалидацию всех сессий пользователя

### Ревокация

- Одиночная: `revoke_session` — для logout
- Массовая: `revoke_user_sessions` — для password reset, logout-all, security events

## Password reset

Общий flow (без раскрытия деталей реализации):

1. **Запрос**: пользователь отправляет email → neutral response (не раскрывает наличие аккаунта), защищён rate limiting
2. **Доставка**: если аккаунт существует — генерируется одноразовый токен сброса с TTL, доставляется пользователю
3. **Подтверждение**: пользователь предоставляет токен + новый пароль → верификация токена → обновление пароля → инвалидация всех старых сессий
4. Токен сброса — одноразовый (`consumed` после успешного использования), с защитой от replay

## Audit logging

Принцип логирования действий аутентификации:

- Каждое действие описывается `AuthAuditNote` с action, result, request_id, actor_user_id и details
- **Строгий инвариант**: audit-поля не могут содержать plaintext passwords, session tokens, refresh tokens, CSRF values, invite/reset tokens, token hashes
- Автоматическая редакция: `redact_auth_audit_details` фильтрует ключи, содержащие фрагменты `authorization`, `cookie`, `csrf`, `password`, `secret`, `session`, `token`
- Логируемые действия: `login_attempt`, `logout`, `password_reset_request`, `password_reset_confirm`, `invite_create`, `invite_resend`, `invite_token_attempt`, `session_revoke`
- Результаты: `accepted_neutral`, `succeeded`, `denied_neutral`, `rate_limited`, `release_blocked`

## Связанные термины

- [[MOC_Finance]] — карта проекта Finance
- [[Neutral_Response]] — паттерн нейтральных ответов
- [[Session_Token]] — токены сессий и их жизненный цикл

## Источник

Исходный код модуля аутентификации:

- `apps/backend/src/app/auth/router.py` — HTTP endpoints
- `apps/backend/src/app/auth/service.py` — бизнес-логика и neutral responses
- `apps/backend/src/app/auth/runtime.py` — `AuthSessionService`, DI, credential verification
- `apps/backend/src/app/auth/schemas.py` — DTO и транспортные контракты
- `apps/backend/src/app/auth/cookies.py` — управление PWA cookie
- `apps/backend/src/app/auth/session_tokens.py` — issuance и хранение сессий
- `apps/backend/src/app/auth/invite_tokens.py` — приглашения и invite-токены
- `apps/backend/src/app/auth/password_reset.py` — сброс пароля
- `apps/backend/src/app/auth/security.py` — примитивы безопасности
- `apps/backend/src/app/auth/rate_limits.py` — rate limiting
- `apps/backend/src/app/auth/models.py` — доменные модели
- `apps/backend/src/app/auth/db_stores.py` — SQLAlchemy persistence
- `apps/backend/src/app/auth/identifiers.py` — нормализация идентификаторов
- `apps/backend/src/app/auth/audit_notes.py` — audit logging
