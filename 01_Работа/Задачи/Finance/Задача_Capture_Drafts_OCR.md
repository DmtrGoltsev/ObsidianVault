---
id: "task-finance-capture-drafts-ocr"
тип: "задача"
проект: "Finance"
статус: "выполнено"
создано: "2026-06-05"
обновлено: "2026-06-05"
уверенность: "высокая"
теги: ["задача", "finance", "ocr", "capture"]
ссылки:
  - "[[MOC_Finance]]"
  - "[[Задача_Wave1_MVP]]"
---

# Задача: OCR Capture Drafts

## Цель

Реализовать user-initiated OCR capture чеков/скриншотов: on-device Android (ML Kit), server-side Tesseract (PWA/iOS), layout-aware parser, category mappings.

## Контекст

- **Ветка**: `codex/auto-capture-drafts`
- Flow: пользователь выбирает скриншот → OCR → preview → confirm/edit → transaction
- Android: on-device OCR без загрузки скриншота на сервер
- PWA/iOS: временная загрузка на self-hosted backend OCR endpoint
- Скриншоты и raw OCR text не сохраняются; транзакция создаётся только после confirm/edit

## Definition of Done

- [x] On-device OCR на Android (ML Kit)
- [x] Server-side OCR для PWA/iOS (Tesseract)
- [x] Layout-aware parser для извлечения данных
- [x] Category mappings на основе распознанных данных
- [x] 9 миграций БД
- [x] Тесты и edge cases обработаны
- [x] Скриншоты/raw OCR не персистятся

## Статус

**Выполнено** — реализовано и интегрировано в MVP.

## Доказательства

- Ветка `codex/auto-capture-drafts` смержена
- Тесты в CI проходят

## Связанные заметки

- [[Задача_Wave1_MVP]]
- [[MOC_Finance]]
