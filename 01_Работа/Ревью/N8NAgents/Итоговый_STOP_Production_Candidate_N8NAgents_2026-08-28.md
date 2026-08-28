---
id: "n8nagents-final-stop-production-candidate-2026-08-28"
тип: "ревью"
статус: "заблокировано"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-28"
обновлено: "2026-08-28"
уверенность: "высокая"
источники:
  - "[[Итог_Production_Candidate_Track_D_2026-08-28]]"
  - "[[Production_Candidate_Rebaseline_2026-08-27]]"
доказательства:
  - "C:/Users/style/Documents/ChatGPT/N8NAgents-production-artifacts/attempt2-final-d8e43cb/release-evidence.md"
  - "C:/Users/style/Documents/ChatGPT/N8NAgents-production-artifacts/attempt2-final-d8e43cb/N8NAgents-d8e43cb-run1.tar.gz"
  - "C:/Users/style/Documents/ChatGPT/N8NAgents-production-artifacts/attempt2-final-d8e43cb/N8NAgents-d8e43cb-run2.tar.gz"
теги: ["n8n", "production-candidate", "stop", "p1", "vps-security"]
---

# Итоговый STOP — production candidate N8NAgents

## Решение

**Production rollout заблокирован.** Локальный финальный кандидат и все локальные gates имеют `PASS`, однако финальное независимое переревью дало **2 GO** (workflows/DB и secrets/DR) и **1 STOP** (VPS security). Единственный незакрытый P1 требует новой авторизации владельца: по H7 две корректирующие попытки уже исчерпаны; третью целевую попытку нельзя начинать без нового явного разрешения.

## Идентичность кандидата и локальное доказательство

| Поле | Значение |
|---|---|
| Финальный commit | `d8e43cb748724749c6da8576d2b20ad1e682a2ab` |
| Git tree | `f8d84ff4e8df77eade316526e2792a00d1c26110` |
| Архив | `N8NAgents-d8e43cb-run1.tar.gz` и независимый повтор `run2` |
| SHA-256 обоих архивов | `1630b8451fefa043a4b0009bda5a0267738e5ad55b35fae0baf076fcf8ef2b1e` |
| Состав архива | 140 файлов |
| Локальные gates | `PASS` |

Локальные артефакты и сводка проверок: `C:/Users/style/Documents/ChatGPT/N8NAgents-production-artifacts/attempt2-final-d8e43cb/`; исходный exact-commit worktree: `C:/Users/style/Documents/ChatGPT/N8NAgents-production-candidate/N8NAgents/`. Более ранний baseline и границы запуска зафиксированы в [[Production_Candidate_Rebaseline_2026-08-27]].

## Единственный P1

В `deploy.sh` durable `previous/current` mode и symlink `current` переключаются **до** `consume_public_edge_approval`. Если consume завершается ошибкой либо процесс получает `TERM`, service rollback выполняется, но durable state и symlink `current` не восстанавливаются. В результате bootstrap-services могут остаться с public state и, возможно, с уже потреблённым approval.

Это относится к VPS security; оно не отменяет локальный `PASS`, но делает production activation небезопасной.

## Что не выполнялось

- VPS после read-only baseline не менялся.
- Deploy не выполнялся.
- Внешние Telegram- и DeepSeek-вызовы не выполнялись.
- Исправление P1, третья попытка и fault injection **не выполнялись**.

## Минимальный следующий шаг после новой авторизации

Целевое исправление: сделать порядок транзакционным — либо переносить durable switch до успешного consume, либо при ошибке/`TERM` атомарно откатывать durable mode, `current` symlink и состояние approval. Добавить fault-injection тест в интервале между switch и consume, доказывающий отсутствие сохранённого public state и некорректно consumed approval. После этого повторить независимое VPS-security review exact нового commit/archive.

До такой авторизации и успешного переревью сохраняется `STOP`: никаких production deploy, public edge/DNS activation, credential binding, Telegram traffic или DeepSeek spend.

## Связи

- [[Итог_Production_Candidate_Track_D_2026-08-28]]
- [[Production_Candidate_Rebaseline_2026-08-27]]
- [[N8NAgents]]
