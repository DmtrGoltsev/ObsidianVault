---
id: "n8nagents-plan-v2-exclusions-unknowns-draft"
тип: "ревью"
статус: "черновик"
проект: "AgentSystem"
владелец: "cross-domain-integration-owner"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[План_Лаборатория_Docker_Desktop_N8NAgents_v2_2026-08-27]]", "[[12_CROSS_DOMAIN_INTEGRATION_DECISIONS]]"]
доказательства: []
теги: ["plan-v2", "exclusions", "unknowns", "stop-conditions"]
---

# Exclusions, unknowns и честные границы plan v2

## Исключено без автоматического fallback

- отдельная Ubuntu/WSL distro и любой plan B;
- Hyper-V VM, Windows Sandbox, v86, QEMU;
- VPS, production, remote Docker, provider UI;
- Caddy/public TLS/DNS/tunnel/webhook exposure;
- Windows containers, Kubernetes, Swarm;
- production Telegram bot/token локально;
- privilege/root/SYS_ADMIN/device/Docker-socket expansion ради O5;
- global Docker context changes, repository/Vault/live root binds;
- automatic UAC, reboot, firewall/security exclusion, license acceptance;
- broad cleanup/prune, volume/VHDX/key/backup deletion, in-place restore;
- unknown recipients, costs, secrets, destructive or external actions.

Необходимость любого исключённого пути означает scoped BLOCKED/STOP и новое owner-reviewed решение, а не «поиск обхода» внутри плана.

## Unknown до read-only preflight

Windows support/build/architecture; virtualization/features/WSL state; existing Docker/data/context; license eligibility; RAM/CPU/disk; storage protection/ACL/reparse/sync; App Control/AV; loopback port 5678; UAC/reboot need.

## Unknown до metadata/acquisition/runtime locks

Official current versions/hashes/signers/revocation/license text; OCI leaf digests; SBOM/scanner database and disposition; exact custom tool closure; installed equality and LKG import/recovery.

## Unknown до Docker capability tests

Actual endpoint identity; IPv4/IPv6 loopback; mock/gate no-egress; destination-broker enforcement; named-volume/nonroot/ownership/mount/signal/cleanup semantics; resource stability; deterministic pax loading; validator/collector separation. Mandatory unsupported predicate is BLOCKED, never assumed.

## Unknown до exact n8n/PostgreSQL tests

Native file secret support; no-persistence envelope relay; owner/2FA/recovery/import/credential behavior; exact migration graph; HMAC/constant-time procedure tool closure; representative encrypted Credential restore proof.

## Unknown до owner gates

Dev bot and production deny identity; allowlisted five-part tuple and synthetic data class; webhook/backlog decision; Telegram cap/TTL; DeepSeek model/price/USD/request/data limits; at-rest residual acceptance; roots/resource limits; backup destination/retention/RPO/RTO and independent key custody; cleanup/retirement decisions.

## Known scoped blocker

Under A-only, any required O5 row needing root, `CAP_SYS_ADMIN`, privileged, devices or backend access is `OFFLINE_BLOCKED_CAPABILITY`, global RC `31` for OFFLINE-required/all-scope claim. LAB/LOCAL can still pass their exact requested predicates. Plan v2 does not promise `OFFLINE_READY`, delivery readiness or production readiness.

DeepSeek exact live model/pricing/currency and provider usage reconciliation remain unknown until separate source/owner gates; design contract requires worst-case reserve-before-request and treats ambiguity as consumed. Telegram/DeepSeek brokers do not terminate TLS, so HTTP policy evidence belongs to the narrow secret-bearing client, while broker evidence is limited to destination/SNI/DNS/IP/port.

`backup-verifier` identity and result contract are design-resolved, but exact image/tool/UID/tmpfs behavior is runtime unknown. Wrong-key/tamper/forgery/teardown outcomes cannot be claimed before execution.

## Residual risks that cannot be designed away

- Trusted Windows/Docker control principals can access runtime data and secrets.
- VHDX/pagefile/hiberfil/SSD/dumps may retain data; secure erasure is not promised.
- Public CA/DNS/Telegram/DeepSeek and vendor supply endpoints are external trust dependencies.
- Encrypted full DB backup contains protected verifier/ACK keyring; compromise of ciphertext plus age identity exposes it.
- Hash equality proves bytes/provenance, not semantic correctness.
- Docker Desktop application rollback may not restore equivalent feature/data state.
- Candidate new-ref creation is not reconciliation into the user's dirty checked-out branch.

Every residual must appear in the relevant owner card and final scoped result. Unknown/unreadable/contradictory evidence blocks rather than defaults.
