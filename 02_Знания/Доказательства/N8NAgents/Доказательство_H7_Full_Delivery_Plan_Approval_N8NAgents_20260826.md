---
id: "evidence-n8nagents-h7-full-delivery-plan-approval-20260826"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-26"
обновлено: "2026-08-26"
уверенность: "высокая"
источники:
  - "Явное plan-level утверждение пользователя в текущем диалоге"
  - "[[Доказательство_H6_Third_Stop_Packaging_Incident_N8NAgents_20260826]]"
  - "[[Доказательство_H1_Phase_A_User_Approval_N8NAgents_20260826]]"
  - "[[Доказательство_H3_Phase_A_Reapproval_N8NAgents_20260826]]"
  - "[[Доказательство_H5_Phase_A_Recovery_Approval_N8NAgents_20260826]]"
доказательства: []
теги: ["n8n", "full-delivery", "approval", "governance", "phase-a", "budget", "rollback"]
---

# H7 — plan-level утверждение N8NAgents Full Delivery v1

## Идентификатор и состояние

- `AUTHORIZATION_ID=N8NAgents-FULL-DELIVERY-v1`.
- `PLAN_VERSION=1`.
- Время фиксации: `2026-08-26`, `Europe/Moscow`.
- Execution kickoff: **ACTIVE**.
- Outcome: **PENDING**. Это approval evidence, а не доказательство выполненного deployment, E2E, backup/restore или security hardening.

## Точное утверждение пользователя

Пользователь утвердил N8NAgents Full Delivery v1 целиком, включая завершение текущего Phase A, `plaintext swap 2 GiB`, перечисленные обратимые изменения VPS, Docker, PostgreSQL, n8n, Caddy, firewall, SSH, workflows, backup и monitoring, будущие исправляющие commits, не более двух retries на gate после тестов и независимого `GO`, автоматический недеструктивный rollback, DeepSeek-трафик до `5 USD` и до `20` тестовых Telegram-сообщений только в allowlisted test chat. Пользователь не требует подтверждения каждого шага или commit.

## Разрешённая baseline и границы исполнения

- Baseline Phase A: final independently reviewed commit `9e024c3f5f2aba9d3727e0a26ffb7a6fc8e3147b`.
- Swap: `plaintext-2g` / plaintext swap `2 GiB`.
- Разрешены будущие исправляющие commits в пределах утверждённой архитектуры и максимум два reviewed retries на gate.
- При stop condition разрешён только автоматический **недеструктивный** rollback: остановка нездоровых контейнеров, возврат к последнему known-good release и восстановление конфигурации из immutable snapshot. Данные и volumes автоматически не удаляются.
- До результата каждого gate сохраняются обязательные проверки и независимое `GO`; approval не отменяет stop/kill conditions и не превращает исторические или непроверенные факты в `PASS`.

## Ручные gates, не переданные автоматизации

Пользователь сохранил ручные gates только для:

1. секретов;
2. DNS/provider UI;
3. owner/2FA;
4. destructive/data-loss действий;
5. новых получателей;
6. дополнительных расходов;
7. расширения scope.

Нужные ручные входы остаются: домены, timezone и ACME email; актуальная сверка VPS в Hexcore и provider firewall/IPv6; DNS у регистратора при отсутствии доступа; Telegram bot token и DeepSeek API key через прямой ввод в n8n; numeric Telegram user/chat allowlist; owner и 2FA; backup destination, retention, RPO/RTO и публичный ключ шифрования; свежая проверка web-консоли перед SSH hardening. Секреты и персональные identifiers в Vault не записываются.

## Явные исключения, требующие нового решения

Approval не разрешает удаление данных или volumes, restore поверх production, переустановку ОС, смену VPS/тарифа, покупки, превышение бюджета, новых получателей, новые типы данных или расширение архитектуры.

## Историческая цепочка approvals

H1 (`d1703bdfbdb183836afe7d75c871938ca8a9f196`), H3 (`f6e0c745ab889c11df1ab83ccf7957534be600cd`) и H5 (`bae8c88f7a7d153ffc4a5ae28028045a0a27d319`) сохраняются immutable historical SHA approvals; они не переписываются и не используются как approval нового baseline. H7 заменяет только текущий execution authority в границах Full Delivery v1.

`[[Доказательство_G1_User_Accepted_TOFU_Exception_N8NAgents]]` остаётся **`NOT VERIFIED — USER-ACCEPTED-EXCEPTION`**. H7 не подтверждает fingerprint и не отменяет его security gate.

## Связанные заметки

- [[Доказательство_H6_Third_Stop_Packaging_Incident_N8NAgents_20260826]]
- [[Журнал_Автономной_Работы_N8NAgents]]
- [[Очередь_Ручных_Действий_N8NAgents]]
- [[Задача_Развертывание_N8NAgents]]
- [[MOC_N8NAgents]]
