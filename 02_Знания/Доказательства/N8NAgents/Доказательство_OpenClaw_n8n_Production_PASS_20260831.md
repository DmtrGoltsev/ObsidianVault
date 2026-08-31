---
id: "evidence-n8nagents-openclaw-production-pass-20260831"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-31"
обновлено: "2026-08-31"
уверенность: "высокая"
источники:
  - "Обезличенная production-проверка N8NAgents 2026-08-31"
  - "OpenClaw plugin n8nagents-actions 0.1.2"
  - "n8n workflow metadata 2026-08-31"
доказательства: []
теги: ["n8nagents", "openclaw", "n8n", "production", "pass"]
---

# Production PASS: OpenClaw + n8n

## Итог

31 августа 2026 года целевая связка OpenClaw + n8n прошла проверку на рабочем сервере. Эта запись фиксирует обезличенные факты; секреты, числовые идентификаторы владельца и тексты его задач не сохраняются.

## Подтверждённые факты

| Область | Результат |
|---|---|
| Вход Telegram | OpenClaw получает сообщения долгим опросом; это единственный активный вход |
| OpenClaw | Контейнер работает; расширение `n8nagents-actions` версии `0.1.2` загружено |
| DeepSeek | Обычный диалог и выбор типизированного инструмента проходят через OpenClaw |
| Память | Markdown-память и сеанс сохранились после контролируемого перезапуска |
| Action API | Сценарий `ActionAPI0000001`, версия `83bd9d8b-278c-4dd1-ad7a-3e7cac9edb69`, активен |
| Инструменты | Зарегистрированы ровно `reminder_create`, `reminder_list`, `reminder_cancel`, `reminder_reschedule`, `reminder_confirm` |
| Планировщик | Свежие сценарии материализации и повторов подтверждения активны |
| Таймеры | `n8nagents-scheduler@materializer.timer` и `n8nagents-scheduler@confirmation.timer` активны |
| Плановая отправка | Контрольное напоминание доставлено ровно один раз; Telegram `message_id=56` |
| Данные владельца | Две существовавшие задачи не изменены контрольной проверкой |
| Публичная поверхность | Проверенные внешние пути Action API и scheduler возвращают `404`; панель OpenClaw не опубликована |
| Старые сценарии | Прежний основной сценарий Telegram и прежние сценарии планировщика неактивны |

## Точные сценарии планировщика

| Назначение | ID | Версия | Внутренний путь |
|---|---|---|---|
| Превращение расписания в готовые к отправке события | `SchedMatFresh001` | `2347cf7a-5880-496e-a4c1-3243d641d47c` | `/internal/schedulers/fresh/materializer/v1` |
| Повторные запросы подтверждения | `SchedConfFresh01` | `d0634147-5bf7-49c8-84cc-cd6c910b64f7` | `/internal/schedulers/fresh/confirmation/v1` |

Оба пути вызываются локальным служебным контуром с HMAC-подписью. Внешний клиент не может вызвать их через Caddy.

Шаблоны systemd размещены в `/etc/systemd/system/n8nagents-scheduler@.service` и `/etc/systemd/system/n8nagents-scheduler@.timer`; активны экземпляры `n8nagents-scheduler@materializer.service`, `n8nagents-scheduler@confirmation.service` и соответствующие таймеры.

## Ограничение доказательства

PASS подтверждает текущую связку одного владельца. Он не расширяет область на группы, новых получателей, произвольные инструменты или публичную панель.

Связанные заметки: [[CURRENT_STATE_N8NAgents_2026-08-29]], [[Архитектура_AS_IS_и_API_Tools_N8NAgents]], [[Runtime_Flows_N8NAgents]], [[Change_History_N8NAgents]].
