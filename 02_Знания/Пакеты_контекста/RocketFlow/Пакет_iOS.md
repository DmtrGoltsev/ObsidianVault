---
id: "pkg-ios"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-23"
уверенность: "высокая"
источники: ["docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "ios/README.md", "docs/33-current-state-summary.md"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["пакет_контекста", "ios", "rocketflow"]
---

# Пакет контекста: iOS

## Назначение

Короткий handoff для [[Агент_iOS|iOS-агента]], reviewer или интегратора. Детали не дублируются: архитектура — [[MOC_iOS]], exact CI — [[Док_iOS_Verification]], общий проект — [[RocketFlow]].

## Текущая точка

- Current repo docs HEAD на branch `codex/native-ios-companion`: `201a3de8657e56a3a67e1051522cb5793ce5c0b7`.
- Immutable app-code/build evidence: SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, run `32655691351`; это не утверждение о текущем branch HEAD.
- iOS 16+, Planner/Calendar/Focus, GRDB offline/sync/conflicts, details/editors/sharing, reminders, RU/EN, restoration/deep links, account safety.
- [iOS Verify run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351) green: parity/packages/build, `540` unit + `2` UI.
- CI scheduling `0bbf4acb` пока candidate-only; default branch `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb` без `ios-verify`, подробности [[MOC_DevOps]].
- Simulator clone/build — **GO**; App Store/public release — **NO-GO** до внешних гейтов.

## Source of truth

- [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/70-native-ios-parity-contract.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/71-native-ios-delivery.md) — living parity/delivery docs.
- [`ios/README.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/ios/README.md) — living toolchain и local/CI commands.
- [`ios/project.yml`](https://github.com/DmtrGoltsev/RocketFlow/blob/35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3/ios/project.yml) — XcodeGen source of truth.
- [`AGENTS.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/AGENTS.md) — актуальные agent instructions.

## Production и внешние гейты

Production server: SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`. Candidate V22 для iOS device registrations не deployed; DB в этой задаче не проверялась. Открыты Apple signing/team, `GoogleService-Info.plist` + APNs/Firebase, V22 deploy, HTTPS, real-device/accessibility/manual acceptance.

## Когда использовать

- Перед iOS implementation/review/CI recovery.
- При handoff между [[Оркестратор]], [[Агент_iOS]], [[Агент_QA]] и [[Агент_DevOps]].
- Для release claim всегда переходить к [[Док_iOS_Verification]] и [[Док_Prod_Deploy_State]].
