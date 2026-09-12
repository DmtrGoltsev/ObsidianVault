REJECT

Core identities independently recompute correctly:

- PLAN `69598 / 573ceb10…8432`
- INPUT_SET `51 / ae3d855b…696a`
- CONTENT_SET `69 / b9a971c5…49a5`
- SUBJECT `7c6f4b6c…3e20`
- manifest `34327 / 50f38214…8295`
- corrected A `78791 / 5a8fa787…14e0a`
- B `33080 / 350171ff…a2e7`
- decision set `5209 / a99d5644…ac42`
- pending anchor `1102 / 648444dc…8151`

Все 81 manifest entry identities совпали. Exact 13 baseline/schema binding также корректен: 13 required IDs, 13 properties, все C2 source-span hashes и `source_item_sha256` const совпадают, GO-ветка охватывает все 13.

Release-blocking false-GO остаётся в обоих raw-batch validators:

1. Они не реализуют B-spec input contract `--bundle/--anchor/--reviews/--expected-wave-set` и не читают реальный `R1.json…R10.json`. Node lines 48–79 и Python lines 58–95 запускают только встроенный `selfTest()` с фиктивными identities `1…1`, `2…2`, `3…3`, `4…4`, `5…5`.

2. Full `14_REVIEW_SCHEMA_V2.json` вообще не применяется, вопреки B lines 357–368. `validateRecord` вручную проверяет лишь часть полей. Запись без `model`, timestamps, attestations, audit rationale и section/AT/NC/EV references может получить `semantic_go=true`, если содержит минимальные ADEQUATE/CLOSED flags и hashes. Это прямой ложный GO без доказательства closure.

3. Consensus P1 использует недоверенное `new_findings[].reviewer_role`, а не outer validated reviewer role: Node line 40, Python line 49. Поскольку shape `new_findings` schema не проверяется, два reviewer могут сообщить одинаковый canonical P1 с отсутствующим/одинаково spoofed inner role; set size останется `1`, `consensus_p1_count=0`, и batch `8 GO + 2 CHANGES_REQUIRED` способен ошибочно агрегироваться в `GO`.

4. Сохранённые `20 + 20` FG canaries действительно все `REJECTED`, но проверяют только synthetic in-memory batch. PASS transcripts:

   - Node `bfbf8b16c5273f41096f805d0baa25faadc4dfe2070d24dcb3661c5dc6d6497f`
   - Python `41be95f9eb6a355903326d610c99873c2349ac3497004bdcd500c2c5834219db`

   не являются evidence проверки произвольного actual review directory.

Есть и граница noncircularity: `32_AUDIT_SUPERSESSION_DECISION_SET.json` уже входит в 69-entry content set. Поэтому ratification, связывающий данный CONTENT_SET/SUBJECT, неизбежно транзитивно связывает decision-set; он не может одновременно заявить его исключение. Own ratification bytes и owner-anchor действительно detached, но требуемое исключение decision-set текущим core не соблюдается.

Owner gate должен оставаться `NOT_GRANTED`. Final supersession сейчас не может просто ожидать owner activation после detached ratifications. Сначала нужны реальные file-backed A/B batch validators с full-schema validation, anchor-derived env, outer-role consensus и mutation canaries против actual batch; затем rebuild/re-hash core. Если decision-set требуется исключить из ratified core, его также надо вынести из content set до нового SUBJECT и повторной ratification.
