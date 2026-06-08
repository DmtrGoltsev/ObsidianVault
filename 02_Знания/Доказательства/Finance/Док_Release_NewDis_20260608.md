---
id: "finance-release-newdis-20260608"
тип: "доказательство"
статус: "активно"
проект: "Finance"
владелец: "rocketflow-team"
создано: "2026-06-08"
обновлено: "2026-06-08"
уверенность: "высокая"
источники:
  - "Sanitized release closure handoff for Finance newDis"
доказательства:
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
  - "[[Единый_Документ_Критики_И_План_NewDis]]"
  - "[[Карта_Пользовательских_Путей_Finance]]"
теги: ["finance", "release", "newdis", "production", "evidence", "sanitized"]
ссылки:
  - "[[Finance]]"
  - "[[MOC_Finance]]"
  - "[[Пакет_Finance_Полный]]"
---

# Release evidence — newDis UX simplification (2026-06-08)

## Что доказывается

Release `newDis` закрыт по commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b` (`feat(finance): simplify newDis UX flows`). Production frontend подтвержден как байтово совпадающий с локальным `apps/web-pwa/dist`, Android debug APK собран и проверен по unit/lint evidence, backend redeploy waiver принят.

Эта заметка содержит только sanitized closure: без секретов, сырых логов, скриншотов, session/operator данных и персональных данных.

## Метод проверки

- Git/release metadata: branch `newDis`, `HEAD = origin/newDis = 6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- Diff boundary: commit меняет UI/test files; `apps/backend`, `db`, `api` не менялись.
- Production frontend: `/finance/COMMIT`, `/finance/`, `/finance/sw.js`, manifest и JS/CSS assets сверены с локальным `apps/web-pwa/dist`.
- Production backend health: `/finance-api/health` проверен; exact backend commit endpoint отсутствует.
- Android artifact: APK path, SHA256, size и application metadata сверены.
- QA evidence: Android unit XML, Android lint, historical PWA/backend/OpenAPI evidence классифицированы по актуальности.

## Результат

| Проверка | Значение |
|----------|----------|
| Статус | Закрыто с ограничениями |
| Project branch | `newDis` |
| Project commit | `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Commit message | `feat(finance): simplify newDis UX flows` |
| Remote parity | `HEAD = origin/newDis = 6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Backend/API/DB delta | Нет изменений в `apps/backend`, `db`, `api` |
| Backend redeploy | Waiver принят: exact backend commit напрямую не доказан, но final HEAD не содержит backend/db/api delta |

## Production frontend evidence

| Проверка | Значение |
|----------|----------|
| `/finance/COMMIT` | HTTP `200`, body `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| Local dist `COMMIT` | `6ce31f53f6150050b4cb0dad8488254bd04ff31b` |
| `/finance/` | byte-hash equal local `apps/web-pwa/dist` |
| `/finance/sw.js` | byte-hash equal local `apps/web-pwa/dist` |
| Manifest | byte-hash equal local `apps/web-pwa/dist` |
| JS/CSS assets | byte-hash equal local `apps/web-pwa/dist` |

## PWA hashes

| Artifact | SHA256 |
|----------|--------|
| Index | `c6c7b6331ecbc8b3cfd82a7a41a846ae3c33340be8b334c14777c1a584924540` |
| Service worker | `0aaedaf8d30b892b4cd7faa192b473d2803a285e5753bf87935db0e6ab99498f` |
| Manifest | `23ae090c2961076254e9015bab16dbba3fa10a6d7a05d06eaea590acd2182ad8` |
| JavaScript asset | `bf6d7b481c32d91a95cc17f987ac505b90723abcbdc3c574ee453fa806b9cdaf` |
| CSS asset | `10329625103101e5c48e28fb81135c19fdfb46c97f19a2b0f916c960518e4947` |

## Production backend evidence

| Проверка | Значение |
|----------|----------|
| `/finance-api/health` | HTTP `200`, body `{status:ok}` |
| Exact commit endpoints | `/finance-api/COMMIT`, `/commit`, `/version` return `404` |
| Route surface | Matches post-808/newDis route surface |
| Waiver | Backend exact commit not directly proven; runtime route surface matches post-808/newDis and final HEAD has no backend/db/api delta |

## Android artifact

| Параметр | Значение |
|----------|----------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| SHA256 | `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D` |
| Size | `54,235,660` |
| Local app-debug.apk | Same size and SHA256 |
| applicationId | `com.finance.mvp` |
| versionCode | `1` |
| versionName | `0.1.0` |
| minSdk | `26` |
| targetSdk | `34` |
| Signing | debug-signed, не release-signed |

## QA gate

| Область | Результат |
|---------|-----------|
| Android unit XML | 9 files, 60 tests, 0 failures, 0 errors, 0 skipped |
| Android lint | 0 errors, 6 warnings |
| PWA Vitest | Historical only: old reports, not direct `6ce31f5` closure |
| Backend pytest | Historical only: `152 passed, 4 warnings`, not direct `6ce31f5` closure |
| OpenAPI redocly | Historical PASS, not direct `6ce31f5` closure |
| Android prod rerun sanitized PASS | Historical context only: targets old commits `d9ffc75`/`808f7278` |
| Connected instrumentation stale failing XML | Не используется как green evidence |

## Acceptance clarification

- `newDis` closure подтверждает production PWA static deployment and byte parity for commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- Backend redeploy не требовался по принятому waiver: final HEAD не менял backend/db/api.
- Planning/OCR/product limitations из [[Карта_Пользовательских_Путей_Finance]] остаются действующими: `Overview` read-only, Planning для `newDis` трактуется Android-first без отдельного PWA Planning proof, OCR copy не должна обещать Android on-device OCR без отдельной реализации и QA evidence.

## Известные ограничения и риски

- HTTP IP limits не позволяют считать PWA install/service worker proof полным; для полного PWA install proof ещё нужны HTTPS/domain.
- Backend exact commit endpoint отсутствует, поэтому backend exact commit directly not proven.
- Authenticated production login/OCR smoke и retention/privacy evidence не закрыты этой поставкой.
- APK debug-signed, не release-signed.
- Historical reports не должны подаваться как direct green evidence для commit `6ce31f5`.
