---
id: "finance-release-native-ios-current-parity-20260822"
тип: "доказательство"
статус: "частично готово"
проект: "Finance"
владелец: "finance-team"
создано: "2026-08-22"
обновлено: "2026-08-23"
уверенность: "высокая"
источники:
  - "docs/current-status.md"
  - "docs/testing/ios-native-parity-qa-test-model.md"
доказательства:
  - "MVP_EVIDENCE/native-ios-current-parity-20260822/SUMMARY_SANITIZED.md"
теги: ["finance", "ios", "native", "release", "qa", "swiftdata", "security"]
ссылки:
  - "[[QA_ТестКейсы_Native_iOS_Personal_20260821]]"
  - "[[QA_Результаты]]"
  - "[[Источник_Текущий_Статус]]"
  - "[[MOC_Finance]]"
---

# Release Native iOS Current Parity 2026-08-22

## Результат

Native SwiftUI-приложение получило финальный code/CI approval; тот же exact code
успешно задеплоен на backend/PWA production. Физическая установка на iPhone ещё
не выполнялась.

- Integration branch: `codex/ios-native-current-parity-20260822`.
- Immutable release branch:
  `prod/release-finance-ios-current-parity-20260823-db7ebdd`.
- Deployed code SHA:
  `db7ebdd41a35018ae59e1fc4f5c5e38f0ed37de6`.

GitHub Actions run
`https://github.com/DmtrGoltsev/finance/actions/runs/32603535573`
успешен на точном финальном commit:

- full local backend: 317 passed, 6 skipped;
- Ruff: PASS;
- Alembic: одна head `20260822_0019`;
- XcodeGen, Debug и Release: PASS;
- normal XCTest/UI model: 87/0;
- dedicated PersonalSideloadHTTP transport tests: 10/0;
- launch UI: 1/1.

Финальный независимый reviewer: **APPROVE для code/CI**.

CI artifact: `ios-build-test-evidence-32603535573`, id `9483613408`,
digest
`sha256:52d98838dd947420e0093c308c58286ab3f5db831017030c4f64be61f6c7bc43`.

CI-only package run `32604090062` PASS: оба package jobs и common gate зелёные,
host/deploy skipped. Frontend artifact `9483667044`, digest
`sha256:0e430fdb2cfca47dcac29d18cec1351b45e17807fb2524800337c78a1db28bed`;
backend artifact `9483674722`, digest
`sha256:d38af135dab7b04ca1ce5c72c920f9e3f5b542eb73284964465d60fe3b522864`.

## Зафиксированный функциональный scope

- persistent secure `ios_bearer` session без хранения пароля;
- single-flight refresh, один retry, безопасный `403`, offline logout;
- A -> B isolation, SwiftData, JSON migration/recovery;
- transactional sync и stale-response guards;
- поиск категории по части слова в вертикальном modal picker;
- newest-first операции;
- редактирование суммы, даты, категории и счёта;
- pending investments только для выбранного месяца;
- personal-only;
- OCR online-only;
- payment-account filter;
- компактный month switcher.

Traceability и подробные шаги: [[QA_ТестКейсы_Native_iOS_Personal_20260821]].

## Worker evidence

- Secure session: commit `13bff57b`, run `32554005096`, XCTest 57/57,
  UI 1/1.
- SwiftData/sync: commit `640f93e2`, run `32554343934`, XCTest 52/52,
  UI 1/1.
- UX parity: commit `ba195e2`, run `32552813248`, PASS.
- Backend contract: commit `407e5628`; local backend 304 passed/6 skipped,
  targeted 61 и 29, Ruff PASS.

Worker runs не заменяют final gate; code/CI-вывод основан на run
`32603535573` на exact `db7ebdd...`.

## Закрытые findings двух review-циклов

- Реальный Keychain restore теперь применяет 72-часовой offline cap.
- Refresh/session lifetime продлевается безопасно; в финальной модели access
  TTL 15 минут отделён от sliding refresh/session TTL 30 дней.
- Offline edit/delete корректирует аналитику до синхронизации.
- Logout при гонке с refresh использует стабильное session-bound revoke proof.
- Частичный sync edit -> delete обновляет version и analytics baseline.
- Expense без категории корректирует breakdown через canonical
  `uncategorized`.

Открытых P0/P1 code findings в финальном reviewed scope нет.

## Непройденные внешние gates

- **Physical iPhone/signing: NOT RUN/BLOCKED.** Signed IPA и доказательства
  установки на реальный iPhone отсутствуют. Нужны Mac/Xcode, Apple
  Team/provisioning и устройство.
- **Ordinary Release HTTPS/ATS: NOT RUN/BLOCKED.** Обычный Release остаётся
  HTTPS-only. Отдельный target `FinanceAppPersonalHTTP` разрешён owner waiver
  только для owner/family sideload, exact URL и review до 2026-11-22. Plaintext
  risk принят; broad ATS exception запрещён.
- **Physical OCR и полный offline reconnect: NOT RUN.** Автоматические границы
  PASS, но device evidence отсутствует.

## Production governance waiver

- Required reviewer необязателен только для solo Finance.
- Environment secrets, CI gates, backup, pinned host key, migration/health
  checks, evidence и rollback readiness обязательны.
- Direct SSH/SCP production deployment запрещён.
- Environment proof: `protected_branches=false`,
  `custom_branch_policies=true`, branch policy `prod/release-*`.

## Production deploy 2026-08-23

- GitHub Actions run:
  `https://github.com/DmtrGoltsev/finance/actions/runs/32604838031` — SUCCESS.
- Required order: packages -> common gate -> host preflight -> backend ->
  frontend — PASS.
- Old backend: `finance-personal-backend-20260822-12a1b91f`.
- Old frontend: `20260726T220603Z-55f4ac53`.
- New release ID for both: `20260822T231803Z-db7ebdd4`.
- Backend path: `/opt/finance/releases/20260822T231803Z-db7ebdd4`.
- Frontend path: `/var/www/finance/releases/20260822T231803Z-db7ebdd4`.
- Service active through `/opt/finance/current`.
- DB: `20260618_0017 -> 20260822_0018 -> 20260822_0019`.
- Backup:
  `/opt/finance/backups/postgres/finance_prod-20260822T232027Z-20260822T231803Z-db7ebdd4-20260618_0017-to-20260822_0019.dump`.
- Backup SHA-256:
  `238d8d441b5bacca2a5f0ddba728cdf4066c34bd0e32a6c1a589f13cfcd57142`.
- Evidence file: тот же путь с suffix `.dump.evidence.txt`.
- Smoke PASS: health 200; OpenAPI 200/42 routes; frontend assets/service worker
  200 и scope `/finance/`; login 201; refresh 200 rotated; logout 204;
  post-logout 401; personal read-only endpoints 200.
- Rollback не запускался; release branch сохранена.
- Скачанное sanitized evidence вне Git:
  `C:\Users\style\Documents\Codex\Finance-release-evidence\32604838031`.

## Секреты

Production QA account уже хранится в
[[QA_Учетная_Запись_Production_20260822]]. Новые credentials не создавались и
не копировались в project Git, evidence или эту заметку.

## Связи

- [[QA_Результаты#Wave 28 Native iOS current parity integration (2026-08-22)]]
- [[Источник_Текущий_Статус]]
- [[MOC_Finance]]
- Project Mac Codex prompt:
  `docs/ios-native-mac-codex-install-prompt.md`.
