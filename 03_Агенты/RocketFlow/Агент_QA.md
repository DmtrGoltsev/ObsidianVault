---
id: "agent-qa"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-23"
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

- Current repo docs HEAD: `201a3de8657e56a3a67e1051522cb5793ce5c0b7`; immutable tested app SHA отдельно: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`.
- [Run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`: parity/packages/build PASS, `540` unit + `2` UI tests PASS.
- Exact artifact IDs/digests и coverage boundary: [[Док_iOS_Verification]].
- Green simulator CI разрешает clone/build verification на Mac, но не App Store claim.

## Права на решения

- Определение критериев качества
- Блокировка релиза при падении тестов
- Требование доказательств от других агентов

## Активные задачи

- Staging notification certification
- Валидация MVP3 изменений
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
- [[MOC_iOS]], [[Пакет_iOS]], [[Агент_iOS]] — iOS контекст
- [[MOC_DevOps]] — candidate trigger policy; `origin/master` изменится только после merge
- [[Док_iOS_Verification]] — exact iOS evidence и незакрытые внешние гейты
