APPROVE_SUPERSESSION

Архитектурное решение допустимо как явная перспективная смена authoritative regression baseline. Оно не восстанавливает и не заменяет исторический факт первого аудита: original R1 raw остаётся безвозвратно утраченным. Supersession заменяет только будущий gate-контракт frozen 10-review bundle.

Это не `GO` и не разрешение на freeze: R2 raw имеет `CHANGES_REQUIRED`, 7 из 9 legacy assessments — `INADEQUATE`, плюс 4 новых blocking P1.

Обязательные controls:

1. Создать detached supersession decision, связывающий exact identities:

   - C1 loss incident: `1312` bytes, SHA-256 `52765124ad0e60f6142b24521228b4562bfca3c30bba52a488a0ade43d473f06`.
   - C2 R2 raw: `7957` bytes, SHA-256 `2c6f25a2ab02e7d9995df0ecbc4456f69dfadd0c044f403c0420ea23e13295ae`.
   - C2 attestation: `1124` bytes, SHA-256 `3a5d8d3bcb49a613c39a8695f1b94e5f4e61d45bfc77bae31526ec42c1b4b101`.
   - Точный hash обновлённого A/B specs, review schema и supersession approvals.

   Сейчас C1 называет candidate, но не содержит его bytes/hash, а attestation не связывает C1. Без detached record это provenance gap.

2. Новый record нельзя называть `ORIGINAL_LEGACY_AUDIT_R1` или `ORIGINAL_AUDITOR_OUTPUT`. Требуются отдельные значения вроде:

   - `record_kind=N8NAGENTS_AUTHORITATIVE_REGRESSION_BASELINE_R2`;
   - `source_kind=SECOND_PREFREEZE_AUDIT_R2`;
   - `source_mode=APPROVED_SUPERSESSION`;
   - `original_r1_recovered=false`.

3. Baseline должен иметь exact set из 13 ключей:

   - `P1-01..P1-08,P2-01`;
   - `NEW-P1-01..NEW-P1-04`.

   Для каждого — exact byte span в C2 raw, span SHA-256 и domain-separated `baseline_item_sha256`. Нормативно хешировать, например:

   `SHA256("N8NAGENTS-R2-BASELINE-ITEM-V1\0" || FRAME(id) || U64BE(offset) || U64BE(bytes) || SHA256_RAW(span))`.

   Затем нужен ordered aggregate всех 13 items. Любые производные mapping или пояснения не должны подменять exact source text.

4. Review schema следует изменить с `114/11/15/9` на две явно разделённые карты `9 + 4`, либо exact `13`. Каждый assessment обязан содержать const `baseline_item_sha256`, `closure`, `assessment`, forward/reverse-bound section/AT/NC/EV references и rationale. `GO` возможен только если все 13 имеют `CLOSED + ADEQUATE`. Новые четыре findings нельзя дедуплицировать с перекрывающимися legacy rows.

5. B-spec должен быть нормативно изменён и перехеширован. Текущий B, SHA-256 `350171ffb6727330cb2d218d256f51a5fb568dfa95b605a922411f0478bba2e7`, прямо требует original raw и прекращает freeze при его отсутствии: строки 26, 49–50, 65, 83–85, 524 и 537. До явной замены этих правил supersession не действует.

6. Correction №19, `4583` bytes / SHA-256 `e62873c3be5a887e7dabfcb531cff1fca5dd5d8f52c5a5efd1a39e1a887a5591`, оставить только как `HISTORICAL_NON_AUTHORITATIVE/CROSS_REFERENCE_ONLY`. В нём есть titles и mappings, но нет original claim/evidence/impact/resolution. Validator обязан отвергать bundle, где №19 используется как source любого baseline item.

7. R2 audited-subject identity необходимо сохранить отдельно: как минимум exact old plan, manifest `883f7c…cc9e`, correction №19 и old manifest/input-chain index. C2 raw уже связывает plan/manifest/content/envelope на строках 28–34; frozen bundle должен позволять проверить эти значения, а не доверять Markdown как произвольным 64-hex.

8. Attestation создана тем же author task и использует неуникальный locator `immediately preceding...`. Нужен stable turn/message/transcript locator и независимый capture hash. Если технически недоступно, provenance следует честно понизить до `AUTHOR_ATTESTED_CAPTURE`, а owner и supersession quorum должны явно принять этот residual limitation; нельзя утверждать `independently verified transcript`.

9. Supersession должен вступать в силу только после owner approval и `3/3` независимых `APPROVE_SUPERSESSION`, с уникальными reviewer IDs/raw hashes и без участия `/root/v2_prefreeze_audit`. До этого точный статус — `STOP_SUPERSESSION_NOT_APPROVED`.

10. Два независимых validators должны отвергать nonzero-классами: изменение C1/C2/attestation/decision; missing/extra/swapped один из 13 IDs; неверный span/hash; подстановку №19; relabel R2 как original; subject mismatch; missing approval; и `GO` при одном `OPEN/INADEQUATE/UNVERIFIABLE`. Рекомендуемые классы: `STOP_SUPERSESSION_HASH_MISMATCH`, `STOP_BASELINE_SOURCE_MISMATCH`, `STOP_BASELINE_SET_MISMATCH`, `STOP_BASELINE_ITEM_MISMATCH`, `STOP_CONTRADICTORY_GO`.

Проверено read-only: C1, C2 raw и attestation имеют valid UTF-8, без BOM/CR/NUL, LF и ровно один final LF; заявленный C2 hash совпадает. A-spec identity: `78558` bytes, SHA-256 `27f4b1f56384fb41db54394decad52d38da123aef7cf7c00e85103a96d0e7008`.

Итоговая граница: supersession безопасно заменяет невозможное future gating requirement, но никогда не должна выглядеть как восстановление original R1 provenance.
