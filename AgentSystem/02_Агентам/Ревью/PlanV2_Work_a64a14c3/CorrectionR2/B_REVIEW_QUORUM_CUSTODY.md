---
id: "n8nagents-plan-v2-correction-r2-review-quorum-custody-spec"
тип: "спецификация"
статус: "черновик"
проект: "AgentSystem"
владелец: "review-custody-specialist-b"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[17_INTEGRATION_DRAFT_MANIFEST]]", "[[19_PREFREEZE_CORRECTION_R1]]", "[[15_REVIEWER_INSTRUCTIONS_V2]]"]
доказательства: []
теги: ["plan-v2", "correction-r2", "review", "quorum", "custody", "draft-only"]
---

# Correction R2/B — exact review, quorum and custody implementation spec

## 1. Назначение и границы

Этот документ задаёт исправление custody-контура перед freeze и повторным независимым ревью plan v2. Он является только implementation spec: не меняет canonical plan, `IntegratedDraft`, domain sources, project repository, Windows, Docker или runtime и не доказывает ни одного runtime outcome.

Нормативные инварианты:

1. Единственная архитектура — plan A: локальный Docker Desktop, production target остаётся `linux/amd64`.
2. `OFFLINE_BLOCKED_CAPABILITY` для отдельно запрошенной обязательной O5-row не превращается в `OFFLINE_READY`, но сам по себе не блокирует независимые `LAB_READY` и `LOCAL_STACK_READY`.
3. Reviewer анализирует один и тот же immutable subject и не видит outputs других reviewer до сдачи собственного raw record.
4. Нельзя синтезировать исходный legacy-аудит из correction summary. Нет исходного claim/evidence — `STOP_LEGACY_SOURCE_MISSING`.
5. Любой hash вычисляется по байтам, а не по повторно сериализованному объекту, если ниже явно не задан framed canonical payload.
6. Ни один файл не содержит обязательный SHA-256 собственных полных байтов.
7. Все claims `schema_valid`, `go_semantics_valid`, counters и aggregate verdict вычисляет trusted collector/validator; reviewer или интегратор не являются источником истины для этих полей.

Зафиксированные входные identity текущей correction base:

| Объект | Bytes | SHA-256 |
|---|---:|---|
| canonical plan v2 | `57133` | `91ba3acd07ab0eb87f3ea42d788eb0c6b581734ae14235a75706a011f8f0b672` |
| correction-base manifest | `12184` | `883f7c8901c43329c0f37b8a7923a91afbf13471377326bcfc73ef648809cc9e` |
| correction R1 record | `4583` | `e62873c3be5a887e7dabfcb531cff1fca5dd5d8f52c5a5efd1a39e1a887a5591` |
| normalized V9 source | `64893` | `c2a40596e6010b7e691bf187d2bd978b3da15bd2bc40a0dbf64c460ae7774536` |
| owner-designated master prompt | `27410` | `7b271daf6c3952aff905d2358e2e1a3c36ca789e5be784968311e133d1758da3` |

Любое отличие master prompt от `27410 / 7b271d…8da3` до capture — не автоматическое обновление input, а `STOP_MASTER_PROMPT_IDENTITY_CHANGED` и новый owner-visible input decision.

## 2. R2 artifact set и порядок построения

Freeze-builder обязан создать в новой staging-копии, не поверх текущего `IntegratedDraft`, следующие logical artifacts:

| Logical ID | Рекомендуемый файл | Роль |
|---|---|---|
| `LEGACY-RAW-1` | `Inputs/ORIGINAL_PREFREEZE_AUDITOR_OUTPUT.md` | exact-byte capture исходного auditor output/transcript |
| `LEGACY-ORIGINAL-1` | `24_ORIGINAL_LEGACY_AUDIT_R1.json` | самостоятельная immutable capture исходного аудита `P1-01..P1-08/P2-01` |
| `MASTER-PROMPT-1` | `Inputs/N8N_AGENT_MASTER_PROMPT.md` | exact-byte copy owner-designated master prompt |
| `REVIEW-SCHEMA-2` | `14_REVIEW_SCHEMA_V2.json` | exact 114/11/15/9 raw-review schema |
| `QUORUM-SCHEMA-2` | `23_QUORUM_SCHEMA_V2.json` | aggregate output schema; не validator authority |
| `CUSTODY-A` | `20_PREFREEZE_CHECKER_NODE.mjs` | независимый Node custody validator |
| `CUSTODY-B` | `21_PREFREEZE_CHECKER_PYTHON.py` | независимый Python custody validator |
| `BATCH-A` | `25_RAW_REVIEW_BATCH_VALIDATOR_NODE.mjs` | raw R1–R10/quorum validator A |
| `BATCH-B` | `26_RAW_REVIEW_BATCH_VALIDATOR_PYTHON.py` | raw R1–R10/quorum validator B |
| `PATH-COLLECTOR-A` | `28_WINDOWS_PATH_CUSTODY_COLLECTOR.ps1` | pinned Node-A-only Win32 path/stream/reparse collector; Python B его не использует |
| `PREFREEZE-RUNS` | `27_PREFREEZE_CUSTODY_RUN_RECORD.json` | exact source/command/runtime/stdout/stderr/mutation transcript index |
| `FINAL-MANIFEST` | `00_FROZEN_MANIFEST.json` | final entry list and subject construction; собственные bytes исключены |
| `ANCHOR` | `BUNDLE_ANCHOR.txt` | detached final manifest/validation identities; не входит в manifest |

Порядок обязателен:

1. capture original legacy audit и master prompt;
2. сформировать content artifacts и exact source/input chain;
3. вычислить `content_set_sha256`;
4. сгенерировать review/quorum schemas с content constants;
5. зафиксировать validator sources;
6. вычислить `subject_envelope_sha256`;
7. выполнить prefreeze positive/mutation runs, записать `27_*`;
8. сформировать final manifest последним и вычислить его внешний SHA-256;
9. выполнить final custody validation на immutable staging tree;
10. сформировать detached transcript index и `BUNDLE_ANCHOR.txt`;
11. только после совпадения A/B разрешить state `FROZEN_FOR_REREVIEW`.

Никакой partial publish. Ошибка на любом шаге удаляет только незамороженную staging-копию и оставляет предыдущий immutable subject неизменным.

## 3. Самостоятельный ORIGINAL legacy audit record

### 3.1 Запрет реконструкции

`19_PREFREEZE_CORRECTION_R1.json` является remediation record, а не original audit. Новый `24_ORIGINAL_LEGACY_AUDIT_R1.json` создаётся только из исходного auditor output/transcript. Titles из correction R1 допустимы как cross-check, но не как источник `original_claim`, `original_evidence`, `impact` или `required_resolution`.

Если исходный auditor output не имеет устойчивого локатора и exact bytes, freeze прекращается. Нельзя заменять его пересказом агента, памятью модели или поздней редакцией.

### 3.2 Exact top-level shape

```json
{
  "schema_version": 1,
  "record_kind": "N8NAGENTS_ORIGINAL_LEGACY_PREFREEZE_AUDIT",
  "state": "IMMUTABLE_SOURCE_CAPTURE",
  "source_record": {
    "source_kind": "ORIGINAL_AUDITOR_OUTPUT",
    "captured_path": "Inputs/ORIGINAL_PREFREEZE_AUDITOR_OUTPUT.md",
    "source_locator": "<stable non-secret locator>",
    "captured_bytes": 0,
    "captured_sha256": "<64 lower-hex>",
    "capture_encoding": "UTF-8_NO_BOM_LF_ONE_FINAL_LF"
  },
  "subject_at_audit": {
    "plan_bytes": 0,
    "plan_sha256": "<64 lower-hex>",
    "manifest_sha256": "<64 lower-hex or ABSENT_AT_ORIGINAL_AUDIT>"
  },
  "required_ids": ["P1-01", "P1-02", "P1-03", "P1-04", "P1-05", "P1-06", "P1-07", "P1-08", "P2-01"],
  "items": {
    "P1-01": {},
    "P1-02": {},
    "P1-03": {},
    "P1-04": {},
    "P1-05": {},
    "P1-06": {},
    "P1-07": {},
    "P1-08": {},
    "P2-01": {}
  },
  "items_aggregate_sha256": "<framed aggregate>"
}
```

`required_ids` имеет ровно этот порядок. `items` имеет ровно эти ключи, без extra/missing и без duplicate JSON keys. Для каждого key обязателен объект:

```json
{
  "audit_id": "P1-01",
  "severity": "P1",
  "title": "<original title verbatim>",
  "original_claim": "<verbatim claim, no paraphrase>",
  "original_evidence": [
    {
      "source_locator": "<stable locator inside captured source>",
      "excerpt": "<verbatim evidence excerpt>",
      "excerpt_utf8_sha256": "<SHA-256 of exact UTF-8 excerpt bytes>"
    }
  ],
  "impact": "<original impact verbatim>",
  "required_resolution": "<original required resolution verbatim>",
  "affected_subject_locations": ["<original section/path locator>"],
  "source_spans": {
    "claim": {"offset": 0, "bytes": 0, "sha256": "<exact span hash>"},
    "evidence": [{"offset": 0, "bytes": 0, "sha256": "<exact span hash>"}],
    "impact": {"offset": 0, "bytes": 0, "sha256": "<exact span hash>"},
    "required_resolution": {"offset": 0, "bytes": 0, "sha256": "<exact span hash>"}
  },
  "original_claim_sha256": "<framed claim hash>"
}
```

Пустые строки, placeholder, `TBD`, `unknown`, correction-only title и synthesized prose запрещены. `severity` фиксирован: `P1-01..P1-08 => P1`, `P2-01 => P2`. Каждый `source_spans` указывает диапазон exact raw capture; диапазон остаётся внутри файла, SHA-256 span совпадает, а декодированный текст равен соответствующему verbatim полю. Overlap допустим только когда исходный auditor явно использовал один span для нескольких полей; иначе ranges не пересекаются.

### 3.3 Claim hashing

`original_claim_sha256` вычисляется без JSON reserialization:

```text
SHA256(
  UTF8("N8NAGENTS-ORIGINAL-LEGACY-CLAIM-V1\0") ||
  FRAME(audit_id) || FRAME(severity) || FRAME(title) ||
  FRAME(original_claim) ||
  U32BE(original_evidence.length) ||
  for each evidence in listed order:
    FRAME(source_locator) || FRAME(excerpt) || SHA256_RAW(excerpt_utf8_bytes) ||
  FRAME(impact) || FRAME(required_resolution) ||
  U32BE(affected_subject_locations.length) ||
  for each locator in listed order: FRAME(locator)
)
```

`FRAME(text) = U32BE(length(UTF8(text))) || UTF8(text)`. Все строки должны быть valid Unicode scalar sequences, NFC, без CR/NUL. Arrays сохраняют original order и не сортируются. Повторный locator запрещён.

`items_aggregate_sha256`:

```text
SHA256(
  UTF8("N8NAGENTS-ORIGINAL-LEGACY-SET-V1\0") ||
  for audit_id in exact required_ids order:
    FRAME(audit_id) || SHA256_RAW(items[audit_id].original_claim_sha256)
)
```

Raw captured auditor source является отдельной content entry. `24_*` обязан ссылаться на его exact identity; validator повторно извлекает девять records или сравнивает exact source ranges, а не доверяет только записанным claims.

## 4. Master prompt binding

Freeze-builder читает только literal path:

```text
C:\Users\style\Documents\New project\N8N_AGENT_MASTER_PROMPT.md
```

До copy проверяются exact `27410` bytes и SHA-256 `7b271daf6c3952aff905d2358e2e1a3c36ca789e5be784968311e133d1758da3`. Затем exact bytes копируются в staging как `Inputs/N8N_AGENT_MASTER_PROMPT.md`; source и copy должны совпасть byte-for-byte. Copy включается одновременно:

- в exact input-chain;
- в content records;
- в final manifest entries;
- в reviewer input inventory.

После capture reviewers работают с frozen copy, а не с mutable external path. Final validator не требует, чтобы внешний original оставался неизменным; он проверяет frozen copy против зафиксированного owner-approved identity. Raw secrets, если неожиданно обнаружены deterministic secret scanner-ом, дают `STOP_MASTER_PROMPT_SECRET_FOUND`; автоматическая redaction изменяет subject и запрещена.

## 5. Review schema: exact 114/11/15/9

### 5.1 Mandatory maps

`14_REVIEW_SCHEMA_V2.json` сохраняет exact-key objects:

- `disposition_assessments`: exact set 114 baseline finding IDs;
- `cluster_assessments`: exact set `C01,C03,C04,C06,C07,C08,C10,C12,C14,C15,C17`;
- `xd_assessments`: exact set `XD-01..XD-15`;
- `legacy_assessments`: exact set `P1-01..P1-08,P2-01`.

У каждого объекта одновременно:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["<all exact IDs>"],
  "properties": {"<each exact ID>": {"$ref": "#/$defs/assessment"}}
}
```

Сравнивать нужно полные множества IDs, а не только counts. Parser до schema validation отвергает duplicate JSON keys.

### 5.2 Legacy assessment shape

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "audit_id",
    "original_claim_sha256",
    "closure",
    "assessment",
    "plan_section_ids",
    "acceptance_test_ids",
    "negative_canary_ids",
    "evidence_ids",
    "rationale"
  ],
  "properties": {
    "audit_id": {"const": "<map key>"},
    "original_claim_sha256": {"const": "<value from 24_*>"},
    "closure": {"enum": ["CLOSED", "OPEN", "BLOCKED"]},
    "assessment": {"enum": ["ADEQUATE", "INADEQUATE", "UNVERIFIABLE"]},
    "plan_section_ids": {"type": "array", "minItems": 1, "uniqueItems": true},
    "acceptance_test_ids": {"type": "array", "minItems": 1, "uniqueItems": true},
    "negative_canary_ids": {"type": "array", "minItems": 1, "uniqueItems": true},
    "evidence_ids": {"type": "array", "minItems": 1, "uniqueItems": true},
    "rationale": {"type": "string", "minLength": 1}
  }
}
```

Каждый referenced section/AT/NC/EV должен существовать в frozen catalogs и быть reverse-bound к соответствующему legacy audit ID. Наличие строкового ID без reverse binding не является closure.

### 5.3 GO semantics

Individual `verdict=GO` допустим только когда:

1. все 114 disposition assessments имеют `assessment=ADEQUATE`;
2. все 11 cluster assessments имеют `assessment=ADEQUATE`;
3. все 15 XD assessments имеют `assessment=ADEQUATE`;
4. все 9 legacy assessments имеют `closure=CLOSED` и `assessment=ADEQUATE`;
5. каждый legacy `original_claim_sha256` равен frozen original record;
6. `blocking_new_findings=0`, `new_findings=[]`, `unresolved_design_conflicts=0`;
7. exact plan/content/subject/manifest constants совпадают;
8. reviewer role/review ID соответствуют назначенному slot.

Нельзя реализовывать это одним наличием `if verdict=GO`. Schema обязана перечислить const constraints для каждого из 114+11+15+9 keys; batch validators независимо повторяют semantic check программно.

## 6. Immutable subject без self-hash loop

### 6.1 Три уровня identity

**Content set** содержит план, exact inputs, V0/V1–V10/XD, 114 dispositions, 11 closure records, AT/NC/EV catalogs, alias/status maps, source lock, exclusions, correction R1, original legacy audit record и frozen master prompt. Не содержит review/quorum schemas, validator sources, run transcripts, final manifest или anchor.

```text
content_set_sha256 = SHA256(
  UTF8("N8NAGENTS-PLAN-V2-CONTENT-V3\0") ||
  for each content record in ordinal UTF-8 path order:
    U32BE(path_bytes) || path_utf8 || U64BE(file_bytes) || SHA256_RAW(file)
)
```

**Subject envelope** связывает content и инструменты интерпретации, но не содержит собственный hash:

```text
subject_envelope_sha256 = SHA256(
  UTF8("N8NAGENTS-PLAN-V2-REVIEW-SUBJECT-V3\0") ||
  SHA256_RAW(content_set_sha256) ||
  FILE_FRAME(14_REVIEW_SCHEMA_V2.json) ||
  FILE_FRAME(23_QUORUM_SCHEMA_V2.json) ||
  FILE_FRAME(20_PREFREEZE_CHECKER_NODE.mjs) ||
  FILE_FRAME(21_PREFREEZE_CHECKER_PYTHON.py) ||
  FILE_FRAME(25_RAW_REVIEW_BATCH_VALIDATOR_NODE.mjs) ||
  FILE_FRAME(26_RAW_REVIEW_BATCH_VALIDATOR_PYTHON.py) ||
  FILE_FRAME(28_WINDOWS_PATH_CUSTODY_COLLECTOR.ps1)
)
```

`FILE_FRAME = U32BE(path_bytes)||path_utf8||U64BE(file_bytes)||SHA256_RAW(file)`.
`SHA256_RAW(x)` означает ровно 32 digest bytes: lower-hex representation сначала строго декодируется, а не хешируется как 64 ASCII characters.

**Final manifest** перечисляет content, schemas, validator sources и prefreeze transcript index. Он исключает собственные bytes. Внешний `final_manifest_sha256=SHA256(raw manifest bytes)` записывается только в detached anchor и reviewer dispatch metadata.

### 6.2 Reviewer binding

Каждый raw review record содержит exact constants:

```json
{
  "plan_bytes": 57133,
  "plan_sha256": "91ba3acd07ab0eb87f3ea42d788eb0c6b581734ae14235a75706a011f8f0b672",
  "content_set_sha256": "<frozen const>",
  "subject_envelope_sha256": "<frozen const>",
  "manifest_sha256": "<external frozen const>",
  "validation_index_sha256": "<detached frozen validation index const>"
}
```

Review schema может содержать `content_set` и `plan` const, но не должен содержать hash собственных полных bytes. `subject_envelope` и external `manifest` проверяются batch validator-ом против trusted anchor/config, а не против reviewer-supplied top-level aggregate.

## 7. Raw R1–R10 batch validators

### 7.1 Input contract

Оба независимых batch validator получают:

```text
--bundle <literal frozen bundle root>
--anchor <literal BUNDLE_ANCHOR.txt>
--reviews <literal isolated review output directory>
--expected-wave-set R1,R2,R3,R4,R5,R6,R7,R8,R9,R10
```

Review directory содержит ровно `R1.json` … `R10.json`; unexpected file, directory, ADS, reparse point или alternate spelling — invalid batch. Files открываются literal/no-follow и хешируются из удерживаемого handle; pre/post file identity, size and last-write metadata должны совпасть.

Оба validator используют duplicate-key-rejecting JSON parser. Обычный `JSON.parse`/`json.loads` без duplicate hook недостаточен.

### 7.2 Exact role and review ID

Для каждого slot:

```text
expected_review_id = "N8N-V2-" || role || "-" || first16(subject_envelope_sha256)
```

Raw record обязан иметь `reviewer_role == role` и `review_id == expected_review_id`. Review IDs уникальны автоматически; validator всё равно проверяет uniqueness полного значения.

`record_sha256` не хранится внутри raw review. Collector вычисляет его как SHA-256 exact raw bytes и записывает только в detached batch result. Это исключает self-hash loop. Два разных role с одинаковыми raw bytes/hash — `STOP_DUPLICATE_REVIEW_HASH`, даже если filenames различаются.

### 7.3 Mandatory validation sequence

Для каждого из десяти raw records validator обязан:

1. проверить UTF-8 no BOM, LF only, exactly one final LF, no NUL;
2. отвергнуть duplicate JSON keys до object construction;
3. вычислить raw bytes/sha256;
4. применить full review JSON schema;
5. проверить exact role/review ID;
6. сравнить plan/content/subject/manifest/validation-index identities с anchor, не между самими reviews;
7. проверить exact sets и uniqueness 114/11/15/9;
8. проверить source claim hashes, section/AT/NC/EV forward and reverse references;
9. независимо вычислить `go_semantics_valid` из raw content;
10. извлечь verdict/findings для quorum, не доверяя supplied counters.

Поля `schema_valid` и `go_semantics_valid` запрещены в raw reviewer schema как caller assertions. Они появляются только в collector result со значением, вычисленным validator-ом.

### 7.4 Derived quorum rules

Batch имеет ровно десять valid records. Любой missing/extra/invalid raw record означает batch `STOP_INVALID_REVIEW_SET`, а не уменьшение denominator.

Collector сам вычисляет:

- `go_count`, `stop_count`, `blocked_count`, `changes_required_count`;
- `validated_p0_count` из всех valid raw findings;
- `consensus_p1_count` по одинаковому `canonical_new_finding_sha256`, подтверждённому минимум двумя различными релевантными roles, либо по exact frozen authoritative-source reference;
- `contradictory_go_count` из independently computed GO semantics;
- unique review IDs и unique raw record hashes.

Aggregate `GO` возможен только при одновременном выполнении:

```text
valid_review_count == 10
go_count >= 8
stop_count == 0
blocked_count == 0
validated_p0_count == 0
consensus_p1_count == 0
contradictory_go_count == 0
all_subject_and_manifest_bindings_exact == true
all_raw_record_hashes_unique == true
all_review_ids_and_roles_exact == true
```

Оставшиеся не-GO records могут быть только `CHANGES_REQUIRED` с P2/P3 без consensus P1/P0 и без невозможности оценить bundle. Любой `BLOCKED` исключает aggregate GO. Counters в proposed aggregate input не принимаются; validator генерирует их сам. Если отдельно передан summary, каждое поле сравнивается с derived value, и mismatch даёт `STOP_COUNTER_OR_VERDICT_CONTRADICTION`.

## 8. Два независимых custody validators

Node A и Python B не импортируют общий validation module, не читают output друг друга и не используют один внешний script как единственный источник verdict. Допустимы общие frozen schemas/data; алгоритм enumeration, parsing, path checking, hashing и verdict реализуется независимо.

Каждый проверяет:

### 8.1 Physical root and path safety

- bundle root и expected Vault root разрешены в absolute canonical form до чтения;
- manifest paths только relative UTF-8 `/`, NFC, без drive/UNC/root, `.`/`..`, backslash, NUL, colon/ADS, trailing dot/space и Windows reserved basename;
- exact ordinal path uniqueness, а также отсутствие collisions после NFC, NFD, Unicode casefold и Windows case-insensitive comparison;
- recursive actual file set в bundle равен exact manifest allowlist плюс отдельно объявленные detached artifacts; missing/extra directory/file запрещены;
- ни один path component не symlink/junction/reparse point;
- regular file only; `nlink==1`; pre/post device+file-id+size+mtime стабильны;
- alternate data streams отсутствуют. Python B использует `FindFirstStreamW/FindNextStreamW`; Node A использует только `28_WINDOWS_PATH_CUSTODY_COLLECTOR.ps1`, exact hash которого включён в subject. Один и тот же helper для A и B запрещён;
- file handles открываются до hash; final path from handle остаётся внутри approved root; identity повторно проверяется после чтения.

### 8.2 Byte and manifest custody

- valid UTF-8, no BOM, LF, exactly one final LF для каждого text artifact;
- declared bytes/SHA-256 каждой manifest entry равны actual;
- entry order exact ordinal UTF-8 и aggregate framing пересчитан;
- canonical plan exact identity;
- master prompt frozen copy exact `27410 / 7b271d…8da3`;
- source/input chain пересчитан полностью, включая V9 `64893 / c2a40596…74536`, XD и original legacy record;
- content set пересчитан из exact records, не из count;
- subject envelope пересчитан из content+schema+validator source identities;
- manifest не содержит себя, subject не содержит schemas that contain subject hash, transcript не требует собственного hash;
- schema exact sets 114/11/15/9 и original legacy hash mappings;
- no unlisted source, generator state, temp file or stale previous review output.

### 8.3 Transcript binding

Каждый validator выдаёт один canonical JSON transcript без self-hash:

```json
{
  "validator_id": "CUSTODY-A",
  "validator_source": {"bytes": 0, "sha256": "<actual>"},
  "runtime_fingerprint": {},
  "started_utc": "<RFC3339>",
  "completed_utc": "<RFC3339>",
  "manifest_sha256": "<actual external>",
  "content_set_sha256": "<actual>",
  "subject_envelope_sha256": "<actual>",
  "checks": [{"check_id": "<stable ID>", "result": "PASS", "observed_sha256": "<when applicable>"}],
  "mutation_runs": [],
  "result": "PASS",
  "process_rc": 0
}
```

Detached `VALIDATION_INDEX.json` содержит path/bytes/SHA-256 обоих exact transcript files, source hashes, final manifest hash и subject hash. `BUNDLE_ANCHOR.txt` содержит SHA-256 exact bytes `VALIDATION_INDEX.json`. Index не содержит собственного hash; anchor не входит в manifest/index. Reviewer dispatch binds exact anchor bytes/hash. A/B disagreement даёт `STOP_VALIDATOR_DIVERGENCE`.

Run record обязан сохранять exact command, cwd, executable/runtime bytes or official installed identity, OS/kernel/filesystem fingerprint, stdout bytes/hash, stderr bytes/hash, exit code и complete mutation result list. Простого `"all_pass": true` недостаточно.

## 9. Required false-GO and custody mutation matrix

Оба validators выполняют каждый canary на isolated in-memory/disposable copy. Original frozen candidate не изменяется. Каждый canary обязан вернуть exact nonzero class и доказать, что mutation действительно применена.

| Canary ID | Единственная mutation | Ожидаемый результат |
|---|---|---|
| `FG-001` | `8 GO + 2 BLOCKED`, остальные поля правдоподобны | `STOP_QUORUM_BLOCKED_PRESENT` |
| `FG-002` | duplicate `review_id` у R1/R2 | `STOP_DUPLICATE_REVIEW_ID` |
| `FG-003` | два raw review имеют одинаковый SHA-256/bytes | `STOP_DUPLICATE_REVIEW_HASH` |
| `FG-004` | R2 record содержит role/review ID R1 | `STOP_ROLE_ID_MISMATCH` |
| `FG-005` | один review содержит другой subject hash | `STOP_SUBJECT_MISMATCH` |
| `FG-006` | один review содержит arbitrary but valid 64-hex manifest hash | `STOP_MANIFEST_MISMATCH` |
| `FG-007` | supplied counter отличается от derived counter | `STOP_COUNTER_OR_VERDICT_CONTRADICTION` |
| `FG-008` | aggregate verdict GO при derived non-GO | `STOP_COUNTER_OR_VERDICT_CONTRADICTION` |
| `FG-009` | GO review имеет одну legacy closure `OPEN` | `STOP_CONTRADICTORY_GO` |
| `FG-010` | GO review имеет legacy assessment `INADEQUATE` | `STOP_CONTRADICTORY_GO` |
| `FG-011` | missing один из 9 legacy keys | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-012` | extra legacy key | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-013` | wrong legacy `original_claim_sha256` | `STOP_LEGACY_CLAIM_MISMATCH` |
| `FG-014` | missing/extra один из 114 finding keys | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-015` | missing/extra один из 11 cluster keys | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-016` | missing/extra один из 15 XD keys | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-017` | duplicate JSON key, скрытый обычным parser | `STOP_DUPLICATE_JSON_KEY` |
| `FG-018` | reviewer asserts `schema_valid=true` while raw invalid | `STOP_REVIEW_SCHEMA_INVALID` |
| `FG-019` | raw review bytes changed after recorded hash | `STOP_REVIEW_HASH_MISMATCH` |
| `FG-020` | 10 invented metadata rows, raw files отсутствуют | `STOP_INVALID_REVIEW_SET` |
| `CU-001` | master prompt one-byte change | `STOP_MASTER_PROMPT_IDENTITY_CHANGED` |
| `CU-002` | manifest entry wrong bytes/hash | `STOP_MANIFEST_ENTRY_MISMATCH` |
| `CU-003` | content aggregate wrong при верных counts | `STOP_CONTENT_SET_MISMATCH` |
| `CU-004` | subject aggregate wrong | `STOP_SUBJECT_MISMATCH` |
| `CU-005` | unlisted regular file | `STOP_UNEXPECTED_PATH` |
| `CU-006` | case-only или NFC/NFD collision | `STOP_PATH_COLLISION` |
| `CU-007` | `..`, absolute, UNC, colon/ADS path | `STOP_UNSAFE_PATH` |
| `CU-008` | symlink/junction/reparse target | `STOP_REPARSE_POINT` |
| `CU-009` | alternate data stream | `STOP_ALTERNATE_DATA_STREAM` |
| `CU-010` | hardlinked entry (`nlink>1`) | `STOP_HARDLINK` |
| `CU-011` | BOM, CRLF или extra final LF | `STOP_ENCODING_POLICY` |
| `CU-012` | validator source hash differs from subject | `STOP_VALIDATOR_SOURCE_MISMATCH` |
| `CU-013` | transcript hash differs from detached validation index | `STOP_TRANSCRIPT_MISMATCH` |
| `CU-014` | source/input-chain entry missing, включая XD/V9/legacy | `STOP_INPUT_CHAIN_MISMATCH` |

Canary record содержит `canary_id`, `base_subject_sha256`, `mutation_path`, `pre_sha256`, `post_sha256`, `mutation_observed=true`, `expected_status`, `expected_rc`, `actual_status`, `actual_rc`, `forbidden_effects_observed=[]`. Canary PASS только если mutation доказана, validator вернул expected nonzero class и original candidate post-hash не изменился.

## 10. Process RC and result namespace

Process RC остаётся переносимым `0..31`; structured status даёт точную причину:

| RC | Класс |
|---:|---|
| `0` | exact PASS |
| `20` | unsafe path/physical identity/encoding |
| `21` | manifest/input/content identity mismatch |
| `22` | subject/anchor/transcript identity mismatch |
| `23` | original legacy/master prompt custody failure |
| `24` | raw review/schema/exact-set invalid |
| `25` | duplicate/mismatched role, review ID or record hash |
| `26` | quorum `CHANGES_REQUIRED`, не GO |
| `27` | quorum STOP/P0/P1/BLOCKED/contradiction |
| `28` | validator A/B divergence |
| `29` | unexpected internal validator error; fail closed |

Structured status никогда не смешивается с runtime readiness namespaces `LAB`, `LOCAL`, `OFFLINE`, `REMOTE`. Review/custody PASS не создаёт `LAB_READY`, `LOCAL_STACK_READY`, `OFFLINE_READY` или production claim.

## 11. Acceptance criteria для R2 correction

Correction R2 считается `READY_FOR_INDEPENDENT_PREFREEZE_REVIEW`, только если представлены exact artifacts и evidence:

1. standalone original legacy record с raw source capture и exact 9 claim hashes;
2. master prompt frozen copy exact `27410 / 7b271d…8da3` во всех identity chains;
3. review schema exact 114/11/15/9 и GO closure constraints;
4. quorum implementation требует 10 valid, `>=8 GO`, `STOP=0`, `BLOCKED=0`, `P0=0`, `consensus P1=0`;
5. два raw-batch validator не доверяют caller booleans/counters/hashes;
6. два независимых custody validator пересчитывают actual bytes, manifests, content, subject, input chain и physical path invariants;
7. все `FG-001..FG-020` и `CU-001..CU-014` rejected exact nonzero, positive control PASS у A и B;
8. transcripts и source hashes связаны detached validation index/anchor без self-reference;
9. validators совпадают по subject, manifest, exact sets, derived counters и verdict;
10. UTF-8 no BOM, LF, exactly one final LF у каждого text artifact;
11. нет canonical/domain/repo/runtime/Windows/Docker/VPS mutation;
12. state остаётся draft до отдельного freeze action.

Любой missing artifact, count-only проверка, непроверенный original claim, произвольный 64-hex subject/manifest, caller-supplied validity flag или BLOCKED-compatible GO означает `CHANGES_REQUIRED`, а не partial acceptance.
