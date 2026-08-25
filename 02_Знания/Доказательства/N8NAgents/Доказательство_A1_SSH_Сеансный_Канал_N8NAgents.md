---
id: "evidence-n8nagents-a1-ssh-session-channel-20260826"
тип: "доказательство"
статус: "заблокировано"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Доказательство_T1_Local_SSH_Preflight_N8NAgents]]"
  - "[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]"
доказательства: []
теги: ["n8n", "ssh", "tofu", "диагностика", "blocked-external"]
---

# A1 — SSH: аутентификация пройдена, сеансный канал не отвечает

## Что доказывается

Только результат первой ограниченной TOFU-попытки SSH. Это не является read-only discovery VPS и не доказывает выполнение удалённой команды.

## Границы и сохранённые безопасные параметры

- TCP-соединение, закреплённый project-scoped SSH host key и public-key authentication прошли со статусом `PASS`.
- Путь identity file, SHA-256 fingerprint закреплённого host key и file hash уже были известны в локальном контексте попытки; значения намеренно не дублируются в vault.
- Использовались ранее зафиксированные TOFU scope и key-only authentication из [[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]].
- Секреты, содержимое ключей, IP, токены, пароли и служебный вывод не сохранялись.

## Наблюдаемый результат

| Шаг | Результат | Статус |
|---|---|---|
| TCP transport | Установлен | PASS |
| Pinned host key | Принят в ожидаемом project-scoped состоянии | PASS |
| Public-key authentication | Успешна | PASS |
| Session channel | Запрос отправлен; сервер перестал отвечать до запуска `/usr/bin/id` | BLOCKED-EXTERNAL |
| SSH process | Завершился с exit code `255` | BLOCKED-EXTERNAL |
| Удалённые команды и mutations | Не выполнены | PASS |

## Вывод

`A1` не переходит в discovery: запрос канала был отправлен, однако доказательства исполнения `/usr/bin/id` отсутствуют. Новая попытка `A2` **не начата**. Статус SSH discovery: **`BLOCKED-EXTERNAL`**.

## Безопасный следующий шаг

Требуется диагностировать provider console / SSH session-channel со стороны провайдера. Не повторять подключение, не менять SSH, firewall, users или VPS configuration до свежей console-проверки и решения внешнего блокера.

## Верификатор

- Кто проверял: ограниченный SSH-диагностический поток.
- Роль: read-only transport/authentication validation.

## Связанные заметки

- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[MOC_N8NAgents]]
