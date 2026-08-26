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
доказательства:
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
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
