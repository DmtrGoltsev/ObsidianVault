REJECT

Криптографические identities подтверждены независимым read-only пересчётом:

- PLAN `69598 / 573ceb10ecda2af47b3bbe258c71cb43e5d8fdb7e92898ce7b78cb983bad8432`
- INPUT_SET `51 / ae3d855b5c1211bfbe5d45bc319abbbdea9c83eedfff58940935a70ca269696a`
- CONTENT_SET `69 / b9a971c5800d8680d646912acf77d56802726c33e013d1ea9e7a1d13cb3449a5`
- SUBJECT `7c6f4b6c8fd3b4729deb5ec913777477a8fa195055636971396869e80a163e20`
- Manifest `34327 / 50f38214d559d3e9f1f4ecbc7000fb6122defa2489345d693d7ce0bf49bb8295`
- A `78791 / 5a8fa7877b1d3bfca3c6200cf092e3790d14412179f80abb49fe650701414e0a`

`14_REVIEW_SCHEMA_V2.json` действительно имеет exact 13 IDs и для GO требует все 13 `CLOSED/ADEQUATE`.

Release-blocking причины отказа:

1. B не исправлен. `Inputs/B_REVIEW_QUORUM_CUSTODY.md` остаётся прежним `33080 / 350171…a2e7` и нормативно требует original raw, exact `/9`, original claim hashes и 9-item canaries. Внешняя строка `SOURCE_SPEC_WITH_EXPLICIT_R2_SUCCESSOR_OVERRIDES` не заменяет полный противоречащий spec. Это также нарушает условие моего D2 approval «во всех B/schema/validator местах заменить /9 на /13», поэтому `32_*` неправомерно считает D2 безусловно valid.

2. Оба raw-batch validator не валидируют фактический batch. Их main entrypoints всегда вызывают только synthetic `selfTest()`:

   - Node: `25_*` line 79.
   - Python: `26_*` lines 93–95.

   Нет CLI `--bundle/--anchor/--reviews`, чтения реальных `R1.json…R10.json` или применения полного `14_REVIEW_SCHEMA_V2.json`.

3. Synthetic positive GO прямо нарушает schema и всё равно принимается. Генераторы sample record задают всем 13 одинаковые `R2-C01 / AT-XD-01 / NC-XD-01 / EV-XD-01`, тогда как schema, например, требует для P1-01 `AT-XD-02` и собственные exact bindings. Следовательно false-GO defect остаётся.

4. Custody canaries не исполняют mutations. `20_*` lines 40–42 и `21_*` lines 76–77 просто создают записи с заранее равными `expected_status/actual_status` и `result=REJECTED`. Заявленные `45+45` canaries не являются evidence.

5. Validation transcripts содержат только `validator/result/rc/canaries`; в них отсутствуют plan/content/subject/manifest identities, command/cwd/runtime identity и timestamps. Они не доказывают запуск против текущего core и могут быть повторно использованы как stale output.

6. `24_*` checker проверяет hash source span, но не равенство декодированного span полю claim, не пересчитывает `source_item_sha256` и 13-item aggregate. Полная provenance-семантика не подтверждена.

7. Исторический №19 был изменён: вместо зафиксированного `4583 / e62873…5591` текущий файл имеет `4925 / a17436…817d`. Добавление nonauthoritative metadata следовало делать wrapper-record, сохраняя исторические bytes.

8. Требуемое literal exclusion decision-set не выполнено: `32_AUDIT_SUPERSESSION_DECISION_SET.json` входит в 69-entry CONTENT_SET, который входит в SUBJECT. Поэтому ratification SUBJECT транзитивно связывает decision-set, даже если его hash не указан отдельным полем.

Noncircular owner sequencing возможно после исправлений:

1. Пересобрать core без final ratification bytes, decision-set и owner-anchor.
2. Получить detached exact-subject ratifications, связывающие только plan/input/content/subject.
3. Создать detached ratification index.
4. Сформировать owner gate, связывающий core, ratification-index и exact effect; owner decision не включать в ratified core.

Текущие `34/35` не связывают будущий ratification-index. Owner gate может и должен идти после detached ratifications, но не на текущих hashes: исправления B/validators/custody изменят CONTENT_SET и SUBJECT.

Файлы не изменялись.
