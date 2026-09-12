---
id: "review-input-n8nagents-docker-plan-exclusions-v1"
тип: "ревью"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"]
доказательства: []
теги: ["review-bundle", "exclusions", "unknowns"]
---

# Exclusions и unknowns

## Явно исключено

- Plan B: отдельная Ubuntu WSL distro.
- Hyper-V VM, Windows Sandbox, v86/QEMU.
- Production VPS testing/deployment и provider UI.
- Public Caddy, TLS, DNS, tunnels и webhook exposure.
- Kubernetes/Swarm/Windows containers.
- Production Telegram bot token локально.
- Secret values и raw PII в review.
- Repo implementation до решения по review.
- Destructive Docker/WSL cleanup.

## Неизвестно до read-only preflight

- Windows support state, virtualization, WSL features, Docker installation/data.
- Hardware resources и disk quota.
- License eligibility.
- Corporate security policy/antivirus/App Control effects.
- Exact current official Docker Desktop version/hash/publisher certificate.
- Port conflicts.

## Неизвестно до capability/runtime tests

- Loopback publication behavior на фактическом host, включая IPv6.
- Mock network действительно без egress.
- Overlay/named-volume behavior для `chattr`, mountinfo, nested/same-device binds.
- Signal/cleanup semantics WSL kernel + Docker Engine.
- Resource stability n8n/PostgreSQL на host.
- Exact n8n 2.36.7 workflow/credential/node contracts.
- Credential decryptability verification без unsafe export.

## Неизвестно до owner manual gate

- Наличие отдельного dev Telegram bot.
- Разрешение снять webhook у dev bot.
- Allowlisted test chat/user и test data class.
- Применимый local Telegram/DeepSeek budget.
- Backup retention/destination/key custody.
- Local owner/2FA readiness.

## Требование reviewer

Не заполнять unknown предположением. Если unknown делает claim/acceptance недоказуемым, создать finding с точным preflight/runtime/manual gate и stop condition.
