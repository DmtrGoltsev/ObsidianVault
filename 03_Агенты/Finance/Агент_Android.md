---
id: "agent-finance-android"
тип: "агент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["агент", "finance", "android", "mobile"]
ссылки:
  - "[[MOC_Finance]]"
---

# Агент Android — Finance

## Зона ответственности

Нативный Android-клиент: on-device OCR (ML Kit Text Recognition v2),
capture parser, session management, Jetpack Compose UI.

## Стек

- Kotlin 1.9, Jetpack Compose
- ML Kit Text Recognition v2
- compileSdk 34, minSdk 26
- JUnit 5, Turbine

## Права на решения

- Изменение `apps/android/` (ui, data, domain, ocr, navigation)

## Активные задачи

- [ ] On-device OCR pipeline (ML Kit)
- [ ] Capture parser → structured transaction draft
- [ ] Session management, auth flow
- [ ] Compose UI: capture, review, history

## Связанные заметки

- [[MOC_Finance]]
- [[Finance]]
