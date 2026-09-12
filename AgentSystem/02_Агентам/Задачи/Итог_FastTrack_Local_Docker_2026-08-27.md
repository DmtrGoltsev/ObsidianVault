---
id: "n8nagents-fasttrack-local-docker-final-2026-08-27"
тип: "задача"
статус: "выполнено"
проект: "AgentSystem"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники:
  - "[[План_N8NAgents_Local_Docker_FastTrack_v1]]"
  - "[[Журнал_Исполнения_FastTrack_2026-08-27]]"
  - "C:/Users/style/Documents/ChatGPT/Агенты/N8NAgents/local/README.md"
доказательства:
  - "[[Журнал_Исполнения_FastTrack_2026-08-27]]"
теги: ["n8n", "docker-desktop", "windows", "telegram", "local-lab", "handover"]
---

# Итог Fast Track — локальная лаборатория N8NAgents

## Результат

Fast Track завершён с итоговым независимым `FINAL_QA_PASS`, блокеров нет.

- `LOCAL_CORE_READY=PASS` — PostgreSQL и n8n работают локально, данные пережили полный `down`/`up` без удаления volumes.
- `TELEGRAM_LOCAL_READY=PASS` — mock-контур прошёл проверки, а отдельный dev/test bot выполнил один разрешённый реальный E2E через локальный n8n.
- Финальное безопасное состояние Telegram — `DISARMED`: real bridge остановлен и удалён, token не смонтирован, активных Telegram egress endpoints нет.
- VPS, provider UI, DNS, DeepSeek и production-инфраструктура не затрагивались.

Полные sanitized доказательства и исправления: [[Журнал_Исполнения_FastTrack_2026-08-27]].

## Фактическая архитектура

Лаборатория работает на Windows через Docker Desktop с управляемым WSL 2 backend (`desktop-linux`, Linux/amd64). Проверены Docker Desktop 4.88.1, Docker Engine 29.7.2 и Docker Compose 5.4.0.

Основной контур:

- `postgres` — PostgreSQL 17.11, без host-порта;
- `n8n` — n8n 2.36.7 во внутренних Docker-сетях;
- `n8n-loopback` — единственная публикация `127.0.0.1:5678`;
- `telegram-mock`, `workflow-mock`, `telegram-bridge-mock` — постоянный безопасный mock-контур;
- `telegram-bridge-real` — отдельный profile, запускаемый только явным owner gate;
- одноразовые init/test services подготавливают права volumes и выполняют mock tests без публикации портов.

Постоянные named volumes хранят PostgreSQL, n8n data, n8n files и состояния мостов. Docker API/socket в сервисы не монтируется. Существующая Windows-служба PostgreSQL не менялась.

Адрес n8n: [http://127.0.0.1:5678](http://127.0.0.1:5678).

## Команды владельца

Открыть PowerShell в корне проекта `C:\Users\style\Documents\ChatGPT\Агенты\N8NAgents`.

```powershell
./local/n8nagents-local.ps1 preflight
./local/n8nagents-local.ps1 start
./local/n8nagents-local.ps1 status
./local/n8nagents-local.ps1 mock-test
./local/n8nagents-local.ps1 stop
```

`start` поднимает только core и mock. `stop` выполняет Compose `down` без `-v`, поэтому named volumes сохраняются. Нельзя использовать `docker compose down --volumes`, если отдельно не принято решение удалить данные.

Реальный dev/test Telegram включается только вручную:

```powershell
./local/n8nagents-local.ps1 arm-real -AllowRealTelegram
./local/n8nagents-local.ps1 start-real -AllowRealTelegram
./local/n8nagents-local.ps1 disarm-real
```

После теста выполнен `disarm-real`; повторный запуск сейчас не требуется. Persistent send cap — 20 сообщений, а 21-е блокируется.

Полный owner runbook: [local/README.md](file:///C:/Users/style/Documents/ChatGPT/%D0%90%D0%B3%D0%B5%D0%BD%D1%82%D1%8B/N8NAgents/local/README.md).

## Секреты

Локальные secret leaves находятся только в ignored-каталоге:

`C:\Users\style\Documents\ChatGPT\Агенты\N8NAgents\local\secrets\`

Там хранятся локальные DB credentials, n8n encryption key, dev/test Telegram token, allowlists и arm marker. Значения не записаны в Git, Vault, Compose render, Docker logs или evidence. Каталог защищён локальными NTFS ACL. Токен и allowlist нельзя передавать через аргументы команд, чат или Obsidian.

## Backup и восстановление

Проверенные логические PostgreSQL backup находятся в ignored-каталоге:

`C:\Users\style\Documents\ChatGPT\Агенты\N8NAgents\local\evidence\backups\`

Проверенная процедура:

1. Создать custom-format dumps через `pg_dump` той же версии с `--no-owner --no-acl`, не выводя credentials.
2. Проверить читаемость архивов командой `pg_restore --list` и сохранить контрольные суммы несекретных backup-файлов отдельно.
3. Восстанавливать сначала только в disposable PostgreSQL container с `network=none`, `PGDATA` на tmpfs и без persistent volumes.
4. Выполнить проверки таблиц и синтетического marker; основной stack и его volumes во время smoke не изменять.
5. Удалить только точно идентифицированный disposable verifier; затем проверить health основного контура.

Эта процедура успешно прошла `BACKUP_RESTORE_PASS`. Она не является production DR: backup остаётся на том же компьютере, off-host retention и автоматизация не настроены. Отдельный backup файлового volume n8n не входит в сохранённый E6-набор и остаётся задачей следующей фазы.

## Остаточные ограничения

- Это локальная лаборатория, не production и не готовность VPS.
- Docker Desktop не обеспечивает доказанную жёсткую egress-фильтрацию; real Telegram остаётся выключенным вне явного теста.
- Public webhook, Caddy/TLS, production bot, monitoring и production backup retention отсутствуют.
- DeepSeek не подключался, расходов и LLM-трафика не было.
- Удаление volumes, Docker Desktop/WSL data или ротация секретов остаются отдельными owner gates.
- Исходные изменения проекта вне `local/` сохранены без drift; этот Fast Track их не интегрировал и не коммитил.

## Связанные материалы

- [[План_N8NAgents_Local_Docker_FastTrack_v1]]
- [[Журнал_Исполнения_FastTrack_2026-08-27]]
- [[N8NAgents]]
- [[MOC_N8NAgents]]
