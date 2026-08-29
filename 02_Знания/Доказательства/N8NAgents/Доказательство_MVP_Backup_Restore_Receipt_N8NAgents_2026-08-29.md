---
id: "n8nagents-evidence-mvp-backup-restore-receipt-20260829"
тип: "доказательство"
статус: "historical-verified-evidence"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "local/evidence/20260829T064145Z-mvp-direct-backup-restore.receipt.tsv"
  - "[[Регламент_Backup_Restore_N8NAgents]]"
доказательства:
  - "raw SHA-256: 72ec3a639832d1b37a8bbe848a0ae2039fc1fe676a698d48a418ff1cde0ac949"
теги: ["evidence", "backup", "restore", "receipt", "redacted", "n8n"]
source_path: "local/evidence/20260829T064145Z-mvp-direct-backup-restore.receipt.tsv"
source_repository_head_at_import: "dd9e10a9b9b51e33761971e517a61a6bd9fa899c"
source_repository_status: "LOCAL_ONLY / NO_ORIGIN / NOT_DEPLOYED"
source_tracking_status: "ignored local evidence; bytes are not part of the commit tree"
source_file_sha256: "72ec3a639832d1b37a8bbe848a0ae2039fc1fe676a698d48a418ff1cde0ac949"
source_hash_semantics: "SHA-256 of exact 3729 raw source bytes; UTF-8 without BOM; 71 LF-terminated logical lines"
redaction_manifest_version: "n8nagents-evidence-redaction-v1"
redaction_status: "PASS"
redacted_payload_sha256: "d5d9c2b771edc18c8a2efa6111f3e0d75dea05e02e19a65dbe533a00da0efa03"
redacted_payload_hash_semantics: "SHA-256 of UTF-8 bytes of LF-normalized fenced payload between markers, including one final LF and excluding markers/fence lines"
---

# Доказательство — MVP direct backup/restore receipt, 2026-08-29

Безопасная field-complete копия receipt о verified backup и isolated restore. Несекретные поля, statuses, counts, versions and hashes сохранены; absolute paths, host IP and credential values исключены.

## Provenance и hash semantics

- source_file_sha256 — exact raw TSV bytes до преобразований.
- redacted_payload_sha256 — LF-normalized безопасный TSV payload.
- source repository HEAD — только context; ignored receipt не входит в tree.
- Redaction односторонняя; удалённые values не восстанавливаются.

## Redaction manifest v1

Порядок 71 строк и три TSV columns сохранены. Поля path classes заменены на <REDACTED_PATH>; embedded host paths — <REDACTED_LOCAL_PATH>; non-loopback IPv4/email — markers; non-sentinel secret values — <REDACTED_SECRET_VALUE>. Hashes, pins, versions, counts, statuses and cleanup outcomes retained.

Срабатывания: path fields 6; embedded local paths 1; IP 1; emails 0; secret values 0. Receipt states secrets_in_receipt=NONE; acceptance дополнительно требует independent pattern scan.

## Redacted payload

<!-- REDACTED_PAYLOAD_BEGIN n8nagents-evidence-redaction-v1 -->
```tsv
N8NAGENTS_MVP_DIRECT_BACKUP_RESTORE_RECEIPT_V1
field	attested_utc	2026-08-29T06:41:45.161Z
field	attestation_scope	actual_direct_age_backup_and_disposable_isolated_restore
field	operator_task	<REDACTED_LOCAL_PATH>
field	result	BACKUP_VERIFIED_AND_RESTORE_PASS
exception	storage	MVP_USER_ACCEPTED_LOCAL_C_BACKUP_SAME_PHYSICAL_DISK
backup	id	20260829T060609Z-4efd8100c2cf
backup	remote_path	<REDACTED_PATH>
backup	remote_size_bytes	573768
backup	remote_sha256	23e1fdad6728b62cbe007d4cdfc39721c749f32df9ed28a034b315edd03f3395
backup	local_path	<REDACTED_PATH>
backup	local_size_bytes	573768
backup	local_sha256	23e1fdad6728b62cbe007d4cdfc39721c749f32df9ed28a034b315edd03f3395
backup	remote_local_hash_match	PASS
backup	remote_local_size_match	PASS
backup	local_sidecar_match	PASS
backup	local_acl	PASS_CURRENT_USER_SYSTEM_ADMINISTRATORS_ONLY
backup	age_recipient_match	PASS
backup	age_full_aead_decrypt	PASS
backup	plaintext_server_stage_removed	PASS
backup	production_live_mutation	NONE_OBSERVED
backup	production_release_id	20260828T072000Z-15e14e3735d195e38d9c3d90a77976d1b0e1ad25
backup	production_workflows_before_after	8_TOTAL_0_ACTIVE
backup	wrapper_local_path	<REDACTED_PATH>
backup	wrapper_sha256	e9e4510430dd9b92314a119ccc4208becbe19c186194cf364d0bc5b2945de543
backup	wrapper_size_bytes	11822
backup	wrapper_format	UTF8_NO_BOM_LF_CR0_SH_N_PASS
backup	wrapper_review	INDEPENDENT_GO_P0_0_P1_0_P2_0
backup	wrapper_remote_path	<REDACTED_PATH>
backup	execution_command	ssh_root_at_<REDACTED_IP>_exec_sh_exact_remote_wrapper
backup	execution_tool_reference	exec_chunk_dcface
backup	execution_exit	0
backup	execution_log_hash	unknown/not-recorded
cleanup	failed_pg_dump_literal_dash_artifact	REMOVED_AFTER_EXACT_LSTAT_AND_PG_RESTORE_LIST_PASS
cleanup	failed_pg_dump_literal_dash_path	<REDACTED_PATH>
cleanup	failed_pg_dump_literal_dash_final_state	ABSENT_NONLINK_POSTGRES_HEALTHY
restore	method	LOCAL_DISPOSABLE_DOCKER_INTERNAL_ONLY
restore	docker_client_version	29.7.2
restore	docker_server_version	29.7.2
restore	docker_server_os_arch	linux_amd64
restore	postgres_image	postgres:17.11-alpine3.24@sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73
restore	n8n_image	docker.n8n.io/n8nio/n8n:2.36.7@sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c
restore	n8n_runtime_version	unknown/not-recorded
restore	network_internal	PASS
restore	host_port_bindings	0
restore	postgres_ready	PASS
restore	n8n_metadata_database	RESTORED_PG_CUSTOM_FORMAT_PASS
restore	assistant_app_database	RESTORED_PG_CUSTOM_FORMAT_PASS
restore	n8n_state	RESTORED_PASS
restore	n8n_health_http_status	200
restore	workflow_count	8
restore	active_workflow_count	0
restore	credential_count	2
restore	credential_decrypt_validation	PASS
restore	credential_values_output	NEVER
restore	n8n_public_started	NO
restore	caddy_started	NO
restore	script_local_path	<REDACTED_PATH>
restore	script_sha256	0529f9567bd6407050b18f08bc8dc87cab84f6739fcfffff4e43b284bbd42cf5
restore	script_size_bytes	9641
restore	execution_command	pwsh_one-shot-isolated-restore.ps1
restore	execution_tool_reference	exec_session_76819_chunk_f987ff
restore	execution_exit	0
restore	execution_log_hash	unknown/not-recorded
cleanup	disposable_containers_volumes_networks_remaining	0
cleanup	plaintext_restore_temp_exists	false
cleanup	plaintext_credential_export_exists	false
cleanup	encrypted_local_backup_exists	true
evidence	secrets_in_receipt	NONE
evidence	command_logs_persisted	NO
evidence	missing_log_hashes	EXPLICIT_UNKNOWN_NOT_RECORDED
```
<!-- REDACTED_PAYLOAD_END n8nagents-evidence-redaction-v1 -->

## Ограничения

- Point-in-time historical evidence; не заменяет fresh production revalidation.
- Paths/IP нельзя восстанавливать или использовать как recovery inputs из этой заметки.
- Decrypted credential values отсутствуют.
