---
id: "ctx-n8nagents-current-state-20260829"
тип: "пакет_контекста"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-31"
уверенность: "высокая"
источники:
  - "[[Доказательство_OpenClaw_n8n_Production_PASS_20260831]]"
  - "[[Архитектура_AS_IS_и_API_Tools_N8NAgents]]"
  - "Git N8NAgents production base 36e149374802263d644cc98e510f6113e1095dae"
доказательства:
  - "[[Доказательство_OpenClaw_n8n_Production_PASS_20260831]]"
  - "[[Доказательство_Production_Acceptance_N8NAgents_20260829]]"
теги: ["n8n", "openclaw", "production", "текущее-состояние", "передача-контекста"]
---

# Текущее состояние N8NAgents

Это канонический снимок рабочего сервера после production PASS 31 августа 2026 года. OpenClaw теперь действующая часть системы, а не целевой план.

## Коротко

- OpenClaw через долгий опрос Telegram является единственным получателем входящих сообщений одного разрешённого личного чата.
- DeepSeek ведёт диалог под управлением OpenClaw.
- OpenClaw хранит сеанс и Markdown-память; оба слоя пережили перезапуск.
- Любое изменение напоминаний проходит через закрытый HMAC-подписанный Action API n8n.
- PostgreSQL — главный источник истины для задач, подтверждений и аудита.
- n8n отправляет плановые напоминания независимо от диалогового процесса.

## Компоненты и точные идентификаторы

| Компонент | Состояние |
|---|---|
| OpenClaw | Активен; Telegram long polling, DeepSeek, сеансовая и Markdown-память |
| `n8nagents-actions` | Активное расширение OpenClaw `0.1.2` |
| Action API n8n | `ActionAPI0000001`, версия `83bd9d8b-278c-4dd1-ad7a-3e7cac9edb69`, путь `/internal/actions/v1` |
| Материализатор | `SchedMatFresh001`, версия `2347cf7a-5880-496e-a4c1-3243d641d47c`, путь `/internal/schedulers/fresh/materializer/v1` |
| Повторы подтверждения | `SchedConfFresh01`, версия `d0634147-5bf7-49c8-84cc-cd6c910b64f7`, путь `/internal/schedulers/fresh/confirmation/v1` |
| systemd | Активны `n8nagents-scheduler@materializer.timer` и `n8nagents-scheduler@confirmation.timer` |
| Caddy | Публичные Action API и scheduler-пути отвечают `404`; панель OpenClaw не публикуется |

## Действующие инструменты

`reminder_create`, `reminder_list`, `reminder_cancel`, `reminder_reschedule`, `reminder_confirm`.

Инструменты не дают DeepSeek выбирать SQL, URL, учётные данные, получателя или имя workflow (сценария n8n).

## Плановая отправка

Два защищённых systemd-таймера ежеминутно вызывают внутренние HMAC-подписанные webhook. Контрольное событие доставлено в Telegram ровно один раз (`message_id=56`). Две существовавшие задачи владельца при этом не изменены.

## Что отключено

- прежний `01_telegram_assistant` не получает Telegram updates;
- прежние `reminders_v2_materializer_dispatcher` и `reminders_v2_confirmation_dispatcher` неактивны;
- групповые чаты, browser, shell, Docker socket и произвольный HTTP не входят в разрешённую поверхность OpenClaw.

## Ограничения

Это однопользовательский MVP на малом VPS. Новые получатели, группы, общие сетевые инструменты, платежи и необратимые действия не разрешены этим PASS.

Связанные заметки: [[MOC_N8NAgents]], [[Архитектура_AS_IS_и_API_Tools_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Регламент_Operations_N8NAgents]].
