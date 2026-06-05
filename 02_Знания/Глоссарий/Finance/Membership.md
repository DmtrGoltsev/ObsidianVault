---
id: "term-membership"
тип: "термин"
проект: "Finance"
термин: "Членство"
термин_en: "Membership"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["глоссарий", "finance"]
источник: "apps/backend/src/app/domain/entities.py, apps/backend/src/app/domain/enums.py"
ссылки:
  - "[[MOC_Finance]]"
---

Членство пользователя в household — связь «пользователь ↔ домохозяйство» с конечным автоматом статусов. Определяет доступ к shared-ресурсам.

## Ключевые аспекты

- **Статусы**: `invited` → `active` → `left` / `revoked` — enum `MembershipStatus`
- **Доменная сущность**: `Membership` в `domain/entities.py` — frozen dataclass с `user_id`, `household_id`, `status`
- **Actor context**: членства загружаются в `Actor.memberships` для авторизации каждого запроса
- **Проверка active membership**: `_is_active_household_member()` — используется в accounts, categories, capture для валидации доступа к household-ресурсам

## Связанные термины

- [[Scope_Isolation]] — определяет видимость shared-ресурсов
- [[Account]] — shared-счета привязаны к household через membership
- [[Category]] — household-категории доступны через membership
- [[Report]] — shared_family_report требует active membership
