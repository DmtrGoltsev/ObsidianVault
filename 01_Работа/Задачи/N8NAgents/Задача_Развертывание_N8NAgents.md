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
теги: ["n8n", "развертывание", "ssh-preflight", "безопасность"]
---

# Развертывание N8NAgents

## Цель

Пройти контролируемые этапы подготовки и развертывания self-hosted n8n assistant без обхода security gates.

## Контекст

Источник требований: [[Источник_Мастер_Промпт_N8NAgents]]. Локальная проверка SSH-предпосылок завершена. Пользователь 2026-08-26 явно принял ограниченное TOFU-исключение для первого подключения без независимой проверки host fingerprint: [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].

## Definition of Done (DoD)

- [x] Локальный SSH-preflight завершён без раскрытия секретов.
- [ ] Фактический SSH-порт и ожидаемый host fingerprint независимо подтверждены. Исключение пользователя не закрывает этот пункт.
- [x] Явное принятие риска TOFU зафиксировано для точного ограниченного scope; G1 не повышен до `PASS`.
- [ ] Выполнен только read-only discovery VPS; evidence сохранён без секретов.
- [ ] Представлены архитектура, затрагиваемые файлы, rollback и non-secret параметры.
- [ ] Получен явный approval перед любыми изменениями VPS.
- [ ] MVP Phase A прошёл заявленные проверки.

## Уровень рассуждения

- [ ] medium (рутина)
- [ ] high (архитектура/интеграция)
- [x] xhigh (безопасность/критичные данные)

## Stop / Go / Kill

**Stop если:** попытка выходит за принятое TOFU-исключение: иной target, port или user; password fallback; `StrictHostKeyChecking=no`; глобальный `known_hosts`; port scan; изменившийся/reinstalled host key; mutation или неоднозначный endpoint. Также Stop, если private key отсутствует, повреждён, не соответствует public key или имеет небезопасный ACL.

**Stop если:** discovery обнаружит неизвестную установку, конфликт портов 80/443, недостаток ресурсов или иной стоп-фактор из мастер-промпта.

**Go только для узкой read-only discovery:** точный IP `154.59.110.121`, предполагаемый `TCP/22`, SSH user `root`, key-only authentication, отдельный project-scoped `known_hosts` и `StrictHostKeyChecking=accept-new`. Это user-accepted exception, а не подтверждение G1.

**Kill если:** дальнейший шаг требует обхода TLS, использования `StrictHostKeyChecking=no`, ослабления firewall/authentication либо любого действия вне документированного TOFU-исключения и явно согласованного scope.

## Текущий gate

- T1 local SSH-preflight: `PASS` — [[Доказательство_T1_Local_SSH_Preflight_N8NAgents]].
- Текущий gate — **G1: NOT VERIFIED — USER-ACCEPTED-EXCEPTION (TOFU via accept-new)**.
- Host fingerprint и фактический SSH-порт не подтверждены; G1 никогда не считать `PASS` на основании этого исключения.
- Разрешена только одна узкая read-only discovery-сессия в точном scope из [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].
- До discovery, архитектуры и явного approval изменения VPS запрещены.

## Сделанные изменения

- Создана стартовая структура знаний и навигация проекта.
- Выполнен только локальный read-only SSH-preflight; key material и fingerprint не сохранены, ключи и ACL не изменялись.
- Дословно и с датой зафиксировано явное принятие пользователем остаточного риска TOFU; SSH/VPS-действия в рамках этой фиксации не выполнялись.

## Оставшаяся работа

- Выполнить только ограниченную read-only SSH discovery для `154.59.110.121:22` в режиме key-only + project-scoped `known_hosts` + `accept-new`; без port scan и mutations.
- Сохранить redacted evidence фактически принятого host key и discovery, не повышая G1 до `PASS`.
- Независимое подтверждение host fingerprint и фактического SSH-порта остаётся незакрытым, если пользователь позднее потребует verified gate.
- Перед любыми изменениями VPS представить архитектуру, точные команды/объекты, downtime/rollback и получить отдельный явный approval.

## Доказательства

- Контрольная сумма исходного мастер-промпта: [[Источник_Мастер_Промпт_N8NAgents]].
- Local SSH-preflight: [[Доказательство_T1_Local_SSH_Preflight_N8NAgents]].
- User-accepted TOFU exception: [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].

## Связанные заметки

- [[N8NAgents]]
- [[MOC_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[Промпт_N8NAgents_v1_2026-08-25]]
