---
id: "n8nagents-stageb-workflows-runtime-pass-20260828"
тип: "доказательство"
статус: "выполнено"
проект: "N8NAgents"
владелец: "production-rollout"
создано: "2026-08-28"
обновлено: "2026-08-28"
уверенность: "высокая"
источники: ["Итог_INTERNAL_Rollout_PASS_N8NAgents_2026-08-28"]
доказательства: ["/opt/n8n-stack/shared/evidence/20260828T101500Z-post2fa-adoption-stageb-retry"]
теги: ["n8nagents", "production", "n8n", "workflows", "stage-b", "pass"]
---

# N8NAgents — Stage B: workflows и n8n runtime PASS

## Итог

**PASS.** На production VPS запущен только сервис n8n из текущего точного release. Повторный импорт, удаление данных, изменение конфигурации, Caddy или сетевой границы не выполнялись.

- release: `/opt/n8n-stack/releases/20260828T072000Z-15e14e3735d195e38d9c3d90a77976d1b0e1ad25`;
- release fingerprint: `aef467f0d54e39a53da217e8dbcceb8613fc3898ae43d741933cecec812bbc08`;
- n8n: `2.36.7`, running/healthy, `RestartCount=0`, `OOMKilled=false`;
- PostgreSQL: `17.11-alpine3.24`, running/healthy, `RestartCount=0`, `OOMKilled=false`;
- listener n8n: только `127.0.0.1:5678`;
- public ports `80/443/5432/2375/2376`: отсутствуют;
- Caddy и временные import networks: отсутствуют.

## Workflow state

- workflows: `8`;
- active: `0`;
- shared owner bindings: `8`;
- history rows: `8`;
- dependency rows: `83`;
- executions, credentials, webhooks, tags: `0`.

До и после запуска совпали:

- entity SHA-256: `6af7c66271184719da16af94d1b6697f4bdcbaf7c664654bf80db1fc99ed8914`;
- dependency SHA-256: `f2f4e3347b852f617d27b5ce03261045688ee4bc92bb2174de17b5e8a46d11e6`;
- полный DB tuple SHA-256: `5a54d5575b099ece05b8c4bae08c14dcd1943c71d44cc4062f2f07c24823da50`.

Следовательно, startup n8n не изменил импортированные сущности или derived dependency index.

## Корректировка валидатора

Из повторной проверки убрано ровно одно ошибочное условие: равенство `workflow_history.name` имени workflow. Для plain JSON import в n8n `2.36.7` это поле ожидаемо `NULL`. Все остальные проверки сохранены.

## Immutable evidence

- каталог: `/opt/n8n-stack/shared/evidence/20260828T101500Z-post2fa-adoption-stageb-retry`;
- каталог и файлы защищены immutable-флагом;
- `evidence.sha256` SHA-256: `187302923645ebe4e41fd097c2a1d40390f2fd75ebad73b009c2b7374883b64a`;
- `00-before.txt`: `f9f1ca1336a5a85752064a6c702ed8ece3413c09b2a5cc851a505052dc978389`;
- `01-after.txt`: `24f72f4faca459c71336c517ba9dd7eae3a23598367c903fa8012407459f5516`;
- operator script: `8b158f8bf650fafd95027ed38f1fb1b2d1e698a9babb7a1c8ced02a473c0105f`.

## Граница этапа

Stage B подтверждает внутренний production runtime и точные неактивные workflows. Публичный edge, credentials, Telegram/DeepSeek traffic, backup/restore и monitoring остаются последующими этапами.

Связано: [[Итог_INTERNAL_Rollout_PASS_N8NAgents_2026-08-28]], [[Очередь_Ручных_Действий_N8NAgents]].
