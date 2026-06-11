---
id: "moc-finance"
тип: "MOC"
проект: "Finance"
статус: "активно"
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-12"
уверенность: "высокая"
теги: ["MOC", "finance", "навигация"]
источники:
  - "README.md"
  - "docs/product-mvp.md"
  - "docs/current-status.md"
ссылки:
  - "[[Finance]]"
  - "[[MOC_Все_Проекты]]"
  - "[[Док_Release_NewDis_20260608]]"
---

# MOC — Finance

Навигационная карта проекта Finance. Все заметки проекта собраны здесь.

## Проект

- [[Finance]] — главная заметка проекта

## Под-MOC

_(под-MOC проекта будут добавляться по мере роста vault)_

## Глоссарий

- [[Household]] — семейное пространство
- [[Personal_Shared]] — personal vs shared данные
- [[Transaction]] — операция (income/expense/transfer/brokerage)
- [[Transfer]] — перевод между счетами
- [[Capture_Draft]] — OCR черновик
- Asset categories — source of truth для категорий активов: `manualAmount`, `isInvestment`, `assetType`, `icon_key`, `account.assetCategoryId`, без stale totals от удалённых счетов; compact card/edit hides manual amount when linked accounts exist and uses trending-up investment badge
- Planning MVP — планирование доходов и распределений во вкладке Analytics; новые allocations выбирают expense category или investment asset category, account target для новых allocations не предлагается

## Источники

- [[Источник_README]]
- [[Источник_Продукт_MVP]]
- [[Источник_Текущий_Статус]]
- [[Источник_ADR_0001]]
- [[Источник_Security_Baseline]]

## Пакеты контекста

- [[Пакет_Finance_Полный]] — агрегирующий пакет со всеми ссылками
- [[Кворум_Finance]] — кворум-саммари проекта

## Дизайн и UX

- [[Карта_Пользовательских_Путей_Finance]] — карта основных пользовательских путей Finance для дизайнеров
- [[Единый_Документ_Критики_И_План_NewDis]] — кворум-синтез 6 дизайн-критик и план первой итерации `newDis`

## Агенты

_(роли агентов проекта — см. `03_Агенты/Finance/`)_

## Решения

_(архитектурные и проектные решения — см. `04_Решения/Finance/`)_

## Доказательства

- [[QA_Результаты]] — результаты прогонов тестирования
- [[QA_Фиксы]] — журнал фиксов багов
- [[Док_Release_NewDis_20260608]] — sanitized closure/evidence по production frontend release `newDis`, commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; latest Android critical investment fix addendum 2026-06-12 records project commit `d8175116f5123b6a304d4bd22dc083f2725505a0`
- [[Док_Release_Planning_MVP_20260607]] — concise evidence по production release `20260607T225457Z-819b5815`
- Planning evidence — см. [[QA_Фиксы#Волна 3 (2026-06-06)]], [[QA_Фиксы#Волна 4 (2026-06-07)]], [[QA_Фиксы#Волна 5 (2026-06-07)]] и [[QA_Фиксы#Волна 6 (2026-06-07)]]
- Release context — текущая поставка 2026-06-08: `newDis`; production frontend commit `6ce31f53f6150050b4cb0dad8488254bd04ff31b`; latest finance fix commit `09ea6479451c61b3d06a412e5aaaecec534fc96a`; frontend `/finance/COMMIT` 200 и byte-hash parity с local `apps/web-pwa/dist`; backend health 200 с accepted backend redeploy waiver; backend targeted suite `31 passed, 2 warnings`; Android `:app:testDebugUnitTest` successful; `:app:assembleDebug` successful; integration review P0/P1 clean; debug APK SHA256 `D1734426439FF38627C230D454D04E66229655C8DF6FD651087DC065B7A30733`
- Release context — текущая поставка 2026-06-07: Planning iteration MVP; project commit `819b5815fed8c81bfa6a6e6131e790429454c2e8`; release `20260607T225457Z-819b5815`; backend `/opt/finance/releases/20260607T225457Z-819b5815`; web `/var/www/finance/releases/20260607T225457Z-819b5815`; Alembic `20260607_0013 (head)`; backend `243 passed, 9 warnings`; Android unit/assemble PASS; health/static checks OK

## Схемы

_(схемы проекта — см. `05_Система/Схемы/Finance/`)_

## Регламенты

_(регламенты проекта — см. `05_Система/Регламенты/Finance/`)_

## Промпты

_(промпты агентов — см. `05_Система/Промпты/Finance/`)_

## Навигация

- [[MOC_Все_Проекты]] — ← все проекты

## Latest evidence update (2026-06-10)

- Latest `newDis` project commit: `1013e632d54c6af6ed9326d8b7f761bdd381bade`.
- Evidence recorded in [[QA_Результаты]], [[QA_Фиксы]], [[Док_Release_NewDis_20260608]] and [[Пакет_Finance_Полный]].
- Summary: asset category expanded linked rows restored, legacy `Карта`/`Банк` visibility restored without duplicates, category-level `isInvestment` save/local state fixed, planning past-month clamp and missing-plan friendly empty state fixed, Russian input diagnosed as likely emulator/IME configuration.
- APK evidence: `finance-mvp-newd-0.1.0-debug.apk`, SHA256 `FCD7EE0D870A12B3B88416DAEBCB3CF35FC513618C865B427E30E5F77F688411`, production API base present, dev URLs absent, installed on AVD `Codex`.

## Latest evidence update (2026-06-12)

- Critical Android regression `Брокер -> Инвестиция -> Сохранить` closed by removing `iconKey` from `POST /api/v1/asset-categories` create payload; deployed OpenAPI rejects extra fields for `AssetCategoryCreateRequest`.
- Project commit: `d8175116f5123b6a304d4bd22dc083f2725505a0` (`fix(finance): migrate legacy brokerage assets`), pushed to `origin/newDis`.
- Evidence recorded in [[QA_Результаты]], [[QA_Фиксы]], [[Док_Release_NewDis_20260608]] and project summary `MVP_EVIDENCE/critical-investment-fix-20260612/SUMMARY_SANITIZED.md`.
- QA: `compileDebugKotlin` PASS; `testDebugUnitTest` PASS, 71 tests; `assembleDebug` PASS; quick critical-path QA PASS and harness PASS on `emulator-5556`.
- APK evidence: `artifacts/apk/finance-mvp-newd-0.1.0-debug.apk`, SHA256 `B6960DB5D13198405984C027746343432CB95B0C08BB24F54D6A7FCD5061DCC7`, size `54235740` bytes.
