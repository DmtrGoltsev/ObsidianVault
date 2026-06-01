---
id: "src-cicd-policy"
тип: "источник"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md"]
доказательства: []
теги: ["документация", "ci-cd", "процесс"]
---

# Источник: CI/CD Политика

## Путь

`docs/58-github-cicd-policy.md`

## Роль в проекте

Определяет политику CI/CD: воркфлоу GitHub Actions, триггеры, окружения, правила мёрджа, политику тегов.

## Краткое содержание

Четыре основных воркфлоу: `backend-verify` (mvn test + Docker build + smoke), `web-verify` (npm build), `android-verify` (assembleDebug), `backend-hexcore-prod-deploy` (production деплой). Плюс `backend-image-publish` для ручной публикации в GHCR. Триггеры: push в main, PR, manual workflow_dispatch.

## Статус актуальности

Актуален.

## Связанные заметки

- [[Регламент_CI_CD]] — регламент на основе политики
- [[Регламент_Деплоя]] — продакшен деплой
- [[Агент_DevOps]] — ответственный за CI/CD
