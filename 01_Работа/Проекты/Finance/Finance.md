---
id: "project-finance"
тип: "проект"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["проект", "finance", "финансы", "учёт", "MVP"]
источники:
  - "docs/product-mvp.md"
  - "docs/current-status.md"
  - "docs/architecture/decision-records/adr-0001-stack-repo-layout.md"
  - "README.md"
ссылки:
  - "[[MOC_Finance]]"
  - "[[MOC_Все_Проекты]]"
---

# Finance — ручной учёт личных и семейных финансов

> **Синхронизировано 2026-06-05.** Знания обновлены по состоянию кода на ветку `codex/auto-capture-drafts`. Глоссарий расширен (18 терминов), добавлены ADR, архитектурные пакеты контекста. Delivery-слои (задачи, доказательства, промпты, схемы) — в процессе заполнения.

## Цель

Ручной учёт личных и семейных финансов. Personal/shared разделение, user-initiated OCR черновики. Закрытый MVP.

**Production GO:** 2026-05-19

## Стек

| Слой | Технологии |
|------|-----------|
| Backend | Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x (async), Alembic, Pydantic |
| БД | PostgreSQL 16 (decimal numeric) |
| PWA | TypeScript, React 19, Vite 7, TanStack Query, Capacitor iOS, Vitest, Playwright |
| Android | Kotlin, Jetpack Compose, Retrofit/OkHttp, Room (scoped cache), JUnit, on-device OCR |
| API | OpenAPI 3.1 contract-first (`api/openapi/openapi.yaml`) |
| Auth | PWA: HttpOnly Secure SameSite cookie + CSRF; Android: Bearer + rotating refresh (Keystore) |
| OCR | Android on-device; PWA/iOS: Tesseract backend (временная загрузка) |
| Деплой | Self-hosted Linux (systemd/nginx), `/finance/` + `/finance-api/`, без Docker |
| QA | pytest, Schemathesis, Vitest, Playwright, JUnit |
| Security | Argon2id/bcrypt, gitleaks, pip-audit, npm audit |

## Архитектура

Contract-first монолит-монорепо. Backend FastAPI — единственный сервер. Клиенты: PWA (React/Vite + Capacitor iOS), Android (Kotlin/Compose). OpenAPI 3.1 — source of truth → генерация клиентов. REST API `/api/v1`.

## Модули

| Модуль | Путь | Назначение |
|--------|------|-----------|
| Backend | `apps/backend/` | FastAPI сервер |
| PWA | `apps/web-pwa/` | React/Vite PWA + Capacitor iOS |
| Android | `apps/android/` | Kotlin/Compose приложение |
| API Spec | `api/openapi/` | OpenAPI 3.1 контракт |
| Миграции | `db/migrations/` | Alembic миграции |
| Фикстуры | `db/seeds/` | Тестовые фикстуры |
| QA | `qa/` | Чек-листы |
| Security | `security/` | Сканы, evidence |
| Ops | `ops/` | Backup/restore |
| Docs | `docs/` | Архитектура, compliance, planning |
| Клиенты | `packages/` | Генерация клиентов |
| Evidence | `MVP_EVIDENCE/` | Production QA evidence |

## Текущая стадия

**Production MVP functional GO (2026-05-19)** — закрытый MVP в production.

## Ветки

- `codex/auto-capture-drafts` — текущая активная ветка
- `main` — стабильная

## Окружения

| Окружение | Описание |
|-----------|----------|
| Development | Локально, .venv, npm run dev, Android emulator |
| Staging | Упоминается |
| Production | Self-hosted Linux, nginx |

## Ключевые термины

См. [[MOC_Finance#Глоссарий|глоссарий проекта]].

## Privacy/Security инварианты

1. Personal owner-only
2. Shared active-only
3. Filter-before-aggregate
4. Same-scope transfers
5. Neutral responses
6. Capture drafts user-initiated
7. No secrets in logs
8. No bank/broker credentials
9. Server-side authz only
10. Backup encryption

## Риски

| ID | Описание |
|----|----------|
| P1-B02 | Критический баг №02 |
| P1-B03 | Критический баг №03 |
| Tag | Tag misalignment |

## Связанные заметки

- [[MOC_Finance]] — навигационная MOC-карта
- [[MOC_Все_Проекты]] — все проекты vault
