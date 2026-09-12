APPROVE_SUPERSESSION — условно, на уровне governance-протокола; не как уже активированный baseline.

Причина: C1 честно фиксирует необратимую потерю первого raw без реконструкции, а C2 является точной доступной provenance-source. Prospective supersession допустим, если C2 никогда не называется «original/first audit» и C1 остаётся постоянной частью цепочки.

Проверенные identity:

- C1: `1312` bytes, SHA-256 `52765124ad0e60f6142b24521228b4562bfca3c30bba52a488a0ade43d473f06`
- C2 raw: `7957` bytes, SHA-256 `2c6f25a2ab02e7d9995df0ecbc4456f69dfadd0c044f403c0420ea23e13295ae`
- C2 attestation: `1124` bytes, SHA-256 `3a5d8d3bcb49a613c39a8695f1b94e5f4e61d45bfc77bae31526ec42c1b4b101`
- A: `78558` bytes, SHA-256 `27f4b1f56384fb41db54394decad52d38da123aef7cf7c00e85103a96d0e7008`
- B: `33080` bytes, SHA-256 `350171ffb6727330cb2d218d256f51a5fb568dfa95b605a922411f0478bba2e7`
- Все пять: UTF-8 без BOM, LF-only, один final LF, без NUL.
- C2 attestation соответствует фактическим bytes/format raw.

Точные 0-based spans полных Markdown-строк C2, без завершающего LF:

| ID | line | offset | bytes | SHA-256 |
|---|---:|---:|---:|---|
| P1-01 | 9 | 384 | 547 | `b52fbcb042a8411a589f147104bc87c6bb58a89c46cd4d7aae214dbbb9109001` |
| P1-02 | 10 | 932 | 543 | `e8861b4330f8882f4345c6acb8971b775c395b5890beaca6262fb05e847cf2e5` |
| P1-03 | 11 | 1476 | 296 | `9f2fb676eac5430ec414d02add6f1a0ac9e7cf021ddfa181febe8c32f9b26c44` |
| P1-04 | 12 | 1773 | 431 | `e9be26aa4fa06e7b8898bffd22658efa5fa3405085bd44dc1d0a7190527cae4d` |
| P1-05 | 13 | 2205 | 483 | `48be678f9d1f00258e9d119909e8183646beb91fb377b9144cc73acd73f2d290` |
| P1-06 | 14 | 2689 | 485 | `d479d9221535686db48612d52aff16f9ec8fb7fb79b3ba3957d6064f47ba3fa3` |
| P1-07 | 15 | 3175 | 479 | `774aada7e7e98e9bd8a35340e7d5516ddac9512d30bbb1db440a20c85b0e411e` |
| P1-08 | 16 | 3655 | 264 | `7de88511d8546175d64000c1bbc3adef6540270126c9e0e4d590b09e29613990` |
| P2-01 | 17 | 3920 | 347 | `3f82579ed1069be7fef00e2f839d63b55da271feb90a00a2ddc69d12cdbc9677` |
| NEW-P1-01 | 21 | 4314 | 177 | `b0fca035dd1f728fc47e9bedefea76124849461bfec380d1f3711b74156fa8e5` |
| NEW-P1-02 | 22 | 4492 | 187 | `e0da331a90e8951ae44a8bae9e300597dc1360635448def565bcbb6139721d16` |
| NEW-P1-03 | 23 | 4680 | 147 | `3eb671fcae87b3aa9f10910be456cd91becc0b659e06111cd8ef6467c2036444` |
| NEW-P1-04 | 24 | 4828 | 178 | `8dd12091923d9a62b2d186f4ba523efe0a30e976958cf1356bb0b44be7d49ba0` |

Общие acceptance-resolution spans, строки 43–48:

`6590/364/b1a625…43d61`, `6955/287/7d6843…3c4e`, `7243/175/f893eb…d16`, `7419/291/8c3ecf…451f`, `7711/136/54ea25…8135`, `7848/108/c99aec…2c03`.

Обязательные контроли:

1. Постоянно хранить C1 и C2 raw/attestation в content/input/manifest chains. Запрещены реконструкция первого raw, переименование C2 в original и удаление C1 после активации.
2. Создать отдельный record kind вроде `SUPERSEDING_PREFREEZE_BASELINE_R2`, а не `ORIGINAL_LEGACY_AUDIT`. Exact ordered set: `P1-01..P1-08`, `P2-01`, `NEW-P1-01..NEW-P1-04`.
3. `19_PREFREEZE_CORRECTION_R1.json` оставить только historical remediation/cross-check: `4583` bytes, SHA-256 `e62873…5591`; он не может поставлять claim/evidence/impact/resolution.
4. Привязать successor к audited subject из C2 строк 28–34: plan `57133/91ba3a…b672`, manifest `12184/883f7c…cc9e`, correction №19, manifest aggregate `71298d…12e`, input chain `39/2a3996…c840`, content set `12/7cbab1…f1d5`, envelope `5/740679…6cc`. Если старые bytes нельзя replay-проверить, поле должно честно говорить `SOURCE_ASSERTED_NOT_REPLAYED`; нельзя заявлять validator-recomputed binding.
5. Во всех B/schema/validator местах заменить exact `/9` на exact `/13`, включая mandatory maps, GO semantics, content/input chains, canaries и acceptance criteria. Epoch/namespace должен исключать смешение одноимённых P1/P2 из утраченного первого аудита и C2.
6. Individual review `GO` разрешён только если все 13 имеют одновременно `closure=CLOSED` и `assessment=ADEQUATE`, с forward/reverse binding к section/AT/NC/EV. Это относится и к уже `ADEQUATE` в C2 P1-03/P1-08: автоматическая closure запрещена.
7. Meta-quorum supersession — отдельные `3/3` независимые detached decisions. Он не заменяет окончательный R1–R10 quorum `10 valid / >=8 GO / STOP=0 / BLOCKED=0 / P0=0 / consensus P1=0`.
8. Каждое из трёх решений обязано иметь уникальные reviewer slot/task/raw-decision hash и связывать C1, C2 raw, attestation, successor record, финальные A/B, review/quorum schemas, validators, manifest/content/subject/anchor. Разные hashes, duplicate decision или `<3/3` дают STOP.
9. После любых правок A/B/schema нужны новые exact bytes/hashes и повторное подтверждение reviewers. Текущая conditional approval не может быть переписана как будто reviewer видел будущие bytes.
10. Два независимых validator и canaries обязаны отвергать: missing/extra ID; 9-only schema; один `OPEN/INADEQUATE` при GO; подмену C2 на №19; relabel C2 как first/original; C1 missing; wrong old-subject binding; 2/3 или duplicate approvals; один approval на иной hash; post-approval изменение A/B/schema; generic/unbound owner decision.
11. Активация не даёт freeze/integration/runtime authority и не стирает исторический `STOP_LEGACY_SOURCE_MISSING`.

Текущее B ещё нормативно требует original raw и exact `114/11/15/9`, поэтому supersession сейчас не активен.

Owner authorization: `делай` достаточно для подготовки/редактирования документации и проведения review. Для активации нового authoritative baseline этого недостаточно. Нужен новый явный owner gate после финальных rehash и `3/3`, содержащий exact hashes, effect set `review-baseline supersession only`, отсутствие ретроактивного original-claim, запрет freeze/integration/runtime и, желательно, decision ID/TTL. Это следует и из hash/effect-bound gate принципа A/XD-15; generic imperative не связывает ещё не существующие финальные artifacts.

Никакие файлы не создавались и не изменялись; project runtime и сеть не использовались.
