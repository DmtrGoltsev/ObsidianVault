---
id: "pkg-ios"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md", "docs/33-current-state-summary.md"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["пакет_контекста", "ios", "rocketflow"]
---

# Пакет контекста: iOS

## Назначение

Короткий handoff для [[Агент_iOS|iOS-агента]], reviewer или интегратора. Детали не дублируются: архитектура — [[MOC_iOS]], установка на Mac/iPhone — [[Пакет_iOS_Mac_Установка]], exact CI — [[Док_iOS_Verification]], общий проект — [[RocketFlow]].

## Текущая точка

- Current repo docs HEAD на branch `codex/native-ios-companion`: `b75ca723f767f520bee39ea72052b1a4b03a7e59`.
- Immutable tooling evidence: SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`, [run 32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719), job `97269056380`; Mac contracts `174/174`, unit `540/0`, UI `2/0`, artifacts `9501177125` (`1,317,064` bytes) и `9501179599` (`25,070` bytes).
- Отдельное immutable app behavior/build evidence: SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, run `32655691351`; оно не является текущим branch HEAD или tooling identity.
- iOS 16+, Planner/Calendar/Focus, GRDB offline/sync/conflicts, details/editors/sharing, reminders, RU/EN, restoration/deep links, account safety.
- [Behavior iOS Verify run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351) green: parity/packages/build, `540` unit + `2` UI.
- Feature push auto run `0` действует только на candidate branch; manual verify доступен, а PR/master policy станет default behavior только после merge. Production workflows и branch protection не менялись; [[MOC_DevOps]].
- Simulator clone/build и Mac handoff tooling — **GO**; physical iPhone install ещё внешний непроверенный шаг, App Store/public release — **NO-GO** до внешних гейтов.

## Source of truth

- [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/70-native-ios-parity-contract.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/71-native-ios-delivery.md) — living parity/delivery docs.
- [`docs/ios-native-mac-codex-install-prompt.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/ios-native-mac-codex-install-prompt.md), [`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/72-native-ios-mac-device-handoff.md) — canonical Mac Codex prompt и human handoff.
- [`ios/README.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/ios/README.md) — living toolchain и local/CI commands.
- [`ios/project.yml`](https://github.com/DmtrGoltsev/RocketFlow/blob/35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3/ios/project.yml) — XcodeGen source of truth.
- [`AGENTS.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/AGENTS.md) — актуальные agent instructions.

## Production и внешние гейты

Production server: SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`). Candidate V22 для iOS device registrations не deployed; backend/DB не менялись и DB в этой задаче не проверялась. Для personal `no-push` handoff нужны Mac, Apple Account/Team, уникальный bundle ID и iPhone. Push optional и дополнительно требует `GoogleService-Info.plist`, APNs/Firebase и production V22; App Store также блокируют HTTPS и real-device/accessibility/manual acceptance.

## Когда использовать

- Перед iOS implementation/review/CI recovery.
- Перед установкой на iPhone использовать [[Пакет_iOS_Mac_Установка]].
- При handoff между [[Оркестратор]], [[Агент_iOS]], [[Агент_QA]] и [[Агент_DevOps]].
- Для release claim всегда переходить к [[Док_iOS_Verification]] и [[Док_Prod_Deploy_State]].
