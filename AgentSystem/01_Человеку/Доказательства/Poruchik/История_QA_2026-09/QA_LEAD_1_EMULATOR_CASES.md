# Независимый каталог QA-лида 1: эмулятор и production backend

Статус: самостоятельный черновик до обмена с двумя другими QA-лидами. Каталог основан на актуальных исходниках `Poruchik` и `N8NAgents`, OpenAPI-контрактах и политиках состояний. Результаты прежних матриц сюда не переносились. Это дизайн проверок: в этой волне тесты не запускались, production не изменялся, физический телефон не использовался.

Цель будущего прогона — ноль открытых дефектов в согласованной после дедупликации матрице. Каталог не утверждает отсутствие всех возможных ошибок.

## Обозначения и правила исполнения

- **ЭМУ-UI** — Android Emulator, управление только тестовым профилем и тестовыми данными.
- **ЭМУ-СИС** — эмулятор с управляемыми системными состояниями: сеть, процесс, перезапуск, биометрия, разрешения.
- **API-ИЗО** — официальный production API с отдельным workspace/principals/devices и точечным ledger; после группы — guarded cleanup.
- **API-ЧТ** — production только для чтения: health, metadata, baseline, без изменения данных.
- **ЛОК-К** — локальная контрактная проверка, когда внешний провайдер не нужен.
- **Класс**: `+` положительный, `−` отрицательный, `Г` граничный, `С` с состоянием/последовательностью, `К` конкурентный.
- **Параллельная группа** задаёт безопасную волну. Кейсы одной группы параллельны лишь при разных `fixture_key`. Один AVD UI-сеанс, один principal/device, один cursor, один task/version, один conversation и один Telegram pending action — последовательные общие ресурсы.
- Для API-изменений обязательны: уникальный префикс, уникальные idempotency keys, до/после-счётчики, audit/change/outbox oracle и точечная очистка. Секреты, токены и пользовательский текст в evidence не сохраняются.

Колонки **Зависимости / ресурс** содержат как порядок, так и общий ресурс. **Изоляция** задаёт минимальную фикстуру и способ очистки.

## A. Сборка, установка, профиль и базовая навигация

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| ENV-01 | +Г | ЭМУ-UI | Чистый AVD API 26 | Установить подписанный release; запустить | Установка и старт без crash; `com.poruchik.app` | package/version/signature hash; screenshot первого экрана; logcat crash=0 | Новый snapshot AVD | P-ENV-A | Общий AVD; первый |
| ENV-02 | +С | ЭМУ-UI | Release предыдущей версии с тестовыми Room-данными | Обновить APK тем же сертификатом | Данные и локальный PIN сохранены; миграции успешны | signer до/после; Room counts; UI | Отдельный AVD snapshot | P-ENV-B | APK signer; последовательно с ENV-03 |
| ENV-03 | − | ЭМУ-UI | Установлен release | Попытаться установить APK с другим сертификатом/пониженным versionCode | Android отклоняет; данные не меняются | `adb install` error class; package/data counts | Тот же AVD, без uninstall | P-ENV-B | После ENV-02 |
| ENV-04 | + | ЭМУ-UI | Авторизованная сессия | Повернуть экран/изменить размер окна на каждом из 5 разделов | Нет потери выбранного раздела и несохранённого UI state, нет перекрытий | Compose hierarchy + screenshots | Один UI principal | P-UI-1 | Один AVD UI-сеанс |
| ENV-05 | +С | ЭМУ-СИС | Приложение разблокировано | Background→foreground; затем process kill→launch | После обычного возврата состояние корректно; после нового процесса локальные данные закрыты PIN | lifecycle/logcat; screen oracle | Один AVD | P-ENV-C | PIN fixture; последовательный lifecycle |
| ENV-06 | − | ЭМУ-СИС | Приложение с данными | Reboot AVD | Сессия зашифрована, приложение заблокировано; автосинхронизация не раскрывает UI | экран lock; отсутствие plaintext в prefs/files | Snapshot AVD | P-ENV-C | После ENV-05 |
| ENV-07 | + | ЭМУ-UI | Разблокировано | Пройти вкладки Задачи→Фокус→Агент→Календарь→Входящие | Ровно 5 стабильных разделов, подпись и выбранное состояние корректны | semantics tree + screenshots | UI-only | P-UI-1 | Общий UI-сеанс |
| ENV-08 | +Г | ЭМУ-UI | Большой шрифт 1.3–2.0; русский язык | Пройти auth, task detail, inbox, agent | Критичные кнопки доступны; текст не обрезан до потери смысла | screenshots + accessibility tree | UI-only | P-UI-2 | Отдельный AVD configuration |
| ENV-09 | +Г | ЭМУ-UI | TalkBack/semantics inspection | Открыть карточки задач, календаря, inbox, голос | У интерактивных целей есть понятные описания; порядок фокуса логичен | semantics dump | UI-only | P-UI-2 | Может идти после ENV-08 |
| ENV-10 | − | ЛОК-К | Release/qa/debug variants | Сравнить manifest/source-set/artifact contents | QA diagnostics отсутствует в release UI; нет exported QA component; backup=false | manifest/aapt/source scan | Без устройства | P-BUILD | Нет общего runtime |

## B. Deep link и переходы между экранами

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| NAV-01 | +С | ЭМУ-UI | Задача есть в локальном кеше | Открыть `poruchik://task/{uuid}` из cold start | После unlock открывается точная задача | activity intent + title/id correlation | Fixture task A | P-NAV-A | Один AVD; auth готов |
| NAV-02 | +С | ЭМУ-UI/API-ИЗО | Задачи нет локально, доступ есть на сервере | Открыть task link | Показан recovery/loading; один refresh; затем detail | UI phases; Gateway request count=1; cache | Fixture task B | P-NAV-A | Последовательно в UI |
| NAV-03 | − | ЭМУ-UI | UUID отсутствует/нет ACL | Открыть task link; нажать Обновить; назад | Нет чужого содержимого; recovery не зациклен; возврат в список | UI + API 404 + logs no content | Cross-principal task | P-NAV-B | Изолированный principal |
| NAV-04 | + | ЭМУ-UI | Inbox event с targetTaskId | Открыть `poruchik://inbox/{subject}` | Открываются Входящие и соответствующий элемент/задача | selected tab + event/task IDs | Inbox fixture A | P-NAV-C | Один AVD UI |
| NAV-05 | + | ЭМУ-UI | Conversation есть | Открыть `poruchik://agent/{conversationId}` | Выбран Агент и точная история | conversation ID; messages | Conversation A | P-NAV-D | Agent fixture |
| NAV-06 | −Г | ЭМУ-UI | Любое состояние | Открыть malformed UUID, unknown host/path, extra segments | Fail closed на home; без crash/запроса к произвольному URL | activity state; Gateway requests=0 | UI-only | P-NAV-E | Можно параллельно отдельными AVD |
| NAV-07 | С | ЭМУ-UI | Быстро два intents | Последовательно отправить task A, agent B до завершения первого | Последний валидный intent побеждает; stale destination не открывается позже | navigationRequestId/state trace | Fixtures A/B | P-NAV-E | Один AVD, строго последовательно |
| NAV-08 | + | ЭМУ-UI | Detail открыт | Системная Back и кнопка «← К списку» | Оба пути возвращают в список, не закрывая приложение неожиданно | selected route/UI | UI-only | P-UI-1 | Один UI-сеанс |

## C. Приглашение, локальная блокировка и сессия

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| AUTH-01 | +С | ЭМУ-UI/API-ИЗО | Fresh owner invite; RSA fingerprint известен | Открыть exact invite; redeem; задать PIN 4–12 цифр | Один principal/device/session; экран приложения | API 2xx, DB counts, signer proof, screenshots | Workspace AUTH-A; invite1 | P-AUTH-A | Invite одноразовый; UI последовательно |
| AUTH-02 | + | ЭМУ-UI/API-ИЗО | Fresh member invite в буфере | Нажать «Вставить приглашение» | Валидная строка распознана и погашена | UI + invitations consumed once | Workspace AUTH-B | P-AUTH-B | Clipboard общий одному AVD |
| AUTH-03 | −Г | ЭМУ-UI | Signed out | Пустой clipboard; произвольный текст; query-token legacy; percent/padding/oversize | Понятная ошибка; сеть не вызывается для локально невалидного | UI message; request count=0 | UI-only variants | P-AUTH-C | Параллельно по AVD |
| AUTH-04 | −С | ЭМУ-UI/API-ИЗО | Просроченный invite | Redeem | Отказ без principal/device/session; можно использовать другой валидный invite | Problem code; DB delta0 | Workspace AUTH-C | P-AUTH-D | Clock fixture |
| AUTH-05 | −С | ЭМУ-UI/API-ИЗО | Invite уже успешно использован | Повторить exact invite | `INVITATION_ALREADY_USED`; кнопка retry не создаёт повтор | HTTP/problem; counts unchanged; UI | Workspace AUTH-A | P-AUTH-A | После AUTH-01 |
| AUTH-06 | − | API-ИЗО | Валидный token, malformed/non-P256 public key/algorithm | Redeem variants | 4xx; никаких identity side effects | DB counts/audit; problem | Workspace AUTH-D | P-AUTH-D | Отдельные invite на variant |
| AUTH-07 | +Г | ЭМУ-UI | PinSetupRequired | Ввод 3, 4, 12, 13 цифр; несовпадение; буквы | Кнопка только при 4–12 совпавших цифрах; лишнее/буквы не принимаются | semantics + visual field length | UI-only | P-AUTH-C | Один AVD sequential |
| AUTH-08 | − | ЭМУ-UI | PIN настроен | Неверный PIN, затем верный | Ошибка без открытия данных; поле очищено; верный PIN открывает | UI + auth state | PIN fixture | P-AUTH-E | Один AVD sequential |
| AUTH-09 | +С | ЭМУ-СИС | PIN и сессия сохранены | Убить процесс/reboot; запустить | Экран locked; верный PIN открывает те же данные | state + encrypted store + Room | Snapshot AVD | P-AUTH-E | После AUTH-08 |
| AUTH-10 | +С | ЭМУ-СИС | AVD с enrolled fingerprint и Android credential | Нажать биометрию; `adb emu finger touch` success | Authenticated | BiometricPrompt + UI | Biometric AVD | P-AUTH-F | Возможность конкретного образа подтвердить |
| AUTH-11 | − | ЭМУ-СИС | Биометрия доступна | Cancel/negative/failure | Остаётся locked; PIN доступен | prompt callback + UI | Biometric AVD | P-AUTH-F | Последовательно AUTH-10/11 |
| AUTH-12 | Г | ЭМУ-СИС | Биометрия не enrolled/нет strong | Открыть lock | Кнопка биометрии скрыта; PIN работает | BiometricManager state + UI | Non-biometric AVD | P-AUTH-G | Параллельно отдельный AVD |
| AUTH-13 | +С | API-ИЗО | Access истёк, refresh valid, device key есть | Выполнить защищённый запрос | Challenge→ES256 refresh→исходный запрос; token generation +1 | Gateway/DB/session generation; request trace | Device AUTH-E | P-AUTH-H | Один device/session sequential |
| AUTH-14 | +С | API-ИЗО | Access ещё принят, server отвечает 401 один раз | Защищённый запрос | Ровно один refresh и один retry; без бесконечного цикла | request counts; rotated session | Device AUTH-F | P-AUTH-I | Controlled fixture transport |
| AUTH-15 | −С | API-ИЗО | Refresh token использован/повторен | Повторить refresh proof | 401; вся семья revoked; старые/new access не действуют | DB family states; 401 probes | Device AUTH-G | P-AUTH-J | Изолированная семья |
| AUTH-16 | +С | ЭМУ-UI/API-ИЗО | Authenticated + Room data | Logout один раз | Server logout best effort; local session/key/PIN/Room wiped; SignedOut | UI; encrypted store absent; DB/session state | Device AUTH-H | P-AUTH-K | Деструктивно только для fixture AVD |
| AUTH-17 | ГС | API-ИЗО | После AUTH-16 | Повторить logout старым bearer | 401 допустим; состояние неизменно, новых side effects нет | DB counts/audit/idempotency | Device AUTH-H | P-AUTH-K | После AUTH-16 |
| AUTH-18 | − | ЭМУ-UI | Сеть недоступна при redeem/refresh | Redeem/refresh, затем восстановить сеть и «Повторить» | Санитизированный код; секрет не показан; валидная операция повторяема | UI/log scan; API deltas | Invite/device fixture | P-AUTH-L | Network shaping shared AVD |

## D. Gateway, HTTP-контракт и защита границы

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| NET-01 | −Г | API-ИЗО | Нет bearer | Все 26 allowlisted mobile routes, включая query | 401 `AUTH_REQUIRED`; route не превращается в 404 | status/problem/traceId matrix | Нет данных | P-NET-A | Rate limit отдельный source |
| NET-02 | −Г | API-ИЗО | Нет/есть bearer | Unsupported method/path; nested admin; `//`,`..`,`%2e`,`%2f` | 404 до auth; без redirect/405/bypass | status + upstream count0 | Нет данных | P-NET-B | Параллельные probes с лимитом |
| NET-03 | − | API-ИЗО | Bearer principal A | Добавить spoof identity/role/workspace headers | Gateway удаляет/заменяет; backend видит только token identity | backend context + 404 cross-scope | Principals A/B | P-NET-C | Workspace pair |
| NET-04 | −Г | API-ИЗО | Authenticated mutating route | Нет/invalid/duplicate Idempotency-Key | 400; side effects0 | DB/audit/outbox deltas0 | Fixture entity | P-NET-D | Один entity sequential |
| NET-05 | +С | API-ИЗО | Idempotent operation | Тот же key+payload дважды; затем key+changed payload | Original replay; changed payload 409 reuse | same resource/version; idempotency row1 | Fixture entity | P-NET-D | После NET-04 |
| NET-06 | −Г | API-ИЗО | Versioned mutation | Missing/malformed If-Match, stale, valid | 400/409/2xx; stale без side effects | resource version/audit/outbox | Fixture task | P-NET-E | Один task sequential |
| NET-07 | −Г | API-ИЗО | Любой JSON route | Malformed JSON, unknown field, wrong type, oversize body | 4xx; no persistence; bounded response | status/problem; DB delta0 | Fixture scope | P-NET-F | Параллельно по route |
| NET-08 | −К | API-ИЗО | Rate-limit identity/source | N−1,N,N+1 concurrent requests | До границы проходят, лишнее 429; другие identity/source не затронуты | status histogram; limiter state | No business writes | P-NET-G | Отдельный source IP/key |
| NET-09 | − | API-ИЗО | Internal endpoint | Missing/invalid HMAC/timestamp/body hash/nonce | 400/401; nonce не принят при failed auth | service_nonces/audit0 | Unique nonces | P-NET-H | No shared nonce |
| NET-10 | +С | API-ИЗО | Валидный HMAC | Вызов; exact replay nonce; новый nonce same body | Первый исполняется; replay rejected; новый проходит согласно idempotency | nonce/idempotency/audit | Unique operation | P-NET-H | Sequential nonce chain |
| NET-11 | − | API-ИЗО | Mobile bearer | Попытка `/internal/*` и server internal port снаружи | Недоступно/404; internal identity не импersonated | boundary status + network exposure | Read-only | P-NET-I | Infra shared read-only |
| NET-12 | +Г | ЭМУ-СИС | Direct production HTTP transport | DNS/IPv4/IPv6/read timeout/refused/unreachable variants | Ошибка типизирована; нет произвольного URL fallback; один запрос | safe phase/category; request count | Network fixture endpoints allowlisted | P-NET-J | Network shaping per AVD |
| NET-13 | − | ЛОК-К | Network telemetry sink | Sink throws / message contains URL/token/query | Запрос не меняется; sink failure contained; only allowlisted category/host | unit oracle/source scan | No external IO | P-NET-K | Independent |
| NET-14 | +С | ЭМУ-СИС/API-ИЗО | Краткий timeout до Gateway | Создать offline op; 3 transient failures; восстановить сеть | Operation durable; backoff bounded; одна server mutation | Room/outbox + backend singleton | Fixture task/client | P-NET-L | Общий AVD network; sequential |

## E. Задачи: список, поля, состояния и результат

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| TASK-01 | + | ЭМУ-UI/API-ИЗО | Нет задач | Открыть список | Empty state и две доступные точки «+ Задача» без дубликата действия | UI hierarchy/screenshot | Empty workspace | P-TASK-A | One UI session |
| TASK-02 | +С | ЭМУ-UI/API-ИЗО | Online | Создать title из 1/300 Unicode chars | Placeholder сразу; canonical task после sync; title exact | UI/Room/outbox/API/audit | Task prefix A | P-TASK-B | One client sequential |
| TASK-03 | −Г | ЭМУ-UI/API-ИЗО | Create dialog | Blank/whitespace/301 chars | UI prevents/limits; API rejects bypass; no task | UI + DB delta0 | Empty workspace | P-TASK-C | Variants separate keys |
| TASK-04 | + | ЭМУ-UI | PLANNED/IN_PROGRESS/BLOCKED/DONE/CANCELLED | Переключить «Активные»/«Все»/«Готовые» | «Активные»=PLANNED/IN_PROGRESS/BLOCKED; «Все»=все пять состояний; «Готовые»=только DONE; CANCELLED доступна через «Все»; без дублей | visible IDs/status | Five tasks | P-TASK-D | One UI resource |
| TASK-05 | + | ЭМУ-UI/API-ИЗО | Task with UTC and +03 deadlines | List/detail/calendar | Instant preserved; display follows intended timezone rules; day boundary correct | API dueAt + rendered text | Time fixtures | P-TASK-E | Freeze test clock/timezone |
| TASK-06 | + | ЭМУ-UI/API-ИЗО | Task exists | Open detail online | Title,status,due,visibility,description,result/version match API | UI/API/Room correlation | Task A | P-TASK-F | Read-only after seed |
| TASK-07 | − | ЭМУ-UI | Cached task, network off | Open detail | Core cached fields remain; explicit offline notice; no false empty detail | UI + Room | Task cache A | P-TASK-G | Network off shared AVD |
| TASK-08 | +С | ЭМУ-UI/API-ИЗО | Task v1 | Edit title only | Only title changes; description/due/visibility preserved | request payload; task v2; audit1/outbox1 | Task E1 | P-TASK-H | One task sequential |
| TASK-09 | +С | ЭМУ-UI/API-ИЗО | Task v1 full fields | Edit description only, including Unicode/newlines | Exact description; other fields preserved | API + UI detail | Task E2 | P-TASK-H | Separate task can parallel |
| TASK-10 | +С | ЭМУ-UI/API-ИЗО | Description present | Clear description explicitly | Null persisted and section hidden; other fields preserved | API JSON null + UI | Task E3 | P-TASK-H | Separate task |
| TASK-11 | +С | ЭМУ-UI/API-ИЗО | Due present/absent | Set RFC3339 then clear blank | Set exact instant then null; unrelated fields preserved | API + calendar change | Task E4 | P-TASK-I | One task sequential |
| TASK-12 | −Г | ЭМУ-UI/API-ИЗО | Edit form | Invalid RFC3339; extreme valid offset; invalid API type | UI/API reject invalid without enqueue/side effect | UI error; Room/API deltas | Task E5 | P-TASK-I | Variants sequential |
| TASK-13 | +С | ЭМУ-UI/API-ИЗО | Owner task | PRIVATE→TEAM→ASSIGNED | Allowed transitions render exact visibility and ACL follows contract | UI/API/can_read | Task E6 + principal B | P-TASK-J | Shared ACL fixture |
| TASK-14 | − | API-ИЗО | Member/assigned task | Attempt content/due/visibility without permission | 404/403; no version/audit/outbox change | DB/API | Task owned by A | P-TASK-K | Principals A/B |
| TASK-15 | +С | ЭМУ-UI/API-ИЗО | PLANNED | PLANNED→IN_PROGRESS→BLOCKED→PLANNED→DONE | Every valid transition version+1; focus/calendar reflect state | API/UI/change/audit | Task S1 | P-TASK-L | Sequential state machine |
| TASK-16 | −Г | API-ИЗО | DONE/CANCELLED terminal | Attempt any outgoing status; DONE without completion invariant | Typed conflict/invalid; state/version unchanged | API/DB/audit0 | Tasks S2/S3 | P-TASK-M | Separate terminal tasks |
| TASK-17 | +С | ЭМУ-UI/API-ИЗО | Nonterminal vN | Add result Unicode up to 50000; then mark DONE | Result exact; terminal display; TaskRun status independent | UI/API/audit | Task R1 | P-TASK-N | Sequential |
| TASK-18 | −Г | ЭМУ-UI/API-ИЗО | Detail | Empty result/50001; stale version | UI/API reject; draft retained where applicable | UI + DB delta0 | Task R2 | P-TASK-O | One task variants |
| TASK-19 | +С | API-ИЗО | Same create/update operation | Exact replay then changed replay payload | Singleton task/version/audit; changed reuse rejected | idempotency/audit/outbox | Task I1 | P-TASK-P | Sequential same key |
| TASK-20 | − | API-ИЗО | Private task owner B | Owner A list/get/calendar/focus/inbox spoof probes | Hidden as 404/excluded across every read surface | response sets + can_read | Two principals | P-TASK-Q | Shared ACL fixture read-only |

## F. Offline outbox, синхронизация, cursor и конфликт

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| SYNC-01 | +С | ЭМУ-СИС/API-ИЗО | Network off | CREATE_TASK→kill process→launch→network on | PENDING+placeholder survive; one canonical task; local ID remapped; APPLIED | Room before/after; backend singleton | Client C1/task O1 | P-SYNC-A | One AVD lifecycle |
| SYNC-02 | +С | ЭМУ-СИС/API-ИЗО | Canonical task cached, offline | CHANGE_TASK_STATUS; restart; sync | Optimistic UI durable; exact status once | Room/outbox/API | Task O2 | P-SYNC-B | Per task sequential |
| SYNC-03 | +С | ЭМУ-СИС/API-ИЗО | Cached task offline | ADD_TASK_RESULT Unicode; restart; sync | Draft/result durable and applied once | Room/outbox/API | Task O3 | P-SYNC-B | Separate task parallel |
| SYNC-04 | +С | ЭМУ-СИС/API-ИЗО | Cached full task offline | UPDATE_TASK partial fields; restart; sync | Dirty fields applied; server concurrent untouched fields preserved | payload + API values | Task O4 | P-SYNC-C | Controlled server bump |
| SYNC-05 | +С | ЭМУ-СИС/API-ИЗО | Focus vN cached | SET_FOCUS offline; restart; sync | Ordered list durable and applied once | Room/outbox/API focus version | Focus F1 | P-SYNC-D | Shared focus principal sequential |
| SYNC-06 | +С | ЭМУ-СИС/API-ИЗО | Inbox unread cached | MARK_INBOX_READ offline; restart; sync | State READ once; event retained | Room/API/version/audit | Inbox I1 | P-SYNC-E | Per event |
| SYNC-07 | +С | ЭМУ-СИС/API-ИЗО | Offline create localId plus dependent status/result/focus | Queue chain; sync one-by-one | Every dependency rewritten to canonical ID/version; ordered apply; no local ghost | outbox payload evolution; API singleton | Client C2 | P-SYNC-F | One client strictly sequential |
| SYNC-08 | СГ | ЭМУ-СИС/API-ИЗО | 101 pending operations | Sync | Batches ≤100; all eventually applied in client order | request batch sizes/order; DB counts | Client C3 | P-SYNC-G | Dedicated client/cursor |
| SYNC-09 | +С | ЭМУ-СИС/API-ИЗО | Applied op response lost | Interrupt after server apply before local record; resume | Server replay; local APPLIED; no duplicate audit/task | idempotency + Room | Client C4 | P-SYNC-H | Fault injection local transport |
| SYNC-10 | −С | ЭМУ-СИС | Server returns missing/extra/duplicate operation result | Sync phase | Entire response rejected; cursor and outbox not falsely advanced | Room transaction/cursor | Fake transport only | P-SYNC-I | Local contract fixture |
| SYNC-11 | +С | ЭМУ-СИС/API-ИЗО | Cursor C0; changes after C0 | Pull pages | Opaque cursor monotonic; each change applied before cursor commit | cursor/Room/API sequences | Client C5 | P-SYNC-J | Dedicated principal/cursor |
| SYNC-12 | − | API-ИЗО | Cursor from workspace/principal A | Use as B or malformed/rewound | Reject; no data leak; B cursor unchanged | 4xx/DB/no payload | Principals A/B | P-SYNC-K | Cursor pair |
| SYNC-13 | СК | ЭМУ-СИС | Delayed old sync and fresh sync | Complete fresh first, then delayed old | Old response cannot replace fresher data/cursor | Room versions/cursor | Fake transport | P-SYNC-I | Controlled concurrency |
| SYNC-14 | СГ | ЭМУ-СИС | Same entity/version but distinct event IDs; duplicate/stale events | Apply events | New event does not disappear solely by same version; duplicate/stale handled per entity/version contract | Room push/change rows | Local fixture | P-SYNC-L | No backend needed |
| SYNC-15 | −С | ЭМУ-UI/API-ИЗО | Local UPDATE v1; server v2 | Sync | Outbox CONFLICT/currentVersion2; server untouched; conflict UI replaces success notice; draft quoted | UI/Room/API/audit0 | Task C6 | P-SYNC-M | One task/version sequential |
| SYNC-16 | +С | ЭМУ-UI/API-ИЗО | Recorded changedFields conflict | Explicit «Загрузить v2»; compare; save | Form shows server plus only intended local dirty fields; old op SUPERSEDED atomically; one new PENDING v2 | UI/Room transaction/payload | Task C6 | P-SYNC-M | После SYNC-15 |
| SYNC-17 | −С | ЭМУ-UI/API-ИЗО | Legacy conflict without changedFields | Open/attempt Save; explicit compare; fresh edit | Save blocked before compare; no unsafe merge; fresh edit records intent | UI/Room/outbox | Legacy op C7 | P-SYNC-N | Sequential |
| SYNC-18 | −С | ЭМУ-UI | Replacement enqueue forced to fail | Retry conflict | Old conflict remains CONFLICT, no supersede/no lost draft | Room transaction oracle | Local fault fixture | P-SYNC-O | Local only |
| SYNC-19 | С | ЭМУ-UI/API-ИЗО | Retry from conflict gets newer v3 conflict | Sync retry; reopen app | CurrentVersion advances; draft/dirty fields remain; no endless auto retry | UI/Room/API | Task C8 | P-SYNC-P | One task sequential |
| SYNC-20 | − | ЭМУ-UI | Conflict operationId belongs task A, detail B | Attempt supersede from B | SQL task/entity/action scope prevents transition and enqueue | Room rows unchanged | Tasks A/B | P-SYNC-O | Local DB fixture |
| SYNC-21 | +С | ЭМУ-СИС/API-ИЗО | Server DELETE/UPSERT for task/inbox/doc/assignment/calendar | Pull changes | Exact local row upsert/delete; no unrelated deletion | Room tables + cursor | Dedicated workspace | P-SYNC-Q | Changes can seed parallel by entity type |
| SYNC-22 | −С | ЭМУ-СИС/API-ИЗО | Permanent REJECTED mutation | Sync/restart/refresh | Не ретраится бесконечно; пользователь видит безопасный код; cursor continues | Room state/request count | Client C9 | P-SYNC-R | Dedicated op |

## G. Фокус, календарь и входящие

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| FOC-01 | +С | ЭМУ-UI/API-ИЗО | ≥3 active tasks | Открыть редактор; выбрать; ↑/↓; сохранить | Exact unique order ≤20; version+1 | UI order/API focus/outbox | Principal F1 | P-FOC-A | Shared focus sequential |
| FOC-02 | −Г | ЭМУ-UI/API-ИЗО | 0/20/21 tasks; duplicate IDs | Save/probe API | 0 and 20 valid; 21/duplicate/hidden/missing rejected | UI/API/DB | Principal F2 | P-FOC-B | Dedicated focus |
| FOC-03 | С | ЭМУ-UI/API-ИЗО | Focus contains task | Mark task DONE/CANCELLED/delete access | It disappears from visible focus and snapshot remains consistent | UI/API/change | Task F3 | P-FOC-C | Same task sequential |
| FOC-04 | −С | ЭМУ-UI/API-ИЗО | Two clients focus v1 | A saves v2; B saves v1 | B conflict; no last-write-wins; B selection retained | API/Room/UI | Principal F4 devices2 | P-FOC-D | Shared focus, deliberate race |
| CAL-01 | + | ЭМУ-UI/API-ИЗО | Tasks before/inside/after range | Open calendar interval | Only due tasks in range, stable ascending order | IDs/dueAt API vs UI | Calendar C1 | P-CAL-A | Read-only after seed |
| CAL-02 | Г | ЭМУ-UI/API-ИЗО | UTC/+03/day-boundary deadlines | Change emulator timezone | Instant/order correct; display policy explicit; no double shift | rendered vs API epoch | Calendar C2 | P-CAL-B | Freeze timezone per run |
| CAL-03 | С | ЭМУ-UI/API-ИЗО | Due task | Clear/change due; DONE/CANCELLED | Calendar item upsert/delete matches contract | change log + UI | Task C3 | P-CAL-C | One task sequential |
| CAL-04 | + | ЭМУ-UI | Calendar card | Tap task then back | Exact detail opens and returns without losing calendar state | navigation/UI | Task C4 | P-CAL-D | One UI session |
| INB-01 | + | ЭМУ-UI/API-ИЗО | UNREAD/READ/RESOLVED events | Filter/list/mark read | Sequence ascending/bounded; state changes exact | UI/API/version/audit | Inbox A | P-INB-A | Event-specific parallel possible |
| INB-02 | −Г | API-ИЗО | afterSequence 0, exact, beyond, negative | GET inbox | Correct tail; invalid rejected; no duplicates | response IDs/sequences | Inbox B | P-INB-B | Read-only |
| INB-03 | +С | ЭМУ-UI/API-ИЗО | Assignment PENDING event online | Accept once | Assignment accepted; task/access appears; event resolves | UI/API/change sequence | Assignment A | P-INB-C | One assignment sequential |
| INB-04 | +С | ЭМУ-UI/API-ИЗО | Assignment PENDING | Decline | Terminal DECLINED; no task access; event resolves | API/UI/audit | Assignment B | P-INB-D | Separate assignment |
| INB-05 | +С | ЭМУ-UI/API-ИЗО | Approval PENDING | Approve/reject in separate fixtures | Exact terminal; one decision side effect; event resolves | API/UI/audit | Approvals A/B | P-INB-E | Parallel separate approvals |
| INB-06 | − | ЭМУ-UI | Offline and decision event | Tap decision | Disabled/explicit «требуется подключение»; no local forbidden outbox | UI + Room no mutation | Cached event | P-INB-F | Network off |
| INB-07 | + | ЭМУ-UI | Generic unread event | «Отметить прочитанным» offline then sync | Optimistic/durable READ once | UI/Room/API | Inbox C | P-INB-G | Same event sequential |
| INB-08 | − | API-ИЗО | Event belongs B | A list/update/deep link | Excluded/404; title/task not leaked | API sets/UI generic state | Principals A/B | P-INB-H | ACL pair |

## H. Назначения, согласования, предложения и ACL

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| ASN-01 | +С | ЭМУ-UI/API-ИЗО | Owner task v1; approved TASK_ASSIGN; member | Create assignment with canRedelegate false/roots | PENDING once; member task unreadable until ACCEPT | API/can_read/audit/inbox | Task A1 | P-ASN-A | Approval before assignment |
| ASN-02 | +С | API-ИЗО | ASN-01 pending, member cursor captured | ACCEPT | ASSIGNMENT UPSERT→TASK UPSERT→CALENDAR after cursor; access true | ordered change seq + UI after sync | Task A1 | P-ASN-A | После ASN-01 |
| ASN-03 | +С | API-ИЗО | Pending assignment | DECLINE | Terminal once; no task/document grant | state/audit/change/can_read | Task A2 | P-ASN-B | Separate task |
| ASN-04 | − | API-ИЗО | Pending assignment for member B | Wrong actor A decides | 404; no state/audit change | DB/API | Assignment A3 | P-ASN-C | Principals A/B |
| ASN-05 | −Г | API-ИЗО | Assign task | Missing member/doc root, root from other task, stale task version, invalid decision | 400/409; no assignment/grant | DB deltas/audit0 | Task A4 | P-ASN-D | Variants distinct keys |
| ASN-06 | +С | API-ИЗО | Same key/payload | Create/decision replay; changed payload/new opposite decision | Exact replay; mismatch/terminal opposite 409 | singleton rows/audit1 | Assignment A5 | P-ASN-E | Sequential |
| ASN-07 | КС | API-ИЗО | One PENDING assignment | Concurrent ACCEPT vs DECLINE distinct keys | Exactly one 2xx, one typed 409; one audit; TASK change iff ACCEPT | HTTP pair/DB/change | Assignment A6 | P-RACE-ASN | Dedicated task; no other writers |
| ASN-08 | +С | API-ИЗО | Accepted assignment canRedelegate=true + permission | Redelegate through approved flow | New assignment valid, scope no wider than source grant | grants/can_read/audit | Assignment A7 | P-ASN-F | Sequential graph |
| ASN-09 | − | API-ИЗО | canRedelegate=false or permission absent | Redelegate | 404/denied; no new assignment | DB delta0 | Assignment A8 | P-ASN-G | Separate task |
| APP-01 | +С | API-ИЗО | Authorized task/run/capability | REQUEST_APPROVAL | One PENDING approval/inbox; exact scope | approval/audit/inbox | Approval P1 | P-APP-A | Unique run/task |
| APP-02 | − | API-ИЗО | Invalid decider/capability/cross-task/taskless disallowed | Request | Rejected, no approval/inbox | DB delta0 | Approval P2 | P-APP-B | Variants isolated |
| APP-03 | +С | ЭМУ-UI/API-ИЗО | PENDING | APPROVE and REJECT in separate fixtures | One terminal decision, exact audit and inbox resolution | UI/API/audit | Approvals P3/P4 | P-APP-C | Parallel distinct approvals |
| APP-04 | КС | API-ИЗО | PENDING | Concurrent APPROVE vs REJECT | Exactly one terminal winner; loser typed conflict; audit1 | HTTP/DB | Approval P5 | P-RACE-APP | Dedicated approval |
| PROP-01 | +С | API-ИЗО | Agent-derived CREATE_TASK | Execute intent | Only PENDING proposal; no active task before human | proposal/task counts/audit | Proposal R1 | P-PROP-A | Unique run |
| PROP-02 | +С | API-ИЗО | PENDING proposal | ACCEPT | Exactly one PLANNED task; proposal ACCEPTED | task/proposal/audit/change | Proposal R1 | P-PROP-A | После PROP-01 |
| PROP-03 | +С | API-ИЗО | PENDING | REJECT | REJECTED; no created task | counts/audit | Proposal R2 | P-PROP-B | Separate proposal |
| PROP-04 | +С | API-ИЗО | PENDING + valid assignee | DELEGATE | One task + one assignment; exact assignee; proposal DELEGATED | DB relationships/audit | Proposal R3 | P-PROP-C | Valid principal |
| PROP-05 | − | API-ИЗО | DELEGATE missing/invalid assignee | Decide | 400; proposal remains pending; no task/assignment | DB delta0 | Proposal R4 | P-PROP-D | Dedicated proposal |
| PROP-06 | СК | API-ИЗО | PENDING | Concurrent ACCEPT vs REJECT/DELEGATE | One 2xx, one typed 409; task count matches winner; audit1 | HTTP/DB/change | Proposal R5 | P-RACE-PROP | Dedicated proposal |
| ACL-01 | − | API-ИЗО | Member private task; owner same workspace | Owner list/get/update/agent/docs | All denied/excluded absent explicit grant | API/can_read/audit | Principals O/M | P-ACL-A | Shared ACL fixture |
| ACL-02 | +С | API-ИЗО | Assignment grants task + selected doc roots | Member reads task, selected descendants, sibling | Task+selected true; sibling false; revocation removes inherited access | API/can_read_document | Tree ACL2 | P-ACL-B | One assignment sequential |

## I. Документы

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| DOC-01 | +С | API-ИЗО/ЭМУ-UI | Authorized tool/task | Write `root.md` valid Markdown | Metadata/content/checksum v1; tree visible after sync | API/DB/UI/cache | Task D1 | P-DOC-A | Tool approval/auth first |
| DOC-02 | +С | API-ИЗО/ЭМУ-UI | Root exists | Write nested children/siblings in non-sort order | Tree renders stable depth-first parent-before-child | API order + UI hierarchy | Task D2 | P-DOC-B | One tree writer sequential |
| DOC-03 | −Г | API-ИЗО | Write endpoint | Traversal, backslash, absolute, dot segments, non-md, >500 | 4xx before SQL; documents/audit unchanged | DB delta0/problem | Task D3 | P-DOC-C | Variants isolated keys |
| DOC-04 | − | API-ИЗО | Two tasks | parentDocumentId from other task/self/cycle | Rejected by service/DB; no partial row | constraints + counts | Tasks D4a/b | P-DOC-D | One graph sequential |
| DOC-05 | Г | API-ИЗО | Deep tree at supported bound | Create at max depth/size then exceed | Bound accepted; overflow rejected predictably, no recursion failure | status/DB/query time | Task D5 | P-DOC-E | Dedicated tree |
| DOC-06 | +С | API-ИЗО | Existing doc checksum C1 | Update with expected C1 | v2 exact markdown/checksum | API/DB | Doc D6 | P-DOC-F | Sequential versions |
| DOC-07 | −С | API-ИЗО | Existing doc C2 | Update with stale/wrong checksum | Typed conflict; v/content/audit unchanged | API/DB | Doc D7 | P-DOC-G | Dedicated doc |
| DOC-08 | −Г | API-ИЗО | Write | Empty/301 title; >1MB markdown; malformed checksum; media/reference forbidden by client policy | Reject without partial update | API/DB delta0 | Docs variants | P-DOC-H | Parallel tasks |
| DOC-09 | +С | ЭМУ-UI/API-ИЗО | Metadata synced | Open document online | Markdown exact, verified checksum, `fromCache=false`; then cached | UI/repository/cache hash | Doc D9 | P-DOC-I | One client/doc |
| DOC-10 | +С | ЭМУ-СИС | Verified cache exists | Network off; reopen | Verified cached content shown with cache state | UI/cache row | Doc D9 | P-DOC-I | После DOC-09 |
| DOC-11 | −С | ЭМУ-СИС | Good cache exists | Server/mock wrong checksum or media payload | New content rejected; prior verified cache retained | Repository result/cache hash | Doc D10 | P-DOC-J | Local controlled API |
| DOC-12 | − | API-ИЗО/ЭМУ-UI | No task/document ACL | List/get/deep link by outsider | 404/excluded; title/path/markdown not leaked | API/UI + audit | Principals A/B | P-DOC-K | ACL fixture |
| DOC-13 | С | API-ИЗО/ЭМУ-UI | Assignment selected root | Revoke assignment; refresh/open cache | Metadata/access disappears; cached content not exposed after auth scope loss | can_read + UI/repository | Assignment D13 | P-DOC-L | Sequential revoke |
| DOC-14 | − | ЭМУ-UI | Offline | Attempt document write from mobile | No write controls/outbox/API call; read-only UX | UI/Room/request count | UI-only | P-DOC-M | Independent |

## J. Агент, разговоры и запуски

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| AGT-01 | +С | ЭМУ-UI/API-ИЗО | Authenticated | Отправить Unicode text без taskId | One taskless run/conversation; user bubble once; terminal response | UI/run/dispatch/outbox/audit | Conversation A1 | P-AGT-A | Provider cost bounded; one message |
| AGT-02 | +С | ЭМУ-UI/API-ИЗО | Readable task | Submit text with taskId | Run scoped to exact task; no cross-task context | API/run/context audit | Task A2 | P-AGT-B | Dedicated task |
| AGT-03 | −Г | ЭМУ-UI/API-ИЗО | Agent input | Blank/20001 chars/malformed task UUID | UI/API reject; no run/dispatch | request count/DB delta0 | No fixture | P-AGT-C | Variants parallel |
| AGT-04 | − | API-ИЗО | Task from other workspace/private | Submit scoped command | 404/denied; no run/provider call | run/dispatch counts0 | ACL pair | P-AGT-D | Separate principals |
| AGT-05 | +С | API-ИЗО/ЭМУ-UI | Run transitions | QUEUED→RUNNING→WAITING_INPUT→RUNNING→SUCCEEDED | Valid versions and visible terminal message; task state unchanged automatically | run/audit/UI | Run A5 | P-AGT-E | One run sequential |
| AGT-06 | +С | API-ИЗО/ЭМУ-UI | Run transitions | QUEUED/RUNNING→CANCELLED | No provider/tool after cancel; terminal immutable | dispatch/log/DB/UI | Run A6 | P-AGT-F | Dedicated run |
| AGT-07 | −С | API-ИЗО/ЭМУ-UI | Unsupported intent/retry budget | Dispatch until exhausted | Bounded attempts; DLQ; run FAILED with sanitized code | attempts/outbox/run/UI | Run A7 | P-AGT-G | No global provider change |
| AGT-08 | +С | API-ИЗО | FAILED run | Explicit retry | New run ID/attempt; old immutable; new dispatch exactly once | run pair/outbox | Run A8 | P-AGT-H | Sequential retry |
| AGT-09 | − | API-ИЗО | Terminal run | Attempt terminal escape/stale version/false success without verified tool result | Conflict/reject; no mutation | DB/audit | Runs A9 | P-AGT-I | Separate runs |
| AGT-10 | +С | ЭМУ-UI/API-ИЗО | ≥101 runs in conversation | GET pages limit 1/50/100 with cursor | Stable descending/bounded pagination, no duplicates/omissions | concatenated IDs/API | Conversation A10 | P-AGT-J | Dedicated conversation; cursor sequential |
| AGT-11 | − | API-ИЗО | Conversation/run owned by B | A lists with B conversation/cursor | 404/empty; no text/error/result leak | API payload | Principals A/B | P-AGT-K | ACL fixture |
| AGT-12 | −Г | API-ИЗО | Runs with tool result/internal metadata | List history | Only public redacted fields; no prompts, secrets, tool args, human content in audit metadata | schema/secret scan | Conversation A12 | P-AGT-L | Read-only after seed |
| AGT-13 | +С | ЭМУ-UI/API-ИЗО | Conversations old/new | Launch app; restore latest | Most recently updated ANDROID conversation selected; history survives repository recreation | UI/API/Room | Conversations A/B | P-AGT-M | One principal sequential |
| AGT-14 | С | ЭМУ-UI/API-ИЗО | Agent response changes RUNNING→terminal | Background sync/push refresh | Existing message updated in place, no duplicate bubble | Room message IDs/UI | Conversation A14 | P-AGT-N | One conversation |
| AGT-15 | +С | API-ИЗО | Agent side-effect CREATE_TASK | Execute | Agent-derived creates proposal; human-originated authorized create can apply task; audit correlates | proposal/task/run/audit | Runs A15a/b | P-AGT-O | Separate operations |
| AGT-16 | −С | API-ИЗО/N8N | Correlation/result mismatch or tool reports false success | Complete run | Action Executor rejects; run not SUCCEEDED; no side effect | executor response/audit/task counts | Run A16 | P-AGT-P | Controlled fixture response |

## K. Голосовой ввод

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| VOI-01 | +С | ЭМУ-UI | AVD image has recognizer + Russian language data/input | Голос→распознать русскую фразу | Review dialog shows actual transcript; no send before confirmation | screenshot/hierarchy; runs delta0 | Conversation V1 | P-VOICE | Возможность конкретного AVD предварительно подтвердить |
| VOI-02 | +С | ЭМУ-UI/API-ИЗО | Review dialog | «Использовать»→исправить текст→«Отправить» | Edited text sent once; one run | UI exact text + backend singleton | Conversation V1 | P-VOICE | После VOI-01 |
| VOI-03 | −С | ЭМУ-UI | Existing draft | Start recognizer then cancel/back/no speech | Existing draft unchanged; no run | UI + runs delta0 | Conversation V2 | P-VOICE | One UI sequential |
| VOI-04 | − | ЭМУ-UI | Recognizer unavailable/disabled | Нажать Голос | Safe error; text input remains usable; no crash | UI/logcat | AVD without recognizer | P-VOICE-B | Separate AVD |
| VOI-05 | − | ЭМУ-UI | Recognition returns empty/error | Complete activity result | No review/send; draft preserved | UI/state | Fake activity result | P-VOICE-C | Instrumentation |
| VOI-06 | Г | ЭМУ-UI | Long/Unicode/punctuation transcript | Recognize/review | Bounded editable text; `Ё/й`, time numerals visible; no implicit semantics claim | exact transcript screenshot | Local recognizer | P-VOICE | Provider variability recorded |
| VOI-07 | − | ЛОК-К | APK/source | Inspect storage/network/logs | Raw audio is not persisted/uploaded by app; system recognizer intent only | source/manifest/file/network scan | No user data | P-VOICE-D | Independent |
| VOI-08 | Г | ВНЕ ЭТАПА | Physical mic/OEM speech provider | Three real Russian utterances + cancel | Human microphone path and OEM recognizer verified | recording-free UI evidence + singleton runs | Temporary user only | P-PHYSICAL-LATER | Требует физическое устройство; не блокирует emulator catalog execution |

## L. Push/FCM, уведомления и маршрутизация

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| PUSH-01 | +С | ЭМУ-UI/API-ИЗО | AVD Google Play, authenticated device, permission granted | Получить FCM token/auto registration path | Exactly one enabled registration with ANDROID/appVersion; no token in logs | DB hash/count, log secret scan | Device P1 | P-PUSH-A | Конкретный Play image availability gate |
| PUSH-02 | +С | ЭМУ-UI/API-ИЗО | Registration exists | `onNewToken` rotation | New token pending then registered; old disabled/updated per contract; sync business result unaffected by push failure | registration rows/timestamps | Device P1 | P-PUSH-A | Sequential token lifecycle |
| PUSH-03 | +С | API-ИЗО | Enabled registration | DELETE unregister + same key replay | 204/204; enabled true→false→false; device active | DB/idempotency | Device P2 | P-PUSH-B | Dedicated device |
| PUSH-04 | − | API-ИЗО | Registration route | Missing auth/key, malformed/short token, wrong platform/appVersion, changed replay payload | 4xx/409; no unintended row | DB deltas | Device P3 | P-PUSH-C | Variants isolated keys |
| PUSH-05 | +С | ЭМУ-UI/API-ИЗО | Permission granted; app foreground | TASK_CREATED neutral data payload | One WorkManager job, one authoritative refresh, notification opens exact task | push event/requests/UI | Task P5 | P-PUSH-D | Unique eventId |
| PUSH-06 | +С | ЭМУ-UI/API-ИЗО | Background | TASK_CHANGED | Notification generic, no title/content; tap exact task after unlock | notification dump + route/API | Task P6 | P-PUSH-E | One AVD notification state |
| PUSH-07 | +С | ЭМУ-СИС/API-ИЗО | Process dead/cold | TASK_RUN_CHANGED | App starts, unlocks, opens exact agent conversation, refreshes authoritative history | notification/deep link/run UI | Run P7 | P-PUSH-F | One AVD lifecycle |
| PUSH-08 | +С | ЭМУ-UI/API-ИЗО | App any state | INBOX_EVENT_CREATED | Generic task notification routes to authoritative target task/inbox; no embedded human text | raw payload + UI/API | Inbox P8 | P-PUSH-G | Unique event |
| PUSH-09 | +С | ЭМУ-UI/API-ИЗО | App any state | APPROVAL_DECIDED | Generic signal; authoritative inbox/task refresh; no approval details in payload | payload schema/UI | Approval P9 | P-PUSH-H | Unique event |
| PUSH-10 | −С | ЭМУ-СИС | Android 13+, permission denied | Deliver valid data payload | Authoritative refresh still scheduled; notification absent | WorkManager/request + notification dump | AVD P10 | P-PUSH-I | Permission state shared AVD |
| PUSH-11 | +С | ЭМУ-СИС | После PUSH-10 | Grant permission; deliver next event | Notification appears only for new accepted event; prior event not duplicated | notification IDs/event store | AVD P10 | P-PUSH-I | Sequential permission transition |
| PUSH-12 | С | ЭМУ-СИС | Valid event repeated | Deliver same eventId twice/concurrently | Unique work + durable event make one refresh/notification | WorkManager/event row/request count | Event P12 | P-PUSH-J | Dedicated event |
| PUSH-13 | СГ | ЭМУ-СИС | Entity latest v3 | Deliver v2 stale, v3 duplicate, v4 new | Stale/duplicate no refresh/notify; v4 accepted | event decisions/request counts | Entity P13 | P-PUSH-K | Sequential versions |
| PUSH-14 | −Г | ЭМУ-СИС | Firebase service | Malformed UUID/version/type/entityType/route/conflicting IDs/unknown keys | Fail closed: no work, request, notification | scheduler/event/request delta0 | Payload variants | P-PUSH-L | Parallel fresh event IDs |
| PUSH-15 | +С | API-ИЗО | Business events and enabled registration | Generate TASK/RUN/INBOX/APPROVAL | Outbox seeded once only after accepted transaction; payload data-only routing IDs | outbox/delivery/payload secret scan | Workspace P15 | P-PUSH-M | Separate entities can parallel |
| PUSH-16 | −С | API-ИЗО | Provider transient/permanent response | Dispatch retries | Bounded backoff then DELIVERED or DLQ; transaction acceptance not rolled back | delivery attempts/state | Fake provider/local integration | P-PUSH-N | No external send required |
| PUSH-17 | С | API-ИЗО | Event created before migration cutoff vs after | Publisher scan | Historical backlog not seeded; new events delivered | cutoff/outbox counts | Disposable DB/local | P-PUSH-O | Contract-level |
| PUSH-18 | Г | ВНЕ/УСЛОВНО | AVD Google Play image may or may not obtain real token | Inventory image/GMS; send one isolated real FCM event | If supported, end-to-end real delivery closes on AVD; otherwise mark current-environment blocker, not product fail | token registration + FCM accepted/delivery + UI | Dedicated AVD/device/workspace | P-PUSH-REAL | В принципе доступно эмулятору; подтверждается лидом среды |

## M. Telegram-привязка и OpenClaw Poruchik tools

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| TGL-01 | +С | ЭМУ-UI/API-ИЗО | Authenticated device, unlinked | Create link nonce; consume trusted Telegram identity | One active binding; status linked exact user ID server-side | API/DB/audit | Principal T1/test chat | P-TGL-A | External trusted chat only when authorized |
| TGL-02 | −С | API-ИЗО | Link nonce | Expired/replayed/wrong actor/chat/bot/HMAC | Fail closed; no binding/policy widening | DB/audit/nonce | Principal T2 | P-TGL-B | Separate nonces |
| TGL-03 | +С | ЭМУ-UI/API-ИЗО | Linked | Revoke + same key replay; status | 204 replay-safe; status unlinked; policy/binding effects scoped | API/DB | Principal T3 | P-TGL-C | Dedicated binding |
| TGL-04 | − | API-ИЗО | Principal A/B | Status/revoke cross-principal | No leak/mutation | API/DB | A/B | P-TGL-D | ACL pair |
| PRT-01 | + | ЛОК-К/API-ИЗО | Trusted Android run context | Each of 13 `poruchik_*` tools schema | Runtime identity injected, model cannot override; signed dispatch stable | plugin manifest + Action API audit | Tool fixture per name | P-PRT-A | Parallel different workspace/tool |
| PRT-02 | − | ЛОК-К | Untrusted Telegram/non-owner/wrong actor/chat; malformed Android context | Invoke tool | Reject before network | fetch count0/error code | Context variants | P-PRT-B | Pure local |
| PRT-03 | −Г | ЛОК-К | Tool args | Unknown property, invalid UUID/state/date/version, >limits | Schema rejects before HTTP; no secret/URL/identity args exposed | validator/fetch count0 | Pure local | P-PRT-C | Parallel definitions |
| PRT-04 | +С | API-ИЗО | `poruchik_create_task` human vs agent derived | Invoke | Human authorized outcome/APPLIED; agent derived proposal pending as policy requires | task/proposal/audit | Runs T4a/b | P-PRT-D | Separate run contexts |
| PRT-05 | +С | API-ИЗО | Tasks/status/due fixtures | list/update/focus/calendar/inbox/read_documents tools | Results scoped, typed and consistent with mobile API | tool response vs DB/API | Workspace T5 | P-PRT-E | Read tools parallel; mutations isolated |
| PRT-06 | +С | API-ИЗО | Approval/assignment/proposal fixtures | request/decide/assign tools | Required approvals and exact terminal states; one side effect | audit/resource counts | Workspace T6 | P-PRT-F | Decision entities separate |
| PRT-07 | −С | API-ИЗО | Upstream correlation mismatch/false success/oversize/timeout | Tool call | Fail closed, sanitized, no business success | plugin/executor/audit | Fault fixture | P-PRT-G | Local mock preferred |
| PRT-08 | С | ЛОК-К | Same toolCallId vs changed args | Retry | Stable idempotency same call; changed payload cannot silently reuse | request envelope/hash | Pure local | P-PRT-H | One toolCall chain |

## N. Напоминания, inline confirmation и scheduler

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| REM-01 | +С | API-ИЗО/Telegram | Trusted owner/chat/policy | `reminder_create` one-time Moscow | PENDING proposal + inline ✅/❌; no active task before click | pending/task/audit/message | Marker R1 | P-REM-CHAT | Один chat/pending строго последовательно |
| REM-02 | +С | Telegram/API-ИЗО | REM-01 pending | Genuine ✅ | One ACTIVE reminder/version1/occurrence; keyboard removed or terminal acknowledgement | callback audit/task/message | Marker R1 | P-REM-CHAT | После REM-01 |
| REM-03 | +С | Telegram/API-ИЗО | Separate create pending | Genuine ❌ | Pending cancelled; no reminder/occurrence | callback/task counts/UI | Marker R2 | P-REM-CHAT | После capture; same chat sequential |
| REM-04 | + | API-ИЗО/Telegram | Active reminders incl target | `reminder_list` states/limit | Returns authorized task_id/current_version/public handle, canonical states only | tool result/DB scope | Marker R3 | P-REM-CHAT | Before any mutation selection |
| REM-05 | − | API-ИЗО | Cross actor/chat, unsupported state/limit | list | Empty/denied/22023 mapped; no UUID outside scope | result/DB | Actor/chat pair | P-REM-A | Isolated API no external message |
| REM-06 | +С | Telegram/API-ИЗО | Target just listed | `reminder_reschedule` exact task_id/version | Pending proposal; old schedule stays active until confirm | pending/version/occurrences | Marker R3 | P-REM-CHAT | После REM-04 |
| REM-07 | +С | Telegram/API-ИЗО | REM-06 | Genuine ✅ | Same task version+1; old occurrences superseded; new due Moscow exact | DB/audit/UI ack | Marker R3 | P-REM-CHAT | Sequential |
| REM-08 | +С | Telegram/API-ИЗО | Active target listed | `reminder_cancel`; genuine ✅ | Task CANCELLED; future pending/retry/lease/sending/uncertain=0; old baseline unchanged | DB/audit/UI | Marker R4 | P-REM-CHAT | Sequential |
| REM-09 | −С | ЛОК-К/API-ИЗО | Mutation without latest list; uses pending_action_id as task_id | Invoke reschedule/cancel | `REMINDER_SELECTION_REQUIRED`; turn closes; no HTTP after guard/no mutation | fetch count/DB delta0 | Pure/local + DB readonly | P-REM-B | No shared chat |
| REM-10 | −С | ЛОК-К | Action API returns deterministic ACTION_REJECTED | list→mutation rejected→model tries other actions | Current run closes; no retries/unrelated tools; next inbound run fresh | HTTP call sequence/run IDs | Pure local | P-REM-C | Run lifecycle controlled |
| REM-11 | КС | ЛОК-К | Run A in-flight; same session run B starts; late A fail/end | Execute tools | A cannot close/delete B; ended A fails closed; B works until own end | call trace/state map | Pure local | P-REM-D | Controlled lifecycle |
| REM-12 | −С | Telegram/API-ИЗО | Callback clicked twice/concurrently | Duplicate update | Domain action once; SDK dispatcher dedupe committed even if UI ack fails | callback calls/task version/audit1 | Pending R12 | P-REM-E | One callback token |
| REM-13 | − | Telegram/API-ИЗО | Wrong owner/chat, malformed/expired token | Click/dispatch | Fail closed; buttons/state not falsely successful | Action API audit/task unchanged | Pending variants | P-REM-F | Separate tokens |
| REM-14 | +С | ЛОК-К | Domain confirm success; editMessage fails | Handler | clearButtons best effort, one success reply; all UI failures still handled:true | mock call order/dispatcher dedupe | Pure local | P-REM-G | No external chat |
| REM-15 | −С | API-ИЗО | Pending with cadence/TTL | Do not click; run confirmation scheduler across boundaries | Cadence preserved, Russian Moscow expiry/buttons guidance; TTL terminal behavior exact; no codes/raw IDs | pending count/timestamps/copy | Pending R15 | P-REM-H | Virtual clock/local preferred |
| REM-16 | +С | API-ИЗО | Due reminder outside quiet hours | Materialize/claim/authorize/send/finalize | Exactly one delivery, lease ownership and provider message id recorded | delivery state/audit | Reminder R16 | P-REM-I | Fake Telegram provider preferred |
| REM-17 | +СГ | API-ИЗО | Due during 00:00–06:00, backlog > thresholds | Scheduler | Defer to digest; bounded batches/max5; overflow summary; no storm | deliveries/digest text length | Reminders R17 | P-REM-J | Virtual clock/isolated chat |
| REM-18 | −С | API-ИЗО | Policy disabled/version changed/429/400/403/network uncertain | Pre-send/finalize | Reauthorize immediately before send; retry_wait/dead_letter/uncertain correct; no unauthorized send | provider call count/delivery state | Reminder variants | P-REM-K | No real external recipient |

## O. Миграции, очереди, развёртывание и очистка

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| OPS-01 | +С | ЛОК-К | Fresh PostgreSQL | Apply all Gateway/TaskCore/N8N migrations from zero | Schema reaches expected version without manual patch; functions/ACL exact | migration history + metadata | Disposable DB | P-OPS-A | Independent local DB |
| OPS-02 | +С | ЛОК-К | Migrated DB | Ordered reapply/idempotent bootstrap where supported | No drift/data corruption; expected guarded errors only | schema hash/tests | Disposable DB | P-OPS-A | После OPS-01 |
| OPS-03 | − | ЛОК-К/API-ЧТ | Functions SECURITY DEFINER | Inspect owner/search_path/ACL/PUBLIC | Owner and fixed search_path correct; PUBLIC revoked; only runtime roles execute | catalog query | Read-only | P-OPS-B | DB metadata shared read-only |
| OPS-04 | + | API-ЧТ | Deployed services | Health/readiness and restart count | Required services healthy/restart0; migrations current | container/status endpoints | Read-only | P-OPS-C | Shared production read-only |
| OPS-05 | + | API-ЧТ | OpenClaw+relay deployed | Run binding assertion | Relay NetworkMode targets current OpenClaw container; both healthy | verify-rollout-binding output | Read-only | P-OPS-C | После any OpenClaw recreate |
| OPS-06 | −С | ЛОК-К | Relay lease/outbox | Expire lease/retry until max | Exactly bounded retries, then DLQ; no duplicate accept | rows/attempts/state | Disposable DB | P-OPS-D | Dedicated run |
| OPS-07 | +С | API-ИЗО | Queued run; relay temporarily unavailable then restored | Restore relay without resubmit | Existing outbox claimed once; run terminal once | outbox/dispatch/run | Workspace O7 | P-OPS-E | Controlled service window; separate authorization required for prod restart |
| OPS-08 | + | API-ЧТ | TaskCore needs FCM OAuth/DNS | Resolve/reach provider unauthenticated | DNS/TLS egress works; network remains external as designed | container DNS/HTTPS result | Read-only | P-OPS-F | No token/send |
| OPS-09 | +С | API-ИЗО | Completed fixture group | Guarded exact cleanup using ledger | Only listed objects deleted; protected baselines unchanged; residual0 | before/after counts + ledger hash | Per-group prefix | P-CLEANUP | Sole cleanup writer per workspace |
| OPS-10 | − | ЛОК-К | Evidence bundle | Secret-pattern scan, diff-check, artifact hashes | No token/key/chat numeric ID/human content leakage; hashes bind tested artifact | scans/hashes | Local files | P-EVIDENCE | После group execution |

## P. Сквозные пользовательские сценарии

| ID | Класс | Среда | Предусловия | Шаги | Ожидаемый результат | Oracle / evidence | Изоляция | Параллельная группа | Зависимости / ресурс |
|---|---|---|---|---|---|---|---|---|---|
| E2E-01 | +С | ЭМУ-UI/API-ИЗО | Fresh owner invite | Onboard→PIN→create offline→restart→sync→edit→done→result | Один жизненный цикл задачи без потери/дубля; UI/API/audit согласованы | Screenshots + Room/outbox/API ledger | Workspace E1/device1 | P-E2E-A | Монопольно AVD/device/task |
| E2E-02 | +С | ЭМУ-UI/API-ИЗО | Owner/member devices | Owner task→approval→assign→member accept→sync→doc branch→complete | ACL появляется только после accept и только в границах; terminal consistent | Two client caches/API/change/audit | Workspace E2/devices2 | P-E2E-B | Два AVD, orchestrated barriers |
| E2E-03 | +С | ЭМУ-UI/API-ИЗО | Agent available | Voice/text→run→proposal→human accept→task appears→calendar | Human gate respected; one task/run/proposal | UI/API/audit | Workspace E3 | P-E2E-C | Provider budget; voice availability gate |
| E2E-04 | +С | ЭМУ-UI/API-ИЗО | FCM-capable AVD | Background event→generic notification→unlock/deep link→authoritative refresh | No content in push; exact entity appears once | raw push/UI/API/cache | Workspace E4/device | P-E2E-D | Real FCM availability or local envelope variant |
| E2E-05 | −С | ЭМУ-UI/API-ИЗО | Two AVD same task v1 | Both edit; A sync v2; B sync conflict→compare→intent-only retry | No silent overwrite; B draft preserved; final v3 merges selected fields only | two Room DBs/API/audit versions | Workspace E5/devices2 | P-E2E-E | Shared task; strict barriers |
| E2E-06 | −С | ЭМУ-UI/API-ИЗО | Cached session/data | Revoke refresh family server-side; process restart/sync | Local session and protected cache wiped/locked per security policy; no stale content exposure | auth state/files/Room/API401 | Workspace E6/device | P-E2E-F | Destructive only fixture device |

## План параллельного исполнения после объединения трёх каталогов

1. **Волна контрактов без общего состояния:** `P-BUILD`, `P-NET-B/F/K`, локальные `P-SYNC-I/L/O`, `P-PRT-B/C/G/H`, `P-REM-B/C/D/G`, `P-OPS-A/D`. Их можно делить между workers и запускать одновременно.
2. **Волна независимых production fixtures:** AUTH, TASK, DOC, ACL, AGENT, PUSH и decisions получают отдельные workspace/principal/device/client/cursor и `fixture_key`. Один cleanup writer назначается на workspace; параллельные таблицы допустимы только при разных workspaces.
3. **Волна AVD:** разные snapshot AVD для auth/biometry, offline/conflict, UI/accessibility и FCM. Внутри одного AVD lifecycle, clipboard, permission, Room/outbox и UI navigation выполняются последовательно.
4. **Сквозные сценарии:** E2E запускаются последними на новых fixtures после прохода их зависимостей. Не переиспользовать Telegram chat pending action, conversation, focus principal или task version между параллельными кейсами.
5. **Очистка и evidence:** после каждой изолированной группы точечная очистка и baseline proof; общая документация обновляется один раз после дедупликации результатов.

## Доступность среды и честные остатки

- **Доступно в принципе на эмуляторе:** UI, process death/reboot, сеть, Android biometric success/cancel при enrolled fingerprint, permission flows и реальная FCM-доставка на AVD с Google Play services. Доступность именно выбранного образа проверяется до прогона; отсутствие capability — blocker среды, а не PASS/FAIL продукта.
- **Требует production backend, но не физического телефона:** ACL, idempotency, optimistic concurrency, decision races, service HMAC, outbox/DLQ, migrations, FCM publisher с изолированным token/device, agent/reminder state machines.
- **Не закрывается детерминированно одним AVD:** реальный микрофон и конкретный OEM speech provider, аппаратная биометрия/OEM keyguard, OEM background restrictions и доставка FCM на конкретную модель/прошивку. Эти проверки остаются отдельной физической воротой после завершения emulator/backend этапа.
- **Внешние сообщения:** Telegram/реальная FCM delivery выполняются только в заранее разрешённый тестовый recipient/device с лимитом и cleanup. Большинство ошибок scheduler/provider закрываются fake-provider/contract fixtures без внешней отправки.
- **Текущий известный WIP:** конфликтный Android UI/rebase существует в незавершённом рабочем состоянии. Каталог фиксирует требуемое итоговое поведение, но этот черновик не считает его исправленным и ничего в WIP не изменяет.

## Критерий завершения будущего прогона

Каждый применимый ID получает `PASS` с указанным oracle либо `BLOCKED/NOT RUN` с точной причиной и влиянием. `PASS` требует совпадения UI и авторитетного источника (API/Room/БД/audit/outbox), когда кейс stateful. Для конкурентных кейсов требуются точные side-effect counts. Для fixture-групп обязательны residual0 и сохранность baseline. Этап готов к физическому телефону только после нуля открытых дефектов во всех согласованных и доступных emulator/backend кейсах; аппаратные остатки перечисляются отдельно и не маскируются локальными тестами.
