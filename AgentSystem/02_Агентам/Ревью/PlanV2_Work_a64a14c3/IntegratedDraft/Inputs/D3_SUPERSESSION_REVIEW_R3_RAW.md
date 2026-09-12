R3 DECISION: `APPROVE_SUPERSESSION`

Статус решения: условное, prospective-only, `NOT_ACTIVE`. Оно разрешает подготовку supersession-пакета, но не его активацию.

Проверено независимо:

- C1: `1312` bytes, SHA-256 `52765124ad0e60f6142b24521228b4562bfca3c30bba52a488a0ade43d473f06`.
- C2 raw: `7957` bytes, SHA-256 `2c6f25a2ab02e7d9995df0ecbc4456f69dfadd0c044f403c0420ea23e13295ae`.
- C2 attestation: `1124` bytes, SHA-256 `3a5d8d3bcb49a613c39a8695f1b94e5f4e61d45bfc77bae31526ec42c1b4b101`.
- Все три файла: UTF-8 без BOM, LF, ровно один финальный LF.
- C2 содержит ровно 13 уникальных baseline IDs. Zero-based byte spans `[start,end)`, включая LF:

| ID | Span | SHA-256 |
|---|---:|---|
| P1-01 | 384–932 | `e1a936cb64c83fd7c400611021ddeb86c668a5f2633f2998220bed09b1299ad9` |
| P1-02 | 932–1476 | `fcf474040be7de7fe223852fd1ae3752dc2d72de891cb32bda7faf3d7a98411f` |
| P1-03 | 1476–1773 | `7a30563f5db47961d11cc3cb7e64ab9dba64f851b0bec4becb5c4ba43a24f1e5` |
| P1-04 | 1773–2205 | `f4e8a85325b9f1f6314a4f437f529b14889ea105d901343672e9a4112d827ffa` |
| P1-05 | 2205–2689 | `295297b4379636b6ea9470a3c846af8435e57f2ddc61d953b37d3e05ee3f3439` |
| P1-06 | 2689–3175 | `a3939b5e3af7a598716f9e8a00509770c213b9907f2ed5ff03b35cb43f4af733` |
| P1-07 | 3175–3655 | `25ee745a8ac024ea0e0227c7e22e08028b9ae2471ec6359ee47b412f1d7c201f` |
| P1-08 | 3655–3920 | `6350f93d59651efc60970bc45be8d3007641603e3e13bb099d41cb2f48377965` |
| P2-01 | 3920–4268 | `0f7cfd0af64b3465fb1bb481e06f1a0ca75f54bd1a5bc4b685f40c0991158ff7` |
| NEW-P1-01 | 4314–4492 | `660f63abf4dd908740e6081e5202c1f6242a47747464668b047e68c6c7635c42` |
| NEW-P1-02 | 4492–4680 | `5525228ff052a6effc9e13cd57679fb66c9e8c8e51c01e8dc2698a373859537c` |
| NEW-P1-03 | 4680–4828 | `4860342856fe33f1f94a3b50e3882dfcbfd8420b168a67b75187774261f33f96` |
| NEW-P1-04 | 4828–5007 | `20495441e50ce7aa63171414d1f4fe02e25d013743cb3afc1f7ec9c2f44755f7` |

Обязательные условия:

1. C1 остаётся постоянным immutable loss incident со статусом `STOP_LEGACY_SOURCE_MISSING`.
2. C2 называется только `second pre-freeze audit prospective successor baseline`; запрещены `original`, `recovered original`, ретроактивная замена или утверждение, что loss устранён.
3. Исходный `CHANGES_REQUIRED` и оценки C2 не переписываются. Последующее `13 × CLOSED/ADEQUATE` хранится отдельно как assessment финального subject.
4. №19 остаётся только remediation record и не используется для baseline-текста, spans или item hashes.
5. Review schema требует exact set 13 и GO только при `closure=CLOSED && assessment=ADEQUATE` для каждого ID.
6. Нужны три detached независимых решения с уникальными reviewer/review IDs и raw hashes; только `3/3 APPROVE_SUPERSESSION`.
7. Raw-batch и custody validators должны пересчитывать C1/C2/attestation, spans, item hashes, exact 13 set, decisions, manifest/subject/anchor и отвергать missing/extra ID, ложный `original`, authority от №19, duplicate decision и activation без owner gate.
8. Supersession не даёт freeze/runtime/publication authority.

Текущая активация невозможна:

- B всё ещё требует отсутствующий `ORIGINAL` и exact legacy set 9; этот контур необходимо заменить successor-семантикой.
- Текущий A имеет `78791 / 5a8fa787…14e0a`, тогда как registry №29 привязан к прежнему `78558 / 27f4b1f5…e7008`.
- Финальные validator artifacts, согласованные hashes, 3/3 detached decisions и owner activation отсутствуют.

Owner gate: прежнее общее `делай` достаточно только для подготовки. После финальных hashes и 3/3 требуется новый точный owner command, связывающий C1, C2, attestation, supersession record, final manifest/subject/anchor и три decision hashes, например `ACTIVATE_C2_PROSPECTIVE_SUPERSESSION <anchor_sha256>`. Без него supersession остаётся неактивным.
