---
id: "finance-release-native-ios-current-parity-20260822"
тип: "доказательство"
статус: "заблокировано"
проект: "Finance"
владелец: "finance-team"
создано: "2026-08-22"
обновлено: "2026-08-22"
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

Native SwiftUI-приложение получило финальный code/CI approval в branch
`codex/ios-native-current-parity-20260822`, commit
`a5a332093587fc2467383686cca089877d03f90e`.

GitHub Actions run
`https://github.com/DmtrGoltsev/finance/actions/runs/32563222674`
успешен на точном финальном commit:

- full local backend: 313 passed, 6 skipped;
- backend CI auth/migration: 63 tests PASS;
- Ruff: PASS;
- Alembic: одна head `20260822_0019`;
- XcodeGen, Debug и Release: PASS;
- XCTest: 77/77;
- launch UI: 1/1.

Финальный независимый reviewer: **APPROVE для code/CI**.

CI artifact: `ios-build-test-evidence-32563222674`, id `9473425949`,
digest
`sha256:028cd3b931aec26c119ca649eb4f392eda1d1d60182c1295fd57e3302d22e801`.

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
`32563222674`.

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
- **Production HTTPS/ATS: NOT RUN/BLOCKED.** Production Finance API остаётся
  plain HTTP. Нужен trusted HTTPS endpoint; broad ATS exception запрещён.
- **Backend production deploy: PREFLIGHT BLOCKED / NOT PERFORMED.** Environment
  `production` имеет `protection_rules=[]`; branch
  `prod/release-finance-ios-backend-20260822` существует только локально и не
  запушена; production DB остаётся на `20260618_0017`; health HTTP 200;
  HTTPS/FQDN отсутствует. Head `20260822_0019` в production не применён.
- **Physical OCR и полный offline reconnect: NOT RUN.** Автоматические границы
  PASS, но device evidence отсутствует.

## Секреты

Production QA account уже хранится в
[[QA_Учетная_Запись_Production_20260822]]. Новые credentials не создавались и
не копировались в project Git, evidence или эту заметку.

## Связи

- [[QA_Результаты#Wave 28 Native iOS current parity integration (2026-08-22)]]
- [[Источник_Текущий_Статус]]
- [[MOC_Finance]]
