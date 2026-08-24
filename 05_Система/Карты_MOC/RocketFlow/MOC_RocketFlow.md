---
id: "moc-rocketflow-main"
тип: "MOC"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["README.md", "docs/33-current-state-summary.md", "docs/58-github-cicd-policy.md", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "docs/72-native-ios-mac-device-handoff.md", "docs/ios-native-mac-codex-install-prompt.md", "ios/README.md"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State", "Док_Artifacts_Retention_Policy"]
исторические_доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Production_Rollout_20260810", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification"]
теги: ["moc", "навигация", "rocketflow"]
---

# MOC RocketFlow — Главная навигационная карта

Главная точка входа в Obsidian vault проекта RocketFlow. Связывает все компоненты знаний: проекты, архитектуру, глоссарий, источники, агентов, системные заметки, решения, доказательства и пакеты контекста.

Current repo docs HEAD: `codex/native-ios-companion` / `b75ca723f767f520bee39ea72052b1a4b03a7e59`. Immutable Mac tooling checkpoint отдельно: `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149` / run `32669924719`; app behavior checkpoint отдельно: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` / run `32655691351`; [[Док_iOS_Verification]]. Production server: SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21; V22 not deployed, DB здесь не проверялась.

CI trigger policy `0bbf4acb` остаётся candidate-only: feature push auto run `0`, manual verify доступен, default PR/master behavior изменится после merge. Production workflows и branch protection не менялись; см. [[MOC_DevOps]].

## Проект

- [[RocketFlow]] — основной проект
- [[Wave_A]] — Волна A: фундамент
- [[Wave_B]] — Волна B: надстройка
- [[Wave_C]] — Волна C: финализация
- [[MVP3_Упрощение]] — упрощение MVP3

## Архитектура

- [[MOC_Бэкенд]] — карта бэкенд-компонентов
- [[MOC_Веб]] — карта веб-клиента
- [[MOC_Android]] — карта Android-клиента
- [[MOC_iOS]] — карта native iOS-клиента
- [[Пакет_iOS_Mac_Установка]] — handoff на другой Mac и personal iPhone
- [[MOC_DevOps]] — карта DevOps и CI/CD

## Глоссарий

- [[Folder]] — папка
- [[Goal]] — цель
- [[Task]] — задача
- [[02_Знания/Глоссарий/RocketFlow/Green_Task|Green_Task]] — зелёная задача
- [[02_Знания/Глоссарий/RocketFlow/Red_Task|Red_Task]] — красная задача
- [[Tag]] — тег
- [[Task_Link]] — связь между задачами
- [[Planned_Time]] — плановое время
- [[Due_Time]] — срок выполнения
- [[02_Знания/Глоссарий/RocketFlow/Reminder_Rule|Reminder_Rule]] — правило напоминания
- [[02_Знания/Глоссарий/RocketFlow/Recurrence_Rule|Recurrence_Rule]] — правило повторения
- [[Reschedule_Event]] — событие переноса
- [[02_Знания/Глоссарий/RocketFlow/Priority_Decay|Priority_Decay]] — выведенный из продукта legacy-механизм; compatibility shadow до завершения V20/old APK support
- [[Share_Invitation]] — приглашение к совместному доступу
- [[Collaborator]] — соавтор
- [[Device_Registration]] — регистрация устройства
- [[Notification_Delivery]] — доставка уведомлений
- [[Modular_Monolith]] — модульный монолит
- [[REST_API]] — REST API
- [[JWT]] — JSON Web Token
- [[FCM]] — Firebase Cloud Messaging
- [[Flyway]] — миграции БД
- [[Docker_Image]] — Docker-образ
- [[HexCore]] — production-сервер
- [[PostgreSQL_Advisory_Lock]] — блокировка PostgreSQL
- [[Optimistic_Locking]] — оптимистичная блокировка
- [[Soft_Delete]] — мягкое удаление
- [[Idea]] — идея внутри папки
- [[EntityLink]] — обобщённая связь между сущностями
- [[TaskPlan]] — Android-план с детерминированной сортировкой без task priority
- [[PlanningSync]] — офлайн-синхронизация планирования
- [[FolderNote]] — заметка в папке

## Источники

- [[02_Знания/Источники/RocketFlow/Источник_README|Источник_README]] — README проекта
- [[Источник_MVP_План]] — план MVP
- [[Источник_Спецификация_Домена]] — спецификация домена
- [[02_Знания/Источники/RocketFlow/Источник_Архитектура|Источник_Архитектура]] — архитектурный blueprint
- [[Источник_API_Контракты]] — API контракты
- [[Источник_QA_Стратегия]] — стратегия QA
- [[Источник_План_Оркестрации]] — план оркестрации
- [[Источник_Текущее_Состояние]] — текущее состояние
- [[Источник_CI_CD_Политика]] — CI/CD политика
- [[Источник_Продакшен_Runbook]] — production runbook
- [[Источник_Нотификация_Смок]] — smoke-тест нотификаций
- [[Источник_Нотификация_Пруф]] — доказательство нотификаций
- [[Источник_Агент_Плейбук]] — плейбук агентов
- [[Источник_MVP3_Контракт]] — контракт MVP3
- [[Источник_MVP2_Иерархия]] — контракт MVP2: иерархия и связи
- [[Источник_MVP3_QA_Модель]] — QA-модель приёмки MVP3
- [[Источник_MVP3_BA_Пути]] — BA-контракт: пользовательские пути MVP3
- [[Источник_Бэкап_Runbook]] — runbook скачивания production backup
- [[Источник_Android_Local_Setup]] — локальная Android SDK/emulator конфигурация
- [[Источник_AGENTS]] — AGENTS.md

## Агенты

- [[Оркестратор]] — агент-оркестратор
- [[Агент_Бэкенд]] — бэкенд-агент
- [[Агент_Веб]] — веб-агент
- [[Агент_Android]] — Android-агент
- [[Агент_iOS]] — iOS-агент
- [[Агент_QA]] — QA-агент
- [[Агент_DevOps]] — DevOps-агент

## Система

### Регламенты
- [[Регламент_CI_CD]]
- [[Регламент_Деплоя]]
- [[Регламент_Нотификационного_Смока]]
- [[Регламент_Оркестратора]]
- [[Регламент_Субагента]]

### Схемы
- [[Схема_Базы_Данных]]
- [[Схема_Развертывания]]

### Промпты
- [[Промпт_Оркестратора]]
- [[Промпт_Правил_Оркестратора]]

### Входные точки
- [[Старт_Агента]]

### Шаблоны
- [[Шаблон_Проект]]
- [[Шаблон_Термин]]
- [[Шаблон_Источник]]
- [[Шаблон_Агент]]
- [[Шаблон_Задача]]
- [[Шаблон_Решение]]
- [[Шаблон_Доказательство]]
- [[Шаблон_Регламент]]
- [[Шаблон_Пакет_Контекста]]
- [[Шаблон_MOC]]

## Решения

- [[ADR_Модульный_Монолит]]
- [[ADR_PostgreSQL]]
- [[ADR_JWT_Токены]]
- [[ADR_Flyway_Миграции]]
- [[ADR_Мягкое_Удаление]]
- [[ADR_Оптимистичная_Блокировка]]
- [[ADR_Firebase_Admin_SDK]]
- [[ADR_Scheduler_Advisory_Lock]]
- [[ADR_Logical_Device_Upsert]]
- [[ADR_Отказ_От_Приоритета_Задач]]
- [[ADR_V21_Release_Backup_Waiver]]

## Доказательства

### Актуальные

- [[Док_iOS_Verification]]
- [[Док_Prod_Deploy_State]]
- [[Док_Artifacts_Retention_Policy]]

### Исторические checkpoints

- [[Док_Backend_Тесты]]
- [[Док_Web_Build]]
- [[Док_Android_Build]]
- [[Док_Нотификации_E2E]]
- [[Док_Calendar_Weekly_Focus_WebPush_20260810]]
- [[Док_Cleanup_Manifest]]
- [[Док_Backend_Verification]]
- [[Док_Web_Verification]]
- [[Док_Android_Verification]]
- [[Док_Production_Rollout_20260810]]
- [[Док_V21_Scroll_Priority_20260822]]

## Пакеты контекста

- [[Пакет_RocketFlow_Полный]]
- [[Пакет_Бэкенд]]
- [[Пакет_Android]]
- [[Пакет_iOS]]
- [[Пакет_iOS_Mac_Установка]]

## Задачи

- [[Задача_Production_Deploy_Backup_Rollback]]
- [[Задача_GHCR_Publish]]
- [[Задача_Staging_Notification_Cert]]
- [[Задача_CI_Runtime_Lanes]]
- [[Ограничения_и_Риски]]
