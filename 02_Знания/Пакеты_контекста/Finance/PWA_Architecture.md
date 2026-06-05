---
id: "ctx-pwa-architecture"
тип: "пакет_контекста"
проект: "Finance"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["finance", "pwa", "react", "web", "архитектура"]
ссылки:
  - "[[MOC_Finance]]"
---

# Web PWA Architecture (Архитектура веб-приложения)

## Обзор

`@finance/web-pwa` — React-приложение с PWA-поддержкой для браузеров и Capacitor-обёрткой для iOS. Реализует клиентскую панель семейных финансов: аутентификация, учёт операций, OCR-захват чеков со скриншотов, аналитика. Работает как standalone-сайт и как нативное iOS-приложение через Capacitor.

**Пакет:** `apps/web-pwa`
**App ID (Capacitor):** `com.codex.finance`
**WebDir (сборка):** `dist/`

---

## Стек

| Слой | Технология | Версия |
|---|---|---|
| UI | React | ^19.2 |
| Bundler | Vite | ^7.2 |
| Язык | TypeScript | ^5.9 |
| Native bridge | Capacitor | ^8.3 |
| Иконки | lucide-react | ^0.561 |
| Тесты | Vitest + Testing Library + jsdom | ^4.0 |
| CSS | Vanilla CSS (без preprocessors) | — |

---

## Структура

```
apps/web-pwa/
├── src/
│   ├── App.tsx                    # Корневой компонент, все секции UI
│   ├── main.tsx                   # Точка входа: render + SW registration
│   ├── styles.css                 # Глобальные стили, responsive
│   ├── pwaPaths.ts                # Manifest builder, basePath utils
│   ├── registerServiceWorker.ts   # SW registration с scope awareness
│   └── api/
│       ├── client.ts              # Typed HTTP-клиент + DTO маппинг
│       └── types.ts               # Доменные типы и interfaces
├── public/
│   ├── sw.js                      # Service Worker (cache-first shell)
│   └── pwa-icon.svg               # PWA иконка
├── scripts/
│   └── build-ios.mjs              # iOS-сборка с hardcoded env
├── capacitor.config.ts            # Capacitor конфигурация
├── vite.config.ts                 # Vite + manifest plugin + Vitest
├── package.json
└── ios/                           # Capacitor iOS native wrapper
    └── App/App/
        ├── AppDelegate.swift
        ├── Assets.xcassets/
        ├── Info.plist
        └── capacitor.config.json
```

---

## API клиент

**Файл:** `src/api/client.ts`

### Архитектура

`LiveFinanceApiClient` реализует interface `FinanceApiClient` — typed обёртка над `fetch`. Все вызовы идут через единый метод `request<T>()`, который:

- Определяет `baseUrl` из `VITE_API_BASE_URL` (dev: `http://127.0.0.1:8000`, prod: `/finance-api`)
- Управляет CSRF-токеном через cookie `finance_csrf` и header `X-CSRF-Token`
- Авторизация через cookie-based сессию (`credentials: "include"`)
- При 403 сбрасывает CSRF, при 401 — клиент знает что сессия истекла
- Возвращает typed `DashboardSnapshot` как агрегированную модель

### DTO → Domain mapping

Входящие JSON DTO (`AccountDto`, `TransactionDto`, `CategoryDto`, `CaptureDraftDto`, `ReportSummaryDto`) маппятся в доменные типы из `types.ts` через набор `map*()` функций. Dev-seed имена переводятся в пользовательские через `userFacingSeedText()`.

### Основные группы endpoints

| Группа | Paths | Операции |
|---|---|---|
| Sessions | `/api/v1/sessions` | login (POST), current (GET), logout (DELETE) |
| Accounts | `/api/v1/accounts` | CRUD, archive, restore |
| Categories | `/api/v1/categories` | CRUD, archive, restore |
| Transactions | `/api/v1/transactions` | create operation/transfer, update, archive, restore |
| Reports | `/api/v1/reports/summary` | summary by mode (shared_family_report, combined_viewer_overview) |
| Capture Drafts | `/api/v1/capture-drafts` | create, list, update, confirm, discard |
| OCR | `/api/v1/capture-drafts/screenshot-ocr` | upload screenshot → parse |
| Category Mappings | `/api/v1/capture-drafts/category-mappings` | save externalLabel → categoryId mapping |

### Dashboard Snapshot

Единый агрегат `DashboardSnapshot` собирается из параллельных GET-запросов к `/sessions/current`, `/accounts`, `/categories`, `/transactions` + отчёты. Содержит: session info, accounts, categories, operations, transfers, reports.

---

## OCR Capture Flow

**Связанные заметки:** [[OCR_Pipeline]], [[Capture_Draft_Lifecycle]]

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│ Screenshot   │───▶│ uploadScreenshot │───▶│ ScreenshotOcrResult │
│ (PNG/JPEG/   │    │ Ocr()           │    │ (category aggregates)│
│  WebP file)  │    │ POST FormData    │    │ + confidence +       │
└─────────────┘    └──────────────────┘    │   idempotencyKey     │
                                            └──────────┬──────────┘
                                                       │
                                          User reviews & maps
                                          externalLabel → categoryId
                                                       │
                                                       ▼
                              ┌──────────────────────────────────────┐
                              │ saveCategoryMapping()                │
                              │ + createCaptureDraft() для каждого   │
                              │ выбранного candidate                 │
                              └──────────────┬───────────────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │ PendingCaptureDraftsPanel     │
                              │ Пользователь редактирует      │
                              │ сумму/дату/счет/категорию     │
                              │ и подтверждает или отклоняет  │
                              └──────────────┬───────────────┘
                                             │
                                    confirm / discard
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │ confirmCaptureDraft()         │
                              │ → создаёт реальную операцию   │
                              │ discardCaptureDraft()         │
                              │ → помечает черновик удалённым │
                              └──────────────────────────────┘
```

Ключевые моменты:
- OCR возвращает `categoryAggregate` кандидатов — агрегированные расходы по категориям
- Каждый кандидат содержит `confidence`, `idempotencyKey`, `evidenceHash`
- Пользователь маппит `externalLabel` на `categoryId` и выбирает счёт
- Черновики проходят через статусы: `pending` → `confirmed` / `discarded`

---

## PWA

### Service Worker (`public/sw.js`)

- **Cache name:** `finance-mvp-shell-v2`
- **Стратегия:** cache-first для app shell (index, manifest, icon)
- **Install:** pre-cache shell → `skipWaiting()`
- **Activate:** удалить старые кэши → `clients.claim()`
- **Fetch:** только GET-запросы в scope, не API — отдаются из кэша, fallback к сети
- API-запросы (префиксы `/api/`, `/finance-api/`, `/rocket-api/`) **не кэшируются**

### Web Manifest (`pwaPaths.ts`)

Manifest генерируется программно как Vite-плагин `finance-pwa-manifest`:
- Динамический `basePath` через `VITE_BASE_PATH` / `FINANCE_PWA_BASE_PATH`
- Отдаётся и как middleware (dev), и как asset (build)
- `display: "standalone"`, `lang: "ru"`, одна SVG-иконка (any + maskable)

### Registration (`registerServiceWorker.ts`)

- Регистрация только в `PROD` режиме
- Проверка `isSecureContext` (или localhost/127.0.0.1 для HTTP)
- SW scope вычисляется из `BASE_URL`
- Ошибки регистрации глушатся (Plain HTTP IP origins)

---

## iOS / Capacitor

### Конфигурация

**`capacitor.config.ts`:** appId `com.codex.finance`, appName `Finance`, webDir `dist`

### Native wrapper (`ios/App/App/`)

- `AppDelegate.swift` — стандартный CapacitorAppDelegate
- `Assets.xcassets/` — AppIcon, LaunchStoryboard
- `Info.plist` — bundle конфигурация
- `capacitor.config.json` — mirror Capacitor конфига

### iOS Build pipeline

**`scripts/build-ios.mjs`:**
1. Запускает `tsc -b` с env `VITE_BASE_PATH="/"`
2. Запускает `vite build` с тем же env
3. `VITE_API_BASE_URL` хардкодится на production endpoint

**Скрипты:**
- `npm run build:ios` — сборка web-assets для iOS
- `npm run cap:sync:ios` — build + `cap sync ios`
- `npm run cap:open:ios` — `cap open ios`

---

## Секции UI

Приложение — single-page с sidebar-навигацией (desktop) и bottom nav (mobile). Sidebar + content layout через CSS Grid.

### View Modes

| Mode | Описание | Report |
|---|---|---|
| `personal` | Личные счета/категории | — |
| `shared` | Общие семейные | `shared_family_report` |
| `overview` | Комбинированный | `combined_viewer_overview` |

### Секции

| Section ID | Label | Компонент | Назначение |
|---|---|---|---|
| `money` | Деньги / Обзор | `MoneyDashboard` | Капитал, расходы/доходы месяца, группы активов, топ категорий, последние операции |
| `operations` | Операции | `OperationsPage` | Timeline + OCR capture + pending drafts |
| `assets` | Счета и активы | `AssetsPage` | Grid активов по видам |
| `categories` | Категории | `CategoriesPage` | Grid + CRUD форма категорий |
| `analytics` | Аналитика | `AnalyticsPage` | Метрики, категории bar chart, капитал по группам |
| `settings` | Настройки | `SettingsPage` | Режим по умолчанию, валюта |

### Quick Add

Модальный sheet для быстрого добавления: expense, income, transfer, asset. Desktop — primaryButton в topbar, mobile — FAB. Форма включает выбор вида, суммы, счёта, категории, даты, комментария, видимости (personal/shared).

### Responsive

- Desktop (>1020px): sidebar 260px + content, 4-col metric grid, 3-col asset grid
- Tablet (760–1020px): 2-col grids
- Mobile (<760px): sidebar скрыт, bottom nav (5 кнопок), FAB, single-column, bottom sheet

---

## Доменные типы (`src/api/types.ts`)

| Тип | Назначение |
|---|---|
| `CurrencyCode` | RUB / USD / EUR |
| `MoneyAmount` | { value, currency } |
| `AccountKind` | card, bank, cash, deposit, brokerage, metal, other |
| `AccountSummary` | Счёт с балансом, ownership, статусом |
| `CategoryDirection` | income / expense |
| `CategoryScope` | personal / household |
| `CategorySummary` | Категория с planned/actual |
| `OperationSummary` | Операция с signed amount |
| `TransferSummary` | Перевод between accounts |
| `ScreenshotOcrCandidate` | OCR-кандидат: label, amount, confidence, evidenceHash |
| `CaptureDraftSummary` | Черновик захвата с lifecycle status |
| `ReportMode` | shared_family_report / combined_viewer_overview |
| `ReportSummary` | Отчёт: income, expense, balanceDelta |
| `SessionSnapshot` | Текущая сессия: viewer, household |
| `DashboardSnapshot` | Агрегат всего состояния UI |

---

## Тестирование

- **Framework:** Vitest 4 + Testing Library + jsdom
- **Environment:** `jsdom`, globals: true
- **Setup:** `vitest.setup.ts`
- **Команды:** `npm test` (run), `npm run test:watch` (watch)

---

## Ссылки

- [[MOC_Finance]]
- [[OCR_Pipeline]]
- [[Auth_Model]]
- [[Capture_Draft_Lifecycle]]
