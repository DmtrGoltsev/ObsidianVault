---
id: "agent-ios"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["AGENTS.md", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md", "ios/project.yml"]
доказательства: ["Док_iOS_Verification"]
теги: ["агент", "ios", "swift", "swiftui"]
---

# Агент iOS

## Зона ответственности

- Native iOS 16+ на Swift/SwiftUI.
- Planner, Calendar, Focus, details/editors/sharing и RU/EN accessibility.
- GRDB persistence, account isolation, sync/conflicts и terminal-auth cleanup.
- Reminders, deep links и durable navigation restoration.
- XcodeGen project parity, Swift package lock parity и simulator verification.
- Mac handoff, signed personal `no-push` build и redacted physical-device evidence.

## Источники истины

1. Project instructions на docs HEAD `b75ca723f767f520bee39ea72052b1a4b03a7e59`: [`AGENTS.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/AGENTS.md), [`Ru_OrchestratorRules.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/Ru_OrchestratorRules.md), [`Ru_SubagentFirstFinishNew.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/Ru_SubagentFirstFinishNew.md).
2. Living iOS docs: [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/70-native-ios-parity-contract.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/71-native-ios-delivery.md), [`ios/README.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/ios/README.md).
3. Mac execution: [`docs/ios-native-mac-codex-install-prompt.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/ios-native-mac-codex-install-prompt.md) и [`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/72-native-ios-mac-device-handoff.md); vault entry — [[Пакет_iOS_Mac_Установка]].
4. Immutable tooling evidence: SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`, run `32669924719`, job `97269056380`, contracts `174/174`, unit `540`, UI `2`, artifacts `9501177125` и `9501179599`.
5. Immutable behavior source: [`ios/project.yml`](https://github.com/DmtrGoltsev/RocketFlow/blob/35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3/ios/project.yml), app SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, run `32655691351`.
6. Vault handoff/evidence: [[Пакет_iOS]], [[MOC_iOS]], [[Док_iOS_Verification]].

## Definition of done

- `project.yml`, generated project и `Package.resolved` проходят fail-closed parity checks.
- Unsigned simulator build и unit/UI tests зелёные на exact SHA.
- Account-scoped offline/sync/navigation behavior покрыт regression tests.
- Evidence содержит run/job/test counts/artifact IDs и не смешивает simulator readiness с App Store readiness.
- Physical device success заявляется только после redacted Mac evidence; canonical flow выполняется default `no-push`, push остаётся optional.

## Ограничения решений

- Не заявлять production push до deploy V22 и настройки APNs/Firebase.
- Не добавлять секреты или `GoogleService-Info.plist` в vault/repository.
- Не считать unsigned simulator CI доказательством Apple signing, real-device или App Store acceptance.
- В рамках personal handoff не выполнять backend deploy и не проверять production DB.
- Любая исходная пользовательская задача основного чата сначала проходит planner по project `AGENTS.md`; ограниченный subagent собственного planner не запускает, если это не поручено.

## Связанные заметки

- [[Агент_QA]], [[Агент_DevOps]], [[Оркестратор]]
- [[MOC_Бэкенд]], [[MOC_DevOps]]
- [[Источник_Текущее_Состояние]]
