---
id: "proof-rocketflow-production-rollout-2026-08-10"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-10"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["https://github.com/DmtrGoltsev/RocketFlow/actions/runs/31357406631", "https://github.com/DmtrGoltsev/RocketFlow/pull/1", ".github/workflows/backend-hexcore-prod-deploy.yml", ".github/workflows/rocketflow-prod-rollback.yml", "production post-deploy inspection 2026-08-10", "production PostgreSQL server_version inspection 2026-08-10", "fresh backup catalog inspection 2026-08-10", "Android release artifact inspection 2026-08-10"]
доказательства: ["Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Prod_Deploy_State", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification"]
теги: ["доказательство", "production", "deploy", "calendar", "weekly-focus", "web-push", "rollback", "backup"]
---

# Док: Production rollout 2026-08-10

## Результат

Production rollout Calendar/Weekly Focus выполнен успешно 2026-08-10. Source/deployed SHA: `910c061de4af9395d9bb682624bd966b2977a738`; release ID: `sha-910c061de4af`.

- Release branch: `release-weekly-focus-calendar-910c061de4af`.
- [GitHub Actions run 31357406631](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/31357406631): `completed/success`; jobs `package` и `deploy` завершились успешно.
- Backend promoted: `rocketflow-backend-sha-910c061de4af.jar`.
- Web promoted: `rocketflow-web-sha-910c061de4af`.
- Production DB: PostgreSQL `18.4`; версия подтверждена на production-сервере и независимо заголовком каталога свежего pre-rollout backup.
- Flyway: `20/20` successful, `0` failed, current `V20`; `V19` и `V20` применены по одному разу успешно.
- Local/public API health: HTTP `200`, status `UP`; local/public web: HTTP `200` с ожидаемым root marker.
- Post-deploy runtime: service `active/running`, `NRestarts=0`; backend journal errors/exceptions после promotion: `0`; Nginx `5xx`: `0`.
- Rollback не потребовался и не запускался.

## Backup evidence

Fresh pre-rollout backup создан и проверен без сохранения данных БД или credentials в vault:

| Поле | Значение |
|---|---|
| Basename | `rocketflow_prod_20260810T045958Z.dump` |
| Timestamp UTC | `2026-08-10T04:59:58Z` |
| Size | `223191` bytes |
| SHA-256 | `783590b8fa26f6d2882aab0a5cf670b483be5895fd80b6a915cd4c9946841b39` |
| `pg_restore -l` | PASS, `238` catalog entries |
| PostgreSQL version | `18.4`, совпадает с production server inspection и backup catalog header |

Restore не выполнялся; backup payload и catalog listing в vault не копировались.

## Rollback readiness

- [PR #1](https://github.com/DmtrGoltsev/RocketFlow/pull/1) merged в `master` 2026-08-10; merge commit `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb`.
- [RocketFlow Prod Rollback workflow](https://github.com/DmtrGoltsev/RocketFlow/blob/master/.github/workflows/rocketflow-prod-rollback.yml), workflow ID `330828165`, state `active`.
- Rollback workflow не запускался, потому что promotion и post-deploy gates прошли.

## Notification flags

- Focus cadence остаётся disabled: packaged default `false`, runtime override отсутствует.
- Web Push остаётся disabled: packaged default `false`, runtime override отсутствует.
- Production environment/config в ходе rollout не менялись.

## Android boundary

Production-configured release artifact собран локально как `app-release-unsigned.apk`:

- Size: `3261969` bytes; timestamp `2026-08-10T07:28:52.8668174+03:00`.
- SHA-256: `1763de390dd587c686fe84152c521a2d92e65b747fb2689ec2076c0560c576d7`.
- Artifact unsigned; `apksigner verify` завершился `DOES NOT VERIFY`.
- APK не устанавливался, не передавался и не публиковался; он не является installable/publishable production release.
- `android/app/google-services.json` и подтверждённая Firebase Android production configuration отсутствуют; Android FCM production delivery не заявляется.

## Smoke boundary

- Sanctioned QA/production credentials для authenticated smoke отсутствовали; authenticated read smoke остаётся evidence gap.
- Non-mutating unauthenticated protection checks прошли: login validation вернул ожидаемый `400`; legacy `/me` и `/folders`, Calendar, Focus current/candidates/history/settings и Web Push config вернули ожидаемый protected status `401`.
- Provider delivery smoke не выполнялся, поскольку Focus cadence и Web Push оставлены disabled.

## Связанные заметки

- [[RocketFlow]]
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]]
- [[Док_Prod_Deploy_State]]
- [[Док_Backend_Verification]]
- [[Док_Web_Verification]]
- [[Док_Android_Verification]]
- [[Источник_Текущее_Состояние]]
- [[MOC_RocketFlow]]
- [[MOC_DevOps]]
