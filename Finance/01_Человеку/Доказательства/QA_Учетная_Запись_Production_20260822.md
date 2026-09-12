---
id: "finance-production-qa-account-locator"
тип: "доказательство"
статус: "ограниченный доступ"
проект: "Finance"
владелец: "owner"
создано: "2026-08-22"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["QA_Результаты", "Регламент_Деплоя_Finance"]
доказательства: []
теги: ["finance", "qa", "production", "credential-locator", "never-delete"]
---

# Finance production QA account locator

Persistent production test account: `NEVER DELETE`.

Credential values are prohibited in Git, Obsidian, task chat, logs, screenshots,
test evidence and build artifacts.

## Approved locators

- Automation: GitHub Environment `production`, secret names
  `FINANCE_QA_EMAIL` and `FINANCE_QA_PASSWORD`.
- Owner-local recovery: DPAPI locator `Finance/production-qa-credential`.

Only the locator names may be copied into QA instructions. Values are entered or
consumed directly from the approved secret store and must never be printed.

## Incident note

The earlier plaintext record was treated as compromised on 2026-08-24. Its
reachable public history must be cleaned under an owner-approved history rewrite.
The account remains present. Its credential was rotated through the approved
security workflow, all active pre-rotation sessions were revoked, and the old
credential was independently confirmed invalid. No deployment, migration or
backend restart was performed during rotation.
