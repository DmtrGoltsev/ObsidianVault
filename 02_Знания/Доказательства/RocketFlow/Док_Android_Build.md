---
id: "proof-android-build"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: [".github/workflows/android-verify.yml", "android/local.properties", "delivery APK build 2026-06-08", "production-configured APK inspection 2026-08-10"]
доказательства: ["Док_Production_Rollout_20260810", "Док_Android_Verification", "Источник_Android_Local_Setup"]
теги: ["доказательство", "сборка", "android", "ci"]
---

# Доказательство: Android build / CI lane

## Что проверено

Android CI lane больше не описывается как build-only: актуальная модель — unit/build/lint. Локальная среда SDK исправлена; финальный полный Android verifier после cleanup прошёл.

Delivery build 2026-06-08: `.\gradlew.bat app:assembleDebug app:assembleRelease` прошёл, `BUILD SUCCESSFUL in 2m08s`.

## Кем проверено

CI: android-verify.yml; локальный setup см. [[Источник_Android_Local_Setup]].

## Когда проверено

Автоматически по правилам `android-verify.yml`; финальный post-cleanup result дописан в [[Док_Android_Verification]] 2026-06-07. Новый локальный APK build зафиксирован 2026-06-08.

## Результат

- Локальная Android SDK конфигурация исправлена
- emulator `emulator-5554` видим
- Kotlin 1.9.24, minSdk 26, targetSdk 34
- Android unit inventory: 8 files / 49 tests
- Android instrumented inventory: 2 files / 7 tests
- Финальный локальный gate: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon`, exit code `0`
- Delivery gate 2026-06-08: `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon`, `BUILD SUCCESSFUL in 1m19s`, 53 actionable tasks
- Debug APK: `C:\Users\style\Documents\Codex\RocketFlow\android\app\build\outputs\apk\debug\app-debug.apk`, 4,443,235 bytes, timestamp 2026-06-08 11:14:37 +03, debug-signed, `apksigner` OK v2 signature
- Release APK: `C:\Users\style\Documents\Codex\RocketFlow\android\app\build\outputs\apk\release\app-release-unsigned.apk`, 3,196,165 bytes, timestamp 2026-06-08 11:40:06 +03, unsigned, `apksigner` DOES NOT VERIFY

Post-rollout build evidence 2026-08-10:

- Production-configured release APK: `android/app/build/outputs/apk/release/app-release-unsigned.apk`, `3261969` bytes, timestamp `2026-08-10T07:28:52.8668174+03:00`.
- SHA-256: `1763de390dd587c686fe84152c521a2d92e65b747fb2689ec2076c0560c576d7`.
- Artifact unsigned; `apksigner verify` -> `DOES NOT VERIFY`.
- APK не устанавливался, не передавался и не публиковался. Без release keystore и Firebase Android production config он не является installable/publishable production release.

## Ограничение

Staging notification/security/prod gates остаются отдельными проверками; локальный unit/build/lint gate зелёный.

## Ссылка на CI

GitHub Actions → android-verify.yml

## Связанные заметки

- [[MOC_Android]]
- [[Регламент_CI_CD]]
- [[Док_Android_Verification]]
- [[Док_Production_Rollout_20260810]]
