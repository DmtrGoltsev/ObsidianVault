# N8NAgents — INTERNAL rollout PASS (Attempt6)

Дата фиксации: 2026-08-28 (UTC). Область: только внутренний bootstrap на VPS; публичный edge не включался.

## Итог

**PASS — exact reviewed release активирован в bootstrap mode.**

- commit: `15e14e3735d195e38d9c3d90a77976d1b0e1ad25`
- tree: `455863643a6af9cad31a8921adf04193d8c910d1`
- canonical archive SHA-256: `84f0d373ee4eeb78f4b5a60954e1e1e00f2144e6ec2d72a319396c9e1c21b6e7`
- archive size/files: `164743` bytes / `143` files
- remote incoming: `/srv/.incoming-n8nagents-20260828T072000Z-15e14e3735d195e38d9c3d90a77976d1b0e1ad25.tar.gz`
- active release: `/opt/n8n-stack/releases/20260828T072000Z-15e14e3735d195e38d9c3d90a77976d1b0e1ad25`
- current: exact active release above
- current mode: `bootstrap`; previous release empty; previous mode `none`; activation journal absent

## Integrity and admission

- archive SHA-256 verified before extraction;
- archive policy: 173 members = 143 regular files + 30 directories, no links or unsupported nodes;
- production manifest: 142 entries, aggregate SHA-256 `24dbcebd7091d780f55ffbe4cea29ec0f802c5feff05b8817ecd14da79da67a2`;
- manifest file SHA-256: `f993c1d632b2921b133f5a6b98272a6aba948629dfe9bcfa7975c2c59264924a`;
- exact modes/sizes/hashes PASS; secret scan PASS; eight exports inactive and fail-closed;
- production Compose bind contract PASS for bootstrap/maintenance/public; actual runtime binds come only from `<release>/infra` and are read-only;
- wrong-root compatibility paths absent; release remained 143 files, with no symlinks or writable files.

Перед rollout точный stopped failure container Attempt5 был удалён только после immutable inspect/mount/log evidence. Том `n8nagents_postgres_data` не удалялся и был принят как пустой двумя независимыми read-only `--network none` проверками exact pinned image. Legacy pointer/evidence, failed releases/archives и старые `releases/.env` сохранены.

## Runtime validation

- exact preflight: PASS; resource plan steady `1275068416`, reserve `402653184`, required `1677721600` bytes;
- `n8nagents-postgres-1`: running/healthy, OOM false, RestartCount 0, PostgreSQL 17.11 pinned digest;
- `n8nagents-n8n-1`: running/healthy, OOM false, RestartCount 0, n8n 2.36.7 pinned digest;
- only two containers in project; volumes: `n8nagents_postgres_data`, `n8nagents_n8n_data`, `n8nagents_n8n_files`;
- migrations `001`–`008` present and applied;
- sentinels verified: `20260826.1`, `20260828.1`, `20260828.2` with reviewed checksums;
- foundation health and required database objects PASS;
- controlled stop/start of PostgreSQL+n8n PASS: same container IDs, same PostgreSQL volume metadata, same redacted DB tuple SHA-256 `2ba6c18b597fa57263dd65705a61293eea5a9448b08a1443359e483a117291ba`;
- after controlled start both services remained healthy/OOM false/RestartCount 0;
- two final samples: MemTotal `1653048 KiB`, MemAvailable `980916–997088 KiB`, swap free `2065788 KiB`, PSI full avg10 `0.00`, OOM kill counter `0`; n8n about `316.7–316.8 MiB`, PostgreSQL about `27.1–27.4 MiB`.

## Network boundary

- n8n: only `127.0.0.1:5678`;
- PostgreSQL has no host-published port;
- ports 80/443/5432/2375/2376 closed;
- Caddy absent/stopped;
- no DNS, firewall/SSH hardening, public edge, Telegram or DeepSeek mutation was performed.

## Owner/workflow gate

n8n created a placeholder user/personal-project relation, but authoritative setup state is `userManagement.isInstanceOwnerSetUp=false`; MFA-enabled count is 0. Therefore this is **not a legitimate configured owner**. Workflow import was not performed; runtime workflow count remains 0. Eight exact inactive exports are ready in the release.

Consolidated manual gate:

1. Through an approved SSH tunnel, complete the sole n8n owner setup and enable/test 2FA.
2. Only then import all eight exact exports with explicit owner/project binding and inactive state.
3. Bind credentials, Telegram numeric allowlists/secret header, and provider settings without exposing values; complete negative/positive tests.
4. Separately complete backup/restore drill and external review.
5. Public rollout remains a separate gated operation requiring DNS, provider/firewall and IPv4+IPv6 edge evidence; it was not authorized or executed here.

## Redacted immutable evidence

- empty-volume admission: `/opt/n8n-stack/shared/evidence/20260828T071000Z-attempt6-empty-volume-admission`; `evidence.sha256` SHA-256 `d2f45e7560b512f40eb1244d7c6422f40fcd4a6115cae66a8c4fac8bd5e7708b`;
- internal PASS bundle: `/opt/n8n-stack/shared/evidence/20260828T073500Z-attempt6-internal-pass`; `SHA256SUMS` SHA-256 `7da35fe3eff28968961f4f7ccc384653ddf994aa7e5cd3bb0456bbd96e965233`;
- evidence reference addendum: `/opt/n8n-stack/shared/evidence/20260828T073800Z-attempt6-evidence-addendum`; `evidence.sha256` SHA-256 `9196cab8b3a84a782095b7ad766f67c64be528ae598d9176d4bc2443caa29091`.

Addendum preserves and corrects one blank prior-index reference in the already immutable primary PASS bundle; runtime/release state was not changed by this correction.

## Обновление Stage B

После настройки owner и 2FA восемь точных workflow были импортированы с owner/project binding и оставлены неактивными. n8n повторно запущен без reimport или изменения БД; до/после совпали entity, dependency и полный DB tuple digests. Подробности и immutable evidence: [[Доказательство_StageB_Workflows_Runtime_PASS_N8NAgents_20260828]].
