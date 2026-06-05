---
id: "evidence-finance-pwa-ios-qa"
тип: "доказательство"
проект: "Finance"
статус: "утверждено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["доказательство", "finance", "pwa", "ios", "qa"]
ссылки:
  - "[[MOC_Finance]]"
---

# PWA / iPhone Final QA — Production

## Что доказывается

PWA Finance MVP в Safari/iPhone browser на production (`808f7278`) проходит финальный QA. Подтверждены: login/logout, accounts/assets CRUD, categories add/edit, income/expense/transfer, reports modes (Личное/Общее/Обзор), brokerage/investment API smoke. PWA service worker на plain HTTP IP — environmental limitation, не code HOLD.

## Метод проверки

Device testing: Safari browser на iPhone против production backend `45.10.110.42`. Проверены layout, manifest, health endpoints, import placeholder fixture. Desktop layout scan подтверждён.

## Результат

Проверки пройдены. PWA/iPhone GO подтверждён. Service worker и PWA install требуют HTTPS/domain — documented limitation.

## Артефакты

| Тип | Путь |
|-----|------|
| PWA/iPhone final QA report | `MVP_EVIDENCE/prod-qa-20260519-040710/pwa-iphone-final/prod-pwa-iphone-final-qa-report.md` |
| iPhone layout scan | `MVP_EVIDENCE/prod-qa-20260519-040710/pwa-iphone-final/data/iphone-layout-scan.json` |
| Health check | `MVP_EVIDENCE/prod-qa-20260519-040710/pwa-iphone-final/data/health.json` |
| Manifest summary | `MVP_EVIDENCE/prod-qa-20260519-040710/pwa-iphone-final/data/manifest-summary.json` |

## Связанные заметки

- [[Доказательство_Production_GO]]
- [[Доказательство_Android_QA]]
