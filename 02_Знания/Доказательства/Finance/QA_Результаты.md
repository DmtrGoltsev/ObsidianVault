---
id: "qa-results-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-06-06"
ссылки:
  - "[[Finance]]"
  - "[[QA_Фиксы]]"
---

# QA Результаты — Finance MVP Android

## Волна 1: Статический аудит кода (2026-06-06)

**Метод:** Статический анализ FinanceApp.kt (~3030 строк) + ApiClient.kt (~936 строк) + аудит API-контрактов

**Агенты:** 2 параллельных (ревьюер кода + API-ревьюер)

### Сводка

| Метрика | Значение |
|---------|----------|
| Всего багов найдено | 25 |
| P0 (критические) | 3 |
| P1 (важные) | 8 |
| P2 (минорные) | 14 |
| API endpoint'ов проверено | 26 |
| Критических API расхождений | 0 |
| Исправлено в этой волне | 12 |

### Результаты по багам

#### P0 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-001 | `userFacingMessage()` скрывает реальные ошибки API | FIXED |
| BUG-003 | Пароли в `rememberSaveable` (persisted state) | FIXED |
| BUG-005 | Сессия не сбрасывается при 401 — UI остаётся «авторизованным» | FIXED |

#### P1 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-002 | `updateTransaction` хардкодит сумму и описание | FIXED |
| BUG-004 | Архивированные счета/категории видны в QuickAdd | FIXED |
| BUG-010 | `parseSession` игнорирует displayName пользователя | FIXED |

#### P1 — Открытые

| ID | Описание | Статус |
|----|----------|--------|
| BUG-006 | AddAccountSheet всегда создаёт shared-счёт | OPEN |
| BUG-007 | Нет защиты от double-tap на деструктивные действия | OPEN |
| BUG-008 | Удаление транзакции без подтверждения | OPEN |
| BUG-009 | Суммирование мультивалют без конвертации | OPEN |
| BUG-023 | `quickAddCategoryFor` молча подменяет выбор | OPEN |

#### P2 — Исправлены

| ID | Описание | Статус |
|----|----------|--------|
| BUG-011 | FAB и кнопки TopAppBar видны неавторизованному | FIXED |
| BUG-012 | Кнопка «Подтвердить» активна без выбора счёта/категории | FIXED |
| BUG-015 | Несогласованность fallback-валюты RUB/USD | FIXED |
| BUG-016 | «Включить» вместо «Включено» для включённого элемента | FIXED |
| BUG-017 | editName не сбрасывается при отмене редактирования | FIXED |
| BUG-019 | captureSource отображается на английском | FIXED |
| BUG-022 | SignInCard мигает при загрузке авторизованного пользователя | FIXED |

#### P2 — Открытые

| ID | Описание | Статус |
|----|----------|--------|
| BUG-013 | HttpURLConnection никогда не disconnect() | OPEN |
| BUG-014 | Dashboard делает 4-6 последовательных запросов | OPEN |
| BUG-018 | AssetChips onClick не делает ничего | OPEN |
| BUG-020 | Избыточный запрос /sessions/current в dashboard() | OPEN |
| BUG-021 | Нет валидации формата email | OPEN |
| BUG-024 | restoreAccount/restoreCategory/restoreTransaction не вызываются из UI | OPEN |
| BUG-025 | Race condition между loadDashboard и loadCaptureDrafts | OPEN |

### API-аудит

| Проверка | Результат |
|----------|-----------|
| Все endpoint'ы существуют на backend | OK |
| HTTP-методы совпадают | OK |
| Имена полей JSON корректны | OK |
| Response parsing корректен | OK |
| Dashboard обрезает данные при >50 записях | WARN |
| CaptureDraft description nullable vs required | WARN |

### Русификация

| Метрика | Значение |
|---------|----------|
| Строк переведено | 44 |
| Непереведённых пользовательских строк | 0 |
| Сборка после русификации | OK |

### Тест-кейсы

| Модуль | Кейсов |
|--------|--------|
| AUTH | 14 |
| HOME | 11 |
| OPERATIONS | 9 |
| CAPTURE | 13 |
| ASSETS | 12 |
| CATEGORIES | 9 |
| ANALYTICS | 7 |
| QUICK-ADD | 16 |
| **Итого** | **91** |

### Сборка

| Параметр | Значение |
|----------|----------|
| APK | `artifacts/apk/finance-mvp-0.1.0-debug.apk` |
| Размер | 51.72 MB |
| URL | `http://45.10.110.42/finance-api` |
| Сборка | BUILD SUCCESSFUL |
| Дата | 2026-06-06 |

## Волна 2: Assets UI + account edit + backend account PATCH (2026-06-06)

**Метод:** targeted backend tests, Android debug build, `git diff --check`, runtime smoke на эмуляторе `Codex`.

**Scope:** Assets UI, редактирование счёта, backend `PATCH account`.

### Сводка

| Проверка | Результат |
|----------|-----------|
| Backend targeted tests | `22 passed, 1 warning` |
| Android build | `BUILD SUCCESSFUL in 57s` |
| Android build command | `assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` |
| `git diff --check` | exit 0, только CRLF warnings |
| Runtime smoke | APK установлен на `Codex`, `MainActivity` открыт |
| Эмуляторы | `Codex` использован; `Android1` не трогали |
| Account edit runtime flow | `NOT_RUN` — на `Codex` нет активных счетов/данных |

### Backend/API

| Проверка | Результат |
|----------|-----------|
| `PATCH account` payload | `name`, `currentBalance`, `currency`, `version` |
| `initialBalance` | Не меняется через PATCH |
| Optimistic conflict | `CONFLICTING_UPDATE` |
| Валюта счёта с транзакциями | `ACCOUNT_CURRENCY_IMMUTABLE_AFTER_TRANSACTIONS` |

### Android

| Область | Результат |
|---------|-----------|
| Assets category tap | expand/collapse группы |
| Edit group name | без refresh icon |
| Archive group accounts | long press >1s + confirmation |
| Account edit dialog | `name`, `balance`, `currency` |
| XAU | label `граммы`, icon gold bar |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Нет runtime proof для existing account edit flow | OPEN |
| Архивация группы может примениться частично, если последовательный `archiveAccount` упадёт | OPEN |
| Имя виртуальной группы хранится только в локальном UI state | OPEN |

## Волна 3: Аналитика -> Планирование MVP (2026-06-06)

**Метод:** full backend pytest, targeted planning/openapi/db tests, OpenAPI parse, Android debug build, runtime smoke на эмуляторе `Codex`, `dev_seed` smoke.

**Scope:** Planning MVP во вкладке Analytics, backend planning API/DB, Android planning UI и локальные reminders.

### Сводка

| Проверка | Результат |
|----------|-----------|
| `python -m pytest` | `224 passed`, 4 warnings |
| Targeted planning/openapi/db tests | `29 passed` |
| Android build | `BUILD SUCCESSFUL` |
| OpenAPI parse | OK |
| OpenAPI paths | `PATH_COUNT=37`, все planning paths присутствуют |
| `dev_seed` smoke | login 201, planning history 200, personal plan 200, без internal server error |
| `git diff --check` | pass, только LF/CRLF warnings |
| Runtime smoke | Planning screen открыт на `Codex`, показал следующий месяц/current plan/totals |
| Эмуляторы | `Codex` использован; `Android1` не targeted |

### Возможности

| Область | Результат |
|---------|-----------|
| Scope | personal + shared |
| Валюта | one currency |
| Income sources | `amount`, `source`, `dayOfMonth` |
| Reminders | local Android reminders per income |
| Confirm | обновляет только план, транзакции не создаёт |
| Allocations | expense categories, accounts, assets, investments |
| Allocation mode | `amount` или `percent` |
| Контроль заполнения | underallocated banner, overallocated warning |
| История | history/copy |
| Создание сущностей | category/account creation inherits scope |

### Backend/API

| Проверка | Результат |
|----------|-----------|
| Package | new planning package |
| DB tables | `planning_plans`, `planning_income_sources`, `planning_allocations` |
| Migration | `20260606_0010` |
| OpenAPI | planning endpoints добавлены |
| Authz personal | owner-only |
| Authz household | active-member |
| Totals | derived totals |
| Copy | attention rows |
| Validation | positive income validation |
| Seed/runtime | `dev_seed` planning runtime fix |

### Android

| Область | Результат |
|---------|-----------|
| API client | planning DTO/methods в `ApiClient` |
| UI | `PlanningUi` во вкладках Analytics |
| Notifications | `AlarmManager` + `BroadcastReceiver` |
| Permission | `POST_NOTIFICATIONS` |
| Explicitly excluded | без FCM/SMS/NotificationListener/exact alarm |
| Runtime | Codex smoke |

### Остаточные риски

| Риск | Статус |
|------|--------|
| Exact visual/end-to-end creation flow только smoke-tested, не exhaustive manual scenario | OPEN |
| Local alarms reset if app force-stopped; boot/package replace covered | OPEN |
| `dev_seed` planning targets need sync if demo seed expands | OPEN |
| Past plans not strictly read-only at API level; history/copy implemented | OPEN |

## Открытые вопросы (NEEDS_CLARIFICATION)

1. Фильтрация категорий — какие типы доступны в каких режимах?
2. Transfer-фильтрация по режиму видимости
3. Ограничение длины имени категории/счёта
4. Restore без UI — как пользователь восстанавливает удалённое?
5. Report только для household — нужен ли personal?
6. Мультивалютная конвертация — как отображать капитал?
