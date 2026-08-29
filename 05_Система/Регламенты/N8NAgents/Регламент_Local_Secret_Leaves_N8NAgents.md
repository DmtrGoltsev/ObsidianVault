---
id: "regulation-n8nagents-local-secret-leaves"
тип: "регламент"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents local/secrets/README.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "local/secrets/README.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
source_repository_publication: "LOCAL_ONLY — source repository has no origin; source_base and successor are not upstream-published"
source_snapshot: "untracked/ignored working-tree source document at import"
source_file_sha256: "3b09e17ceeb90141fc0d9c826614721f304babfa0745dd8d73c04f20f723c8ff"
source_hash_semantics: "SHA-256 of exact raw source bytes: UTF-8 without BOM, LF line endings, two terminal LFs"
transform_manifest_version: "n8nagents-source-import-v1"
transformed_payload_sha256: "6cb3eefa2d09be587c977be4defdff94bc8ab27aa855b3fa86f07111287fbe23"
transformed_payload_semantics: "SHA-256 of UTF-8/LF bytes between SOURCE_PAYLOAD markers, excluding marker-adjacent LF delimiters"
imported_date: "2026-08-29"
source_status: "local secret-file handling snapshot; no secret values are imported"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

<!-- SOURCE_PAYLOAD_BEGIN n8nagents-source-import-v1 -->
# Local secret leaves

Run `./local/n8nagents-local.ps1 init` to create the ignored leaf files used by
the local Compose project. Never add values to this directory in Git.

The `init` command generates the database passwords and n8n encryption key. It
creates empty, disarmed Telegram leaves. The owner later writes a separate
dev/test bot token and numeric allowlists directly to those files; tokens and
IDs are never accepted as command-line arguments.
<!-- SOURCE_PAYLOAD_END n8nagents-source-import-v1 -->

## Transform-aware provenance manifest

- Source snapshot: `local/secrets/README.md`, untracked/ignored working-tree source document imported in the context of base `09824a6e...`.
- Raw source hash: `3b09e17ceeb90141fc0d9c826614721f304babfa0745dd8d73c04f20f723c8ff`; semantics are the exact UTF-8 bytes without BOM, LF line endings, with exactly two terminal LFs.
- Embedded transformed payload hash: `6cb3eefa2d09be587c977be4defdff94bc8ab27aa855b3fa86f07111287fbe23`; extract bytes after the LF ending `SOURCE_PAYLOAD_BEGIN` through the byte before the LF preceding `SOURCE_PAYLOAD_END`.
- Content transform and redaction: none. Frontmatter, canonical-placement callout, payload markers and this manifest are wrappers outside the payload.
- Independent raw reconstruction: extract the transformed payload by the rule above; append exactly two LFs; hash the resulting UTF-8 bytes. Expected SHA-256 is the raw source hash above.
- Redaction result: none required; the source contains secret filenames and handling rules but no secret values or personal identifiers. Secret/PII scan `PASS`; no absolute local source path is stored.
