---
id: "term-report"
тип: "термин"
проект: "Finance"
термин: "Отчёт"
термин_en: "Report"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/reports/"
ссылки:
  - "[[MOC_Finance]]"
---

Агрегированный финансовый отчёт по счетам, категориям и транзакциям. Строится на основе предварительно отфильтрованных (filter-before-aggregate) видимых ресурсов с учётом scope actor'а.

## Ключевые аспекты

- **Режимы**: `shared_family_report` — только shared-ресурсы household; `combined_viewer_overview` — personal + shared
- **Filter-before-aggregate**: сначала `context()` фильтрует видимые accounts и categories, затем `visible_report_transactions()` — транзакции, затем агрегация
- **Виды отчётов**: summary totals, category breakdown, expenses by category, account balances, balance groups, net worth, cash flow, transaction drill-down
- **Bucketing**: `day` / `month` — группировка по периоду для cash flow
- **Authz**: `canReadReport` проверяет режим + household_id; `_record_is_inside_visible_report_scope` — каждая транзакция

## Связанные термины

- [[Scope_Isolation]] — filter-before-aggregate
- [[Account]] — балансы и группы
- [[Category]] — breakdown по категориям
- [[Money]] — формат сумм в отчётах
- [[Membership]] — доступ к shared_family_report
