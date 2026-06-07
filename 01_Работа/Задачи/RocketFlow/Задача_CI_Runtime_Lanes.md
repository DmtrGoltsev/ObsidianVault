---
id: "task-ci-runtime-lanes"
тип: "задача"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "средняя"
источники: [".github/workflows/web-verify.yml", ".github/workflows/android-verify.yml"]
доказательства: ["Док_Web_Build", "Док_Android_Build"]
теги: ["задача", "ci", "тестирование", "web", "android"]
---

# Задача: Добавление runtime-верификации в CI

## Описание

Закрыть runtime-verification gaps в web и Android после cleanup/repo audit.

## Контекст

Сейчас:
- **web-verify.yml** — `npm run build`; web test scripts отсутствуют.
- **android-verify.yml** — больше не build-only: unit/build/lint lane.

Требуется добавить:
- **Web**: test scripts и минимальный runtime/unit lane (Jest/Vitest + Playwright или аналог).
- **Android**: финальный post-cleanup verifier и отдельный instrumented/runtime lane при необходимости.

## Критерии приёмки

- [ ] web имеет test scripts и CI запускает их после сборки
- [ ] android unit/build/lint lane подтверждён актуальным evidence
- [ ] Android instrumented/runtime verifier либо добавлен в CI, либо явно вынесен в отдельный регламентированный gate
- [ ] Падение тестов блокирует merge PR
- [ ] Время CI не превышает 15 минут

## Связанные заметки

- [[MOC_Веб]]
- [[MOC_Android]]
- [[Регламент_CI_CD]]
- [[Док_Web_Build]]
- [[Док_Android_Build]]
- [[Док_Web_Verification]]
- [[Док_Android_Verification]]
