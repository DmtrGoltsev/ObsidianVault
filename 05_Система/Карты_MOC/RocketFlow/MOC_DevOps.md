---
id: "moc-devops"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-23"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/71-native-ios-delivery.md", "docs/production/rocketflow-cicd-runbook.md", ".github/workflows/ios-verify.yml", "commit 0bbf4acb0ba9620b931fa843dc9d2997379304fb"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["moc", "devops", "ci-cd", "rocketflow"]
---

# MOC DevOps

Карта CI/CD и production boundary RocketFlow. Verify lanes работают в GitHub Actions; iOS использует macOS, остальные платформы — свои workflow environments. Production остаётся jar/systemd backend + web static/Nginx на [[HexCore]].

Current repo docs HEAD на candidate branch: `201a3de8657e56a3a67e1051522cb5793ce5c0b7`. Immutable iOS build/test evidence отдельно закреплено за app SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` и run `32655691351`.

## Verify workflows

| Workflow | Основной gate |
|---|---|
| `backend-verify.yml` | backend compile/tests и repository-defined checks |
| `web-verify.yml` | `npm test`, `npm audit --audit-level=low`, `npm run build` |
| `android-verify.yml` | Android unit/build/lint |
| `ios-verify.yml` | macOS: XcodeGen parity, Swift package lock parity, unsigned simulator build, unit/UI tests, xcresult и generated-project artifacts |

Точный green iOS checkpoint: app SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, проверенный на `codex/native-ios-companion`, [run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`, `540` unit + `2` UI tests PASS. Текущий branch HEAD этим не определяется; см. [[Док_iOS_Verification]].

## Trigger policy

Candidate commit `0bbf4acb0ba9620b931fa843dc9d2997379304fb` задаёт в `codex/native-ios-companion` новый контракт для четырёх verify workflow files:

- `workflow_dispatch` доступен на любой ref;
- конфигурация `pull_request` targeting `master` объявлена автоматической fail-closed verification;
- конфигурация `push` в `master` объявлена автоматической полной verification;
- обычный push в feature/codex/release branch verify не запускает;
- workflow-level path filters удалены, чтобы PR/master checks публиковались независимо от затронутого пути.

Это уже прекратило automatic verify runs и постоянные fail-email от push в candidate branch. Но `origin/master` на `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb` ещё не содержит ни commit `0bbf4acb`, ни `ios-verify`; default-branch behavior изменится только после merge. Genuine manual/PR и будущие master failures могут уведомлять. Production deploy/package/rollback workflows unchanged. Branch protection не настроена и не менялась.

Living policy/runbooks: [`docs/58-github-cicd-policy.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/58-github-cicd-policy.md), [`docs/60-hexcore-prod-runbook.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/60-hexcore-prod-runbook.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/71-native-ios-delivery.md), [`docs/production/rocketflow-cicd-runbook.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/201a3de8657e56a3a67e1051522cb5793ce5c0b7/docs/production/rocketflow-cicd-runbook.md).

## Production

- Current backend/web release: SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, release `sha-50a63270ae09`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`; evidence [[Док_Prod_Deploy_State]].
- Candidate V22 для iOS device registrations находится только в repository и не deployed.
- Production DB в рамках этой документационной актуализации не проверялась.
- Production workflow нельзя запускать для обычной verification задачи.

## iOS external gates

Simulator CI не закрывает Apple signing/team, `GoogleService-Info.plist`, APNs/Firebase, V22 production deploy, HTTPS и real-device/accessibility/manual acceptance. Поэтому clone/build на Mac — **GO**, App Store/public release — **NO-GO**; см. [[MOC_iOS]] и [[Док_iOS_Verification]].

## Связанные заметки

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — backend и migration boundary
- [[MOC_iOS]] — native iOS
- [[Агент_DevOps]], [[Агент_QA]] — исполнительные роли
- [[Регламент_CI_CD]], [[Регламент_Деплоя]] — регламенты
- [[Задача_Production_Deploy_Backup_Rollback]], [[Задача_GHCR_Publish]], [[Задача_CI_Runtime_Lanes]] — открытые инфраструктурные задачи
