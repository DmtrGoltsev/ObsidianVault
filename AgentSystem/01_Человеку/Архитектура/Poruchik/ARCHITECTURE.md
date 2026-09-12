# Архитектура Poruchik

Актуально на 7 сентября 2026 года. Фактический production-релиз подтверждён прогоном от 6 сентября 2026 года.

## Границы системы

Poruchik состоит из двух локальных репозиториев:

- `C:\Users\style\Documents\Codex\Poruchik` — Android, Gateway, Task Core, Action Executor и контракты;
- `C:\Users\style\Documents\ChatGPT\Агенты\N8NAgents` — OpenClaw, relay, n8n-интеграция и эксплуатационная инфраструктура агента.

PostgreSQL является авторитетным хранилищем серверного состояния. Room является локальным источником интерфейсного состояния Android и очередью офлайн-операций. OpenClaw `MEMORY.md` не заменяет доменную базу: подтверждённые задачи, напоминания, approvals и аудит хранятся через серверные инструменты.

## Основной поток мобильных данных

```text
Android UI
  ↓ локальная запись
Room + очередь мутаций
  ↓ HTTP Bearer API
public HTTP allowlist proxy
  ↓
Gateway :18791
  ↓ подписанный внутренний запрос
Task Core :8080
  ↓
PostgreSQL (schema poruchik)
```

После onboarding рабочие `/v1/*` идут напрямую на `http://154.59.110.121/`. VPN, WebSocket и постоянный SSH-туннель не входят в активный runtime-путь. Машиночитаемый `contracts/policies/mobile-transport.json` и OpenAPI фиксируют этот direct HTTP путь; SSH сохраняется только для одноразового bootstrap приглашения и операторского доступа.

### Сессия и локальная защита

- приглашение одноразовое;
- access/refresh session хранится локально зашифрованно;
- refresh доказывает владение устройством;
- холодный запуск закрыт PIN или системной биометрией;
- logout/revoke может завершить семью сессий устройства;
- прямой HTTP не шифрует транспорт: это принятый риск MVP, а не эквивалент HTTPS.

## Офлайн-синхронизация

Изменение сначала записывается в Room. `SyncCoordinator` отправляет ожидающие операции последовательно по зависимым фазам. После `CREATE_TASK` локальный идентификатор заменяется каноническим серверным UUID; только затем отправляются status/result/cancel и связанные операции. Идемпотентные operation IDs предотвращают повторное применение после разрыва.

Проверенный сценарий: офлайн `CREATE → IN_PROGRESS → DONE → result` дал одну задачу на сервере, версию 4 и один результат; офлайн-отмена также не создала дубль.

## Push-first

```text
Доменная транзакция
  ├─ меняет данные
  └─ пишет outbox event
          ↓
     FCM publisher
          ↓ data-only, без предметного текста
       Android FCM
          ↓ WorkManager
    дедупликация в Room
          ├─ планирование HTTP sync ──> актуальные данные в Room
          └─ нейтральное уведомление + deep link
```

Публикуются типы:

- `TASK_CREATED`;
- `TASK_CHANGED`;
- `TASK_RUN_CHANGED`;
- `INBOX_EVENT_CREATED`;
- `APPROVAL_DECIDED`.

Payload ограничен техническими полями: event ID, тип, entity type/ID, версия и маршрут назначения. Он не содержит заголовок/описание задачи, сообщение или результат агента, access/refresh token и invite payload.

Дедупликация выполняется по событию и версии. Сервер хранит состояние dispatch, отдельные доставки устройствам, повторы и DLQ. После push Android всегда запрашивает авторитетное состояние. Если push потерян или запрещены уведомления, данные восстанавливаются синхронизацией при запуске, восстановлении сети, ручном обновлении и резервным polling.

Worker не ждёт завершения HTTP-синхронизации перед показом нейтрального уведомления: он планирует синхронизацию и создаёт уведомление как две ветви обработки принятого сигнала. При открытии цели интерфейс читает Room и получает обновление после завершения синхронизации.

Нажатие на уведомление:

- для задачи сохраняет маршрут `task/{taskId}`;
- для run сохраняет диалог агента;
- если приложение заблокировано, маршрут применяется после PIN/биометрии;
- после cold start цель не теряется.

## Агентный поток

```text
Android command
  ↓
Task Core: TaskRun QUEUED + outbox
  ↓ claim
task-run-relay
  ↓
OpenClaw + DeepSeek
  ├─ обычный ответ
  └─ типизированный инструмент
       ↓ HMAC
      n8n intent dispatcher
       ↓
      Action Executor
       ↓ HMAC + повторная авторизация
      Task Core
  ↓
TaskRun RUNNING/terminal + TASK_RUN_CHANGED
  ↓ FCM
Android GET /v1/agent/runs
```

OpenClaw не имеет filesystem/web/runtime/UI/automation/agent инструментов. Его allowlist содержит только 18 явно названных действий. Каждый побочный эффект проходит типизированный контракт, подписанный запрос, повторную авторизацию, идемпотентность и аудит. Агент не определяет личность, роль или результат approval самостоятельно.

## Компоненты и ответственность

| Компонент | Ответственность | Не должен делать |
|---|---|---|
| Android | UI, Room, offline queue, PIN/biometry, FCM, HTTP sync | хранить серверные секреты; считать push авторитетным состоянием |
| Public proxy | разрешить health и допустимые `/v1/*`, ограничить размер/частоту | публиковать internal/admin/n8n |
| Gateway | invitation/session/auth, allowlist маршрутов, сервисная подпись | выполнять доменную логику агента |
| Task Core | доменные инварианты, ACL, аудит, outbox, push publisher | доверять данным push или решению агента без проверки |
| PostgreSQL | авторитетное состояние и миграции Flyway | быть доступным из интернета |
| Relay | надёжно забрать `QUEUED` run и вернуть состояние | напрямую менять задачи |
| OpenClaw | модель, контекст и выбор разрешённого инструмента | выходить за allowlist |
| n8n | маршрутизация типизированного намерения | становиться публичным мобильным API |
| Action Executor | проверенный вызов Task Core и replay-защита | хранить пользовательскую истину отдельно от Task Core |

## Доменная функциональность

- задачи: `PLANNED`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`;
- task runs: `QUEUED`, `RUNNING`, `WAITING_INPUT`, `WAITING_APPROVAL`, терминальные состояния;
- назначения и решения;
- предложения агента: побочный эффект не активируется до решения человека;
- approvals и inbox;
- focus snapshot и calendar views;
- документы с ACL, не шире доступа к задаче;
- audit и change log;
- push registrations/deliveries/dispatch state.

## Топология production

- внешняя точка Android: `154.59.110.121:80`;
- Gateway: loopback хоста `127.0.0.1:18791` и внутренние Docker-сети;
- OpenClaw Gateway: loopback внутри контейнера `127.0.0.1:18789`;
- Task Core: внутренняя сеть, порт 8080;
- PostgreSQL: внутренняя сеть;
- n8n и Action Executor: внутренние сети `n8nagents_data` / `poruchik_internal`;
- FCM, DeepSeek и Telegram используют исходящий HTTPS независимо от незашифрованного мобильного HTTP.

## Связанные источники

- [Мобильный OpenAPI](../contracts/mobile.openapi.yaml)
- [Внутренний OpenAPI](../contracts/internal.openapi.yaml)
- [Машины состояний](../contracts/policies/state-machines.json)
- [Матрица доступа](../contracts/policies/access-matrix.json)
- [Офлайн-мутации](../contracts/policies/offline-mutations.json)
- [V8 push-first](../server/task-core/src/main/resources/db/migration/V8__push_first_outbox.sql)
- [OpenClaw allowlist](../../../ChatGPT/Агенты/N8NAgents/openclaw/openclaw.json)
- [Интеграция OpenClaw/n8n](../../../ChatGPT/Агенты/N8NAgents/docs/PORUCHIK_INTEGRATION.md)
