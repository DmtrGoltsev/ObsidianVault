---
id: "task-n8nagents-historical-phase-a-manifest"
тип: "задача"
статус: "историческое"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "Git N8NAgents docs/deploy-rollback-manifest.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства: []
source_path: "docs/deploy-rollback-manifest.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
source_repository_publication: "LOCAL_ONLY — source repository has no origin; source_base and successor are not upstream-published"
source_snapshot: "working tree at import; includes 24 added lines beyond source_base"
source_file_sha256: "e8a484571ec3b9c7700935b601929719081a2c82f52643c3bb44b734d7a4126b"
source_hash_semantics: "SHA-256 of exact raw source bytes: UTF-8 without BOM, LF line endings, one terminal LF"
transform_manifest_version: "n8nagents-source-import-v1"
transformed_payload_sha256: "a6f311c294c635b681cf0daa54ecef5ff39a87603a5fa62bc22cdfd706230b8d"
transformed_payload_semantics: "SHA-256 of UTF-8/LF bytes between SOURCE_PAYLOAD markers, excluding marker-adjacent LF delimiters"
imported_date: "2026-08-29"
source_status: "plan-only Phase A manifest; not current production procedure"
проверка_редакции: "PASS — secret/PII values absent; identifiers are placeholders or redacted source facts"
каноничность: "canonical vault location for this imported human-readable source document; CURRENT_STATE and the full architecture note win for runtime facts"
теги: ["n8n", "source-import", "obsidian-only-docs"]
---

> [!important] Canonical placement and source status
> Полный human-readable source document перенесён в canonical Obsidian vault. Source path указан только как provenance и может быть удалён из repository. Current verified runtime state: [[CURRENT_STATE_N8NAgents_2026-08-29]].
>

<!-- SOURCE_PAYLOAD_BEGIN n8nagents-source-import-v1 -->
# Phase A internal foundation deployment and rollback manifest

Status: **plan only; not executed**. A2 discovery is `PASS`; facts are in [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826|server-discovery.md]]. Phase A ends with PostgreSQL+n8n healthy, no workflows/credentials/traffic, Caddy off, and n8n reachable only through `127.0.0.1:5678` plus an SSH tunnel. It is not production success.

## K4R v2 recovery authority (supersedes historical fragments below)

`GO-O4-ATTEMPT1-QUORUM-v2` authorizes offline implementation and evidence work only. It authorizes no VPS, SSH, SCP, provider, Vault, network, activation or OS-reinstall action. Historical command fragments later in this document are retained as background and are not execution authority.

The release evidence flow is acyclic: build an unpublished deterministic candidate from one exact commit; obtain a strict 18-field contained-Linux capability record; execute the exact candidate bootstrap and fixed-path production runner; derive the 26-field behaviour report from the canonical 17-column execution matrix and the 18-field static record from the canonical nine-column static matrix; rebuild byte-identically; then publish the final package evidence. Review V2 is exactly 28 fields and ledger V2 exactly 29 fields. All records are UTF-8 without BOM, LF-only, exactly one final LF, ordered, duplicate-free and unknown-field-free.

`scripts/run-k4r-offline.ps1` is deliberately two-phase. With a validated capability record and an empty external output directory it emits only `K4R_OFFLINE_STATUS=CANDIDATE_BUILT`. O5 must then execute that exact candidate and write `execution-matrix.tsv`, `fault-shims.tsv` and the Linux static matrix without overwrite; Windows static verification derives `static-matrix.tsv` in the same candidate directory. A second invocation accepts only those fixed in-directory names, validates the exact 34-row fault-shim manifest, builds derived evidence, performs the byte-identical final rebuild and emits `K4R_OFFLINE_STATUS=PACKAGE_READY_FOR_REVIEW`. Neither status means `OFFLINE_READY`.

The production runner CLI is exactly:

```text
/usr/local/sbin/n8nagents-phase-a-release-gate <release-id> <attempt> <execution-go-sha256>
```

The bootstrap CLI is exactly:

```text
/bin/sh /srv/.incoming-n8nagents-<release-id>.bootstrap <release-id> <attempt> <execution-go-sha256>
```

Both reject extra arguments and copied/nonfixed execution. Every transfer source is derived under the real, symlink-free `/srv`; source, private staging and immutable final tuples/hashes are rechecked around dependent stages. Exact-root, nested and same-device bind mounts are rejected from decoded `/proc/self/mountinfo`. Activation captures the logical prior `current` target or absence. A post-activation failure or HUP/INT/TERM restores and verifies that logical state; rollback failure is terminal RC `78` with `COMMITTED_UNVERIFIED` or `UNKNOWN`. Cleanup never replaces an existing nonzero primary RC.

`OFFLINE_READY` is not remote authority. After independent acceptance, a separate owner-confirmed 21-field `N8NAgents-K4R-EXECUTION-GO-v1` record for gate `K4R-REMOTE-1` must bind the exact commit, attempt, archive, package/static/behaviour evidence, review, ledger, runner, bootstrap and owner authorization anchor. Until that separate exact record is confirmed, every remote action remains forbidden.

This document is not self-authorizing. The user authorization is the one immutable full-delivery plan envelope `N8NAgents-FULL-DELIVERY-v1`; it is not a per-commit approval and it never makes a branch, wildcard, mutable pointer, environment variable, or executor self-review authoritative. Before any delivery mutation, publish the envelope once at the fixed path below with `root:root` ownership, parent mode `0700`, record mode `0400`, and the immutable bit. Publication uses a same-directory temporary plus a no-overwrite hard link, so a duplicate envelope is a stop rather than an overwrite. The canonical scope file SHA-256 is `d95736bc4ecf4be0db63a58ce2dee9abda7f555b6d8ddf6ba5769f87393f1732`.

```sh
set -eu
plan_root=/root/n8nagents-governance
plan_record=$plan_root/N8NAgents-FULL-DELIVERY-v1.plan
install -d -o root -g root -m 0700 "$plan_root"
test ! -e "$plan_record"
plan_tmp=$(mktemp "$plan_root/.N8NAgents-FULL-DELIVERY-v1.XXXXXXXX")
cleanup_plan_tmp() { test -z "${plan_tmp:-}" || rm -f -- "$plan_tmp"; }
trap cleanup_plan_tmp EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
cat >"$plan_tmp" <<'EOF'
STATUS=APPROVED
AUTHORIZATION_ID=N8NAgents-FULL-DELIVERY-v1
PLAN_VERSION=1
BASELINE_COMMIT=9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b
SCOPE=n8nagents-full-delivery-v1
SCOPE_HASH=d95736bc4ecf4be0db63a58ce2dee9abda7f555b6d8ddf6ba5769f87393f1732
SWAP_OPTION=plaintext-2g
MAX_RETRIES_PER_GATE=2
DEEPSEEK_TEST_BUDGET_USD=5
TELEGRAM_TEST_MESSAGE_LIMIT=20
EOF
chown root:root "$plan_tmp"
chmod 0400 "$plan_tmp"
ln "$plan_tmp" "$plan_record"
rm -f "$plan_tmp"
plan_tmp=
chattr +i "$plan_record"
test "$(stat -c %U:%G:%a "$plan_root")" = root:root:700
test ! -L "$plan_root"
test ! -L "$plan_record"
test "$(stat -c %U:%G:%a "$plan_record")" = root:root:400
plan_lsattr=$(lsattr -d -- "$plan_record") || exit 3
case "$plan_lsattr" in *"
"*) exit 3 ;; esac
plan_attributes=${plan_lsattr%% *}
plan_rendered_path=${plan_lsattr#* }
test "$plan_rendered_path" = "$plan_record"
case "$plan_attributes" in *i*) ;; *) exit 3 ;; esac
trap - EXIT HUP INT TERM
```

Every mutation session must validate all ten fields with an exact-schema parser: blank, missing, duplicate, unknown, or mismatched fields stop execution. Old `/root/n8nagents-approvals/*.approved` records are retained as historical evidence only and are never authorization inputs. The envelope fixes plaintext 2 GiB swap, at most two retries per gate, a total DeepSeek test budget of USD 5, and at most twenty Telegram test messages to the single manually confirmed allowlisted test chat. A new recipient, data class, production/personal data, extra spend, or extra message requires separate explicit authorization. A specific release is authorized only by its separate immutable ledger entry and external independent-review artifact; the envelope alone cannot authorize code.

## Entry gates and stop conditions

Before mutation, recheck: Ubuntu 26.04/kernel 7.0, 2 vCPU, at least 1,610,612,736 bytes of installed RAM, 25 GiB free disk, UTC/NTP, outbound DNS/HTTPS, only SSH listening, ports 80/443/5678/5432 free, and `/opt` and `/srv` still empty, and Docker/Compose/application services still absent. The RAM admission is deliberately based on `MemTotal`, not reclaimable memory: 1,342,177,280 bytes of bootstrap container limits plus a 268,435,456-byte host reserve. Capture `MemAvailable` as evidence only; it is not an entry admission threshold. Require exactly `dpkg --print-architecture = amd64` and `uname -m = x86_64`; any other result stops Phase A.

Also require a tested provider-console recovery path and the expected client authorization public-key fingerprint. The server SSH host key remains the user's explicitly accepted and pinned TOFU identity; it is **not** independently verified. Provider firewall and IPv6 policy are deferred for Phase A without being weakened because it adds no public host listener: Caddy is default-off behind `public-edge`, while bootstrap n8n binds only `127.0.0.1:5678`. Both policies become mandatory gates before any later public edge. Do not change SSH root access, install a host firewall, or enable Caddy. Stop on any fact drift, unsupported Docker apt repository/candidate, wrong pinned host key, unexpected file/service/data, package/digest/platform mismatch, public 5678/5432, failed migration/health/static check, secret output, swap failure or memory pressure.

The approved envelope fixes a plaintext 2 GiB swapfile; it can persist sensitive pages, and changing that choice requires a new plan authorization rather than an executor override. Bootstrap limits are 512 MiB/0.75 CPU/200 PIDs for PostgreSQL and 768 MiB/1.25 CPU/300 PIDs for n8n, with a 512 MiB Node heap. A health/OOM failure is a stop signal, not permission to silently raise limits.

## Exact touched objects

- `/swapfile`, one `/etc/fstab` entry, and collision-safe immutable `/root/n8nagents-phase-a-state.XXXXXXXX/{fstab.before,state}`.
- Fixed plan envelope `/root/n8nagents-governance/N8NAgents-FULL-DELIVERY-v1.plan`, external independent-review artifacts under root-owned mode-`0700` `/root/n8nagents-review-artifacts/`, and collision-safe immutable release entries under root-owned mode-`0700` `/root/n8nagents-release-ledger/`.
- Official Docker key/source files under `/etc/apt/keyrings/docker.asc` and `/etc/apt/sources.list.d/docker.sources`; exact pinned Docker packages; `docker.service`/`containerd.service`.
- Login `deploy-n8n`, its home/authorized key, root-owned `/usr/local/sbin/n8nagents-phase-a`, `/etc/sudoers.d/deploy-n8n-phase-a`, and empty root-owned `/var/lib/n8nagents-phase-a/{home,docker}`. The user is never added to the root-equivalent `docker` group.
- Root-owned releases `/opt/n8n-stack/releases/<UTC>-<git-sha>` containing only directories and single-link regular files; `/opt/n8n-stack/current` is the sole permitted symlink and is outside a release tree. The root-only `/opt/n8n-stack/shared/.env` is mode `0600` and a single-link regular file.
- Compose project `n8nagents`: internal containers `postgres`,`n8n`; networks `edge`,`data` (`data` internal); volumes `postgres_data`,`n8n_data`,`n8n_files`. No Caddy container/volume is required in Phase A.

## Root preflight and reversible swap

Run from a fresh provider-console-capable root session; do not enable shell tracing:

```sh
set -eu
test "$(id -u)" -eq 0
plan_record=/root/n8nagents-governance/N8NAgents-FULL-DELIVERY-v1.plan
test ! -L "$(dirname "$plan_record")"
test ! -L "$plan_record"
test "$(stat -c %U:%G:%a "$(dirname "$plan_record")")" = root:root:700
test "$(stat -c %U:%G:%a "$plan_record")" = root:root:400
plan_lsattr=$(lsattr -d -- "$plan_record") || exit 3
case "$plan_lsattr" in *"
"*) exit 3 ;; esac
plan_attributes=${plan_lsattr%% *}
plan_rendered_path=${plan_lsattr#* }
test "$plan_rendered_path" = "$plan_record"
case "$plan_attributes" in *i*) ;; *) exit 3 ;; esac
awk -F= '
BEGIN {
  expected["STATUS"]="APPROVED"; expected["AUTHORIZATION_ID"]="N8NAgents-FULL-DELIVERY-v1"; expected["PLAN_VERSION"]="1"
  expected["BASELINE_COMMIT"]="9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b"; expected["SCOPE"]="n8nagents-full-delivery-v1"
  expected["SCOPE_HASH"]="d95736bc4ecf4be0db63a58ce2dee9abda7f555b6d8ddf6ba5769f87393f1732"
  expected["SWAP_OPTION"]="plaintext-2g"; expected["MAX_RETRIES_PER_GATE"]="2"
  expected["DEEPSEEK_TEST_BUDGET_USD"]="5"; expected["TELEGRAM_TEST_MESSAGE_LIMIT"]="20"
}
{
  if ($0=="" || index($0,"=")==0) exit 2
  key=$1; value=substr($0,index($0,"=")+1)
  if (!(key in expected) || seen[key]++ || value != expected[key]) exit 3
}
END {if (NR != 10) exit 4; for (key in expected) if (!seen[key]) exit 5}
' "$plan_record"
swap_option=plaintext-2g
grep -qx 'ID=ubuntu' /etc/os-release
grep -qx 'VERSION_ID="26.04"' /etc/os-release
test "$(dpkg --print-architecture)" = amd64
test "$(uname -m)" = x86_64
test "$(nproc)" -eq 2
test "$(findmnt -n -o AVAIL -b /)" -ge 26843545600
container_total_bytes=1342177280
host_reserve_bytes=268435456
required_memtotal_bytes=$((container_total_bytes + host_reserve_bytes))
test "$required_memtotal_bytes" -eq 1610612736
memtotal_kib=$(awk '/^MemTotal:/{print $2}' /proc/meminfo)
test -n "$memtotal_kib"
test $((memtotal_kib * 1024)) -ge "$required_memtotal_bytes"
memavailable_kib=$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)
test -n "$memavailable_kib"
printf 'EVIDENCE_PRE_SWAP_MEMAVAILABLE_KIB=%s\n' "$memavailable_kib"
test "$(timedatectl show -p NTPSynchronized --value)" = yes
test "$(date +%z)" = +0000
test -r /usr/share/zoneinfo/Etc/UTC
cmp -s /etc/localtime /usr/share/zoneinfo/Etc/UTC
psi_memory_full_avg10() {
  awk '/^full / {for (i = 1; i <= NF; i++) if ($i ~ /^avg10=/) {split($i, pair, "="); print pair[2]; exit}}' /proc/pressure/memory
}
oom_kill_before_phase_a=$(awk '/^oom_kill / {print $2}' /proc/vmstat)
test -n "$oom_kill_before_phase_a"
test "$(psi_memory_full_avg10)" = 0.00
case "$swap_option" in
  plaintext-2g)
    test -z "$(swapon --show --noheadings)"
    test ! -e /swapfile
    if awk '$0 !~ /^[[:space:]]*#/ && $1=="/swapfile" && $3=="swap" {found=1} END{exit !found}' /etc/fstab; then exit 3; fi
    command -v chattr >/dev/null
    umask 077
    state_dir=$(mktemp -d /root/n8nagents-phase-a-state.XXXXXXXX)
    fstab_snapshot="$state_dir/fstab.before"
    state_record="$state_dir/state"
    install -o root -g root -m 0400 /etc/fstab "$fstab_snapshot"
    printf 'FSTAB_SNAPSHOT=%s\nSWAPFILE=/swapfile\nFSTAB_ENTRY=/swapfile none swap sw 0 0\nSWAP_OPTION=%s\n' "$fstab_snapshot" "$swap_option" >"$state_record"
    chmod 0400 "$state_record"
    chattr +i "$fstab_snapshot" "$state_record" "$state_dir"
    fallocate -l 2G /swapfile
    chmod 0600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    printf '%s\n' '/swapfile none swap sw 0 0' >>/etc/fstab
    awk '$0 !~ /^[[:space:]]*#/ && $1=="/swapfile" && $2=="none" && $3=="swap" && $4=="sw" && $5==0 && $6==0 {found=1} END{exit !found}' /etc/fstab
    test "$(stat -c %s /swapfile)" -eq 2147483648
    test "$(stat -c %a /swapfile)" = 600
    swap_names=$(LC_ALL=C swapon --show=NAME --noheadings --raw)
    test "$swap_names" = /swapfile
    swap_total_kib=$(awk '/^SwapTotal:/{print $2}' /proc/meminfo)
    swap_page_slack_kib=$(( $(getconf PAGESIZE) / 1024 ))
    test -n "$swap_total_kib"
    test "$swap_total_kib" -ge $((2097152 - swap_page_slack_kib))
    test "$(awk '/^oom_kill / {print $2}' /proc/vmstat)" = "$oom_kill_before_phase_a"
    test "$(psi_memory_full_avg10)" = 0.00
    printf 'Record this exact rollback state path in redacted evidence: %s\n' "$state_dir"
    ;;
  *) exit 3 ;;
esac
```

Before these commands, independently verify listeners, outbound HTTPS, paths, package absence, architecture, console and public-key fingerprint. The preflight commands above are the required NTP/UTC, memory, OOM and PSI evidence. Any mismatch stops the plan.

## Official Docker repository and exact candidates

Use the official Ubuntu repository only. Verify its current signing fingerprint against Docker's official installation page at execution time; expected candidate fingerprint is `9DC858229FC7DD38854AE2D88D81803C0EBFCD88`. Do not `apt upgrade`:

```sh
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod 0644 /etc/apt/keyrings/docker.asc
test "$(gpg --show-keys --with-colons /etc/apt/keyrings/docker.asc | awk -F: '$1=="fpr"{print $10; exit}')" = 9DC858229FC7DD38854AE2D88D81803C0EBFCD88
. /etc/os-release
printf 'Types: deb\nURIs: https://download.docker.com/linux/ubuntu\nSuites: %s\nComponents: stable\nSigned-By: /etc/apt/keyrings/docker.asc\n' "$VERSION_CODENAME" >/etc/apt/sources.list.d/docker.sources
apt-get update
docker_ce_version=$(apt-cache madison docker-ce | awk '$3 ~ /^5:29[.]7[.]2-/ {print $3; exit}')
compose_version=$(apt-cache madison docker-compose-plugin | awk '$3 ~ /^5[.]5[.]0-/ {print $3; exit}')
test -n "$docker_ce_version" && test -n "$compose_version"
containerd_version=$(apt-cache policy containerd.io | awk '/Candidate:/{print $2}')
buildx_version=$(apt-cache policy docker-buildx-plugin | awk '/Candidate:/{print $2}')
test "$containerd_version" != '(none)' && test "$buildx_version" != '(none)'
apt-get install -y docker-ce="$docker_ce_version" docker-ce-cli="$docker_ce_version" containerd.io="$containerd_version" docker-buildx-plugin="$buildx_version" docker-compose-plugin="$compose_version"
test "$(docker version --format '{{.Server.Version}}')" = 29.7.2
test "$(docker compose version --short)" = 5.5.0
systemctl is-active --quiet docker
```

Capture all five resolved package versions in execution evidence. Stop if exact Engine/Compose candidates are absent; do not substitute versions.

## Dedicated login gate

Create `deploy-n8n` with no Docker-group membership. Copy only the already verified single client public-key line and set its ownership/modes:

```sh
test "$(awk 'NF && $1 !~ /^#/{n++} END{print n+0}' /root/.ssh/authorized_keys)" -eq 1
useradd --create-home --shell /bin/bash deploy-n8n
install -d -o deploy-n8n -g deploy-n8n -m 0700 /home/deploy-n8n/.ssh
install -o deploy-n8n -g deploy-n8n -m 0600 /root/.ssh/authorized_keys /home/deploy-n8n/.ssh/authorized_keys
```

The `authorized_keys` copy is allowed only after proving the source has exactly the intended verified key; otherwise stop and install the single matched line rather than copying the file.

Before installing any sudo privilege or starting deployment, retain the root/console session and prove a separate `ssh deploy-n8n@host` login using the user-accepted pinned TOFU host key. Verify `id deploy-n8n` and that `id -nG deploy-n8n` does not contain `docker` or `sudo`. Failure stops all further work.

## Versioned release, secrets and digests

From the repository root on the operator workstation, use the reviewed packaging gate below with PowerShell 7.4 or later. It resolves the full commit object, uses the full `N8NAgents` pathspec while preserving that top-level prefix, fixes LF conversion/modes/mtime independently of workstation Git defaults, and proves every regular archive member byte-for-byte against its raw Git blob. The archive output must be a unique, non-existing path outside the repository. The gate validates a private same-parent staging file, then publishes it with one atomic no-overwrite move. Pathspec-dot, tree-ish-subtree, shell-pipeline and redirected-stdout archive forms are prohibited.

```powershell
$reviewedGitSha = '<independently-reviewed-full-40-character-git-sha>'
$archive = 'C:\phase-a-transfer\n8nagents-<unique-release-id>.tar.gz'
if (Test-Path -LiteralPath $archive) { throw 'archive path must be unique' }
$packageEvidence = @(& .\N8NAgents\scripts\package-reviewed-release.ps1 `
    -ReviewedCommit $reviewedGitSha -OutputPath $archive)
$packageEvidence
```

Record every emitted local field: `PACKAGE_COMMIT`, `PACKAGE_MTIME_EPOCH`, `ARCHIVE_SHA256`, `ARCHIVE_SIZE`, `ARCHIVE_ENTRY_COUNT`, `ARCHIVE_REGULAR_FILE_COUNT`, `ARCHIVE_SYMLINK_COUNT`, `ARCHIVE_REGULAR_CONTENT_SHA256`, `RELEASE_TREE_SHA256`, `TOUCHSET_SHA256`, `SCOPE_HASH`, `STATIC_STATUS`, `STATIC_EVIDENCE_SHA256`, `ARCHIVE_ALL_REGULAR_MEMBERS_VERIFIED`, `PHASE_A_WRAPPER_BLOB_ID`, `PHASE_A_WRAPPER_SHA256`, and `PHASE_A_WRAPPER_SIZE`. They are redacted packaging evidence and contain no environment values or secrets. Two clean runs for the exact full SHA must produce identical archive SHA-256, size, tree hash, touchset hash, scope hash, and static-evidence hash. Transfer one exact archive to `/srv`; do not rebuild it on the server.

Before a remote prewrite gate, run the offline labelled fixture `sh N8NAgents/scripts/test-remote-package-gate.sh`. It performs separate hash, size, archive-type, extract, zero-CR, target-shell and governance checks, emits only `STEP=... STATUS=... RC=...` plus stderr hash/size, and cleans only its own temporary directory. Do not replace these checks with an unlabeled shell chain or expose command stderr in evidence.

The only production-equivalent remote publisher is the reviewed root-only runner `infra/phase-a-release-gate.sh`, installed as `/usr/local/sbin/n8nagents-phase-a-release-gate` from the independently reviewed commit before the transfer is accepted. Record its Git blob ID and SHA-256 in the review artifact; a different runner is a STOP. It labels `PUBLISH_ARCHIVE`, hash, size, type, regular-content, wrapper, extract/normalize, governance, activation and cleanup with `START`, `PASS` or `FAIL` plus `RC`. It emits hashes and sizes of captured stderr only, never stderr. The failure harness injects `EXTRACT` failure and proves that no later step starts and cleanup is still labelled.

The transfer source is a unique `/srv/.incoming-*` regular file. The runner reads it exactly once to make a root-owned, root-group, `0400`, single-link staging inode, publishes with `ln` only if the final `/srv/n8nagents-<release-id>.tar.gz` does not exist, drops the staging link, and from then on validates and extracts only that final `0400` root-private inode. A collision is a STOP. The runner checks `/proc/self/mountinfo` before every recursive ownership or mode change; this catches same-filesystem bind mounts which `st_dev` alone misses. It rejects all symlinks, specials and hard links in the extracted tree, then requires directories `0755`, `*.sh` `0755`, and all other regular files `0644` before governance and activation.

Run it only from a retained root/console session, after the independent `GO` artifact and ledger have been created as described below. Substitute the recorded evidence literally; do not use shell interpolation, an archive rebuilt on the server, or an existing destination path.

```sh
/usr/local/sbin/n8nagents-phase-a-release-gate \
  /srv/.incoming-n8nagents-<unique-release-id>.tar.gz \
  '<YYYYMMDDTHHMMSSZ>-<independently-reviewed-40-character-git-sha>' \
  '<local-PACKAGE_COMMIT>' '<local-ARCHIVE_SHA256>' '<local-ARCHIVE_SIZE>' \
  '<local-ARCHIVE_ENTRY_COUNT>' '<local-ARCHIVE_REGULAR_FILE_COUNT>' \
  '<local-ARCHIVE_REGULAR_CONTENT_SHA256>' '<local-RELEASE_TREE_SHA256>' \
  '<local-TOUCHSET_SHA256>' '<local-SCOPE_HASH>' '<local-STATIC_STATUS>' \
  '<local-STATIC_EVIDENCE_SHA256>' '<local-PHASE_A_WRAPPER_SHA256>' \
  '<local-PHASE_A_WRAPPER_SIZE>'
```

The historical shell fragment below is retained as a review specification for its field-level checks only. It is deliberately non-runnable and must not be copied, adapted or executed: the labelled runner above replaces it.

Before creating or extracting a release directory, copy the local evidence into the expected values below. The remote archive hash/size, safe prefixed listing, entry/type/mode counts, every regular member's aggregate hash, streamed wrapper hash/size/zero-CR check, and target `/bin/sh -n` parse must all pass. Only then strip the single `N8NAgents` prefix and extract without owner preservation into `/opt/n8n-stack/releases/<UTC>-<git-sha>`. Make the tree `root:root`, directories `0755`, ordinary files `0644`, intended scripts `0755`; atomically point `/opt/n8n-stack/current` at it. Keep previous releases.

```sh
stack_root=/opt/n8n-stack
release_id='<YYYYMMDDTHHMMSSZ>-<independently-reviewed-40-character-git-sha>'
archive="/srv/n8nagents-$release_id.tar.gz"
expected_package_commit='<local-PACKAGE_COMMIT>'
expected_archive_sha256='<local-ARCHIVE_SHA256>'
expected_archive_size='<local-ARCHIVE_SIZE>'
expected_archive_entry_count='<local-ARCHIVE_ENTRY_COUNT>'
expected_archive_regular_file_count='<local-ARCHIVE_REGULAR_FILE_COUNT>'
expected_archive_symlink_count='<local-ARCHIVE_SYMLINK_COUNT>'
expected_regular_content_sha256='<local-ARCHIVE_REGULAR_CONTENT_SHA256>'
expected_release_tree_sha256='<local-RELEASE_TREE_SHA256>'
expected_touchset_sha256='<local-TOUCHSET_SHA256>'
expected_scope_hash='<local-SCOPE_HASH>'
expected_static_status='<local-STATIC_STATUS>'
expected_static_evidence_sha256='<local-STATIC_EVIDENCE_SHA256>'
expected_wrapper_sha256='<local-PHASE_A_WRAPPER_SHA256>'
expected_wrapper_size='<local-PHASE_A_WRAPPER_SIZE>'
# Historical, non-runnable specification fragment.  The labelled runner above
# is mandatory; fail closed if this fragment is pasted into a shell.
exit 3
case "$release_id" in *-"$expected_package_commit") ;; *) exit 3 ;; esac
printf '%s\n' "$release_id" | grep -Eq '^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{40}$'
case "$expected_archive_sha256:$expected_regular_content_sha256:$expected_release_tree_sha256:$expected_touchset_sha256:$expected_scope_hash:$expected_static_evidence_sha256:$expected_wrapper_sha256" in *[!0-9a-f:]*|*:|:*) exit 3 ;; esac
test "${#expected_archive_sha256}" -eq 64
test "${#expected_regular_content_sha256}" -eq 64
test "${#expected_release_tree_sha256}" -eq 64
test "${#expected_touchset_sha256}" -eq 64
test "${#expected_scope_hash}" -eq 64
test "${#expected_static_evidence_sha256}" -eq 64
test "${#expected_wrapper_sha256}" -eq 64
test "$expected_scope_hash" = d95736bc4ecf4be0db63a58ce2dee9abda7f555b6d8ddf6ba5769f87393f1732
test "$expected_static_status" = PASS
case "$expected_archive_size:$expected_archive_entry_count:$expected_archive_regular_file_count:$expected_archive_symlink_count:$expected_wrapper_size" in *[!0-9:]*|*:|:*) exit 3 ;; esac
test "$expected_archive_symlink_count" -eq 0
test -f "$archive"
test ! -L "$archive"
remote_archive_sha256=$(sha256sum "$archive" | awk '{print $1}')
test "$remote_archive_sha256" = "$expected_archive_sha256"
test "$(stat -c %s "$archive")" = "$expected_archive_size"
test "$(stat -c %h "$archive")" = 1
remote_archive_listing=
remote_archive_verbose=
remote_regular_manifest=
remote_member_tmp=
remote_wrapper_tmp=
cleanup_remote_package_gate() {
  for temporary in "$remote_archive_listing" "$remote_archive_verbose" "$remote_regular_manifest" "$remote_member_tmp" "$remote_wrapper_tmp"; do
    test -z "$temporary" || rm -f -- "$temporary"
  done
}
trap cleanup_remote_package_gate EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
remote_archive_listing=$(mktemp /srv/n8nagents-archive-listing.XXXXXXXX)
remote_archive_verbose=$(mktemp /srv/n8nagents-archive-verbose.XXXXXXXX)
remote_regular_manifest=$(mktemp /srv/n8nagents-regular-manifest.XXXXXXXX)
remote_member_tmp=$(mktemp /srv/n8nagents-member.XXXXXXXX)
remote_wrapper_tmp=$(mktemp /srv/n8nagents-phase-a-wrapper.XXXXXXXX)
tar -tzf "$archive" >"$remote_archive_listing"
tar -tvzf "$archive" >"$remote_archive_verbose"
LC_ALL=C awk '
  index($0,"\r") || $0 !~ /^N8NAgents\// || $0 ~ /(^|\/)\.\.(\/|$)/ || seen[$0]++ {exit 1}
  END {if (NR == 0) exit 1}
' "$remote_archive_listing"
remote_archive_entry_count=$(wc -l <"$remote_archive_listing" | tr -d ' ')
test "$remote_archive_entry_count" = "$expected_archive_entry_count"
remote_archive_symlink_count=$(awk 'substr($1,1,1)=="l" {count++} END {print count+0}' "$remote_archive_verbose")
remote_archive_regular_file_count=$(awk 'substr($1,1,1)=="-" {count++} END {print count+0}' "$remote_archive_verbose")
test "$remote_archive_symlink_count" = "$expected_archive_symlink_count"
test "$remote_archive_regular_file_count" = "$expected_archive_regular_file_count"
awk '$1 !~ /^(drwxr-xr-x|-rw-r--r--|-rwxr-xr-x)$/ {exit 1}' "$remote_archive_verbose"
: >"$remote_regular_manifest"
while IFS= read -r member; do
  case "$member" in */) continue ;; esac
  tar -xOf "$archive" "$member" >"$remote_member_tmp"
  member_sha256=$(sha256sum "$remote_member_tmp" | awk '{print $1}')
  member_size=$(stat -c %s "$remote_member_tmp")
  printf '%s\t%s\t%s\n' "$member_sha256" "$member_size" "$member" >>"$remote_regular_manifest"
done <"$remote_archive_listing"
remote_regular_content_sha256=$(sha256sum "$remote_regular_manifest" | awk '{print $1}')
test "$remote_regular_content_sha256" = "$expected_regular_content_sha256"
tar -xOf "$archive" N8NAgents/infra/phase-a-compose.sh >"$remote_wrapper_tmp"
remote_wrapper_sha256=$(sha256sum "$remote_wrapper_tmp" | awk '{print $1}')
remote_wrapper_size=$(stat -c %s "$remote_wrapper_tmp")
test "$remote_wrapper_sha256" = "$expected_wrapper_sha256"
test "$remote_wrapper_size" = "$expected_wrapper_size"
test "$(LC_ALL=C tr -cd '\r' <"$remote_wrapper_tmp" | wc -c)" -eq 0
/bin/sh -n "$remote_wrapper_tmp"
printf 'EVIDENCE_REMOTE_PACKAGE_COMMIT=%s\nEVIDENCE_REMOTE_ARCHIVE_SHA256=%s\nEVIDENCE_REMOTE_ARCHIVE_ENTRY_COUNT=%s\nEVIDENCE_REMOTE_REGULAR_CONTENT_SHA256=%s\nEVIDENCE_REMOTE_PHASE_A_WRAPPER_SHA256=%s\nEVIDENCE_REMOTE_PHASE_A_WRAPPER_SIZE=%s\n' \
  "$expected_package_commit" "$remote_archive_sha256" "$remote_archive_entry_count" "$remote_regular_content_sha256" "$remote_wrapper_sha256" "$remote_wrapper_size"
cleanup_remote_package_gate
trap - EXIT HUP INT TERM

# An independent reviewer, not the implementer/executor, must create the canonical review
# artifact outside this host with exact REVIEW_STATUS=GO and convey its SHA-256 through the approved manual evidence channel.
# SHA-256 provides integrity binding only; this manifest does not claim a cryptographic signature.
review_root=/root/n8nagents-review-artifacts
ledger_root=/root/n8nagents-release-ledger
review_artifact="$review_root/$release_id.review"
ledger_entry="$ledger_root/$release_id.ledger"
review_source="/srv/n8nagents-review-$release_id.review"
expected_review_artifact_sha256='<independent-review-artifact-SHA256>'
case "$expected_review_artifact_sha256" in *[!0-9a-f]*|'') exit 3 ;; esac
test "${#expected_review_artifact_sha256}" -eq 64
test -f "$review_source"
test ! -L "$review_source"
test "$(stat -c %h "$review_source")" = 1
test "$(sha256sum "$review_source" | awk '{print $1}')" = "$expected_review_artifact_sha256"
awk -F= \
  -v release_sha="$expected_package_commit" \
  -v archive_sha="$expected_archive_sha256" \
  -v tree_sha="$expected_release_tree_sha256" \
  -v touchset_sha="$expected_touchset_sha256" \
  -v static_sha="$expected_static_evidence_sha256" '
function safe_id(value) { return length(value)>=3 && length(value)<=64 && value ~ /^[A-Za-z0-9][A-Za-z0-9._-]*$/ }
BEGIN {
  order[1]="AUTHORIZATION_ID"; order[2]="PHASE"; order[3]="RELEASE_GIT_SHA"; order[4]="ARCHIVE_SHA256"; order[5]="RELEASE_TREE_SHA256"; order[6]="TOUCHSET_SHA256"
  order[7]="IMPLEMENTER_ID"; order[8]="REVIEWER_ID"; order[9]="STATIC_STATUS"; order[10]="STATIC_EVIDENCE_SHA256"; order[11]="REVIEW_STATUS"; order[12]="REVIEW_ROLE"; order[13]="TIMESTAMP_UTC"
  expected["AUTHORIZATION_ID"]="N8NAgents-FULL-DELIVERY-v1"; expected["PHASE"]="phase-a-internal"; expected["RELEASE_GIT_SHA"]=release_sha
  expected["ARCHIVE_SHA256"]=archive_sha; expected["RELEASE_TREE_SHA256"]=tree_sha; expected["TOUCHSET_SHA256"]=touchset_sha
  expected["STATIC_STATUS"]="PASS"; expected["STATIC_EVIDENCE_SHA256"]=static_sha
  expected["REVIEW_STATUS"]="GO"; expected["REVIEW_ROLE"]="independent-release-reviewer"
}
{
  if ($0=="" || index($0,"=")==0) exit 2
  key=$1; value=substr($0,index($0,"=")+1)
  if (key != order[NR] || (key != "IMPLEMENTER_ID" && key != "REVIEWER_ID" && key != "TIMESTAMP_UTC" && !(key in expected)) || seen[key]++) exit 3
  if (key in expected && value != expected[key]) exit 4
  if ((key=="IMPLEMENTER_ID" || key=="REVIEWER_ID") && !safe_id(value)) exit 5
  if (key=="IMPLEMENTER_ID") implementer=value
  if (key=="REVIEWER_ID") reviewer=value
  if (key=="TIMESTAMP_UTC" && value !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$/) exit 6
}
END {if (NR!=13 || implementer==reviewer) exit 7; for (key in expected) if (!seen[key]) exit 8}
' "$review_source"
implementer_id=$(awk -F= '$1=="IMPLEMENTER_ID" {print substr($0,index($0,"=")+1)}' "$review_source")
reviewer_id=$(awk -F= '$1=="REVIEWER_ID" {print substr($0,index($0,"=")+1)}' "$review_source")
review_timestamp_utc=$(awk -F= '$1=="TIMESTAMP_UTC" {print substr($0,index($0,"=")+1)}' "$review_source")
test "$implementer_id" != "$reviewer_id"
test "$(date -u -d "$review_timestamp_utc" '+%Y-%m-%dT%H:%M:%SZ')" = "$review_timestamp_utc"

install -d -o root -g root -m 0700 "$review_root" "$ledger_root"
test ! -e "$review_artifact"
test ! -e "$ledger_entry"
review_tmp=$(mktemp "$review_root/.$release_id.XXXXXXXX")
ledger_tmp=$(mktemp "$ledger_root/.$release_id.XXXXXXXX")
cleanup_governance_tmp() {
  test -z "${review_tmp:-}" || rm -f -- "$review_tmp"
  test -z "${ledger_tmp:-}" || rm -f -- "$ledger_tmp"
}
trap cleanup_governance_tmp EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
install -o root -g root -m 0400 "$review_source" "$review_tmp"
test "$(sha256sum "$review_tmp" | awk '{print $1}')" = "$expected_review_artifact_sha256"
ln "$review_tmp" "$review_artifact"
rm -f "$review_tmp"
review_tmp=
chattr +i "$review_artifact"
cat >"$ledger_tmp" <<EOF
AUTHORIZATION_ID=N8NAgents-FULL-DELIVERY-v1
PHASE=phase-a-internal
RELEASE_GIT_SHA=$expected_package_commit
ARCHIVE_SHA256=$expected_archive_sha256
RELEASE_TREE_SHA256=$expected_release_tree_sha256
TOUCHSET_SHA256=$expected_touchset_sha256
IMPLEMENTER_ID=$implementer_id
REVIEWER_ID=$reviewer_id
REVIEW_STATUS=GO
REVIEW_ROLE=independent-release-reviewer
REVIEW_ARTIFACT_SHA256=$expected_review_artifact_sha256
STATIC_STATUS=PASS
STATIC_EVIDENCE_SHA256=$expected_static_evidence_sha256
TIMESTAMP_UTC=$review_timestamp_utc
EOF
chown root:root "$ledger_tmp"
chmod 0400 "$ledger_tmp"
ln "$ledger_tmp" "$ledger_entry"
rm -f "$ledger_tmp"
ledger_tmp=
chattr +i "$ledger_entry"
test "$(stat -c %U:%G:%a "$review_root")" = root:root:700
test "$(stat -c %U:%G:%a "$ledger_root")" = root:root:700
test ! -L "$review_artifact"
test ! -L "$ledger_entry"
test "$(stat -c %U:%G:%a "$review_artifact")" = root:root:400
test "$(stat -c %U:%G:%a "$ledger_entry")" = root:root:400
assert_immutable_record() {
  immutable_record=$1
  immutable_lsattr=$(lsattr -d -- "$immutable_record") || exit 3
  case "$immutable_lsattr" in *"
"*) exit 3 ;; esac
  immutable_attributes=${immutable_lsattr%% *}
  immutable_rendered_path=${immutable_lsattr#* }
  test "$immutable_rendered_path" = "$immutable_record"
  case "$immutable_attributes" in *i*) ;; *) exit 3 ;; esac
}
assert_immutable_record "$review_artifact"
assert_immutable_record "$ledger_entry"
trap - EXIT HUP INT TERM

install -d -o root -g root -m 0755 "$stack_root/releases" "$stack_root/shared"
release="$stack_root/releases/$release_id"
test ! -e "$release"
install -d -o root -g root -m 0755 "$release"
tar --no-same-owner --strip-components=1 -xzf "$archive" -C "$release"
release_type_violation=$(find "$release" -xdev -mindepth 1 ! \( -type d -o -type f \) -print -quit)
test -z "$release_type_violation"
release_device=$(stat -c %d "$release")
release_devices=$(find "$release" -xdev -mindepth 1 -printf '%D\n')
for release_device_candidate in $release_devices; do test "$release_device_candidate" = "$release_device"; done
release_hardlink_violation=$(find "$release" -xdev -type f ! -links 1 -print -quit)
test -z "$release_hardlink_violation"
chown -R root:root "$release"
find "$release" -type d -exec chmod 0755 {} +
find "$release" -type f -exec chmod 0644 {} +
find "$release" -type f -name '*.sh' -exec chmod 0755 {} +
install -d -o root -g root -m 0700 /var/lib/n8nagents-phase-a/home /var/lib/n8nagents-phase-a/docker
test -z "$(find /var/lib/n8nagents-phase-a/docker -mindepth 1 -maxdepth 1 -print -quit)"
/bin/sh "$release/infra/verify-release-governance.sh" \
  "$release" \
  /root/n8nagents-governance/N8NAgents-FULL-DELIVERY-v1.plan \
  /root/n8nagents-release-ledger \
  /root/n8nagents-review-artifacts \
  /var/lib/n8nagents-phase-a/home \
  0:0 \
  /srv \
  yes \
  -
ln -s "$release" "$stack_root/current.next"
mv -Tf "$stack_root/current.next" "$stack_root/current"
```

Pull only `docker.n8n.io/n8nio/n8n:2.36.7` and `postgres:17.11-alpine3.24`; obtain each `RepoDigest`, require `@sha256:`, and construct the exact `tag@sha256:digest` values. Record platform, pull UTC time and digest in the inventory/evidence. Caddy is neither pulled nor started in Phase A.

```sh
n8n_tag=docker.n8n.io/n8nio/n8n:2.36.7
postgres_tag=postgres:17.11-alpine3.24
docker pull "$n8n_tag"
docker pull "$postgres_tag"
test "$(docker image inspect --format '{{.Os}}' "$n8n_tag")" = linux
test "$(docker image inspect --format '{{.Architecture}}' "$n8n_tag")" = amd64
test "$(docker image inspect --format '{{.Os}}' "$postgres_tag")" = linux
test "$(docker image inspect --format '{{.Architecture}}' "$postgres_tag")" = amd64
n8n_repo_digest=$(docker image inspect --format '{{index .RepoDigests 0}}' "$n8n_tag")
postgres_repo_digest=$(docker image inspect --format '{{index .RepoDigests 0}}' "$postgres_tag")
case "$n8n_repo_digest" in *@sha256:*) ;; *) exit 5 ;; esac
case "$postgres_repo_digest" in *@sha256:*) ;; *) exit 5 ;; esac
n8n_image="$n8n_tag@${n8n_repo_digest##*@}"
postgres_image="$postgres_tag@${postgres_repo_digest##*@}"
```

Create `/opt/n8n-stack/shared/.env` as `root:root` mode `0600`, with shell tracing disabled. It contains the two resolved image references, independently generated server-side n8n/DB secrets, `TIMEZONE=UTC`, localhost bootstrap URLs, `N8N_PROXY_HOPS=1`, and harmless reserved public placeholders (`localhost`, `.invalid`). No value is printed, passed in argv, copied to chat or committed. The bootstrap override changes protocol to HTTP and proxy hops to `0` only inside the localhost listener.

```sh
set +x
umask 077
env_tmp=$(mktemp "$stack_root/shared/.env.XXXXXX")
{
  printf 'EDITOR_DOMAIN=localhost\nWEBHOOK_DOMAIN=hooks.invalid\nACME_EMAIL=unused@example.invalid\n'
  printf 'TIMEZONE=UTC\nN8N_WEBHOOK_URL=http://127.0.0.1:5678/\nN8N_EDITOR_BASE_URL=http://127.0.0.1:5678/\nN8N_PROXY_HOPS=1\n'
  printf 'N8N_IMAGE=%s\nPOSTGRES_IMAGE=%s\n' "$n8n_image" "$postgres_image"
  printf 'N8N_ENCRYPTION_KEY='; openssl rand -hex 32
  printf 'POSTGRES_ADMIN_PASSWORD='; openssl rand -hex 32
  printf 'N8N_DB_PASSWORD='; openssl rand -hex 32
  printf 'ASSISTANT_DB_PASSWORD='; openssl rand -hex 32
  printf 'MEMORY_DB_PASSWORD='; openssl rand -hex 32
} >"$env_tmp"
install -o root -g root -m 0600 "$env_tmp" "$stack_root/shared/.env"
rm -f "$env_tmp"
test "$(stat -c '%U:%G:%a' "$stack_root/shared/.env")" = root:root:600
```

## Minimal privileged wrapper

Only after the second SSH login, root-owned release and `.env` gates pass, install the reviewed wrapper, empty root-only Docker environment and sudo rule. The wrapper accepts one allowlisted action, hard-codes both Compose files/project/socket/context, and launches Docker under `env -i`; it never accepts caller Docker config, plugin paths or pass-through arguments.

```sh
install -d -o root -g root -m 0700 /var/lib/n8nagents-phase-a/home /var/lib/n8nagents-phase-a/docker
test -z "$(find /var/lib/n8nagents-phase-a/docker -mindepth 1 -maxdepth 1 -print -quit)"
install -o root -g root -m 0755 /opt/n8n-stack/current/infra/phase-a-compose.sh /usr/local/sbin/n8nagents-phase-a
printf '%s\n' \
  'Defaults:deploy-n8n env_reset' \
  'Defaults:deploy-n8n !setenv' \
  'Defaults:deploy-n8n secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"' \
  'deploy-n8n ALL=(root) NOPASSWD:NOSETENV: /usr/local/sbin/n8nagents-phase-a' \
  >/etc/sudoers.d/deploy-n8n-phase-a
chmod 0440 /etc/sudoers.d/deploy-n8n-phase-a
visudo -cf /etc/sudoers.d/deploy-n8n-phase-a
/bin/sh -n /usr/local/sbin/n8nagents-phase-a
```

From the already-tested second `deploy-n8n` session, run `sudo -n /usr/local/sbin/n8nagents-phase-a config`. Require exit 0 before any privileged deployment action; retain the original root/console session.

## Internal start and owner gate

Run through the allowlisted wrapper:

```sh
sudo -n /usr/local/sbin/n8nagents-phase-a config
sudo -n /usr/local/sbin/n8nagents-phase-a pull-internal
sudo -n /usr/local/sbin/n8nagents-phase-a up-internal
sudo -n /usr/local/sbin/n8nagents-phase-a ps
```

Require healthy PostgreSQL sentinel/grants and healthy n8n. Verify host listeners show only SSH publicly and `127.0.0.1:5678` locally; 5432, 80 and 443 remain unbound. From the operator workstation:

After health is first reported, retain the root/console session and collect two admission samples 30 seconds apart before proceeding to the owner step. Each sample must prove at least 131,072 KiB `MemAvailable` evidence, `memory/full` PSI `avg10=0.00`, the unchanged host `oom_kill` counter captured before Phase A, and at least 1,048,576 KiB `SwapFree` for the envelope-fixed plaintext 2 GiB swap. Both Phase A containers must remain healthy, have `OOMKilled=false`, and have `RestartCount=0`. Any failure stops Phase A; do not raise a memory, CPU, PID or Node heap limit to continue.

```sh
phase_a_release=$(/usr/bin/readlink -f "$stack_root/current")
case "$phase_a_release" in "$stack_root"/releases/*) ;; *) exit 3 ;; esac
test -f "$phase_a_release/infra/compose.yaml"
test -f "$phase_a_release/infra/compose.bootstrap.yaml"
test "$(stat -c %U:%G:%a "$stack_root/shared/.env")" = root:root:600
/bin/sh "$phase_a_release/infra/verify-release-governance.sh" \
  "$phase_a_release" \
  /root/n8nagents-governance/N8NAgents-FULL-DELIVERY-v1.plan \
  /root/n8nagents-release-ledger \
  /root/n8nagents-review-artifacts \
  /var/lib/n8nagents-phase-a/home \
  0:0 \
  /srv \
  yes \
  -
swap_option=plaintext-2g
phase_a_docker() {
  /usr/bin/env -i \
    PATH=/usr/sbin:/usr/bin:/sbin:/bin HOME=/var/lib/n8nagents-phase-a/home \
    DOCKER_HOST=unix:///var/run/docker.sock DOCKER_CONTEXT=default DOCKER_CONFIG=/var/lib/n8nagents-phase-a/docker \
    /usr/bin/docker "$@"
}
phase_a_compose() {
  phase_a_docker compose --project-name n8nagents \
    --project-directory "$phase_a_release" \
    --env-file "$stack_root/shared/.env" \
    --file "$phase_a_release/infra/compose.yaml" \
    --file "$phase_a_release/infra/compose.bootstrap.yaml" "$@"
}
post_start_sample() {
  sample_memavailable_kib=$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)
  test -n "$sample_memavailable_kib"
  test "$sample_memavailable_kib" -ge 131072
  test "$(psi_memory_full_avg10)" = 0.00
  test "$(awk '/^oom_kill / {print $2}' /proc/vmstat)" = "$oom_kill_before_phase_a"
  case "$swap_option" in
    plaintext-2g)
      sample_swapfree_kib=$(awk '/^SwapFree:/{print $2}' /proc/meminfo)
      test -n "$sample_swapfree_kib"
      test "$sample_swapfree_kib" -ge 1048576
      ;;
    *) exit 3 ;;
  esac
  for service in postgres n8n; do
    container_id=$(phase_a_compose ps -q "$service")
    test -n "$container_id"
    test "$(phase_a_docker inspect --format '{{.State.Health.Status}}' "$container_id")" = healthy
    test "$(phase_a_docker inspect --format '{{.State.OOMKilled}}' "$container_id")" = false
    test "$(phase_a_docker inspect --format '{{.RestartCount}}' "$container_id")" = 0
  done
}
post_start_sample
sleep 30
post_start_sample
```

```sh
ssh -N -L 5678:127.0.0.1:5678 deploy-n8n@approved-host
```

Open `http://127.0.0.1:5678`, create the sole owner, enable/test 2FA, then close the tunnel. Do not create Telegram/DeepSeek credentials, import/activate workflows, set a webhook or start Caddy in Phase A. Redacted proof must never include environment, headers, bodies, prompts or tokens.

## Rollback

On any application failure run only `stop-internal`; preserve `.env`, release and volumes for diagnosis. If a new release is faulty, stop internal services, repoint `current` to the previous compatible release, run `config`, and restart only with database-schema compatibility evidence. Never use `down -v`, remove volumes, drop databases, replace the encryption key or claim rollback success without health/listener checks.

Host rollback is staged: disable/stop Docker while retaining packages; lock (do not delete) `deploy-n8n`; retain release/evidence. If swap was selected, use the exact immutable state path printed and recorded by that run—never a guessed/latest path:

```sh
rollback_state='<exact-recorded-/root/n8nagents-phase-a-state.XXXXXXXX>'
test "$(stat -c %U:%G:%a "$rollback_state/fstab.before")" = root:root:400
swapoff /swapfile
install -o root -g root -m 0644 "$rollback_state/fstab.before" /etc/fstab
if awk '$0 !~ /^[[:space:]]*#/ && $1=="/swapfile" && $3=="swap" {found=1} END{exit !found}' /etc/fstab; then exit 3; fi
test -z "$(swapon --show --noheadings)"
```

Retain `/swapfile` and the immutable state directory until separate deletion approval. Package removal, user/file deletion and Docker reinstall also require separate explicit approval. Root/console access is retained throughout.

## Later public-edge prerequisites

The `public-edge` profile remains off until domains/DNS, ACME email, provider IPv4+IPv6 firewall policy, owner+2FA, Caddy digest/validation, exact webhook trust tests, workflow import/spikes and backup/restore gates pass. That is a separate GO and is outside Phase A.
<!-- SOURCE_PAYLOAD_END n8nagents-source-import-v1 -->

## Transform-aware provenance manifest

- Source snapshot: `docs/deploy-rollback-manifest.md`, uncommitted working-tree state imported against base `09824a6e...`.
- Raw source hash: `e8a484571ec3b9c7700935b601929719081a2c82f52643c3bb44b734d7a4126b`; semantics are the exact UTF-8 bytes without BOM, LF line endings, with exactly one terminal LF.
- Embedded transformed payload hash: `a6f311c294c635b681cf0daa54ecef5ff39a87603a5fa62bc22cdfd706230b8d`; extract bytes after the LF ending `SOURCE_PAYLOAD_BEGIN` through the byte before the LF preceding `SOURCE_PAYLOAD_END`.
- Forward transform contains exactly one content substitution and no redaction: `[server-discovery.md](server-discovery.md)` → `[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826|server-discovery.md]]`. Frontmatter, canonical-placement callout, payload markers and this manifest are wrappers outside the payload.
- Independent raw reconstruction: extract the transformed payload by the rule above; replace that exact wikilink with `[server-discovery.md](server-discovery.md)`; append exactly one LF; hash the resulting UTF-8 bytes. Expected SHA-256 is the raw source hash above.
- Redaction result: none required; secret/PII scan `PASS`. No absolute local source path is stored.
