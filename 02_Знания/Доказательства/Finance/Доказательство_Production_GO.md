---
id: "evidence-finance-production-go"
тип: "доказательство"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["доказательство", "finance", "production", "mvp"]
ссылки:
  - "[[MOC_Finance]]"
---

# Production MVP Functional GO (2026-05-19)

## Что доказывается

Production MVP Finance получил **functional GO** 2026-05-19 для iPhone/browser и Android. Deployed commit: `808f7278` (`808f7278a7cc29aaf6f179adb22b61ffdc6fa06a`). Backend release path: `/opt/finance/releases/20260519T010232Z-808f7278`. Frontend: `/var/www/finance/releases/20260519T010232Z-808f7278`. Tag `v0.1.0-mvp` alignment — open, требует owner approval.

## Метод проверки

Production QA на deployed instance (HexCore, `45.10.110.42`). Финальный production-отчёт подтверждает: login/logout, accounts/assets, categories, income/expense/transfer, reports (personal/shared/overview), brokerage/investment API smoke. Backend health: OK. DB migration: Alembic `20260519_0006 (head)`.

## Результат

GO подтверждён для iPhone/browser и Android. Не является full security GO — CVE/HTTPS/backup/restore proofs остаются open follow-up.

## Артефакты

| Тип | Путь |
|-----|------|
| Финальный production-отчёт | `MVP_EVIDENCE/prod-final-20260519/FINAL_PROD_MVP_REPORT.md` |
| Release report | `MVP_EVIDENCE/MVP_RELEASE_REPORT.md` |
| Commit hash | `808f7278a7cc29aaf6f179adb22b61ffdc6fa06a` |
| Tag | `v0.1.0-mvp` → `94d2484a74131f53badf0cd83610b925770fb710` |

## Связанные заметки

- [[Доказательство_Android_QA]]
- [[Доказательство_PWA_iOS_QA]]
- [[Доказательство_MVP_Release]]
