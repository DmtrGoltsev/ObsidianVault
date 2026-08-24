---
id: "proof-backend-verification-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["backend/mvn test", "backend/target/surefire-reports", "docs/68-scroll-and-priority-retirement-delivery.md", "docs/66-weekly-focus-calendar-delivery.md", "repo audit 2026-06-07", "final verifier 2026-06-07", "backend package 2026-06-08"]
доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Production_Rollout_20260810", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Тесты"]
теги: ["доказательство", "backend", "verification", "tests", "package"]
---

# Док: Backend Verification

## Текущий V21 candidate 2026-08-22

- Backend suite: `142/142` PASS.
- Покрыты V20 -> V21 metadata-only migration без rewrite, legacy/new wire shapes, historical priority-shadow preservation, отключённый decay, compatibility settings и deterministic ordering.
- UUID tie-break использует unsigned ordering с parity к PostgreSQL `uuid ASC`.
- V21 не развёрнут: production остаётся Flyway V20 (`20/20`). См. [[Док_V21_Scroll_Priority_20260822]] и [[Док_Prod_Deploy_State]].

## Текущий feature checkpoint 2026-08-10

- Branch: `codex/weekly-focus-calendar-web-push`.
- Surefire reports: 135 tests, 0 failures, 0 errors, 0 skipped, 29 suites.
- Calendar, Weekly Focus, Focus cadence, FCM/Web Push routing and Flyway `V19`/`V20` входят в current working-tree scope.
- Final implementation review: PASS.
- Последующий production rollout 2026-08-10: backend `sha-910c061de4af` promoted, Flyway current `V20` (`20/20`, `0` failed), local/public health `UP/200`; errors/restarts `0`. Provider delivery smoke не выполнялся при disabled Focus cadence/Web Push.
- Сводное evidence: [[Док_Calendar_Weekly_Focus_WebPush_20260810]].
- Rollout evidence: [[Док_Production_Rollout_20260810]].

## Исторический факт 2026-06

Последний зафиксированный backend package evidence 2026-06-08: `mvn --batch-mode --no-transfer-progress package` прошёл на втором запуске. Итог: `Tests run: 63, Failures: 0, Errors: 0, Skipped: 0`, `BUILD SUCCESS`, total `02:42`, finished `2026-06-08T11:50:48+03`. На текущем HEAD `21f95c1` fresh backend verification в этой документационной задаче не прогонялся и требуется перед утверждением актуального gate.

Jar: `C:\Users\style\Documents\Codex\RocketFlow\backend\target\rocketflow-backend-0.1.0-SNAPSHOT.jar`, 115,319,880 bytes, timestamp 2026-06-08 11:48:27 +03.

Финальный verifier 2026-06-07 подтвердил backend gate: `mvn --batch-mode --no-transfer-progress test` прошёл успешно. Итог: `Tests run: 63, Failures: 0, Errors: 0, Skipped: 0`, `BUILD SUCCESS`, total `03:47`.

Предупреждения не блокируют gate: commons-logging conflict, Mockito/ByteBuddy dynamic agent warning. После audit зафиксирована инвентаризация: backend содержит 16 test files / 63 tests.

## Cleanup/audit notes

- Repo source tests curated: реальные obsolete source tests не удалялись.
- Tracked deletions cleanup относились к artifact/test-artifacts cleanup, не к актуальным source tests.
- Финальный verifier добавил post-cleanup run summary 2026-06-07.

## Definition of done для обновления статуса

- `mvn --batch-mode --no-transfer-progress package` проходит на ветке `MVP3` / HEAD `21f95c1` или явно отмечен как требующий fresh evidence.
- В заметку добавлены дата прогона и краткий итог stdout.
- При падении тестов указан failing class/test и ссылка на лог.

## Связанные заметки

- [[Док_Backend_Тесты]]
- [[Регламент_CI_CD]]
- [[MOC_Бэкенд]]
- [[Док_Production_Rollout_20260810]]
