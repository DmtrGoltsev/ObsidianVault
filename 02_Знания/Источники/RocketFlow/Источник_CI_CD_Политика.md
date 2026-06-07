---
id: "src-cicd-policy"
тип: "источник"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md"]
доказательства: ["Док_Prod_Deploy_State", "Док_Android_Verification"]
теги: ["документация", "ci-cd", "процесс"]
---

# Источник: CI/CD Политика

## Путь

`docs/58-github-cicd-policy.md`

## Роль в проекте

Определяет политику CI/CD: воркфлоу GitHub Actions, триггеры, окружения, правила мёрджа, политику тегов.

## Краткое содержание

Основные воркфлоу: `backend-verify` (mvn test + build/smoke), `web-verify` (npm build), `android-verify` (unit/build/lint), `backend-hexcore-prod-deploy.yml` (production deploy на HexCore). `production-deploy.yml` не является актуальным workflow. GHCR publish workflow отсутствует или требует восстановления, поэтому Docker/GHCR остаётся open gate. Триггеры зависят от файлов workflow; для production factual state см. [[Док_Prod_Deploy_State]].

## Статус актуальности

Актуален на 2026-06-07 после cleanup/repo audit.

## Связанные заметки

- [[Регламент_CI_CD]] — регламент на основе политики
- [[Регламент_Деплоя]] — продакшен деплой
- [[Док_Prod_Deploy_State]] — фактический deploy state
- [[Агент_DevOps]] — ответственный за CI/CD
