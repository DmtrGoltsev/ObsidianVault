---
id: "proof-web-build"
тип: "доказательство"
статус: "выполнено"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: [".github/workflows/web-verify.yml"]
доказательства: ["Док_Web_Verification"]
теги: ["доказательство", "сборка", "web", "ci"]
---

# Доказательство: Web build зелёный

## Что проверено

Полная production-сборка веб-клиента: `npm ci` + `npm run build`.

## Кем проверено

CI: web-verify.yml

## Когда проверено

Автоматически при каждом push/pull_request в web/; эта запись является historical/last recorded evidence, а не fresh gate для текущего HEAD `21f95c1`.

## Результат

- Last recorded web build завершается успешно (зелёный билд); канонический verification-док содержит актуальную оговорку, а текущий HEAD `21f95c1` требует fresh evidence.
- Vite 5 генерирует статические файлы (JS, CSS, HTML)
- TypeScript-компиляция без ошибок
- Audit 2026-06-07: web test scripts отсутствуют; см. [[Док_Web_Verification]]

## Ограничение

Сборка build-only: runtime-тесты (Playwright, Jest) не запускаются. См. [[Задача_CI_Runtime_Lanes]].

## Ссылка на CI

GitHub Actions → web-verify.yml

## Связанные заметки

- [[MOC_Веб]]
- [[Регламент_CI_CD]]
- [[Док_Web_Verification]]
