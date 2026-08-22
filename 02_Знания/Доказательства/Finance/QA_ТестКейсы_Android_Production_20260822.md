---
id: "qa-testcases-finance-android-production-20260822"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
теги: ["finance", "qa", "android", "production", "session", "sync"]
ссылки:
  - "[[Finance]]"
  - "[[QA_Результаты]]"
  - "[[Док_Release_Android_Production_20260822]]"
  - "[[QA_Учетная_Запись_Production_20260822]]"
---

# QA ТестКейсы - Android Production 2026-08-22

## P0

- `AUTH-001`: login -> force-stop -> relaunch; session restored, password not stored.
- `AUTH-002`: expired access + valid refresh; one rotation and one request retry.
- `AUTH-003`: concurrent clients; process-wide single refresh, new pair preserved.
- `AUTH-004`: A sync overlaps login B; no A request/write under B session.
- `SYNC-001`: offline create -> reconnect -> sync; one converged mutation under the same user.
- `INVEST-001`: only selected-month incoming investment transfers enter Analytics.
- `OPS-001`: transactions and transfers are deterministically newest-first.
- `APK-001`: production URL only, non-debuggable, ZIP/alignment/signature/certificate PASS.
- `DEPLOY-001`: backend-only Actions deploy succeeds; frontend and migrations skipped.

## P1

- `AUTH-005`: offline logout clears tokens, UI, local user data and scheduled work.
- `AUTH-006`: late logout A does not erase current session B or show dashboard A.
- `OCR-001`: 401 causes one refresh and at most one upload retry; no offline queue.
- `CATEGORY-001`: button opens vertical scrollable searchable category dialog.
- `CATEGORY-002`: partial-name search filters expense categories and selection works.
- `ACCOUNT-001`: payment account revalidates immediately after refresh.
- `DATE-001`: selected transfer date is preserved online and offline.
- `ANALYTICS-001`: narrow viewport shows one-line month and three non-overlapping controls.

## Result

Unit `167/167`, lint 0, APK binary gates and targeted emulator E2E PASS.
Full final-APK UI offline convergence and real-image OCR were not rerun. Android
17 Espresso fails in framework setup before assertions; instrumentation compiles.

Use [[QA_Учетная_Запись_Production_20260822]] for production tests. Account is
`NEVER DELETE`; do not expose credentials in evidence/logs/chat.
