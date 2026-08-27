---
id: "review-input-n8nagents-docker-plan-architecture-v1"
тип: "ревью"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники: ["[[N8NAgents]]", "N8NAgents/docs/architecture.md"]
доказательства: []
теги: ["review-bundle", "architecture", "baseline"]
---

# Architecture baseline для ревью

## Production baseline

- n8n Community + PostgreSQL + Caddy в Docker Compose.
- Только Caddy публикует production 80/443.
- Telegram webhook проходит secret-header и allowlist до LLM/tools.
- DeepSeek native-tool compatibility требует live spike; deterministic router — documented fallback.
- Separate metadata/app/memory database boundaries и narrow tools.

## Proposed local delta

- Docker Desktop Linux containers, WSL 2 backend, но без отдельной Ubuntu distro.
- Local project name/volumes/secrets полностью отделены от production.
- n8n editor только `127.0.0.1:5678`; PostgreSQL не публикуется.
- Mock profile с internal-only services и проверяемым отсутствием egress.
- Real-dev profile с отдельным Telegram dev bot.
- Local inbound заменяет public webhook на long-polling bridge; общий downstream normalized contract должен оставаться тем же.
- DeepSeek real mode выключен по умолчанию.
- B2r/O5 запускаются одноразово без NIC и без Docker socket.

## Критичные boundaries

1. Windows user/Docker control plane — trusted operator boundary.
2. Docker Desktop managed VM — не доказанная сама по себе security boundary; capability/containment требует runtime tests.
3. Browser → loopback-only n8n.
4. Telegram API → bridge → authenticated internal n8n ingress.
5. n8n → internal PostgreSQL.
6. n8n/bridge → external APIs только в real-dev.
7. Dirty source repo → read-only input test containers.
8. Persistent volumes → encrypted backup + isolated restore.

## Review targets

Reviewer должен искать нарушения trust boundary, неявные egress paths, privilege expansion, расхождение local/production contracts, невозможный rollback, данные/секреты в evidence и ложные Linux capability claims.
