---
id: "term-transfer"
тип: "термин"
проект: "Finance"
термин: "Transfer"
термин_en: "Transfer"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
теги: ["глоссарий", "finance", "домен"]
источник: "docs/architecture/domain-model.md"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Transaction]]"
  - "[[Personal_Shared]]"
---

# Transfer (перевод)

**Определение:** Операция перевода средств между двумя счетами. Типы переводов:
- **personal_same_owner** — перевод между собственными счетами одного пользователя (personal → personal)
- **household_same_household** — перевод между счетами в рамках одного household (shared → shared)

Инвариант: same-scope transfers — переводы только в одном скоупе (personal ↔ personal, shared ↔ shared).

**Связанные термины:**
- [[Transaction]] — родительский тип операции
- [[Personal_Shared]] — определяет скоуп перевода

**Источник:** `docs/architecture/domain-model.md`
