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

Native SwiftUI-приложение интегрировано в branch
`codex/ios-native-current-parity-20260822`, commit
`33df6710a7ee3fb6386634563a0e8c5a33b80d20`.

GitHub Actions run
`https://github.com/DmtrGoltsev/finance/actions/runs/32556492248`
успешен на точном интегрированном commit:

- backend auth/migration: 29 tests PASS;
- Ruff: PASS;
- Alembic: одна head `20260822_0018`;
- XcodeGen, Debug и Release: PASS;
- XCTest: 69/69;
- launch UI: 1/1.

CI artifact: `ios-build-test-evidence-32556492248`, id `9471631068`,
digest
`sha256:40641f8822e91a36737fd7c9c448e43a12edd689aaecb38878729fad13aadc3a`.

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

Worker runs не заменяют integrated gate; release-вывод основан на run
`32556492248`.

## Непройденные внешние gates

- **Physical iPhone/signing: NOT RUN/BLOCKED.** Signed IPA и доказательства
  установки на реальный iPhone отсутствуют. Нужны Mac/Xcode, Apple
  Team/provisioning и устройство.
- **Production HTTPS/ATS: NOT RUN/BLOCKED.** Production Finance API остаётся
  plain HTTP. Нужен trusted HTTPS endpoint; broad ATS exception запрещён.
- **Backend production deploy: NOT PERFORMED.** Миграция `20260822_0018`
  проверена CI, но не применена к production DB в этой волне.
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
