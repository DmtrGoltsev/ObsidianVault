---
id: "term-neutral-response"
тип: "термин"
проект: "Finance"
термин: "Нейтральный ответ"
термин_en: "Neutral Response"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/auth/service.py, apps/backend/src/app/auth/schemas.py"
ссылки:
  - "[[MOC_Finance]]"
---

Паттерн ответа auth-endpoint, при котором сервер возвращает одинаковое сообщение для всех исходов (успех/неудача/отсутствие ресурса), не раскрывая существование учётной записи, invite или email.

## Ключевые аспекты

- **Три потока**: `login_failure`, `password_reset_request`, `invite_request` — enum `NeutralFlow`
- **Формат**: `NeutralPublicResponse` с полями `flow`, `message`, `status`, `request_id`
- **Login**: при неверных кредах — `Unable to complete login with the supplied credentials.` (HTTP 401)
- **Registration conflict**: при существующем email — HTTP 202 с одинаковым сообщением (не раскрывает, что email занят)
- **Headers**: все auth-ответы содержат `Cache-Control: private, no-store`

## Связанные термины

- [[Rate_Limiting]] — rate limit также возвращает neutral message
- [[Session_Token]] — создание сессии после успешного login
