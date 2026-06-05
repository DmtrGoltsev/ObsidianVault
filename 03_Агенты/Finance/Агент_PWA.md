---
id: "agent-finance-pwa"
тип: "агент"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["агент", "finance", "pwa", "frontend"]
ссылки:
  - "[[MOC_Finance]]"
---

# Агент PWA — Finance

## Зона ответственности

Веб-клиент (PWA): OCR capture UI, draft confirmation flow, service worker (offline),
навигация, адаптивная вёрстка. iOS-сборка через Capacitor.

## Стек

- React 19, Vite 7, TypeScript 5.9
- Capacitor 8 (iOS native shell)
- Vitest, Playwright (e2e)

## Права на решения

- Изменение `apps/web-pwa/` (components, hooks, services, workers, assets)

## Активные задачи

- [ ] Capture UI для фото чеков
- [ ] Draft confirmation flow
- [ ] Service Worker: offline-first стратегия
- [ ] iOS build через Capacitor

## Связанные заметки

- [[MOC_Finance]]
- [[Finance]]
