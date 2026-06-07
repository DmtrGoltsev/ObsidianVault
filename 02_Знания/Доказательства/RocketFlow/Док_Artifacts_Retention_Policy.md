---
id: "proof-artifacts-retention-policy-2026-06-07"
тип: "доказательство"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["repo cleanup/audit 2026-06-07"]
доказательства: ["Док_Cleanup_Manifest"]
теги: ["доказательство", "artifacts", "retention", "security"]
---

# Док: Artifacts Retention Policy

## Правило после cleanup

Repo не является хранилищем тяжёлых evidence/build/cache artifacts. Компактные доказательства переносятся в Obsidian vault, релизные архивы — в внешний archive directory, secret-risk candidates не копируются.

## Retain

- Компактные visual/runtime proofs: `Активы\RocketFlow\evidence\...`
- Human-readable манифесты cleanup
- Production DB backups: `tmp/prod-db-backups`
- Локальные конфиги, которые нужны для разработки и игнорируются git

## Remove from repo

- `test-artifacts`
- ad hoc screenshots
- transient `tmp/**` кроме `tmp/prod-db-backups`
- browser logs
- build/cache dirs
- root release package tarballs после архивирования

## Do not copy

- `prod` paths
- `authenticated` paths
- любые secret-risk candidates

## Связанные заметки

- [[Док_Cleanup_Manifest]]
- [[Док_Prod_Deploy_State]]
