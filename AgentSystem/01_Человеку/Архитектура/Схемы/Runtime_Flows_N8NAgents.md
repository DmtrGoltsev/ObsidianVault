---
id: "schema-n8nagents-runtime-flows-20260829"
тип: "схема"
статус: "утверждено"
проект: "AgentSystem"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-31"
уверенность: "высокая"
источники: ["[[CURRENT_STATE_N8NAgents_2026-08-29]]"]
доказательства: ["[[Доказательство_OpenClaw_n8n_Production_PASS_20260831]]"]
теги: ["n8n", "openclaw", "схема", "выполнение", "потоки", "фактическое-состояние"]
---

# Потоки выполнения N8NAgents

## Текущая схема рабочего сервера

```mermaid
flowchart TB
    U[Владелец] --> T[Telegram Bot API]
    T -->|долгий опрос, единственный вход| O[OpenClaw]
    O --> D[DeepSeek API]
    O <--> M[(Markdown-память и SQLite-сессия)]
    O -->|подписанная команда| A[Action API n8n]
    A --> P[(PostgreSQL)]
    S[systemd-таймеры] --> W1[Материализатор n8n]
    S --> W2[Подтверждения n8n]
    W1 --> P
    W2 --> P
    W1 --> T
    W2 --> T
    O --> T
    C[Caddy, публичный периметр] -.->|404 для внутренних путей| A
```

OpenClaw не имеет публичного интерфейса. PostgreSQL, n8n и внутренние webhook доступны только внутри сервера; административный доступ выполняется через SSH-туннель.

## Обычный разговор

```mermaid
sequenceDiagram
    participant U as Владелец
    participant T as Telegram
    participant O as OpenClaw
    participant M as Память
    participant D as DeepSeek
    U->>T: Сообщение
    T->>O: Обновление через долгий опрос
    O->>O: Проверка разрешённого чата
    O->>M: Загрузка контекста
    O->>D: Запрос без секретов
    D-->>O: Ответ
    O->>M: Разрешённое обновление памяти
    O->>T: Ответ владельцу
    T-->>U: Сообщение
```

После перезапуска OpenClaw память и сессия сохраняются; это подтверждено проверкой на рабочем сервере.

## Действие с напоминанием

```mermaid
sequenceDiagram
    participant U as Владелец
    participant O as OpenClaw
    participant A as Action API n8n
    participant P as PostgreSQL
    U->>O: Создать, показать, отменить, перенести или подтвердить
    O->>A: HMAC-подписанная типизированная команда
    A->>A: Проверка подписи, схемы, прав и повтора
    A->>P: Атомарная операция и аудит
    P-->>A: Структурированный результат
    A-->>O: Код и данные результата
    O-->>U: Понятный ответ
```

Точный исполнитель — workflow `ActionAPI0000001`, версия `83bd9d8b-278c-4dd1-ad7a-3e7cac9edb69`, внутренний путь `/internal/actions/v1`.

## Плановая отправка

```mermaid
sequenceDiagram
    participant S as systemd-таймер
    participant N as n8n планировщик
    participant P as PostgreSQL
    participant T as Telegram
    S->>N: Внутренний HMAC-запрос
    N->>P: Найти и атомарно забрать готовую работу
    P-->>N: Не более одного задания на ключ
    N->>T: Отправить уведомление
    N->>P: Записать результат и аудит
```

| Назначение | Workflow | Версия | Внутренний путь | Таймер |
|---|---|---|---|---|
| Материализация напоминаний | `SchedMatFresh001` | `2347cf7a-5880-496e-a4c1-3243d641d47c` | `/internal/schedulers/fresh/materializer/v1` | `n8nagents-scheduler@materializer.timer` |
| Подтверждения и служебная доставка | `SchedConfFresh01` | `d0634147-5bf7-49c8-84cc-cd6c910b64f7` | `/internal/schedulers/fresh/confirmation/v1` | `n8nagents-scheduler@confirmation.timer` |

Оба таймера активны. Ранняя контрольная отправка доставлена ровно один раз (`message_id=56`), а две существующие пользовательские задачи остались без изменений.

## Реальный E2E с подтверждением

```mermaid
sequenceDiagram
    participant U as Владелец
    participant O as OpenClaw 0.1.3
    participant A as Action API n8n
    participant P as PostgreSQL
    participant S as Свежий планировщик
    participant T as Telegram
    U->>O: Команда создать напоминание
    O->>A: reminder_create
    A->>P: Ожидающее предложение
    O->>T: Кнопки «Подтвердить» и «Отменить»
    U->>T: Нажатие «Подтвердить»
    T->>O: callback_query
    O->>A: reminder_confirm
    A->>P: Однократное применение
    O->>T: Удалить клавиатуру и показать итог
    S->>P: Получить одну готовую доставку
    S->>T: Отправка attempt 1
    S->>P: TELEGRAM_SENT
```

Фактический результат: предложение `7644fe60…` применено один раз к задаче `121347b3…`; создано по одному событию и доставке; Telegram `message_id=62`, попытка `1`, итог `TELEGRAM_SENT` в 13:17 по Москве. Все проверенные счётчики дубликатов равны нулю, а кратность операции и отправки — единице.

## Сбой и остановка

При размножении сообщений останавливается только проблемный получатель обновлений или конкретный таймер. PostgreSQL, задачи и аудит сохраняются. Прежний основной сценарий и старые планировщики остаются неактивными, пока отдельный план отката не исключит появление двух входов Telegram.

Связанные документы: [[Participants_and_Flows_N8NAgents]], [[Change_History_N8NAgents]], [[Доказательство_OpenClaw_n8n_Production_PASS_20260831]], [[Регламент_Operations_N8NAgents]].
