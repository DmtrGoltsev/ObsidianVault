---
id: "agent-devops"
тип: "агент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-10"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/33-current-state-summary.md"]
доказательства: ["Док_Production_Rollout_20260810"]
теги: ["агент", "devops", "ci-cd", "деплой"]
---

# Агент DevOps

## Зона ответственности

- GitHub Actions CI/CD (ubuntu-24.04)
- [[Docker_Image]] сборка и публикация в GHCR
- Деплой на [[HexCore]] (systemd + Nginx)
- PostgreSQL 18.4 эксплуатация в production — [[Док_Production_Rollout_20260810]]
- Secrets management (без хранения секретов в коде)
- Мониторинг production

## CI/CD воркфлоу

- `backend-verify` — mvn test + Docker build + /actuator/health smoke
- `web-verify` — npm run build
- `android-verify` — assembleDebug
- `backend-hexcore-prod-deploy` — production деплой
- `backend-image-publish` — ручная публикация в GHCR

Файлы: `.github/workflows/`

## Права на решения

- Конфигурация CI/CD пайплайнов
- Выбор инфраструктурных решений
- Управление доступом к production

## Активные задачи

- GHCR publish (гейт)
- Staging notification certification (инфраструктурная поддержка)
- Поддержка production на [[HexCore]]

## Выполненные волны

- Wave A: backend CI
- Wave B: staging secrets
- Wave C: production deploy

## Связанные заметки

- [[Регламент_CI_CD]] — CI/CD регламент
- [[Регламент_Деплоя]] — регламент деплоя
- [[HexCore]] — production сервер
- [[Docker_Image]] — контейнеризация
- [[RocketFlow]] — проект
