---
id: "proof-rocketflow-calendar-weekly-focus-webpush-2026-08-10"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-10"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["README.md", "docs/33-current-state-summary.md", "docs/66-weekly-focus-calendar-delivery.md", "android/README.md"]
доказательства: ["backend/target/surefire-reports", "web npm test 2026-08-10", "android/app/build/test-results/testDebugUnitTest", "delivery final review 2026-08-10", "Док_Production_Rollout_20260810"]
теги: ["доказательство", "calendar", "weekly-focus", "web-push", "tests", "production"]
---

# Док: Calendar, Weekly Focus и Web Push — checkpoint 2026-08-10

## Статус поставки

- Текущий статус: source/deployed SHA `910c061de4af9395d9bb682624bd966b2977a738` успешно развёрнут в production как release `sha-910c061de4af`; canonical rollout evidence: [[Док_Production_Rollout_20260810]].
- Исторический feature checkpoint до rollout: branch `codex/weekly-focus-calendar-web-push`; на момент checkpoint изменения ещё готовились к commit/push и remote feature SHA не фиксировался как evidence.
- Calendar и Weekly Focus реализованы для backend, web и Android.
- Серверная cadence для Focus поддерживает FCM и Web Push; browser lifecycle и account-scoped cleanup описаны в `docs/66-weekly-focus-calendar-delivery.md`.
- Миграции feature-ветки: `V19__weekly_focus.sql` и `V20__focus_notifications.sql`.
- Финальное review реализации: **PASS**; последующий production rollout также **PASS**.

## Проверки

| Контур | Результат | Источник |
|---|---:|---|
| Backend | 135 tests, 0 failures, 0 errors, 0 skipped | `backend/target/surefire-reports/TEST-*.xml` |
| Web | 54 tests passed, 9 test files | `npm test -- --run --reporter=dot`, повторно подтверждено 2026-08-10 |
| Android | 77 unit tests, 0 failures, 0 errors, 0 skipped | `android/app/build/test-results/testDebugUnitTest/TEST-*.xml` |

Счётчики являются evidence этого checkpoint, а не постоянными минимальными порогами suite.

## Production rollout и boundary

- Историческая запись checkpoint о состоянии **не задеплоено** была верна до rollout и заменена 2026-08-10: GitHub Actions run `31357406631` успешно promoted backend/web, а Flyway завершён на `V20` (`20/20`, `0` failed).
- Backend/web health и unauthenticated protection smoke прошли; rollback не использовался. Focus cadence и Web Push намеренно остаются disabled.
- Исторический deploy baseline от 2026-06-19 остаётся отдельным evidence в [[CI_CD_Production_Status_20260619]]; текущий rollout доказан отдельно в [[Док_Production_Rollout_20260810]].
- Android direct-sideload boundary закрыт installable `RocketFlow-0.1.0-prod-debugcert.apk` для exact source SHA `910c061de4af9395d9bb682624bd966b2977a738`; SHA-256 `2209f2b5e8ee8f01fa486d997f898d9fc08db98cf02e0b22d3182fa1026cc4d1`. Install/runtime/build checks PASS; подробности в [[Док_Android_Verification]]. Прежний unsigned SHA-256 `1763de390dd587c686fe84152c521a2d92e65b747fb2689ec2076c0560c576d7` сохранён как superseded damaged/non-installable evidence. Play Store production signing и Firebase/FCM остаются открытыми boundaries.
- Authenticated read smoke остаётся evidence gap; provider delivery smoke не выполнялся при disabled Focus cadence/Web Push.

## Связанные заметки

- [[RocketFlow]]
- [[Док_Backend_Verification]]
- [[Док_Web_Verification]]
- [[Док_Android_Verification]]
- [[Док_Prod_Deploy_State]]
- [[Док_Production_Rollout_20260810]]
- [[Регламент_CI_CD]]
- [[Регламент_Деплоя]]
