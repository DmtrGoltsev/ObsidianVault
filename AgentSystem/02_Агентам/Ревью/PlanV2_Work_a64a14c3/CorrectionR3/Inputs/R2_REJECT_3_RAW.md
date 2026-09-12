R3 DECISION: `REJECT`

Идентичности пересчитаны независимо и совпадают:

- PLAN: `69598 / 573ceb10…8432`
- INPUT_SET: `51 / ae3d855b…696a`
- CONTENT_SET: `69 / b9a971c5…49a5`
- SUBJECT: `7c6f4b6c…3e20`
- Manifest: `34327 / 50f38214…8295`
- Decision set: `5209 / a99d5644…ac42`
- Pending anchor: `1102 / 648444dc…8151`
- A: `78791 / 5a8fa787…14e0a`
- Schema содержит exact 13 IDs, `additionalProperties=false`, а GO-ветка требует для всех 13 `CLOSED/ADEQUATE`.

Release-blocking причины:

1. Оба custody checker не выполняют заявленные 45 mutation canaries. Их `selfTest/report` непосредственно присваивает `actual_status=expected_status`, `mutation_observed=true`, `result=REJECTED`, не применяя мутацию и не вызывая validator. Поэтому transcripts и run record доказывают только самозаявленные результаты.

2. Raw-batch validators проверяют только сгенерированный synthetic batch. Их environment использует фиктивные hashes `1…5`; реальные R1–R10 records не загружаются. Более того, synthetic GO records не соответствуют `14_REVIEW_SCHEMA_V2.json`: отсутствуют обязательные timestamps, а audit references используют общие `R2-C01/AT-XD-01/NC-XD-01/EV-XD-01` вместо schema const bindings. Validators саму JSON Schema не исполняют и reverse bindings не проверяют.

3. Noncircular requirement не выполнен: `32_AUDIT_SUPERSESSION_DECISION_SET.json` входит в 69-entry CONTENT_SET. Следовательно, ratification, связывающий CONTENT_SET/SUBJECT, транзитивно связывает decision set и не может одновременно явно исключить его.

4. Текущий pending anchor и owner request связывают прежний conditional decision set, но не будущий detached exact-subject ratification set. Поэтому owner gate после новых ratifications не будет доказывать их состав и hashes.

На текущем subject supersession не может просто ожидать owner gate. Требуется:

- исключить decision set из immutable core content/input construction;
- заменить custody canaries реальными isolated mutations;
- прогнать batch validators над фактическими schema-valid raw reviews;
- получить detached 3/3 exact-core ratifications;
- сформировать отдельный detached ratification index;
- только затем пересобрать pending anchor/owner request, связывающие core и ratification index.

До этого `PENDING_OWNER_SUPERSESSION / NOT_ACTIVE`; owner activation недопустима. Файлы не изменялись.
