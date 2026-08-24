---
id: "proof-ios-verification-2026-08-23"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["GitHub Actions run 32655691351", "job 97233929959", "GitHub Actions run 32669924719", "job 97269056380", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md"]
доказательства: ["GitHub artifact 9497494137", "GitHub artifact 9497494432", "GitHub artifact 9501177125", "GitHub artifact 9501179599", "Док_Prod_Deploy_State"]
теги: ["доказательство", "ios", "ci", "tests", "release-gate"]
---

# Док: iOS Verification 2026-08-24

## Что доказано

На branch `codex/native-ios-companion` существуют две отдельные immutable evidence identity. Behavior/build SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` доказывает app behavior через run `32655691351`. Tooling SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` доказывает Mac handoff scripts/contracts через run `32669924719`. Финальный docs HEAD `b75ca723f767f520bee39ea72052b1a4b03a7e59` содержит canonical prompt/handoff, но не подменяет ни одну evidence identity.

## Exact CI evidence

| Поле | Значение |
|---|---|
| Workflow run | [32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), `success` |
| Job | [97233929959](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351/job/97233929959), `Generate, build, and test`, `success` |
| Verified app source | `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` on `codex/native-ios-companion` at run time |
| Current docs HEAD | `b75ca723f767f520bee39ea72052b1a4b03a7e59` on `codex/native-ios-companion` |
| Tests | `540` unit + `2` UI, PASS |
| Result artifact | `RocketFlow-xcresult`, ID `9497494137`, digest `sha256:73610a53af8e2443e727083dd0f625ee327400b92b94f975d1b6ad97f10f0d48` |
| Project artifact | `RocketFlow-xcodeproj-xcodegen-2.46.0`, ID `9497494432`, digest `sha256:5825b9347d985d3218d217c7541c138887ed3aad96760c396369144449d2150f` |

Green steps включают Xcode selection/reporting, XcodeGen 2.46.0 install, generation/parity, package resolution/lock parity, dynamic simulator selection, build/test without signing, xcresult validation и загрузку обоих artifacts.

## Exact Mac tooling evidence

| Поле | Значение |
|---|---|
| Workflow run | [32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719), `success` |
| Job | [97269056380](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719/job/97269056380), `success` |
| Tooling source | `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` |
| Mac contracts | `174/174` PASS, `0` skipped |
| Build gates | XcodeGen `2.46.0`, generated-project parity, packages/lock и simulator build PASS |
| Tests | unit `540` passed / `0` failed; UI `2` passed / `0` failed; total `542/0` |
| Result artifact | `RocketFlow-xcresult`, ID `9501177125`, `1,317,064` bytes |
| Project artifact | `RocketFlow-xcodeproj-xcodegen-2.46.0`, ID `9501179599`, `25,070` bytes |

Tooling run доказывает fail-closed Mac handoff contract, но не физическую установку на iPhone. Canonical выполнение: [[Пакет_iOS_Mac_Установка]].

## Product coverage

Native iOS 16+ содержит Planner, Calendar и Focus, offline GRDB/sync/conflicts, details/editors/sharing, reminders, RU/EN, durable restoration/deep links и account safety. Living contract/delivery docs: [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/70-native-ios-parity-contract.md) и [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/71-native-ios-delivery.md). Build/test identity остаётся behavior SHA из таблицы; Mac tooling identity остаётся отдельной.

## Factual boundary

- **GO:** clean clone/generation/package resolution/build/test на iOS Simulator и использование проверенного Mac handoff tooling.
- **Внешний шаг:** signed physical iPhone build/install/launch на Mac с Apple Account/Team, уникальным bundle ID и выбранным device; evidence пока отсутствует.
- **NO-GO:** App Store или public iOS release claim.
- Default personal flow — `no-push`; push optional и требует `GoogleService-Info.plist`, APNs/Firebase и production deploy V22. App Store дополнительно блокируют HTTPS и real-device/accessibility/manual acceptance.
- Production backend/web остаётся на SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`. V22 находится только в repository и не deployed.
- Production DB в рамках документирования не проверялась.

## CI policy boundary

Candidate commit `0bbf4acb0ba9620b931fa843dc9d2997379304fb` меняет scheduling только в `codex/native-ios-companion`: feature push auto run `0`, а `workflow_dispatch`, PR в `master` и будущий push в `master` описаны новым контрактом. Default-branch behavior изменится только после merge. Поэтому почтовый storm остановлен на candidate branch, а genuine manual/PR и будущие master failures всё ещё могут уведомлять. Production workflows unchanged; branch protection не настроена и не менялась. См. [[MOC_DevOps]].

## Связанные заметки

- [[MOC_iOS]], [[Пакет_iOS]], [[Пакет_iOS_Mac_Установка]], [[Агент_iOS]]
- [[Источник_Текущее_Состояние]], [[RocketFlow]]
- [[Док_Prod_Deploy_State]], [[MOC_Бэкенд]]
