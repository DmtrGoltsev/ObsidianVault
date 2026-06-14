---
id: "reg-cicd"
тип: "регламент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-13"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md"]
доказательства: ["Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Prod_Deploy_State"]
теги: ["регламент", "ci-cd", "процесс"]
---

# Регламент CI/CD

## Цель

Обеспечить автоматическую проверку качества кода при каждом push и PR через GitHub Actions.

## Область применения

Все изменения в репозитории RocketFlow. Воркфлоу определены в `.github/workflows/`.

## Воркфлоу

| Воркфлоу | Файл | Триггер | Проверки |
|----------|------|---------|----------|
| Backend Verify | `backend-verify.yml` | push, PR в main | mvn test, Docker build, /actuator/health smoke |
| Web Verify | `web-verify.yml` | push, PR в main | npm run build |
| Android Verify | `android-verify.yml` | push, PR | unit tests, debug build, lint |
| Backend Deploy | `backend-hexcore-prod-deploy.yml` | manual / push в ветку с `release` в имени | Деплой на [[HexCore]] |
| Image Publish | отсутствует / open gate | n/a | GHCR workflow требует восстановления или явного отказа |

## Триггеры запуска

- **Автоматически:** verify workflows — push в main и pull request; production deploy — push только в ветки, имя которых содержит `release`, с guard `contains(github.ref_name, 'release')`.
- **Вручную:** workflow_dispatch для deploy workflow; GHCR publish не считать доступным без актуального workflow evidence.
- **Production environment:** deploy workflow использует GitHub environment `production` и concurrency.
- **Production deploy path:** GitHub Actions release-branch deploy is the primary production deploy path; direct SSH/SCP upload to HexCore is retained only as a manual/emergency fallback and is not evidence that deploy already happened.
- **Required deploy secrets by name:** `HEXCORE_PROD_SSH_HOST`, `HEXCORE_PROD_SSH_USER`, `HEXCORE_PROD_SSH_PRIVATE_KEY`, optional `HEXCORE_PROD_SSH_PORT`, а также project-specific secrets/env, если они требуются workflow.
- **Важно:** ветка `MVP2` больше не является auto-deploy веткой без `release` в имени.

## Участники

- [[Агент_DevOps]] — владелец CI/CD
- [[Агент_Бэкенд]] — backend verify
- [[Агент_Веб]] — web verify
- [[Агент_Android]] — android verify
- [[Агент_QA]] — приёмка результатов

## Критерии успеха

- Все verify-воркфлоу зелёные
- PR не мёрджится при красных проверках
- Production деплой только при зелёном backend-verify
- Production auto deploy разрешен только для release-named branches; main/MVP ветки без `release` не запускают production deploy автоматически.
- Android gate не считать закрытым после cleanup без финального verifier evidence

## Эскалация

При падении CI — [[Агент_DevOps]] диагностирует и либо чинит, либо эскалирует на [[Оркестратор]].

## Связанные заметки

- [[Источник_CI_CD_Политика]] — политика-источник
- [[Регламент_Деплоя]] — связанный регламент
- [[Док_Prod_Deploy_State]] — фактический production deploy state
- [[Док_Android_Verification]] — Android verifier после cleanup
- [[Агент_DevOps]] — ответственный
