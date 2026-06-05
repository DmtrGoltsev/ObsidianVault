---
id: "term-rate-limiting"
тип: "термин"
проект: "Finance"
термин: "Rate limiting"
термин_en: "Rate Limiting"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/auth/rate_limits.py"
ссылки:
  - "[[MOC_Finance]]"
---

Ограничение частоты запросов на публичных auth-endpoints для защиты от брутфорса и злоупотреблений. Реализовано как sliding-window in-memory rate limiter с конфигурируемыми правилами.

## Ключевые аспекты

- **Архитектура**: `InMemoryRateLimiter` — sliding-window на deque + monotonic clock, thread-safe через Lock
- **Ключи идентификации**: по IP (`auth_rate_limit_identity_for_ip`), по email hash (`auth_rate_limit_identity_for_email`), по actor hash
- **Конфигурация**: `RateLimitConfig` с дефолтами из ADR и методом `with_overrides()` для deployment-overrides
- **Ответ 429**: заголовок `Retry-After`, neutral message `Too many requests.`
- **Все лимиты pending**: каждое правило отмечено `pending_product_security_approval=True` — требуют подтверждения до production

## Связанные термины

- [[Neutral_Response]] — нейтральные ответы при rate limit и ошибках auth
- [[Session_Token]] — защищаемые endpoints (login, registration)
