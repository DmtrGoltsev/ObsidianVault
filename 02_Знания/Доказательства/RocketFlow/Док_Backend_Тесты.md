---
id: "proof-backend-tests"
тип: "доказательство"
статус: "выполнено"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: [".github/workflows/backend-verify.yml"]
доказательства: []
теги: ["доказательство", "тесты", "backend", "ci"]
---

# Доказательство: Backend-тесты зелёные

## Что проверено

Полный прогон модульных тестов бэкенда: `mvn test`.

## Кем проверено

CI: backend-verify.yml

## Когда проверено

Автоматически при каждом push/pull_request в backend/.

## Результат

- Все тесты проходят (зелёный билд)
- Используется Embedded PostgreSQL (zonky) для изоляции от внешней БД
- Покрытие: модули auth, accounts, folders, goals, tasks, sharing, calendar, recurrence, reminders, prioritypolicy, notifications

## Ссылка на CI

GitHub Actions → backend-verify.yml

## Связанные заметки

- [[MOC_Бэкенд]]
- [[Регламент_CI_CD]]
