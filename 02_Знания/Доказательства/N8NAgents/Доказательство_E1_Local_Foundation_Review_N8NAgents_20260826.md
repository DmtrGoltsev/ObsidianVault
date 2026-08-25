---
id: "evidence-n8nagents-e1-local-foundation-review-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Матрица_Совместимости_N8NAgents_2026-08-26]]"
доказательства: []
теги: ["n8n", "foundation", "local", "ревью", "go-local", "безопасность"]
---

# E1 — локальная foundation и независимое ревью

## Итог

Локальная foundation подготовлена и независимое ревью дало **`GO-LOCAL`**. Это разрешает только дальнейшую локальную работу с артефактами foundation; это не `GO` на серверное развертывание, не доказательство работающего бота и не acceptance production.

Поставленная ветка разработки: `codex/n8nagents-foundation`; проверенный HEAD: `1839a29e1620a670c80b1428bfb4d4f56ba867ac` (`fix(n8nagents): restore services after partial stop`). Ранее зафиксирован handoff «49+ артефактов»; после последующих исправлений точное число не объявляется в этой заметке без отдельной повторной инвентаризации.

## Локальные доказательства

- `./scripts/verify-static.ps1`: `PASS` для JSON, YAML с проверкой duplicate keys, ссылок/указателей JSON Schema, migration sentinel, статической Compose-топологии, Caddy route-гейтов, secret-like scan и PowerShell syntax.
- Временная, secret-free проверка через официальный PyPI разрешила `jsonschema 4.26.0` и `referencing 0.37.0`; все 12 Draft 2020-12 metaschemas и ссылки прошли `PASS`. DeepSeek fixtures: 6 positive / 3 negative — `PASS`; tool fixtures: 5 positive / 5 negative — `PASS`. Временное окружение после проверки удалено, project tree не изменялся.
- WSL доступен, но Linux distribution отсутствует, поэтому Bash syntax остаётся `BLOCKED-LOCAL`. Docker/Compose parser и runtime, Caddy container validation и disposable PostgreSQL также `BLOCKED-LOCAL`; import workflow, live integrations, persistence, external exposure и backup/restore этой локальной проверкой не подтверждены.
- Выполнена read-only проверка ветки и HEAD; сервер, VPS, SSH и production-сервисы этим evidence не затрагивались.

## Зафиксированные security outcomes foundation

- Модели доступны ровно пять недеструктивных инструментов: `tool_save_note`, `tool_search_notes`, `tool_list_notes`, `tool_create_reminder`, `tool_list_reminders`. Generic SQL, shell, filesystem, code execution, произвольный HTTP/URL, credentials, Docker, n8n administration и выбор получателя отсутствуют.
- PostgreSQL разделён на metadata, application и memory; runtime-роли имеют least privilege. `assistant_runtime` вызывает только пять fixed-search-path Security Definer API и не получает прямой DML, DDL или административные права; owner-роли `NOLOGIN`.
- Owner bootstrap закрыт: editor не публикуется до localhost-only bootstrap и завершения owner account/2FA.
- Edge делает Caddy: только он публикует `80/443`; webhook принимает exact JSON `POST /webhook/telegram-assistant`, ограничен 1 MB и возвращает `404` для остальных маршрутов.
- Persistence execution fail-closed: error execution data не сохраняется; live-подтверждение отсутствия чувствительных данных всё ещё требуется.
- Backup design требует exclusive quiesce, локального шифрования, подписи, off-host/immutable upload и isolated authenticated restore; дизайн не является проверенным restore drill.
- Исполняемый workflow JSON сознательно не добавлен: до live import gate не подтверждены exact n8n/node/runner contracts и credential binding.

## Раздельный deployment-статус

**`NO-GO` для server deployment.** A2 SSH discovery остаётся `BLOCKED-EXTERNAL`: A1 дошла до transport, pinned host key и public-key authentication, но session channel не выполнил remote command. До provider-console diagnosis нельзя начинать A2, hardening или mutations.

Даже после снятия SSH-блокера обязательны evidence: Docker/Bash/Compose и runtime checks, immutable image digests, n8n workflow import, Telegram/DeepSeek E2E, persistence/isolation, edge exposure, quiesced signed backup и authenticated isolated restore. Никаких секретов, workflow exports или server facts в этой заметке нет.

## Связанные заметки

- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Матрица_Совместимости_N8NAgents_2026-08-26]]
- [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]
