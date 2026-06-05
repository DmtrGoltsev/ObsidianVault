---
id: "adr-finance-0004"
тип: "решение"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["ADR", "finance", "архитектура", "capture", "lifecycle"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[ADR_0003_OCR_Architecture]]"
  - "[[ADR_0005_Scope_Isolation]]"
---

# ADR-0004: Жизненный цикл Capture Drafts

## Статус

Утверждено. Реализовано в `apps/backend/src/app/capture_drafts/`.

## Контекст

Пользователь Finance может создать транзакцию из скриншота через OCR-распознавание. Однако распознанный результат может содержать ошибки (неправильная сумма, категория, merchant). Автоматическое создание транзакции без подтверждения неприемлемо — финансовые данные требуют явного consent пользователя.

Система также должна предотвращать дублирование: пользователь может повторно отправить один и тот же скриншот, а network retries могут дублировать запросы.

## Решение

### State machine: `pending` → `confirmed` | `discarded`

```
pending ──confirm──→ confirmed (создаёт Transaction)
pending ──discard──→ discarded
```

Три статуса (`CaptureDraftStatus`):

- **`pending`** — начальный. Черновик создан, ожидает пользовательского подтверждения. Доступен для редактирования (update).
- **`confirmed`** — пользователь подтвердил. Создана связная `Transaction`, `transaction_id` записан в draft. Статус терминальный — повторный confirm возвращает существующую запись.
- **`discarded`** — пользователь отклонил. Статус терминальный. Транзакция не создаётся.

### User-initiated capture

Все capture drafts инициируются пользователем (выбор скриншота). Нет auto-capture, нет background scanning, нет interception уведомлений.

`CaptureSource` = `screenshot` — единственный источник в MVP.

### Idempotent create-or-get

`create_draft` использует `idempotency_key` (генерируется клиентом на основе evidence hash + time bucket). Метод `create_or_get_existing` в репозитории:

- Если draft с таким `idempotency_key` уже существует — возвращает существующую запись без создания дубликата.
- Если нет — создаёт новый draft.

Это обрабатывает network retries и повторные отправки одного скриншота.

### Confirm с валидацией и транзакцией

`confirm_draft` выполняется под `RLock` для thread safety:

1. Проверяет ownership (`owner_user_id == actor.user_id`).
2. Проверяет, что статус `pending` (иначе `CaptureDraftConflictError`).
3. Валидирует обязательные поля: `account_id`, `category_id`, `description`, `amount > 0`.
4. Создаёт `TransactionCreateRequest` (`source_type=MANUAL`, `transaction_type=EXPENSE`).
5. Вызывает `TransactionService.create_transaction()` — полная authz-проверка через predicates.
6. Сохраняет draft с `status="confirmed"` и `transaction_id`.

### Ownership isolation

Каждый draft принадлежит одному `owner_user_id`. Все операции (`list_drafts`, `update_draft`, `confirm_draft`, `discard_draft`) проверяют ownership. Не-owner не может прочитать, изменить или подтвердить чужой draft — получает neutral `CaptureDraftNotFoundOrInaccessible`.

## Альтернативы

1. **Auto-confirm** — отклонено. OCR может ошибаться; неподтверждённые финансовые транзакции неприемлемы.
2. **Separate queue / async processing** — отклонено для MVP. Добавляет infrastructure complexity. Synchronous confirm достаточно для текущего масштаба.
3. **Manual-only (без OCR)** — отклонено. OCR-захват — ключевая feature, но результат всегда проходит через user confirmation.

## Последствия

### Положительные

- Явное подтверждение пользователем — никакая OCR-ошибка не создаёт транзакцию автоматически.
- Idempotency предотвращает дубли при retries.
- Thread-safe confirm (`RLock`) предотвращает race conditions при параллельных confirm-запросах.
- Ownership isolation — пользователи не видят чужие drafts.

### Издержки

- Два шага вместо одного (create + confirm) — дополнительный API round trip.
- Pending drafts накапливаются, если пользователь не подтверждает — требуется cleanup/review стратегия.
- `RLock` — in-process lock, не распределённый. Для multi-instance deployment потребуется DB-level locking (`SELECT FOR UPDATE`).

## Ссылки

- `apps/backend/src/app/capture_drafts/service.py` — `CaptureDraftService`, state machine, confirm logic
- `apps/backend/src/app/capture_drafts/schemas.py` — `CaptureDraftStatus`, DTOs, `ScreenshotOcrCandidateDto`
- `apps/backend/src/app/capture_drafts/repository.py` — `CaptureDraftRepository`, `create_or_get_existing`
- `apps/backend/src/app/capture_drafts/router.py` — API endpoints
