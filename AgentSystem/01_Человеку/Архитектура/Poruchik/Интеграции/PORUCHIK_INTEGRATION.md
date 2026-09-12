# Интеграция Poruchik с OpenClaw и n8n

Актуально на 7 сентября 2026 года. Канонический обзор всего проекта: [PROJECT_HANDOFF.md](../../../../Codex/Poruchik/docs/PROJECT_HANDOFF.md).

## Роли компонентов

- OpenClaw ведёт диалог, вызывает только разрешённые типизированные инструменты и использует модель DeepSeek.
- n8n принимает подписанное намерение и маршрутизирует сценарий.
- Action Executor проверяет replay/idempotency и вызывает Task Core подписанным запросом.
- Task Core повторно авторизует действие, применяет доменные правила и пишет аудит/outbox.
- task-run relay забирает `QUEUED` run из Task Core, запускает OpenClaw и возвращает `RUNNING`/terminal состояние.

OpenClaw не является базой задач. Операционная истина находится в PostgreSQL за Task Core.

## Активный runtime

- OpenClaw image закреплён digest в [provenance.json](../openclaw/dist/provenance.json).
- Плагин `n8nagents-actions`: версия **0.2.1**.
- Конфигурация: [openclaw.json](../openclaw/openclaw.json).
- Compose: [compose.openclaw.yaml](../openclaw/compose.openclaw.yaml).
- Relay source: каталог `openclaw/relay/`.
- Production commit репозитория: `cd5d65a` (`feat(openclaw): relay Poruchik task runs`).

Артефакты пакетов 0.1.x и 0.2.0 в `openclaw/dist` являются историческими. Текущий пакет — 0.2.1; источники версии и manifest должны совпадать.

## Разрешённые инструменты

### Напоминания — 5

- `reminder_create`
- `reminder_list`
- `reminder_cancel`
- `reminder_reschedule`
- `reminder_confirm`

### Poruchik — 13

- `poruchik_create_task`
- `poruchik_update_task`
- `poruchik_list_tasks`
- `poruchik_assign_task`
- `poruchik_decide_assignment`
- `poruchik_get_focus`
- `poruchik_set_focus`
- `poruchik_get_calendar`
- `poruchik_get_inbox`
- `poruchik_read_documents`
- `poruchik_request_approval`
- `poruchik_decide_proposal`
- `poruchik_decide_approval`

Итого: **18**. Список должен совпадать в:

- [openclaw.json](../openclaw/openclaw.json) → `tools.allow`;
- [openclaw.plugin.json](../openclaw/plugin/openclaw.plugin.json) → `contracts.tools`;
- регистрации функций в source плагина;
- n8n dispatcher и серверном контракте.

## Ограничения безопасности

По умолчанию deny. Запрещены группы filesystem, web, runtime, sessions, UI, automation, messaging, nodes, agents, media, а также gateway/cron/subagents. `elevated`, `codeMode`, native commands, configuration writes, control UI и terminal отключены. Telegram разрешён только владельцу из allowlist; группы отключены.

Каждый n8n/Task Core вызов использует HMAC и correlation/idempotency metadata. Секреты задаются только server-side environment. Их значения запрещено выводить в команды, evidence или документацию.

## Как добавить новый инструмент

Новый инструмент — это изменение контракта, а не только prompt.

1. Сформулировать пользовательское действие, входную JSON-схему, ответ и ошибки.
2. Определить, read-only это действие или побочный эффект; для side effect задать approval, capability, idempotency и audit event.
3. Добавить/изменить Task Core endpoint и авторизацию, затем интеграционный тест.
4. Добавить безопасный маршрут в Action Executor и replay-тест.
5. Добавить ветку в n8n intent dispatcher; workflow не должен хранить отдельную доменную истину.
6. Реализовать типизированную функцию плагина OpenClaw без произвольного URL/command/input passthrough.
7. Добавить имя в manifest и `tools.allow`; убедиться, что deny-группы не расширились.
8. Повысить версию plugin package, собрать tgz и обновить provenance/compose на точный новый файл.
9. Прогнать unit/contract/replay/security tests.
10. Развернуть canary с rollback и проверить один полный путь OpenClaw → n8n → Action Executor → Task Core → audit/outbox.
11. Обновить этот список и [TEST_STATUS.md](../../../../Codex/Poruchik/docs/TEST_STATUS.md).

Нельзя добавлять универсальные `shell`, `http_request`, `sql`, `eval`, filesystem или browser tools ради обхода типизированного контракта.

## USER.md, MEMORY.md и правила агента

- [USER.md](../openclaw/workspace/USER.md) — язык, часовой пояс и подтверждённые пользовательские предпочтения.
- [MEMORY.md](../openclaw/workspace/MEMORY.md) — только подтверждённые долговременные сведения.
- [openclaw.json](../openclaw/openclaw.json) — модели, каналы, plugins, allow/deny и runtime-политики.

Стиль/поведение меняется в USER/MEMORY только когда это действительно пользовательская долговременная информация. Доступ к новой системе или действие добавляется через инструментальный конвейер выше.

## Настройка n8n

n8n не публикуется как мобильный endpoint. Для UI используется SSH local forwarding:

```powershell
ssh -i C:\Users\style\.ssh\n8n-vps-ed25519 -N -L 5678:127.0.0.1:5678 root@154.59.110.121
```

Затем открыть `http://127.0.0.1:5678`.

При изменении workflow:

1. экспортировать текущую production-версию и зафиксировать fingerprint;
2. изменить копию, не live-workflow;
3. прогнать fixture/contract/replay и отрицательную HMAC-проверку;
4. импортировать новую версию неактивной;
5. выполнить canary;
6. переключить активность и сохранить старую версию для rollback;
7. проверить execution status, audit и отсутствие дублей;
8. удалить тестовые данные по ledger.

## Подтверждённый E2E

В production подтверждён полный read-only маршрут `poruchik_list_tasks`: OpenClaw увидел инструмент, n8n и Action Executor вызвали Task Core, audit записал `ALLOWED`, а побочных мутаций не появилось. Manifest/allowlist содержат остальные 17 инструментов, однако каждый из них отдельно на живом production не прогонялся — это прямо отмечено в [TEST_STATUS.md](../../../../Codex/Poruchik/docs/TEST_STATUS.md).

## Известные оговорки

- `cron` и `nodes` одновременно упоминаются в deny-настройках; предупреждения об этих именах не дают разрешений и считаются безвредными до отдельной чистки конфигурации.
- `full-delivery-scope-v1` и `phase-a` contracts описывают инфраструктурное управление N8NAgents и не являются спецификацией мобильного push Poruchik.
- `local/`, `.tmp*`, scheduler exports и старые tgz не являются источником production truth.
- `local/secrets/` должен быть явно исключён из git отдельным безопасным изменением; содержимое не переносить и не перечислять.
