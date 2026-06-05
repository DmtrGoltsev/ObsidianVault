---
id: "adr-finance-0002"
тип: "решение"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["ADR", "finance", "архитектура", "auth", "безопасность"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[ADR_0001_Stack_Repo_Layout]]"
---

# ADR-0002: Двухплатформенная модель аутентификации

## Статус

Утверждено. Реализовано в `apps/backend/src/app/auth/`.

## Контекст

Finance MVP работает на двух клиентских платформах: PWA (браузер) и Android (нативное приложение). Каждая платформа имеет свои ограничения безопасности:

- **PWA** работает в браузерном sandbox. Токены в JavaScript доступны XSS-атакам. LocalStorage не подходит для хранения session-cred. Требуется защита от CSRF при cookie-based аутентификации.
- **Android** — нативное приложение. Не подвержено CSRF и XSS. Имеет доступ к Android Keystore для аппаратного шифрования. Носит токен в памяти и `EncryptedSharedPreferences`.

Единая модель (JWT везде или session-only) ухудшает безопасность хотя бы одной платформы.

## Решение

Две параллельные транспортные модели аутентификации с общим server-side ядром:

### PWA: Cookie-based sessions

- **HttpOnly + Secure + SameSite** cookie с opaque session token. Клиент не имеет JavaScript-доступа к cookie.
- Отдельный читаемый CSRF cookie (не HttpOnly) — значение передаётся в заголовке для unsafe-методов (POST, PUT, PATCH, DELETE).
- TTL сессии: 12 часов (`pwa_session_ttl`).
- `AuthClientKind.PWA` — сервер различает PWA-клиентов.

### Android: Bearer + rotating refresh

- Opaque bearer access token в заголовке `Authorization: Bearer <token>`.
- Rotating refresh token для продления сессии, хранится в `EncryptedSharedPreferences` с AES256-GCM через Android Keystore (`MasterKey.KeyScheme.AES256_GCM`).
- TTL refresh: 30 дней (`android_refresh_ttl`).
- `AuthClientKind.ANDROID` — сервер различает Android-клиентов.

### Общие механизмы

- **Neutral responses** — ошибки логина, регистрации, reset, invite не раскрывают существование аккаунта (`neutral_login_failure_response`, `neutral_password_reset_request_response`).
- **Rate limiting** — In-memory rate limiter с бакетами по IP и email (login, registration, password reset, invite).
- **Session versioning** — каждая сессия имеет `session_version` для инвалидации при критических событиях (password reset, logout-all).
- **Hash-only storage** — в БД хранятся только хеши токенов, никогда plaintext.
- **Cache-Control: private, no-store** — все auth-ответы запрещают кэширование.

## Альтернативы

1. **JWT везде** — отклонено. PWA хранение JWT в localStorage создаёт XSS-риск. HttpOnly cookie с JWT порождает проблему отзывability (нужен revocation list, сложнее чем opaque token).
2. **OAuth2 provider** — отклонено. MVP не требует third-party авторизации. Добавляет infrastructure overhead без пропорционального gain.
3. **Session-only (server-side)** — отклонено для Android. Нативному приложению не нужна CSRF-защита, bearer token + secure storage проще и безопаснее.

## Последствия

### Положительные

- Каждая платформа использует оптимальный для неё механизм безопасности.
- PWA защищена от XSS-кражи токенов (HttpOnly) и CSRF (double-submit cookie).
- Android токены аппаратно зашифрованы в Keystore.
- Neutral responses предотвращают user enumeration.

### Издержки

- Две реализации хранения на клиентах (cookie logic для PWA, Keystore logic для Android).
- Серверный `session_creation_response` branching по `AuthTransport` — два пути сериализации ответа.
- Выпущенные release blockers: production wiring хеширования, persistent session store, CSRF rotation, refresh-token rotation.

## Ссылки

- `apps/backend/src/app/auth/router.py` — маршруты login/register/logout, branching по transport
- `apps/backend/src/app/auth/cookies.py` — set/clear PWA cookies (HttpOnly + CSRF)
- `apps/backend/src/app/auth/session_tokens.py` — `SessionTokenService`, `issue_pwa_cookie_session`, `issue_android_tokens`
- `apps/backend/src/app/auth/models.py` — `AuthClientKind`, `SessionStorageRecord`, `TokenRecordStatus`
- `apps/backend/src/app/auth/service.py` — neutral responses, release blockers
- `apps/backend/src/app/auth/security.py` — `RandomTokenFactory`, `TokenHashingBackend`
- `apps/android/app/src/main/java/com/finance/mvp/session/TokenStore.kt` — `AndroidSecureTokenStore`, EncryptedSharedPreferences
