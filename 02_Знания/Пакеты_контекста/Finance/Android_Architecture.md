---
id: "ctx-android-architecture"
тип: "пакет_контекста"
проект: "Finance"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["finance", "android", "kotlin", "архитектура"]
ссылки:
  - "[[MOC_Finance]]"
---

# Android Architecture (Архитектура Android-приложения)

## Обзор

Нативный Android-клиент Finance — одноактивностное приложение на Kotlin + Jetpack Compose. Отвечает за: управление счетами/категориями/транзакциями, on-device OCR скриншотов чеков, secure-авторизацию через Bearer-токены, просмотр аналитики.

Пакет: `com.finance.mvp`. Версия: `0.1.0`.

## Стек

| Компонент | Версия / Значение |
|---|---|
| Kotlin | 1.9.24 |
| AGP | 8.5.2 |
| Jetpack Compose BOM | 2024.10.00 |
| Compose Compiler Extension | 1.5.14 |
| Material3 | из BOM |
| ML Kit Text Recognition | 16.0.1 |
| androidx.security-crypto | 1.1.0 |
| kotlinx-coroutines-android | 1.8.1 |
| compileSdk / targetSdk | 34 |
| minSdk | 26 (Android 8.0) |
| JVM target | 17 |

HTTP-клиент: `HttpURLConnection` (без Retrofit). JSON: `org.json`. Сетевые таймауты: connect 5s, read 5s.

## Структура модулей

```
com.finance.mvp/
├── MainActivity.kt          — точка входа, DI через конструктор
├── api/
│   └── ApiClient.kt         — FinanceApiClient (interface), LiveFinanceApiClient, модели DTO
├── capture/
│   ├── CaptureParser.kt           — парсинг OCR-текста в CaptureCandidate
│   ├── CaptureCandidate.kt        — модели: CaptureCandidate, CategoryAggregateCandidate, ScreenshotOcrParseResult
│   └── CategoryAggregateMappingStore.kt — интерфейс + EncryptedSharedPreferences-реализация
├── session/
│   └── TokenStore.kt        — SecureTokenStore (interface), AndroidSecureTokenStore, InMemorySecureTokenStore
└── ui/
    ├── FinanceApp.kt         — главный @Composable, навигация, состояния
    ├── AppSection.kt         — enum секций навигации
    └── theme/
        └── Theme.kt          — FinanceTheme, FinanceLightColors
```

## OCR на устройстве

Модуль `capture/` выполняет распознавание и парсинг полностью on-device, без отправки изображений на сервер.

### ML Kit Text Recognition

В `FinanceApp.kt` функция `recognizeScreenshotText()` получает `InputImage` из URI через Photo Picker, обрабатывает `TextRecognizer` (latin-модель) и возвращает распознанный текст. GMS Task оборачивается в `suspendCancellableCoroutine`.

### CaptureParser

`CaptureParser` (object) — stateless-парсер с двумя режимами:

**Одиночный чек** — `parseScreenshotOcr()`:
- Фильтрует переводы (`transferSignals`) и доходы (`incomeSignals`)
- Извлекает сумму regex: `amountAfterRegex` / `amountBeforeRegex` — поддерживает `₽ RUB RUR USD $ € EUR`
- Нормализует разделители (пробел как thousands separator, запятая → точка)
- При `preferContextualAmount = true` приоритет сумме рядом с `primaryAmountSignals` (purchase, payment, total…), отфильтровывает `balanceSignals`
- Извлекает merchant: regex-паттерны `at/merchant/broker` + stop-words + фильтр sensitivity (цифры, телефоны)
- Вычисляет confidence (0.0–0.95): базовый 0.45 + бонусы за expense-сигналы, broker-сигналы, merchant, card-keywords
- Порог для скриншотов: minimumConfidence 0.55
- Генерирует `evidenceHash` (SHA-256) и `idempotencyKey` (capture-v1:source:timeBucket:amount:currency:merchant:hash)

**Категорийный агрегат** — `parseCategoryAggregateScreenshotOcr()`:
- Парсит строки вида «Категория  1234.56 ₽  5 операций»
- Использует `aggregateOperationCountRegex` для подсчёта операций
- `aggregateSummaryRegex` для пропуска служебных строк
- `aggregateHeaderLines` — стоп-множество заголовков
- Возвращает `List<CategoryAggregateCandidate>` с confidence 0.82
- Дедупликация по `(normalizedLabel, amount, operationCount)`

### CategoryAggregateMappingStore

`AndroidCategoryAggregateMappingStore` — хранилище маппинга `(userContext, externalLabel) → categoryId` в `EncryptedSharedPreferences` (AES256-SIV keys, AES256-GCM values). Ключ нормализуется через SHA-256.

## API клиент

### FinanceApiClient (interface)

Определяет полный набор операций: `login`, `register`, `sessionStatus`, `dashboard`, CRUD счетов/категорий/транзакций, `createDemoTransfer`, capture-drafts (`create/list/update/confirm/discard`), `logout`.

### LiveFinanceApiClient

Реализация на `HttpURLConnection`:
- `ApiConfig` — `baseUrl` (default: `http://10.0.2.2:8000` из BuildConfig)
- `safeCall` — обёртка: `ApiResult.Success` / `ApiResult.Failure` с перехватом `ApiException` и общих ошибок
- Авторизация: `Authorization: Bearer <token>` из `SecureTokenStore`
- При 401/403 — автоматическая очистка токена
- JSON-парсинг: `JSONObject` / `JSONArray` с вспомогательными extension-функциями
- URL-encoding путей и query-параметров
- Optimistic concurrency: `version` в PATCH-запросах

### Модели DTO

`SessionStatus`, `FinanceDashboard`, `AccountSummary`, `CategorySummary`, `TransactionSummary`, `MoneyTotal`, `CaptureDraft`, `CaptureDraftCreateRequest`, `CaptureDraftUpdateRequest`, `RegistrationResult`, `ApiResult<T>` (sealed: Success / Failure).

## Session management

### SecureTokenStore (interface)

Три метода: `readAccessToken()`, `saveAccessToken()`, `clear()`. Все suspend.

### AndroidSecureTokenStore

Хранит Bearer-токен в `EncryptedSharedPreferences` (`finance_secure_session`):
- `MasterKey` с AES256-GCM
- Pref keys: AES256-SIV, values: AES256-GCM
- I/O через `Dispatchers.IO`
- Файл: `shared_prefs/finance_secure_session.xml`

### InMemorySecureTokenStore

In-memory реализация для тестов и preview.

### Auth flow

1. `POST /api/v1/sessions` → `accessToken` сохраняется в `TokenStore`
2. Все последующие запросы — с `Authorization: Bearer`
3. `DELETE /api/v1/sessions/current` → logout + `tokenStore.clear()`
4. При 401/403 → автоматический `tokenStore.clear()`

## UI

### FinanceApp.kt

Главный `@Composable` (~2500 строк). Содержит:
- `Scaffold` с `TopAppBar`, `NavigationBar` (5 секций), `FloatingActionButton`
- Управление состоянием через `rememberSaveable` / `mutableStateOf`
- `LaunchedEffect` для восстановления сессии и загрузки capture drafts
- Секции: Home (CapitalCard, MonthExpenseCard, TopCategoriesCard, RecentOperationsCard), Operations (TransactionRow + CaptureDraftReviewCard), Assets, Categories (CategoryManagementCard), Analytics

### AppSection

Enum с пятью вкладками: Home, Operations, Assets, Categories, Analytics. Каждая с `title` и `subtitle`.

### FinanceTheme

Material3 light-only тема. Кастомная палитра `FinanceLightColors` — зелёно-бирюзовый primary (#256B5F), тёплый secondary (#6E5F1F), нейтральный background (#FBFCFA).

### QuickAdd

`ModalBottomSheet` с выбором типа (Expense/Income/Transfer/Asset), суммы, счета, категории, режима (Personal/Shared/Overview).

### FinanceMode

Personal / Shared / Overview — фильтрация счетов и операций.

## Тесты

### Unit tests (app/src/test/)

| Файл | Область |
|---|---|
| `CaptureParserTest.kt` | regex-парсинг CaptureParser |
| `ApiClientCaptureDraftTest.kt` | capture-drafts API |
| `ApiClientRegistrationTest.kt` | регистрация / accepted |
| `ApiClientScopeTest.kt` | scope и helper-функции API |
| `ApiConfigTest.kt` | валидация ApiConfig |
| `LoginFormTest.kt` | валидация credentials |
| `FinanceSessionRestoreTest.kt` | восстановление сессии |
| `AppSectionTest.kt` | навигационные секции |

Фреймворк: JUnit 4.13.2 + `org.json:json:20240303`.

### Instrumented tests (app/src/androidTest/)

| Файл | Область |
|---|---|
| `CaptureParserMlKitInstrumentationTest.kt` | ML Kit OCR на устройстве |
| `FinanceAppUiTest.kt` | Compose UI тесты |
| `AndroidSecureTokenStoreTest.kt` | EncryptedSharedPreferences token store |

Фреймворк: `androidx.test.ext:junit:1.2.1` + `androidx.compose.ui:ui-test-junit4`.

---

Связанные заметки: [[MOC_Finance]], [[OCR_Pipeline]], [[Auth_Model]], [[Capture_Draft_Lifecycle]]
