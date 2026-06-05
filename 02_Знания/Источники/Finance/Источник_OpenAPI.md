---
id: "source-openapi"
тип: "источник"
проект: "Finance"
название: "Источник — OpenAPI"
файл: "api/openapi/openapi.yaml"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["источник", "finance"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
---

# Источник — OpenAPI

## Файл-источник

`api/openapi/openapi.yaml`

## Содержит

OpenAPI 3.1.0 спецификацию REST API Finance — единый source of truth для контракта между клиентом и сервером.

## Ключевые данные

- ~2364 строк; описывает все endpoint'ы, request/response DTO, схемы аутентификации (Bearer JWT, API Key)
- Покрывает ресурсы: transactions, accounts, categories, households, memberships, analytics, capture-drafts
- Включает `components/schemas` с полными моделями данных и примерами (examples)
