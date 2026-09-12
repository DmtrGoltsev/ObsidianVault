---
id: "review-input-n8nagents-docker-plan-context-v1"
тип: "ревью"
статус: "на_ревью"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-27"
обновлено: "2026-08-27"
уверенность: "высокая"
источники: ["[[Источник_Мастер_Промпт_N8NAgents]]", "[[Доказательство_R8_K4R_Offline_v2_Blocked_N8NAgents_20260827]]"]
доказательства: []
теги: ["review-bundle", "constraints", "security"]
---

# Контекст и ограничения ревью

## Product baseline

Production target остаётся Linux `amd64` VPS с Docker Compose, PostgreSQL, n8n Community, Caddy, Telegram и DeepSeek. Локальная лаборатория предназначена для разработки, Linux QA, workflow import/live spikes, реального ограниченного Telegram dev testing и owner handover. Она не заменяет production gates.

## Security baseline из мастер-промпта

- Никаких секретов в Git, Vault, exports, logs, screenshots и чат.
- Раздельные dev/prod Telegram bots; production webhook и local polling не смешиваются.
- Unauthorized identity отклоняется до LLM, memory и tools.
- LLM не получает generic SQL/shell/filesystem/unrestricted HTTP/Docker/admin capabilities.
- Отдельные PostgreSQL boundaries и least-privilege roles.
- Постоянный `N8N_ENCRYPTION_KEY`; DB backup и instance key образуют restore pair.
- Не обещать exactly-once; доказывать bounded effectively-once cases.
- No `latest`; exact platform/digests после compatibility check.
- Не объявлять общий успех без evidence.

## Governance

- Frozen v1 не редактируется после раздачи reviewer.
- Текущий цикл только documentation/review: Windows, Docker, project repo и VPS не меняются.
- Любой confirmed P0 блокирует.
- План B, VPS testing и публичный edge исключены.
- Любое destructive действие, новый recipient, secret input, расход или scope expansion остаются manual gate.
- Reviewer должен отличать `PASS`, `FAIL`, `BLOCKED`, `MANUAL-PASS`; отсутствие capability не превращается в PASS.

## Исторические полномочия и их предел

Владелец ранее утвердил Full Delivery v1 для production в пределах обратимых действий, двух retries/gate, ограниченного DeepSeek/Telegram тестового бюджета и ручных gates. Remote K4 retries позже исчерпаны. Это не является автоматическим approval установки Docker Desktop или нового local real-traffic cycle. Текущий план обязан получить решение владельца после десяти reviews.

## Evidence baseline

- Host static/parsing/package tests имеют локальное evidence.
- Linux B2r/O5 execution не завершено.
- Initial two-engine semantics не принято reviewers из-за provenance/containment gaps.
- Последний B2r terminal: `BLOCKED` до validator start, без candidate/commit.
- Dirty draft сохраняется; reviewer не должен требовать его commit как условие чтения плана.
