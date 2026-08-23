---
id: "proj-rocketflow"
тип: "проект"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["README.md", "docs/33-current-state-summary.md", "docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md", "docs/production/rocketflow-live-status.md"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
исторические_доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Production_Rollout_20260810", "docs/50-notification-runtime-clean-pass.md", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification"]
теги: ["проект", "rocketflow", "mvp"]
---

# RocketFlow

## Цель

Приложение для планирования папок, целей и задач с календарём, недельным фокусом, напоминаниями и совместным доступом. Фокус формируется явным списком задач и учитывает их трудоёмкость; числовой приоритет задач больше не является пользовательским или бизнес-понятием.

## Стек

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.5, Spring Security, Spring Data JPA, Flyway, PostgreSQL 18.4 ([[Док_Prod_Deploy_State|production evidence]]) |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6, lucide-react |
| Android | Kotlin 1.9.24, minSdk 26, targetSdk 34, WorkManager 2.9.1, FCM 24.1.0 |
| iOS | Native iOS 16+, Swift/SwiftUI, GRDB, XcodeGen, Swift Package Manager |
| CI/CD | GitHub Actions; macOS iOS Verify и platform-specific backend/web/Android lanes |
| Production | [[HexCore]] (45.10.110.42), systemd + Nginx |
| Тестирование | JUnit + Embedded PostgreSQL (zonky), Robolectric 4.12.2 |

## Архитектура

[[Modular_Monolith]] — один бэкенд, одна БД, один фоновый планировщик, web SPA, Android и native iOS клиенты.

Модули бэкенда: `auth`, `accounts`, `settings`, `folders`, `goals`, `tasks`, `sharing`, `calendar`, `recurrence`, `reminders`, `notifications`, `ideas`, `links`, `notes`, `health`, `common`, `config`. Legacy priority-policy wire/storage остаётся временным слоем совместимости V21 с V20 application rollback и старыми APK.

## Текущий статус

- Current repo docs HEAD: branch `codex/native-ios-companion`, SHA `b75ca723f767f520bee39ea72052b1a4b03a7e59`.
- Immutable Mac tooling evidence: SHA `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`, [run 32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719), job `97269056380`: contracts `174/174`, XcodeGen/parity/packages/build PASS, unit `540/0`, UI `2/0`; artifacts `9501177125` (`1,317,064` bytes) и `9501179599` (`25,070` bytes).
- Отдельное immutable app behavior/build evidence: SHA `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`, проверенный run `32655691351`; это не текущий branch HEAD или tooling SHA.
- Native iOS 16+ готов для clone/build/test на simulator: Planner, Calendar, Focus, offline GRDB/sync/conflicts, details/editors/sharing, reminders, RU/EN, durable restoration/deep links и account safety.
- [Behavior iOS Verify run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`: project/package parity и build PASS, `540` unit + `2` UI tests PASS; artifacts `9497494137` и `9497494432`. Exact evidence: [[Док_iOS_Verification]].
- CI policy пока candidate-only: feature push auto run `0` на `codex/native-ios-companion`; manual verify доступен, PR/master behavior станет default только после merge. Production workflows unchanged, branch protection не настроена; [[MOC_DevOps]].
- Mac handoff готов: другой Mac clone/pull branch и передаёт Codex canonical prompt из `docs/ios-native-mac-codex-install-prompt.md`; human boundary — `docs/72-native-ios-mac-device-handoff.md` и [[Пакет_iOS_Mac_Установка]]. Physical iPhone install ещё не доказан.
- Default personal iPhone flow — `no-push` с Apple Account/Team, уникальным bundle ID и device. Push optional и требует `GoogleService-Info.plist`, APNs/Firebase и production V22. App Store/public release остаётся **NO-GO** до HTTPS и real-device/accessibility/manual acceptance.

- Production rollout 2026-08-22 PASS: exact source SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, release `sha-50a63270ae09`, [GitHub Actions run 32551808905](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32551808905) `success`.
- Backend и web promoted совместно; preflight был `>=20`, manifest target и post-start count `>=21`; фактический Flyway достиг V21 (`21/21`). Backend health и web вернули HTTP `200`; duplicate promotion и rollback отсутствуют.
- Production server baseline остаётся V21 (`21/21`). Candidate V22 для iOS device registrations находится только в repository и не deployed; production DB в этой документационной задаче не проверялась.
- Authenticated disposable API smoke PASS; cleanup завершён, за окно smoke HTTP `5xx` — `0`.
- Personal direct-sideload APK `0.1.1` (`versionCode 2`) подписан и проверен: SHA-256 `3DF9EB210D801D932A4C736A0EF682C8C0AADCB36536B81CA19267F326C52AF7`; `adb install -r` сохранил UID и `firstInstallTime`; cold launch PASS, crash/ANR `0/0`, текущий экран — Login.
- Rollout выполнен по одноразовому [[ADR_V21_Release_Backup_Waiver]] без fresh DB recovery point. Waiver consumed и не является precedent; постоянный gate [[Задача_Production_Deploy_Backup_Rollback]] остаётся открытым.
- Canonical current evidence: [[Док_Prod_Deploy_State]] и [[Док_iOS_Verification]]. Dated V20/V21 и Android sideload records ниже являются historical evidence.

### Исторический production rollout 2026-08-10

- Production rollout 2026-08-10: exact SHA `910c061de4af9395d9bb682624bd966b2977a738` развёрнут как release `sha-910c061de4af`; backend/web promotion и Flyway `V19`/`V20` завершены успешно.
- Исторический feature checkpoint ранее в тот же день фиксировал branch `codex/weekly-focus-calendar-web-push` до commit/push и rollout; этот контекст сохранён в evidence.
- Flyway additions: `V19__weekly_focus.sql` и `V20__focus_notifications.sql`.
- Verification: backend `135/0/0/0`, web `54 passed`, Android unit `77/0/0/0`; final implementation review **PASS**. Счётчики относятся к этому checkpoint.
- Production: [GitHub Actions run 31357406631](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/31357406631) `success`; backend/web health `UP/200`, Flyway `20/20`, errors/5xx/restarts `0`.
- Focus cadence и Web Push остаются disabled. Authenticated read smoke не выполнен; unauthenticated protections прошли.
- Android Play Store production signing остаётся открытым gate. Текущий production-source sideload APK устанавливается и подписан существующим debug certificate, но не является Play Store release; Firebase config отсутствует. Старый unsigned artifact сохранён только как superseded damaged/non-installable evidence.
- Canonical evidence: [[Док_Production_Rollout_20260810]] и [[Док_Calendar_Weekly_Focus_WebPush_20260810]].

### Исторический MVP3 baseline

- Три волны (A, B, C) завершены
- Wave C.1 завершён (web scheduling authoring)
- Историческая стадия того периода: [[MVP3_Упрощение]]; она не является текущей стадией проекта.
- Historical checkpoint 2026-06-13: ветка `MVP3`, `origin/MVP3` была synced, HEAD `21f95c15166b9c41de4279c4209d00da429688f3` (`Fix Android goal and task creation flow`). Текущая candidate-ветка: `codex/native-ios-companion`.
- `git rev-list --count MVP2..MVP3` = 23
- DB: в этой документационной задаче не перепроверялась; пользователь подтвердил, что DB работает
- Backend: последний зафиксированный evidence 2026-06-08 — `mvn --batch-mode --no-transfer-progress package` зелёный на втором запуске; `63/0/0/0`, `BUILD SUCCESS`, total `02:42`; jar `rocketflow-backend-0.1.0-SNAPSHOT.jar` 115,319,880 bytes. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Web: последний зафиксированный evidence 2026-06-07 — `npm run build` зелёный; 1792 modules transformed, built in `2.09s`; test scripts отсутствуют. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Android: последний зафиксированный evidence 2026-06-08 — `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon` зелёный, `BUILD SUCCESSFUL in 1m19s`. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Android APK: `app-debug.apk` debug-signed и `apksigner` OK v2; `app-release-unsigned.apk` unsigned и `apksigner` DOES NOT VERIFY
- Cleanup/repo audit завершён: evidence сохранены в [[Док_Cleanup_Manifest]], cleanup invariants healthy, `.gitignore` покрывает generated paths и `android/local.properties`
- Notification E2E доказан локально
- Production model: [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, jar/systemd backend `rocketflow-backend` + web static via Nginx. Исторический baseline deploy 2026-06-19 см. в [[CI_CD_Production_Status_20260619]]; feature rollout 2026-08-10 см. в [[Док_Production_Rollout_20260810]].

Источник: [[Источник_Текущее_Состояние]]

## Команда

Роли агентов: [[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_iOS]], [[Агент_QA]], [[Агент_DevOps]]

## Окружения

- Production: [[HexCore]] (45.10.110.42)
- Staging: через CI (GitHub Actions)
- Локально: dev-профиль Spring Boot, Embedded PostgreSQL

## Активные гейты

- [ ] [[Задача_Production_Deploy_Backup_Rollback]] — dedicated backup identity, fresh verified backup before promotion и tested application rollback для будущих releases.
- Production-equivalent FCM/Web Push configuration и provider smoke.
- Android Play Store release identity и production Firebase configuration остаются отдельными gates; personal APK `0.1.1` подтверждён только для direct sideload.
- Apple signing/team и App Store provisioning.
- Optional push: `GoogleService-Info.plist`, APNs/Firebase и production deploy V22.
- HTTPS вместо временного host-scoped HTTP ATS exception.
- Выполнение [[Пакет_iOS_Mac_Установка]] и redacted physical iPhone evidence; затем accessibility/manual acceptance.

## Известные риски

- Одноразовый waiver для exact SHA `50a63270ae094fe08ee57b945be0930cb1115dfe` consumed при успешном rollout; fresh DB recovery point для этого release отсутствует. Waiver не может использоваться повторно: [[ADR_V21_Release_Backup_Waiver]].
- Web Push и Focus cadence нельзя включать до production-equivalent credentials/configuration и контролируемого provider smoke.
- Android debug/unit evidence не закрывает signing, Play-services device и production FCM delivery.
- Green iOS simulator/tooling CI не закрывает Apple signing, physical iPhone result, production push или App Store acceptance; V22 не deployed.
- Historical MVP3/release baselines и текущий candidate checkpoint `codex/native-ios-companion` должны оставаться явно разделены.

## Документация

- [[Источник_MVP_План]] — план MVP
- [[Источник_Спецификация_Домена]] — доменная модель
- [[02_Знания/Источники/RocketFlow/Источник_Архитектура|Источник_Архитектура]] — архитектурный блюпринт
- [[Источник_API_Контракты]] — API
- [[Источник_Текущее_Состояние]] — текущий статус
- [[Источник_Android_Local_Setup]] — локальная Android SDK/emulator конфигурация
- [[Источник_CI_CD_Политика]] — CI/CD
- [[Источник_Продакшен_Runbook]] — production runbook
- [[Источник_MVP2_Иерархия]] — контракт MVP2: иерархия, заметки, связи
- [[Источник_MVP3_QA_Модель]] — QA-модель приёмки MVP3
- [[Источник_MVP3_BA_Пути]] — BA-контракт: пользовательские пути MVP3
- [[Источник_Бэкап_Runbook]] — runbook скачивания production backup
- [[Док_Cleanup_Manifest]] — cleanup/evidence manifest
- [[Док_Backend_Verification]], [[Док_Web_Verification]], [[Док_Android_Verification]] — статус verification после audit
- [[Док_Prod_Deploy_State]] — фактическая production deploy model
- [[Док_V21_Scroll_Priority_20260822]] — historical V21 delivery и production rollout evidence
- [[MOC_iOS]], [[Пакет_iOS]], [[Пакет_iOS_Mac_Установка]], [[Агент_iOS]] — iOS architecture, Mac/iPhone handoff и ownership
- [[Док_iOS_Verification]] — exact iOS run/job/tests/artifacts и release boundary
- [[ADR_V21_Release_Backup_Waiver]] — исполненный одноразовый waiver для exact SHA
- [[Задача_Production_Deploy_Backup_Rollback]] — открытый постоянный backup/rollback gate
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]] — исторический feature checkpoint и release boundary
- [[Док_Production_Rollout_20260810]] — historical V20 production rollout, backup, rollback readiness и smoke boundary

## Скрипты

- `Invoke-ProdPostgresBackupDownload.ps1` — скачивание production backup через SSH/SCP
- `Invoke-TwoUserSharingSmoke.ps1` — smoke-тест двухпользовательского sharing
- `Set-GitHubBranchProtection.ps1` — настройка защиты веток GitHub

## Ветки

- Текущая candidate-ветка `codex/native-ios-companion`: docs HEAD `b75ca723f767f520bee39ea72052b1a4b03a7e59`; immutable tooling evidence `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`; immutable app behavior evidence `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`. `codex/weekly-focus-calendar-web-push`, `release-weekly-focus-calendar-910c061de4af`, `MVP3`, `MVP2`, historical release refs и `master` перечислены только как historical/adjacent refs, не как текущая стадия.

## Historical production CI/CD checkpoint (2026-06-19)

- **Статус на 2026-06-19:** production deploy через GitHub Actions был выполнен и был green; это historical checkpoint, а не текущий production state.
- **Repo:** RocketFlow repository root (`.`), remote `DmtrGoltsev/RocketFlow`.
- **Branches:** implementation `codex/rocketflow-cicd-prod-deploy-update`; release `release/rocketflow-prod-ci-cd-ec377a7`.
- **Release commit:** `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`.
- **GitHub Actions:** `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/27803394498`, success; package/deploy success.
- **Companion workflows:** verify runs on previous release commit succeeded; final release-branch companion workflows also completed successfully per worker.
- **Production symlinks:** backend `rocketflow-backend-sha-4dbf10b0d693.jar`; web `rocketflow-web-sha-4dbf10b0d693`.
- **Production smoke:** public/local health `UP`; `http://45.10.110.42/rocket/` -> 200; `http://45.10.110.42/rocket-api/health` -> 200, `{"status":"UP"}`.
- **Flyway на этом checkpoint:** rows `18 -> 18`; app Flyway lifecycle reported no migration necessary. Текущий production baseline отдельно зафиксирован как V21 (`21/21`).
- **Residual risk:** independent DB read via local SSH principal unavailable; DB evidence comes from deploy logs.
- **Evidence:** [[CI_CD_Production_Status_20260619]].

## Historical production rollout state (2026-08-10)

- **Статус:** backend/web rollout PASS; rollback не использован.
- **Source/deployed SHA:** `910c061de4af9395d9bb682624bd966b2977a738`; release `sha-910c061de4af`.
- **GitHub Actions:** `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/31357406631`, success.
- **Flyway на historical checkpoint 2026-08-10:** `V20`, `20/20` successful, `0` failed. Текущий production baseline: V21 (`21/21`).
- **Runtime:** health `UP/200`; errors/5xx/restarts `0`.
- **Flags:** Focus cadence и Web Push disabled.
- **Residuals:** authenticated read smoke gap; unsigned/non-publishable Android artifact; Firebase Android config absent.
- **Evidence:** [[Док_Production_Rollout_20260810]].

## Связанные заметки

- [[Wave_A]], [[Wave_B]], [[Wave_C]] — завершённые волны
- [[MVP3_Упрощение]] — historical MVP3 baseline; текущая candidate-ветка `codex/native-ios-companion`
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]] — historical Calendar/Weekly Focus/Web Push checkpoint
- [[Док_Production_Rollout_20260810]] — historical V20 production rollout 2026-08-10
- [[Док_V21_Scroll_Priority_20260822]] — historical V21 production rollout 2026-08-22
- [[Док_iOS_Verification]] — green native iOS delivery 2026-08-23
- [[Пакет_iOS_Mac_Установка]] — canonical Mac/iPhone handoff 2026-08-24
- [[MOC_iOS]] — native iOS карта
- [[ADR_V21_Release_Backup_Waiver]] — consumed waiver для exact SHA
- [[Задача_Production_Deploy_Backup_Rollback]] — будущий обязательный gate
- [[Схема_Развертывания]] — схема деплоймента
- [[Схема_Базы_Данных]] — схема БД
