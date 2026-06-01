---
id: "reg-cicd"
тип: "регламент"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-05-31"
уверенность: "высокая"
источники: ["docs/58-github-cicd-policy.md"]
доказательства: []
теги: ["регламент", "ci-cd", "процесс"]
---

# Регламент CI/CD

## Цель

Обеспечить автоматическую проверку качества кода при каждом push и PR через GitHub Actions.

## Область применения

Все изменения в репозитории RocketFlow. Воркфлоу определены в `.github/workflows/`.

## Воркфлоу

| Воркфлоу | Файл | Триггер | Проверки |
|----------|------|---------|----------|
| Backend Verify | `backend-verify.yml` | push, PR в main | mvn test, Docker build, /actuator/health smoke |
| Web Verify | `web-verify.yml` | push, PR в main | npm run build |
| Android Verify | `android-verify.yml` | push, PR в main | assembleDebug |
| Backend Deploy | `backend-hexcore-prod-deploy.yml` | manual / merge в main | Деплой на [[HexCore]] |
| Image Publish | `backend-image-publish` | manual workflow_dispatch | Публикация в GHCR |

## Триггеры запуска

- **Автоматически:** push в main, pull request
- **Вручную:** workflow_dispatch для деплоя и публикации образа

## Участники

- [[Агент_DevOps]] — владелец CI/CD
- [[Агент_Бэкенд]] — backend verify
- [[Агент_Веб]] — web verify
- [[Агент_Android]] — android verify
- [[Агент_QA]] — приёмка результатов

## Критерии успеха

- Все verify-воркфлоу зелёные
- PR не мёрджится при красных проверках
- Production деплой только при зелёном backend-verify

## Эскалация

При падении CI — [[Агент_DevOps]] диагностирует и либо чинит, либо эскалирует на [[Оркестратор]].

## Связанные заметки

- [[Источник_CI_CD_Политика]] — политика-источник
- [[Регламент_Деплоя]] — связанный регламент
- [[Агент_DevOps]] — ответственный
