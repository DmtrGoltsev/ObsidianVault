---
id: "agent-devops"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/71-native-ios-delivery.md", "docs/33-current-state-summary.md", ".github/workflows/ios-verify.yml", "commit 0bbf4acb0ba9620b931fa843dc9d2997379304fb"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["агент", "devops", "ci-cd", "деплой"]
---

# Агент DevOps

## Зона ответственности

- GitHub Actions CI/CD: macOS для iOS Verify и platform-specific runners для остальных lanes
- [[Docker_Image]] сборка и публикация в GHCR
- Деплой на [[HexCore]] (systemd + Nginx)
- PostgreSQL 18.4 эксплуатация в production — current carried-forward state [[Док_Prod_Deploy_State]]; [[Док_Production_Rollout_20260810]] только historical V20 evidence
- Secrets management (без хранения секретов в коде)
- Мониторинг production

## CI/CD воркфлоу

- `backend-verify` — mvn test + Docker build + /actuator/health smoke
- `web-verify` — `npm test`, low-level audit и production build
- `android-verify` — unit tests, debug build и lint
- `ios-verify` — XcodeGen/package parity, unsigned simulator build, unit/UI tests, xcresult/generated-project artifacts
- `backend-hexcore-prod-deploy` — production деплой
- `backend-image-publish` — ручная публикация в GHCR

Файлы: `.github/workflows/`

Candidate trigger contract из commit `0bbf4acb0ba9620b931fa843dc9d2997379304fb` находится только в `codex/native-ios-companion`: feature push auto run `0`, `workflow_dispatch` доступен, а PR targeting `master` и push в `master` станут default behavior только после merge. На candidate branch это остановило постоянные feature-push fail emails. Genuine manual/PR и будущие master failures всё ещё могут уведомлять. Production workflows unchanged; branch protection не настроена и не менялась. Детали: [[MOC_DevOps]].

Living docs зафиксированы на `b75ca723f767f520bee39ea72052b1a4b03a7e59`: [`docs/58-github-cicd-policy.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/58-github-cicd-policy.md), [`docs/60-hexcore-prod-runbook.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/60-hexcore-prod-runbook.md), [`docs/71-native-ios-delivery.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/71-native-ios-delivery.md), [`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/b75ca723f767f520bee39ea72052b1a4b03a7e59/docs/72-native-ios-mac-device-handoff.md).

## Права на решения

- Конфигурация CI/CD пайплайнов
- Выбор инфраструктурных решений
- Управление доступом к production

## Активные задачи

- GHCR publish (гейт)
- Staging notification certification (инфраструктурная поддержка)
- Поддержка production на [[HexCore]]
- Apple signing/team, APNs/Firebase и HTTPS prerequisites для iOS release
- Production deploy candidate V22 перед заявлением iOS push; сейчас production остаётся V21 (`21/21`), release checks preflight `>=20`, manifest/post `>=21`
- Mac handoff tooling evidence `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` / run `32669924719`; physical install остаётся внешним шагом [[Пакет_iOS_Mac_Установка]]

## Выполненные волны

- Wave A: backend CI
- Wave B: staging secrets
- Wave C: production deploy

## Связанные заметки

- [[Регламент_CI_CD]] — CI/CD регламент
- [[Регламент_Деплоя]] — регламент деплоя
- [[HexCore]] — production сервер
- [[Docker_Image]] — контейнеризация
- [[RocketFlow]] — проект
- [[MOC_DevOps]] — актуальная trigger/deploy карта
- [[MOC_iOS]], [[Агент_iOS]] — iOS integration boundary
- [[Док_iOS_Verification]] — green simulator CI и external gates
- [[Док_Prod_Deploy_State]] — current production V21
