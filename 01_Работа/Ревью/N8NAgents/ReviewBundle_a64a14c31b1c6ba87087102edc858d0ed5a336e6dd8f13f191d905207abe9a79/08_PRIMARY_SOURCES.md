---
id: "review-input-n8nagents-docker-plan-primary-sources-v1"
тип: "источник"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "средняя"
источники: ["официальная документация поставщиков; требует live verification перед execution"]
доказательства: []
теги: ["review-bundle", "primary-sources", "docker", "n8n", "telegram"]
---

# Primary sources для обязательной проверки reviewer

Ссылки перечислены как маршруты к authoritative documentation. Bundle создан без internet browsing; поэтому exact current versions, hashes, license text и platform requirements должны быть проверены на дату будущего исполнения.

## Docker/Microsoft

- Docker Desktop Windows install: `https://docs.docker.com/desktop/setup/install/windows-install/`
- Docker Desktop WSL 2 backend: `https://docs.docker.com/desktop/features/wsl/`
- Docker Desktop license: `https://docs.docker.com/subscription/desktop-license/`
- Docker network `none`: `https://docs.docker.com/engine/network/drivers/none/`
- Docker network drivers/internal networks: `https://docs.docker.com/engine/network/`
- Compose profiles: `https://docs.docker.com/compose/how-tos/profiles/`
- Compose secrets: `https://docs.docker.com/compose/how-tos/use-secrets/`
- Docker Desktop backup/recovery: `https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/`
- Microsoft WSL install/status: `https://learn.microsoft.com/windows/wsl/install`

## Product stack

- n8n Docker installation: `https://docs.n8n.io/hosting/installation/docker/`
- n8n Docker Compose setups: `https://docs.n8n.io/hosting/installation/server-setups/docker-compose/`
- n8n environment variables/security: `https://docs.n8n.io/hosting/configuration/environment-variables/security/`
- n8n CLI/import/export: `https://docs.n8n.io/hosting/cli-commands/`
- Official PostgreSQL image: `https://hub.docker.com/_/postgres`

## Telegram/DeepSeek

- Telegram Bot API `getUpdates`: `https://core.telegram.org/bots/api#getupdates`
- Telegram Bot API `setWebhook`: `https://core.telegram.org/bots/api#setwebhook`
- Telegram Bot API `deleteWebhook`: `https://core.telegram.org/bots/api#deletewebhook`
- Telegram Bot API security/token guidance: `https://core.telegram.org/bots/features#botfather`
- DeepSeek API docs: `https://api-docs.deepseek.com/`

## Source acceptance rule

- Для technical/security утверждений reviewer опирается только на official vendor docs/specifications либо reproducible runtime evidence.
- Search snippets, blogs, форумы и remembered behavior не закрывают P0/P1.
- Если official source недоступен или противоречив, finding получает `BLOCKED`/`CHANGES_REQUIRED`, а не speculative GO.
