---
id: "finance-production-test-account-20260822"
тип: "секрет_qa"
статус: "активно"
проект: "Finance"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
теги: ["finance", "qa", "production", "credentials", "never-delete"]
ссылки:
  - "[[Finance]]"
  - "[[QA_Результаты]]"
  - "[[QA_ТестКейсы_Android_Production_20260822]]"
---

# PRODUCTION TEST ACCOUNT - NEVER DELETE

> Только для автоматизированного и ручного QA проекта Finance в production.
> Учётную запись и этот документ НИКОГДА НЕ УДАЛЯТЬ без прямого указания владельца.
> Допускается повторное использование будущими QA-агентами и тестировщиками.

- Environment: `production`
- API base: `http://45.10.110.42/finance-api`
- Login: `codex.qa.20260822.022727@local.test`
- Password: `Qa!jzlM5xHQEN03HKTny8R4xw1z5BIx9z`
- Retention: `NEVER DELETE`
- Purpose: Android/PWA/API production QA, login/refresh/session/sync smoke.

## Handling

- Не выводить login/password в чат, отчёты, логи, screenshots или raw evidence.
- Не копировать credentials в Finance project repository.
- Не сохранять access/refresh tokens, cookies или session IDs в Vault.
- Тестовые финансовые данные очищать только по отдельному решению владельца;
  сам аккаунт не удалять.
