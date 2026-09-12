---
id: "task-n8nagents-local-docker-fasttrack-v1"
тип: "задача"
статус: "выполнено"
проект: "AgentSystem"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[N8NAgents]]"
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Пакет_N8NAgents_Стартовый]]"
доказательства:
  - "[[Журнал_Исполнения_FastTrack_2026-08-27]]"
  - "[[Итог_FastTrack_Local_Docker_2026-08-27]]"
теги: ["n8n", "docker-desktop", "windows", "fast-track", "telegram", "local-lab"]
---

# N8NAgents — локальная лаборатория Docker Desktop, Fast Track v1

> [!success] Выполнено 2026-08-27
> `LOCAL_CORE_READY=PASS`, `TELEGRAM_LOCAL_READY=PASS`, `BACKUP_RESTORE_PASS`, `FINAL_QA_PASS`; финальный real Telegram state — `DISARMED`. Итог и handover: [[Итог_FastTrack_Local_Docker_2026-08-27]]. Полные доказательства: [[Журнал_Исполнения_FastTrack_2026-08-27]].

## 1. Решение и измеримый результат

План создаёт постоянную локальную лабораторию N8NAgents на Windows через Docker Desktop. Владелец и агент смогут одинаково запускать, останавливать и проверять её стандартными командами проекта.

После исполнения должны быть доступны:

- PostgreSQL и n8n Community в Docker Compose;
- отдельный Telegram bridge, который владеет Telegram transport и передаёт в n8n только нормализованные разрешённые события;
- локальный Telegram mock для тестов без реальной сети и токена;
- n8n editor только на loopback-адресе Windows;
- реальный тест отдельного dev/test Telegram bot в режиме polling, только для allowlisted пользователя/чата и максимум с 20 исходящими тестовыми сообщениями за один разрешённый прогон;
- сохранение данных после остановки и повторного запуска стека;
- минимальный backup и изолированный restore smoke на синтетических данных;
- понятные ручные команды и журнал результатов в Obsidian.

Fast Track не означает готовность production. На этом этапе не создаются публичные webhook, Caddy/TLS, production bot, DeepSeek-интеграция, полноценные tools/reminders, monitoring production и deployment на VPS.

## 2. Жёсткие границы Plan A

Разрешён только **Plan A: Docker Desktop на текущем Windows-компьютере**.

Допустимо, что Docker Desktop использует собственный управляемый WSL 2 backend, если это соответствует проверенным на дату исполнения официальным требованиям. Это часть Docker Desktop, а не отдельная пользовательская Ubuntu-среда и не ранее обсуждавшийся Plan B.

Вне scope и запрещено:

- отдельная Ubuntu/другой Linux-дистрибутив в WSL как среда проекта;
- Hyper-V VM, QEMU/v86, отдельная физическая Linux-машина или cloud runner как замена Plan A;
- любые подключения, команды, файлы, контейнеры или изменения на VPS;
- provider UI, DNS, firewall сервера, SSH и production domains;
- DeepSeek-трафик и DeepSeek API key — интеграция явно отложена;
- production Telegram bot/token и новые получатели;
- сохранение секретов, raw chat/user IDs или приватных данных в Git, Vault, логах, screenshots и evidence;
- удаление существующих Docker/WSL данных без отдельного решения владельца.

Если Docker Desktop невозможно безопасно запустить в этих границах, результат этапа — `BLOCKED_PLAN_A`, а не автоматический переход на Plan B.

## 3. Упрощение процесса

Предыдущая цепочка v2/R2/R3, расширенные finding-catalogs, mutation-canaries, frozen bundle custody и повторяющиеся prefreeze-аудиты получают статус:

`REJECTED_ARCHIVE_NOT_PREREQUISITE`

Эти материалы остаются историческим архивом, но не являются входным условием установки, реализации или проверки Fast Track. Их нельзя использовать для задержки исполнения этого плана.

Для текущего решения применяется короткий контур:

1. Один самодостаточный план — этот файл.
2. Пять независимых критических ревью без создания новой многоуровневой audit-машины.
3. Одна сводка: общие замечания, одиночные критические замечания, принятые и отклонённые корректировки.
4. Не более одной правки плана перед решением владельца.
5. Отдельное явное разрешение владельца на установку и изменения Windows.
6. Исполнение тонкими проверяемыми этапами до `LOCAL_LAB_READY` либо до конкретного STOP.

Для принятия плана достаточно отсутствия доказанного P0/STOP и согласия не менее 4 из 5 reviewers. Одиночное замечание блокирует только при конкретном сценарии потери данных, утечки секрета, несанкционированного внешнего действия или необратимого изменения. Повторный полный круг ревью не запускается без новой существенной архитектуры.

## 4. Факты и обязательный read-only preflight

### Известно из текущего проектного контекста

- Хост — Windows, проект читается с локальной файловой системы.
- Владелец выбрал Docker Desktop Plan A и отклонил Plan B.
- Локальный n8n и реальный dev/test Telegram bot должны запускаться как агентом, так и владельцем вручную.
- VPS не участвует в этой работе.
- Текущий цикл не даёт разрешения на установку, скачивание, запуск Docker, ввод секретов или изменение Windows: это наступает только после отдельного approval владельца.

Ранее зафиксированное отсутствие Docker runtime считается историческим снимком, а не текущим фактом. Перед действиями состояние проверяется заново.

### Неизвестно до preflight

- редакция, build и архитектура Windows;
- включена ли аппаратная виртуализация;
- состояние WSL и Virtual Machine Platform;
- установлен ли Docker Desktop, есть ли его существующие images, containers, volumes и данные;
- соответствие условиям лицензии Docker Desktop;
- свободные CPU, RAM и место на системном диске и диске данных Docker;
- ограничения App Control, антивируса, корпоративной политики и локального firewall;
- наличие прав администратора, UAC и необходимость reboot;
- свободен ли `127.0.0.1:5678`;
- могут ли выбранные текущие образы n8n и PostgreSQL работать на архитектуре хоста;
- поддерживаемый безопасный способ передачи file-based secrets в выбранные образы.

### Preflight без изменений

До скачивания и установки исполнитель собирает sanitized evidence:

1. Windows edition/build/architecture и состояние pending reboot.
2. Hardware virtualization и необходимые Windows features.
3. Наличие Docker Desktop/Engine/Compose и состояние существующих данных без чтения секретов.
4. CPU, RAM, свободное место и предполагаемый лимит ресурсов Docker.
5. Занятость loopback-порта 5678.
6. Политику лицензии для фактического типа использования.
7. Возможные запреты security software и управляемого устройства.
8. Официальные на дату исполнения prerequisites и совместимость.

В плане намеренно нет неподтверждённых номеров версий, tags, digests и SHA-256. Они выбираются только по актуальным официальным источникам во время разрешённого исполнения, затем фиксируются в evidence. `latest` не используется.

## 5. Какие изменения Windows возможны

Установка Docker Desktop может затронуть Windows сильнее обычного приложения. До approval владелец должен увидеть фактический список, который показали preflight и installer.

Потенциально затрагиваются:

- установка Docker Desktop в системные каталоги и создание per-user данных;
- установка или запуск Docker Desktop service/helper;
- добавление пользователя в локальную группу доступа Docker, если это требуется выбранной конфигурацией;
- включение WSL и Virtual Machine Platform для управляемого WSL 2 backend;
- создание или обновление управляемого Docker backend и его виртуального диска;
- виртуальные сетевые адаптеры, NAT/DNS integration и локальные firewall rules;
- автозапуск Docker Desktop при входе пользователя — только если владелец отдельно выберет его;
- изменение места хранения и лимитов CPU/RAM/disk Docker Desktop;
- один или несколько reboot, если Windows потребует завершить feature/installer changes.

Не выполняются автоматически:

- изменение BIOS/UEFI;
- включение полного Hyper-V, если он не требуется подтверждённой конфигурацией;
- удаление/перерегистрация существующих WSL distributions;
- удаление существующих Docker images, containers, volumes или virtual disk;
- отключение защит Windows или антивируса;
- изменение глобального firewall сверх узко подтверждённого требования Docker Desktop.

Любой из этих пунктов переводит работу в manual gate.

## 6. Docker Desktop: установка, проверка и rollback

### 6.1 Входной gate

После read-only preflight исполнитель показывает одним пакетом:

- что уже установлено;
- какие Windows features требуется включить;
- потребуется ли UAC/reboot;
- ожидаемые каталоги и объём данных;
- условия лицензии;
- точный источник installer и способ проверки его подписи/checksum;
- rollback с сохранением чужих данных.

Только затем владелец даёт одно approval на весь обратимый install cycle.

### 6.2 Установка или использование существующей установки

1. Если совместимый Docker Desktop уже установлен, не переустанавливать его; сохранить read-only inventory и проверить Engine/Compose.
2. Если отсутствует — загрузить installer только с официального источника, проверить цифровую подпись и опубликованный integrity metadata, если он доступен.
3. Включить только минимальные официально необходимые компоненты WSL 2 backend.
4. Не создавать отдельный пользовательский Linux distribution.
5. После требуемого reboot убедиться, что Windows и Docker Desktop запустились без ошибок.
6. Выделить консервативные лимиты CPU/RAM/disk после измерения ресурсов; не истощать Windows host.
7. Не включать Kubernetes, публичный daemon socket, privileged remote API и лишние extensions.
8. Проверить `docker version`, `docker compose version`, тестовый local image run и отсутствие непредусмотренной публикации портов.

Версии и image digests фиксируются после проверки, а не предсказываются этим планом.

### 6.3 Rollback установки

Rollback выполняется по слоям и не удаляет неизвестные данные:

1. Остановить только Compose project N8NAgents без `--volumes`.
2. Экспортировать или сохранить созданные N8NAgents данные, если они уже нужны владельцу.
3. Удалить только созданные этим проектом containers, network и, после отдельного подтверждения, его named volumes.
4. Если Docker Desktop был установлен специально этим циклом — деинсталлировать штатным installer/uninstaller.
5. Удалять управляемые backend data только после отдельного подтверждения и проверки, что там нет чужих данных.
6. Windows features отключать только если preflight доказал, что они были включены этим циклом и не используются другим ПО; это отдельный manual gate и может требовать reboot.
7. Проверить, что существующие пользовательские WSL distributions и unrelated files не затронуты.

## 7. Планируемая локальная архитектура Compose

### 7.1 Сервисы

| Сервис | Назначение | Публикация на Windows |
|---|---|---|
| `postgres` | metadata n8n и локальные прикладные тестовые данные | нет |
| `n8n` | локальный editor и workflows | только `127.0.0.1:5678` |
| `telegram-bridge` | polling, allowlist, dedup, лимит отправок и transport к n8n | нет |
| `telegram-mock` | локальная имитация Telegram API для автоматических тестов | нет; только mock network |
| `test-runner` | повторяемые smoke/negative tests | нет; запускается по профилю |

### 7.2 Сети и границы

- `data-internal`: только n8n ↔ PostgreSQL, без публикации PostgreSQL на host.
- `app-internal`: n8n ↔ Telegram bridge.
- `mock-internal`: bridge в mock-режиме ↔ Telegram mock; сеть не получает реальный token.
- Реальный bridge получает исходящий HTTPS только на Telegram Bot API; отсутствие жёсткой egress-фильтрации Docker Desktop документируется как residual risk, а не как ложный PASS.
- n8n editor bind — строго `127.0.0.1`, не `0.0.0.0` и не LAN IP.
- Docker API/socket не монтируется ни в один сервис.
- PostgreSQL, bridge и mock не имеют host ports.
- Compose project name фиксируется, чтобы команды владельца всегда обращались к одной лаборатории.

### 7.3 Данные и жизненный цикл

- PostgreSQL и n8n используют отдельные named volumes.
- `compose down` по умолчанию не удаляет volumes.
- Images закрепляются проверенными tags и digests после compatibility smoke.
- Health checks и bounded startup dependencies не подменяют проверку готовности.
- `restart` policy выбирается для восстановления после перезапуска Docker Engine, но автозапуск Docker Desktop при входе остаётся выбором владельца.
- Resource limits задаются после preflight и проверяются под нагрузкой простого workflow.

## 8. Секреты и локальные ignored files

В Git добавляются только placeholders и документация. Реальные значения создаются владельцем локально после manual gate.

Планируемая модель:

- `.env.example` — только несекретные имена переменных и placeholders;
- `.env.local` — локальные несекретные настройки и ссылки на secret files, обязательно в `.gitignore`;
- `.local-secrets/` — token dev/test bot, n8n encryption key и локальные DB credentials как отдельные файлы, каталог обязательно в `.gitignore`;
- secret files монтируются read-only только в сервис, которому значение действительно нужно;
- Telegram token доступен bridge, но не n8n, PostgreSQL, mock или test-runner;
- `N8N_ENCRYPTION_KEY` постоянен для этой лаборатории и хранится отдельно от backup;
- raw `docker compose config`, environment, inspect и process arguments не попадают в evidence;
- скрипты не печатают секреты и не передают их через CLI arguments или shell history;
- перед первым commit и после тестов выполняется secret scan проекта и staged diff.

Конкретный file-based secret mechanism утверждается compatibility test выбранных images. Если образ требует env variable, разрешён минимальный container entrypoint, который читает mounted file внутри контейнера без печати значения. Если безопасный transport не подтверждён — STOP.

## 9. Этапы реализации

### E0 — Preflight и owner approval

Выполнить проверки раздела 4, показать изменения Windows и rollback. Выход: `READY_TO_INSTALL` или конкретный STOP. Никаких изменений до approval.

### E1 — Docker Desktop foundation

Установить или проверить Docker Desktop, WSL 2 backend, Engine и Compose. Выход: `DOCKER_READY`. Rollback — раздел 6.3.

### E2 — Файлы проекта

После проверки фактического состояния репозитория создать минимальный набор:

- Compose-файл и profiles `mock`/`real`;
- Dockerfile/код одного Telegram bridge с переключаемым provider endpoint;
- конфигурацию PostgreSQL и migrations;
- `.env.example`, `.gitignore` и ignored local secret layout;
- PowerShell-команды `preflight`, `up`, `down`, `status`, `test-mock`, `arm-real`, `disarm-real`, `backup`, `restore-smoke`;
- owner runbook без секретов.

Перед редактированием dirty working tree инвентаризируется. Никакие существующие изменения не stash/reset/clean/overwrite.

### E3 — Mock-first stack

1. Запустить PostgreSQL, n8n, тот же build Telegram bridge и mock provider.
2. Использовать только синтетические IDs/token/payload.
3. Проверить health, migration, доступ n8n на `127.0.0.1:5678` и отсутствие host-порта PostgreSQL.
4. Проверить allowed и unauthorized update, duplicate update, malformed payload, timeout, bridge restart и превышение send cap.
5. Доказать, что mock profile не может прочитать real token и не может переключиться на реальный endpoint.

Выход: `MOCK_PASS`. Любая реальная Telegram операция до этого запрещена.

### E4 — Реальный ограниченный Telegram test

Владелец вручную создаёт или выбирает отдельного dev/test bot и локально вводит token и numeric allowlist, не отправляя их в чат/Vault/Git.

Перед включением bridge:

1. Выполнить read-only `getMe` и `getWebhookInfo` через безопасный локальный механизм.
2. Если у bot уже есть webhook или неизвестное использование — STOP; не вызывать `deleteWebhook` без отдельного решения владельца.
3. Показать владельцу bot identity, allowlist status и нулевой счётчик разрешённого прогона без раскрытия token/IDs.
4. Получить manual arm на один тестовый прогон.

В реальном прогоне:

- только polling;
- только allowlisted test user/chat;
- неизвестные IDs отклоняются до n8n и не сохраняются;
- ответ всегда возвращается в исходный разрешённый chat, новый recipient невозможен;
- persistent ledger блокирует 21-е исходящее сообщение;
- retries учитываются в лимите безопасно, неоднозначный timeout не приводит к безусловной повторной отправке;
- сообщения не содержат DeepSeek-ответов: тестируется deterministic echo/health workflow;
- после теста bridge переводится в disarmed state и token не остаётся в логах/evidence.

Выход: `REAL_TELEGRAM_PASS` либо `REAL_TELEGRAM_BLOCKED`. Лимит `<=20` нельзя расширять без нового approval.

### E5 — Restart и persistence

На синтетических данных проверить:

1. Запись в PostgreSQL и сохранённый n8n workflow.
2. `compose stop`/`start`.
3. `compose down`/`up` без `--volumes`.
4. Перезапуск Docker Desktop.
5. Reboot Windows — только если владелец отдельно согласовал время и сохранение открытой работы.

После каждого шага должны сохраняться данные, workflow и encryption-key compatibility. Реальный Telegram bridge во время restart tests остаётся disarmed.

### E6 — Backup и restore smoke

Минимальный backup включает PostgreSQL dump, n8n persistent data/config, workflow exports и inventory без значений секретов. Если backup содержит чувствительные данные, он шифруется, а ключ не хранится рядом.

Restore smoke:

- отдельное Compose project name и отдельные volumes;
- только synthetic backup fixture;
- без real Telegram token, polling, schedules и внешнего API egress;
- другой loopback port либо вообще без host publication;
- проверка checksum, восстановления БД, запуска n8n и чтения тестовой записи;
- teardown только restore-smoke project после проверки exact ownership.

Выход: `RESTORE_SMOKE_PASS`. Ошибка restore не уничтожает source volumes и блокирует `LOCAL_LAB_READY`.

### E7 — Handover

Владелец по runbook самостоятельно выполняет `status`, `up`, `test-mock`, разрешённый `arm-real`, `disarm-real`, `backup` и `down`. Команды должны работать без знания внутренностей Docker и не раскрывать секреты.

## 10. Проверки готовности

`LOCAL_LAB_READY` ставится только если:

- Docker Desktop/Engine/Compose работают после install/restart;
- n8n доступен только на `127.0.0.1:5678`;
- PostgreSQL, bridge, mock и Docker API не опубликованы на host/LAN;
- mock tests проходят тем же bridge build, который используется в real profile;
- unauthorized Telegram identity не достигает n8n и DB;
- реальный dev/test bot прошёл allowlisted тест либо явно отмечен `BLOCKED_MANUAL` без ложного общего PASS;
- 21-е исходящее сообщение блокируется;
- данные переживают stop/start и down/up без удаления volumes;
- backup checksum и isolated restore smoke проходят;
- secret scan не находит секреты в Git/Vault/logs/evidence;
- владелец вручную повторил основные команды;
- Obsidian содержит sanitized журнал, evidence и residual risks.

Статусы этапов: `PASS`, `FAIL`, `BLOCKED_MANUAL`, `BLOCKED_EXTERNAL`. Approval не является `PASS`.

## 11. Obsidian и доказательства

После разрешённого исполнения обновляются или создаются:

- журнал локальной установки и Windows changes;
- evidence Docker foundation без account/device identifiers;
- evidence mock test;
- evidence реального Telegram теста только со счётчиками и masked identity;
- evidence restart/persistence;
- evidence backup/restore smoke;
- owner runbook и rollback;
- статус в [[N8NAgents]], [[MOC_N8NAgents]] и [[Пакет_N8NAgents_Стартовый]].

В evidence допустимы команды, exit codes, timestamps, service health, loopback listeners, hashes созданных несекретных артефактов и redacted test results. Запрещены tokens, passwords, encryption keys, raw IDs, message contents, raw environment/inspect и screenshots с чувствительными данными.

## 12. STOP и ручные gates

Немедленный STOP:

- требуется Plan B, VPS или иной неразрешённый runtime;
- preflight обнаружил существующие Docker/WSL данные, которые установка или rollback может повредить;
- официальный installer/signature/integrity не подтверждён;
- лицензия не подходит или неясна;
- недостаточно RAM/disk либо Docker destabilizes Windows;
- требуется изменение BIOS/UEFI, отключение security control или неизвестное firewall exception;
- host port опубликован не только на loopback либо PostgreSQL/Docker API доступен с host/LAN;
- секрет обнаружен в Git, Vault, logs, evidence или process arguments;
- mock profile имеет доступ к real token/endpoint;
- Telegram bot уже используется webhook/другой системой;
- unauthorized identity достигла n8n, DB или исходящей отправки;
- счётчик допускает более 20 сообщений;
- backup checksum или restore smoke не прошли;
- обнаружено destructive действие или scope expansion.

Обязательный manual gate:

- admin/UAC, включение Windows feature и reboot;
- подтверждение Docker Desktop license;
- изменение Docker Desktop startup/resources/data location;
- ввод/ротация/revoke любого секрета;
- выбор dev/test bot и allowlist;
- изменение webhook state и arm реального polling/send;
- Windows reboot для persistence test;
- удаление volumes, backup, backend data или uninstall;
- новый recipient, более 20 сообщений, расходы, DeepSeek или любое внешнее API кроме ограниченного Telegram test;
- любое обращение к VPS/provider/DNS.

## 13. Rollback по этапам

| Этап | Откат |
|---|---|
| Preflight | изменений нет |
| Docker foundation | штатный uninstall; feature rollback только после отдельной проверки зависимости и approval |
| Project files | отдельный commit/revert только созданных Fast Track файлов; чужие dirty changes не трогать |
| Compose mock/real | `down` без volumes; real bridge сначала disarm |
| Telegram test | stop/disarm bridge; revoke/rotate token владельцем при подозрении на утечку; webhook не менять автоматически |
| Persistence | вернуть previous Docker settings; volumes сохранить |
| Restore smoke | удалить только точно идентифицированные restore-smoke containers/network/volumes |

Любое удаление данных требует отдельного подтверждения exact targets.

## 14. Отложено после Fast Track

- DeepSeek compatibility spike, стоимость и реальные LLM-вызовы;
- production workflows, tools, reminders и memory isolation для нескольких пользователей;
- Caddy, HTTPS, public webhook и domains;
- production backup retention/off-host storage и monitoring;
- hardening и deployment на VPS.

Следующая фаза может начаться только после `LOCAL_LAB_READY`, отдельного плана и отдельного approval. Fast Track не наследует remote permissions.

## 15. Definition of Done этого плана

Этот документ готов к решению владельца, когда пять reviewers закончили один круг, оркестратор показал краткую кворум-сводку, а принятые изменения внесены не более чем одной ревизией. Исполнение готово, когда выполнены E0–E7 и подтверждены критерии раздела 10.

До отдельного approval этот файл разрешает только документирование и review. Он не разрешает скачивание, установку, изменение Windows, запуск Docker, редактирование project repo, ввод секретов, Telegram-трафик или действия на VPS.

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
