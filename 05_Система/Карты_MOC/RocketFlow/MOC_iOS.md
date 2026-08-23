---
id: "moc-ios"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-23"
уверенность: "высокая"
источники: ["docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "ios/README.md", "docs/33-current-state-summary.md", "ios/project.yml"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["moc", "ios", "swiftui", "rocketflow"]
---

# MOC iOS

Точка входа для native RocketFlow iOS 16+. Current repo docs HEAD на branch `codex/native-ios-companion`: `201a3de8657e56a3a67e1051522cb5793ce5c0b7`. Отдельное immutable app-code/build evidence: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` и run `32655691351`; branch HEAD не приравнивается к app SHA.

## Функциональный контур

- три основные вкладки: Planner, Calendar, Focus;
- offline persistence на GRDB, sync и conflict handling;
- детали, редакторы и sharing;
- reminders, RU/EN localization;
- durable navigation restoration и deep links;
- account-scoped safety и очистка состояния.

Living contract: [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/70-native-ios-parity-contract.md), delivery: [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/71-native-ios-delivery.md), toolchain/configuration: [`ios/README.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/ios/README.md). Immutable verified XcodeGen source: [`ios/project.yml`](https://github.com/DmtrGoltsev/RocketFlow/blob/35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3/ios/project.yml).

## Verification

[[Док_iOS_Verification]] фиксирует exact run `32655691351`, job `97233929959`, green parity/packages/build, `540` unit + `2` UI tests и оба artifact ID. [[MOC_DevOps]] фиксирует trigger policy и границы CI.

## Server boundary

Production backend/web остаётся на SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); release checks используют preflight `>=20`, manifest/post `>=21`. Candidate V22 для iOS device registrations существует только в repository; без его production deploy iOS push end-to-end не заявляется. Production DB здесь не проверялась.

## Release verdict

- **GO:** clone, XcodeGen/package parity, unsigned build и simulator tests на Mac.
- **NO-GO:** App Store/public release до Apple signing/team, `GoogleService-Info.plist` + APNs/Firebase, V22 deploy, HTTPS, real-device/accessibility/manual acceptance.

## Связанные заметки

- [[Пакет_iOS]] — компактный handoff
- [[Агент_iOS]] — роль исполнителя
- [[MOC_RocketFlow]], [[MOC_Бэкенд]], [[MOC_DevOps]] — соседние карты
- [[Источник_Текущее_Состояние]] — общий current state
