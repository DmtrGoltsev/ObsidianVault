---
id: "quorum-finance"
тип: "пакет_контекста"
проект: "Finance"
название: "Кворум Finance — саммари высокой уверенности"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
теги: ["кворум", "finance", "саммари"]
источники:
  - "[[Источник_README]]"
  - "[[Источник_Продукт_MVP]]"
  - "[[Источник_ADR_0001]]"
  - "[[Источник_Security_Baseline]]"
  - "[[Источник_Текущий_Статус]]"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
  - "[[Пакет_Finance_Полный]]"
---

# Кворум Finance — саммари

**Уверенность:** высокая — данные подтверждены документацией проекта и доказательствами production QA.

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

`apps/backend/`, `apps/web-pwa/`, `apps/android/`, `api/openapi/`, `db/migrations/`, `db/seeds/`, `qa/`, `security/`, `ops/`, `docs/`, `packages/`, `MVP_EVIDENCE/`

## Ключевые термины (18)

Household, Personal, Shared, Membership (invited/active/left/revoked), Active member, Invited/Former Member, Invite (hash-only), Account (cash/bank/deposit/brokerage, personal/shared), Transaction (income/expense/transfer/brokerage, sourceType=manual), Transfer (personal_same_owner/household_same_household), Category (income/expense, personal/household), Report (shared_family_report, combined_viewer_overview), Capture Draft (pending/confirmed/discarded), Source type manual, Neutral response, Filter-before-aggregate.

## Privacy/Security инварианты (10)

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

## Окружения

| Окружение | Описание |
|-----------|----------|
| Development | Локально, .venv, npm run dev, Android emulator |
| Production | Self-hosted, nginx |
| Staging | Упоминается |

## Ветки

- `codex/auto-capture-drafts` — текущая
- `main` — стабильная

## Ключевая документация

- `README.md`
- `AGENTS.md`
- `docs/product-mvp.md`
- `docs/current-status.md`
- `docs/user-guide-ru.md`
- `docs/product/ux-quorum-design-decision-ru.md`
- `docs/architecture/domain-model.md`
- `docs/architecture/access-model.md`
- `docs/architecture/canonical-api-vocabulary.md`
- `docs/architecture/decision-records/adr-0001-stack-repo-layout.md`
- `docs/security/security-baseline.md`
- `docs/security/security-release-checklist.md`
- `docs/compliance/privacy-flows-mvp.md`
- `docs/deploy/finance-production-install.md`
- `docs/planning/wave-2-backlog.md`
- `ops/backup-restore-plan.md`
- `security/evidence-plan.md`
- `MVP_EVIDENCE/release-checklist.md`
- `MVP_EVIDENCE/MVP_RELEASE_REPORT.md`

## Риски

- **P1-B02** — критический баг
- **P1-B03** — критический баг
- **Tag misalignment** — расхождение тегов

## Разногласия

Разногласий по ключевым аспектам не зафиксировано. Данные кворума подтверждены документацией и production QA evidence.
