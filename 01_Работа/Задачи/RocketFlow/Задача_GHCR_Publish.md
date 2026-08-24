---
id: "task-ghcr-publish"
тип: "задача"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md"]
доказательства: ["Док_Prod_Deploy_State"]
теги: ["задача", "docker", "ghcr", "devops"]
---

# Задача: Первый remote publish бэкенд-образа через GHCR

## Описание

Выполнить первую успешную публикацию [[Docker_Image|Docker-образа]] бэкенда в GitHub Container Registry (GHCR).

## Контекст

Бэкенд может собираться как Docker image, но фактическая production model сейчас jar/systemd + web static на [[HexCore]]. Актуальный GHCR publish workflow отсутствует или требует восстановления; `production-deploy.yml` не является текущим deploy workflow. Фактический deploy workflow: `backend-hexcore-prod-deploy.yml`.

## Критерии приёмки

- [ ] Docker-образ бэкенда опубликован в GHCR
- [ ] Тег образа соответствует версии/коммиту
- [ ] GHCR workflow создан/восстановлен и успешно выполняет publish, либо принято явное решение не использовать GHCR в MVP3 production
- [ ] Если GHCR используется: [[HexCore]] может pull-ить образ из GHCR
- [ ] [[Док_Prod_Deploy_State]] обновлён после решения

## Связанные заметки

- [[MOC_DevOps]]
- [[Docker_Image]]
- [[Регламент_Деплоя]]
- [[Док_Prod_Deploy_State]]
