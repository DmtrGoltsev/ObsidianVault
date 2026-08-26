---
id: "task-n8nagents-deployment-001"
тип: "задача"
статус: "активно"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Промпт_N8NAgents_v1_2026-08-25]]"
доказательства:
  - "[[Доказательство_T1_Local_SSH_Preflight_N8NAgents]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
  - "[[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]]"
  - "[[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]]"
  - "[[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]]"
теги: ["n8n", "развертывание", "ssh-preflight", "безопасность"]
---

# Развертывание N8NAgents

## Цель

Пройти контролируемые этапы подготовки и развертывания self-hosted n8n assistant без обхода security gates.

## Контекст

Источник требований: [[Источник_Мастер_Промпт_N8NAgents]]. Локальная проверка SSH-предпосылок завершена. Пользователь 2026-08-26 явно принял ограниченное TOFU-исключение для первого подключения без независимой проверки host fingerprint: [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]. Compatibility baseline: [[Матрица_Совместимости_N8NAgents_2026-08-26]]; runtime-утверждения, помеченные `UNVERIFIED`, требуют live evidence.

## Definition of Done (DoD)

- [x] Локальный SSH-preflight завершён без раскрытия секретов.
- [ ] Фактический SSH-порт и ожидаемый host fingerprint независимо подтверждены. Исключение пользователя не закрывает этот пункт.
- [x] Явное принятие риска TOFU зафиксировано для точного ограниченного scope; G1 не повышен до `PASS`.
- [x] Выполнен read-only discovery VPS без mutations: [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]].
- [ ] Представлены архитектура, затрагиваемые файлы, rollback и non-secret параметры.
- [ ] Получен явный approval перед любыми изменениями VPS.
- [ ] MVP Phase A прошёл заявленные проверки.
- [x] Локальная foundation подготовлена и получила `GO-LOCAL`; этот пункт не заменяет server/runtime гейты.

## Уровень рассуждения

- [ ] medium (рутина)
- [ ] high (архитектура/интеграция)
- [x] xhigh (безопасность/критичные данные)

## Stop / Go / Kill

**Stop если:** попытка выходит за принятое TOFU-исключение: иной target, port или user; password fallback; `StrictHostKeyChecking=no`; глобальный `known_hosts`; port scan; изменившийся/reinstalled host key; mutation или неоднозначный endpoint. Также Stop, если private key отсутствует, повреждён, не соответствует public key или имеет небезопасный ACL.

**Stop если:** discovery обнаружит неизвестную установку, конфликт портов 80/443, недостаток ресурсов или иной стоп-фактор из мастер-промпта.

**Go к plan review:** A2 read-only discovery `PASS`; до server mutations необходимы exact command/object list, архитектура, downtime/rollback, firewall/IPv6 решение и отдельный approval.

**Kill если:** дальнейший шаг требует обхода TLS, использования `StrictHostKeyChecking=no`, ослабления firewall/authentication либо любого действия вне документированного TOFU-исключения и явно согласованного scope.

## Текущий gate

- T1 local SSH-preflight: `PASS` — [[Доказательство_T1_Local_SSH_Preflight_N8NAgents]].
- A1: первоначальная session-channel проблема зафиксирована в [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]].
- A2: **`PASS`** после reboot VPS; полный read-only discovery clean, без mutations — [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]].
- Server mutations: не начаты. Следующий gate — exact deployment plan/review и отдельный approval.
- E1 local foundation review: **`GO-LOCAL`**; server deployment: **`NO-GO`** — [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]].

## Сделанные изменения

- Создана стартовая структура знаний и навигация проекта.
- Выполнен только локальный read-only SSH-preflight; key material и fingerprint не сохранены, ключи и ACL не изменялись.
- Дословно и с датой зафиксировано явное принятие пользователем остаточного риска TOFU; SSH/VPS-действия в рамках этой фиксации не выполнялись.
- A1 ограниченно подтвердила transport/authentication, но не выполнила remote command; удалённых mutations не было.
- Локальная secret-free foundation подготовлена в `codex/n8nagents-foundation` на HEAD `1839a29e1620a670c80b1428bfb4d4f56ba867ac`; статические проверки прошли в объёме evidence E1.

## Оставшаяся работа

- Подготовить и пройти review exact deployment plan: команды/объекты, архитектура, firewall/IPv6 policy, downtime и rollback.
- Не считать G1 `PASS` без независимой проверки.
- Закрыть compatibility acceptance gates из [[Матрица_Совместимости_N8NAgents_2026-08-26]] до production deployment.
- Перепроверить JSON Schema semantic validation, когда локальный `jsonschema`-валидатор даст отдельное evidence; не считать её пройденной по статическому `PASS`.
- Закрыть non-secret входные данные из ручной очереди; секреты вводить напрямую в server-side credential flow.
- Перед server mutation иметь завершённый discovery, архитектуру, точные команды/объекты, downtime/rollback и fresh console check.

## Доказательства

- Контрольная сумма исходного мастер-промпта: [[Источник_Мастер_Промпт_N8NAgents]].
- Local SSH-preflight: [[Доказательство_T1_Local_SSH_Preflight_N8NAgents]].
- User-accepted TOFU exception: [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].
- A1 SSH session-channel: [[Доказательство_A1_SSH_Сеансный_Канал_N8NAgents]].
- A2 read-only discovery: [[Доказательство_A2_ReadOnly_Discovery_N8NAgents_20260826]].
- E1 local foundation/review: [[Доказательство_E1_Local_Foundation_Review_N8NAgents_20260826]].

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Промпт_N8NAgents_v1_2026-08-25]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Матрица_Совместимости_N8NAgents_2026-08-26]]
