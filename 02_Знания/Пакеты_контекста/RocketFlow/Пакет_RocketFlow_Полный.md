---
id: "pkg-rocketflow-full"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-05-31"
обновлено: "2026-08-23"
уверенность: "высокая"
источники: ["README.md", "docs/33-current-state-summary.md", "docs/58-github-cicd-policy.md", "docs/60-hexcore-prod-runbook.md", "docs/70-native-ios-parity-contract.md", "docs/71-native-ios-delivery.md", "ios/README.md"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
исторические_доказательства: ["Док_V21_Scroll_Priority_20260822", "Док_Calendar_Weekly_Focus_WebPush_20260810", "Док_Cleanup_Manifest", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification"]
теги: ["пакет_контекста", "rocketflow", "агрегат"]
---

# Пакет контекста: RocketFlow (полный)

Агрегирующий пакет контекста для любого агента. Предоставляет полную картину проекта через ссылки на все ключевые заметки vault.

## Быстрый старт

1. Прочитать [[RocketFlow]] — цель и стек проекта
2. Изучить [[MOC_RocketFlow]] — навигационная карта vault
3. Выбрать пакет для своей роли: [[Пакет_Бэкенд]], [[Пакет_Android]] или [[Пакет_iOS]]

## Current application checkpoint 2026-08-23

- Current repo docs HEAD: `codex/native-ios-companion` / `201a3de8657e56a3a67e1051522cb5793ce5c0b7`.
- Immutable app-code/build evidence: `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3` / run `32655691351`; branch HEAD и app SHA не тождественны.
- Native iOS 16+ реализует Planner/Calendar/Focus, offline GRDB/sync/conflicts, details/editors/sharing, reminders, RU/EN, restoration/deep links и account safety.
- [iOS Verify run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351), job `97233929959`: parity/packages/build PASS, `540` unit + `2` UI tests PASS; [[Док_iOS_Verification]].
- Commit `0bbf4acb` и `ios-verify` пока есть только в candidate branch; `origin/master` `7d1ac74cf8f2bf7935c2578f3675db4ca54764bb` изменится только после merge. Candidate push email storm остановлен; production workflows unchanged, branch protection не настроена; [[MOC_DevOps]].
- Clone/build/test simulator на Mac — **GO**; App Store/public release — **NO-GO** до внешних гейтов.
- Production server остаётся на SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21 (`21/21`); preflight `>=20`, manifest/post `>=21`. Candidate V22 для iOS device registrations не deployed; DB здесь не проверялась.

## Production checkpoint 2026-08-22

- Production release `sha-50a63270ae09` from exact SHA `50a63270ae094fe08ee57b945be0930cb1115dfe`; run `32551808905` success.
- Backend/web joint promotion PASS, Flyway `20 -> 21`, health/web HTTP `200`, no duplicate promotion or rollback.
- Authenticated disposable API smoke and cleanup PASS; HTTP `5xx` — `0`.
- Personal APK `0.1.1` (`versionCode 2`) signed and direct-sideload verified; [[Док_Android_Verification]].
- Exact-SHA backup waiver consumed without fresh recovery point and is not precedent; permanent task [[Задача_Production_Deploy_Backup_Rollback]] remains open.
- Current state: [[Док_Prod_Deploy_State]]. Historical V21 rollout/waiver evidence: [[Док_V21_Scroll_Priority_20260822]], [[ADR_V21_Release_Backup_Waiver]].

## Структура знаний

### Проект и волны
- [[RocketFlow]] — основной проект
- [[Wave_A]], [[Wave_B]], [[Wave_C]] — волны разработки
- [[MVP3_Упрощение]] — упрощение MVP3

### Архитектурные карты
- [[MOC_Бэкенд]] — бэкенд: модули, API, БД, тесты, Docker
- [[MOC_Веб]] — веб-клиент: роуты, компоненты, сборка
- [[MOC_Android]] — Android: активности, FCM, smoke-процедуры
- [[MOC_iOS]] — native iOS: архитектура, offline/sync, navigation и release gates
- [[MOC_DevOps]] — CI/CD, HexCore, деплой, бэкапы

### Глоссарий (27 терминов)
[[Folder]], [[Goal]], [[Task]], [[Green_Task]], [[Red_Task]], [[Tag]], [[Task_Link]], [[Planned_Time]], [[Due_Time]], [[Reminder_Rule]], [[Recurrence_Rule]], [[Reschedule_Event]], [[Priority_Decay|legacy Priority Decay]], [[ADR_Отказ_От_Приоритета_Задач]], [[Share_Invitation]], [[Collaborator]], [[Device_Registration]], [[Notification_Delivery]], [[Modular_Monolith]], [[REST_API]], [[JWT]], [[FCM]], [[Flyway]], [[Docker_Image]], [[HexCore]], [[PostgreSQL_Advisory_Lock]], [[Optimistic_Locking]], [[Soft_Delete]]

### Источники
[[Источник_README]], [[Источник_MVP_План]], [[Источник_Спецификация_Домена]], [[Источник_Архитектура]], [[Источник_API_Контракты]], [[Источник_QA_Стратегия]], [[Источник_План_Оркестрации]], [[Источник_Текущее_Состояние]], [[Источник_CI_CD_Политика]], [[Источник_Продакшен_Runbook]], [[Источник_Нотификация_Смок]], [[Источник_Нотификация_Пруф]], [[Источник_Агент_Плейбук]], [[Источник_MVP3_Контракт]], [[Источник_AGENTS]], [[Источник_Android_Local_Setup]]

### Решения
[[ADR_Модульный_Монолит]], [[ADR_PostgreSQL]], [[ADR_JWT_Токены]], [[ADR_Flyway_Миграции]], [[ADR_Мягкое_Удаление]], [[ADR_Оптимистичная_Блокировка]], [[ADR_Firebase_Admin_SDK]], [[ADR_Scheduler_Advisory_Lock]], [[ADR_Logical_Device_Upsert]], [[ADR_Отказ_От_Приоритета_Задач]], [[ADR_V21_Release_Backup_Waiver]]

### Доказательства
Актуальные: [[Док_iOS_Verification]], [[Док_Prod_Deploy_State]], [[Док_Artifacts_Retention_Policy]].

Исторические checkpoints: [[Док_Backend_Тесты]], [[Док_Web_Build]], [[Док_Android_Build]], [[Док_Нотификации_E2E]], [[Док_Calendar_Weekly_Focus_WebPush_20260810]], [[Док_Cleanup_Manifest]], [[Док_Backend_Verification]], [[Док_Web_Verification]], [[Док_Android_Verification]], [[Док_V21_Scroll_Priority_20260822]].

### Агенты (7)
[[Оркестратор]], [[Агент_Бэкенд]], [[Агент_Веб]], [[Агент_Android]], [[Агент_iOS]], [[Агент_QA]], [[Агент_DevOps]]

### Системные заметки
[[Регламент_CI_CD]], [[Регламент_Деплоя]], [[Регламент_Нотификационного_Смока]], [[Схема_Базы_Данных]], [[Схема_Развертывания]], [[Схема_Ветвления]], [[Промпт_Оркестратора]]

### Задачи
[[Задача_Production_Deploy_Backup_Rollback]], [[Задача_GHCR_Publish]], [[Задача_Staging_Notification_Cert]], [[Задача_CI_Runtime_Lanes]], [[Ограничения_и_Риски]]

## Ролевые пакеты
- [[Пакет_Бэкенд]] — выжимка для бэкенд-агента
- [[Пакет_Android]] — выжимка для Android-агента
- [[Пакет_iOS]] — выжимка для iOS-агента
