---
id: "proj-rocketflow"
тип: "проект"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "docs/66-weekly-focus-calendar-delivery.md", "README.md", "docs/04-architecture-blueprint.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Prod_Deploy_State"]
теги: ["проект", "rocketflow", "mvp"]
---

# RocketFlow

## Цель

Приложение для планирования задач с приоритетами, напоминаниями и совместным доступом. Помогает пользователю фокусироваться на важном через систему зелёных/красных задач, автоснижения приоритета при прокрастинации и повторяющихся задач.

## Стек

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.5, Spring Security, Spring Data JPA, Flyway, PostgreSQL 16 |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6, lucide-react |
| Android | Kotlin 1.9.24, minSdk 26, targetSdk 34, WorkManager 2.9.1, FCM 24.1.0 |
| CI/CD | GitHub Actions (ubuntu-24.04) |
| Production | [[HexCore]] (45.10.110.42), systemd + Nginx |
| Тестирование | JUnit + Embedded PostgreSQL (zonky), Robolectric 4.12.2 |

## Архитектура

[[Modular_Monolith]] — один бэкенд, одна БД, один фоновый планировщик, web SPA, Android клиент.

Модули бэкенда: `auth`, `accounts`, `settings`, `folders`, `goals`, `tasks`, `sharing`, `calendar`, `recurrence`, `reminders`, `prioritypolicy`, `notifications`, `ideas`, `links`, `notes`, `health`, `common`, `config`.

## Текущий статус

- Feature checkpoint 2026-08-10: ветка `codex/weekly-focus-calendar-web-push` готовится к commit/push; Calendar и Weekly Focus реализованы для backend, web и Android, server-owned Focus cadence поддерживает FCM и Web Push.
- Flyway additions: `V19__weekly_focus.sql` и `V20__focus_notifications.sql`.
- Verification: backend `135/0/0/0`, web `54 passed`, Android unit `77/0/0/0`; final implementation review **PASS**. Счётчики относятся к этому checkpoint.
- Production: feature-ветка **НЕ ЗАДЕПЛОЕНА**; migrations, backend/web promotion, APK rollout, notification enablement и production smoke не выполнялись.
- Android production signing **BLOCKED**: отсутствуют release keystore и Firebase production config. Debug/unit evidence не является production APK evidence.
- Canonical evidence: [[Док_Calendar_Weekly_Focus_WebPush_20260810]].

### Исторический MVP3 baseline

- Три волны (A, B, C) завершены
- Wave C.1 завершён (web scheduling authoring)
- Текущая стадия: [[MVP3_Упрощение]]
- Текущая точка 2026-06-13: ветка `MVP3`, `origin/MVP3` synced, HEAD `21f95c15166b9c41de4279c4209d00da429688f3` (`Fix Android goal and task creation flow`)
- `git rev-list --count MVP2..MVP3` = 23
- DB: в этой документационной задаче не перепроверялась; пользователь подтвердил, что DB работает
- Backend: последний зафиксированный evidence 2026-06-08 — `mvn --batch-mode --no-transfer-progress package` зелёный на втором запуске; `63/0/0/0`, `BUILD SUCCESS`, total `02:42`; jar `rocketflow-backend-0.1.0-SNAPSHOT.jar` 115,319,880 bytes. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Web: последний зафиксированный evidence 2026-06-07 — `npm run build` зелёный; 1792 modules transformed, built in `2.09s`; test scripts отсутствуют. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Android: последний зафиксированный evidence 2026-06-08 — `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug :app:lintDebug --no-daemon` зелёный, `BUILD SUCCESSFUL in 1m19s`. Для HEAD `21f95c1` нужен fresh evidence, если требуется актуальный gate.
- Android APK: `app-debug.apk` debug-signed и `apksigner` OK v2; `app-release-unsigned.apk` unsigned и `apksigner` DOES NOT VERIFY
- Cleanup/repo audit завершён: evidence сохранены в [[Док_Cleanup_Manifest]], cleanup invariants healthy, `.gitignore` покрывает generated paths и `android/local.properties`
- Notification E2E доказан локально
- Production model: [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, jar/systemd backend `rocketflow-backend` + web static via Nginx. Исторический baseline deploy 2026-06-19 выполнен через GitHub Actions release branch; он не включает текущую feature-ветку. См. [[CI_CD_Production_Status_20260619]].

Источник: [[Источник_Текущее_Состояние]]

## Команда

Роли агентов: [[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_QA]], [[Агент_DevOps]]

## Окружения

- Production: [[HexCore]] (45.10.110.42)
- Staging: через CI (GitHub Actions)
- Локально: dev-профиль Spring Boot, Embedded PostgreSQL

## Активные гейты

- Commit/push reviewed feature delta и подготовка release ref.
- Production rollout `V19`/`V20` с backup/rollback decision и post-migration verification.
- Production-equivalent FCM/Web Push configuration и provider smoke.
- Android signed production artifact: release keystore и Firebase config пока отсутствуют.

## Известные риски

- Automated tests не заменяют production migration/deploy/smoke evidence.
- Web Push и Focus cadence нельзя включать до production-equivalent credentials/configuration и контролируемого smoke.
- Android debug/unit evidence не закрывает signing, Play-services device и production FCM delivery.
- Historical baseline и current feature checkpoint должны оставаться явно разделены.

## Документация

- [[Источник_MVP_План]] — план MVP
- [[Источник_Спецификация_Домена]] — доменная модель
- [[Источник_Архитектура]] — архитектурный блюпринт
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
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]] — текущий feature checkpoint и release boundary

## Скрипты

- `Invoke-ProdPostgresBackupDownload.ps1` — скачивание production backup через SSH/SCP
- `Invoke-TwoUserSharingSmoke.ps1` — smoke-тест двухпользовательского sharing
- `Set-GitHubBranchProtection.ps1` — настройка защиты веток GitHub

## Ветки

- `codex/weekly-focus-calendar-web-push` (текущая feature-ветка), `MVP3`, `MVP2`, historical release refs, `master`

## Final production CI/CD state (2026-06-19)

- **Статус:** production deploy через GitHub Actions выполнен и зеленый.
- **Repo:** `C:\Users\style\Documents\Codex\RocketFlow`, remote `DmtrGoltsev/RocketFlow`.
- **Branches:** implementation `codex/rocketflow-cicd-prod-deploy-update`; release `release/rocketflow-prod-ci-cd-ec377a7`.
- **Release commit:** `4dbf10b0d693ea9f160993fe15199bc0047bb2ea`.
- **GitHub Actions:** `https://github.com/DmtrGoltsev/RocketFlow/actions/runs/27803394498`, success; package/deploy success.
- **Companion workflows:** verify runs on previous release commit succeeded; final release-branch companion workflows also completed successfully per worker.
- **Production symlinks:** backend `rocketflow-backend-sha-4dbf10b0d693.jar`; web `rocketflow-web-sha-4dbf10b0d693`.
- **Production smoke:** public/local health `UP`; `http://45.10.110.42/rocket/` -> 200; `http://45.10.110.42/rocket-api/health` -> 200, `{"status":"UP"}`.
- **Flyway:** rows `18 -> 18`; app Flyway lifecycle reported no migration necessary.
- **Residual risk:** independent DB read via local SSH principal unavailable; DB evidence comes from deploy logs.
- **Evidence:** [[CI_CD_Production_Status_20260619]].

## Связанные заметки

- [[Wave_A]], [[Wave_B]], [[Wave_C]] — завершённые волны
- [[MVP3_Упрощение]] — текущая стадия
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]] — Calendar/Weekly Focus/Web Push checkpoint
- [[Схема_Развертывания]] — схема деплоймента
- [[Схема_Базы_Данных]] — схема БД
