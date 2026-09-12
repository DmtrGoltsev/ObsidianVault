---
id: "term-transaction"
тип: "термин"
проект: "Finance"
термин: "Transaction"
термин_en: "Transaction"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
теги: ["глоссарий", "finance", "домен"]
источник: "docs/architecture/domain-model.md"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Transfer]]"
  - "[[Personal_Shared]]"
---

# Transaction (операция)

**Определение:** Финансовая операция в системе. Типы:
- **income** — доход
- **expense** — расход
- **transfer** — перевод между счетами
- **brokerage** — брокерская операция

Атрибут `sourceType` имеет значение `manual` для операций, введённых вручную. Может быть personal (привязана к personal-счёту) или shared (привязана к shared-счёту).

**Связанные термины:**
- [[Transfer]] — частный случай операции (перевод)
- [[Personal_Shared]] — определяет видимость операции
- [[Capture_Draft]] — черновик, из которого может быть создана операция

**Источник:** `docs/architecture/domain-model.md`
