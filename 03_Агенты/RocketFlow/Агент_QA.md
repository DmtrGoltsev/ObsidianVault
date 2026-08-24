---
id: "agent-qa"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/06-qa-strategy.md", "docs/33-current-state-summary.md", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", ".github/workflows/ios-verify.yml"]
доказательства: ["Док_iOS_Verification", "Док_Android_Verification", "Док_Backend_Verification", "Док_Web_Verification"]
теги: ["агент", "qa", "тестирование"]
---

# Агент QA

## Зона ответственности

- Backend unit tests (JUnit)
- Backend integration tests (Embedded PostgreSQL zonky)
- Web build verification (`npm run build`)
- Android Robolectric tests (4.12.2)
- iOS XcodeGen/package parity, unsigned simulator build, unit и UI tests
- Notification E2E smoke ([[FCM]] push-tap flow)
- Валидация API контрактов
- Proof-документирование результатов

## Инструменты

- JUnit 5 + Embedded PostgreSQL (zonky)
- Robolectric 4.12.2 для Android unit-тестов
- macOS GitHub Actions, Xcode/XCTest и `.xcresult` для native iOS
- Скрипт smoke: `scripts/Start-NotificationSmokeBackend.ps1`

## Текущий iOS gate

- Current repo docs HEAD: `99172cd171e8cade0545fb442c9233961c7865d1`; immutable tooling SHA отдельно: `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`; tested app behavior SHA отдельно: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`.
- [Run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`: parity/packages/build PASS, `540` unit + `2` UI tests PASS.
- [Tooling run 32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719), job `97269056380`: Mac contracts `174/174`, unit `540/0`, UI `2/0`, artifacts `9501177125` и `9501179599`.
- Exact artifact IDs/digests и coverage boundary: [[Док_iOS_Verification]].
- Green simulator/tooling CI разрешает clone/build verification и handoff на Mac, но physical iPhone install ещё не доказан и App Store claim запрещён.

## Права на решения

- Определение критериев качества
- Блокировка релиза при падении тестов
- Требование доказательств от других агентов

## Активные задачи

- Staging notification certification
- Валидация текущего candidate `codex/native-ios-companion`; MVP3 сохраняется только как historical baseline
- Поддержание зелёных CI-воркфлоу
- Real-device, RU/EN accessibility и manual acceptance для iOS до public release

## Выполненные волны

- Wave A: backend API validation
- Wave B: scheduling validation
- Wave C: notification E2E proof

## Связанные заметки

- [[Источник_QA_Стратегия]] — стратегия тестирования
- [[Регламент_Нотификационного_Смока]] — smoke-процедура
- [[Источник_Нотификация_Пруф]] — результаты proof
- [[RocketFlow]] — проект
- [[MOC_iOS]], [[Пакет_iOS]], [[Пакет_iOS_Mac_Установка]], [[Агент_iOS]] — iOS контекст
- [[MOC_DevOps]] — trigger policy уже в `origin/master`; green Android/Backend/Web evidence и границы старых branches
- [[Док_iOS_Verification]] — exact iOS evidence и незакрытые внешние гейты
