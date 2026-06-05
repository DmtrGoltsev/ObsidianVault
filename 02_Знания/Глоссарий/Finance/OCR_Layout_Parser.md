---
id: "term-ocr-layout-parser"
тип: "термин"
проект: "Finance"
термин: "OCR Layout Parser"
термин_en: "OCR Layout Parser"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/capture_drafts/aggregate_parser.py"
ссылки:
  - "[[MOC_Finance]]"
---

Парсер агрегированных строк расходов из OCR-скриншота. Использует layout-aware эвристику с двухколоночной разбивкой (label слева, amount справа) для извлечения категорий и сумм.

## Ключевые аспекты

- **Двухколоночная эвристика**: `_right_column_left()` — разделение на 58% ширины; label = левая часть, amount = правая
- **Layout-линии**: OCR-слова группируются по Y-координате в `_LayoutLine` с bounding box
- **Fallback**: text-based парсинг через regex (`_AMOUNT_AFTER_RE`, `_AMOUNT_BEFORE_RE`) при отсутствии word-coordinates
- **Дедупликация**: по нормализованному ключу (label, amount, operation_count)
- **Edge cases**: multi-line labels, split operation count (number + «операций» на разных строках), noise trimming

## Связанные термины

- [[Capture_Category_Mapping]] — маппинг распознанных меток на категории
- [[Screenshot_Source]] — источник данных для парсера
- [[Money]] — формат распознанных сумм
