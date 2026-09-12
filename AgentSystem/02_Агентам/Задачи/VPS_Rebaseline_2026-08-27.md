# N8NAgents — свежий read-only rebaseline VPS

- Capture: `2026-08-27T21:18:41Z` — `2026-08-27T21:24:26Z`
- Локальная дата: 2026-08-28 MSK
- Target: `root@154.59.110.121:22`
- Режим: `READ_ONLY`, `BatchMode`, bounded timeout
- Итог доступа: `PASS`
- Итог production readiness: `NOT_READY`

## Границы доказательства

Снимок получен после успешной public-key аутентификации разблокированным локальным ключом. На VPS не выполнялись установка, запись, перезапуск, изменение служб, firewall, пользователей, Docker-объектов или файлов. Значения `.env`, credentials, tokens и private keys не читались. Для потенциально секретного `/opt/n8n-stack/shared/.env` получены только путь, тип, владелец, mode и размер.

Реальные production domains в документации ещё не определены, поэтому DNS-запросы не выполнялись. Provider firewall нельзя достоверно вывести из guest OS; его состояние остаётся неизвестным.

## Сводка состояния

| Область | Свежий факт |
|---|---|
| ОС | Ubuntu 26.04 LTS `resolute`, `amd64` / `x86_64` |
| Kernel / VM | `7.0.0-30-generic`, Xen HVM |
| Hostname | `n8n-agents` |
| Uptime / load | 1 день 15 часов; load `0.18 / 0.16 / 0.11` |
| CPU | 2 vCPU, Intel Xeon E5-2680 v4 |
| RAM | 1,692,721,152 bytes; около 1.3 GiB available |
| Swap | `/swapfile`, 2,147,479,552 bytes; 29,728,768 bytes used; priority `-1` |
| Root disk | ext4, 39 GiB; 9.2 GiB used, 28 GiB free, 25% |
| Pending reboot | `NO` |
| IPv4 | `154.59.110.121/24`, default via `154.59.110.1` |
| IPv6 | `2a01:48a0:4301:77::/64`, default route present |
| Docker | Engine/CLI `29.7.2`, containerd `2.3.3`, Compose `5.5.0`, context `default` |
| Runtime | containers `0`, volumes `0`, Compose projects `0` |
| Images | ровно 2 pinned amd64 images: n8n и PostgreSQL |
| Caddy / host n8n / host PostgreSQL | не установлены и не запущены |
| Project units/timers | отсутствуют |
| Public listeners | только SSH `0.0.0.0:22` и `[::]:22` |
| Clock | synchronized, Chrony active, stratum 3, leap status normal |

## Docker и образы

Службы `docker.service`, `docker.socket` и `containerd.service` активны; Docker включён при загрузке. Docker root: `/var/lib/docker`, driver `overlayfs`, cgroup v2/systemd, live restore выключен.

Имеющиеся образы:

1. `docker.n8n.io/n8nio/n8n:2.36.7`
   - platform: `linux/amd64`
   - digest/image ID: `sha256:14c4285bc3034dc5b51034aea393711d27053588e460722bce523453a626f23c`
2. `postgres:17.11-alpine3.24`
   - platform: `linux/amd64`
   - digest/image ID: `sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73`

Контейнеры, пользовательские networks, volumes и Compose projects отсутствуют. Есть только стандартные Docker networks `bridge`, `host`, `none`.

## Release custody на VPS

На сервере находятся два root-owned release-кандидата:

- `/opt/n8n-stack/releases/20260826T115345Z-f6e0c745ab889c11df1ab83ccf7957534be600cd`
- `/opt/n8n-stack/releases/20260826T133537Z-bae8c88f7a7d153ffc4a5ae28028045a0a27d319`

`/opt/n8n-stack/current` по-прежнему указывает на первый, `f6e0c745...`. Более поздний `bae8c88f...` существует, но не является current.

Архивы:

- `/srv/n8nagents-20260826T115345Z-f6e0c745ab889c11df1ab83ccf7957534be600cd.tar.gz` — SHA-256 `b8c9ecf1fa724dc96ed97c7eb17e7ba8326fea5d70b46828b644e11ade97d65c`
- `/srv/n8nagents-20260826T133537Z-bae8c88f7a7d153ffc4a5ae28028045a0a27d319.tar.gz` — SHA-256 `929eb015e7a6f825b48ec2262ff43f5bef9d8b94effcd02c37a6b1995554d89c`

Пути `/opt/n8n-stack`, `current`, releases, shared и архивы принадлежат `root:root`. Секретный файл существует только как metadata evidence:

`/opt/n8n-stack/shared/.env` — regular file, `root:root`, mode `0600`, 850 bytes; содержимое не читалось.

## Пользователи

- `root`: login shell `/bin/bash`.
- `deploy-n8n`: uid/gid `1000`, home `/home/deploy-n8n`, shell `/bin/bash`.
- Группы `sudo` и `docker` не содержат пользователей.
- Отдельные host users `n8n` и `caddy` отсутствуют.

## SSH и host identity

Эффективная конфигурация sshd:

- `port 22`, listen `0.0.0.0:22` и `[::]:22`;
- `PermitRootLogin yes`;
- `PasswordAuthentication yes`;
- `PubkeyAuthentication yes`;
- `KbdInteractiveAuthentication no`;
- `MaxAuthTries 6`, `MaxSessions 10`;
- `X11Forwarding yes`;
- `AllowTcpForwarding yes`;
- `PermitOpen any`, `PermitListen any`.

Public host-key fingerprints, вычисленные из server-side `.pub` файлов:

- ED25519: `SHA256:Cms9Q+QMlrtK2pn566N3NF0MyAbIGTQYioaVM2MOJ9U`
- ECDSA: `SHA256:LpGWjbP4stIt1ABl+bSKIA6s6z8KLNWjtL9J1pxsaJw`
- RSA: `SHA256:9PXHV0j4zlwfHCrF51eaEKukseuFgPKfRSu4dzBK8gU`

Журнал текущей загрузки показывает регулярное внешнее сканирование SSH, включая серии исчерпания `MaxAuthTries` для `root` и несуществующих пользователей. IP атакующих в эту заметку не переносились.

## Firewall и экспозиция

- `ufw` отсутствует.
- `fail2ban` отсутствует.
- Host `iptables/nftables` имеет `INPUT ACCEPT` для IPv4 и IPv6.
- Docker создал стандартные forwarding/NAT chains; опубликованных container ports нет.
- Единственный внешний guest listener сейчас — SSH/22, но он открыт одновременно по IPv4 и IPv6.
- Provider-side firewall и recovery-console availability этим guest-снимком не подтверждаются.

Текущее отсутствие app listeners уменьшает немедленную поверхность атаки, но не заменяет firewall/hardening gate перед production deployment.

## Службы, таймеры и наблюдаемость

Активны Docker/containerd и SSH. Caddy, n8n, PostgreSQL, fail2ban, N8NAgents units отсутствуют. Project backup/monitoring timers отсутствуют. Есть только стандартные OS timers (`apt`, `dpkg-db-backup`, `fstrim`, filesystem scrub, tmpfiles и др.).

В журнале были повторяющиеся ошибки NTS certificate verification от Chrony после старта системы. На момент свежей проверки проблема не проявляется как loss of synchronization: `System clock synchronized: yes`, reachability источников полная, offset около десятков микросекунд. Это операционный warning, а не текущий stop blocker; после deployment нужен monitoring повторения.

## Сравнение с прежним baseline

Подтверждено без ухудшения:

- Ubuntu 26.04 amd64, 2 vCPU и около 1.6 GiB RAM;
- Docker `29.7.2`, Compose `5.5.0`;
- оба pinned production images присутствуют;
- app containers, volumes и public app listeners отсутствуют;
- `current` всё ещё указывает на `f6e0c745...`;
- более поздний `bae8c88f...` остаётся non-current;
- Caddy/public edge не установлен.

Изменение относительно раннего A2 discovery:

- ранее swap отсутствовал; теперь plaintext `/swapfile` 2 GiB создан, активен и используется примерно на 28 MiB.

Исторические H4/H6 STOP-состояния не превращены в PASS: наличие release-файлов и образов не является выполненным deployment.

## Production readiness и блокеры

### Что готово как инфраструктурная основа

- SSH-доступ и server identity доступны.
- Архитектура amd64 подтверждена.
- Ресурсный baseline и plaintext swap подтверждены.
- Docker/Compose работают.
- Нужные pinned amd64 images уже локальны на VPS.
- Release-кандидаты и защищённый server-side `.env` существуют.
- Pending reboot отсутствует, текущее время синхронизировано.

### Что блокирует production-ready

1. **Приложение не развернуто:** контейнеров, volumes, n8n/PostgreSQL runtime, project units и health evidence нет.
2. **Нужен новый exact production candidate:** current — старый `f6e0c745...`; non-current `bae8c88f...` связан с историческим wrapper/packaging STOP и не должен молча активироваться.
3. **SSH hardening отсутствует:** root login и password auth разрешены, X11/TCP forwarding открыты, rate protection/fail2ban нет; Интернет уже активно сканирует порт.
4. **Host/provider firewall gate не закрыт:** guest INPUT policy — ACCEPT по IPv4/IPv6, provider rules неизвестны.
5. **Public edge отсутствует:** нет Caddy, TLS, реальных domains/DNS/ACME, webhook и внешних negative-route tests.
6. **Backup/monitoring/alerting отсутствуют:** нет project timers, off-host encrypted backup и recovery evidence.
7. **Ресурсы тесные:** 1.6 GiB RAM; production compose должен пройти admission с жёсткими limits и контролем swap/OOM.
8. **Secrets/owner gates не доказаны:** существование `.env` с mode `0600` не доказывает корректность значений; owner/2FA/production credentials не проверялись.

## Безопасное следующее действие

1. Сформировать и независимо проверить один exact committed production candidate, исправляющий исторический wrapper/packaging STOP.
2. Отдельным mutation gate развернуть только внутренний PostgreSQL+n8n без public edge, с resource limits, health, roles/grants, persistence и rollback evidence.
3. Отдельным security gate выполнить SSH/firewall hardening с подтверждённой аварийной console и вторым deploy login, не блокируя себе доступ.
4. После internal core — owner/2FA, backup/restore и monitoring.
5. Только после ручных domains/DNS/provider inputs включать Caddy/TLS/Telegram webhook и выполнять внешние IPv4/IPv6 tests.

## Вердикт

`VPS_BASELINE_READY=PASS`

`PRODUCTION_RUNTIME_READY=FAIL_NOT_DEPLOYED`

`PUBLIC_EDGE_READY=FAIL_NOT_CONFIGURED`

Никакие production изменения в ходе этой проверки не выполнялись.

## Predeploy drift-check 2026-08-28T04:26:48Z

Повторный короткий read-only snapshot выполнен перед возможным internal rollout и сопоставлен с evidence SHA-256 `d069ed94edc1a187e25571a84af852175cb8160fdf237fb4544165b471142152`.

Результат: `NO_MATERIAL_DRIFT`.

- boot ID не изменился: `d3103d69-185f-41c6-8660-2294cb9a6267`;
- Docker/Compose остались `29.7.2` / `5.5.0`;
- containers `0`, volumes `0`, Compose projects `0`, images `2`;
- оба image digests и platform `linux/amd64` совпали;
- `current`, оба release-каталога, `.env` metadata и SHA-256 обоих `/srv` archives совпали;
- `.env`: `root:root`, mode `0600`, 850 bytes; значение не читалось;
- RAM, swap и disk не имеют существенного дрейфа: available RAM около 1.31 GiB, swap used около 28.6 MiB, root disk 25%;
- listeners не изменились: только SSH/22 публично по IPv4/IPv6 и локальные DNS/Chrony;
- `ufw`/`fail2ban` по-прежнему отсутствуют, INPUT policy по IPv4/IPv6 остаётся `ACCEPT`;
- root password status — `P` (password set); `PermitRootLogin yes`, `PasswordAuthentication yes`, `PubkeyAuthentication yes`;
- root и `deploy-n8n` имеют отдельные `authorized_keys` mode `0600`; содержимое ключей не читалось;
- pending reboot `NO`, NTP synchronized `yes`.

Provider console не может быть проверена guest-командами. Наличие ранее открывавшейся web/VNC console остаётся пользовательским утверждением, но непосредственно перед SSH/firewall mutation её требуется открыть и проверить вручную повторно.

### Exact non-destructive snapshot checklist для remote operator

Перед первой mutation выполнить и сохранить один связанный evidence record:

1. `date -Is`, hostname и `/proc/sys/kernel/random/boot_id`.
2. `free -b`, `swapon --show --bytes`, `df -B1 /`, `/proc/loadavg`, pending-reboot flag.
3. `docker version`, `docker compose version`, selected `docker info` counts.
4. Exact sets: `docker ps -a`, `docker volume ls`, `docker network ls`, `docker compose ls --all`.
5. Для двух ожидаемых images: tag, `linux/amd64`, image ID и RepoDigest; оба должны совпасть с этой заметкой.
6. `readlink` и `readlink -f` для `/opt/n8n-stack/current`; `stat` только metadata для stack/current/shared/.env; SHA-256 обоих `/srv` archives.
7. `ss -lntup`, INPUT policy IPv4/IPv6, UFW/fail2ban presence, безопасные effective sshd fields.
8. `passwd -S root` и metadata `authorized_keys` без чтения содержимого.
9. Отдельно вручную открыть provider web/VNC console и убедиться, что доступен login prompt; этот факт не выводить из SSH.
10. Зафиксировать expected rollback anchor: current=`f6e0c745...`, containers=`0`, volumes=`0`, public app ports=`0`. Ничего не удалять и не создавать на snapshot-шаге.

STOP до mutation при любом из условий:

- появились неизвестные containers, volumes, Compose projects или listeners;
- изменился current link, release/archive hash, image digest/platform или `.env` metadata;
- pending reboot стал `YES`, Docker unhealthy, disk/RAM admission не проходит exact candidate limits;
- provider console недоступна перед SSH/firewall изменением;
- нет отдельного проверенного rollback и exact candidate identity.
