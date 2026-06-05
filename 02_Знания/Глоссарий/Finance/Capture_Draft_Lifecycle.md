---
id: "term-capture-draft-lifecycle"
тип: "термин"
проект: "Finance"
термин: "Capture Draft Lifecycle"
термин_en: "Capture Draft Lifecycle"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance", "capture-drafts", "backend"]
источник: "apps/backend/src/app/capture_drafts/service.py"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Capture_Draft]]"
  - "[[OCR_Pipeline]]"
---

# Capture Draft Lifecycle (Жизненный цикл черновика захвата)

## Определение

**Capture Draft Lifecycle** — полный жизненный цикл OCR-черновика в системе Finance: от распознавания скриншота (Screenshot OCR) через создание draft-записи, редактирование, категоризацию до финального подтверждения (confirm), которое порождает [[Transaction]], или отклонения (discard).

Модуль реализует паттерн **capture → review → confirm/discard**, позволяя пользователю проверить и скорректировать данные, полученные из OCR, перед тем как они станут финансовой транзакцией.

## State Machine

```
         ┌──────────────────────────────────────────┐
         │                                          │
         ▼                                          │
     ┌─────────┐   confirm    ┌───────────┐         │
     │ pending │ ───────────► │ confirmed │         │
     └────┬────┘              └─────┬─────┘         │
          │                         │               │
          │   discard               │ transaction_id│
          ▼                         ▼   привязан    │
     ┌───────────┐            (финальное            │
     │ discarded │             состояние)            │
     └───────────┘                                   │
         ▲                                           │
         │  повторный confirm уже подтверждённого    │
         └───────────────────────────────────────────┘
```

- **pending** — начальное состояние после `create_or_get_existing`. Черновик можно редактировать (`PATCH`) и подтверждать/отклонять.
- **confirmed** — финальное состояние. Привязан `transaction_id`. Повторный `confirm` возвращает существующую запись (идемпотентность), но только если `transaction_id` не `None`.
- **discarded** — финальное состояние. Черновик отклонён, транзакция не создаётся.

**Ограничения переходов:**
- `confirm` и `discard` допустимы **только** из `pending` — иначе `CaptureDraftConflictError` (409).
- `update` (PATCH) допустим **только** из `pending`.

## API Endpoints

Все эндпоинты определены в `router.py` с префиксом `/capture-drafts`.

| HTTP-метод | Путь                          | operationId                          | Назначение                                          |
|------------|-------------------------------|--------------------------------------|-----------------------------------------------------|
| `POST`     | `/screenshot-ocr`             | `recognizeCaptureDraftScreenshotOcr` | Распознавание скриншота через Tesseract OCR         |
| `PUT`      | `/category-mappings`          | `putCaptureDraftCategoryMapping`     | Создание/обновление маппинга OCR-категории          |
| `POST`     | `/`                           | `createCaptureDraft`                 | Создание черновика (idempotent)                     |
| `GET`      | `/`                           | `listCaptureDrafts`                  | Список черновиков текущего пользователя             |
| `PATCH`    | `/{draftId}`                  | `updateCaptureDraft`                 | Частичное обновление черновика (только `pending`)   |
| `POST`     | `/{draftId}/confirm`          | `confirmCaptureDraft`                | Подтверждение: создаёт Transaction                  |
| `POST`     | `/{draftId}/discard`          | `discardCaptureDraft`                | Отклонение черновика                                |

> См. `apps/backend/src/app/capture_drafts/router.py`

## Confirm → Transaction Flow

Подтверждение черновика — ключевая операция, превращающая OCR-данные в финансовую транзакцию. Реализована в `CaptureDraftService.confirm_draft()` (`service.py:159`).

**Шаги:**

1. **Thread-safe захват** — `confirm_draft` выполняется под `RLock` (`self._confirm_lock`), чтобы предотвратить параллельный двойной confirm одного черновика.
2. **Ownership check** — `_require_owned_draft` проверяет, что `actor.user_id == record.owner_user_id`; при несовпадении — `CaptureDraftNotFoundOrInaccessible` (404).
3. **Idempotent confirm** — если `status == "confirmed"` и `transaction_id` задан, запись возвращается как есть.
4. **Валидация обязательных полей:**
   - `account_id` не `None`
   - `category_id` не `None`
   - `description` — непустая строка после `strip()`
   - `amount > 0`
   - При нарушении — `CaptureDraftValidationError` (422), код `CONFIRMATION_FIELDS_REQUIRED`.
5. **Создание Transaction** — формируется `TransactionCreateRequest` (`TransactionType.EXPENSE`, `SourceType.MANUAL`), вызывается `TransactionService.create_transaction()`.
   - `occurred_at` берётся из записи (`record.occurred_at` или fallback `record.captured_at`).
6. **Сохранение** — запись обновляется: `status="confirmed"`, `transaction_id=<id новой транзакции>`, `version` инкрементируется.

**Обработка ошибок Transaction:**
- `TransactionReferencedResourceError` → `CaptureDraftReferencedResourceError` (404)
- `TransactionValidationError` → `CaptureDraftValidationError` (422/409)
- `TransactionConflictError` → `CaptureDraftConflictError` (409)
- `TransactionServiceError` → `CaptureDraftServiceError` (403)

## Category Mapping

`CaptureCategoryMappingService` (`category_mapping_service.py`) решает задачу маппинга внешних OCR-категорий (распознанных текстовых меток) на внутренние категории пользователя.

**Механизм:**
- Внешняя метка (`external_label`) нормализуется и хешируется через `external_label_hash` (SHA-256).
- `upsert_mapping` — создаёт или обновляет связь `external_label_hash → category_id` в контексте `(owner_user_id, household_id)`.
- `lookup_suggested_category_id` — обратный поиск: по внешней метке возвращает `category_id`, если маппинг существует и категория доступна.
- **Валидация категории:** категория должна быть `ACTIVE`, тип `EXPENSE`, и пользователь должен иметь право на чтение (`canReadCategory`). Для personal-контекста — personal-категория владельца; для household — household-категория.
- **Валидация household:** проверяется активное членство через `actor.memberships`.

> Хранение: `apps/backend/src/app/capture_drafts/category_mappings_repository.py`

## Idempotency

Создание черновика реализовано как **create-or-get**:

- Каждый черновик имеет уникальный `idempotency_key` (в рамках `owner_user_id`).
- `repository.create_or_get_existing` сначала ищет существующую запись по паре `(owner_user_id, idempotency_key)`. Если найдена — возвращается она.
- В SQL-реализации используется `IntegrityError` при `flush()` как второй уровень защиты от race condition.
- Поле `evidence_hash` (SHA-256, до 128 символов) позволяет связать черновик с исходным доказательством (скриншотом) без хранения самого файла.

## Scope

- **Household-scoped** — операции учитывают `household_id` из контекста actor.
- **Авторизация** — каждый запрос проходит через `CurrentActor` (FastAPI dependency), извлекающий `Actor` из auth context.
- **Ownership check** — `_require_owned_draft` на каждую операцию с конкретным draft: `record.owner_user_id` должен совпадать с `actor.user_id`.
- **Rate limiting** — OCR-эндпоинт защищён in-memory rate limiter (`SCREENSHOT_OCR_ACTOR_MINUTE`, `SCREENSHOT_OCR_IP_MINUTE`), при превышении — 429.

## Ключевые DTO

Все схемы определены в `apps/backend/src/app/capture_drafts/schemas.py`:

| DTO                                | Назначение                                                    |
|------------------------------------|---------------------------------------------------------------|
| `CaptureDraftCreateRequest`        | Тело запроса на создание черновика                            |
| `CaptureDraftUpdateRequest`        | Тело PATCH-запроса (все поля опциональны)                     |
| `CaptureDraftDto`                  | Полное представление черновика в ответе API                   |
| `CaptureDraftEnvelope`             | Обёртка `{"data": CaptureDraftDto}`                           |
| `CaptureDraftPageEnvelope`         | Пагинированный список + `PageInfo`                            |
| `ScreenshotOcrResponseDto`         | Результат OCR-распознавания: список кандидатов + warnings     |
| `ScreenshotOcrEnvelope`            | Обёртка для OCR-ответа                                        |
| `CategoryAggregateDto`             | Агрегат распознанной категории (`external_label`)             |
| `CaptureCategoryMappingPutRequest` | Запрос на создание/обновление маппинга категории              |
| `CaptureCategoryMappingDto`        | Результат маппинга в ответе API                               |
| `CaptureDraftRecord`               | Внутренняя запись (frozen dataclass), `repository.py`         |
| `CaptureDraftCreateValues`         | Значения для создания записи (без генерируемых полей)         |

**Перечисления:**
- `CaptureDraftStatus`: `pending`, `confirmed`, `discarded`
- `CaptureSource`: `screenshot`

## Связанные термины

- [[Capture_Draft]] — сущность черновика захвата
- [[OCR_Pipeline]] — пайплайн распознавания скриншотов
- [[Transaction]] — финансовая транзакция, создаваемая при confirm
- [[Category]] — категория расходов, на которую маппятся OCR-метки
- [[Account]] — счёт, к которому привязывается подтверждённая транзакция

## Источник

- `apps/backend/src/app/capture_drafts/service.py` — бизнес-логика (`CaptureDraftService`)
- `apps/backend/src/app/capture_drafts/router.py` — API-эндпоинты
- `apps/backend/src/app/capture_drafts/repository.py` — data access (`CaptureDraftRepository`)
- `apps/backend/src/app/capture_drafts/schemas.py` — DTO и перечисления
- `apps/backend/src/app/capture_drafts/category_mapping_service.py` — маппинг категорий (`CaptureCategoryMappingService`)
- `apps/backend/src/app/capture_drafts/category_mappings_repository.py` — хранение маппингов
