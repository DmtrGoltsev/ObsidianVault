---
id: "qa-fixes-finance"
тип: "доказательство"
статус: "активно"
проект: "Finance"
создано: "2026-06-06"
обновлено: "2026-06-06"
ссылки:
  - "[[Finance]]"
  - "[[QA_Результаты]]"
---

# QA Фиксы — Finance MVP Android

## Волна 1 (2026-06-06)

| ID | Описание | Файл | Дата | Верифицирован |
|----|----------|------|------|---------------|
| BUG-001 | userFacingMessage показывает реальные ошибки | FinanceApp.kt:2870 | 2026-06-06 | Да (сборка OK) |
| BUG-002 | updateTransaction использует реальные данные | ApiClient.kt:498 | 2026-06-06 | Да (сборка OK) |
| BUG-003 | Пароли в remember вместо rememberSaveable | FinanceApp.kt:111-112 | 2026-06-06 | Да (сборка OK) |
| BUG-004 | Фильтрация архивных записей в QuickAdd | FinanceApp.kt:2285-2286 | 2026-06-06 | Да (сборка OK) |
| BUG-005 | Сессия сбрасывается при 401 с понятным сообщением | FinanceApp.kt:319 | 2026-06-06 | Да (сборка OK) |
| BUG-010 | parseSession извлекает displayName из API | ApiClient.kt:731 | 2026-06-06 | Да (сборка OK) |
| BUG-011 | FAB скрыт на экране логина | FinanceApp.kt:613 | 2026-06-06 | Да (сборка OK) |
| BUG-012 | Кнопка «Подтвердить» отключена без выбора счёта/категории | FinanceApp.kt:1447 | 2026-06-06 | Да (сборка OK) |
| BUG-015 | Унификация fallback-валюты на RUB | FinanceApp.kt:518 | 2026-06-06 | Да (сборка OK) |
| BUG-016 | «Включено» вместо «Включить» | FinanceApp.kt:1285 | 2026-06-06 | Да (сборка OK) |
| BUG-017 | editName сбрасывается при отмене | FinanceApp.kt:1859, 2050 | 2026-06-06 | Да (сборка OK) |
| BUG-019 | captureSource локализован (Скриншот/Ручной ввод) | FinanceApp.kt:1382 | 2026-06-06 | Да (сборка OK) |
| BUG-022 | SignInCard не мигает + loading indicator | FinanceApp.kt:634, 663-673 | 2026-06-06 | Да (сборка OK) |
| L10N | 44 английских строки переведены на русский | FinanceApp.kt (全局) | 2026-06-06 | Да (сборка OK) |
| API-URL | Production URL через nginx: /finance-api | build.gradle.kts | 2026-06-06 | Да (curl 401 OK) |

## Волна 2 (2026-06-06)

| ID | Описание | Область | Дата | Верифицирован |
|----|----------|---------|------|---------------|
| ASSETS-UI | Tap category expand/collapse; edit group name без refresh icon; long press >1s confirmation/archive group accounts | Android Assets UI | 2026-06-06 | Да (сборка OK, runtime smoke MainActivity) |
| ACCOUNT-EDIT | Диалог редактирования счёта: `name`, `balance`, `currency`; XAU label `граммы`, icon gold bar | Android account edit | 2026-06-06 | Частично (`NOT_RUN` runtime flow: нет активных счетов/данных на `Codex`) |
| ACCOUNT-PATCH | `PATCH account` принимает `name`/`currentBalance`/`currency`/`version`; `initialBalance` не меняется | Backend/API | 2026-06-06 | Да (`22 passed, 1 warning`) |
| ACCOUNT-CURRENCY-GUARD | Запрет смены валюты счёта с транзакциями: `ACCOUNT_CURRENCY_IMMUTABLE_AFTER_TRANSACTIONS` | Backend/API + business rule | 2026-06-06 | Да (`22 passed, 1 warning`) |
| ACCOUNT-CONFLICT | Optimistic conflict для PATCH account: `CONFLICTING_UPDATE` | Backend/API | 2026-06-06 | Да (`22 passed, 1 warning`) |
| VIRTUAL-ASSET-GROUP-DELETE | Удаление виртуальной категории активов архивирует все активные счета группы | Android + business rule | 2026-06-06 | Частично (сборка OK; риск частичного применения при sequential `archiveAccount` failure) |

## Коммиты

| Хэш | Описание |
|------|----------|
| `95c882c` | feat(android): UI overhaul — edit/delete icons, account creation dialog, currency picker, category management, server OCR |
| `50a8f8c` | fix: 12 bugs fixed (P0-P2), full Russian localization, 91 QA test cases |
