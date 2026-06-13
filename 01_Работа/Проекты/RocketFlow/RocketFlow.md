---
id: "proj-rocketflow"
тип: "проект"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-13"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "README.md", "docs/04-architecture-blueprint.md"]
доказательства: ["docs/50-notification-runtime-clean-pass.md", "Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Prod_Deploy_State"]
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
- Production model: [[HexCore]] `rocketflow-prod-01` / `45.10.110.42`, jar/systemd backend `rocketflow-backend` + web static via Nginx. Backend prod deploy 2026-06-08: **NOT DEPLOYED / BLOCKED** до решения по target ref/method, backup expectation и secrets/env readiness.

Источник: [[Источник_Текущее_Состояние]]

## Команда

Роли агентов: [[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_QA]], [[Агент_DevOps]]

## Окружения

- Production: [[HexCore]] (45.10.110.42)
- Staging: через CI (GitHub Actions)
- Локально: dev-профиль Spring Boot, Embedded PostgreSQL

## Активные гейты

- GHCR publish/workflow восстановление (workflow отсутствует/open gate)
- Staging notification certification
- Backend prod deploy approval/readiness: current branch `MVP3`, canonical workflow deploy branches `MVP2`/`release_1`; local shell lacks `HEXCORE_PROD_SSH_*` and `ROCKETFLOW_PROD_BACKUP_*`

## Известные риски

- Notification smoke на staging ещё не сертифицирован
- GHCR интеграция не закрыта: workflow отсутствует или требует восстановления, credentials не подтверждены
- Android push-tap flow требует staging-валидации; локальный Android full gate после cleanup зелёный
- Prod deploy preflight выявил backup user mismatch: preferred `rocketbackup`, ignored local config points to `rocketdeploy`

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

## Скрипты

- `Invoke-ProdPostgresBackupDownload.ps1` — скачивание production backup через SSH/SCP
- `Invoke-TwoUserSharingSmoke.ps1` — smoke-тест двухпользовательского sharing
- `Set-GitHubBranchProtection.ps1` — настройка защиты веток GitHub

## Ветки

- `MVP3` (активная), `MVP2`, `release_1`, `backup/release_1-before-rollback-20260518`, `master`

## Связанные заметки

- [[Wave_A]], [[Wave_B]], [[Wave_C]] — завершённые волны
- [[MVP3_Упрощение]] — текущая стадия
- [[Схема_Развертывания]] — схема деплоймента
- [[Схема_Базы_Данных]] — схема БД
