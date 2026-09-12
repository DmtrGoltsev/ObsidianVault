Историческая исходная матрица 7 сентября. Не использовать её колонку статуса как актуальную. Текущие 284/0/14 и 298 случаев: [QA_EMULATOR_PROD_MATRIX.md](qa/QA_EMULATOR_PROD_MATRIX.md).

# Матрица приёмочного тестирования Poruchik MVP0

Статус: рабочий план критического QA-аудита на 7 сентября 2026 года. Матрица описывает целевое состояние следующего выпуска после исправления P2 и добавления полного редактирования задач. Факт прохождения конкретного сценария фиксируется отдельно; наличие строки в этой матрице не означает, что тест уже выполнен.

## 1. Цель и границы

Выпуск MVP0 принимается только как единая система:

```text
Android → публичный HTTP proxy → Gateway → Task Core → PostgreSQL
Android ← FCM signal ← push outbox ← Task Core
Android → Task Run → relay → OpenClaw → n8n → Action Executor → Task Core
```

Проверяются Android, Gateway, Task Core, Action Executor, relay, OpenClaw, n8n, PostgreSQL, FCM и выпускной APK. Пострегистрационный мобильный runtime использует прямой HTTP к `154.59.110.121`; SSH применяется только в процедуре первичного bootstrap приглашения и в операторском доступе. Старые постоянный SSH-туннель и WebSocket не являются основанием для приёмки runtime.

Источники требований:

- `docs/PROJECT_HANDOFF.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `TEST_STATUS.md`, `OPERATIONS_AND_RELEASE.md`;
- `contracts/mobile.openapi.yaml`, `contracts/internal.openapi.yaml`, схемы и политики в `contracts/`;
- Android UI, repository ports, Room, sync и push-код в `app/`, `core/`, `feature/`;
- `N8NAgents/docs/PORUCHIK_INTEGRATION.md`, OpenClaw plugin 0.2.1, relay и workflow n8n;
- production E2E от 6 сентября 2026 года.

Обозначения уровней:

- **U** — модульный тест с заглушками, без сети;
- **I** — интеграционный тест компонента с реальной БД или HTTP-заглушкой;
- **B** — вызов backend/API без Android UI в изолированном тестовом workspace;
- **A** — Android-инструментальный тест на локальном эмуляторе;
- **E** — полный E2E на production через локальный Android-эмулятор;
- **O** — эксплуатационная read-only проверка production.

Статусы исходного покрытия: **есть** — сценарий подтверждён применимым тестом; **частично** — проверена только часть пути; **устарело** — тест относится к прежнему transport; **нет** — необходим новый тест.

## 2. Жёсткие условия прогона

1. До первого production write создаётся ledger с уникальным префиксом прогона, workspace, principal, device, invitation, API session, task, run, proposal, approval, assignment, document, inbox, outbox, push delivery, audit и OpenClaw session/file ID.
2. Используются только созданные прогоном сущности. Данные владельца не изменяются и не удаляются.
3. Секреты, bearer-токены, invite payload, Firebase service account, HMAC и приватные ключи не попадают в команды, снимки экрана, отчёты и git.
4. Перед и после прогона фиксируются число workspace/principal владельца, health/restart всех контейнеров, Flyway version, outbox ready/DLQ, зависшие `QUEUED` runs и fingerprints активных workflow/package.
5. Для сетевых сбоев используются управляемые эмулятором airplane mode/network shaping либо тестовые заглушки. Намеренное нарушение production FCM или остановка общих сервисов допускаются только в отдельном окне с rollback; до него DLQ и восемь ошибок доказываются интеграционно.
6. После прогона удаляются только ID из ledger; затем доказываются нулевые ссылки тестового workspace во всех связанных таблицах и отсутствие тестовых OpenClaw sessions/files.

## 3. Главная матрица функциональности

| ID | P | Область и сценарий | Уровни | Критерий приёмки | Исходное покрытие / требуемое действие |
|---|---:|---|---|---|---|
| AUTH-01 | P0 | Валидное одноразовое приглашение | U/I/B/E | Строгое fragment-only приглашение принимается один раз; создаются device/principal/session нужного workspace; повтор даёт стабильный отказ без второй учётной записи | Частично есть; повторить E на чистой установке |
| AUTH-02 | P0 | Невалидное, истёкшее, слишком большое и изменённое приглашение | U/I/A | Fail closed, стабильный код, никакой постоянной credential/session и утечки payload | Есть U; добавить A для пользовательского сообщения |
| AUTH-03 | P0 | PIN | U/A/E | Разрешены только 4–12 цифр; несовпадение не сохраняется; верный PIN открывает; неверный оставляет сессию заблокированной и показывает ошибку | Есть U и прошлый E; повторить E |
| AUTH-04 | P0 | Биометрия | U/A/E | Показывается только при доступности; успех открывает; cancel/failure не обходят lock; deep link сохраняется до успешной разблокировки | Частично есть; добавить A негативных исходов и E deep link |
| AUTH-05 | P0 | Cold start/restart с сохранённой сессией | U/A/E | Сессия восстанавливается в состоянии Locked; локальные данные недоступны до unlock; PIN setup не повторяется | Есть U и прошлый E; повторить обновление APK поверх данных |
| AUTH-06 | P0 | Access token expiry и refresh rotation | U/I/B/E | Один 401 запускает challenge + ES256 proof + rotation и повтор исходного запроса; старый refresh не переиспользуется; onboarding не повторяется | Есть U/I и прошлый E; повторить B/E |
| AUTH-07 | P0 | Refresh replay/revocation/logout | U/I/B/A | Replay/revoked family очищает сессию, локальную БД, push token и device keys; повторный logout идемпотентен | Частично есть U; нужен B/A с тестовой учётной записью |
| AUTH-08 | P1 | Telegram link nonce/status/revoke | I/B | Nonce одноразовый и краткоживущий; binding использует numeric ID; status не раскрывает секрет; revoke прекращает resolve | Контракт есть, Android UI нет; проверить API как доступную backend-функцию |
| NET-01 | P0 | Public allowlist и auth boundary | I/B/O | Health разрешён; каждый разрешённый `/v1/*` доходит до auth/domain; без bearer — 401; `/internal/*`, `/`, path traversal, `//` и лишний method — 404 | Частично есть; построить параметрическую матрицу всех маршрутов |
| NET-02 | P0 | Query string через proxy | I/B/E | `status`, `dueFrom/dueTo`, `cursor`, `afterSequence`, conversation pagination доходят без изменения; path policy проверяет только нормализованный path | Исправлено ранее; нужна регрессия для новых agent conversation endpoints |
| NET-03 | P0 | Idempotency/If-Match/problem | U/I/B | Все write требуют UUID idempotency key, versioned write — quoted positive If-Match; replay возвращает исходный результат; иной payload с тем же ключом отклоняется; 400/401/403/404/409/429 сохраняют code+trace | Частично есть; расширить на редактирование, push unregister, approvals |
| NET-04 | P1 | Direct HTTP policy | U/A/E | Приложение обращается к принятому production origin без SSH/WS; cleartext разрешён только точным принятым host; credentials отсутствуют в URL и логах | Частично есть; исправить устаревший машинный transport contract отдельным изменением |
| TASK-01 | P0 | Список и фильтры задач | U/B/A/E | Active/All/Done корректны; cancelled не попадает в Active/Done; server status/due range фильтры корректны; `+ Задача` всегда видна | Частично есть; добавить UI тест всех фильтров и B границ дат |
| TASK-02 | P0 | Создание online/offline | U/I/B/A/E | Непустой title до 300; local ID сразу виден; после sync заменяется canonical UUID; повтор sync не создаёт дубль; description/due/visibility сохраняются при online create | Offline есть; расширить новым UI/контрактом полей |
| TASK-03 | P0 | Полное редактирование title | U/I/B/A/E | 1–300 символов, пробельное/пустое значение отклонено; успешное изменение повышает version, обновляет Room/list/detail и создаёт один push | Нет; обязательный новый сквозной тест |
| TASK-04 | P0 | Полное редактирование description | U/I/B/A/E | До 20 000; omitted сохраняет, `null` очищает, значение заменяет; Unicode/русский текст не повреждается | Backend частично умеет; нет Android UI/API полного пути |
| TASK-05 | P0 | Полное редактирование dueAt | U/I/B/A/E | RFC3339 с offset; omitted сохраняет, `null` очищает, значение заменяет; календарь обновляется и использует Europe/Moscow; неверная дата отклоняется | I semantics есть; нет Android полного пути |
| TASK-06 | P0 | Полное редактирование visibility | U/I/B/A/E | Только PRIVATE/ASSIGNED/TEAM; version/ACL пересчитываются; недоступная чужая private задача остаётся скрыта как 404; push не содержит поле | Нет и отсутствует в текущем update contract; обязательный сквозной тест |
| TASK-07 | P0 | Совместное редактирование полей | U/I/B/A/E | Один merge patch атомарно изменяет выбранный набор; untouched поля сохранены; один version increment, audit и событие; отмена диалога не меняет данные | Нет |
| TASK-08 | P0 | Конфликт редактирования | U/I/B/A/E | Два клиента с одной version: первый применён, второй получает 409/currentVersion; UI сохраняет черновик, предлагает обновить, не делает silent overwrite | Частично status; нет для новых полей/UI |
| TASK-09 | P0 | State machine | U/I/B/A/E | Разрешённые переходы работают; выход из DONE/CANCELLED запрещён; DONE ставит completedAt; cancel не удаляет audit | Частично есть; параметризовать все переходы |
| TASK-10 | P0 | Результат задачи | U/I/B/A/E | До 50 000; offline queue; версия соблюдается; результат виден после restart; пустой UI draft не отправляется | Есть частично; повторить E Unicode и конфликт |
| TASK-11 | P0 | Offline chain | U/I/A/E | CREATE → status → result → DONE/cancel выполняется фазами после ID remap, с актуальными версиями, после прерывания продолжается без дублей | Есть U и прошлый E; обязательный E повтор |
| TASK-12 | P1 | Карточка по deep link | U/A/E | Точная существующая задача открывается после foreground/background/cold start и unlock; системный Back возвращает список | Частично есть; E повтор |
| TASK-13 | P1 | Удалённая/невидимая задача | U/A/E | Online 404 приводит к понятному состоянию и выходу в список; offline deep link не висит бесконечно и после восстановления сети разрешается либо закрывается | Нет; обязательный push edge case |
| FOCUS-01 | P0 | Выбор, лимит и порядок | U/I/B/A/E | 0–20 активных уникальных задач; порядок сохраняется; 21-я недоступна; завершённые/удалённые исчезают; server version синхронизируется | U есть; нужен чистый E SET_FOCUS после ID remap |
| FOCUS-02 | P1 | Offline focus/conflict | U/I/A/E | Изменение ставится в outbox; local IDs переписываются; конфликт не теряется и не затирает сервер | U есть; нужен E conflict recovery |
| CAL-01 | P1 | Календарь | U/I/B/A/E | Только задачи со сроком и без CANCELLED; сортировка/группировка по Москве; today/tomorrow/overdue/DONE и границы суток/DST отображаются корректно | Частично U отсутствует для дат; добавить U/A/E |
| CAL-02 | P2 | Неверный dueAt из кэша | U/A | UI не падает, показывает диагностическое состояние «Время указано неверно» | Нет |
| INBOX-01 | P0 | Durable inbox и фильтры | U/I/B/A/E | События доступны без push; afterSequence монотонен; All/Decisions/Errors корректны; title/subject/task links сохраняются | Частично есть; добавить A фильтров и B pagination |
| INBOX-02 | P1 | READ offline | U/I/A/E | UNREAD→READ ставится в outbox, replay-safe; push сам состояние не меняет; RESOLVED не возвращается назад | Частично U; нужен E |
| ASN-01 | P0 | Назначение | U/I/B/A/E | Валидный assignee UUID; online-only; canRedelegate и выбранные document roots соблюдаются; version conflict/ACL дают понятный результат | Частично есть; нужен двухпользовательский E |
| ASN-02 | P0 | Решение назначения | U/I/B/A/E | PENDING→ACCEPT или DECLINE ровно один раз; повтор/конкурирующее решение 409; offline UI не обещает успех | Частично есть; нужен E обеих веток |
| ACL-01 | P0 | Изоляция OWNER/MEMBER/service | I/B/E | Владелец не видит private member task без назначения; assigned scope не расширяется; document access не шире task; role/identity spoof отклоняется | Частично I; нужен B двух principal |
| DOC-01 | P1 | Дерево документов | U/I/B/A/E | Метаданные строят устойчивый depth-first порядок, включая orphan/cycle без зависания; видны только разрешённые ветви | Частично; добавить U порядка/cycle и E |
| DOC-02 | P0 | Markdown read-only и кэш | U/I/B/A/E | Только `text/markdown` + readOnly; SHA-256 совпадает; mismatch/иной media type отклоняются; offline показывает последнюю проверенную копию и помечает её | Частично U; нужен B/A/E |
| DOC-03 | P0 | Запись документом через tool | I/B/E | Только подписанный service path, capability+approval, checksum/audit; mobile write отсутствует | Частично agent bridge; проверить tool E2E |
| APR-01 | P0 | Approval | U/I/B/A/E | APPROVE/REJECT online-only, один terminal decision; неверный decider/capability/run запрещён; inbox обновлён; side effect только после approval | Частично прошлый E; обе ветки и race обязательны |
| PROP-01 | P0 | Agent-derived proposal | I/B/A/E | Агент не создаёт активную задачу: сначала PENDING proposal; ACCEPT создаёт одну PLANNED task; REJECT ничего не создаёт; DELEGATE требует валидные данные | Частично I; полный E трёх решений |
| AGENT-01 | P0 | Текстовая команда | U/I/B/A/E | 1–20 000, русская Unicode строка; user message сохраняется; QUEUED→RUNNING→terminal; refresh обновляет одну запись in place | Частично есть; E повтор |
| AGENT-02 | P0 | История/пагинация/redaction | U/I/B/A/E | История принадлежит principal+conversation, limit 1–100, cursor без дублей; restart сохраняет; structured secret/internal result не отображается | Частично есть; нужен B/A pagination |
| AGENT-03 | P0 | P2: новый диалог после force-stop | U/I/B/A/E | Если во время force-stop появился новый conversation, первый ручной запуск после unlock через HTTP выбирает самый новый доступный conversation и показывает его terminal result без нажатия на notification | Нет; обязательный release blocker |
| AGENT-04 | P0 | P2 без ложного переключения | U/I/A/E | Известный текущий диалог не переключается на старый; explicit deep link имеет приоритет над latest fallback; malformed/cross-workspace conversation отклонён; отсутствие истории оставляет пустой чат | Нет |
| AGENT-05 | P1 | Ошибки/повтор | U/I/A/E | Network failure сохраняет user draft/понятное сообщение; FAILED/CANCELLED отображаются один раз; retry создаёт новый run/attempt, а не изменяет terminal run | Частично |
| VOICE-01 | P0 | Реальная русская речь | A/E | На Play-enabled AVD установлен/доступен русский recognizer; фразы с датой, временем, именами и пунктуацией распознаются на `ru-RU`; текст показывается до отправки | Не проверено; прежний блокер — нет русского language pack |
| VOICE-02 | P1 | Подтверждение/cancel/error голосового ввода | U/A/E | Recognizer cancel/failure не отправляет команду; «Использовать» переносит текст в редактируемый draft; пользователь может исправить; raw audio не сохраняется приложением | Частично по коду; нужны A/E |
| VOICE-03 | P1 | Серверный transcription contract | I/B | Audio size/type/expiry/delete-on-success/failure/cancel и confirm text проверены, если endpoint остаётся частью MVP0; иначе он явно исключён из runtime contract | Контракт есть, MobileController реализации не видно; требуется решение/сведение контракта |
| PUSH-01 | P0 | Регистрация и ротация FCM token | U/I/B/A/E | Token регистрируется после auth, не логируется/не возвращается; новый token заменяет старый; retry переживает sync failure; unregister отключает доставку | Частично; реальная rotation не проверена |
| PUSH-02 | P0 | События task/run/inbox/approval | U/I/B/A/E | Для каждого поддержанного события создаётся один data-only сигнал правильному устройству с корректной route/version; authoritative data загружается HTTP | Task/run E есть; inbox/approval нужны E |
| PUSH-03 | P0 | Privacy | U/I/B/E | Payload содержит только allowlisted routing identifiers; нет title, description, content, result, token, principal data | Есть; повторить после task edit |
| PUSH-04 | P0 | Deep link lifecycle | U/A/E | Foreground, background, process-dead и cold start; PIN и biometric; точная task/agent/inbox route; новый intent заменяет старый | Частично; полная параметрическая E матрица обязательна |
| PUSH-05 | P0 | Duplicate/stale/out-of-order | U/I/A/E | Event ID duplicate и version stale не запускают второй refresh/notification; newer принимается; порядок версий не откатывает Room | U/I есть; выполнить контролируемую live-инъекцию только в тестовый device/workspace |
| PUSH-06 | P0 | Permission denied/revoked | U/A/E | Authoritative refresh выполняется без уведомления; после выдачи permission следующие сигналы видимы; SecurityException не ломает worker | U есть; нужен E |
| PUSH-07 | P1 | Force-stop | A/E | Зафиксировано системное подавление FCM; после ручного запуска polling fallback восстанавливает task/inbox/agent и P2 latest conversation | Частично; повторить после P2 fix |
| PUSH-08 | P0 | Retry/backoff/DLQ | U/I/O | Publish только после commit; временные ошибки дают ограниченный backoff; после 8 попыток DLQ один раз; restart продолжает очередь; historical cutoff не сеет backlog | I есть; O read-only, разрушительный live fault не обязателен для релиза |
| PUSH-09 | P1 | Удалённая задача без сети | U/A/E | Нажатие не приводит к crash/вечному spinner; показан понятный recovery; после сети authoritative 404 закрывает маршрут | Нет |
| SYNC-01 | P0 | Pull cursor/atomic apply | U/I/B/A/E | Changes применяются до cursor advance; crash между фазами не теряет change; replay не дублирует; DELETE удаляет/скрывает сущность | Частично U/I; E interruption |
| SYNC-02 | P0 | Mutation boundary | U/I/B | Разрешены только пять offline actions плюс целевое расширение, если редактирование заявлено offline; approval/assignment/ACL/tool/docs/telegram остаются online-only | Есть для пяти; решение для offline task edit должно быть явно отражено в contract |
| SYNC-03 | P0 | WorkManager recovery | U/A/E | Unique work не дублируется; network loss даёт retry; reboot/process death продолжает; sanitized log не содержит токены/content | Частично U; добавить A/E |
| UI-01 | P1 | Навигация и back stack | A/E | Пять разделов, переход calendar/inbox→task, notification routes, системный Back, create dialog и document back работают без зацикливания | Smoke частичный |
| UI-02 | P1 | Пустые/loading/error состояния | A/E | Каждый экран имеет конечное понятное состояние и действие восстановления; loading не бесконечен после terminal 404/error | Частично; обязательный обход всех экранов |
| UI-03 | P1 | Конфигурационные изменения | A | Rotate/activity recreation сохраняют безопасные drafts, выбранный экран и edit dialog; не повторяют write | Нет |
| UI-04 | P1 | Доступность и локализация | A/E | Семантические labels есть у интерактивных элементов; touch targets/контраст приемлемы; пользовательские тексты на русском; длинные строки/клавиатура/scroll не перекрывают действия | Частично; ручной проход |

## 4. Матрица всех 18 инструментов агента

Для каждого инструмента выполняются четыре обязательных проверки: схема/границы параметров с заглушкой; прямой backend путь OpenClaw plugin → n8n → Action Executor → Task Core; вызов естественной русской командой через реальную модель; replay/ACL/approval/audit и точечная очистка. Read-only вызовы не должны создавать доменные мутации. Побочный эффект считается успешным только по авторитетному ресурсу Task Core и `audit=ALLOWED`, а не по тексту модели.

| ID | Инструмент | Подготовка и позитивный E2E | Обязательные отрицательные проверки | Ожидаемый эффект |
|---|---|---|---|---|
| T01 | `reminder_create` | Русская команда с Europe/Moscow, title/description/due, затем inline confirm | пустой/длинный title, неверная timezone/date, expired/cancel callback, duplicate callback | До confirm только pending; после confirm ровно одно активное напоминание |
| T02 | `reminder_list` | Список тестовых active/pending/cancelled с limit | limit 0/51, неверный state, отсутствие результатов | Ограниченный актуальный список без мутаций |
| T03 | `reminder_cancel` | Сначала authoritative list, затем cancel выбранного task/revision и confirm | случайный ID, stale revision, cancel дважды, отмена callback | Только выбранное напоминание отменено один раз |
| T04 | `reminder_reschedule` | List → новая дата/текст → confirm | stale revision, неверная дата/timezone, cancel/expired proposal | Старый срок авторитетен до confirm; после него одна новая revision |
| T05 | `reminder_confirm` | confirm и cancel валидного `C-…` token | malformed, чужой actor/chat, expired/replayed/уже terminal token | Атомарное terminal решение; клавиатура удалена; token скрыт от модели |
| T06 | `poruchik_create_task` | Human command создаёт task; agent-derived run создаёт proposal | 301-char/blank title, invalid visibility/date/UUID, agent-derived без run | Human: одна task; agent-derived: только PENDING proposal |
| T07 | `poruchik_update_task` | По очереди и одним вызовом title/description/status/due/result с expectedVersion и approval где нужно | stale version, terminal escape, null/omitted semantics, agent-derived без approval | Ровно одно допустимое изменение/version/event на вызов |
| T08 | `poruchik_list_tasks` | Без фильтра, status и due interval | invalid status/date/range, cross-workspace visibility | Только доступные задачи; ноль мутаций |
| T09 | `poruchik_assign_task` | Owner назначает member с/без redelegation и document roots после approval | без approval, stale version, чужой principal/document root, duplicate | Одно PENDING assignment, scope не расширен |
| T10 | `poruchik_decide_assignment` | Member ACCEPT и отдельный DECLINE | agent-derived вызов, чужой assignee, повтор/конкуренция | Ровно одно terminal/accepted решение |
| T11 | `poruchik_get_focus` | Получить пустой и непустой ordered focus | cross-principal, malformed context | Версия и порядок без мутаций |
| T12 | `poruchik_set_focus` | 0, 1, 20 задач; local/canonical IDs уже разрешены | 21, duplicate, completed/foreign ID, stale version, agent-derived | Один новый ordered snapshot |
| T13 | `poruchik_get_calendar` | Диапазон через границу суток Москвы | from≥to, invalid date, inaccessible tasks | Только доступные due tasks без мутаций |
| T14 | `poruchik_get_inbox` | afterSequence 0 и продолжение | negative sequence, cross-principal | Монотонный список без мутаций |
| T15 | `poruchik_read_documents` | Tree по task и конкретный разрешённый document | private/неназначенная ветвь, bad UUID, checksum/media mismatch | Только разрешённый Markdown; ноль write |
| T16 | `poruchik_request_approval` | Запросить каждую разрешённую capability для корректного task/run/decider | неизвестная capability, чужой decider/task, duplicate, taskless task-bound request | Одно PENDING approval и inbox event |
| T17 | `poruchik_decide_proposal` | Отдельные ACCEPT, REJECT, DELEGATE | agent-derived решение, чужой decider, повтор; DELEGATE без assignee | Одно terminal решение; ACCEPT создаёт одну task |
| T18 | `poruchik_decide_approval` | Отдельные APPROVE и REJECT | agent-derived решение, чужой decider, повтор/race | Одно terminal решение; side effect только после APPROVE |

Общие security cases для каждого Poruchik tool: identity fields в model payload запрещены; неизвестный tool/action и произвольные URL/headers/method отклоняются; HMAC с неверным key/body/path/timestamp/nonce отклоняется; replay nonce отклоняется; operation ID стабилен для повтора одного tool call; correlation и resource в ответе обязательны; ложный success и oversized/invalid JSON response отклоняются; Android run identity берётся только из process-bound context, Telegram identity — только из owner allowlist.

## 5. Детальная FCM-матрица

| Измерение | Значения, которые нужно покрыть |
|---|---|
| Сущность | `TASK_CREATED`, `TASK_CHANGED`, `TASK_RUN_CHANGED` RUNNING/WAITING/terminal, `INBOX_EVENT_CREATED`, `APPROVAL_DECIDED` |
| Состояние приложения | foreground; background; процесс выгружен; cold start; явный force-stop с последующим ручным запуском |
| Защита | уже unlocked; PIN; biometric success/cancel/failure; biometric unavailable |
| Permission | Android <33; Android 33+ granted; denied; revoked между проверкой и notify |
| Сеть | online; offline при получении; сеть восстановилась; timeout/401 с успешным refresh; permanent 404 target |
| Порядок | unique; duplicate eventId; одинаковая entity version с новым eventId; stale; newer; out-of-order newer→older |
| Token | первый token; rotation; старый token invalid; unregister; несколько устройств одного principal |
| Доставка сервера | accept после commit; transient retry; restart; 8 failures→DLQ; duplicate publisher claim; migration cutoff |
| Privacy | ни в payload, ни в notification нет пользовательского title/description/result/content/token; локальный текст нейтрален |

Каждая E-проверка FCM подтверждается тремя доказательствами: одна server delivery/outbox запись, один Android receive/decision без чувствительного logcat и правильное авторитетное состояние после HTTP sync. Наличие только provider message ID не доказывает получение устройством.

## 6. Контракты и backend без UI

Backend smoke должен параметрически пройти все mobile operation IDs: invitation redeem; refresh challenge/refresh/logout; push register/unregister; Telegram link nonce/status/revoke; sync; task list/create/detail/update; assignment create/decision; documents list/get; proposals list/decision; approvals decision; inbox list/update; focus get/put; calendar; agent text/history/latest conversation; voice transcription/confirm — либо явно удалить нереализованные operation из MVP0 contract.

Для каждого endpoint проверяются:

- valid happy path и границы размеров/дат/UUID;
- строгий JSON без неизвестных полей и trailing data;
- auth, workspace/role/ACL, 404 вместо раскрытия скрытой сущности;
- idempotency replay и payload mismatch;
- optimistic version race;
- audit без human content и один корректный outbox event;
- restart/retry там, где есть очередь или lease;
- соответствие OpenAPI реальному Gateway allowlist и MobileController.

Internal API отдельно покрывает context resolve, create/transition/list task runs, dispatch claim/complete/fail, proposals, effects, documents, inbox events, intent execute и Telegram consume/resolve. Все internal routes должны быть недоступны через публичный proxy и требовать HMAC с nonce replay protection.

## 7. Автоматизация, которую нужно исправить или добавить

| Приоритет | Набор | Требование |
|---:|---|---|
| P0 | Contract drift | Тест должен сравнивать все OpenAPI method/path с Gateway allowlist и фактическими MobileApi/MobileController; сейчас заметны расхождения direct HTTP policy, agent history/latest conversation и voice |
| P0 | Task edit | Unit для merge patch tri-state, API serialization, repository/Room; Task Core integration title/description/due/visibility+ACL+event; Compose UI test draft/save/conflict |
| P0 | P2 | Unit выбора conversation, MockWebServer latest/history, Room смены scope, activity cold-start/deep-link priority; production force-stop E2E |
| P0 | 18 tools | Табличный runner, который проверяет registration/schema/allowlist/n8n branch/Action Executor intent/Task Core outcome/audit для каждого имени |
| P0 | FCM | Параметрические publisher tests всех event types/routes/privacy; Android duplicate/stale/out-of-order и permission; live test-device injector с allowlist и ledger |
| P1 | UI | Compose tests auth, task filters/edit, focus, inbox decisions, docs, agent history, error/recovery, rotation |
| P1 | Calendar | Чистые функции date grouping/Moscow boundary/overdue/malformed date |
| P1 | Release | Скрипт формирует единый отчёт commit/image/Flyway/APK hash/signer/test results/health и не читает секретные значения |
| P2 | Legacy isolation | Старые tunnel/WS tests маркируются как bootstrap/legacy и не учитываются в post-enrollment release coverage |

## 8. Последовательность цикла «тестирование → исправление»

### Волна 0 — неизменяемый baseline

Read-only git/status, toolchain, production health, versions, active workflow/plugin fingerprints и owner counts. Локально выполняются существующие contract/unit/integration/lint/assemble. Любой исходный P0 фиксируется до изменений.

### Волна 1 — release blockers локально

Сначала P2 и полный task edit. Для каждого дефекта: воспроизводящий автоматический тест → минимальное исправление → узкий тест → весь затронутый модуль. После согласования контрактов запускается полный локальный набор Android/Gateway/Task Core/Action Executor/agent bridge/OpenClaw.

### Волна 2 — backend canary без UI

В отдельном workspace выполняются API matrix, ACL с OWNER+MEMBER, offline/replay/version races, documents, proposal/approval и 13 Poruchik tools. Каждая мутация сверяется с БД/audit/outbox по ledger. Ошибки исправляются локально, затем выпускается новый неизменяемый image tag и повторяется только затронутый canary плюс общий P0 smoke.

### Волна 3 — Android на локальном эмуляторе

Сначала чистая установка, затем обновление поверх предыдущего подписанного APK. Проходятся auth, task edit, offline chains, focus, calendar, inbox, documents, agent history/P2, voice и FCM состояния. Для реальной русской речи нужен Play-enabled AVD с рабочим `ru-RU` recognizer и подачей реального аудио/голоса; текстовая подстановка через `adb` не считается доказательством speech recognition.

### Волна 4 — полный production E2E

Изолированный ledger, все P0/P1 happy paths, 18 tools, push matrix с безопасной test-device инъекцией, force-stop recovery, session refresh, upgrade/cold install. После каждого исправления повторяются воспроизводящий сценарий, соседние инварианты и один сквозной smoke. Восемь реальных FCM failures на общей production инфраструктуре не обязательны, если интеграционный тест и read-only operational state подтверждены.

### Волна 5 — очистка и выпуск

Точечная cleanup по ledger, доказательство нулевых ссылок, owner baseline unchanged, 9/9 health, пустой недопустимый backlog. Фиксируются commit Android/backend/N8NAgents, image tags, Flyway, plugin version/fingerprint, signed APK versionCode/versionName/hash/signer и финальная таблица PASS/FAIL/NOT RUN.

## 9. Критерии выпуска MVP0

Выпуск разрешён, когда:

- все P0 и P1 строки этой матрицы имеют PASS либо согласованное и документированное исключение владельца;
- P2 новый диалог после force-stop проходит без нажатия на сохранённое уведомление;
- title/description/dueAt/visibility редактируются сквозным путём, конфликты не теряют черновик;
- все 18 tools прошли production E2E по одному разу, а побочные эффекты подтверждены Task Core/audit;
- реальная русская речь подтверждена на эмуляторе или явно исключена из MVP0 владельцем;
- task/agent/inbox/approval push пройдены в foreground/background/cold start, включая unlock и privacy;
- локальные unit/integration/lint/assemble, backend tests и contract drift gate зелёные;
- подписанный APK имеет одного ожидаемого signer, v2/v3, новый versionCode и проверен upgrade + clean install;
- production health, queues, DLQ, relay и данные владельца после cleanup соответствуют baseline;
- нет P0/P1 дефектов, непроверенных обязательных критериев и незаписанных production изменений.

## 10. Итог критического цикла 8 сентября 2026 года

1. P2 восстановления нового диалога закрыт на production: приложение было принудительно остановлено, backend создал новый диалог штатным подписанным маршрутом, а ручной запуск без уведомления после PIN выбрал новый диалог и показал terminal result через HTTP.
2. Мобильное редактирование `title`, `description`, `dueAt` и `visibility` прошло online и offline. Подтверждены очистка nullable-полей, авторитетная версия, повторная синхронизация и нейтральное FCM-уведомление. Конфликт двух клиентов и полный offline state-chain остаются частичным покрытием.
3. Ошибки отображения срока и фокуса исправлены и перепроверены новым подписанным APK: `15:30+03:00` отображается как `15:30` по `Europe/Moscow`, а непустой авторитетный focus snapshot появляется после refresh.
4. FCM-доставка сначала фактически падала до DLQ из-за отсутствия egress у Task Core. После добавления отдельной сети без публичных портов один новый `TASK_CHANGED` дошёл с первой попытки; системное уведомление было нейтральным и открыло точную задачу. Старые DLQ не переигрывались.
5. Все 13 инструментов Poruchik прошли положительный production E2E через Android или штатный подписанный runtime с реальными `task_run`, relay, n8n, Action Executor, Task Core и audit. Пять reminder-инструментов прошли регистрацию, схему и отрицательный `SCOPE_DENIED`; положительная Telegram-доставка не запускалась без разрешения на тестовый чат.
6. Двухпользовательский сценарий выявил cursor-gap: после принятия назначения новый исполнитель имел право чтения, но не получал старый `TASK` change. Исправление `23ff88e` публикует `TASK UPSERT` после `ASSIGNMENT ACCEPTED`. Изолированная PostgreSQL-регрессия прошла, затем новый production-сценарий дал последовательность `ASSIGNMENT` → `TASK UPSERT` → `CALENDAR_ITEM`; задача появилась у MEMBER после одного refresh.
7. Реальное русское распознавание речи не доказано. Три содержательные попытки исчерпаны: две завершились provider error 9, третья после выдачи `RECORD_AUDIO` не вернула callback за 60 секунд. Текстовая русская команда и обработка cancel/provider absence не заменяют это доказательство.
8. На отдельном MEMBER AVD FCM token не зарегистрировался: установленный Google Play services `261136038` старее требуемого `261200000`, журнал содержит `AUTHENTICATION_FAILED` и `FCM Registration failed`. OWNER-устройство с рабочим provider подтвердило production E2E; rotation/stale-token и multi-device остаются частичными.
9. В `N8NAgents` остаются многочисленные изменения соседней работы. Они не относятся к QA-артефактам этого цикла и не очищались, не откатывались и не включались в выпуск.

## 11. Статус прогона 2026-09-08 после production-цикла

Обозначения: **PASS** — весь критерий строки подтверждён; **ЧАСТИЧНО** — подтверждены исходники/локальные уровни, но отсутствует обязательный сквозной уровень; **BLOCKED** — проверка начата и остановлена конкретным внешним блокером; **NOT RUN** — фактический сценарий не запускался; **ИСКЛЮЧЕНО** — операция удалена из MVP0-контракта как несуществующий runtime.

Контрольные точки реализации: `1234be2` (P2 и task edit), `1354e71` (RSA bootstrap regression), `85de26d` (Москва), `23ff88e` (snapshot после принятия назначения). Локально прошли contracts 34, Gateway и Action Executor `go test ./...`, agent bridge 19, OpenClaw plugin 14, static 4, Android `test lintRelease assembleRelease`; финальное исправление назначения прошло изолированный PostgreSQL `mvn test` — 26/26, 0 skipped. Production Task Core работает на image `sha256:44aab7124416e91fd63b7f96da64df97cd14d389a7722c0b15c3aeaf461faa9b`, healthy, restart 0, Flyway v8 и egress без публичных портов.

Финальный подписанный APK: `C:\BackUp\Poruchik-Signing\Poruchik-MVP0-moscow-focus-signed-2026-09-08.apk`, SHA-256 `86fe125e367a5176ae92cd310ba6b133579aa2d0bf49836f6ef634365a3f8dff`, один ожидаемый signer, v2/v3. Все 616 payload-entry совпадают с последней unsigned-сборкой. Upgrade OWNER и MEMBER сохранил `firstInstallTime`, локальный PIN и сессию; чистая установка и RSA-pinned onboarding OWNER/MEMBER прошли.

Итог 63 строк: **PASS — 10, ЧАСТИЧНО — 43, BLOCKED — 1, NOT RUN — 8, ИСКЛЮЧЕНО — 1**. `PASS` ставится только там, где весь основной критерий строки подтверждён; положительный E2E отдельного инструмента отражён дополнительно в разделе 11.1.

| ID | Статус | Подтверждено | Что осталось |
|---|---|---|---|
| AUTH-01 | ЧАСТИЧНО | RSA pin совпал с listener; чистые OWNER/MEMBER приглашения приняты и bootstrap завершён | Повтор consumed invite и истечение в Android |
| AUTH-02 | ЧАСТИЧНО | Unit/contract негативных payload прошли; stale ECDSA fail-closed подтверждён | Android сообщения и отсутствие следов для всех вариантов |
| AUTH-03 | ЧАСТИЧНО | PIN создан на двух чистых AVD, mismatch не позволил сохранить, unlock после upgrade прошёл | Явный неверный PIN и границы 4/12 |
| AUTH-04 | NOT RUN | В коде сохранён biometric gate | Success/cancel/failure/deep-link E2E |
| AUTH-05 | PASS | Signed upgrade на OWNER/MEMBER сохранил firstInstallTime, сессию и Locked state | — |
| AUTH-06 | ЧАСТИЧНО | Refresh unit/integration исходного набора прошли | Production expiry/rotation на изолированной учётной записи |
| AUTH-07 | ЧАСТИЧНО | Локальная очистка/revocation покрыта частично | Production replay/revoke/logout |
| AUTH-08 | ЧАСТИЧНО | Контракт и backend код существуют | Изолированный API E2E |
| NET-01 | ЧАСТИЧНО | Contract allowlist; live/ready 200; tasks/runs/latest без auth 401; internal boundary прежнего baseline | Параметрический live обход каждого method/path |
| NET-02 | ЧАСТИЧНО | Query forwarding и новые agent routes покрыты контрактами | Authenticated pagination/filter E2E |
| NET-03 | ЧАСТИЧНО | Локальные idempotency/version/problem проверки | Production writes и race |
| NET-04 | PASS | Direct HTTP contract и authenticated OWNER/MEMBER runtime подтверждены production | — |
| TASK-01 | ЧАСТИЧНО | Production list, authoritative state и private/assigned visibility подтверждены | Все status/due filters |
| TASK-02 | ЧАСТИЧНО | Offline create regression прошёл локально | Production online/offline ID remap |
| TASK-03 | PASS | Title изменён online и offline; Room/list/backend/version и push подтверждены | — |
| TASK-04 | PASS | Description установлено и очищено в production, backend получил `NULL` | — |
| TASK-05 | PASS | dueAt установлено/очищено; `15:30+03:00` отображается по Москве как `15:30` | — |
| TASK-06 | ЧАСТИЧНО | PRIVATE/ASSIGNED/PRIVATE и двухпользовательская видимость проверены | TEAM и conflict/404 границы |
| TASK-07 | ЧАСТИЧНО | Совместный online edit и offline очистка полей атомарно синхронизированы | Cancel-draft и точный audit-count совместного patch |
| TASK-08 | ЧАСТИЧНО | Version conflict покрыт локально | Два production клиента и сохранение UI draft |
| TASK-09 | ЧАСТИЧНО | State machine tests прошли | Production UI/backend transitions |
| TASK-10 | ЧАСТИЧНО | Offline result regression прошёл | Unicode/conflict/restart E2E |
| TASK-11 | ЧАСТИЧНО | Offline repository chain tests прошли | Process interruption и real sync E2E |
| TASK-12 | ЧАСТИЧНО | FCM tap открыл точную существующую задачу; background lifecycle подтверждён | Cold unlock + системный Back |
| TASK-13 | NOT RUN | Recovery критерий зафиксирован | Deleted/invisible task route E2E |
| FOCUS-01 | ЧАСТИЧНО | Production focus v2 с одной задачей и Android refresh подтверждены | 20/21, порядок и удаление terminal |
| FOCUS-02 | ЧАСТИЧНО | Offline/version логика частично покрыта | Production conflict |
| CAL-01 | ЧАСТИЧНО | Production due task и форматирование Europe/Moscow подтверждены | Today/tomorrow/overdue и границы суток |
| CAL-02 | NOT RUN | Критерии описаны | Android grouping/overdue/malformed date |
| INBOX-01 | ЧАСТИЧНО | API/source покрытие | Pagination/read UI E2E |
| INBOX-02 | NOT RUN | Критерии описаны | Cross-device push/idempotency E2E |
| ASN-01 | ЧАСТИЧНО | OWNER→MEMBER назначение после approval, v6 и redelegation=false прошло production E2E | Document roots, stale/conflict и отказ без approval |
| ASN-02 | ЧАСТИЧНО | Два независимых ACCEPT прошли; повторный snapshot gap исправлен live | DECLINE, повтор и race |
| ACL-01 | ЧАСТИЧНО | MEMBER не видел PRIVATE до ACCEPT, `can_read=false`; после ACCEPT `can_read=true` и задача появилась | Service spoof, чужая private 404 и document scope |
| DOC-01 | ЧАСТИЧНО | Backend/plugin контракты | Tree/roots production E2E |
| DOC-02 | NOT RUN | Критерии описаны | Checksum/media/cache/offline E2E |
| DOC-03 | NOT RUN | Критерии описаны | Атаки path traversal/symlink в test fixture |
| APR-01 | ЧАСТИЧНО | REQUEST+APPROVE прошли production с audit и assignment side effect | REJECT, повтор и race |
| PROP-01 | ЧАСТИЧНО | ACCEPT прошёл production и создал ровно одну task | REJECT и DELEGATE |
| AGENT-01 | ЧАСТИЧНО | Многократный production text path QUEUED→RUNNING→SUCCEEDED подтверждён | Русская Unicode команда и FAILED/CANCELLED |
| AGENT-02 | ЧАСТИЧНО | Authenticated history/latest и restart restore подтверждены | Cursor pagination и redaction adversarial case |
| AGENT-03 | PASS | Force-stop, новый conversation, ручной launch/PIN и HTTP restore нового terminal result прошли | — |
| AGENT-04 | ЧАСТИЧНО | Приоритет deep link/latest и owner isolation проверены локально | Production explicit/cross-workspace cases |
| AGENT-05 | ЧАСТИЧНО | Draft/error код и local tests | FAILED/CANCELLED/retry production E2E |
| VOICE-01 | BLOCKED | `ru-RU` system recognizer и Google RecognitionService доступны; prerecorded harness собран | Три harness попытки исчерпаны до recognizer; реальный русский audio result не получен |
| VOICE-02 | ЧАСТИЧНО | ActivityNotFoundException и cancel/draft код проверены; raw audio приложением не создаётся | Authenticated UI cancel/use/edit/send E2E |
| VOICE-03 | ИСКЛЮЧЕНО | Несуществующие backend voice operations удалены из OpenAPI/Gateway | Ничего: системный recognizer является фактическим MVP0 runtime |
| PUSH-01 | ЧАСТИЧНО | OWNER registration работала и не изменилась при успешной доставке | Rotation/unregister/multi-device; MEMBER AVD provider устарел |
| PUSH-02 | ЧАСТИЧНО | Task/run publishers и реальная TASK_CHANGED доставка подтверждены | Inbox и approval receive на устройстве |
| PUSH-03 | PASS | Payload/privacy tests и live нейтральное `Задача обновилась` без пользовательских данных | — |
| PUSH-04 | ЧАСТИЧНО | Background notification и точный task deep link прошли; force-stop HTTP fallback прошёл | Foreground banner и cold notification unlock |
| PUSH-05 | ЧАСТИЧНО | Duplicate/stale/out-of-order локальные проверки | Контролируемая live injection |
| PUSH-06 | ЧАСТИЧНО | Permission/SecurityException логика покрыта локально | Android 33+ deny/revoke live |
| PUSH-07 | PASS | Production force-stop без notification → manual launch → latest HTTP restore прошёл | — |
| PUSH-08 | PASS | Реальные 8 failures/DLQ наблюдались; после egress fix новая delivery прошла attempts=1, старый DLQ не replay | — |
| PUSH-09 | NOT RUN | Критерий описан | Deleted target offline/recovery E2E |
| SYNC-01 | ЧАСТИЧНО | Cursor-gap назначения воспроизведён и исправлен; ASSIGNMENT→TASK→CALENDAR применились после refresh | Process interruption во время транзакции |
| SYNC-02 | PASS | Offline UPDATE_TASK синхронизировал title/null due/null description/PRIVATE с authoritative v3 | — |
| SYNC-03 | ЧАСТИЧНО | WorkManager/local retry код проверен | Reboot/process-death production E2E |
| UI-01 | ЧАСТИЧНО | Authenticated Tasks/Focus/Agent/Calendar/Inbox, task detail и notification route пройдены | Полный back stack/deep link cold lifecycle |
| UI-02 | ЧАСТИЧНО | Signed-out/error состояния проверены | Все authenticated loading/empty/error состояния |
| UI-03 | NOT RUN | Критерии описаны | Rotate/recreate draft/write проверки |
| UI-04 | ЧАСТИЧНО | Русские onboarding/error тексты и voice semantics проверены | Полный accessibility/long text/keyboard pass |

### 11.1. Статус 18 инструментов

Для T06–T18 положительный production E2E прошёл: реальная модель, n8n branch, Action Executor, Task Core outcome и audit подтверждены уникальными run/correlation ID в `docs/MVP0_BACKEND_QA_20260908.md`. Это **13 из 13 инструментов Poruchik**. Полная отрицательная матрица каждого инструмента остаётся частичной.

Для T01–T05 подтверждены регистрация, схема, локальные plugin/static tests и production `SCOPE_DENIED` без внешнего сообщения. Положительный Telegram E2E **BLOCKED** до предоставления изолированного собственного test chat либо явного разрешения владельца; сторонним получателям ничего не отправлялось.

| ID | Статус | ID | Статус | ID | Статус |
|---|---|---|---|---|---|
| T01 | BLOCKED positive | T07 | PASS positive | T13 | PASS positive |
| T02 | BLOCKED positive | T08 | PASS positive | T14 | PASS positive |
| T03 | BLOCKED positive | T09 | PASS positive | T15 | PASS positive |
| T04 | BLOCKED positive | T10 | PASS positive | T16 | PASS positive |
| T05 | BLOCKED positive | T11 | PASS positive | T17 | PASS positive |
| T06 | PASS positive | T12 | PASS positive | T18 | PASS positive |

### 11.2. Незакрытые выпускные ворота

MVP0 нельзя объявить полностью принятым без документированного решения по следующим воротам:

1. Реальная русская речь: `BLOCKED` после трёх попыток; нужен рабочий `ru-RU` provider/physical device либо явное исключение владельца.
2. Пять reminder tools: positive Telegram E2E не выполнялся без test chat/разрешения; отрицательный безопасный production path прошёл.
3. Обязательные негативные/edge E2E, оставшиеся частичными: refresh replay/logout, optimistic two-client conflict с сохранением draft, assignment DECLINE/race, proposal REJECT/DELEGATE, approval REJECT/race, FCM rotation/stale/duplicate/cold unlock и deleted-target recovery.
4. API 34 Android instrumented suite не запустился: загрузка system image трижды остановилась; смена worker не обнуляет лимит попыток. Основной production E2E выполнен на существующих Play-enabled AVD.
5. MEMBER AVD не зарегистрировал FCM token из-за устаревшего Google Play services; обновление требует штатного Play Store без внешнего аккаунта, иначе сценарий остаётся внешне заблокированным. OWNER FCM production E2E прошёл.
Production-fixtures очищены: по тестовому workspace нулевые ссылки, глобальный baseline восстановлен до 2 рабочих пространств / 2 principals / 1 device / 1 run, VPS invite artifact удалён. Локальные owner-only ledger/invite-файлы остались из-за отказа автоматической политики удаления; их содержимое не читалось и не раскрывалось.
