CHANGES_REQUIRED

Итог независимого pre-freeze аудита: `P0=0`; исправление пока нельзя замораживать. Обнаружены `4` release-blocking группы дефектов, затрагивающие `6` прежних P1 и `1` прежний P2.

## Per-ID assessment

| ID | Оценка | Основание |
|---|---|---|
| P1-01 | INADEQUATE | Exact-set формально присутствует, но семантика остаётся шаблонной: `114/129` AT используют один общий четырёхшаговый procedure, `71/129` NC используют значения `VALID:<field> → INVALID:<id>`, evidence почти полностью boilerplate. Нормативный `EV-V3-ACL` из domain draft ошибочно помечен `REJECTED_TEMPLATE_PLACEHOLDER` в `12_CANONICAL_ALIAS_MAP_V2.json` (`alias_id EV-V3-ACL`). |
| P1-02 | INADEQUATE | `23_QUORUM_SCHEMA_V2.json` не обеспечивает cross-record invariants: uniqueness/equality/count rules находятся только в `x-quorum-validator-rules`. Реальный schema engine принял duplicate review ID, duplicate record hash, несовпадающие manifest/subject hashes и противоречивый STOP при заявленном `10 GO / 0 STOP`. Checkers проверяют только встроенный synthetic sample, а не произвольный batch. |
| P1-03 | ADEQUATE | `V06-C05`, `V05-C03`, `V07-C02`, `V10-C01/C02`: durable reserve-before-request, request/USD caps, concurrency, retry reuse, `AMBIGUOUS_CONSUMED`, reconciliation, отдельный DeepSeek key consumer и owner CLI определены. Runtime остаётся `NOT_RUN`. |
| P1-04 | INADEQUATE | Разделение ответственности broker/client в `V04-C05` сформулировано корректно, но связанный `NC-XD-08` мутирует только `egress.destination_sni`. В каталоге нет ни одного отдельного canary для client-side HTTP method/path/body/redirect, хотя план требует именно split acceptance. |
| P1-05 | INADEQUATE | Невыполнимая MOCK-топология: `V04-C04` разрешает в `mock_tg` только `n8n` и `mock-telegram`, тогда как `V04-C06` требует, чтобы тот же `telegram-bridge` обращался к `mock-telegram` через эту сеть. `telegram-bridge` в `mock_tg` не допускается. `NC-F-R5-F14` также не проверяет identity exact bridge binary/entrypoint и contamination real lock. |
| P1-06 | INADEQUATE | `18_CHILD_STATUS_MAPPING_V2.json` содержит прямой false GO: `V04:V4_STOP_UNVERIFIED → PASS / G_PASS_EXACT_REQUESTED_SCOPES / RC0`, хотя источник требует nonzero и запрещает утверждать остановку egress. Другие ошибки: `V07:INCIDENT_CLOSED → G_INCIDENT_OPEN/54`; `V08_FAIL_AUTH/BACKUP/PLAINTEXT/RESTORE → BLOCKED_UNKNOWN/30`; read-only PASS получает `mutation_started=true`. |
| P1-07 | INADEQUATE | Текущая цепочка из 39 inputs и её hashes верны, но оба validator source не загружают и не проверяют `13_PRIMARY_SOURCE_LOCK.md`, `17_INTEGRATION_DRAFT_MANIFEST.json` или `22_CHECKER_RUN_RECORD.json`; не пересчитывают content set/envelope и фактический plan SHA. Они могут PASS при изменении непроверяемых байтов/manifest/input chain. |
| P1-08 | ADEQUATE | `V10-C01/C02/C04` содержит стабильный launcher, masked stdin, secret set/status/rotate/revoke, dev/prod fingerprint binding, tuple/webhook ceremonies, Telegram two-phase arm, DeepSeek key/arm/reconcile и black-box handoff. |
| P2-01 | INADEQUATE | `V08-C04` хорошо определяет verifier/key isolation, но `backup-verifier` отсутствует в закрытом canonical service list `V04-C03`, где undeclared service запрещён. Следовательно, verifier нельзя легально включить в exact Compose topology. |

## Новые конкретные findings

- `NEW-P1-01 — false-GO quorum`: опубликованная schema принимает пять проверенных противоречивых quorum-вариантов.
- `NEW-P1-02 — unsafe normalization`: `V4_STOP_UNVERIFIED` нормализуется в RC `0`, что может скрыть продолжающийся внешний трафик.
- `NEW-P1-03 — impossible exact topology`: MOCK bridge и backup verifier противоречат закрытым membership/service manifests.
- `NEW-P1-04 — validators not subject-bound`: два заявленных hash-bound checker фактически не проверяют manifest/input/content/envelope chain.

## Проверенные положительные факты

- Plan: `57133` bytes, SHA-256 `91ba3acd07ab0eb87f3ea42d788eb0c6b581734ae14235a75706a011f8f0b672`.
- Manifest: `12184` bytes, SHA-256 `883f7c8901c43329c0f37b8a7923a91afbf13471377326bcfc73ef648809cc9e`.
- Correction №19: `4583` bytes, SHA-256 `e62873c3be5a887e7dabfcb531cff1fca5dd5d8f52c5a5efd1a39e1a887a5591`.
- Manifest aggregate: `71298dbb9f031743b2ac7d3a0a06acd0cbd5149a657b5f8db208311d8fccd12e`.
- Input chain: `39`, aggregate `2a39969856847fd2558c5651a5b141eb57b48967898bb1d71613df0728a1c840`.
- Content set: `12`, SHA-256 `7cbab1c8de24bad08d0eb0c492629522ca1c04cd28ac8a25cee852dd5515f1d5`.
- Envelope: `5`, SHA-256 `74067913446bbcc1092e457d018ec83989d53e0cf5331ffdbb447cc4bc3e96cc`.
- Counts: `114 = P0:1/P1:83/P2:28/P3:2`; blocking `84`, nonblocking `30`; dispositions `114`; AT/NC/EV `129/129/129`; aliases `601`; statuses `306`; operations `11`; clusters `11`; XD `15`; conflicts `20/20`.
- Оба supplied checker воспроизвели PASS и отклонили по `23` своих mutation canary.
- Дополнительно выполнено `12` независимых in-memory canary: все mutations отклонены.
- A-only, no fallback, two-phase Telegram arm, no-DB bridge, DeepSeek ledger, privacy и отсутствие runtime PASS claims сформулированы корректно.
- Временных файлов не осталось; три контрольных файла после аудита имеют исходные hashes.

## Exact acceptance resolution

1. Добавить standalone hash-bound quorum validator для фактического batch: schema-validation каждого record, recomputed record hashes, exact roles, unique IDs/hashes, subject/manifest equality, пересчитанные counters и GO semantics. Прогнать invalid batches через него, не через synthetic sample.
2. Пересобрать все 306 status mappings по семантике источников; отдельно исправить перечисленные false mappings и ввести phase-aware `mutation_started`, если status сам по себе недостаточен.
3. Добавить `telegram-bridge` в exact MOCK route/membership и `backup-verifier` в canonical one-shot services; проверить rendered topology exact-set tests.
4. Заменить placeholder AT/NC fixtures реальными typed fixtures; исправить `EV-V3-ACL`; добавить canaries для client HTTP policy, exact bridge binary/real-lock contamination, полной input/manifest/checker custody и verifier identity/key isolation.
5. Обязать оба checker пересчитывать plan/input/manifest/content/envelope hashes, encoding и transcript binding.
6. После исправлений пересобрать manifest и повторить pre-freeze audit.
