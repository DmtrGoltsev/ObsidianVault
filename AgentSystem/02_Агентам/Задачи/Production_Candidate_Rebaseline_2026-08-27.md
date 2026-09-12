---
id: "n8nagents-production-candidate-rebaseline-2026-08-27"
тип: "аудит"
статус: "активно"
проект: "AgentSystem"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "C:/Users/style/Documents/New project/N8N_AGENT_MASTER_PROMPT.md"
  - "C:/Users/style/Documents/ChatGPT/Агенты/N8NAgents"
  - "[[Итог_FastTrack_Local_Docker_2026-08-27]]"
  - "[[VPS_Rebaseline_2026-08-27]]"
доказательства:
  - "git status/rev-parse/diff/ls-files, read-only, 2026-08-27"
теги: ["n8n", "production", "rebaseline", "release", "gap-analysis"]
---

# N8NAgents — rebaseline production-кандидата

## Вывод

Текущий репозиторий — сильная production foundation, но **не готовый production-кандидат и не финальный продукт**. Локальная Docker-лаборатория доказала PostgreSQL+n8n, persistence, mock Telegram, один dev-bot E2E и локальный logical restore. Production acceptance из master prompt пока не выполнен: отсутствуют реальные production workflows, DeepSeek gate, публичный Caddy/TLS и Telegram webhook, проверенная память/reminders, encrypted off-host backup и действующее monitoring/alerting.

Финальный статус на этом снимке: `PRODUCTION_CANDIDATE=NOT_READY`, `LOCAL_LAB=PASS`, `VPS_FRESH_STATE=BLOCKED`.

## Git baseline

- Репозиторий: `C:/Users/style/Documents/ChatGPT/Агенты/N8NAgents`
- Ветка: `codex/n8nagents-foundation`
- `HEAD`: `11974a33fa78bb72598059671cef9465402ab091`
- Последний commit: `fix: harden phase a release publication gate`
- Index/staged: `0`
- Modified, unstaged: `12`
- Untracked files: `29`
- Stash/reset/clean/checkout не выполнялись; все пользовательские изменения сохранены.

Modified:

1. `docs/deploy-rollback-manifest.md`
2. `docs/local-verification-result.md`
3. `docs/verification-matrix.md`
4. `infra/phase-a-compose.sh`
5. `infra/phase-a-release-gate.sh`
6. `infra/verify-release-governance.sh`
7. `scripts/package-reviewed-release.ps1`
8. `scripts/test-package-reviewed-release.ps1`
9. `scripts/test-release-governance.sh`
10. `scripts/test-remote-package-gate.sh`
11. `scripts/verify-static.ps1`
12. `scripts/verify-static.sh`

Untracked production/release work (`9`):

1. `infra/phase-a-runner-bootstrap.sh`
2. `scripts/build-k4r-evidence.py`
3. `scripts/build-reviewed-candidate.ps1`
4. `scripts/lib/GitTreeValidation.psm1`
5. `scripts/requirements-k4r.lock`
6. `scripts/run-k4r-offline.ps1`
7. `scripts/test-k4r-evidence.py`
8. `scripts/test-phase-a-release-gate-linux.sh`
9. `scripts/test-runner-bootstrap-linux.sh`

Untracked local laboratory (`20`, весь `local/`): `.env.example`, `.gitignore`, `README.md`, Compose/PowerShell control plane, two entrypoints, loopback proxy, bridge core/runtime, two mocks, four tests, local Telegram workflow, secrets README и evidence sentinel. Secret values и ignored runtime artifacts в Git baseline не включались.

## Группировка по production readiness

| Группа | Существующие файлы | Оценка |
|---|---|---|
| Core topology | `infra/compose.yaml`, `infra/compose.bootstrap.yaml`, `infra/Caddyfile`, `.env.example` | Архитектурный draft готов; внутренний PG+n8n и public-edge profile описаны. Не развернуто и не подтверждено production evidence. |
| PostgreSQL foundation | `infra/postgres/init`, migrations `001–004`, healthcheck, SQL contract/fault tests | Наиболее зрелая часть: роли, схемы, пять SQL API, memory table, idempotency/update/reminder tables. Production runtime и n8n bindings не доказаны. |
| Trust contracts | `contracts/*.schema.json`, fixtures | Готовы к использованию как границы данных; сами по себе не реализуют workflows. |
| Production workflows | `workflows/specs/*.md` | Только спецификации. Production JSON exports отсутствуют намеренно; exact n8n 2.36.7 import/live gate не пройден. |
| Release/candidate custody | K4R packaging/evidence/governance scripts и Linux tests | Механизм содержательный, но текущая реализация распределена между 12 modified и 9 untracked files. Нет единого committed exact candidate, frozen package, accepted independent review или remote execution-GO. |
| Backup/restore | `infra/backup/*`, `infra/systemd/n8nagents-backup*`, backup runbook | Реализация draft существует. Нет production encryption/signing custody, immutable off-host remote, установленного timer, live backup, tamper evidence и isolated production restore drill. |
| Monitoring | Compose healthchecks, operations runbook, backup `OnFailure` journal placeholder | Health primitives есть, но отдельного monitoring service/check runner, alert delivery, SLO/thresholds и проверенного failure path нет. |
| Local laboratory | `local/*` | `LOCAL_CORE_READY` и `TELEGRAM_LOCAL_READY` доказаны локально. Это источник проверенных паттернов, но не production candidate. |

## Exact candidate/release assets, которые уже существуют

Candidate/package pipeline:

- `scripts/build-reviewed-candidate.ps1` — deterministic archive из exact Git commit, два byte-identical build, outputs вне repo.
- `scripts/run-k4r-offline.ps1` — двухфазный offline orchestrator; без Linux capability/matrices fail-closed.
- `scripts/package-reviewed-release.ps1` — пересборка и binding candidate/static/behaviour evidence.
- `scripts/build-k4r-evidence.py` и `scripts/lib/GitTreeValidation.psm1` — schema/evidence и Git-tree validation.

Remote release pipeline:

- `infra/phase-a-runner-bootstrap.sh` — pinned no-network bootstrap fixed-path runner.
- `infra/phase-a-release-gate.sh` — publication/activation/rollback gate.
- `infra/verify-release-governance.sh` — binding package/review/ledger/execution-GO/release tree.
- `infra/phase-a-compose.sh` — narrow allowlisted Compose wrapper для internal PG+n8n.

Existing tests:

- `scripts/test-k4r-evidence.py`
- `scripts/test-package-reviewed-release.ps1`
- `scripts/test-phase-a-release-gate-linux.sh`
- `scripts/test-runner-bootstrap-linux.sh`
- `scripts/test-release-governance.sh`
- `scripts/test-remote-package-gate.sh`
- `scripts/verify-static.ps1` / `.sh`
- `scripts/verify-postgres.ps1` и `infra/postgres/tests/*`

Ограничение: эти файлы не образуют exact release, пока не интегрированы в один clean committed tree и не пройдены его bound tests/review. Старый `docs/local-verification-result.md` фиксирует K4R `BLOCKED-LOCAL`; более поздняя установка Docker Desktop устранила часть host prerequisites, но не создала требуемое contained-Linux evidence и не превращает dirty worktree в candidate.

## Gap matrix до полного финала

| Acceptance area | Уже доставлено | Отсутствует до PASS |
|---|---|---|
| VPS core | Compose, PG schema, release/rollback design | Свежий authenticated VPS rebaseline; exact committed candidate; internal deploy; health/resource/reboot persistence evidence. Текущий свежий rebaseline заблокирован локально закрытым SSH key/agent, см. [[VPS_Rebaseline_2026-08-27]]. |
| Caddy/TLS | Caddyfile с отдельными editor/webhook vhosts и exact POST route | Реальные domains/DNS/ACME email, pinned Caddy digest, config validation, provider firewall/IPv6 policy, TLS issuance, editor protection и external route/port scans. |
| Telegram webhook | Route/spec/contracts; локальный polling bridge проверил allowlist/cap/idempotency patterns | Production Webhook workflow JSON, header-auth credential binding, `secret_token`, `setWebhook`, production bot separation, negative tests до DB/LLM/tools и delivery uncertainty evidence. Local polling bridge не переносится в production как замена webhook. |
| DeepSeek | Base URL/model placeholders, response schema и compatibility spec | Server-side credential, актуальный exact model choice, native node spike для thinking/tools, два последовательных tool calls, timeout/malformed/result tests и tested deterministic fallback при необходимости. |
| Пять Tools | Пять least-privilege SQL functions, payload/response schemas и workflow specs | Пять импортируемых n8n sub-workflow JSON, credential bindings, parameterized calls, idempotency/audit E2E и публикация до main workflow. |
| Memory | Separate role/schema/table и session-key design | Exact memory node import/DDL compatibility, persistence/restart, two-user/two-chat isolation и retention cleanup. |
| Reminders | Table, create/list API и dispatcher specification | Dispatcher workflow, bounded schedule, concurrent claim, retry/backoff/dead-letter/uncertain-send tests и owner-visible operations. |
| Backup/restore | Encrypted/signed/off-host scripts, systemd units и isolated-restore design; local logical PG restore smoke | Production age/minisign/rclone custody, immutable remote policy, helper digest, scheduled run, failure notification, tamper negative, authenticated isolated restore, data/credential recovery evidence и RPO/RTO. |
| Monitoring | Container healthchecks и ручной daily checklist | Автоматические redacted checks для service health, capacity, certs, DB, dead letters, backup age/status; thresholds; alert destination; tested alert failure/recovery; runbook linkage. |
| Final handover | Architecture, threat model, runbooks, verification matrix | Executed evidence for every mandatory acceptance criterion, exact inventory/digests, owner/2FA/credentials UI gates, residual-risk signoff. |

## Проверенные уроки local, которые нужно переиспользовать

1. Публиковать только loopback/admin ingress до public-edge; PostgreSQL никогда не получает host port.
2. Секреты передавать через protected file leaves/Docker secrets, не argv/environment/output; после теста real Telegram переводить в `DISARMED`.
3. Реальный egress должен быть отдельным profile/gate; mock должен использовать тот же deterministic core и проверять unauthorized, malformed, duplicate и hard cap.
4. Persistence доказывать полным container recreation без `down -v` и двумя независимыми markers.
5. Restore сначала выполнять в disposable isolated environment, не затрагивая production volumes.
6. Local success нельзя повышать до production success: local workflow отвечает статической фразой, DeepSeek/Caddy/public webhook/off-host DR/monitoring там не проверялись.
7. У локального bridge есть полезный fail-closed паттерн, но его `remember-before-send` оставляет явное окно ambiguous delivery; production workflow должен опираться на DB state/lease/audit design и документировать effectively-once границу.

## Минимальные implementation tracks

### T0 — Source integration и exact candidate

Интегрировать текущие 12 modified + 9 production untracked files без изменения пользовательских данных; обновить stale docs; выполнить static, PostgreSQL, package/governance и contained-Linux matrices; создать один clean exact commit, deterministic package и independent GO. Это prerequisite для любого production deploy.

### T1 — VPS internal foundation

После разблокировки SSH-agent выполнить свежий read-only rebaseline. Затем по exact candidate развернуть только PG+n8n localhost/internal, проверить resource admission, roles/grants, restart/reboot persistence, rollback и owner+2FA. Public edge остаётся выключен.

### T2 — n8n application workflows

В exact n8n 2.36.7 создать/import/re-export пять Tool sub-workflows, memory binding, main Telegram workflow, reminder dispatcher и error handler. Проверить schemas, identity propagation, isolation, idempotency, audit и crash/retry cases в disposable/local среде, затем повторно импортировать в clean target.

### T3 — DeepSeek compatibility

Безопасно привязать credential и провести ограниченный live spike. Зафиксировать native/fallback decision только по evidence; после PASS подключить main workflow и провести разрешённые тестовые вызовы в пределах утверждённого бюджета.

### T4 — Public edge и Telegram webhook

Получить ручные domain/DNS/ACME/provider firewall inputs; pin/validate Caddy; включить editor и exact webhook routes; привязать production bot secret/allowlists; выполнить HTTPS, header-auth, route-negative, IPv4/IPv6 и closed-port tests. Только после этого активировать production workflow/webhook.

### T5 — DR, monitoring и финальная приёмка

Настроить encrypted immutable off-host backup и schedule, выполнить tamper test и isolated restore drill. Реализовать redacted monitoring/alerts и проверить failure delivery. Затем пройти master prompt acceptance matrix целиком и оформить handover. Только после этого допустим `FINAL_STATUS=SUCCESS`.

## Рекомендуемый порядок

`T0 → T1 → T2 → T3 → T4 → T5`. T2 можно разрабатывать локально параллельно с ожиданием ручного SSH unlock для T1, но production activation требует последовательного прохождения всех gates. Следующее рациональное действие в репозитории — T0, не очередной общий план и не новый круг широкого ревью.
