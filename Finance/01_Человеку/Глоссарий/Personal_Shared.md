---
id: "term-personal-shared"
тип: "термин"
проект: "Finance"
термин: "Personal / Shared"
термин_en: "Personal / Shared"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
теги: ["глоссарий", "finance", "домен", "privacy"]
источник: "docs/architecture/access-model.md"
ссылки:
  - "[[MOC_Finance]]"
  - "[[Household]]"
---

# Personal / Shared (личное / совместное)

**Определение:** Базовое разделение данных в системе Finance:
- **Personal** — данные, принадлежащие одному пользователю. Доступны только владельцу (owner-only).
- **Shared** — данные, принадлежащие household. Доступны всем активным членам household (active members only).

Применяется к счетам (Account), категориям (Category), операциям (Transaction). Инвариант: personal owner-only, shared active-only.

**Связанные термины:**
- [[Household]] — семейное пространство для shared-данных
- [[Transaction]] — операция (может быть personal или shared)

**Источник:** `docs/architecture/access-model.md`
