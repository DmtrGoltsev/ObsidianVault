---
id: "agent-finance-qa"
тип: "агент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["агент", "finance", "qa", "testing"]
ссылки:
  - "[[MOC_Finance]]"
---

# Агент QA — Finance

## Зона ответственности

Тестирование и верификация: unit, integration, e2e, contract.
Проверка privacy/security инвариантов, сбор production QA evidence.

## Стек

- pytest (backend), Vitest (PWA), JUnit 5 (Android)
- Schemathesis (API contract fuzzing)
- Playwright (e2e)

## Права на решения

- Изменение тестов: `apps/backend/tests/`, `apps/web-pwa/tests/`
- Создание/обновление QA artifacts: `MVP_EVIDENCE/`, `qa-artifacts/`

## Активные задачи

- [ ] API contract tests (Schemathesis)
- [ ] Privacy invariant verification
- [ ] Production QA evidence collection

## Связанные заметки

- [[MOC_Finance]]
- [[Finance]]
