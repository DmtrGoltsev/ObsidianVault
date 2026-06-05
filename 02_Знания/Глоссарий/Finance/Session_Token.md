---
id: "term-session-token"
тип: "термин"
проект: "Finance"
термин: "Сессионный токен"
термин_en: "Session Token"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/auth/session_tokens.py, apps/backend/src/app/auth/cookies.py, apps/backend/src/app/auth/schemas.py"
ссылки:
  - "[[MOC_Finance]]"
---

Opaque-токен сессии для аутентификации пользователя. Два транспорта: PWA (cookie-based) и Android (bearer + refresh). Хранение — только хеш токена, plaintext возвращается клиенту однократно.

## Ключевые аспекты

- **PWA cookie**: HttpOnly cookie `__Host-finance_session` + readable CSRF cookie `finance_csrf`, TTL ~12ч
- **Android bearer**: opaque `accessToken` в Authorization header + refresh token в secure storage, TTL refresh ~30 дней
- **Хранение**: `SessionStorageRecord` — только `session_token_hash`, `csrf_token_hash`, `refresh_token_hash`
- **IssuedSession**: boundary object с plaintext-токенами, возвращается клиенту один раз при создании
- **Статусы**: `active`, `revoked`, `expired` — revocation через `revoke_session` / `revoke_user_sessions`

## Связанные термины

- [[Neutral_Response]] — neutral failure при логине
- [[Rate_Limiting]] — защита endpoints выдачи токенов
