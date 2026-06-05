---
id: "term-money"
тип: "термин"
проект: "Finance"
термин: "Money"
термин_en: "Money Value Object"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/domain/money.py"
ссылки:
  - "[[MOC_Finance]]"
---

Value object для денежных сумм. Инкапсулирует `Decimal` amount + ISO 4217 currency code. Строго запрещает float, ограничивает дробность до 6 знаков, валидирует формат wire-string.

## Ключевые аспекты

- **Запрет float**: `parse_money_decimal()` выбрасывает `TypeError` при передаче float — защита от binary rounding
- **MAX_MONEY_SCALE = 6**: максимальная дробность (микро-единицы), валидация через regex `DecimalString`
- **Money dataclass**: frozen, slots; `from_wire()` — фабрика с валидацией currency (`^[A-Z]{3}$`)
- **Wire format**: `decimal_to_wire()` — форматирование Decimal в строку для API (`format(value, "f")`)
- **PostgreSQL**: суммы хранятся как `NUMERIC` без потери точности; API использует `DecimalString` (max_digits=24, decimal_places=6)

## Связанные термины

- [[Account]] — `initial_balance`, `current_balance`
- [[Report]] — агрегация сумм по currency
- [[OCR_Layout_Parser]] — парсинг сумм из OCR
