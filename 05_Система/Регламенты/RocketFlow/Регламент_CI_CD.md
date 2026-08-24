---
id: "reg-cicd"
тип: "регламент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md", "docs/68-scroll-and-priority-retirement-delivery.md"]
доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Prod_Deploy_State"]
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
- **Production deploy path:** GitHub Actions release-branch deploy is the primary production deploy path; direct SSH/SCP upload to HexCore is retained only as a manual/emergency fallback. Финальный deploy подтвержден 2026-06-19.
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

- [[Регламент_GitHub_Actions_без_лишних_запусков]] — общий trigger policy, диагностика лишних runs и профилактика
- [[Источник_CI_CD_Политика]] — политика-источник
- [[Регламент_Деплоя]] — связанный регламент
- [[Док_Prod_Deploy_State]] — фактический production deploy state
- [[Док_Android_Verification]] — Android verifier после cleanup
- [[Агент_DevOps]] — ответственный

## Final CI/CD local preparation status (2026-06-14)

Status: PASS for local CI/CD preparation. This does not claim that a new production deploy was executed.

- User confirmed RocketFlow is production.
- Read-only HexCore inventory confirmed live service `rocketflow-backend.service`.
- Live routes: `/rocket/ -> /var/www/rocketflow-web/current`; `/rocket-api/ -> 127.0.0.1:8080/api/`.
- Backend current symlink: `/opt/rocketflow/current/rocketflow-backend.jar`.
- Database: `rocketflow_prod`; Flyway rows: 18.
- Health: OK.
- Workflow state: `.github/workflows/backend-hexcore-prod-deploy.yml` hardened; GHCR package and rollback workflows added.
- Repo docs: `docs/production/rocketflow-*` prepared; policy/runbook updated.
- Historical 2026-06-14 preparation state: release push was package-only and production deploy dispatch-only; superseded by 2026-06-19 release-branch deploy evidence.
- Safety: GHCR publish gated; pinned `known_hosts`; health URL fixed.
- Final review: all 7 workflow YAML files parse, no raw `${{ inputs.* }}` in `run` or `script`, release push no prod mutation, dispatch gates present, no hardcoded secret values.
- Historical note: no production deploy was executed during the 2026-06-14 preparation update; superseded by final deploy evidence on 2026-06-19.
- Residual approvals: GitHub production environment/secrets/required reviewers, first production workflow run, deploy/restart/migration/rollback/GHCR publish approvals, DB backup proof; DB rollback out of scope.
- Evidence: [[CI_CD_Production_Status_20260614]].

## Final production CI/CD state (2026-06-19)

Status: PASS. GitHub Actions release-branch production deploy is now green.

- Release branch: `release/rocketflow-prod-ci-cd-ec377a7`; release commit `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`.
- Final deploy run: `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/27803394498`, success.
- Trigger rule: branch name must contain `release`; push/cherry-pick/merge desired commit into `release/<project>-prod-...`, then watch GitHub Actions.
- Manual `workflow_dispatch` remains available.
- Direct SSH/SCP remains documented fallback, not primary.
- GitHub `production` environment and environment secrets are configured; secret values must never be stored in docs.
- Verify after deploy: `http://45.10.110.42/rocket/` and `http://45.10.110.42/rocket-api/health`.
- Rollback: use project rollback workflow where available; DB rollback is not automated and requires manual restore from backups after approval.
- Evidence: [[CI_CD_Production_Status_20260619]].

## Calendar/Weekly Focus/Web Push release boundary (2026-08-10)

- Production rollout завершён: source `910c061de4af9395d9bb682624bd966b2977a738`, release `sha-910c061de4af`, Flyway V20 (`20/20`).
- Historical implementation gates: backend 135 tests, web 54 tests, Android 77 unit tests; final implementation review PASS.
- Focus cadence и Web Push должны оставаться disabled до production-equivalent configuration и provider smoke.
- Android production lane blocked без release keystore и Firebase config.
- Evidence: [[Док_Calendar_Weekly_Focus_WebPush_20260810]], [[Док_Production_Rollout_20260810]], [[Док_Prod_Deploy_State]].

## V21 candidate boundary (2026-08-22)

- Local candidate gates: backend `142/142`; web `61/61`, build/audit PASS; Android `90/90`, assemble/lint/debug Android-test APK PASS.
- Commit, push и deploy в этой задаче не выполнялись; не читать candidate evidence как production state.
- Release sequence: reviewed commit/push -> release ref -> backup/rollback decision -> preflight Flyway `>=20` -> manifest target `21` -> совместный backend/web promotion -> post Flyway `>=21` и authenticated smoke -> отдельный Android rollout.
- Application rollback fail-closed требует readable target manifest и JSON integer `flyway_history_min_rows` в диапазоне `20..PRE_FLYWAY_COUNT`. Равное pre-count и меньшее совместимое значение принимаются; missing/unreadable manifest, missing field, string/boolean, `<20` и `>pre` отклоняются. Post Flyway остаётся `>=20` и `>=pre`; V20 binary с minimum 20 разрешён на сохранённой V21 schema без DB downgrade/repair/restore.
- Проверка rollback contract: accepted `7/7`, invalid `4/4`, YAML/Bash PASS; `actionlint` и `shellcheck` недоступны.
- Evidence: [[Док_V21_Scroll_Priority_20260822]], [[Док_Prod_Deploy_State]].
