---
id: "proof-ios-verification-2026-08-23"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-23"
обновлено: "2026-08-23"
уверенность: "высокая"
источники: ["GitHub Actions run 32655691351", "job 97233929959", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "ios/README.md"]
доказательства: ["GitHub artifact 9497494137", "GitHub artifact 9497494432", "Док_Prod_Deploy_State"]
теги: ["доказательство", "ios", "ci", "tests", "release-gate"]
---

# Док: iOS Verification 2026-08-23

## Что доказано

MacOS iOS Verify завершился успешно для immutable app-code/build SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, запущенного на branch `codex/native-ios-companion`: generated-project parity, Swift package resolution/lock parity, unsigned simulator build и тесты. Branch позже продвинулся docs-only commit до `201a3de8657e56a3a67e1051522cb5793ce5c0b7`; этот docs HEAD не подменяет verified app SHA.

## Exact CI evidence

| Поле | Значение |
|---|---|
| Workflow run | [32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), `success` |
| Job | [97233929959](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351/job/97233929959), `Generate, build, and test`, `success` |
| Verified app source | `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` on `codex/native-ios-companion` at run time |
| Current docs HEAD | `201a3de8657e56a3a67e1051522cb5793ce5c0b7` on `codex/native-ios-companion` |
| Tests | `540` unit + `2` UI, PASS |
| Result artifact | `RocketFlow-xcresult`, ID `9497494137`, digest `sha256:73610a53af8e2443e727083dd0f625ee327400b92b94f975d1b6ad97f10f0d48` |
| Project artifact | `RocketFlow-xcodeproj-xcodegen-2.46.0`, ID `9497494432`, digest `sha256:5825b9347d985d3218d217c7541c138887ed3aad96760c396369144449d2150f` |

Green steps включают Xcode selection/reporting, XcodeGen 2.46.0 install, generation/parity, package resolution/lock parity, dynamic simulator selection, build/test without signing, xcresult validation и загрузку обоих artifacts.

## Product coverage

Native iOS 16+ содержит Planner, Calendar и Focus, offline GRDB/sync/conflicts, details/editors/sharing, reminders, RU/EN, durable restoration/deep links и account safety. Living contract/delivery docs: [`docs/70-native-ios-parity-contract.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/70-native-ios-parity-contract.md) и [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/71-native-ios-delivery.md). Build/test identity остаётся app SHA из таблицы.

## Factual boundary

- **GO:** clean clone/generation/package resolution/build/test на iOS Simulator в поддерживаемом Mac CI окружении.
- **NO-GO:** App Store или public iOS release claim.
- Не закрыты: Apple signing/team, `GoogleService-Info.plist` + APNs/Firebase, production deploy V22 для iOS device registrations/push, HTTPS, real-device/accessibility/manual acceptance.
- Production backend/web остаётся на SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`. V22 находится только в repository и не deployed.
- Production DB в рамках документирования не проверялась.

## CI policy boundary

Candidate commit `0bbf4acb0ba9620b931fa843dc9d2997379304fb` меняет scheduling только в `codex/native-ios-companion`: feature pushes там больше не запускают verify, а `workflow_dispatch`, PR в `master` и будущий push в `master` описаны новым контрактом. `origin/master` на `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb` пока не содержит ни policy commit, ни `ios-verify`; default-branch behavior изменится только после merge. Поэтому почтовый storm остановлен на candidate branch, а genuine manual/PR и будущие master failures всё ещё могут уведомлять. Production workflows unchanged; branch protection не настроена и не менялась. См. [[MOC_DevOps]].

## Связанные заметки

- [[MOC_iOS]], [[Пакет_iOS]], [[Агент_iOS]]
- [[Источник_Текущее_Состояние]], [[RocketFlow]]
- [[Док_Prod_Deploy_State]], [[MOC_Бэкенд]]
