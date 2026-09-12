# Независимая матрица приёмки: эмулятор и production backend

Дата среза: 2026-09-09. Авторская область: QA lead 3. Это проектирование проверок; в ходе подготовки матрицы production не изменялся, тестовые запросы не отправлялись и физический телефон не использовался.

## 1. Область и источники

Матрица покрывает реализованный MVP0 по актуальным исходникам и контрактам двух репозиториев:

- `contracts/mobile.openapi.yaml`, `contracts/internal.openapi.yaml`, схемы и политики в `contracts/`;
- Gateway, Task Core, Android `app`, `core/*`, `feature/*`, миграции Flyway и существующие модульные/интеграционные тесты;
- `N8NAgents/openclaw/plugin/dist/{index,core}.js`, контракты инструментов, миграции `005`–`011`, активные шаблоны n8n планировщика и подтверждений;
- `docs/ARCHITECTURE.md` и `docs/PROJECT_HANDOFF.md` как описание фактической топологии.

В таблицах «production» означает ограниченную функциональную проверку на изолированной области, без нагрузочного тестирования, DoS, перебора путей вне опубликованного API и воздействия на данные владельца. Любая мутация получает уникальный маркер и заносится в журнал фикстур до выполнения.

Контракт конфликта синхронизации фиксируется особо: `/v1/sync` отвечает HTTP 200 с результатом операции `CONFLICT`, `currentVersion` и `errorCode=VERSION_CONFLICT`. Ожидание отдельного HTTP 409 для пакетной синхронизации является ошибкой теста. Прямой `PATCH /v1/tasks/{taskId}` при конфликте версии по-прежнему проверяется как HTTP 409.

Текущие незавершённые локальные Android-изменения считаются кандидатом следующей сборки. Кейсы, зависящие от панели разрешения конфликта и повторной отправки только изменённых полей, помечены зависимостью `APK-CONFLICT`; production-фикстура конфликта остаётся неизменной до этой сборки.

## 2. Обозначения, оракулы и доказательства

| Обозначение | Значение |
|---|---|
| `Л` | локальный автоматический тест без production |
| `П` | ограниченная проверка production API или очереди |
| `Э` | Android-эмулятор с подписанной сборкой |
| `Т` | настоящий доверенный Telegram-чат и подлинное нажатие пользователем |
| `Ф` | физическое устройство; до отдельного этапа эти кейсы не выполняются |
| `+` | позитивный сценарий |
| `−` | отрицательный сценарий |
| `Г` | граничное значение |
| `С` | сценарий с состоянием или последовательностью |
| `К` | конкурирующий сценарий |

Для позитивной мутации достаточное доказательство состоит из ответа API/инструмента, авторитетного ресурса Task Core, ровно одной разрешённой записи аудита и ожидаемого события/outbox. Текст модели или карточка интерфейса без серверного оракула не доказывает побочный эффект. Для отказа нужны код/результат, отсутствие изменения версии и нулевые доменные побочные эффекты. Секреты, bearer-токены, ключи, callback token и содержимое приглашений в доказательства не попадают.

Каждый production-журнал хранит: workspace/principal/device/session, conversation/run, task/document/proposal/approval/assignment, idempotency key, correlation ID, outbox/delivery, исходные счётчики и процедуру точечной очистки. После группы проверяется ноль ссылок только на её маркеры и неизменность исходного состояния.

## 3. Параллельные группы и общие ресурсы

| Группа | Область | Изоляция | Общие ресурсы | Зависимости | Правило параллельности |
|---|---|---|---|---|---|
| G0 | локальные контракты и сборка | отдельные процессы/БД | рабочее дерево, Gradle, Docker | нет | параллельно по модулям; один процесс пишет отчёт |
| G1 | публичная граница и сеть | без доменных фикстур | public proxy, Gateway | health baseline | параллельно с G2–G7; малая частота, без flood |
| G2 | invitation/auth/session/device/link | workspace `AUTH-*`, отдельные ключи | Gateway identity DB | G1 route smoke | цепочки одной session family последовательны; разные principals параллельны |
| G3 | задачи, ACL, решения | workspace `CORE-*`, OWNER+MEMBER | Task Core DB | действующие сессии G2 | разные task branches параллельны; одна version-chain последовательна |
| G4 | offline sync и устойчивость | workspace `SYNC-*`, отдельный Android clientId на AVD | Task Core cursor/outbox, Room | G2, подписанный APK | разные AVD/workspaces параллельны; remap/conflict/retry внутри цепочки последовательны |
| G5 | документы | workspace `DOC-*`, отдельная задача/ветви | Task Core documents | G3 ACL | чтение ветвей параллельно; создание дерева и изменение checksum последовательно |
| G6 | агент и 13 Poruchik tools | workspace `AGENT-*`, отдельные conversations/tasks | Gateway, Task Core, relay, OpenClaw, n8n | G2, healthy runtime | read-only tools по разным conversations параллельны; мутации одной сущности последовательны |
| G7 | run lifecycle/history | workspace `RUN-*`, без push registration | Task Core dispatch, relay/OpenClaw | G6 runtime | SUCCEEDED/FAILED/CANCELLED в разных conversations параллельны |
| G8 | FCM | workspace `PUSH-*`, один явно выбранный QA device | FCM project, Task Core publisher | G2 registration, healthy egress | события посылаются по одному; серверные локальные тесты параллельны |
| G9 | Telegram и напоминания | существующий приватный owner-chat, один маркер | Telegram bot/chat, OpenClaw, n8n schedulers | healthy runtime и сохранённый baseline | строго последовательно; только подлинные сообщения/нажатия пользователя |
| G10 | восстановление, deep link, UI | AVD snapshots и отдельные profiles | Emulator, Room/Keystore | G2/G4, стабильная сборка | несколько AVD параллельны; process-death цепочка на одном AVD последовательна |
| G11 | очистка и выпуск | журналы всех групп | production DB, артефакты | завершение группы | один cleanup writer на workspace; не параллелить с мутациями этого workspace |

Допустимый общий запуск: G0, G1, G2 на разных principals, G3 на разных задачах, G5, G6 на разных conversations и G7 выполняются одновременно. G8 сериализует только реальные push-события. G9 всегда выполняется отдельно от других Telegram/n8n действий. Развёртывание, миграция, restart общего сервиса и очистка являются глобальными барьерами: в это время production-сценарии приостанавливаются.

## 4. Среда, контракты и публичная граница

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| ENV-01 | G0 | Л,+ | чистый checkout и отдельно текущее дерево | собрать список commit, версий схем, image/plugin/APK fingerprint | все компоненты однозначно сопоставлены; незакоммиченные файлы перечислены и не затёрты | status, hashes, manifest |
| ENV-02 | G0 | Л,+ | доступен toolchain | собрать Gateway, Task Core, Android и plugin; запустить существующие unit/integration tests | сборка воспроизводима; 0 failed/0 skipped в обязательных наборах | отчёты Go/Maven/Gradle/Node |
| ENV-03 | G0 | Л,− | OpenAPI и маршрутизаторы | сравнить method/path всех 29 mobile и 9 internal операций | нет опубликованного маршрута без обработчика и нет лишнего public route | машинный diff списков |
| ENV-04 | G0 | Л,+ | схемы JSON/SQL | проверить 18 имён инструментов и payload schemas против plugin/action executor | каждое имя зарегистрировано один раз и имеет типизированный путь | inventory + schema tests |
| ENV-05 | G0 | Л,+ | чистая PostgreSQL | применить Flyway с нуля и повторно проверить metadata | миграции последовательны; SECURITY DEFINER/search_path/owner/ACL сохранены | schema history и metadata |
| ENV-06 | G0 | Л,− | логи тестового запуска | искать bearer, refresh token, private key, invite payload, callback token, human content | чувствительных значений нет | redaction scan с именами правил |
| NET-01 | G1 | П,+ | production read-only | GET live/ready через public endpoint и внутри контейнера | 200, ожидаемые service/version, без доменной мутации | timestamp/status/health |
| NET-02 | G1 | П,−,Г | без auth | проверить неизвестный путь, вложенный `/admin`, неверный method, OPTIONS, двойной slash, `..`, percent-encoded traversal | единый 404 до auth; ни один запрос не попал в Task Core | status + Gateway counter/log |
| NET-03 | G1 | П,− | без auth | вызвать каждый защищённый allowlisted route без bearer | 401, без раскрытия ресурса | route/status matrix |
| NET-04 | G1 | Л/П,− | public host | обратиться к `/internal/v1/*`, n8n webhook и служебному порту через public proxy | маршрут недоступен снаружи | 404/connection boundary |
| NET-05 | G1 | Л,Г | тестовый handler | body ровно лимит, limit+1, неверный Content-Length, медленный body в пределах тестового стенда | допустимый body обработан; превышение/timeout ограничены, процесс жив | status/elapsed/health |
| NET-06 | G1 | Л,+ | proxy unit fixture | проверить POST body, keep-alive, query, correlation и stripping bearer на internal boundary | байты/метод/query сохранены; mobile bearer не проброшен как service identity | captured upstream request |
| NET-07 | G1 | Л,− | proxy unit fixture | spoof `X-Forwarded-For`, correlation/service headers | недоверенные заголовки заменены/отброшены | upstream headers без значений секретов |
| NET-08 | G1 | П,Г | малая серия запросов | проверить лимит unauthenticated и authenticated ровно у границы, без нагрузки | отдельные квоты, 429 после границы, восстановление по окну | counts/status; не более договорённого лимита |
| NET-09 | G1 | Л,− | конфигурация upstream | неподдержанный scheme/host/IP, redirect и upstream failure | fail closed, 502/служебная ошибка без утечки | error code + health |
| NET-10 | G1 | П,+ | current network | подтвердить порт 80 → public proxy → Gateway, DNS/TLS egress Task Core к FCM/OAuth | заявленная топология доступна; внутренних портов снаружи нет | socket metadata/health, без packet payload |

## 5. Регистрация, аутентификация, сессии, устройства и Telegram-link

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| AUTH-01 | G2 | П/Э,+,С | новое приглашение `AUTH-*`, новая пара ключей | вставить корректную invitation URI, создать PIN, redeem один раз | workspace/principal/device/session созданы один раз, роль верна, private key остаётся на клиенте | HTTP, DB IDs/counts, экран без payload |
| AUTH-02 | G2 | Л/Э,−,Г | экран приглашения | wrong scheme/path, missing/invalid/oversized payload, whitespace вокруг валидной ссылки | валидная с пробелами принимается; прочие не отправляются и дают понятную ошибку | UI + zero redeem audit |
| AUTH-03 | G2 | П,−,С | одно приглашение | повторить redeem тем же и другим ключом; попробовать после expiry/revoke | consume-once; повтор/истечение не создают principal/device/session | status/code + counts |
| AUTH-04 | G2 | П,− | invite для OWNER/MEMBER | подменить workspace, role, principal, bootstrap RSA payload/signature | сервер доверяет подписанному invitation artifact, подмена отклонена | error + zero rows |
| AUTH-05 | G2 | Э,+ | активная сессия, локальный PIN | lock/unlock правильным PIN; activity recreation/process death | локальное хранилище открывается, bearer не нужен до сетевого запроса; данные сохраняются | UI state + process generation |
| AUTH-06 | G2 | Э,−,Г | локальный PIN | неверный PIN, пустой, короткий/длинный, повторные ошибки | отказ без удаления данных/сессии; секрет не логируется | UI/log redaction |
| AUTH-07 | G2 | Э,+/− | biometric доступна | success, cancel, failure, unavailable с fallback PIN | только success открывает; cancel/failure не обходят PIN | UI + authenticator result |
| AUTH-08 | G2 | П,+,С | активная device-bound session | challenge → подпись ключом устройства → refresh | новая generation выдана, старая refresh credential погашена, device last_seen обновлён | session generations/audit |
| AUTH-09 | G2 | П,−,С | challenge AUTH-08 | replay challenge/signature, wrong device/key/alg, malformed DER/ES256, expired challenge | 401/400; generation и last_seen не меняются | status + before/after |
| AUTH-10 | G2 | П,−,Г | refresh request | timestamp/skew/nonce/body hash у границ; unknown fields/trailing JSON | строгий контракт; нулевые session side effects | status/code/counts |
| AUTH-11 | G2 | П,+,С | session family | сделать две последовательные штатные rotation | generations монотонны, только последняя credential активна | family graph/audit |
| AUTH-12 | G2 | П,−,С | после rotation | использовать предыдущее access/refresh значение | старый refresh отвергнут; политика access expiry соблюдена | status + active sessions |
| AUTH-13 | G2 | П,+,С | отдельная QA family | logout один раз, затем protected GET | logout завершает family, защищённый запрос 401 | audit/revoked_at/status |
| AUTH-14 | G2 | П,− | после logout | повторить logout старым bearer | допускается 401 согласно фактическому контракту; новых аудитов/сессий нет | status + audit delta0 |
| AUTH-15 | G2 | П,+,С | два устройства одного principal | revoke только QA device через официальный путь | его sessions/push недействительны; второе устройство работает | device/session/push rows |
| AUTH-16 | G2 | П,+,С | push registration QA device | PUT token, повтор PUT, rotation token, DELETE, повтор DELETE | одна активная запись; replay не дублирует; unregister не вызывает device revoke | status + registration history |
| AUTH-17 | G2 | П,− | QA device и чужой device UUID | попытаться удалить/заменить чужую registration | скрытый ресурс не раскрыт, чужая запись неизменна | 404/403 + hashes |
| AUTH-18 | G2 | П,+,С | active mobile session | создать Telegram link nonce, проверить status, consume подлинным trusted Telegram actor/chat | link появляется ровно один раз и относится к текущему principal | nonce metadata без nonce, link row/audit |
| AUTH-19 | G2 | П,−,С | nonce AUTH-18 | replay, expired, wrong actor/chat/bot, group chat, другой principal | link не создаётся/не меняется | status + link count |
| AUTH-20 | G2 | П,+,С | linked QA principal | DELETE link, status, повтор DELETE | link снят, Telegram resolve больше не возвращает principal; mobile session жива | status/audit |
| AUTH-21 | G2 | Л/П,− | internal service auth | wrong key id/signature/body hash/path/method/timestamp/nonce replay | fail closed до доменного кода | 401/403 + zero domain rows |
| AUTH-22 | G2 | Л/П,+ | разные service roles | вызвать каждый internal route разрешённой и другой ролью | работает только `x-allowed-service`, bound role нельзя подменить body | route/role matrix |
| AUTH-23 | G2 | П,− | OWNER и MEMBER разных workspaces | bearer A с resource/context B | workspace/principal берутся из session, body spoof игнорируется/отклоняется | 404/403 + audit denied |
| AUTH-24 | G2 | Э,С | signed upgrade | обновить APK тем же сертификатом поверх активного профиля | firstInstallTime/Room/Keystore/PIN/session сохраняются; миграции Room проходят | package metadata + UI/DB counts |

## 6. Задачи, состояния, ACL, предложения, согласования и назначения

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| TASK-01 | G3 | П/Э,+ | OWNER `CORE-*` | создать PRIVATE и WORKSPACE задачи с title/description/due/visibility | по одной v1, поля и московское отображение верны | API/DB/audit/outbox/UI |
| TASK-02 | G3 | П,−,Г | активная сессия | blank/301-char title, bad date/UUID/status/visibility, unknown field, non-JSON | 400, task/audit/outbox delta0 | response + counts |
| TASK-03 | G3 | П,+,С | task v1 | patch title, description, dueAt, visibility по очереди и вместе | версия растёт ровно один раз на запрос, только заданные поля меняются | versions/diff/audit/outbox |
| TASK-04 | G3 | П,+,Г | task с заполненными nullable полями | explicit null description/dueAt; omission; empty description | null очищает, omission сохраняет, пустое значение соответствует contract | before/after JSON |
| TASK-05 | G3 | П,−,Г | task vN | explicit null/non-text title/visibility; пустой title | 400, версия/audit/outbox неизменны | invariant counts |
| TASK-06 | G3 | П,−,С | два клиента читают vN | два PATCH с expectedVersion=N | один применён, второй 409 `VERSION_CONFLICT`; нет lost update | statuses/version/audit1 |
| TASK-07 | G3 | П,+,С | PLANNED task | пройти допустимые ветви PLANNED→IN_PROGRESS/BLOCKED/DONE/CANCELLED на отдельных задачах | каждое допустимое состояние и completedAt/terminal metadata корректны | task events/audit |
| TASK-08 | G3 | П,−,С | terminal DONE/CANCELLED | попытаться выйти из terminal; недопустимые переходы | typed 409/400, версия не меняется | state/version/audit delta0 |
| TASK-09 | G3 | П,+ | задачи разных due/status | GET list без фильтра, status, due interval, pagination/query boundaries | порядок/фильтр совпадают с авторитетной выборкой | response vs DB |
| TASK-10 | G3 | П,− | два workspaces, PRIVATE tasks | OWNER A читает/получает detail PRIVATE B | 404 без раскрытия существования | status + no content |
| TASK-11 | G3 | П,+/− | OWNER и MEMBER одного workspace | проверить WORKSPACE, own PRIVATE, foreign PRIVATE | видимость строго по матрице ACL | endpoint matrix |
| TASK-12 | G3 | П,+,С | task с result capability | добавить result, затем повтор с тем же idempotency key | один result/version/audit; replay возвращает исходное | response hashes/counts |
| TASK-13 | G3 | П,−,С | TASK-12 | тот же idempotency key с другим payload | `IDEMPOTENCY_KEY_REUSE`, без второго эффекта | error + counts |
| TASK-14 | G3 | П,+,С | pending proposal | OWNER ACCEPT | terminal ACCEPTED, создана ровно одна task | proposal/task/audit/outbox |
| TASK-15 | G3 | П,+,С | отдельные pending proposals | OWNER REJECT и DELEGATE с assignee | REJECT task0; DELEGATE одна task и одно PENDING assignment | authoritative counts |
| TASK-16 | G3 | П,−,С | terminal proposal | повторить то же и противоположное решение | typed 409/идемпотентный replay по ключу, terminal не меняется | audit1/task≤1 |
| TASK-17 | G3 | П,К | proposal PENDING, два соединения | синхронно ACCEPT против REJECT | ровно один 200 и один typed409; ACCEPT⇒task1, REJECT⇒task0; audit1 | concurrent responses/DB |
| TASK-18 | G3 | П,+,С | task, allowed capability, decider | создать approval request, APPROVE и на другой REJECT | один PENDING+inbox; одно terminal решение | approval/inbox/audit |
| TASK-19 | G3 | П,− | approval context | unknown capability, foreign task/decider, taskless task-bound request | отказ, approval/inbox delta0 | error/counts |
| TASK-20 | G3 | П,К | approval PENDING | противоположные решения одновременно | один победитель, одна terminal запись и один audit | responses/row lock evidence |
| TASK-21 | G3 | П,+,С | approved task assignment | OWNER назначает MEMBER, canRedelegate false, selected doc roots | ровно одно PENDING assignment; до ACCEPT task не виден как assigned | assignment/change snapshots |
| TASK-22 | G3 | П,− | TASK-21 | без approval, stale task version, foreign assignee/root, duplicate root | отказ без assignment/access widening | counts/ACL oracle |
| TASK-23 | G3 | П,+,С | PENDING assignment | assignee ACCEPT; отдельное assignment DECLINE | terminal state корректен; ACCEPT открывает task и выбранные docs | assignment/task/document ACL |
| TASK-24 | G3 | П,С | ACCEPTED assignment | COMPLETE и REVOKE на отдельных ветвях | terminal transition, доступ после revoke закрыт по contract | state/ACL/change |
| TASK-25 | G3 | П,− | чужой principal/terminal assignment | решить чужое или повторить решение | 404/409, audit terminal1 | response/counts |
| TASK-26 | G3 | П,К | PENDING assignment | одновременно ACCEPT против DECLINE | один 200, один typed409, decision audit1; task UPSERT только если ACCEPT | responses/changes/audit |
| TASK-27 | G3 | П,+/− | ACCEPTED assignment canRedelegate false/true | MEMBER пытается переназначить | false запрещает; true плюс grant/approval создаёт ровно одно PENDING | ACL/audit/assignment |
| TASK-28 | G3 | П,+ | accepted assignment после cursor | MEMBER выполняет sync/list | появляются ASSIGNMENT, TASK UPSERT и CALENDAR в монотонном порядке; задача видна без ручного DB patch | change sequences/UI |

## 7. Offline sync, Room, фокус, календарь и входящие

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| SYNC-01 | G4 | Л/Э,+,С | AVD offline, пустой `SYNC-*` | создать task, закрыть процесс, вернуть сеть, unlock и один sync | pending CREATE переживает reopen; local ID заменён canonical; task ровно одна | Room before/after + server count |
| SYNC-02 | G4 | Л/Э,+,С | offline local task | CREATE → status → result → terminal до первой сети | зависимые операции переписаны на canonical ID/version и применены по порядку | outbox phases/server versions |
| SYNC-03 | G4 | Л/Э,+,С | две offline creates | включить обе в SET_FOCUS по local IDs и синхронизировать | все ссылки remapped, ordered focus содержит canonical IDs | Room/outbox/focus snapshot |
| SYNC-04 | G4 | Л/Э,+,С | offline created task | отменить до/после remap | cancel применён к canonical task без дубля | task count/state/id map |
| SYNC-05 | G4 | Л,+,С | прерываемый fake API | оборвать после CREATE и до dependent operation, открыть БД снова | повтор продолжает с первой незавершённой фазы | outbox states/calls |
| SYNC-06 | G4 | П,+,С | queued mutation с operationId | отправить одинаковый batch дважды | первый `APPLIED`, второй `REPLAYED`, ответ/версия одинаковы | HTTP200 results + counts |
| SYNC-07 | G4 | П,−,С | SYNC-06 | тот же operationId, другой payload/action/entity | `REJECTED`/`IDEMPOTENCY_KEY_REUSE`, домен неизменен | embedded result/counts |
| SYNC-08 | G4 | П/Э,−,С | client local vN, сервер vN+1 | отправить UPDATE_TASK expectedVersion=N | HTTP200; `results[].outcome=CONFLICT`, `currentVersion=N+1`, `VERSION_CONFLICT`; сервер не перезаписан | raw envelope + audit delta0 |
| SYNC-09 | G4 | Э,+,С | `APK-CONFLICT`, сохранённый SYNC-08 | открыть detail после sync | виден конфликт и сохранён пользовательский черновик; нет автоматического replay | UI/Room conflict row |
| SYNC-10 | G4 | Э/П,+,С | SYNC-09, загружена current version | выбрать повтор после сравнения; отправить только dirty fields | одна новая operation; title меняется, concurrent description сохраняется | request field set/server vN+2 |
| SYNC-11 | G4 | П,−,Г | partial UPDATE_TASK | omitted title/visibility, explicit null/non-text, nullable description/due null | omission сохраняет; invalid title/visibility rejected; nullable clear работает | embedded result + invariants |
| SYNC-12 | G4 | П,+,Г | cursor C, changes > page | sync limit/page до конца | opaque cursor монотонен; нет пропуска/дубля | sequences/cursors |
| SYNC-13 | G4 | Л,+,С | change envelope | симулировать crash до и после applyChanges, до cursor write | cursor продвигается только после применения; replay безопасен | test checkpoints |
| SYNC-14 | G4 | Э,−,С | сеть отсутствует/timeout | несколько UI refresh и WorkManager retry | unique work, нет duplicate writes; понятное состояние; backoff ограничен | WorkManager/Room/server delta |
| SYNC-15 | G4 | Э,+,С | queued mutations, process death/reboot | force-stop/relaunch и AVD reboot | durable outbox сохраняется и продолжает после unlock/network | process generations/outbox |
| SYNC-16 | G4 | П,−,Г | batch endpoint | 0, 100, 101 операций; malformed cursor; чужой clientId | границы соблюдены, oversized rejected атомарно | result count/status |
| SYNC-17 | G4 | П,− | authenticated MEMBER | offline action proposal/approval/assignment/ACL/tool/docs/Telegram | запрещённые actions `REJECTED`, domain delta0 | per-action matrix |
| SYNC-18 | G4 | Э,+,С | same-cert upgrade с pending outbox | обновить APK и синхронизировать | Room migration сохраняет pending/idempotency/clientId | package/Room/server proof |
| SYNC-19 | G4 | Э,+,С | server DELETE/visibility loss | получить change и открыть старую detail/deep link | локальная сущность скрыта/удалена, бесконечного loading нет | Room/UI/cursor |
| SYNC-20 | G4 | Э,+,С | две client identities одного principal | изменения A и B, затем sync обоих | порядок внутри client сохранён; независимые clients сходятся к серверу без reuse ключей | client IDs/versions |
| FOCUS-01 | G4 | П/Э,+,С | 0/1/20 доступных задач | GET/PUT focus, reorder up/down, save | unique ordered IDs, версия растёт один раз, UI совпадает | snapshot/version/UI |
| FOCUS-02 | G4 | П,−,Г | focus vN | 21 IDs, duplicate, missing/foreign/completed ID, stale version | typed reject/conflict; старый focus неизменен | response/snapshot |
| FOCUS-03 | G4 | Э,+,С | focus с задачей | завершить/скрыть task и синхронизировать | невидимая/terminal task не считается и удаляется из отображения | task/focus changes/UI |
| FOCUS-04 | G4 | Э,+,С | server focus changed без отдельного focus change envelope | один sync | authoritative focus snapshot всё равно заменяет cache | Room snapshot |
| CAL-01 | G4 | П/Э,+,Г | due tasks до/после полуночи Москвы | GET calendar и открыть cards | сортировка и группы суток Europe/Moscow верны | API dueAt/UI labels |
| CAL-02 | G4 | П,−,Г | calendar endpoint | from>=to, invalid date/range, слишком большой interval | 400; read-only, никаких изменений | status + audit delta |
| CAL-03 | G4 | П,+/− | private/assigned/workspace tasks | получить calendar OWNER/MEMBER | только доступные due tasks | result IDs vs ACL |
| INBOX-01 | G4 | П/Э,+,С | разные event kinds/states | GET с afterSequence, filters; открыть related task | монотонный список, корректные deep-link targets | sequences/API/UI |
| INBOX-02 | G4 | Э/П,+,С | UNREAD event | offline MARK_INBOX_READ, sync, затем READ→UNREAD/RESOLVED | допустимые переходы и version one-step | outbox/event state |
| INBOX-03 | G4 | П,−,С | RESOLVED/foreign event | попытаться вернуть terminal или изменить чужой | 409/404, event/audit unchanged | response/counts |
| INBOX-04 | G4 | Э,+,С | assignment/approval inbox item | выполнить online decision из карточки | related aggregate terminal, inbox обновлён, навигация точна | UI/API/audit |

## 8. Документы и ограничение доступа по ветвям

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| DOC-01 | G5 | Л/П,+,С | `DOC-*` task, signed internal writer | создать два корня и root→child→grandchild Markdown | list выдаёт устойчивый depth-first: корень и потомки, затем второй корень | IDs/order/path |
| DOC-02 | G5 | П,+ | DOC-01 | GET metadata и content каждого документа | media `text/markdown`, readOnlyForMobile=true, SHA-256 совпадает | response/hash |
| DOC-03 | G5 | П,−,Г | internal write | path без `.md`, traversal, dot segment, backslash, leading dot/slash, Unicode path, слишком длинный path | 400; canonical regex `^[a-zA-Z0-9_/-]+[.]md$`; документов/аудита0 | response/counts |
| DOC-04 | G5 | П,−,Г | internal write | пустой/слишком длинный title; null/oversized markdown; bad expectedChecksum | строгий reject до JDBC side effect | status + counts |
| DOC-05 | G5 | П,+,С | существующий doc checksum H1 | обновить с expectedChecksum=H1 | version+1, content/hash H2, audit один | before/after/audit |
| DOC-06 | G5 | П,−,С | DOC-05 | обновить со stale/wrong checksum | 409 `DOCUMENT_CHECKSUM_CONFLICT`, H2 сохраняется | status/hash/audit delta0 |
| DOC-07 | G5 | Л/П,− | документы разных tasks | установить parent из другой task | composite FK отклоняет, строки неизменны | constraint code/counts |
| DOC-08 | G5 | Л/П,− | ветвь root-child | self-parent и цикл child→ancestor | cycle trigger отклоняет обе операции | SQLSTATE/counts |
| DOC-09 | G5 | П,+/− | assignment только с selected root | MEMBER list/get root и descendants, второй root | разрешённая ветвь читается, соседняя 404 | response IDs/ACL function |
| DOC-10 | G5 | П,− | foreign PRIVATE task | OWNER/MEMBER без task grant запрашивают doc UUID | 404, checksum/content не раскрыты | status/body |
| DOC-11 | G5 | Э,+,С | DOC-01 synced | открыть tree/content online, отключить сеть, открыть снова | проверенный Markdown читается из cache | UI + Room hash |
| DOC-12 | G5 | Э,−,С | verified cached H1 | серверный/fake response media non-Markdown или checksum mismatch | новый content отвергнут, H1 остаётся доступным, видна ошибка | UI/cache hash |
| DOC-13 | G5 | Л,+,Г | локальные orphan/cycle metadata fixture | построить tree | visited guard не зависает; orphan/cycle показаны один раз устойчиво | ordered IDs/runtime bound |
| DOC-14 | G5 | П,− | mobile bearer | попытаться POST/PATCH documents через public API | route 404; mobile остаётся read-only | status + DB delta0 |
| DOC-15 | G5 | П,+/− | N8N approval-bound write | approved и missing/stale approval | только approved создаёт/обновляет doc; scope task соблюдён | audit/resource counts |

## 9. Агент, история запусков и 18 инструментов

Для каждого инструмента позитивный путь проверяется естественной русской командой через Android или доверенный Telegram, затем по слоям: conversation/run → relay/OpenClaw tool call → n8n/action executor → Task Core/reminders → audit/outbox. Прямой internal-вызов полезен как диагностика контракта, но не заменяет модельный E2E.

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| AG-01 | G6 | Э/П,+,С | `AGENT-*`, unlocked AVD | отправить text command один раз | один user message, один run, terminal result в той же conversation | conversation/run/dispatch/UI |
| AG-02 | G6 | Э,− | offline AVD | попытаться отправить text | отправка недоступна/очередь не фабрикуется, draft сохранён | UI + server run delta0 |
| AG-03 | G6 | Э,+,С | несколько conversations | restore latest после process death, затем новая server conversation | выбирается действительно latest доступная conversation и её история | IDs/history/UI |
| AG-04 | G7 | П,+,Г | >1 page runs | GET runs с limit/cursor до конца | bounded pagination, стабильный порядок, без дублей | page IDs/cursors |
| AG-05 | G7 | П,− | OWNER/MEMBER и два workspaces | читать чужие runs/conversations | 404/пусто, prompts/tool args/secrets не раскрыты | redacted response/ACL |
| AG-06 | G7 | П,+,С | отдельные runs | пройти QUEUED→RUNNING→WAITING_INPUT→RUNNING→SUCCEEDED и WAITING_APPROVAL ветвь | только разрешённые переходы; terminal immutable | state history/audit |
| AG-07 | G7 | П,− | terminal/nonterminal runs | недопустимый переход, stale expectedVersion, повтор terminal transition | typed conflict/replay без новой публикации | state/outbox counts |
| AG-08 | G7 | П,+,С | intentionally unsupported intent | дождаться bounded retry→FAILED/DLQ | попытки ограничены, одна terminal failure; нет tool/domain effect | dispatch attempts/timestamps |
| AG-09 | G7 | П,+,С | QUEUED/RUNNING run | отменить официально до provider/tool | CANCELLED один раз; поздний claim/result не применяется | state/outbox/provider/tool delta0 |
| AG-10 | G7 | П,+,С | FAILED run | retry официальным продуктовым путём | новый distinct run/attempt, старый immutable; только новый может завершиться | old/new IDs/history |
| AG-11 | G6 | Л/П,− | plugin executor | unknown tool, произвольные URL/method/headers, identity fields в args | schema/allowlist reject до сети | error + zero calls |
| AG-12 | G6 | Л/П,− | signed tool response harness | missing/mismatched operation/correlation/intent/resource, false success, invalid/oversized JSON, redirect/timeout | результат не считается success, домен не изменён | guard code/result/counts |
| AG-13 | G6 | Л/П,С | один toolCall | повторить тот же call и другой payload | operation ID стабилен для истинного replay; changed payload отвергнут | operation/correlation/audit |
| AG-14 | G6 | Л/П,−,С | turn guard | после `ACTION_REJECTED` предложить другой доменный tool; доставить поздний failure старого turn | в текущем turn нет fallback mutation; следующий новый turn не отравлен | call sequence/turn keys |
| AG-15 | G6 | П,+/− | ANDROID и TELEGRAM runs | сверить identity context | Android identity process-bound; Telegram только resolve owner allowlist; model args не влияют | context/audit principal IDs |
| TOOL-01 | G9 | Т,+/−,С | trusted private chat, marker, baseline | `reminder_create`: валидная Moscow future date → proposal → genuine confirm; отдельно invalid date/timezone/title | до confirm task0; после — одна ACTIVE v1; invalid даёт no pending/task | chat/run/pending/task/event |
| TOOL-02 | G9 | Т,+/− | TOOL-01 ACTIVE и baseline | `reminder_list` default/states/limit; invalid limit/state | список содержит `task_id`,`current_version`, не pending ID; read-only | tool result + DB delta0 |
| TOOL-03 | G9 | Т,+/−,С | свежий list | `reminder_reschedule` exact marker → proposal → genuine confirm; stale/random/pending ID | до confirm старый due; после same task v2/new due; invalid один раз reject без fallback | pending/task versions/events |
| TOOL-04 | G9 | Т,+/−,С | fresh list current version | `reminder_cancel` → proposal → genuine confirm; stale/foreign/replay | после confirm same task CANCELLED next version; future deliveries прекращены | pending/task/deliveries |
| TOOL-05 | G9 | Т,+/−,С | valid pending inline callback | `reminder_confirm`: genuine confirm и на отдельном pending cancel button; expired/replayed/wrong actor/chat/malformed token | terminal applied/cancelled ровно один раз; token скрыт, unauthorized no effect | callback update/audit/state |
| TOOL-06 | G6 | Э,+/−,С | human Android run | `poruchik_create_task`; blank/oversized/bad visibility/due; agent-derived path | human создаёт одну task; agent-derived создаёт только PENDING proposal | run/tool/task/proposal/audit |
| TOOL-07 | G6 | Э,+/−,С | accessible task/version | `poruchik_update_task` title/description/status/due/result; stale/terminal/null/type/approval errors | только разрешённые fields и state меняются один раз | run/tool/task diff/audit |
| TOOL-08 | G6 | Э,+/− | tasks across ACL/status/due | `poruchik_list_tasks` без фильтра и с filters; invalid range/status | только доступные tasks, zero mutation | tool result vs DB |
| TOOL-09 | G6 | Э,+/−,С | owner task, member, approval | `poruchik_assign_task` roots/redelegate; без approval/stale/foreign/duplicate | одно PENDING assignment или нулевой side effect | tool/assignment/audit |
| TOOL-10 | G6 | Э,+/−,С | pending assignment | `poruchik_decide_assignment` ACCEPT/DECLINE; wrong assignee/replay/race | одно terminal решение; ACL меняется только при ACCEPT | assignment/audit/changes |
| TOOL-11 | G6 | Э,+/− | empty/nonempty focus | `poruchik_get_focus`; malformed/cross-principal context | version/order точны, zero mutation | tool result/snapshot |
| TOOL-12 | G6 | Э,+/−,С | accessible tasks | `poruchik_set_focus` 0/1/20; 21/duplicate/terminal/foreign/stale | один ordered snapshot или полный reject | focus version/audit |
| TOOL-13 | G6 | Э,+/−,Г | due tasks Moscow boundary | `poruchik_get_calendar`; invalid/range reversal/inaccessible | доступные задачи в верном интервале, zero mutation | tool result vs API |
| TOOL-14 | G6 | Э,+/− | inbox sequences | `poruchik_get_inbox` from0/continuation; negative sequence/cross-principal | монотонные доступные events, zero mutation | sequences/tool result |
| TOOL-15 | G6 | Э,+/− | task document branches | `poruchik_read_documents` tree/specific doc; bad UUID/media/checksum/foreign branch | только разрешённый проверенный Markdown, zero write | doc IDs/hash/tool result |
| TOOL-16 | G6 | Э,+/−,С | task/run/decider | `poruchik_request_approval` allowed capabilities; unknown/foreign/taskless-bound/replay | одно PENDING approval+inbox либо no effect | approval/inbox/audit |
| TOOL-17 | G6 | Э,+/−,С | pending proposals | `poruchik_decide_proposal` ACCEPT/REJECT/DELEGATE; missing assignee/foreign/replay/race | один terminal; ACCEPT task1, REJECT task0, DELEGATE task1+assignment1 | proposal/task/assignment/audit |
| TOOL-18 | G6 | Э,+/−,С | pending approvals | `poruchik_decide_approval` APPROVE/REJECT; foreign/replay/race | один terminal; разрешение действует только после APPROVE | approval/audit/effect |
| AG-16 | G6 | Э,+,С | Android voice recognizer ru-RU | произнести команду, проверить review, выбрать «Использовать» | recognized text показан до send; после подтверждения один run | UI/audio interaction/run count |
| AG-17 | G6 | Э,−,С | voice review | cancel, recognizer error/no speech, повторный open | ни draft, ни run не отправлены; понятный fallback | UI + run delta0 |
| AG-18 | G6 | Э,+,С | terminal agent run | refresh/recreate repository/process death | result обновляется in-place, не дублирует bubble и сохраняется в Room | message/run IDs/UI |

## 10. Telegram, подтверждения и планировщик напоминаний

G9 выполняется только в существующем доверенном приватном чате. Перед началом фиксируются две или иное фактическое число старых активных напоминаний; они никогда не изменяются. Все тестовые даты выбираются дальше 24 часов, а созданное тестовое напоминание отменяется до наступления срока. Бюджет одного полного позитивного прохода: не более восьми новых сообщений бота и трёх подлинных нажатий пользователя. Callback нельзя имитировать внутренним запросом.

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| TG-01 | G9 | Т,+,С | trusted private actor/chat linked | отправить естественную команду создания с unique marker и Moscow wall time | одна proposal card с inline confirm/cancel; ACTIVE ещё нет | update/run/pending/chat |
| TG-02 | G9 | Т,+,С | TG-01 pending valid | пользователь нажимает confirm один раз | pending APPLIED, одна ACTIVE v1, due UTC соответствует Moscow | callback/task/version/event |
| TG-03 | G9 | Т,+ | active marker + baseline | запросить список | marker, state, wall time, task_id/current_version верны; старые reminders только отображены | tool result/DB delta0/chat |
| TG-04 | G9 | Т,+,С | TG-03 fresh list | попросить перенести marker на новую future date | одна proposal, старый срок всё ещё действует | pending/task v1/chat |
| TG-05 | G9 | Т,+,С | TG-04 pending | genuine confirm | pending APPLIED, тот же task v2, новый срок; старые deliveries superseded | version/due/deliveries |
| TG-06 | G9 | Т,+,С | fresh list v2 | попросить отменить marker, genuine confirm | тот же task CANCELLED v3, будущих доставок нет | callback/task/deliveries |
| TG-07 | G9 | Т,−,С | отдельный pending | нажать cancel button | pending CANCELLED, reminder не создан/не изменён | pending/task delta0 |
| TG-08 | G9 | Т,− | unlinked/private foreign/group actor | команды и callback из недоверенного контекста | resolve/handler fail closed, нет утечки списка или мутаций | access audit/counts |
| TG-09 | G9 | Л/П,−,С | pending callback token | malformed, expired, superseded, replayed, wrong actor/chat | no effect; applied callback остаётся applied-once | state/events count1 |
| TG-10 | G9 | Л/П,+,С | Telegram API ack/edit failure fixture | domain confirm succeeds, provider edit/ack fails | domain не откатывается и callback не применяется повторно; ошибка безопасно обработана | DB terminal + mocked provider |
| TG-11 | G9 | Л,− | tool turn context | list отсутствует/устарел, mutation с pending_action_id вместо task_id | локальный `ACTION_REJECTED` один раз; нет alternate tool fallback | call trace/domain delta0 |
| TG-12 | G9 | Л/П,+ | `reminders_list` states | active/paused/completed/cancelled и limit | schema содержит task_id/current_version/state/title/due; scope actor/chat | function/tool result |
| TG-13 | G9 | Л/П,С | одинаковая create command/correlation | повтор delivery/tool invocation | canonical payload hash и idempotency дают один pending/task | rows/event counts |
| TG-14 | G9 | Л/П,С | два pending изменения одной task | создать новое после старого | старое superseded, только новое callback-eligible | pending states |
| SCH-01 | G9 | Л/П,+,С | ACTIVE task, bounded horizon | вызвать authenticated materializer tick | occurrences/due/offset deliveries создаются один раз | occurrence/delivery keys |
| SCH-02 | G9 | Л/П,+,Г | one-time/recurrent end modes | materialize count/until/date/exhausted boundaries | ровно ожидаемое число occurrences, cursor exhausted корректен | version/cursor/counts |
| SCH-03 | G9 | Л/П,+,С | quiet 00:00–06:00 Europe/Moscow | delivery попадает в quiet hours | effective_at перенесён, quiet_deferred/digest bucket выставлены | timestamps/flags |
| SCH-04 | G9 | Л/П,+,Г | deferred backlog > digest thresholds | claim batch | не более 5 сообщений, digest показывает bounded items/omitted count | batches/member IDs |
| SCH-05 | G9 | Л/П,− | scheduler webhook | bad key/signature/body hash/timestamp/nonce replay/job name | tick не выполняется, leases/rows unchanged | auth result/counts |
| SCH-06 | G9 | Л/П,+,С | claimable deliveries | два workers claim | SKIP LOCKED/lease исключает двойную отправку | lease owners/unique claim |
| SCH-07 | G9 | Л/П,+,С | expired lease before send | следующий tick | delivery → retry_wait и может быть reclaimed один раз | attempts/state history |
| SCH-08 | G9 | Л/П,+,С | provider transient/429 | finalize retry_wait с retry-after/backoff | bounded backoff, quiet policy повторно применяется | attempts/effective_at |
| SCH-09 | G9 | Л/П,−,С | provider 400/403/permanent | finalize | dead_letter, автоматического бесконечного retry нет | state/attempt count |
| SCH-10 | G9 | Л/П,+,С | ambiguous timeout after send | finalize uncertain | не производится слепая повторная отправка; операторский статус различим | uncertain record |
| SCH-11 | G9 | Л/П,+,С | claimed item, policy changed before send | pre-send authorize | revoked/mismatched policy блокирует send; quiet/rate временно откладывают | authorization result/state |
| SCH-12 | G9 | Л/П,+,С | pending confirmation cadence | initial inline proposal, cadence tick до TTL | reminder prompt не изменяет domain; текст только Moscow/user-action, без token/UTC implementation text | pending counters/chat fixture |
| SCH-13 | G9 | Л/П,+,С | pending applied/cancelled/expired | следующий confirmation tick | больше не claim/send | next_confirmation null/count delta0 |
| SCH-14 | G9 | Л/П,+,Г | max confirmation/TTL | довести до границы без внешних sends в local DB | pending становится expired, lease очищен | state/counts |
| SCH-15 | G9 | Л/П,+,С | active repeating occurrence | complete/snooze/repeat-until-done | новые deliveries создаются по правилам, старые terminal | occurrence/delivery graph |
| SCH-16 | G9 | Л/П,+,С | service restart между claim/finalize | восстановить scheduler | lease expiry обеспечивает bounded recovery, без orphan claimed | states/restarts |

## 11. FCM, нейтральные уведомления и deep link

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| PUSH-01 | G8 | Л/П,+,С | QA registration enabled | создать по одному accepted событию TASK_CREATED/TASK_CHANGED | одна outbox и delivery на тип; publish после commit | event/outbox/delivery/provider ID |
| PUSH-02 | G8 | Л/П,+,С | отдельные fixtures | TASK_RUN_CHANGED RUNNING/WAITING/terminal, INBOX_EVENT_CREATED, APPROVAL_DECIDED | правильные recipients и route type, по одной delivery | event-recipient matrix |
| PUSH-03 | G8 | Л/П,− | payload capture | проверить все keys/values | data-only: только allowlisted routing IDs/type/version; нет title/description/content/result/token/principal | payload key set/hash |
| PUSH-04 | G8 | Э,+,С | app foreground | послать один neutral event | системное поведение foreground соответствует policy, один authoritative refresh | worker decision/sync count |
| PUSH-05 | G8 | Э,+,С | app background | один event | одна нейтральная notification; tap открывает точную task/inbox/agent route после unlock | shade/deep link/server state |
| PUSH-06 | G8 | Э,+,С | process killed, не force-stop | один event, cold launch по tap | notification доставлена, cold start восстанавливает target | process generation/navigation |
| PUSH-07 | G8 | Э,+,С | app force-stopped | event, затем ручной launch без tap | системное подавление не считается серверной ошибкой; polling восстанавливает state/latest conversation | delivery/provider + post-launch sync |
| PUSH-08 | G8 | Э,+/− | Android 33+ permission granted/denied/revoked | по одному контролируемому event на отдельной фикстуре | granted показывает notification; denied/revoked всё равно запускает безопасный refresh без crash | permission/UI/sync |
| PUSH-09 | G8 | Л/Э,−,С | same eventId дважды | обработать duplicate | одна notification/refresh decision | Room push dedup rows |
| PUSH-10 | G8 | Л/Э,−,С | entity versions N+1 затем N | newer, stale, out-of-order, same version new eventId | Room не откатывается; stale не запускает второй эффект | versions/decisions |
| PUSH-11 | G8 | Л/Э,− | malformed/spoof envelope | unknown type, missing/bad UUID/version/route | fail closed без crash, navigation и данных | parser result/log redaction |
| PUSH-12 | G8 | Э,+,С | PIN/biometric gate | tap notification locked; biometric success/cancel/failure | target открывается только после успешного unlock, intent сохраняется/сбрасывается безопасно | UI destination/auth state |
| PUSH-13 | G8 | Э,+/− | task удалён/доступ отозван после push | tap старого route | home/recovery, понятное сообщение, нет вечного spinner/утечки | GET 404 + UI |
| PUSH-14 | G8 | П,+,С | token rotation | зарегистрировать T1→T2, event | delivery только активной registration, T1 не используется | registration/delivery recipients |
| PUSH-15 | G8 | П,+,С | provider invalid token | один event | registration disabled, delivery terminal; другие devices unaffected | provider code/registration state |
| PUSH-16 | G8 | П,+,С | два QA devices одного principal | event для principal | по одной delivery на каждую enabled registration, dedup на device/event | recipient counts |
| PUSH-17 | G8 | Л/П,+,С | transient provider error | dispatcher retry до success/limit | exponential bounded retry; после лимита DLQ один раз | attempts/timestamps/state |
| PUSH-18 | G8 | Л/П,+,С | pre-migration events и new events | publisher startup | historical cutoff не создаёт backlog; новые accepted events публикуются | seed counts |
| PUSH-19 | G8 | П,+,С | Task Core restart с queued event | restart и дождаться dispatcher | очередь продолжается, duplicate claim не публикует второй раз | outbox/delivery/attempts |
| PUSH-20 | G8 | Э,+,С | network offline при receive | event, затем сеть | notification нейтральна; authoritative state появляется после retry | worker/backoff/UI |

## 12. Интерфейс эмулятора, восстановление и интеграционные цепочки

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| UI-01 | G10 | Э,+ | authenticated empty workspace | пройти Задачи/Фокус/Агент/Календарь/Входящие | пять разделов доступны, empty/loading/error состояния конечны | screenshots/semantics |
| UI-02 | G10 | Э,+,С | task fixtures всех states | filters Все/Запланированные/В работе/Заблокированные/Завершённые | каждая карточка ровно в ожидаемой группе; filter сохраняется при navigation | visible IDs/UI state |
| UI-03 | G10 | Э,+,Г | длинные Unicode поля | открыть list/detail/edit при клавиатуре, scroll и малом экране | текст не теряется, действия достижимы, нет overlap | screenshots/semantics |
| UI-04 | G10 | Э,+,С | create/edit dialogs | rotate/activity recreation/Back/cancel | draft сохраняется безопасно; cancel не пишет; Save выполняется один раз | Room/server deltas |
| UI-05 | G10 | Э,+ | task due UTC | показать в detail/calendar | Europe/Moscow wall time точен, включая границу суток и DST-neutral dates | API vs label |
| UI-06 | G10 | Э,+/− | focus editor | add/remove/reorder/save/cancel, max20 | порядок и notices понятны; cancel без write | UI/snapshot |
| UI-07 | G10 | Э,+/− | inbox decision fixtures | filters, card actions, duplicate/stale decision | success/typed conflict показываются по-русски, navigation точна | UI/API state |
| UI-08 | G10 | Э,+/− | docs tree/cache | expand/open/back, offline, checksum error | stable depth-first, verified cache, понятная ошибка | UI/Room hash |
| UI-09 | G10 | Э,+,С | agent run history | RUNNING→terminal refresh, pagination, latest conversation | bubble обновляется in-place, scroll/selection устойчивы | UI/run IDs |
| UI-10 | G10 | Э,− | network timeout/401/404/5xx | открыть каждый основной экран и refresh | нет crash/вечного spinner; recovery action соответствует ошибке | timed UI states |
| UI-11 | G10 | Э,+ | semantic tree | пройти все интерактивные элементы | есть русские contentDescription/labels, touch targets и focus order | accessibility dump |
| UI-12 | G10 | Э,+,С | invalid and valid deep links | task/agent/inbox links foreground/cold, затем invalid | exact target; новый intent заменяет старый; invalid идёт home | route/destination |
| UI-13 | G10 | Э,+,С | signed old APK with data | same-cert upgrade на current release | данные/PIN/session/outbox сохранены, schema migrations one-time | package/Room counts |
| UI-14 | G10 | Э,+,С | queued local changes | low-memory process death и AVD reboot | no duplicate submission, draft/outbox восстанавливаются | generation/operation IDs |
| UI-15 | G10 | Э,+,С | enrollment bootstrap | временный SSH/bootstrap listener и host pin | exact RSA payload/network pin совпадает; после enrollment runtime использует direct HTTP, tunnel не остаётся обязательным | enrollment metadata/topology |
| UI-16 | G10 | Л/Э,− | SSH/WebSocket legacy harness | wrong host key, disconnect/reconnect, malformed frame | fail closed; legacy path не считается текущей рабочей синхронизацией | unit result/UI |
| UI-17 | G10 | Э,+,С | отдельные Android profiles | переключить profile/client/workspace | Room/Keystore/session/deep links не пересекаются | package/profile IDs |
| UI-18 | G10 | Э,+,С | local conflict row `APK-CONFLICT` | показать current version, dirty fields, rebase/retry once | пользовательский Unicode draft сохранён; retry доступен один раз; canonical task без дубля | UI/Room/server versions |
| INT-01 | G3/G4/G6 | Э/П,+,С | OWNER+MEMBER, agent runtime | agent create proposal→OWNER accept→approval→assign→MEMBER accept→sync | одна task, один grant, MEMBER видит task/calendar/docs по scope | сквозной ledger |
| INT-02 | G4/G5/G8 | Э/П,+,С | assigned task + docs + push | assignment ACCEPT публикует changes/push, затем mobile sync | UI показывает task и разрешённую doc branch; push нейтрален | change order/delivery/UI |
| INT-03 | G6/G7/G8 | Э/П,+,С | fresh conversation | command→RUNNING→tool→SUCCEEDED | history/result/push/latest conversation согласованы, один side effect | run/dispatch/tool/audit/push |
| INT-04 | G2/G4/G10 | Э/П,+,С | access истёк, refresh valid, pending outbox | один обычный sync | client сам проходит challenge/refresh и применяет outbox без потери | session generation/result |
| INT-05 | G2/G4/G10 | Э/П,−,С | device revoked с local cache | unlock и refresh | server 401, локальные данные не отправляются/не стираются молча; нужен re-enrollment flow | auth status/Room/UI |

### 12.1 Дополнительные граничные и эксплуатационные проверки

| ID | Группа | Тип | Предусловия и изоляция | Шаги | Ожидаемый результат и оракул | Доказательства |
|---|---|---|---|---|---|---|
| EDGE-01 | G2 | Л/Э,Г | invitation URI generator | payload с `+`/URL-safe base64, максимальная длина и +1 | допустимое значение не искажается clipboard/parser; превышение reject без partial state | parsed bytes/redeem delta |
| EDGE-02 | G3 | П/Э,Г | create/edit task | title 300/301, кириллица, emoji, combining Unicode, newlines description | границы едины UI/API; принятые байты сохраняются точно | request/resource/UI |
| EDGE-03 | G4 | Л,С | server applied, response потерян | оборвать transport после commit до local record и повторить sync | сервер возвращает replay, Room становится APPLIED, audit/task не дублируются | operationId/counts |
| EDGE-04 | G4 | П,К | focus v1 на двух clients | одновременно PUT разных списков expected v1 | один apply, один conflict; смешанного порядка нет | responses/focus snapshot |
| EDGE-05 | G6 | Э/П,−,Г | agent input | пустая/whitespace и строка на/за пределом длины, malformed task UUID | UI/API reject, run/dispatch delta0 | status/run counts |
| EDGE-06 | G7 | П,С | dispatch outbox queued, relay временно недоступен на разрешённом стенде | восстановить relay без resubmit | существующий outbox claim один раз, run terminal один раз | outbox/dispatch/run |
| EDGE-07 | G6 | Л/П,− | approval-bound n8n resource | durable approval, недолговечная/несуществующая approval, mismatched capability | effect только при действующей durable approval | executor result/audit |
| EDGE-08 | G6 | Л/П,− | relay namespace/config fixture | current namespace и устаревший namespace | current dispatch принимается; stale target bounded retry/failure без silent hang | route/config/run states |
| EDGE-09 | G1/G10 | Э,+/− | network security config | direct approved HTTP origin и иной cleartext host | разрешён только опубликованный origin; нет зависимости от adb reverse/VPN | connection result/config |
| EDGE-10 | G10 | Э,Г | отдельные AVD settings | ru/en locale, 12/24h, большой font/display scale, low storage/battery saver | даты/русский продуктовый текст/доступность сохраняются; деградация безопасна | screenshots/OS state |
| OPS-01 | G0 | Л,+,С | disposable empty PostgreSQL | применить Task Core V1–current и N8NAgents 001–011 | clean bootstrap проходит; функции/ACL/constraints соответствуют contract | migration history/metadata |
| OPS-02 | G0 | Л,+,С | migrated disposable DB | повторно запустить supported bootstrap/import | нет drift/повторных данных; ожидаемые guarded operations идемпотентны | schema/data hashes |
| OPS-03 | G0 | Л,+ | package artifacts | сверить SBOM, dependency lock, plugin package/version, APK signer/hash | артефакты принадлежат одному release set и не содержат secrets | hashes/signature/SBOM |
| OPS-04 | G1 | П,+ | read-only production | health/restart/image/schema/plugin/workflow fingerprints до и после будущего rollout | только выбранный компонент меняется, readiness green, restart0 | before/after inventory |
| OPS-05 | G1 | П,+,С | staged immutable image/package | выполнить отдельно разрешённый selected-service rollout и rollback rehearsal без данных | health/readiness проходят, сеть/egress/volumes сохранены | tag/digest/compose diff |
| OPS-06 | G0/G1 | Л/П,− | migration preflight | legacy conflicts, insufficient grants, checksum mismatch | rollout останавливается до DDL; пользовательские rows не преобразуются молча | preflight/result/rollback artifact |
| OPS-07 | G8/G9 | Л/П,+,С | queued deliveries/runs | restart между claim/finalize | lease recovery ограничен; нет orphan/duplicate send | state timelines |
| OPS-08 | G11 | П,+,С | завершённый workspace ledger | выполнить guarded cleanup и повторный read-only residual check | residual0 только scoped IDs; глобальный baseline/legacy queues неизменны | deleted counts/global diff |

## 13. Зависимости и порядок исполнения

| Этап | Параллельные группы | Входной критерий | Выходной критерий |
|---|---|---|---|
| A | G0 + G1 | зафиксирован исходный commit | сборки/контракты зелёные, public boundary известна |
| B | несколько экземпляров G2 | A PASS, созданы изолированные invites | активные OWNER/MEMBER sessions и отдельные client/device IDs |
| C | G3 + G5 + G6 + G7 | B PASS, runtime healthy | доменные/API/agent позитивы и негативы закрыты по отдельным branches |
| D | несколько экземпляров G4 + G10 | B PASS, подписанный APK на AVD | offline, process-death, UI и conflict chains закрыты |
| E | G8, а серверные тесты G9 параллельно | registrations/policies готовы | FCM matrix и scheduler local/integration закрыты |
| F | G9 real chat | C PASS, chat baseline и пользователь доступны | пять reminder tools, три genuine callbacks, test reminder cancelled |
| G | G11 по завершённым workspaces | группы больше не мутируют scope | residual0 по ledger, исходные данные и очереди неизменны |

Внутри C задачи `TASK-17`, `TASK-20`, `TASK-26` используют отдельные aggregates и могут идти параллельно. Внутри D `SYNC-01`, `SYNC-08` и `UI-13` требуют разных AVD/clientId/workspace. В G6 чтения `TOOL-08`, `TOOL-11`, `TOOL-13`, `TOOL-14`, `TOOL-15` можно запускать одновременно в разных conversations; `TOOL-06/07/09/10/12/16/17/18` используют отдельные task branches либо выполняются последовательно по версии. Любой restart/deploy останавливает C–F до readiness и fingerprint проверки.

## 14. Что реально эмулируется и где нужен внешний канал

| Возможность | AVD + production backend | Нужен физический телефон | Нужен настоящий Telegram |
|---|---|---|---|
| API, auth, ACL, idempotency, races, sync, Room, UI | да | нет | нет |
| FCM foreground/background/process-dead на Play-enabled AVD | да | только OEM/Doze/vendor-specific поведение | нет |
| Android force-stop suppression и polling recovery | да | желательно повторить как release smoke | нет |
| PIN/biometric | PIN да; biometric emulator control | аппаратная biometric/OEM lock только на финальном smoke | нет |
| Голосовой ввод ru-RU | возможен при рабочем recognizer и реальном аудио; `adb input text` не доказательство | нужен для окончательного качества микрофона/recognizer | нет |
| Все 13 Poruchik tools | да, Android E2E | нет | нет |
| Пять reminder tools и SQL/plugin/n8n контракты | схемы и backend да | нет | для пользовательского E2E да |
| Trusted actor/chat resolve и inline callback | отрицательные сценарии можно локально | нет | позитив требует реального приватного чата и genuine click |
| Telegram provider delivery/ack/edit/cadence | provider failures моделируются; live факт только Telegram | нет | да |
| OEM background limits, cellular-only route, vendor notification shade | частично | да, отложенный финальный этап | нет |

Физический телефон запрещён на этапе выполнения этой матрицы до завершения эмуляторных и backend-волн. Его нельзя разблокировать, переустанавливать, переключать профиль или использовать для получения доказательств раньше отдельного release-smoke. Существующие пользовательские данные и registrations не являются тестовыми фикстурами.

## 15. Правила фикстур, очистки и остановки

1. Каждая группа получает workspace с уникальным префиксом, двух principals максимум и отдельные device/client/conversation IDs. Исключение — G9, где используется существующая owner policy, но только уникальный reminder marker.
2. До первой мутации фиксируются глобальные и workspace-scoped counts. Запрещены generic delete, очистка по title prefix без UUID ledger, переиспользование consumed invitation и запись напрямую в БД вместо официального продуктового пути.
3. DB corruption fixtures для FK/cycle допустимы только в изолированной локальной PostgreSQL. В production выполняются валидные API writes и негативы, которые гарантированно отклоняются до DML.
4. Конкурирующие тесты используют два официальных запроса с разными idempotency keys и барьером старта; блокировки БД вручную не подменяют реальную гонку.
5. Реальные FCM-события идут последовательно и только на явно выбранные QA registrations. Старый DLQ не replay. Реальный Telegram-тест строго сериализован, с будущим сроком, бюджетом сообщений и немедленной фиксацией callback.
6. При первом неожиданном побочном эффекте группа останавливается. Максимум три содержательные попытки одного блокера допускаются только с новой гипотезой; слепой replay запрещён.
7. Очистка выполняется одним writer после приёмки доказательств: сначала дочерние run/dispatch/delivery/audit-связи, затем aggregates, sessions/devices/principals/invites/workspace согласно FK. Telegram test reminder должен быть CANCELLED и не иметь будущих open/claimable deliveries; старые owner reminders неизменны.
8. Выпускной отчёт содержит PASS/FAIL/NOT RUN для каждого ID, commit/image/Flyway/plugin/APK fingerprints, signer, health/restart counts и ссылку на журнал фикстур. `NOT RUN` обязательно объясняет блокер и влияние на уверенность.

## 16. Критерий завершения

Полная эмуляторная и backend-приёмка завершена, когда все применимые строки G0–G8 и G10 имеют PASS, все 18 инструментов подтверждены сквозным серверным оракулом, а G9 либо выполнена подлинным пользовательским Telegram-путём, либо явно остаётся единственным внешним блокером. Физические OEM-сценарии переносятся в отдельный финальный smoke и не маскируют дефекты, воспроизводимые на AVD. После точечной очистки каждый тестовый workspace имеет residual0, исходные owner rows и очереди не изменены, открытых несогласованных дефектов нет.

## Приложение A. Трассировка API к кейсам

| Контрактные операции | Основные кейсы |
|---|---|
| invitation redeem | AUTH-01–04, EDGE-01 |
| refresh challenge, refresh, logout | AUTH-08–14, INT-04–05 |
| push registration PUT/DELETE, device revoke | AUTH-15–17, PUSH-14–16 |
| Telegram link nonce/status/delete и internal resolve/consume | AUTH-18–22, TG-08 |
| sync | SYNC-01–20, EDGE-03–04 |
| task list/create/detail/patch | TASK-01–13, EDGE-02 |
| assignment create/decision | TASK-21–28, TOOL-09–10 |
| document list/get и internal write | DOC-01–15, TOOL-15 |
| proposal list/decision и internal proposal | TASK-14–17, TOOL-17 |
| approval decision/request | TASK-18–20, TOOL-16/18 |
| inbox list/patch и internal inbox event | INBOX-01–04, TOOL-14 |
| focus GET/PUT | FOCUS-01–04, TOOL-11–12 |
| calendar GET | CAL-01–03, TOOL-13 |
| agent command/latest conversation/runs и internal run/state/context | AG-01–18, TOOL-06–18 |
| internal intent/effect | AG-11–15, TOOL-06–18 |
