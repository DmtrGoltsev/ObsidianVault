---
id: "finance-release-planning-mvp-20260607"
тип: "доказательство"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-08"
обновлено: "2026-06-08"
уверенность: "высокая"
источники:
  - "Project release facts from Finance delivery handoff"
доказательства:
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
теги: ["finance", "release", "planning-mvp", "production", "evidence"]
ссылки:
  - "[[Finance]]"
  - "[[MOC_Finance]]"
  - "[[Пакет_Finance_Полный]]"
---

# Release evidence — Planning iteration MVP (2026-06-07)

## Что доказывается

Planning iteration MVP закрыт, project branch `codex/finance-planning-mvp-gpt5` запушен в `origin`, production backend и web указывают на один project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`.

## Метод проверки

- Проверка release metadata: commit, branch, release id, production `COMMIT` files.
- Проверка БД: Alembic head.
- Проверка production runtime: systemd service, direct/nginx health, web static/PWA endpoints.
- Проверка QA gate: OpenAPI parse, operationId uniqueness, backend tests, Android unit/build.
- Проверка Android artifact: путь, размер, SHA256.

## Результат

| Проверка | Значение |
|----------|----------|
| Статус | Пройдено с ограничениями |
| Project commit | `819b5815fed8c81bfa6a6e6131e790429454c2e8` |
| Commit message | `Release planning iteration MVP` |
| Project branch | `codex/finance-planning-mvp-gpt5` -> `origin` |
| Release id | `20260607T225457Z-819b5815` |
| Backend current | `/opt/finance/releases/20260607T225457Z-819b5815` |
| Web current | `/var/www/finance/releases/20260607T225457Z-819b5815` |
| Production COMMIT files | оба указывают на `819b5815fed8c81bfa6a6e6131e790429454c2e8` |
| Alembic head | `20260607_0013 (head)` |
| Backend service | `finance-backend.service` active |
| Health checks | `127.0.0.1:8081/health` OK; `/finance-api/health` OK |
| Web checks | `/finance/` 200; manifest scope/start_url `/finance/`; `/finance/sw.js` 200 |

## QA gate

| Область | Результат |
|---------|-----------|
| OpenAPI | parse OK |
| OperationId | duplicates `0/58` |
| Backend | `243 passed, 9 warnings` |
| Android unit | PASS |
| Android assembleDebug | PASS |

## Android artifact

| Параметр | Значение |
|----------|----------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-0.1.0-debug.apk` |
| Size | `54,235,660` |
| SHA256 | `E1ACA5858CDD8B31C995BB669791955C3B57079978BE794731E63B82FBB956D4` |
| Signing | debug-signed, не release-signed |

## Acceptance clarification

- Planning progress является allocation-level: `PlanningAllocationDto.actualAmount`, `varianceAmount`, `status`, `attentionReason`.
- Не вводить и не искать plan-level `PlanningPlanDto.progress`.
- `previousMonthSurplus` находится в `PlanningSummaryDto`.

## Исключено из project release commit

- `rules.md`
- unrelated OCR androidTest capture folder
- старые `MVP_EVIDENCE/prod-*`
- build outputs и APK, которые остаются ignored

## Известные ограничения и риски

- Authenticated QA login/OCR smoke не запускался: нет operator password/session token.
- Выполнены только health/static deploy checks для production.
- APK является debug-signed, не release-signed.
