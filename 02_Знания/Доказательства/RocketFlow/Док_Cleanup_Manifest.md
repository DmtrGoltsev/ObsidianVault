---
id: "proof-cleanup-manifest-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["repo cleanup/audit 2026-06-07"]
доказательства: ["Активы/RocketFlow/evidence/cleanup-2026-06-07"]
теги: ["доказательство", "cleanup", "artifacts", "repo-hygiene"]
---

# Док: Cleanup Manifest

## Итог

Cleanup/repo audit завершён 2026-06-07. Компактные доказательства сохранены в Obsidian vault:

`C:\Users\style\Documents\ObsidianVault\Активы\RocketFlow\evidence\cleanup-2026-06-07\`

Сохранено 50 файлов, 8.48 MiB: 45 PNG, 3 human-readable файла, 2 WEBM.

## Манифесты

- `cleanup-pre-manifest.csv`
- `cleanup-pre-size-summary.csv`
- `copied-evidence-manifest.csv`
- `skipped-secret-risk-manifest.csv`
- `deleted-targets-manifest.csv`
- `cleanup-post-summary-manifest.csv`
- `git-status-short-after-cleanup.txt`

## Что удалено или архивировано

- Удалено около 6.55 GiB cleanup-целей.
- `test-artifacts` удалён из repo; 517 tracked deletions staged через `git rm`.
- Удалены `screenshots`, `tmp-collapse-window.xml`, `tmp/**` кроме `tmp/prod-db-backups`, `browser-logs`, build/cache dirs.
- 10 root `rocketflow-web-sha-*.tar.gz` архивированы в `C:\Users\style\Documents\RocketFlow_Archive\release-packages\`.
- SHA256-манифест архивов: `rocketflow-release-packages-sha256-manifest.csv`.

## Что сохранено

- `.secrets`
- `tmp/prod-db-backups`
- local env
- `android/local.properties`
- `web/node_modules`

## Secret-risk boundary

452 copy candidates пропущены как secret-risk (`prod`/`authenticated` paths). Полный список только в `skipped-secret-risk-manifest.csv`; секреты не копировались в заметки.

## Связанные заметки

- [[Док_Artifacts_Retention_Policy]]
- [[Док_Prod_Deploy_State]]
- [[RocketFlow]]
