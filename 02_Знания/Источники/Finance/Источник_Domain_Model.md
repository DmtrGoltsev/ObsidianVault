---
id: "source-domain-model"
тип: "источник"
проект: "Finance"
название: "Источник — Domain Model"
файл: "docs/architecture/domain-model.md"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["источник", "finance"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
---

# Источник — Domain Model

## Файл-источник

`docs/architecture/domain-model.md`

## Содержит

Доменную модель Finance — описание всех сущностей MVP, их связей (cardinality), инвариантов и правил ownership/visibility.

## Ключевые данные

- Основные сущности: User, Household, Membership, Account, Transaction (Operation), Category, Icon, ReportPeriod, AnalyticsView
- Описаны связи и cardinality между сущностями (раздел "Связи и cardinality")
- Зафиксированы правила Ownership и visibility, инварианты и Post-MVP расширения
