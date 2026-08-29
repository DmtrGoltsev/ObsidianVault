---
id: "evidence-n8nagents-a2-readonly-discovery-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Доказательство_T1_Local_SSH_Preflight_N8NAgents]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "Git N8NAgents docs/server-discovery.md @ 09824a6e16e479d2283ddbd4fb5125a50bda5113; tree 5eb0df96c8ab908ba45cdd18c8286ce683528135"
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
source_path: "docs/server-discovery.md"
source_base: "09824a6e16e479d2283ddbd4fb5125a50bda5113"
source_tree: "5eb0df96c8ab908ba45cdd18c8286ce683528135"
imported_date: "2026-08-29"
проверка_редакции: "PASS — infrastructure addresses redacted; no secret/PII values"
теги: ["n8n", "ssh", "vps", "discovery", "read-only", "a2"]
---

# A2 — read-only discovery VPS после перезагрузки

## Итог

**PASS.** После перезагрузки VPS закреплённая минимальная SSH-проверка прошла, затем полный ограниченный read-only discovery завершился с exit code `0`, без stderr и без удалённых mutations. Это закрывает прежний `BLOCKED-EXTERNAL` для SSH session channel, но не разрешает server mutations.

## Подтверждённые факты VPS

| Область | Результат |
|---|---|
| ОС и ядро | Ubuntu 26.04 LTS, kernel `7.0.0-30` |
| Ресурсы | 2 vCPU; 1.6 GiB RAM, из них около 1.4 GiB available; swap отсутствует |
| Диск | root filesystem 39 GiB, около 34 GiB свободно |
| Время | UTC; NTP синхронизирован |
| Сеть | Есть публичная IPv4- и IPv6-связность; адреса намеренно не сохраняются |
| Listeners | Только SSH на `22/tcp` извне; локальные DNS и chrony на loopback |
| Порты для стека | `80`, `443`, `5678` и `5432` свободны |
| Существующий стек | Docker, Compose, Caddy, nginx, Apache, PostgreSQL, n8n и Redis отсутствуют; релевантные systemd units отсутствуют |
| Каталоги/скрипты | В `/opt` и `/srv` кандидатных директорий нет; `deploy-n8n` отсутствует |
| Firewall | UFW, nftables и iptables отсутствуют; provider firewall не подтверждён |
| Внешние зависимости | DNS resolution и исходящий HTTPS прошли |

## Границы проверки

- Выполнялись только read-only команды discovery.
- SSH minimal test и полный discovery завершились clean: exit `0`, stderr отсутствует.
- Пакеты, файлы, сервисы, firewall, users, SSH-configuration, containers, volumes и сети не изменялись.
- Секреты и публичные IP-адреса не записывались.

## Риски и следующий gate

- Для пилота ресурс достаточен только с ограничениями: RAM ниже предпочтительных 4 GiB и swap отсутствует.
- До exact deployment plan нужно определить firewall policy, включая IPv6, и подтвердить provider firewall.
- Server mutation ещё **не начата**. Следующий gate: review точного deployment plan с командами/объектами, архитектурой, downtime и rollback; отдельное одобрение перед применением.

## Связанные заметки

- [[Задача_Развертывание_N8NAgents]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[MOC_N8NAgents]]


## Импортированный source discovery record

> [!note] Source provenance
> Полный source discovery record сохранён ниже как historical provenance snapshot `09824a6e...`; он не описывает current production после rollout.

Status: `PASS` after reboot. This is redacted read-only evidence supplied on 2026-08-26; it authorizes no deployment claim by itself.

| Area | Discovered fact | Phase A consequence |
|---|---|---|
| OS/kernel | Ubuntu 26.04; kernel 7.0 | Verify `ID=ubuntu`, codename and architecture again before adding the official Docker repository. |
| Compute | 2 vCPU; 1.6 GiB RAM, about 1.4 GiB available; no swap | Internal pilot only. Add a reviewed 2 GiB swapfile and bootstrap-only container limits before first start; stop on memory pressure or health failure. |
| Storage | 39 GiB total; about 34 GiB free | Enough for the pilot, not a capacity guarantee. Require at least 25 GiB free before package/image changes. |
| Time/network | UTC, NTP synchronized; outbound DNS and HTTPS pass | Keep UTC. Recheck synchronization and registry HTTPS immediately before pulls. |
| Inbound | Public IPv4 and IPv6; only port 22 listening | Caddy remains disabled. n8n may bind only `127.0.0.1:5678` through the bootstrap override. |
| Free ports | 80, 443, 5678 and 5432 free | Recheck immediately before start. Free does not mean approved for exposure. |
| Installed stack | Docker, Compose, Caddy, PostgreSQL, n8n and Redis absent | Fresh official Docker repository/install path; stop if unexpected packages/services appear. Redis is not part of Phase A. |
| Filtering | No local firewall tools; provider firewall and IPv6 policy unknown | Internal Phase A adds no public listener: Caddy is default-off and bootstrap n8n binds only `127.0.0.1:5678`. Defer these policies without weakening them; both are mandatory before `public-edge`. |
| Filesystem/users | `/opt` and `/srv` empty; `deploy-n8n` absent | Create only the versioned stack paths and dedicated login documented in the manifest. |

Still unknown and therefore a Phase A preflight gate: exact `amd64`/`x86_64` platform, provider-console recovery test, official Docker repository support/candidates for this Ubuntu release, image digests for the target platform, and the user's choice between plaintext 2 GiB swap risk and a no-swap/OOM-risk pilot. Provider firewall and IPv6 policy are explicitly deferred for this loopback-only phase, but become mandatory gates before `public-edge` enablement. The SSH host identity remains user-accepted/pinned TOFU, not independently verified. No secret, domain, DNS, owner account, container, volume or deployment was created during A2.
