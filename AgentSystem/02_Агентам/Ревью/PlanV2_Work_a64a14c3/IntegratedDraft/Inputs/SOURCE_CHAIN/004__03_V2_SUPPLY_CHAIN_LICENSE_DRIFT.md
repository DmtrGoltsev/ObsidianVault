---
id: "n8nagents-plan-v2-supply-chain-license-drift-a64a14c3"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "supply-chain-security-architect"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники:
  - "[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
  - "[[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]"
доказательства:
  - "00_FINDINGS_BASELINE.json"
  - "01_BASELINE_AUDIT.json"
теги: ["n8nagents", "plan-v2", "supply-chain", "license", "drift", "draft"]
---

# Plan V2 — supply chain, лицензии и drift

## 0. Статус, границы и запрет на runtime-утверждения

Это проектируемый раздел полного плана V2, а не разрешение на сеть, загрузку, установку, Docker, Windows, VPS, Telegram, DeepSeek или изменение project repository. Раздел создан офлайн по каноническому V0 baseline из `114` findings и замороженным материалам V1. Он не утверждает, что какой-либо будущий URL, hash, signer, license, OCI digest, scanner database, установленный компонент, backup или rollback уже проверен.

В область входит только план A: Docker Desktop с его штатным WSL 2 backend. Отдельный пользовательский Linux-дистрибутив, VM, план B и VPS не являются fallback. Любая недоступная обязательная capability завершается `BLOCKED-CAPABILITY` и новым решением владельца.

До metadata-discovery неизвестны и намеренно не заполняются: exact Docker Desktop build/channel/installer URL/SHA-256/signer; authoritative requirements и license revisions; exact OCI tuples; tool/scanner versions и database snapshot; полный dependency/license graph. Значение `UNKNOWN` не допускает acquisition или исполнение.

## 1. Нормативные инварианты

1. Ни один installer, OCI blob, package или build material не загружается до immutable `SUPPLY_CHAIN_LOCK` для acquisition.
2. Metadata-discovery отделён от acquisition: он может получать только официальные release/checksum/license/OCI-manifest metadata, не installer, layer, package или image payload. Его scope и origins утверждаются вручную.
3. Ни один downloaded artifact не запускается, не импортируется и не используется как build input до byte/hash/signature/source verification.
4. Ни один locally built image не запускается до immutable successor runtime-lock с exact output digest.
5. Короткие image names, tag-only references, `latest`, неполный platform tuple, mutable build context и runtime package installation запрещены.
6. Отклонение runtime inventory от approved runtime-lock всегда заметно. Неизвестность не превращается в `CURRENT`.
7. Update — отдельная транзакция с новым successor-lock, migration rehearsal, owner gate и last-known-good set. In-place downgrade после migration запрещён.
8. Automation никогда не принимает юридические условия от имени владельца, не передаёт license-acceptance switch и не кликает consent UI.
9. Evidence secret-minimal и content-addressed. URL с credential/query, registry auth, account/serial IDs и PII не сохраняются.
10. Все Docker mutations дополнительно зависят от локального endpoint/control-plane contract V2; supply-chain PASS сам по себе не разрешает mutation.

## 2. Объекты и их состояния

### 2.1. Двухфазная неизменяемая модель lock

Невозможность знать digest ещё не собранного local image до получения его материалов решается двумя новыми immutable объектами, а не редактированием одного lock:

- `SUPPLY_CHAIN_LOCK_ACQUISITION`: создаётся после metadata-discovery и до первого payload byte. Содержит exact external materials, build recipe/context identity и `runtime_allowed=false` для local outputs.
- `SUPPLY_CHAIN_LOCK_RUNTIME`: новый successor, ссылающийся на hash acquisition-lock. Создаётся после offline/no-network build и содержит exact local output digest. Только runtime-lock может разрешить pull/import/start/build-reuse.

Предшествующий lock никогда не изменяется. Любая перемена URL, redirect origin, hash, signer policy, version, OCI digest, source revision, dependency integrity, license revision, tool/policy или exception создаёт новый lock с новым SHA-256 и повторяет disposition.

### 2.2. Canonical envelope

Контракт `V2-SC-LOCK-001`:

```yaml
schema: n8nagents.supply-chain-lock/v2
lock_id: immutable-random-id
phase: ACQUISITION | RUNTIME
predecessor_sha256: null | 64-lower-hex
plan_v2_sha256: 64-lower-hex
v0_baseline_sha256: 934c449aa75ad157b1702afefcbaac4eab80b750801f172226d065b5a528c4aa
authority_id: opaque-nonsecret-id
created_utc: RFC3339-UTC
valid_until_utc: RFC3339-UTC
runtime_allowed: false | true
source_evidence: [EV-V2-SOURCE-*]
docker_desktop: V2-SC-INSTALLER-002
oci_images: [V2-SC-OCI-004]
local_builds: [V2-SC-BUILD-005]
licenses: [V2-SC-LICENSE-006]
tools_and_databases: [V2-SC-SCAN-007]
policies:
  vulnerability_policy_sha256: 64-lower-hex
  license_policy_sha256: 64-lower-hex
  drift_policy_sha256: 64-lower-hex
manual_approvals: [opaque-record-id]
payload_sha256: calculated-outside-payload
```

Payload сериализуется по RFC 8785/JCS, UTF-8 без BOM. `payload_sha256` хранится во внешнем envelope и не входит в hashed payload. Verifier отклоняет duplicate keys, неизвестную schema version, неопределённое обязательное поле, истёкший `valid_until_utc`, повторный `lock_id`, отсутствующий predecessor и несоответствие plan/baseline hashes. Acquisition и runtime evidence всегда ссылаются на exact lock hash.

### 2.3. State machine и RC

Состояние вычисляется, а не выбирается оператором:

| Состояние | Условие | Разрешённые действия |
|---|---|---|
| `CURRENT` | observed installed/runtime identity byte-for-byte/field-for-field совпадает с действующим runtime-lock; обязательные evidence и approvals не истекли | read-only status; approved mock/real/gate операции через другие gates |
| `DRIFTED` | хотя бы одно enforced поле отличается, отсутствует или не читается; auto-update/setting/source/license drift не имеет successor | только status, export evidence, backup/recovery preparation; start/real-dev/gate/pull/build блокируются |
| `UPDATE_PENDING` | successor acquisition/runtime-lock и exact delta одобрены, mutation ещё не завершена | только update state machine и abort до первой mutation; обычный runtime не переводится автоматически |
| `ROLLBACK_REQUIRED` | update/install/build/import частично выполнен, postcondition не прошёл либо data compatibility не доказана | только emergency stop, evidence, restore-first recovery; workload start и in-place downgrade запрещены |

RC contract `V2-SC-RC-008`:

| RC | Значение |
|---:|---|
| `0` | exact scoped operation `PASS`; для `status` только `CURRENT` |
| `20` | `BLOCKED-MANUAL` — отсутствует/истек owner approval |
| `21` | `BLOCKED-SOURCE` — origin/revision/hash metadata неполны |
| `22` | `BLOCKED-SIGNATURE` — signer/chain/EKU/timestamp policy не пройдена |
| `23` | `BLOCKED-REVOCATION` — revocation unknown/unavailable/revoked |
| `24` | `BLOCKED-IDENTITY` — installer/image/installed identity mismatch |
| `25` | `BLOCKED-LICENSE` — license/usage/obligation не dispositioned |
| `26` | `BLOCKED-SCAN` — SBOM/scanner/DB/policy/exception невалидны |
| `27` | `BLOCKED-TOCTOU` — path/ACL/reparse/file identity changed |
| `28` | `BLOCKED-BUILD` — hermetic materials/context/output contract нарушен |
| `29` | `BLOCKED-ROLLBACK` — last-known-good/recovery proof неполон |
| `30` | `DRIFTED` |
| `31` | `UPDATE_PENDING` |
| `32` | `ROLLBACK_REQUIRED` |
| `33` | `BLOCKED-CAPABILITY` |
| `40` | tool/internal error; никогда не PASS |
| `41` | evidence/schema/manifest invalid; никогда не PASS |

Child stdout со словом `PASS`, scanner с пустым результатом, missing row или `UNKNOWN` не меняют RC. Aggregator принимает только schema-valid result и ожидаемый RC/status pair.

## 3. Metadata-discovery до acquisition

Контракт `V2-SC-DISCOVERY-009` разрешает только после отдельного owner gate:

- HTTPS GET/HEAD к заранее перечисленным official origins Docker, Microsoft, n8n, PostgreSQL и выбранным official registries;
- получение release metadata, checksum/signature metadata, license/terms text, support requirements, OCI index/manifest/config metadata и vulnerability DB metadata;
- запрет installer/image layer/package/source archive payload, redirect на неутверждённый origin, credentials, installer execution, registry login и Docker mutation;
- byte/response ceilings по origin и global total; redirect count; TLS validation; UTC start/end;
- новый `SourceEvidence` на каждый claim.

`SourceEvidence` schema `V2-SC-SOURCE-010`:

```yaml
schema: n8nagents.source-evidence/v2
source_id: EV-V2-SOURCE-unique
claim_id: lock-field-path
original_uri: exact-official-https-uri-without-secret
redirect_chain:
  - status: integer
    origin: scheme-host-port
    location_sha256: 64-lower-hex
final_uri: exact-official-https-uri-without-secret
retrieved_utc: RFC3339-UTC
http_status: integer
content_type: exact
bytes: integer
content_sha256: 64-lower-hex
etag: null | exact
last_modified: null | exact
document_revision: exact-stable-id-or-null
effective_date: exact-or-null
signature_metadata_sha256: null | 64-lower-hex
extracted_claim_sha256: 64-lower-hex
acquisition_lock_sha256: 64-lower-hex
redaction_schema: n8nagents-source-redaction/v2
```

Отсутствие stable revision допустимо только как explicit residual с коротким `valid_until_utc` и owner approval; отсутствие content hash/origin/UTC/claim binding недопустимо. Изменение redirect origin или content/revision до acquisition требует нового lock.

## 4. Docker Desktop installer и TOCTOU-safe custody

### 4.1. Exact installer record

`V2-SC-INSTALLER-002` содержит до payload download:

- canonical product, edition, channel, version и build;
- exact original official URL, allowed redirect origins, expected final URL;
- exact bytes cap и expected SHA-256 из отдельно аутентифицированного official vendor metadata, не из downloaded file;
- exact expected embedded signer leaf certificate SHA-256, canonical subject, issuer, serial, Code Signing EKU, allowed signature count;
- chain policy/root-store snapshot identity;
- trusted timestamp policy, timestamp signer identity/chain, signing time bounds;
- mandatory whole-chain revocation mode at acquisition time, CRL/OCSP result and checked UTC;
- expected installer/package identity and allowed installed build/channel;
- SourceEvidence IDs для каждого значения.

Если official vendor не даёт independently authenticated digest, exact signer cannot be resolved, signature is absent/multiple-unexpected, timestamp is untrusted, revocation status is unknown/offline, или metadata changed — `BLOCKED-SOURCE/SIGNATURE/REVOCATION`. Альтернативный acquisition method требует нового reviewed plan/lock; verifier не ослабляется.

### 4.2. Private staging и file identity

Контракт `V2-SC-STAGING-003`:

1. Создать новый unpredictable staging directory на approved local NTFS root вне project/Vault/cloud-sync/removable/network roots.
2. Проверить physical volume identity, exact case/Unicode path, отсутствие reparse point у каждого ancestor, owner и ACL. Доступ — intended owner и SYSTEM; наследуемый broad access запрещён.
3. Создать `.partial` через create-new/no-overwrite. Download writer не использует shell resolution.
4. После download закрыть network writer; открыть file handle с запретом write/delete sharing. Зафиксировать canonical path, volume serial pseudonym, file ID, size, creation/write time и ACL hash.
5. На удерживаемом handle вычислить SHA-256 и проверить embedded Authenticode, Code Signing EKU, chain, timestamp и revocation. Сравнить с lock.
6. Atomic rename внутри того же directory; повторно открыть final path с deny-write/delete, доказать прежний file ID и повторить hash/signature непосредственно перед process creation.
7. Запускать только absolute verified path, без PATH/current-directory/shell lookup. Удерживать custody handle до успешного создания process и зафиксировать process image identity. После запуска сверить file ID/hash ещё раз.
8. Любое изменение ancestor, ACL, reparse tag, file ID, bytes, signer или timestamp даёт `BLOCKED-TOCTOU`; installer не запускается.
9. Cleanup/quarantine допускается только после повторной containment+file-ID проверки. Если identity изменилась, ничего не удалять автоматически вне изолированного staging; сохранить только безопасные metadata.

Доверенная boundary всё ещё включает Windows kernel, intended owner, SYSTEM и локального администратора. Это residual risk, а не утверждение абсолютной защиты от privileged local attacker.

## 5. OCI identity для всех images

Контракт `V2-SC-OCI-004` охватывает каждый Compose service, one-shot migration/backup/restore/QA/scanner image, каждый Dockerfile `FROM`/frontend/builder и local output:

```yaml
image_id: stable-logical-name
official_namespace_proof: EV-V2-SOURCE-*
registry_fqin: registry.example/namespace/repository
registry_endpoint: exact-origin
mirror_or_proxy_state: NONE | exact-reviewed-id
tag_metadata: exact-tag
oci_index_digest: sha256:... | null-if-single-manifest
linux_amd64_child_digest: sha256:...
config_digest: sha256:...
layers: [{digest: sha256:..., bytes: integer}]
compressed_bytes: integer
platform: {os: linux, architecture: amd64, variant: null}
vendor_signature_or_attestation: exact-evidence-id | NOT_PUBLISHED
sbom_id: EV-V2-SBOM-*
scan_id: EV-V2-SCAN-*
license_record_id: EV-V2-LICENSE-*
```

Compose render использует canonical FQIN plus approved digest и explicit `platform: linux/amd64`; short names и tag-only запрещены. До use verifier сравнивает lock, registry metadata, locally loaded image OS/architecture, child manifest, config и layer set. Index digest не заменяет child digest. `NOT_PUBLISHED` для vendor signature является отдельным residual, требующим owner disposition, а не PASS.

Offline restart не выполняет tag resolution. Archive/import evidence связывает тот же index/child/config tuple. Local tag считается только удобным alias и никогда не identity.

## 6. Hermetic bridge/mock build

Контракт `V2-SC-BUILD-005`:

- immutable candidate/build context manifest: exact files, types, modes, bytes, SHA-256, base HEAD, dirty candidate aggregate, `.dockerignore`, effective attributes/EOL;
- pinned Dockerfile frontend/builder/base image по OCI tuple;
- exact Node/runtime/tool versions и tool hashes;
- direct/transitive dependency lock с integrity; Git/URL dependencies только exact commit+content digest;
- OS packages только из approved signed immutable snapshot, exact package version/digest/signing-key identity;
- `npm ci`/equivalent только frozen lock. Lifecycle scripts default deny; каждый разрешённый script имеет source hash, network policy и reviewer disposition;
- remote `ADD`, floating apt/apk/npm, unpinned package, unknown generated asset и secret in build context/layer запрещены;
- material-fetch выполняется отдельно и формирует verified read-only cache. Actual build выполняется с network disabled и не имеет registry credentials, secrets, Docker socket или host-root mount;
- clean cache rehearsal доказывает, что declared materials complete. Build provenance перечисляет recipe/context/materials/toolchain/output;
- local output получает exact OCI child/config/layer digest и successor runtime-lock до первого container create/start.

Если deterministic byte-identical image digest невозможно гарантировать из-за установленного toolchain, policy должна заранее определить и independently review содержательную reproducibility boundary. Нельзя просто принять новый output digest после сборки: он обязан пройти provenance/SBOM/scan/license review и owner approval successor-lock.

Runtime installation community/custom n8n nodes и external modules запрещена. Нужный extension добавляется только как reviewed source/dependency в этот build contract, final image/SBOM/lock и отдельный approval.

## 7. License gates

Контракт `V2-SC-LICENSE-006` создаёт по одному `LicenseDisposition` для Docker Desktop, exact n8n release и каждого third-party component из SBOM:

```yaml
license_record_id: EV-V2-LICENSE-unique
subject: docker-desktop | n8n-release | package-or-image
artifact_digest: exact-or-null-for-terms
official_terms_source: EV-V2-SOURCE-*
license_identifier: exact-SPDX-or-NOASSERTION
revision_and_effective_date: exact
usage_entity_classification: owner-entered-category
obligations: [notice, attribution, source-offer, usage-restriction, subscription]
compatibility_disposition: ALLOW | DENY | OWNER-EXCEPTION
approver_attestation_id: opaque-owner-record
approved_utc: RFC3339-UTC
expires_utc: RFC3339-UTC
lock_sha256: 64-lower-hex
```

Manual gates:

- `MG-V2-LICENSE-DOCKER`: владелец/уполномоченное лицо читает exact current official Docker terms, выбирает применимую entity/usage category и фиксирует subscription basis, если требуется. Automation не принимает terms.
- `MG-V2-LICENSE-N8N`: владелец рассматривает exact license/usage restrictions pinned n8n release и planned local/production-like usage.
- `MG-V2-LICENSE-THIRD-PARTY`: license policy и obligations для полного SBOM; `NOASSERTION`, conflict, prohibited license или unknown obligation дают `BLOCKED-LICENSE`.

Изменение revision/effective date, usage class, artifact digest, dependency graph или policy аннулирует прежний record. NOTICE/source-offer/attribution artifacts включаются в runtime/release package по проверяемому manifest.

## 8. SBOM, vulnerability scan и source evidence

### 8.1. SBOM schema

Контракт `V2-SC-SBOM-011` требует CycloneDX JSON exact schema version, выбранную и закреплённую в lock. Для каждого final linux/amd64 child image:

- image FQIN/index/child/config digests и lock hash;
- generator name/version/image digest/executable hash;
- components с purl/CPE при наличии, exact version, file/package hashes, licenses, supplier/source и dependency edges;
- OS, language, vendored/generated/local components;
- completeness assertions и explicit unknowns;
- canonical JSON bytes/hash, UTC и evidence manifest binding.

SBOM другого child/config digest отклоняется. Пустой SBOM, generator error, missing operational image или unknown schema дают `BLOCKED-SCAN`.

### 8.2. Scanner disposition

Контракт `V2-SC-SCAN-007` фиксирует scanner binary/image digest, vulnerability DB snapshot digest/source/generated/updated UTC, max age, exact policies и offline invocation. Scan охватывает exact final child digest, не tag/index вообще.

Policy minimum:

- scanner/DB/source/schema error, missing component coverage или stale DB — `BLOCKED-SCAN`;
- malware/known-exploited finding и threshold violations — `FAIL`;
- unknown/unfixed critical/high — `BLOCKED-MANUAL`, не автоматический PASS;
- exception содержит owner, affected digest/CVE/license, rationale, compensating control, created/expiry UTC и successor-lock hash; истёкшая/широкая exception запрещена;
- report сохраняет counts/IDs/dispositions без registry credentials/PII и связан с SBOM/lock/evidence manifest.

Точный severity/age threshold утверждается до acquisition как hashed policy. Этот draft не выбирает scanner или DB и не утверждает отсутствие vulnerabilities.

## 9. Installed identity equality

Контракт `V2-SC-INSTALLED-012` выполняется после install/reboot и до первого pull/import/container:

- product/package identity, Desktop version/build/channel и install path;
- installed launcher/binary signer, signature status и file hashes;
- Engine, CLI, Compose, BuildKit, WSL backend/kernel component identities;
- update channel/settings hash и auto-update observed capability;
- Docker endpoint contract identity и Server OS `linux`;
- список любых supplementary payload downloads с собственными source/hash/signature records.

Каждое enforced поле должно равняться installer/runtime-lock. Bootstrapper, immediate auto-update, иной channel/build, дополнительный непредусмотренный payload или unreadable identity дают `BLOCKED-IDENTITY/DRIFTED`. Равенство версии без signer/package/source equality недостаточно.

## 10. Drift и управляемые updates

### 10.1. Drift inventory

Контракт `V2-SC-DRIFT-013` хранит approved и observed значения для:

- Docker Desktop/product/channel/settings, Engine/CLI/Compose/BuildKit/WSL kernel;
- endpoint identity и relevant execution fingerprint;
- всех OCI index/child/config/layer tuples;
- local build output/context/dependency/tool hashes;
- n8n runtime extension inventory;
- source/license/policy revisions и exception expiry;
- SBOM/scanner/tool/database snapshot identity;
- Compose/config/migration schema identities и last-known-good set.

Read-only `lab status` пересчитывает inventory до каждой mutation/start. Любое missing/unreadable/enforced mismatch даёт `DRIFTED` и RC `30`; drift не исправляется pull/update автоматически. Informational OS facts могут быть non-enforced только если exact field classification предварительно hashed и reviewed.

### 10.2. Update state machine

Контракт `V2-SC-UPDATE-014`:

1. `CURRENT` baseline и current last-known-good set проверены.
2. Metadata-discovery создаёт exact from/to delta, release/source/license/security/compatibility evidence.
3. Создаётся successor acquisition-lock; owner одобряет `MG-V2-UPDATE-DELTA`.
4. До mutation: disk/resource preflight, COMPLETE+restore-verified backup DB/n8n/key pair, no real-dev arming, all writers stopped.
5. New images/materials загружаются и проверяются; hermetic local build формирует successor runtime-lock и повторный owner approval.
6. Upgrade репетируется на cloned/restored disposable volumes. n8n schema migration и PostgreSQL major upgrade — отдельные exact procedures. Прямое использование прежнего PostgreSQL data directory с несовместимым major запрещено.
7. Promotion выполняется только после compatibility, capability, exposure, mock, backup/cold-restore и evidence gates.
8. При failure рабочие old volumes не модифицируются либо восстанавливается pre-upgrade generation в новых volumes. Older n8n/PostgreSQL никогда не запускается на migrated state.
9. Success переводит successor в `CURRENT`, previous current — в `LAST_KNOWN_GOOD`. Failure после mutation — `ROLLBACK_REQUIRED`.

In-place downgrade допускается только при exact official support evidence для from/to data formats и отдельном owner gate. Иначе единственный rollback — restore pre-upgrade generation с matching old images/config/key в новых volumes. Отсутствие доказанного пути даёт `BLOCKED-ROLLBACK`.

## 11. Last-known-good retention и offline import proof

Контракт `V2-SC-LKG-015` хранит минимум `CURRENT` и один `LAST_KNOWN_GOOD` набор:

- verified Docker installer bytes и installer/source/signature evidence;
- OCI archives/layouts для каждого vendor/base/tool/final local image с index/child/config/layer metadata;
- acquisition/runtime locks, Compose/config/migration sources, bridge/mock source/context/dependency locks;
- SBOM, scanner DB identity/report/disposition, licenses/NOTICE, tool BOM;
- COMPLETE+restore-verified pre-upgrade backup and non-secret key IDs;
- compatibility/update/capability/evidence manifests.

Удаление последнего validated rollback set запрещено; quota pressure даёт manual cleanup preview, не auto-delete. Новый LKG заменяет старый только после successful update, cold restore и owner `MG-V2-LKG-RETIRE`.

Import proof выполняется без registry/network в disposable nested Docker daemon внутри Docker Desktop: no Docker socket, no host-root/persistent-lab mounts, ephemeral daemon data, `--network none`, exact archive read-only. Это допускается только после отдельного privileged-container containment contract; иначе результат `BLOCKED-CAPABILITY`. В clean nested daemon нужно импортировать archives, сверить child/config/layer digests и запустить только non-secret structural/health fixture. Existing host image cache не может служить proof. После evidence удаляются только exact run-labelled disposable resources.

Для Docker Desktop installer offline proof ограничен повторной проверкой retained bytes/hash/signature/source. Actual Desktop reinstall/downgrade не считается доказанным этим разделом и требует disposable Windows environment либо отдельного destructive/manual recovery gate. Это явный residual risk.

## 12. Manual gates

| Gate | Что утверждает владелец | До чего блокирует |
|---|---|---|
| `MG-V2-DISCOVERY` | exact metadata-only origins, ceilings, redirect policy | любая сеть metadata-discovery |
| `MG-V2-SUPPLY-LOCK` | bytes/hash acquisition-lock и все unresolved/residual dispositions | payload download/pull/material fetch |
| `MG-V2-LICENSE-DOCKER` | exact terms revision, eligibility/subscription basis | Docker installer download/install |
| `MG-V2-LICENSE-N8N` | exact release license и planned usage | n8n image pull/use |
| `MG-V2-LICENSE-THIRD-PARTY` | SBOM license policy/obligations/exceptions | image use/package |
| `MG-V2-RUNTIME-LOCK` | local outputs, SBOM/scan/license/provenance, runtime-lock hash | first container create/start |
| `MG-V2-INSTALL-UAC` | exact installer path/hash, signer evidence и delta | elevated process creation |
| `MG-V2-UPDATE-DELTA` | exact from/to delta, backup, migration, rollback and cost | update mutation |
| `MG-V2-LKG-RETIRE` | exact artifacts to delete and remaining validated set | any LKG deletion |
| `MG-V2-ALT-ACQUISITION` | новый method при отсутствии official hash/signature/source | никакого fail-open fallback |

Reboot/Windows-feature, endpoint, storage, secrets, Telegram, DeepSeek, backup-key и destructive gates остаются у соответствующих V2 sections и не подразумеваются этими approvals.

## 13. Finding coverage: contract + acceptance test + negative canary + evidence

Ниже перечислены все V0 findings, непосредственно решаемые этим разделом либо являющиеся обязательными cross-dependencies. Для каждого есть минимум один именованный contract, acceptance test, negative canary и evidence artifact. Cross-dependency не считается закрытой до PASS владельца соответствующего раздела.

| Finding | Contract | Acceptance test | Negative canary | Evidence |
|---|---|---|---|---|
| `R1-WIN-001` | `V2-XDEP-ENDPOINT-R1-001` | `AT-V2-R1-WIN-001`: pull/import/build/status на exact local Desktop context | `NC-V2-R1-WIN-001`: `DOCKER_HOST` указывает sentinel remote; ноль API mutation | `EV-V2-R1-WIN-001`: endpoint preflight + zero-mutation trace |
| `R1-WIN-002` | `V2-SC-SOURCE-SNAPSHOT-R1-002` | `AT-V2-R1-WIN-002`: eligibility rule с dated Docker/Microsoft evidence | `NC-V2-R1-WIN-002`: unreadable requirement revision | `EV-V2-R1-WIN-002`: SourceEvidence + evaluated predicate |
| `R1-WIN-003` | `V2-SC-COMPONENT-PROVENANCE-R1-003` | `AT-V2-R1-WIN-003`: каждый WSL/package/update artifact lock-bound | `NC-V2-R1-WIN-003`: дополнительный unlisted payload | `EV-V2-R1-WIN-003`: exact delta/material manifest |
| `R1-WIN-005` | `V2-SC-EXISTING-INSTALL-R1-005` | `AT-V2-R1-WIN-005`: fresh/approved-upgrade/blocked branches | `NC-V2-R1-WIN-005`: неизвестный prior data owner | `EV-V2-R1-WIN-005`: installed discovery inventory |
| `R1-WIN-006` | `V2-SC-INSTALL-RECOVERY-R1-006` | `AT-V2-R1-WIN-006`: documented effects и no false non-destructive claim | `NC-V2-R1-WIN-006`: unaccounted WSL/network remnant | `EV-V2-R1-WIN-006`: before/after/change ledger |
| `R1-WIN-007` | `V2-XDEP-LKG-BUDGET-R1-007` | `AT-V2-R1-WIN-007`: peak acquisition+LKG+restore сохраняет reserve | `NC-V2-R1-WIN-007`: projected peak выше hard mark | `EV-V2-R1-WIN-007`: budget equation/pre-growth result |
| `R1-WIN-009` | `V2-SC-DRIFT-R1-009` | `AT-V2-R1-WIN-009`: изменение каждой version/settings field → `DRIFTED` | `NC-V2-R1-WIN-009`: silent Desktop auto-update | `EV-V2-R1-WIN-009`: approved-vs-observed diff |
| `R2-001` | `V2-SC-LOCK-R2-001` | `AT-V2-R2-001`: acquisition/runtime принимают только approved lock hash | `NC-V2-R2-001`: изменить один digest после approval | `EV-V2-R2-001`: lock bytes/hash/approval binding |
| `R2-002` | `V2-SC-INSTALLER-R2-002` | `AT-V2-R2-002`: exact vendor signer/chain/EKU/timestamp/revocation | `NC-V2-R2-002`: signed-by-other/revoked/offline-revocation fixture | `EV-V2-R2-002`: structured signature/source result |
| `R2-003` | `V2-SC-STAGING-R2-003` | `AT-V2-R2-003`: same file ID/hash до process creation | `NC-V2-R2-003`: replace/reparse/ACL/file-ID race | `EV-V2-R2-003`: custody timeline and sentinel hashes |
| `R2-004` | `V2-SC-OCI-R2-004` | `AT-V2-R2-004`: Compose/registry/local inspect converge tuple | `NC-V2-R2-004`: same short name, wrong child/arch/config | `EV-V2-R2-004`: OCI tuple manifest |
| `R2-005` | `V2-SC-BUILD-R2-005` | `AT-V2-R2-005`: clean-cache no-network build matches declared materials | `NC-V2-R2-005`: unlocked dependency/remote ADD/lifecycle fetch | `EV-V2-R2-005`: build provenance/material graph/output digest |
| `R2-006` | `V2-SC-UPDATE-R2-006` | `AT-V2-R2-006`: drift blocks; failed update restores verified generation | `NC-V2-R2-006`: try old binary on migrated data | `EV-V2-R2-006`: update ledger/from-to compatibility |
| `R2-007` | `V2-SC-LICENSE-R2-007` | `AT-V2-R2-007`: all three manual license records current | `NC-V2-R2-007`: missing owner attestation/changed terms | `EV-V2-R2-007`: LicenseDisposition set |
| `R2-008` | `V2-SC-SBOM-SCAN-R2-008` | `AT-V2-R2-008`: schema-valid digest-bound disposition | `NC-V2-R2-008`: stale DB/scanner error/wrong digest/expired waiver | `EV-V2-R2-008`: SBOM+scan+DB+policy hashes |
| `R2-009` | `V2-SC-LKG-R2-009` | `AT-V2-R2-009`: offline clean-daemon import exact set | `NC-V2-R2-009`: delete sole validated set or corrupt layer | `EV-V2-R2-009`: retention manifest/import transcript anchor |
| `R2-010` | `V2-SC-EXTENSIONS-R2-010` | `AT-V2-R2-010`: extension exists only in approved final image | `NC-V2-R2-010`: n8n UI/runtime package install attempt | `EV-V2-R2-010`: extension inventory/SBOM/runtime refusal |
| `R2-011` | `V2-SC-INSTALLED-R2-011` | `AT-V2-R2-011`: installer-to-installed exact equality | `NC-V2-R2-011`: immediate auto-update/different build | `EV-V2-R2-011`: installed identity record |
| `R2-012` | `V2-SC-SOURCE-R2-012` | `AT-V2-R2-012`: offline auditor recovers each official claim | `NC-V2-R2-012`: changed redirect/missing revision/hash | `EV-V2-R2-012`: canonical SourceEvidence set |
| `R3-CTRL-005` | `V2-XDEP-CONTROL-R3-005` | `AT-V2-R3-CTRL-005`: supply tools have no Docker socket/control access unless wrapper stage | `NC-V2-R3-CTRL-005`: injected socket mount | `EV-V2-R3-CTRL-005`: mount/capability inventory |
| `R3-PRIV-001` | `V2-XDEP-LKG-DIND-R3-001` | `AT-V2-R3-PRIV-001`: disposable nested daemon has bounded resources/no host mounts/socket | `NC-V2-R3-PRIV-001`: privileged container requests host root/socket | `EV-V2-R3-PRIV-001`: privileged containment matrix |
| `R4-F05` | `V2-SC-MIGRATION-R4-005` | `AT-V2-R4-F05`: staged n8n/PostgreSQL upgrade and restore-first rollback | `NC-V2-R4-F05`: incompatible PG data-dir reuse | `EV-V2-R4-F05`: migration rehearsal/equality evidence |
| `R4-F08` | `V2-SC-ALL-IMAGES-R4-008` | `AT-V2-R4-F08`: every service/job/stage present in lock | `NC-V2-R4-F08`: hidden helper tag-only image | `EV-V2-R4-F08`: rendered image coverage report |
| `R7-F09` | `V2-SC-NO-DOWNGRADE-R7-009` | `AT-V2-R7-F09`: failure restores pre-upgrade generation in new volumes | `NC-V2-R7-F09`: old image with upgraded volume | `EV-V2-R7-F09`: compatibility/restore gate record |
| `R7-F10` | `V2-SC-LKG-FAULT-DOMAIN-R7-010` | `AT-V2-R7-F10`: no-registry import without current image cache | `NC-V2-R7-F10`: archive set omits one required image | `EV-V2-R7-F10`: clean nested-daemon import manifest |
| `R8-P1-003` | `V2-SC-CANDIDATE-R8-003` | `AT-V2-R8-P1-003`: context/tool/output hashes remain one chain | `NC-V2-R8-P1-003`: byte change between freeze/build/review | `EV-V2-R8-P1-003`: candidate+runner+build anchor |
| `R8-P1-008` | `V2-XDEP-NONET-R8-008` | `AT-V2-R8-P1-008`: no-network build/import plus positive-control probe | `NC-V2-R8-P1-008`: attach second/default network | `EV-V2-R8-P1-008`: interface/route/probe evidence |
| `R8-P1-009` | `V2-SC-FINGERPRINT-R8-009` | `AT-V2-R8-P1-009`: execution result valid only for exact environment fingerprint | `NC-V2-R8-P1-009`: change kernel/storage driver | `EV-V2-R8-P1-009`: environment fingerprint binding |
| `R8-P1-010` | `V2-SC-EVIDENCE-R8-010` | `AT-V2-R8-P1-010`: exact-set manifest/aggregate verifies | `NC-V2-R8-P1-010`: replace report from another run | `EV-V2-R8-P1-010`: source/SBOM/scan/build evidence envelope |
| `R8-P2-011` | `V2-SC-TOOL-BOM-R8-011` | `AT-V2-R8-P2-011`: all tools/hash/features match lock | `NC-V2-R8-P2-011`: hide/substitute scanner/build verifier | `EV-V2-R8-P2-011`: tool BOM/probe report |
| `R9-F05` | `V2-SC-BUILD-CANDIDATE-R9-005` | `AT-V2-R9-F05`: tested/reviewed/committed build inputs equal | `NC-V2-R9-F05`: add ignored file after freeze | `EV-V2-R9-F05`: content-addressed context manifest |
| `R10-F03` | `V2-XDEP-LKG-RESTORE-R10-003` | `AT-V2-R10-F03`: LKG set references independently recoverable backup+key IDs | `NC-V2-R10-F03`: incompatible version/wrong key ID | `EV-V2-R10-F03`: cold-restore compatibility result |
| `R10-F04` | `V2-XDEP-LKG-SPACE-R10-004` | `AT-V2-R10-F04`: retention/import/update preflight preserves hard reserve | `NC-V2-R10-F04`: disk pressure before archive/import | `EV-V2-R10-F04`: measured/projected usage result |
| `R10-F05` | `V2-SC-STATES-R10-005` | `AT-V2-R10-F05`: `CURRENT/DRIFTED/UPDATE_PENDING/ROLLBACK_REQUIRED` transitions | `NC-V2-R10-F05`: mutate one digest/Compose/build value | `EV-V2-R10-F05`: state transition ledger |
| `R10-F09` | `V2-SC-OWNER-CEREMONY-R10-009` | `AT-V2-R10-F09`: license/UAC/reboot resume records exact lock/delta | `NC-V2-R10-F09`: resume with changed lock or repeat installer | `EV-V2-R10-F09`: owner cards/checkpoint hashes |
| `R10-F11` | `V2-SC-DAILY-DRIFT-R10-011` | `AT-V2-R10-F11`: fresh unelevated session runs status/update preview | `NC-V2-R10-F11`: sleep/reboot yields silent stale `CURRENT` | `EV-V2-R10-F11`: black-box daily drift transcript |

Coverage count этого раздела: `36` unique baseline finding IDs; duplicate IDs запрещены.

## 14. Cross-dependencies и владельцы границ

| Зависимость | Требуемый внешний контракт | Поведение при отсутствии |
|---|---|---|
| Local Docker endpoint/control plane | R1/R3/R6 V2 section: explicit local context, no env override, caller boundary | `BLOCKED-IDENTITY`; Docker mutation не выполняется |
| Windows eligibility/change transaction | Windows V2 section: support predicate, exact UAC/feature/reboot state machine | installer download/install блокируется |
| Storage/resource roots | Windows/resource V2 section: roots, ACL/reparse/at-rest, hard reserve | acquisition/LKG/update блокируется |
| No-network/privileged containment | isolation V2 section: actual runtime matrix, no socket/host root | hermetic build/LKG import proof `BLOCKED-CAPABILITY` |
| Migration/backup/key consistency | Compose/backup V2 sections: COMPLETE restore-verified generation and key IDs | update/retirement блокируется |
| Candidate/evidence custody | repository/evidence V2 sections: immutable candidate/runner/manifest | local build/review/runtime-lock блокируется |
| User operability | runbook V2 section: read-only status, exact update preview, recovery states | handoff DoD не закрывается |

Supply-chain section не владеет secrets, Telegram authorization, production deployment, destructive cleanup или backup cryptography. Он потребляет только non-secret IDs/hashes их approved contracts.

## 15. Stop conditions

Немедленный STOP/BLOCKED до следующей mutation:

- отсутствует approved lock hash, истёк approval или найден successor mismatch;
- origin/redirect/revision/checksum/signer/timestamp/revocation не доказаны;
- staging root/ancestor/ACL/file identity изменились;
- OCI FQIN/index/child/config/layer/platform расходятся;
- build делает undeclared fetch, видит secret, Docker socket/host root или сеть на actual-build stage;
- SBOM/scan/tool DB/schema невалидны, stale или относятся к другому digest;
- license unknown/conflict/terms drift или automation пытается принять условия;
- installed identity отличается от exact installer/runtime lock;
- status не `CURRENT`, кроме явно активной approved update/recovery transaction;
- pre-upgrade backup/cold restore/LKG import proof отсутствуют;
- recovery требует unsupported in-place downgrade;
- evidence manifest, candidate, runner, environment или authority identity не сходятся.

## 16. Residual risks и unresolved conflicts

1. Exact official artifacts/terms/signers/digests пока `UNKNOWN`; этот документ не является их подтверждением.
2. Revocation checking зависит от доступности authoritative CRL/OCSP и Windows trust store. Недоступность блокирует acquisition; offline bypass не предусмотрен.
3. Vendor может не публиковать OCI signatures/attestations или independently authenticated installer checksum. Это требует explicit owner residual/new acquisition review, а не автоматический GO.
4. Local administrator/SYSTEM/Windows kernel остаются в trusted boundary installer custody.
5. Docker Desktop downgrade и восстановление самого managed VHDX не доказаны. Retained installer не гарантирует vendor-supported downgrade.
6. Clean import proof через nested privileged daemon зависит от отдельного containment PASS. Без него LKG остаётся `BLOCKED-CAPABILITY`; план B/VPS не включаются.
7. Bit-reproducible local image digest может зависеть от toolchain metadata. Допустимая reproducibility boundary должна быть утверждена до build; новый digest нельзя self-approve.
8. Vulnerability/license disposition имеет временную природу; истечение DB/source/exception/terms переводит environment в `DRIFTED/BLOCKED`, даже если bytes не изменились.
9. Retention `CURRENT + one LKG` требует disk budget. Недостаток места не разрешает auto-delete единственного LKG.
10. `UPDATE_PENDING` не гарантирует rollback. Любая не доказанная migration compatibility до mutation остаётся `BLOCKED-ROLLBACK`.

## 17. Definition of Done этого раздела

Раздел может считаться design-ready для интеграции в полный plan V2, когда:

- все `36` finding IDs механически существуют в V0 baseline и имеют contract/test/canary/evidence IDs;
- канонический lock/source/SBOM/scan/license/drift/update/LKG contracts включены в интегрированный V2 без смыслового ослабления;
- external dependencies названы и их отсутствие fail-closed;
- exact RC/status/manual gates не конфликтуют с общей V2 state machine;
- независимые reviewers атаковали two-lock model, installer TOCTOU, revocation, OCI leaf identity, hermetic build, license authority, update migration и LKG proof;
- никакое предложение не трактуется как runtime PASS или разрешение на installation/acquisition.

## Связи

- [[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[Итог_Кворума_10_Ревью_Docker_Desktop_N8NAgents_v1_2026-08-27]]
- [[N8NAgents]]
