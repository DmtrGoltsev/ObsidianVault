---
id: "n8nagents-plan-v2-reviewer-instructions-draft"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "review-orchestrator"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[План_Лаборатория_Docker_Desktop_N8NAgents_v2_2026-08-27]]", "[[00_FINDINGS_BASELINE]]"]
доказательства: []
теги: ["plan-v2", "review-instructions", "critical-review", "draft-prefreeze"]
---

# Инструкции независимым reviewer — plan v2

## Нулевая предпосылка

Bundle должен быть frozen, read-only и byte/hash-verified до анализа. Текущий `IntegratedDraft` не раздаётся как frozen bundle. Reviewer ничего не устанавливает, не скачивает, не запускает, не меняет и не обращается к Windows/Docker/project repo/VPS/provider/Telegram/DeepSeek/secrets.

## Общая задача

Дать максимум обоснованной критики plan v2 и его claim `114/114 DESIGN_RESOLVED`. Искать ложный PASS, скрытый fallback, union permissions, неполную трассировку, невозможный acceptance test, отсутствующую evidence authority и owner action, спрятанный destructive/external effect. Не снижать severity ради кворума.

Каждый reviewer:

1. проверяет frozen manifest/anchor/plan hash/bytes и UTF-8/LF policy;
2. читает исходную задачу, infrastructure context, v1 plan/quorum/raw baseline, canonical v2, dispositions, consensus closure, catalogs, source lock, exclusions;
3. проверяет все 114 dispositions на неизменность source hash/severity/blocking и существование section/AT/NC/EV;
4. проверяет `12_CANONICAL_ALIAS_MAP_V2.json`, exact per-finding fixtures/results и `18_CHILD_STATUS_MAPPING_V2.json`, включая required/optional scope semantics;
5. проверяет свою semantic область глубже и cross-domain boundaries целиком;
6. возвращает один JSON по `14_REVIEW_SCHEMA_V2.json` с exact-key maps всех 114 findings, 11 clusters и 15 XD; роль не может пропустить key;
7. quorum validator проверяет batch по `23_QUORUM_SCHEMA_V2.json`: ровно R1–R10, уникальные review IDs/roles, один subject/hash tuple и отсутствие противоречивого GO.

## Десять ролей

| Role | Фокус |
|---|---|
| `R1` | Windows/WSL/control plane, endpoint, feature/UAC/reboot, existing install |
| `R2` | supply chain, licenses, signatures, OCI, SBOM, drift/LKG |
| `R3` | isolation, network, mounts, loopback, privileged/capability blast radius |
| `R4` | Compose, PostgreSQL, n8n lifecycle, migrations, exact-version behavior |
| `R5` | Telegram/DeepSeek arming, polling, identity, offset/outbox/caps/errors |
| `R6` | secrets, PII, logs, evidence sinks, at-rest and incidents |
| `R7` | data inventory, encrypted backup, key separation, cold restore/faults |
| `R8` | B2r/O5, 66/34/8, validators, no-network, false-PASS/evidence |
| `R9` | dirty worktree, private authoring, path/TOCTOU, Git/package/rollback |
| `R10` | resources, owner CLI, manual gates, emergency, black-box handoff |

Reviewer не видит другие outputs до сдачи. Cross-domain integration closure проверяется всеми, но findings не объединяются до завершения десяти независимых records.

## Verdict/severity

- `P0`: data/secret/host compromise, unauthorized external/destructive action, fundamental unsafe architecture.
- `P1`: safe/reproducible execution или обязательный outcome недоказуем.
- `P2`: material quality/operations risk with feasible mitigation.
- `P3`: clarity/efficiency only.

Verdict: `GO`, `CHANGES_REQUIRED`, `STOP`, `BLOCKED`. Любой validated P0 blocks. Consensus P0/P1 требует минимум два независимых релевантных reviewer или authoritative primary source. GO threshold будущего кворума: минимум `8/10 GO`, `0 STOP`, `0 P0`, `0 consensus-P1`; bundle-caused BLOCKED требует refreeze и повтор всех десяти reviews.

## Обязательные атаки

- подмена Docker endpoint/context/daemon или control principal;
- unsupported/unknown Windows state, hidden UAC/reboot/update/rollback;
- stale/floating supply identity, revocation/license/SBOM gaps;
- resource peak, VHDX/host reserve, ACL/reparse/TOCTOU/remnants;
- default/mixed Compose topology, extra route/port/mount/service;
- mock/gate egress и real destination bypass/DNS rebind;
- bridge DB path, envelope forgery/replay, route/cap/offset split authority;
- mock должен использовать exact real bridge binary; mock endpoint/key/identity не может войти в real lock;
- prearm/active-arm ordering, production bot, 21st message, stale/reboot arm;
- DeepSeek reserve-before-request, concurrency/retry/ambiguous-consumed reconciliation, price/currency/caps и dedicated API-key consumer;
- non-TLS-terminating broker проверяет destination/SNI/DNS/IP/port, а narrow client — method/path/body/redirect; отсутствие TLS interception;
- secret consumer/transport confusion, evidence/log/support leak;
- backup writer drift/plaintext/wrong key/live root/source reachability и forged/leaking `backup-verifier` result;
- candidate/row/runner/validator/collector/commit/package identity drift;
- false OFFLINE PASS for privileged O5 row;
- owner CLI cwd/PATH/global-context dependence and emergency false success.

## Output rules

Raw secret, VPS address/fingerprint, Windows account identity and raw Telegram tuple are forbidden. Finding must include exact affected section, claim, evidence from frozen bytes, impact, required resolution, acceptance test, blocking and confidence. `disposition_assessments` contains all 114 IDs; `new_findings` contains only newly found issues. Reviewer must report design conflict count honestly and must not claim runtime verification.

`GO` валиден только если все 114 disposition, 11 cluster и 15 XD exact-key values равны `ADEQUATE`, все 13 prospective-audit assessments одновременно равны `closure=CLOSED` и `assessment=ADEQUATE` с exact `baseline_item_sha256`, blocking new findings = 0, `new_findings=[]`, unresolved design conflicts = 0 и subject identity совпадает manifest. Любое иное сочетание с `verdict=GO` является schema/quorum contradiction и само даёт STOP-result-invalid. C1 остаётся permanent loss incident, C2 остаётся prospective successor, №19 не является audit source, а supersession до отдельного owner gate имеет только `PENDING_OWNER_SUPERSESSION`.
