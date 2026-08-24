---
id: "moc-ios"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md", "docs/33-current-state-summary.md", "ios/project.yml"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["moc", "ios", "swiftui", "rocketflow"]
---

# MOC iOS

Точка входа для native RocketFlow iOS 16+. Current repo docs HEAD на branch `codex/native-ios-companion`: `99172cd171e8cade0545fb442c9233961c7865d1`. Immutable tooling evidence отдельно: `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` / run `32669924719`; app behavior/build evidence отдельно: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` / run `32655691351`. Branch HEAD не приравнивается ни к одной evidence identity.

## Функциональный контур

- три основные вкладки: Planner, Calendar, Focus;
- offline persistence на GRDB, sync и conflict handling;
- детали, редакторы и sharing;
- reminders, RU/EN localization;
- durable navigation restoration и deep links;
- account-scoped safety и очистка состояния.

Living contract: [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/70-native-ios-parity-contract.md), delivery: [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/71-native-ios-delivery.md), canonical Mac prompt: [`docs/ios-native-mac-codex-install-prompt.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/ios-native-mac-codex-install-prompt.md), human handoff: [`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/72-native-ios-mac-device-handoff.md), toolchain/configuration: [`ios/README.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/ios/README.md). Immutable verified XcodeGen behavior source: [`ios/project.yml`](https://github.com/DmtrGoltsev/RocketFlow/blob/35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3/ios/project.yml).

## Verification

[[Док_iOS_Verification]] раздельно фиксирует behavior run `32655691351` и tooling run `32669924719`: job `97269056380`, contracts `174/174`, unit `540/0`, UI `2/0`, artifacts `9501177125` (`1,317,064` bytes) и `9501179599` (`25,070` bytes). [[MOC_DevOps]] фиксирует уже действующую `origin/master` trigger policy, эквивалентную candidate policy и границы старых branches.

## Server boundary

Production backend/web остаётся на SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); release checks используют preflight `>=20`, manifest/post `>=21`. Candidate V22 для iOS device registrations существует только в repository; без его production deploy iOS push end-to-end не заявляется. Production DB здесь не проверялась.

## Release verdict

- **GO:** clone, XcodeGen/package parity, unsigned build и simulator tests на Mac; tooling готовит default `no-push` personal device flow.
- **Внешний шаг:** physical iPhone build/install/launch на Mac с Apple Account/Team, уникальным bundle ID и выбранным device; успех ещё не доказан.
- **NO-GO:** App Store/public release до внешних signing/push/HTTPS/accessibility gates. Push optional и требует `GoogleService-Info.plist`, APNs/Firebase и deployed V22.

## Связанные заметки

- [[Пакет_iOS]] — компактный handoff
- [[Пакет_iOS_Mac_Установка]] — установка на другом Mac и personal iPhone
- [[Агент_iOS]] — роль исполнителя
- [[MOC_RocketFlow]], [[MOC_Бэкенд]], [[MOC_DevOps]] — соседние карты
- [[Источник_Текущее_Состояние]] — общий current state
