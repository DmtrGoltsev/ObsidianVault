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

Аддендум Android APK prod API base: исходный APK этой заметки с SHA256 `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D` superseded, потому что аудит APK нашел `http://10.0.2.2:8000` и не нашел `/finance-api`. Актуальный production-path APK собран после project commit `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`) и имеет SHA256 `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94`.

Аддендум Android UX fixes: после P0/P1-clean review применён project commit `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`), branch `newDis`, remote parity OK. Изменения ограничены `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt` и `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`; новый APK supersedes SHA `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94` и имеет SHA256 `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A`.

Аддендум Android final correction: два оставшихся user misses закрыты project commit `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`), branch `newDis`, remote parity OK. Изменения ограничены `apps/android/app/src/main/AndroidManifest.xml`, `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt` и `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt`; новый APK supersedes SHA `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` и имеет SHA256 `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B`.

Эта заметка содержит только sanitized closure: без секретов, сырых логов, скриншотов, session/operator данных и персональных данных.

## Метод проверки

- Git/release metadata: branch `newDis`, `HEAD = origin/newDis = 6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- Diff boundary: commit меняет UI/test files; `apps/backend`, `db`, `api` не менялись.
- Production frontend: `/finance/COMMIT`, `/finance/`, `/finance/sw.js`, manifest и JS/CSS assets сверены с локальным `apps/web-pwa/dist`.
- Production backend health: `/finance-api/health` проверен; exact backend commit endpoint отсутствует.
- Android artifact: APK path, SHA256, size и application metadata сверены.
- Android APK prod-path correction: rebuild with `-PfinanceApiBaseUrl=http://45.10.110.42/finance-api`, APK string scan and production smoke verified.
- Android UX fixes: custom `AddAccountState?` Saver, explicit asset-category edit/delete affordances, keyboard-safe account sheet, safe category archive behavior and local drag reorder persistence verified by code review plus unit/Kotlin gates.
- Android final correction: legacy old asset group conversion to real investment asset category, link rollback safety and strengthened account creation IME handling verified by final review plus unit/Kotlin/assemble gates.
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
| Android APK correction commit | `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` (`fix(android): use production API base for APK`), branch `newDis`, remote parity OK |
| Android UX fix commit | `16a8be832d7c7fbaacf03325325da63db357d450` (`fix(android): refine asset category interactions`), branch `newDis`, remote parity OK |
| Android final correction commit | `f5afcda40e12b881ccc31a6b32221b24327cdbd8` (`fix(android): complete legacy asset edit and IME handling`), branch `newDis`, remote parity OK |

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

## Android APK prod-path correction

| Параметр | Значение |
|----------|----------|
| Status | PASS, supersedes previous APK hash `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D` |
| Project commit | `1581a6fc464521f7d2503ac4bbdcb6c918f8fbd3` |
| Commit message | `fix(android): use production API base for APK` |
| Build command | `.\gradlew.bat :app:testDebugUnitTest :app:assembleDebug -PfinanceApiBaseUrl=http://45.10.110.42/finance-api` -> `BUILD SUCCESSFUL` |
| Unit XML summary | 9 XML files, 61 tests, 0 failures/errors/skipped |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| SHA256 | `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94` |
| Size | `54,235,660` |
| Contains | `http://45.10.110.42/finance-api` |
| Does not contain | `http://10.0.2.2:8000`, `localhost:8000`, `127.0.0.1`, `http://45.10.110.42/api/v1`, `http://45.10.110.42/finance-api/api/v1` as base |
| Prod smoke | `/finance-api/health` -> HTTP `200` `{status:ok}`; protected `/finance-api/api/v1/sessions/current` and `/accounts` -> HTTP `401` without auth |
| Web commit context | `/finance/COMMIT` remains `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; not a blocker for Android-only fix |
| Known waiver | Plain HTTP remains accepted until HTTPS/domain |

## Android UX fixes addendum

| Параметр | Значение |
|----------|----------|
| Status | PASS with manual gesture/IME caveats |
| Project commit | `16a8be832d7c7fbaacf03325325da63db357d450` |
| Commit message | `fix(android): refine asset category interactions` |
| Changed files | `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt`; `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt` |
| Recents/overview stability | Probable crash fixed through custom Saver for nullable `AddAccountState?` |
| Asset category edit | Explicit edit icon; investment checkbox visible and saved through existing update flow |
| Add account keyboard UX | Sheet uses IME padding, scroll and BringIntoView for focused fields above keyboard |
| Destructive category action | Bulk archive gesture removed; trash action requires confirmation; non-empty category archive is blocked and asks user to move/delete accounts first; empty category archive calls backend category archive endpoint |
| Asset category reorder | Long-press drag reorder added with local `SharedPreferences` persistence |
| Review result | P0/P1 clean after P1 fix |
| Unit tests | `:app:testDebugUnitTest` -> `BUILD SUCCESSFUL`; 61 tests, 0 failures/errors/skipped |
| Kotlin compile | `:app:compileDebugKotlin` -> `BUILD SUCCESSFUL` |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| SHA256 | `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` |
| Size | `54,235,660` |
| Content verification | Contains `http://45.10.110.42/finance-api`; no dev/local URLs found |
| Remaining manual QA | Actual recents/overview, keyboard behavior, drag gestures and confirmation dialogs still need device/emulator visual proof |

## Android final correction addendum

| Параметр | Значение |
|----------|----------|
| Status | PASS with live migration/visual IME caveats |
| Project commit | `f5afcda40e12b881ccc31a6b32221b24327cdbd8` |
| Commit message | `fix(android): complete legacy asset edit and IME handling` |
| Changed files | `apps/android/app/src/main/AndroidManifest.xml`; `apps/android/app/src/main/java/com/finance/mvp/api/ApiClient.kt`; `apps/android/app/src/main/java/com/finance/mvp/ui/FinanceApp.kt` |
| Legacy group investment edit | Legacy old asset group like `Вклад` has `Инвестиция` checkbox in legacy edit dialog |
| Rename-only compatibility | Checkbox off keeps old rename-only behavior |
| Legacy conversion | Checkbox on converts legacy group to real asset category with `isInvestment=true` and links active legacy accounts |
| Conversion guards | Blocks empty group, mixed-currency group, overview/no writable scope |
| Rollback safety | Link failure rollback uses updated account versions and archives created category |
| Account creation IME | `adjustResize`, `skipPartiallyExpanded`, `imePadding`, `navigationBarsPadding`, repeated `BringIntoView`, larger spacer |
| Material3 compatibility | `windowInsets` unavailable; compatible fallback used |
| Review result | Final review P0/P1 clean |
| Unit tests | `:app:testDebugUnitTest` PASS; 61 tests, 0 failures/errors/skipped |
| Kotlin compile | `:app:compileDebugKotlin` PASS |
| APK build | `assembleDebug` PASS |
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| SHA256 | `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B` |
| Size | `54,235,660` |
| Content verification | Production API base found x2; dev URLs absent |
| Remaining manual QA | Device/emulator visual IME and live migration proof still required |

## Android artifact

| Параметр | Значение |
|----------|----------|
| APK | `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-mvp-newd-0.1.0-debug.apk` |
| SHA256 | `4A3C32727C69427A714E82C45CF77A2666D2C52A4792B909B3153F763DB34A7B` |
| Size | `54,235,660` |
| Supersedes | Previous APK SHA256 `B0CC0C8D66196CA2503759F2CA4FC07E5700AD6E7DB4B64A229DBEC9D3F3F42A` from Android UX fixes; older production-path APK SHA256 `593F88085D7EC2AE39141CA5AC3317C74A7473C94AE1F24E1CE373DCF11C3F94` already superseded `D1DDE146BB0576D438B173E3910AAADDFFDA1382CDBF5C27BDD1C6E75DC0391D`, which retained emulator dev base URL |
| applicationId | `com.finance.mvp` |
| versionCode | `1` |
| versionName | `0.1.0` |
| minSdk | `26` |
| targetSdk | `34` |
| Signing | debug-signed, не release-signed |

## QA gate

| Область | Результат |
|---------|-----------|
| Android unit XML | 9 files, 61 tests, 0 failures, 0 errors, 0 skipped for prod-path correction |
| Android UX unit gate | `:app:testDebugUnitTest` BUILD SUCCESSFUL; 61 tests, 0 failures/errors/skipped |
| Android Kotlin compile | `:app:compileDebugKotlin` BUILD SUCCESSFUL |
| Android final correction gate | `:app:testDebugUnitTest` PASS, 61 tests, 0 failures/errors/skipped; `:app:compileDebugKotlin` PASS; `assembleDebug` PASS |
| Android UX review | P0/P1 clean after P1 fix |
| Android final review | P0/P1 clean |
| Android lint | 0 errors, 6 warnings |
| PWA Vitest | Historical only: old reports, not direct `6ce31f5` closure |
| Backend pytest | Historical only: `152 passed, 4 warnings`, not direct `6ce31f5` closure |
| OpenAPI redocly | Historical PASS, not direct `6ce31f5` closure |
| Android prod rerun sanitized PASS | Historical context only: targets old commits `d9ffc75`/`808f7278` |
| Connected instrumentation stale failing XML | Не используется как green evidence |

## Acceptance clarification

- `newDis` closure подтверждает production PWA static deployment and byte parity for commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`.
- Backend redeploy не требовался по принятому waiver: final HEAD не менял backend/db/api.
- Android UX addendum закрывает code-review/unit/Kotlin evidence для asset category interactions, AddAccountSheet keyboard handling and recents Saver; финальный Android correction addendum закрывает legacy asset edit conversion и усиленный IME handling; manual device proof остаётся отдельным gate.
- Planning/OCR/product limitations из [[Карта_Пользовательских_Путей_Finance]] остаются действующими: `Overview` read-only, Planning для `newDis` трактуется Android-first без отдельного PWA Planning proof, OCR copy не должна обещать Android on-device OCR без отдельной реализации и QA evidence.

## Известные ограничения и риски

- HTTP IP limits не позволяют считать PWA install/service worker proof полным; для полного PWA install proof ещё нужны HTTPS/domain.
- Backend exact commit endpoint отсутствует, поэтому backend exact commit directly not proven.
- Authenticated production login/OCR smoke и retention/privacy evidence не закрыты этой поставкой.
- APK debug-signed, не release-signed.
- Historical reports не должны подаваться как direct green evidence для commit `6ce31f5`.
- Actual recents/overview, keyboard, long-press drag reorder and confirmation dialogs require emulator/device manual QA; live migration of legacy old asset groups and visual IME behavior also require device/emulator proof.
