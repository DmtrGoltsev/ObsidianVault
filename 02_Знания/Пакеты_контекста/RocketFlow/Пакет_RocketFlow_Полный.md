---
id: "pkg-rocketflow-full"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["docs/33-current-state-summary.md", "README.md", "docs/04-architecture-blueprint.md"]
доказательства: ["Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "Док_Prod_Deploy_State"]
теги: ["пакет_контекста", "rocketflow", "агрегат"]
---

# Пакет контекста: RocketFlow (полный)

Агрегирующий пакет контекста для любого агента. Предоставляет полную картину проекта через ссылки на все ключевые заметки vault.

## Быстрый старт

1. Прочитать [[RocketFlow]] — цель и стек проекта
2. Изучить [[MOC_RocketFlow]] — навигационная карта vault
3. Выбрать пакет для своей роли: [[Пакет_Бэкенд]] или [[Пакет_Android]]

## Структура знаний

### Проект и волны
- [[RocketFlow]] — основной проект
- [[Wave_A]], [[Wave_B]], [[Wave_C]] — волны разработки
- [[MVP3_Упрощение]] — упрощение MVP3

### Архитектурные карты
- [[MOC_Бэкенд]] — бэкенд: модули, API, БД, тесты, Docker
- [[MOC_Веб]] — веб-клиент: роуты, компоненты, сборка
- [[MOC_Android]] — Android: активности, FCM, smoke-процедуры
- [[MOC_DevOps]] — CI/CD, HexCore, деплой, бэкапы

### Глоссарий (27 терминов)
[[Folder]], [[Goal]], [[Task]], [[Green_Task]], [[Red_Task]], [[Tag]], [[Task_Link]], [[Planned_Time]], [[Due_Time]], [[Reminder_Rule]], [[Recurrence_Rule]], [[Reschedule_Event]], [[Priority_Decay]], [[Share_Invitation]], [[Collaborator]], [[Device_Registration]], [[Notification_Delivery]], [[Modular_Monolith]], [[REST_API]], [[JWT]], [[FCM]], [[Flyway]], [[Docker_Image]], [[HexCore]], [[PostgreSQL_Advisory_Lock]], [[Optimistic_Locking]], [[Soft_Delete]]

### Источники
[[Источник_README]], [[Источник_MVP_План]], [[Источник_Спецификация_Домена]], [[Источник_Архитектура]], [[Источник_API_Контракты]], [[Источник_QA_Стратегия]], [[Источник_План_Оркестрации]], [[Источник_Текущее_Состояние]], [[Источник_CI_CD_Политика]], [[Источник_Продакшен_Runbook]], [[Источник_Нотификация_Смок]], [[Источник_Нотификация_Пруф]], [[Источник_Агент_Плейбук]], [[Источник_MVP3_Контракт]], [[Источник_AGENTS]], [[Источник_Android_Local_Setup]]

### Решения (9 ADR)
[[ADR_Модульный_Монолит]], [[ADR_PostgreSQL]], [[ADR_JWT_Токены]], [[ADR_Flyway_Миграции]], [[ADR_Мягкое_Удаление]], [[ADR_Оптимистичная_Блокировка]], [[ADR_Firebase_Admin_SDK]], [[ADR_Scheduler_Advisory_Lock]], [[ADR_Logical_Device_Upsert]]

### Доказательства
[[Док_Backend_Тесты]], [[Док_Web_Build]], [[Док_Android_Build]], [[Док_Нотификации_E2E]], [[Док_Cleanup_Manifest]], [[Док_Backend_Verification]], [[Док_Web_Verification]], [[Док_Android_Verification]], [[Док_Artifacts_Retention_Policy]], [[Док_Prod_Deploy_State]]

### Агенты (6)
[[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_QA]], [[Агент_DevOps]]

### Системные заметки
[[Регламент_CI_CD]], [[Регламент_Деплоя]], [[Регламент_Нотификационного_Смока]], [[Схема_Базы_Данных]], [[Схема_Развертывания]], [[Схема_Ветвления]], [[Промпт_Оркестратора]]

### Задачи
[[Задача_GHCR_Publish]], [[Задача_Staging_Notification_Cert]], [[Задача_CI_Runtime_Lanes]], [[Ограничения_и_Риски]]

## Ролевые пакеты
- [[Пакет_Бэкенд]] — выжимка для бэкенд-агента
- [[Пакет_Android]] — выжимка для Android-агента
