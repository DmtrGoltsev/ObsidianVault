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
доказательства: ["backend/target/surefire-reports", "web npm test 2026-08-10", "android/app/build/test-results/testDebugUnitTest", "delivery final review 2026-08-10"]
теги: ["доказательство", "calendar", "weekly-focus", "web-push", "tests", "release-readiness"]
---

# Док: Calendar, Weekly Focus и Web Push — checkpoint 2026-08-10

## Статус поставки

- Feature branch: `codex/weekly-focus-calendar-web-push`; на checkpoint изменения готовятся к commit/push, поэтому remote feature SHA ещё не фиксируется как evidence.
- Calendar и Weekly Focus реализованы для backend, web и Android.
- Серверная cadence для Focus поддерживает FCM и Web Push; browser lifecycle и account-scoped cleanup описаны в `docs/66-weekly-focus-calendar-delivery.md`.
- Миграции feature-ветки: `V19__weekly_focus.sql` и `V20__focus_notifications.sql`.
- Финальное review реализации: **PASS**. Это PASS implementation/readiness review, а не production release/deploy PASS.

## Проверки

| Контур | Результат | Источник |
|---|---:|---|
| Backend | 135 tests, 0 failures, 0 errors, 0 skipped | `backend/target/surefire-reports/TEST-*.xml` |
| Web | 54 tests passed, 9 test files | `npm test -- --run --reporter=dot`, повторно подтверждено 2026-08-10 |
| Android | 77 unit tests, 0 failures, 0 errors, 0 skipped | `android/app/build/test-results/testDebugUnitTest/TEST-*.xml` |

Счётчики являются evidence этого checkpoint, а не постоянными минимальными порогами suite.

## Production boundary

- Текущая feature-ветка **не задеплоена**: production migration `V19`/`V20`, backend/web promotion, APK rollout, notification enablement и production smoke не выполнялись и не заявляются.
- Исторический deploy baseline от 2026-06-19 остаётся отдельным evidence в [[CI_CD_Production_Status_20260619]]; он не доказывает доставку Calendar/Weekly Focus/Web Push.
- Android production signing заблокирован: release keystore отсутствует; `android/app/google-services.json` и явная Firebase build-time конфигурация также отсутствуют на checkpoint. Production APK и FCM-ready Android release не подтверждены.
- Следующий release gate требует reviewed commit, push feature/release ref, backup и rollout decision, применение `V19`/`V20`, production-equivalent FCM/Web Push config, signed Android artifact и provider/runtime smoke.

## Связанные заметки

- [[RocketFlow]]
- [[Док_Backend_Verification]]
- [[Док_Web_Verification]]
- [[Док_Android_Verification]]
- [[Док_Prod_Deploy_State]]
- [[Регламент_CI_CD]]
- [[Регламент_Деплоя]]
