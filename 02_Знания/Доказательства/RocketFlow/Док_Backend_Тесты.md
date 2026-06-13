---
id: "proof-backend-tests"
тип: "доказательство"
статус: "выполнено"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-08"
уверенность: "высокая"
источники: [".github/workflows/backend-verify.yml", "backend package 2026-06-08"]
доказательства: ["Док_Backend_Verification"]
теги: ["доказательство", "тесты", "backend", "ci"]
---

# Доказательство: Backend-тесты зелёные

## Что проверено

Полный прогон модульных тестов бэкенда: `mvn test`.

## Кем проверено

CI: backend-verify.yml

## Когда проверено

Автоматически при каждом push/pull_request в backend/; эта запись является historical/last recorded evidence, а не fresh verification для текущего HEAD `21f95c1`.

## Результат

- Last recorded backend tests проходят (зелёный билд); это historical evidence, а не fresh verification для текущего HEAD `21f95c1`.
- Local package 2026-06-08: `mvn --batch-mode --no-transfer-progress package` прошёл на втором запуске; `Tests run: 63, Failures: 0, Errors: 0, Skipped: 0`, `BUILD SUCCESS`, total `02:42`, finished `2026-06-08T11:50:48+03`
- Используется Embedded PostgreSQL (zonky) для изоляции от внешней БД
- Покрытие: модули auth, accounts, folders, goals, tasks, sharing, calendar, recurrence, reminders, prioritypolicy, notifications
- Audit 2026-06-07: backend inventory — 16 test files / 63 tests; см. [[Док_Backend_Verification]]

## Ссылка на CI

GitHub Actions → backend-verify.yml

## Связанные заметки

- [[MOC_Бэкенд]]
- [[Регламент_CI_CD]]
- [[Док_Backend_Verification]]
