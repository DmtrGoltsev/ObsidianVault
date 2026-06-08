---
id: "mvp3-simplification"
тип: "проект"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-08"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/62-mvp3-design-simplification-contract.md"]
доказательства: ["Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Android_Build", "Док_Prod_Deploy_State"]
теги: ["mvp3", "активно", "полировка"]
---

# MVP3: Упрощение дизайна и полировка

## Статус: активно (текущая стадия)

## Прогресс

Delivery 2026-06-08 в ветке `MVP3`, base HEAD перед новым коммитом `5f03476d1de4e09d5da0b1bfedfaf28353173124`:
- Android `MainActivity.kt`: goal from folder раскрывает path и открывает GoalDetail; task from GoalDetail сохраняется в правильную goal и возвращает в GoalDetail; target dialogs scroll; child folders/goals/tasks newest-first.
- Android verification: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon` — PASS, `BUILD SUCCESSFUL in 1m19s`.
- Android APK build: `.\gradlew.bat app:assembleDebug app:assembleRelease` — PASS, `BUILD SUCCESSFUL in 2m08s`; debug APK signed/verified, release APK unsigned/not verified.
- Backend package: `mvn --batch-mode --no-transfer-progress package` — PASS on second run; 63 tests, 0 failures/errors/skipped, `BUILD SUCCESS`, total `02:42`; jar built.
- Prod deploy preflight: **NOT DEPLOYED / BLOCKED** pending target ref/method, backup expectation, secrets/env readiness.

Ранее: 21 коммит в ветке `MVP3` относительно `MVP2` (`git rev-list --count MVP2..MVP3` = 21), HEAD `9825a40f6d2e4b909b785ef228aacc5393acec0b`:
- Android UX: drag-drop, иерархия папок, fullscreen alarms (TaskReminderAlarmActivity, AlarmReceiver, AlarmScheduler)
- Sync: офлайн-планирование с синхронизацией (PlanningSyncWorker, ConflictResolver)
- Модуль `planning`: полный цикл офлайн-планирования
- Модуль `sharing`: модели шеринга (ShareTarget, ShareInvitation, fullAccess)
- Последний коммит: `9825a40` — Use due date offsets for Android default reminders

QA-модель приёмки создана ([[Источник_MVP3_QA_Модель|docs/63]]), BA-пути описаны ([[Источник_MVP3_BA_Пути|docs/64]]). После cleanup/repo audit и финального verifier: backend/web/android build health зелёный. Backend `mvn --batch-mode --no-transfer-progress test`: `63/0/0/0`, `BUILD SUCCESS`, total `03:47`; web `npm run build`: 1792 modules transformed, built in `2.09s`; Android `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon`: exit code `0`.

## Цель

Упрощение дизайна и полировка существующей функциональности. Завершающая стадия перед релизом MVP.

## Контекст

После завершения трёх волн (A, B, C) и Wave C.1 проект входит в стадию MVP3 — финальная полировка:
- Упрощение UI/UX (web + Android)
- Исправление багов и несоответствий
- Финализация документации
- Сертификация нотификаций на staging

Источник контракта: [[Источник_MVP3_Контракт]]

QA-модель: [[Источник_MVP3_QA_Модель]]
BA-пути: [[Источник_MVP3_BA_Пути]]

## Критерии завершения

- Все локальные verify/build gates подтверждены на текущем HEAD, включая финальный Android gate после cleanup
- Notification staging smoke сертифицирован
- Docker/GHCR решение явно закрыто: либо GHCR publish восстановлен и доказан, либо production model без GHCR зафиксирована как принятое решение
- Дизайн соответствует контракту MVP3
- Документация актуальна

## Активные гейты

- GHCR publish/workflow или явное решение оставить jar/systemd deploy без GHCR
- Staging notification certification
- Явное решение по backend prod deploy: `workflow_dispatch` vs merge/push to `MVP2`/`release_1`, backup expectation, secrets/env readiness

## Блокеры

- GHCR/Docker deploy остаётся open gate
- Backend prod deploy остановлен: canonical workflow deploy branches `MVP2`/`release_1`, current local branch `MVP3`; shell lacks `HEXCORE_PROD_SSH_*` and `ROCKETFLOW_PROD_BACKUP_*`; backup user mismatch `rocketbackup` vs `rocketdeploy`

## Связанные заметки

- [[RocketFlow]] — главная заметка проекта
- [[Wave_C]] — предыдущая завершённая волна
- [[Регламент_Нотификационного_Смока]] — smoke-процедура
- [[Агент_QA]] — валидация
- [[Док_Cleanup_Manifest]] — cleanup/evidence manifest
- [[Док_Android_Verification]] — Android verifier status
