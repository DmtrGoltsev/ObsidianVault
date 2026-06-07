---
id: "finance-designer-critic-06-ocr-error-service-path"
тип: "дизайн-критика"
проект: "Finance"
роль: "Designer Critic 06"
фокус: ["service design", "end-to-end paths", "error states", "empty states", "offline", "loading", "OCR", "capture drafts"]
создано: "2026-06-08"
статус: "draft"
severity_scale: ["P0", "P1", "P2"]
источники:
  - "C:/Users/style/Documents/ObsidianVault/README.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Пакеты_контекста/Finance/Пакет_Finance_Полный.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md"
  - "C:/Users/style/Documents/ObsidianVault/02_Знания/Глоссарий/Finance/Capture_Draft.md"
  - "C:/Users/style/Documents/Codex/Финансы/docs/current-status.md"
  - "C:/Users/style/Documents/Codex/Финансы/docs/product-mvp.md"
  - "C:/Users/style/Documents/Codex/Финансы/api/openapi/openapi.yaml"
  - "C:/Users/style/Documents/Codex/Финансы/apps/web-pwa/src/App.tsx"
  - "C:/Users/style/Documents/Codex/Финансы/apps/web-pwa/src/api/client.ts"
  - "C:/Users/style/Documents/Codex/Финансы/apps/web-pwa/src/registerServiceWorker.ts"
  - "C:/Users/style/Documents/Codex/Финансы/apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt"
  - "C:/Users/style/Documents/Codex/Финансы/apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt"
  - "C:/Users/style/Documents/Codex/Финансы/apps/android/app/src/main/java/com/finance/mvp/capture/CaptureParser.kt"
---

# Критика 06: ошибки, OCR и сервисный путь

## Позиция критика

Finance уже защищает важный доменный инвариант: OCR создает только pending capture draft, а операция появляется после явного подтверждения. Но сервисный путь вокруг ошибок пока слабее контракта: пользователь часто видит общий сбой, пустое состояние без следующего шага или disabled action без причины. Для финансового продукта это не косметика: неясный recovery path повышает риск повторных загрузок, дублей, неверного подтверждения OCR и потери доверия.

## Критические наблюдения

### 1. P0 - Android обещает on-device OCR, но текущий UI отправляет скриншот на backend

**Наблюдение:** продуктовые документы утверждают, что Android распознает скриншот локально без загрузки, но `FinanceApp.kt` читает bytes из выбранного URI и вызывает `apiClient.screenshotOcr(...)`, а `ApiClient.kt` делает multipart POST на `/api/v1/capture-drafts/screenshot-ocr`.

**Evidence paths:**
- `docs/product-mvp.md:39`, `docs/product-mvp.md:67`
- `docs/current-status.md:29`
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md:260`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:154-172`
- `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt:861-901`

**Рекомендация:** до публичного утверждения privacy-поведения выбрать один истинный контракт: либо вернуть Android на локальный OCR flow, либо явно обновить copy и release notes как "temporary upload to self-hosted backend" для Android тоже. В UI рядом с выбором скриншота показать короткий privacy disclosure по платформе.

### 2. P0 - Production OCR/login smoke не запускался, но UX уже выглядит как подтвержденный путь

**Наблюдение:** Finance KB фиксирует production deploy и health checks, но authenticated login/OCR smoke = `NOT_RUN`; journey map повторяет этот риск. При этом OCR UI на Android/PWA представлен как рабочий путь без явной маркировки production limitation.

**Evidence paths:**
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Пакеты_контекста/Finance/Пакет_Finance_Полный.md:74-76`
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md:47-50`
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md:261`

**Рекомендация:** для release-facing UX добавить gate label в QA/design checklist: OCR production path считается validated только после authenticated smoke на PWA и Android. До этого не усиливать OCR-prominence выше ручного ввода.

### 3. P1 - Android неверно локализует `captureSource=screenshot` как "Импорт"

**Наблюдение:** OpenAPI и клиенты используют `captureSource: "screenshot"`, но Android mapper знает `"screenshot_ocr"` и `"manual"`, а default возвращает "Импорт". Это прямо смешивает OCR screenshot flow с импортом файлов, который исключен из MVP.

**Evidence paths:**
- `api/openapi/openapi.yaml:2568-2578`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1533-1535`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:3611-3615`
- `docs/product-mvp.md:65-67`

**Рекомендация:** в design spec закрепить словарь source labels: `screenshot` = "Скриншот", `manual` = "Ручной ввод"; не использовать "Импорт" для capture drafts до появления отдельного import pipeline.

### 4. P1 - Пустые состояния не дают next-best action

**Наблюдение:** PWA `EmptyState` принимает только `text`, поэтому в ключевых местах пользователь видит "Нет активов", "Пока нет расходов", "Нет черновиков" без кнопки создания, explanation scope или перехода к ручному вводу. Android аналогично показывает "Нет ожидающих черновиков" без предложения выбрать скриншот, создать счет/категорию или внести операцию вручную.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:620`, `apps/web-pwa/src/App.tsx:632`, `apps/web-pwa/src/App.tsx:990-992`
- `apps/web-pwa/src/App.tsx:1284`, `apps/web-pwa/src/App.tsx:1928-1934`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1360-1364`

**Рекомендация:** заменить односложный `EmptyState` на состояние с `reason`, `scope`, `primaryAction`, `secondaryAction`. Для OCR empty: "Черновиков нет" + "Выбрать скриншот" + "Добавить расход вручную". Для активов/категорий: "создать личный счет", "создать категорию расходов".

### 5. P1 - Ошибки OCR скрывают конкретную причину и не различают recovery path

**Наблюдение:** PWA при OCR catch показывает общий текст "попробуйте другой скриншот"; Android прокидывает `userFacingMessage`, но многие ошибки превращаются в API/HTTP-текст. Backend контракт различает unsupported media, invalid image, upload too large, OCR disabled/unavailable/timeout, rate limit, но UI не мапит их на разные действия.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:1079-1081`, `apps/web-pwa/src/App.tsx:1110-1112`
- `apps/web-pwa/src/api/client.ts:813-819`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:176-182`, `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:229-232`
- `api/openapi/openapi.yaml:1673-1675`, `apps/backend/tests/capture_drafts/test_screenshot_ocr_endpoint.py`

**Рекомендация:** создать error taxonomy для OCR UI: формат не поддерживается -> выбрать PNG/JPEG/WebP; файл слишком большой -> сделать скрин области; OCR unavailable/timeout -> повторить позже или ручной ввод; rate limit -> подождать; 401 -> войти снова.

### 6. P1 - Disabled confirm не объясняет, чего не хватает

**Наблюдение:** PWA и Android блокируют создание/подтверждение OCR drafts, если нет счета, категории, даты, описания или выбранных строк, но причина disable не показана. Это особенно плохо в first-run/no-data, где у пользователя еще нет счетов и категорий.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:1125-1131`, `apps/web-pwa/src/App.tsx:1255-1258`
- `apps/web-pwa/src/App.tsx:863-870`, `apps/web-pwa/src/App.tsx:968-975`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1450-1452`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1549-1572`, `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1597-1602`

**Рекомендация:** рядом с disabled action показывать checklist: "Нужен активный счет", "Нужна категория расходов", "Выберите хотя бы одну строку", "Проверьте сумму". В Android для отсутствующих категорий уже есть кнопка "Новая" в aggregate review, но для pending draft row ее нет.

### 7. P1 - OCR aggregate path создает черновики категорий, но copy говорит о платежах/операциях

**Наблюдение:** backend endpoint распознает category aggregate rows from a screenshot; PWA copy говорит "Скрин расходов" и "Категории расходов на скриншоте", Android местами говорит "платеж на скриншоте". Пользователь может ожидать единичные транзакции, хотя создаются агрегированные expense drafts.

**Evidence paths:**
- `api/openapi/openapi.yaml:649-658`
- `apps/web-pwa/src/App.tsx:1173-1178`, `apps/web-pwa/src/App.tsx:1212-1233`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:180-191`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:224-226`

**Рекомендация:** унифицировать copy как "категории расходов со скрина" / "агрегированные черновики". Не говорить "платеж", если распознается category aggregate.

### 8. P1 - Нет явного сохранения/восстановления промежуточного review после сбоя

**Наблюдение:** PWA очищает `rows` при новом recognize и после успешного save; если сохранение части строк падает, UI оставляет общий error, но не показывает, какие строки уже созданы или как безопасно повторить без дублей. Android в цикле создания aggregate drafts останавливается на первой ошибке, но не показывает partial success.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:1070-1075`, `apps/web-pwa/src/App.tsx:1141-1167`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:258-309`
- `api/openapi/openapi.yaml:627-631`

**Рекомендация:** в review state показывать per-row status: "создан", "уже был", "ошибка", "не отправлен". Использовать idempotency как доверенное восстановление, но объяснить повтор: "Повтор безопасен, дубли не создаются".

### 9. P1 - Offline/PWA limitation технически обработан, но не представлен как состояние продукта

**Наблюдение:** service worker тихо не регистрируется на insecure origin, а current status говорит, что plain HTTP IP работает online, но PWA install/offline требует HTTPS/domain. В UI нет offline banner или read-only degraded state; глобальная ошибка загрузки просто заменяет весь app shell.

**Evidence paths:**
- `docs/current-status.md:26`
- `apps/web-pwa/src/registerServiceWorker.ts:25-36`
- `apps/web-pwa/src/App.tsx:316-325`

**Рекомендация:** в PWA добавить top-level degraded state: "Работаем online; offline/install недоступны без HTTPS". При потере сети не стирать весь контекст, а показывать retry и последнюю безопасную локальную оболочку, если она есть.

### 10. P1 - Глобальная ошибка загрузки PWA обрывает сервисный путь

**Наблюдение:** если `loadSnapshot()` падает не 401, PWA возвращает `<main className="loading">Не удалось загрузить финансы</main>` без retry, logout, diagnostics-lite или статуса сети. Для финансов это dead end.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:176-194`
- `apps/web-pwa/src/App.tsx:316-325`

**Рекомендация:** заменить full-screen dead end на error recovery shell: "Повторить", "Войти снова", "Проверить соединение", request id при наличии. 403/401/5xx/network должны иметь разные тексты и действия.

### 11. P2 - Loading states слишком общие и не защищают от повторного действия

**Наблюдение:** PWA показывает "Загружаем деньги...", "Распознаем", "Сохраняем", Android "Отправляем скриншот..." и `captureIsLoading`. Но пользователь не видит этапов: upload -> OCR -> review -> create drafts -> refresh. На слабой сети это выглядит как зависание.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:324-325`
- `apps/web-pwa/src/App.tsx:1057-1060`, `apps/web-pwa/src/App.tsx:1138-1168`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:156-158`, `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:266-300`

**Рекомендация:** сделать staged progress labels и timeout copy. Для OCR: "Загружаем скрин", "Распознаем", "Показываем черновики"; при долгой операции - "Можно вернуться к ручному вводу, скрин не сохранен".

### 12. P2 - Документы о production status конфликтуют между старым и текущим релизом

**Наблюдение:** `docs/current-status.md` указывает production commit `808f727`, а Finance KB и journey map указывают актуальный release `20260607T225457Z-819b5815`. Для дизайнера это риск неверно оценить, какие limitations уже актуальны.

**Evidence paths:**
- `docs/current-status.md:11-16`
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Пакеты_контекста/Finance/Пакет_Finance_Полный.md:63-76`
- `C:/Users/style/Documents/ObsidianVault/02_Знания/Дизайн/Finance/Карта_Пользовательских_Путей_Finance.md:47-52`

**Рекомендация:** в design docs указывать "source of truth as of date" и не брать production limitations из одного файла без сверки с Finance KB release context.

### 13. P2 - Confidence/evidence hash показаны, но не объясняют действие

**Наблюдение:** Android показывает точность и короткий след, PWA показывает процент confidence, но не объясняет, что делать при низкой уверенности. Пользователь видит число, но не получает service guidance.

**Evidence paths:**
- `apps/web-pwa/src/App.tsx:877-885`
- `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt:1545-1548`
- `api/openapi/openapi.yaml:2606-2617`

**Рекомендация:** привязать confidence к microcopy: высокая - "проверьте сумму и категорию"; низкая - "сверьте со скрином, OCR мог ошибиться"; unknown - "точность не определена, проверьте вручную".

## Рекомендации по сервисному пути

1. Зафиксировать единую матрицу OCR по платформам: источник скриншота, где распознается, что отправляется, что хранится, что удаляется, какие ошибки возможны.
2. Ввести единый компонент empty/error/retry для PWA и Android: причина, безопасное действие, альтернативный ручной путь, scope/privacy note.
3. Сделать first-run путь явным: если нет счетов или категорий, OCR не должен быть первым тупиком; сначала "создать счет" и "создать категорию расходов".
4. Разделить "OCR черновик" и "импорт" на уровне словаря, иконок и заголовков.
5. Для partial failure в OCR create drafts показывать per-row status и безопасный retry на idempotency.
6. В production checklist добавить отдельный evidence gate: authenticated OCR smoke на PWA и Android, включая no-data, unsupported file, timeout/rate-limit и offline.

## Что НЕ менять

- Не превращать OCR в автосоздание операций: pending -> review/edit -> confirm должен остаться инвариантом.
- Не добавлять bank API, CSV/Excel/PDF import, SMS/push interception или notification listener в MVP под видом "улучшения OCR".
- Не раскрывать raw OCR text, image bytes, hidden counts или чужие personal данные в ошибках/empty states.
- Не возвращать plan-level progress bar для Planning; progress зафиксирован на allocation-level.
- Не делать OCR главным путем ввода, пока production authenticated smoke не закрыт.
- Не смешивать `shared family report` и `combined viewer overview` в empty/error copy.

## Критерии успеха

- Пользователь без данных видит понятный первый шаг: создать счет, категорию или добавить операцию вручную; OCR не ведет в тупик.
- Все OCR ошибки имеют конкретное recovery action: выбрать другой формат, уменьшить файл, повторить позже, войти снова, добавить вручную.
- Android и PWA используют одинаковые термины: "скриншот", "черновик OCR", "подтвердить", "отклонить"; слово "импорт" не появляется в capture draft flow.
- Android privacy copy соответствует фактической архитектуре OCR.
- Повтор после сбоя создания OCR drafts безопасен и объяснен пользователю через idempotency/no duplicates.
- PWA offline/HTTPS limitation видна как degraded state, а не только как скрытое поведение service worker.
- QA evidence включает скриншоты/логи для no-data, empty, error, loading, offline/degraded, OCR partial failure и successful confirm на обеих платформах.

## Риски и триггеры эскалации

- **P0 escalation:** Android продолжает отправлять скриншот на backend, а release/product copy говорит "on-device without upload".
- **P0 escalation:** OCR доступен в production без authenticated smoke evidence.
- **P1 escalation:** пользователи могут принять aggregate category draft за точную транзакцию/платеж.
- **P1 escalation:** empty/error state раскрывает наличие чужих personal данных или hidden counts.
- **P1 escalation:** повтор OCR после partial failure создает непонятные дубли или выглядит как дубль.
- **P2 escalation:** release notes/status остаются рассинхронизированы и используются как источник дизайн-решений.

## Доказательства, которых не хватает

- Скриншотная матрица Android/PWA по состояниям: first-run, no accounts, no categories, no pending drafts, unsupported image, OCR timeout/unavailable, rate limit, offline, session expired, confirm success.
- Authenticated production OCR smoke на текущем release `20260607T225457Z-819b5815`.
- Явное решение владельца продукта по Android OCR architecture: local-only или backend upload.
- Проверка, что после 401/403/5xx UI не раскрывает private context и дает восстановление.
