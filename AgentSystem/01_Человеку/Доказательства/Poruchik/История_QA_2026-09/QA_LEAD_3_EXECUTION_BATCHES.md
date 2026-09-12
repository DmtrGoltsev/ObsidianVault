# Пакеты исполнения каталога QA-лида 3

Дата подготовки: 2026-09-09. Источник кейсов: `QA_LEAD_3_EMULATOR_CASES.md`. Документ не разрешает production-мутации: пакеты `P-*` остаются `HOLD` до принятия объединённого плана QA-лидом 1. Физический телефон исключён.

## Правила запуска

- Пакеты одной строки «параллельно» запускаются одновременно. Внутри одной session family, task/version, client cursor, conversation, push registration и Telegram pending action шаги последовательны.
- Для production создаётся новый workspace и новый журнал UUID. Файлы session/key/invite старых `.e2e/runs/*` не переиспользуются. Они могут служить только образцом формата.
- Скрипты `.e2e/doc-live-canary.sh` и SQL-файлы с прямыми `INSERT` годятся только для локальной disposable PostgreSQL: они не являются официальным продуктовым E2E.
- `.e2e/decision-lock-live-canary.py`, `run-decision-sequential.ps1`, `run-agent-history.ps1`, auth/push cycles можно использовать только после параметризации под новый workspace/session/ledger. Hard-coded UUID и consumed credentials запрещены.
- Внешние Telegram и реальные FCM sends сериализуются. Общие restart/deploy/migration закрывают окно всех production-пакетов.

## Локальные пакеты, доступные сразу

| Пакет | Case IDs | Команда из корня | Оракул | Параллельность/ресурс |
|---|---|---|---|---|
| L-CONTRACT | ENV-03–06, AUTH-04/21–22, TASK-02/04–05/08/11, SYNC-11/16–17, DOC-03/14, AG-11/15, EDGE-01/09 | `python scripts/verify_contracts.py` | 34 tests, exit 0; OpenAPI refs/routes/state/offline/service roles согласованы | параллельно со всеми L-* |
| L-GATEWAY | NET-02–09, AUTH-03/08–17/21–23 | `cd server/gateway; go test ./...` | все packages PASS; canonical 404, route allowlist, auth/refresh/replay/rate/proxy/header/unregister | отдельный Go cache; параллельно |
| L-TASKCORE | TASK-01–28, DOC-01–10/15, AG-05–10, PUSH-01–03/14–19, EDGE-04/06–08, OPS-01 | `cd server/task-core; mvn test` | disposable PostgreSQL, все тесты PASS/0 skipped; версии, ACL, races, docs, run queue, push side effects | один Testcontainers/PG набор; параллельно с Android/N8N |
| L-ANDROID | AUTH-02/05–07/24, SYNC-01–05/09–15/18–20, FOCUS-01–04, CAL-01, INBOX-01–04, DOC-11–13, AG-03/16–18, PUSH-03–13/20, UI-01–18, EDGE-02/03/10 | `.\gradlew.bat test testQa lintRelease assembleRelease` | Gradle success; все unit/QA tests PASS, lint 0 fatal, release APK собран | общий Gradle cache; один процесс, параллельно с server |
| L-ANDROID-INSTR | AG-16–17, UI-01/03/11–12/15–17 | `.\gradlew.bat connectedAndroidTest` на выделенном AVD | instrumentation PASS; voice availability может стать честным environment blocker | один AVD на invocation; другие AVD-пакеты параллельны |
| L-BRIDGE | AG-11–15, TOOL-06–18, AUTH-21–22 | `cd integrations/agent-bridge; python -m unittest discover -s tests -p test_bridge.py` | 19 tests PASS; 13 typed intents, HMAC, identity, idempotency, false-success guard | параллельно |
| L-PLUGIN | TOOL-01–18, AG-11–15, TG-07–11/13–14 | `cd N8NAgents/openclaw/plugin; npm test` | plugin tests PASS; 18 tools, trusted context, turn guard, callbacks applied-once | параллельно |
| L-N8N-STATIC | SCH-05/12–14/16, OPS-02–03 | `pwsh -NoProfile -File N8NAgents/local/tests/run-static.ps1` и `python N8NAgents/scripts/test-scheduler-artifacts.py` | terminal PASS; workflow/schema/source hygiene без secrets | параллельно с L-POSTGRES |
| L-POSTGRES | TOOL-01–05, TG-09/12–14, SCH-01–16, OPS-01–02 | `pwsh -NoProfile -File N8NAgents/scripts/verify-postgres.ps1` | disposable migrations 001–011, grants/constraints/idempotency PASS, volumes удалены | один Docker Compose project с уникальным именем |
| L-RELEASE | ENV-01–02, OPS-03/06 | Poruchik: `python scripts/verify_ssh_release.py`; N8NAgents: `pwsh -NoProfile -File scripts/verify-static.ps1` | release governance/source hygiene/packaging terminal PASS | после основных L-*; читает рабочее дерево |

Фактическая проверка подготовки: `L-CONTRACT` — PASS 34/34; `L-PLUGIN` — PASS 20/20; `L-BRIDGE` — PASS 19/19. `L-GATEWAY` в текущем Windows shell не запущен: executable `go` отсутствует в `PATH`; это блокер среды, а не дефект продукта. Следующая содержательная попытка допустима после предоставления Go runtime или в штатном build container.

Read-only production baseline на момент подготовки: `/health/live` HTTP 200 и `/health/ready` HTTP 200. Ответы не содержали доменных данных, авторизованные запросы не выполнялись.

## Read-only production baseline

| Пакет | Case IDs | Команда/действие | Оракул | Мутации |
|---|---|---|---|---|
| R-HEALTH | NET-01/10, OPS-04 | один GET public live/ready; read-only container health/image/restart/schema/plugin/workflow fingerprint | 200; expected immutable digests; restart0; current Flyway/plugin | нет |
| R-COUNTS | ENV-01, OPS-08 | scoped/global counts только метаданных: workspaces/principals/devices/sessions/tasks/runs/outbox/deliveries/reminders | baseline сохранён в новом ledger; human content/tokens не читаются | нет |
| R-HELD | SYNC-08–10 | только metadata существующей 409 fixture: task/version/conflict operation | task остаётся v2, conflict operation неизменна до APK gate | нет |
| R-RUNTIME | AG-01/07–10, SCH-16 | read-only health и recent scoped status без payload | Gateway/TaskCore/relay/OpenClaw/n8n healthy, нет активного тестового run в новом scope | нет |

## Production-пакеты после объединённого gate

| Пакет | Case IDs | Существующий образец harness | Новый изолированный scope | Оракул завершения | Зависимость |
|---|---|---|---|---|---|
| P-AUTH-A | AUTH-01–14, EDGE-01 | `provision-mvp0-tools.ps1`, `redeem-mvp0-invite.ps1`, auth-cycle scripts | `AUTH-A-*`, OWNER device/session family | invite once; challenge/rotation/replay/logout exact counts | L-GATEWAY, R-HEALTH |
| P-AUTH-B | AUTH-15–23 | device/link/push-registration cycle scripts | `AUTH-B-*`, MEMBER + second device, no FCM event | scoped revoke/unregister/link/HMAC/ACL, чужие rows unchanged | P-AUTH-A |
| P-CORE-A | TASK-01–13, FOCUS-01–04, CAL-01–03, INBOX-01–03 | request helper из `run-decision-sequential.ps1` | `CORE-A-*`, independent task branches | response/resource/version/audit/outbox; negatives delta0 | P-AUTH-A |
| P-CORE-B | TASK-14–28, INBOX-04, EDGE-04 | `run-decision-sequential.ps1`, `decision-lock-live-canary.py` после параметризации | `CORE-B-*`, OWNER+MEMBER, separate proposals/approvals/assignments | sequential + races: один 200/один typed409, one terminal/side effect | P-AUTH-B, L-TASKCORE |
| P-DOC | DOC-01–15 | product request helper; прямой SQL canary запрещён | `DOC-*`, task/tree/selected roots | valid tree/order/hash/ACL; invalid path/checksum/cycle delta0 | P-CORE-B |
| P-SYNC-A | SYNC-06–08/11–13/16–17 | signed mobile API harness с новым clientId | `SYNC-A-*`, без UI | HTTP200 embedded outcomes, cursor/order/replay/conflict exact | P-AUTH-A, L-ANDROID |
| P-AVD-SYNC | SYNC-01–05/09–10/14–15/18–20, UI-01–18 | UIAutomator/semantic bounds + QA diagnostics APK | `SYNC-E-*`, отдельный AVD snapshot/clientId | Room/outbox/UI/server сходятся; no duplicate/remap/lost draft | P-SYNC-A, APK-CONFLICT |
| P-AGENT-READ | AG-01–05/18, TOOL-08/11/13/14/15 | Android `/v1/agent/commands/text` и official run history | `AGENT-R-*`, отдельные conversations | read-only tool invocation каждого имени, result vs API, domain delta0 | runtime healthy |
| P-AGENT-WRITE | TOOL-06/07/09/10/12/16/17/18, INT-01/03 | official Android agent path; action-executor audit | `AGENT-W-*`, отдельная task branch на tool | 8 mutation tools: exact resource/version/audit/outbox, no inferred success | P-CORE-B, P-AGENT-READ |
| P-RUN | AG-06–10, EDGE-06/08 | `run-agent-history.ps1`, create-failed/cancelled scripts после параметризации | `RUN-*`, no push registration | pagination/redaction; success/fail/retry/cancel terminal exactly once | runtime healthy |
| P-PUSH | PUSH-01–20, INT-02/03 | push unregister cycle + new event observer | `PUSH-*`, только QA registrations | one event→one outbox/delivery; neutral payload; token lifecycle; no DLQ replay | P-AUTH-B; реальные events строго serial |
| P-TG | TOOL-01–05, TG-01–14 | только обычный trusted chat UI, не внутренний callback | unique marker в существующем owner chat | 5 tools, ≤8 bot messages, 3 genuine taps, task cancelled, baseline unchanged | все runtime gates; строго serial |
| P-SCHED | SCH-01–16 | signed scheduler webhook + DB metadata oracle; fake provider для failures | `SCHED-*`, isolated reminder policy кроме P-TG | leases/quiet/digest/retry/uncertain/DLQ/cadence exact | L-POSTGRES; live sends исключены кроме P-TG |
| P-CLEAN | OPS-08 | новый ledger + адаптированный guarded cleanup | каждый созданный workspace | per-table residual0, global baseline unchanged | после принятия evidence каждой группы |

## Порядок параллельного запуска

1. Одновременно: все `L-*`, затем `R-*` read-only. `L-TASKCORE` и `L-POSTGRES` получают разные Docker project/volume names.
2. После gate одновременно: `P-AUTH-A`, `P-AUTH-B` только после его owner chain; затем независимые `P-CORE-A`, `P-SYNC-A`, `P-AGENT-READ`, `P-RUN` в разных workspaces.
3. После их локальных зависимостей одновременно: `P-CORE-B`, `P-DOC`, `P-AVD-SYNC`, `P-AGENT-WRITE`. Shared task/version chains не пересекаются.
4. `P-PUSH` сериализует provider events, но может идти параллельно с `P-DOC` и `P-RUN` в отдельном workspace. `P-SCHED` с fake provider параллелен всем; `P-TG` один и строго последователен.
5. `P-CLEAN` запускается отдельным writer по завершённым workspace. Очистка одного scope может идти параллельно с тестами другого scope, если нет общего principal/device/chat/policy.

## Пробелы harness перед production gate

- Нет единого параметрического runner всех 18 tool names. До production достаточно тонкой таблицы команд над официальными Android/Telegram путями; отдельная новая инфраструктура не нужна. Runner обязан падать, если модель пропустила требуемый tool или отсутствует audit/resource oracle.
- Старые `.e2e` scripts привязаны к завершённым UUID/session files. Нужна механическая параметризация нового run directory; перенос ключей/токенов в вывод запрещён.
- AVD UI execution требует устойчивого semantic/UIAutomator пути. Координатные taps без проверки bounds не считаются действием.
- Реальный Telegram callback и provider FCM нельзя закрыть локальным API вызовом. Они остаются отдельными сериализованными внешними шагами.
