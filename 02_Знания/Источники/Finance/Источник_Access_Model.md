---
id: "source-access-model"
тип: "источник"
проект: "Finance"
название: "Источник — Access Model"
файл: "docs/architecture/access-model.md"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["источник", "finance"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Finance]]"
---

# Источник — Access Model

## Файл-источник

`docs/architecture/access-model.md`

## Содержит

Модель доступа Finance — принципы авторизации, CRUD-матрица прав (actor × resource × action), правила visibility и scope isolation.

## Ключевые данные

- Личные (personal) и общие (shared) scope; ownership определяет видимость ресурсов
- Принцип filter-before-aggregate: данные фильтруются по правам до агрегации в analytics
- Neutral responses: при отсутствии прав возвращается пустой результат (не 403), чтобы не раскрывать существование ресурсов
