---
id: "moc-devops"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "docs/production/rocketflow-cicd-runbook.md", ".github/workflows/ios-verify.yml", "commit 0bbf4acb0ba9620b931fa843dc9d2997379304fb", "origin/master commit c0682493c93ac2d8ff1d31bca9e1b1c2546b3c56"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["moc", "devops", "ci-cd", "rocketflow"]
---

# MOC DevOps

Карта CI/CD и production boundary RocketFlow. Verify lanes работают в GitHub Actions; iOS использует macOS, остальные платформы — свои workflow environments. Production остаётся jar/systemd backend + web static/Nginx на [[HexCore]].

Current repo docs HEAD на candidate branch: `99172cd171e8cade0545fb442c9233961c7865d1`. Immutable Mac tooling evidence отдельно закреплено за SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` и run `32669924719`; iOS behavior/build evidence — за app SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` и run `32655691351`.

## Verify workflows

| Workflow | Основной gate |
|---|---|
| `backend-verify.yml` | backend compile/tests и repository-defined checks |
| `web-verify.yml` | `npm test`, `npm audit --audit-level=low`, `npm run build` |
| `android-verify.yml` | Android unit/build/lint |
| `ios-verify.yml` | macOS: XcodeGen parity, Swift package lock parity, unsigned simulator build, unit/UI tests, xcresult и generated-project artifacts |

Точный green iOS checkpoint: app SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, проверенный на `codex/native-ios-companion`, [run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`, `540` unit + `2` UI tests PASS. Текущий branch HEAD этим не определяется; см. [[Док_iOS_Verification]].

Точный Mac tooling checkpoint: SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`, [run 32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719), job `97269056380`, contracts `174/174`, unit `540/0`, UI `2/0`, artifacts `9501177125` (`1,317,064` bytes) и `9501179599` (`25,070` bytes). Physical iPhone install этим не доказан; [[Пакет_iOS_Mac_Установка]].

## Trigger policy

На `origin/master` политика действует с commit `c0682493c93ac2d8ff1d31bca9e1b1c2546b3c56`, pushed 2026-08-24. Commit содержит ровно `3 workflow files / 12 additions` и ограничивает автоматические verify runs для Android, Backend и Web:

- [Android run 32766368686](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32766368686) — success;
- [Backend run 32766368744](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32766368744) — success;
- [Web run 32766368663](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32766368663) — success;
- iOS verify, deploy и publish workflows этим master commit не запускались и не изменялись.

Контракт на `origin/master`: `workflow_dispatch`, PR targeting `master` и push в `master`; обычный feature-branch push не запускает эти три verify workflows. Candidate docs branch `codex/native-ios-companion` на HEAD `99172cd171e8cade0545fb442c9233961c7865d1` уже имеет эквивалентную расширенную политику через commit `0bbf4acb0ba9620b931fa843dc9d2997379304fb`, включая iOS verify. Docs-only push этого HEAD проверен через GitHub Actions API 2026-08-24 в 23:04 Europe/Moscow, более чем через 120 секунд после commit/push: automatic runs `0`, manual run не запускался. Genuine manual/PR/master failures по-прежнему могут уведомлять. Старые другие branches автоматически не исправлены: их нужно обновить этим контрактом или retire, иначе собственная старая ревизия workflow ещё может запускаться. Общая процедура: [[Регламент_GitHub_Actions_без_лишних_запусков]]. Production deploy/package/rollback workflows и branch protection этим исправлением не менялись.

Living policy/runbooks: [`docs/33-current-state-summary.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/33-current-state-summary.md), [`docs/58-github-cicd-policy.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/58-github-cicd-policy.md), [`docs/60-hexcore-prod-runbook.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/60-hexcore-prod-runbook.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/71-native-ios-delivery.md), [`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/72-native-ios-mac-device-handoff.md), [`docs/production/rocketflow-cicd-runbook.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/production/rocketflow-cicd-runbook.md). `docs/33` и `docs/58` на этом SHA уже фиксируют master commit `c0682493c93ac2d8ff1d31bca9e1b1c2546b3c56` как действующий.

## Production

- Current backend/web release: SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, release `sha-50a63270ae09`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`; evidence [[Док_Prod_Deploy_State]].
- Candidate V22 для iOS device registrations находится только в repository и не deployed.
- Production DB в рамках этой документационной актуализации не проверялась.
- Production workflow нельзя запускать для обычной verification задачи.

## iOS external gates

Simulator/tooling CI не закрывает Apple signing/team и physical device. Default personal flow — `no-push`; push optional и требует `GoogleService-Info.plist`, APNs/Firebase и V22 production deploy. Поэтому clone/build на Mac — **GO**, physical install — внешний шаг, App Store/public release — **NO-GO** до HTTPS и real-device/accessibility/manual acceptance; см. [[MOC_iOS]], [[Пакет_iOS_Mac_Установка]] и [[Док_iOS_Verification]].

## Связанные заметки

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — backend и migration boundary
- [[MOC_iOS]] — native iOS
- [[Агент_DevOps]], [[Агент_QA]] — исполнительные роли
- [[Регламент_CI_CD]], [[Регламент_Деплоя]] — проектные регламенты
- [[Регламент_GitHub_Actions_без_лишних_запусков]] — общий регламент triggers и CI-уведомлений
- [[Задача_Production_Deploy_Backup_Rollback]], [[Задача_GHCR_Publish]], [[Задача_CI_Runtime_Lanes]] — открытые инфраструктурные задачи
