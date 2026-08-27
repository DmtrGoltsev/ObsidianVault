---
id: "review-input-n8nagents-docker-plan-reviewer-instructions-v1"
тип: "ревью"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[План_Лаборатория_Docker_Desktop_N8NAgents_v1_2026-08-27]]"]
доказательства: []
теги: ["review-bundle", "review-instructions", "quorum"]
---

# Инструкции десяти независимым reviewer

## Общая задача

Дать максимум обоснованной критики frozen plan. Не улучшать текст молча, не выполнять установку/тесты, не обращаться к VPS/provider, не читать secrets. Проверить hashes до анализа. Каждый reviewer возвращает один JSON, валидный по `09_REVIEW_SCHEMA.json`.

## Роли

| ID | Специализация | Основной фокус |
|---|---|---|
| R1 | Windows/WSL | prerequisites, feature changes, reboot, update/rollback, managed WSL state |
| R2 | Supply chain/license | official acquisition, checksum/signature, image provenance, licensing, version pinning |
| R3 | Isolation/network/privileged | loopback, egress, Docker boundary, mounts, socket, privileged gates, escape/containment |
| R4 | Compose+n8n+PostgreSQL | profiles, health, resources, migrations, n8n exact-version compatibility, persistence |
| R5 | Telegram | long polling, webhook conflict, offsets, retry/rate limit, allowlist, outbound destination |
| R6 | Secrets/PII/logs | secret lifecycle, ACL, Docker control plane, credentials, evidence/log redaction, retention |
| R7 | Persistence/backup | volumes, quiesce, DB+n8n key restore pair, encryption, restore drill, disk growth/recovery |
| R8 | B2r/O5/evidence gates | Linux capability truth, matrices, no-NIC, canaries, evidence binding, false PASS paths |
| R9 | Dirty worktree/touchset/rollback | 21-path custody, line endings, Git objects, planned writes, rollback/destructive boundaries |
| R10 | User operability/resources/recovery | manual UX, resource budget, troubleshooting, owner handover, failure recovery |

Каждый reviewer анализирует весь bundle, но глубже атакует свою область. Reviewer не видит outputs остальных до сдачи собственного результата и должен засвидетельствовать независимость.

## Severity

- `P0`: может привести к потере/раскрытию данных или секретов, compromise host/VPS, необратимой порче, unauthorized external action либо принципиально неверной архитектуре.
- `P1`: блокирует безопасное/воспроизводимое исполнение или делает обязательный outcome недоказуемым.
- `P2`: существенный риск качества/эксплуатации с доступной mitigation.
- `P3`: улучшение ясности, удобства или efficiency без блокировки.

## Verdict

- `GO`: нет блокирующих findings в области reviewer.
- `CHANGES_REQUIRED`: есть исправимые P1/P2 до исполнения.
- `STOP`: подтверждён P0 либо фундаментальная несовместимость выбранного плана A.
- `BLOCKED`: bundle/hash/source недостаточен для честного review. Не использовать как замену критике.

## Обязательные проверки reviewer

1. `07_FULL_PLAN.md` SHA-256 = `a64a14c31b1c6ba87087102edc858d0ed5a336e6dd8f13f191d905207abe9a79`, bytes = `46234`.
2. Все files/sizes/hashes совпадают с `00_MANIFEST.json`.
3. Recomputed content aggregate совпадает с manifest/anchor.
4. Claims отделены от unknown/assumption.
5. Finding содержит evidence, impact, exact resolution и acceptance test.
6. Не включать raw secrets/PII или адрес VPS.
7. Не снижать severity ради достижения GO.

## Quorum policy

- Любой validated P0 блокирует.
- Consensus P0/P1: минимум два независимых релевантных review либо authoritative source.
- GO threshold: минимум 8/10 GO, 0 STOP, 0 P0, 0 consensus-P1.
- Bundle-caused BLOCKED: исправить bundle, заморозить заново и повторить все десять reviews.
- Single disputed P1 предъявляется владельцу отдельно.
- P2/P3 получают reasoned disposition.

Reviewer не утверждает execution, не пишет plan v2 и не изменяет bundle.
