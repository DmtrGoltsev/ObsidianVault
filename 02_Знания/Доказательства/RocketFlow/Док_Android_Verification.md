---
id: "proof-android-verification-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["android/app/build/test-results/testDebugUnitTest", "android/README.md", "docs/68-scroll-and-priority-retirement-delivery.md", "docs/66-weekly-focus-calendar-delivery.md", "docs/67-weekly-focus-production-rollout-evidence.md", "android local setup", "repo audit 2026-06-07", "final verifier 2026-06-07", "delivery verifier 2026-06-08"]
доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Production_Rollout_20260810", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Источник_Android_Local_Setup", "Док_Cleanup_Manifest", "Док_Android_Build"]
теги: ["доказательство", "android", "verification", "tests", "build", "lint"]
---

# Док: Android Verification

## Текущий V21 candidate 2026-08-22

- `testDebugUnitTest`: `90/90` PASS.
- `assembleDebug`: PASS.
- `lintDebug`: PASS, `0` errors, `34` existing warnings.
- `assembleDebugAndroidTest`: PASS.
- Planner visual QA PASS: stable anchor + pixel offset при expand/collapse, details + Back, refresh, insert above и rotation; parent fallback при удалении; intentional top-tab reset.
- Task priority отсутствует в UI/логике; create сохраняет compatibility `5`, а edit исторической задачи сохраняет её shadow-значение.
- SQLite lifecycle ownership исправлен для planning sync, Focus sync, reminder receiver и acceptance seed; lifecycle покрыт тестами.
- Compact landscape editor visual QA PASS для Title и Details с IME; portrait editor PASS и сохраняет прежний `AlertDialog`.
- Evidence: [[Док_V21_Scroll_Priority_20260822]]. Последний IME rerun не повторял anchor/logcat; отдельный более ранний anchor QA остаётся PASS, а compact-form change не затрагивал anchor code.
- Boundary: это worktree evidence, не APK/release/deploy. Production Android artifact ниже не содержит V21 candidate changes.

## Текущий feature checkpoint 2026-08-10

- Branch: `codex/weekly-focus-calendar-web-push`.
- Unit reports: 77 tests, 0 failures, 0 errors, 0 skipped, 15 suites.
- Feature evidence фиксирует `assembleDebug`, `lintDebug` и debug Android-test APK assembly PASS; Calendar, Weekly Focus и data-only Focus FCM handling реализованы.
- Final implementation review: PASS.
- Актуальный installable direct-sideload APK: `RocketFlow-0.1.0-prod-debugcert.apk`, exact source SHA `910c061de4af9395d9bb682624bd966b2977a738`, SHA-256 `2209f2b5e8ee8f01fa486d997f898d9fc08db98cf02e0b22d3182fa1026cc4d1`, `3287664` bytes.
- Signing/package checks PASS: existing debug certificate SHA-256 `b5675864b9cb8a046d889f54e58f5b0256d6937ecd448e69d7faa955e587aca0`, APK Signature Scheme v2/v3, `zipalign` valid, `debuggable=false`, production API configuration embedded.
- Device/runtime checks PASS: `adb install -r`; installed artifact hash parity; UID, first-install timestamp и app data preserved; cold launch, logcat review и backend health PASS.
- Verification: `77` Android tests PASS; lint `0` errors.
- Distribution boundary: debug certificate не является Play Store production signing identity; будущие sideload updates должны использовать тот же certificate. Firebase Android config отсутствует, поэтому FCM delivery не заявляется.
- Исторический unsigned APK SHA-256 `1763de390dd587c686fe84152c521a2d92e65b747fb2689ec2076c0560c576d7`, `3261969` bytes, сохранён как superseded evidence: Android сообщил о damaged package, APK не устанавливался, `apksigner` возвращал `DOES NOT VERIFY`.
- Сводное evidence: [[Док_Calendar_Weekly_Focus_WebPush_20260810]].
- Rollout boundary: [[Док_Production_Rollout_20260810]].

## Исторический факт 2026-06

Последний зафиксированный Android gate evidence: delivery verifier 2026-06-08 подтвердил gate после правки `android/app/src/main/java/com/rocketflow/companion/MainActivity.kt`: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon` прошёл, `BUILD SUCCESSFUL in 1m19s`, `53 actionable tasks`. На текущем HEAD `21f95c1` fresh Android gate в этой документационной задаче не прогонялся и требуется перед утверждением актуального gate.

Исправления в `MainActivity.kt`:
- goal from folder открывается/появляется внутри папки через раскрытие пути папки и открытие GoalDetail;
- task, созданная из GoalDetail, возвращает пользователя в GoalDetail и сохраняется в правильную goal;
- target dialogs прокручиваются;
- child folders/goals/tasks сортируются newest-first.

Финальный verifier 2026-06-07 подтвердил Android gate: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon` прошёл с exit code `0`.

Локальная Android-среда исправлена и сработала в финальной проверке:

- SDK: `C:\Users\style\AppData\Local\Android\Sdk`
- `android/local.properties`: `sdk.dir=C:/Users/style/AppData/Local/Android/Sdk`
- `android/local.properties` игнорируется git
- emulator `emulator-5554` видим
- SDK/local.properties worked; SDK/AGP/env errors отсутствуют

## Финальный результат

Android local full gate после delivery-fix зелёный как historical evidence: unit/build/lint прошли. APK build details см. [[Док_Android_Build]]. Это не закрывает staging notification/security/prod gates; для HEAD `21f95c1` нужен fresh evidence.

## Инвентаризация тестов

- Android unit: 8 files / 49 tests
- Android instrumented: 2 files / 7 tests
- Android CI больше не считается build-only: ожидаемый lane включает unit/build/lint.

## Definition of done для финального verifier

- Запущен актуальный Android gate на ветке `MVP3` / HEAD `21f95c1` или явно отмечен как требующий fresh evidence.
- В заметку добавлены команда, дата, результат и краткий stdout summary.
- Failing task/test отсутствует.

## Связанные заметки

- [[Источник_Android_Local_Setup]]
- [[Док_Android_Build]]
- [[Задача_CI_Runtime_Lanes]]
- [[MOC_Android]]
- [[Док_Production_Rollout_20260810]]
