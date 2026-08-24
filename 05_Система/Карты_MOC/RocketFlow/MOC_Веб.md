---
id: "moc-web"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "средняя"
источники: ["docs/04-architecture-blueprint.md"]
доказательства: ["Док_Web_Build", "Док_Web_Verification"]
теги: ["moc", "web", "rocketflow"]
---

# MOC Веб

Карта веб-клиента RocketFlow. React 18, TypeScript 5, Vite 5, react-router-dom 6, lucide-react.

## Роуты

Веб-клиент использует react-router-dom 6. Основные маршруты:

- `/login` — страница входа
- `/register` — регистрация
- `/` — главная (дашборд / папки)
- `/planning` — планирование (цели, задачи, календарь)
- `/advanced` — расширенные настройки (sharing, reminders, recurrence)
- `/settings` — настройки пользователя

## Компоненты

- UI-компоненты на базе lucide-react
- Формы входа / регистрации
- Списки папок, целей, задач
- Календарный вид
- Компоненты совместного доступа
- Компоненты напоминаний и повторений

## Фичи

### auth
Аутентификация через [[JWT]]. Логин, регистрация, обновление токенов.

### planning
Управление [[Folder|папками]], [[Goal|целями]], [[Task|задачами]]. Поддержка [[Green_Task|зелёных]] и [[Red_Task|красных]] задач. [[Priority_Decay]].

### advanced
[[Share_Invitation|Совместный доступ]], [[Recurrence_Rule|повторения]], [[Reminder_Rule|напоминания]].

## i18n

Интернационализация (русский, английский).

## Сборка

Vite 5. `npm run build` — production-сборка в статические файлы.

## Статика

Раздаётся Nginx на [[HexCore]].

## CI

[[Регламент_CI_CD]] — web-verify.yml (`npm run build`); web test scripts отсутствуют, runtime lane open. См. [[Док_Web_Build]], [[Док_Web_Verification]], [[Задача_CI_Runtime_Lanes]].

## Связанные MOC

- [[MOC_RocketFlow]] — главная карта
- [[MOC_Бэкенд]] — бэкенд API
- [[MOC_DevOps]] — развёртывание
