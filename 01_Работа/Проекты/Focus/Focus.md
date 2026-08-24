---
id: "proj-focus-001"
тип: "проект"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-01"
обновлено: "2026-06-19"
уверенность: "высокая"
источники:
  - "[[Источник_Промпт]]"
  - "[[Источник_Архитектура]]"
  - "[[Источник_API]]"
доказательства:
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
  - "[[QA_ТестКейсы_v2]]"
теги:
  - "focus"
  - "планировщик"
  - "spring_boot"
  - "react"
  - "android"
---

# Focus

## Цель продукта

Focus — планировщик задач, который помогает пользователю фокусироваться на важном. Ключевая механика: задачи делятся на два типа — **Green** (выполнение двигает к успеху) и **Red** (невыполнение создаёт негативные последствия). Пользователь организует работу в иерархии: **Папки → Цели → Задачи**. Цели и задачи можно шарить с другими пользователями по email-инвайту.

## Стек технологий

| Слой | Технологии |
|------|-----------|
| Backend | Java 21, Spring Boot 3.4.1, Spring Security, Spring Data JPA, Flyway, PostgreSQL 18 |
| Web | React 18, TypeScript 5, Vite 5, react-router-dom 6 |
| Android | Kotlin, minSdk 26, targetSdk 34, Room, WorkManager 2.9.1, FCM |
| CI/CD | GitHub Actions |
| Production | systemd + Nginx |

## Архитектура

**Modular Monolith** — один бэкенд, одна БД, REST API с JWT (access + refresh). Soft delete для folders/goals/tasks. Optimistic locking через @Version. In-process scheduler для напоминаний.

Решение: [[ADR_Modular_Monolith]]

## Модули бэкенда

- `auth` — аутентификация, JWT access/refresh, логаут
- `accounts` — профиль пользователя, часовой пояс
- `settings` — язык интерфейса, политики priority decay
- `folders` — CRUD папок, порядок отображения
- `goals` — CRUD целей внутри папок
- `tasks` — CRUD задач, green/red, приоритет 1-10, статусы, теги, связи
- `sharing` — инвайты по email, goal/task sharing
- `calendar` — day/week/month проекции
- `recurrence` — правила повторения ([[Recurrence_Rule]])
- `reminders` — правила напоминаний ([[Reminder_Rule]])
- `prioritypolicy` — автоснижение приоритета ([[Priority_Decay]])
- `notifications` — push через FCM, регистрация устройств
- `health` — health-check

## Текущий статус

**Production GO (2026-06-07)** — развёрнут на [[HexCore]] (`45.10.110.42`)

### Production deploy policy (2026-06-13)

- Основной путь production deploy: GitHub Actions workflow `.github/workflows/backend-prod-deploy.yml`.
- Auto deploy разрешен только для push в ветки, имя которых содержит `release`; `master`/`main` больше не auto-deploy ветки.
- GitHub environment: `production`; required secrets by name: `SSH_HOST`, `SSH_USERNAME`, `SSH_KEY`.
- Direct SSH/SCP upload to HexCore остается fallback/alternative, не основной путь.
- Production artifact удаляет `frontend/dist/auto-login*.html`; source still needs hardcoded token rotation/review.
- Эта запись описывает policy/update, а не подтверждает новый реальный deploy.

- Backend: systemd `focus.service`, порт 8082, JVM 256 MB
- Frontend: `/var/www/focus/`, nginx location `/focus/`
- API: nginx location `/focus-api/` → proxy на 8082
- БД: PostgreSQL 18, БД `focus_db`, пользователь `focus_user`
- URL: `http://45.10.110.42/focus/`

### Статус кода

- Backend: 22 фикса применён (FIX-A — FIX-V), BE-101 исправлен
- Frontend: ретро-стиль UI, 18/18 Playwright E2E PASS, recurring reminders UI
- Android: офлайн-first компаньон, Room + WorkManager, recurring reminders DTO
- Все сборки: mvn test 21/21 PASS, npm run build OK, assembleDebug OK
- **Новое:** Повторяющиеся напоминания (HOURLY/DAILY/WEEKLY) — backend логика `calculateRecurringTrigger()` с период-выравниванием, фронтенд условный UI, V5 Flyway миграция. Коммит `50a5a0f`.

### QA прогресс (2026-06-12)

| Метрика | Значение |
|---|---|
| Всего тест-кейсов | 253 (v2) + 47 (v3 quorum) + 13 (QA3 backend E2E) + 2 (QA3 Android E2E) = 315 |
| Протестировано (Волны 1-9) | ~155 (61% от v2) |
| Протестировано QE v3 backend | 29/47 (62%) |
| PASS v3 backend | 29 |
| Протестировано QA3 backend E2E | 13/13 (100%) |
| PASS QA3 backend E2E | 13 |
| Протестировано QA3 Android E2E | 2/2 (1 FAIL, 1 SKIP) |
| FAIL (открытые баги) | 2 (BE-101, AND-101) |
| Playwright E2E | 18/18 PASS |
| Android E2E | 9 PASS, 2 MANUAL (color-only) |
| MANUAL | 2 (AND-040, AND-012) |
| Фиксов применено | 22 (FIX-A — FIX-V) |
| FCM интеграция | Реализована (backend+android), верифицирована сборка, ожидает тестирования (disabled по умолчанию) |

См. подробности: [[QA_Результаты]], [[QA_Фиксы]], [[QA_ТестКейсы_v2]]

### Предыдущий аудит (2026-06-04)

Из 24 бизнес-требований: **9 работают полностью, 7 частично, 8 не реализованы**.
Ключевые проблемы: FCM мёртвый, Sharing не давал доступ (FIX-O), Decay settings не сохранялись (FIX-M),
Recurrence/Reminders/Links нет в UI, Offline sync только CREATE.

См. полный аудит: [[Аудит_Реальный_Статус]]
См. план исправлений: [[План_Исправлений_Focus]]

## Риски

- ~~BE-101: Goal owner не может редактировать task созданный shared user → пофикшен~~
- **AND-101: Android — токен не сохраняется в EncryptedSharedPreferences. После force-stop/restart — экран авторизации. Требуется расследование TokenManager/EncryptedSharedPreferences.**
- FCM push — реализована (backend+android, FIX-U wave), disabled по умолчанию. Для активации нужен Firebase project + credentials (Phase 3 nice-to-have)
- ReminderScheduler advisory lock — H2 fallback в тестах (noise, не блокер)

## Ссылки

- [[MOC_Focus]] — карта всех заметок проекта
- [[MOC_Все_Проекты]] — все проекты vault
- [[HexCore]] — production-сервер
- [[Регламент_Деплоя_Focus]] — процедура деплоя
- [[Источник_Промпт]] — промпт инициализации проекта
- [[Источник_Архитектура]] — архитектурные решения
- [[Источник_API]] — API-контракты
- [[Пакет_Focus_Полный]] — пакет контекста (агрегат)

### Final CI/CD local preparation status (2026-06-14)

- User confirmed Focus is prod.
- Read-only HexCore inventory: `focus.service`, `/focus/ -> /var/www/focus/`, `/focus-api/ -> 127.0.0.1:8082/api/`, DB `focus_db`, env `/opt/focus/.env`, health OK.
- Local CI/CD preparation PASS: strengthened `.github/workflows/backend-prod-deploy.yml`, added `.github/workflows/focus-prod-rollback.yml`, prepared `docs/production/focus-*`, aligned nginx example.
- Release push build/package only; prod mutation dispatch-gated; Flyway guarded; rollback requires current-release confirmation.
- No raw input interpolation and no hardcoded secret values in reviewed workflow scope.
- Historical note: no production deploy was executed during the 2026-06-14 preparation update; superseded by final deploy evidence on 2026-06-19.
- Residual approvals: GitHub production environment/secrets/required reviewers, first production run, deploy/restart/migration/rollback approvals, DB backup proof.
- Evidence: [[CI_CD_Production_Status_20260614]].

### Final production CI/CD state (2026-06-19)

- **Статус:** production deploy через GitHub Actions выполнен и зеленый.
- **Repo:** `C:\Users\style\Documents\VS_Agents\Focus`, remote `DmtrGoltsev/Focus`.
- **Branches:** implementation `feature/softer-green-and-reminders`; release `release/focus-prod-ci-cd-fe6f5af`.
- **Release-green commit:** `ddb4262`.
- **Production Deploy:** `https://github.com/DmtrGoltsev/Focus/actions/runs/27804739744`, success; все production jobs success. Более ранний production success `https://github.com/DmtrGoltsev/Focus/actions/runs/27804213793` остается валидным historical evidence.
- **Android Verify:** release branch `https://github.com/DmtrGoltsev/Focus/actions/runs/27804739739`, success; feature proof `https://github.com/DmtrGoltsev/Focus/actions/runs/27804587155`, success.
- **Android rerun fix:** `android/gradlew` executable mode восстановлен в git (`100644 -> 100755`); Gradle wrapper должен оставаться executable.
- **Production smoke:** `http://45.10.110.42/focus/` -> 200; `http://45.10.110.42/focus-api/health` -> 200.
- **Flyway:** V5/V6 применены во время retry; текущая версия `6`; финальный run подтвердил `6 -> 6`.
- **Backup evidence:** `/opt/focus/backups/github-actions/release-focus-prod-ci-cd-fe6f5af-7/focus_db-release-focus-prod-ci-cd-fe6f5af-7-pre-flyway.evidence.txt`, sha256 `c8d60f1b54b2b0f1dc64d8141fa19920c59d276be5e18220abf9dcf48a0e7936`, bytes `93618`.
- **Earlier backup before V4 -> V6:** `/opt/focus/backups/github-actions/release-focus-prod-ci-cd-fe6f5af-6/...`, sha256 `786bf0bd2d938ee569f2b64449956cc8289e386a5c956de818b16c10889466e4`.
- **Evidence:** [[CI_CD_Production_Status_20260619]].
