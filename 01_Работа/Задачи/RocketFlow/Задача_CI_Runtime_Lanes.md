---
id: "task-ci-runtime-lanes"
тип: "задача"
статус: "черновик"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "средняя"
источники: [".github/workflows/web-verify.yml", ".github/workflows/android-verify.yml"]
доказательства: ["Док_Web_Build", "Док_Android_Build"]
теги: ["задача", "ci", "тестирование", "web", "android"]
---

# Задача: Добавление runtime-верификации в CI

## Описание

Расширить CI-воркфлоу web и Android: добавить runtime-тесты дополнительно к текущей build-only проверке.

## Контекст

Сейчас:
- **web-verify.yml** — только `npm run build` (build-only)
- **android-verify.yml** — только `assembleDebug` (build-only)

Требуется добавить:
- **Web**: Jest unit-тесты + Playwright E2E (или аналог)
- **Android**: Robolectric unit-тесты + эмуляторные тесты

## Критерии приёмки

- [ ] web-verify.yml запускает `npm test` (Jest) после сборки
- [ ] android-verify.yml запускает Robolectric-тесты после сборки
- [ ] Падение тестов блокирует merge PR
- [ ] Время CI не превышает 15 минут

## Связанные заметки

- [[MOC_Веб]]
- [[MOC_Android]]
- [[Регламент_CI_CD]]
- [[Док_Web_Build]]
- [[Док_Android_Build]]
