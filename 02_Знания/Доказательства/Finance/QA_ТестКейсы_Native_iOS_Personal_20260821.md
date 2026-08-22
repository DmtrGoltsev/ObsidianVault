---
id: "finance-qa-native-ios-personal-20260821"
тип: "доказательство"
проект: "Finance"
название: "QA тест-кейсы — Native iOS Personal"
создано: "2026-08-21"
обновлено: "2026-08-23"
уверенность: "высокая"
теги: ["qa", "finance", "ios", "native", "personal-only", "regression"]
ссылки:
  - "[[QA_Результаты]]"
  - "[[Источник_Текущий_Статус]]"
  - "[[Пакет_Finance_Полный]]"
  - "[[MOC_Finance]]"
---

# QA тест-кейсы — Native iOS Personal

Матрица для полноценного native-приложения из `apps/ios`. Legacy Capacitor из
`apps/web-pwa/ios` не является целевым iOS-приложением.

## Зафиксированная база

- Branch: `codex/ios-native-current-parity-20260822`.
- Immutable release branch:
  `prod/release-finance-ios-current-parity-20260823-db7ebdd`.
- Verified/deployed code: `db7ebdd41a35018ae59e1fc4f5c5e38f0ed37de6`.
- CI: `https://github.com/DmtrGoltsev/finance/actions/runs/32603535573`.
- Native automated baseline: backend full 317 passed/6 skipped;
  Debug/Release/Personal PASS; normal model 87/0; personal transport 10/0.
- Репозиторный handoff: `docs/ios-native-mac-handoff.md`.
- Copy-paste Mac Codex task: `docs/ios-native-mac-codex-install-prompt.md`.
- Evidence: `MVP_EVIDENCE/native-ios-current-parity-20260822/SUMMARY_SANITIZED.md`.

## Current-parity traceability 2026-08-22

| ID | Требование | Автоматическое доказательство | Статус |
| --- | --- | --- | --- |
| FIN-IOS-AUTH-010 | Secure session, пароль не хранится | SecureSessionTests + Keychain ThisDeviceOnly tests | PASS CI |
| FIN-IOS-AUTH-011 | Single-flight refresh, один retry | Concurrent 401 and second-401 tests | PASS CI |
| FIN-IOS-AUTH-012 | 403 сохраняет session и pending data | Dedicated 403 test | PASS CI |
| FIN-IOS-AUTH-013 | Offline logout | Local invalidation/lease test | PASS CI |
| FIN-IOS-ISO-010 | A -> B isolation | SwiftData account switch + stale response tests | PASS CI |
| FIN-IOS-DB-010 | JSON migration/recovery | Migration, tombstone, idempotency tests | PASS CI |
| FIN-IOS-SYNC-010 | Transactional sync | Atomic commit and rollback tests | PASS CI |
| FIN-IOS-SYNC-011 | Stale response rejection | Stale push/refresh tests | PASS CI |
| FIN-IOS-CAT-010 | Search/modal/vertical picker | IOSUXParityTests | PASS CI |
| FIN-IOS-OPS-010 | Newest-first | Pagination and stable tie-break tests | PASS CI |
| FIN-IOS-OPS-011 | Edit amount/date/category/account | Edit sheet/policy/root wiring tests | PASS CI; device UX NOT RUN |
| FIN-IOS-AN-010 | Selected-month pending investments | DashboardAndDateTests | PASS CI |
| FIN-IOS-PER-010 | Personal-only | Personal contract + launch UI tests | PASS CI |
| FIN-IOS-OCR-010 | OCR online-only | Sync policy/OCR boundary/bearer tests | PASS CI; physical OCR NOT RUN |
| FIN-IOS-PAY-010 | Payment account | Quick expense/editor policy tests | PASS CI |
| FIN-IOS-MONTH-010 | Compact month switcher | Current-month shortcut test | PASS CI; device a11y NOT RUN |

Полная модель и detailed steps находятся в
`docs/testing/ios-native-parity-qa-test-model.md`.

## Точные внешние блокеры

- Physical iPhone/signing: **NOT RUN/BLOCKED**. Signed IPA отсутствует.
- Ordinary Release HTTPS/ATS: **NOT RUN/BLOCKED**. PersonalSideloadHTTP имеет
  отдельный bundle id, exact HTTP allowlist, development-only signing/no archive
  и owner waiver до 2026-11-22.
- Production backend/PWA deploy/migration: **PASS**, run `32604838031`, DB
  `20260822_0019`.
- Physical OCR и полный offline reconnect: **NOT RUN**.

Release evidence: [[Док_Release_Native_iOS_Current_Parity_20260822]].

## Автоматические и статические кейсы

| ID | Приоритет | Кейс | Ожидаемый результат | Статус 2026-08-22 |
| --- | --- | --- | --- | --- |
| FIN-IOS-BLD-001 | P0 | `xcodegen generate` | Проект генерируется без ошибок | PASS CI |
| FIN-IOS-BLD-002 | P0 | Debug device build без signing | `BUILD SUCCEEDED` | PASS CI |
| FIN-IOS-BLD-003 | P0 | Release device build без signing с HTTPS URL | `BUILD SUCCEEDED` | PASS CI |
| FIN-IOS-BLD-004 | P0 | Release с пустым/plain HTTP/local API URL | Приложение блокирует небезопасную конфигурацию | PASS automated/static |
| FIN-IOS-TST-001 | P0 | Полный XCTest | Normal 87/0, personal 10/0 | PASS CI |
| FIN-IOS-TST-002 | P0 | Launch UI personal-only | Вход/регистрация видимы; `Общее`/`Мой обзор` отсутствуют | PASS CI, 1/1 |
| FIN-IOS-PER-001 | P0 | Account/category/asset list API | Только personal scope, household rows отфильтрованы | PASS automated/static |
| FIN-IOS-PER-002 | P0 | Reports API | `reportMode=personal`, `householdId=nil` | PASS automated/static |
| FIN-IOS-CAT-001 | P1 | Категории | Заголовок `Категории расходов`, только expense active/archive | PASS automated/static |
| FIN-IOS-CAT-002 | P1 | Создание категории | Создаётся `expense` + `personal`, переключателей income/expense и mode нет | PASS automated/static |
| FIN-IOS-SYNC-001 | P0 | HTTP 401 | Один refresh/retry; только повторный 401 очищает текущую session | PASS XCTest |
| FIN-IOS-SYNC-002 | P0 | HTTP 403 | Identity, session и pending queue сохраняются | PASS XCTest |
| FIN-IOS-SYNC-003 | P0 | Pending queue после cold start/network error | Очередь сохраняется и доступна для retry | PASS XCTest |
| FIN-IOS-OCR-001 | P0 | OCR boundary | Screenshot/OCR не попадает в local store/pending queue | PASS XCTest/static |
| FIN-IOS-PHTTP-001 | P0 | Personal built plist/identity/signing/archive policy | Exact HTTP host/path only; separate bundle; manual Apple Development; no archive/export | PASS CI |
| FIN-IOS-PHTTP-002 | P0 | 3xx redirect and final URL validation | Redirect rejected; final response URL revalidated | PASS XCTest |

## Обязательные кейсы на Mac и физическом iPhone

| ID | Приоритет | Шаги | Ожидаемый результат | Текущий статус |
| --- | --- | --- | --- | --- |
| FIN-IOS-DEV-001 | P0 | Выбрать Team, уникальный bundle ID, подключить iPhone, Run | Приложение подписано и установлено без App Store | BLOCKED/NOT RUN |
| FIN-IOS-AUTH-001 | P0 | Войти, force quit, открыть снова | Сессия восстановлена, повторный ввод пароля не нужен | BLOCKED/NOT RUN |
| FIN-IOS-AUTH-002 | P0 | Logout, relaunch | Bearer session invalidated; данные/queue прошлого account недоступны | BLOCKED/NOT RUN |
| FIN-IOS-AUTH-003 | P0 | Регистрация нового personal user | Регистрация успешна, UI не раскрывает существование чужого account | BLOCKED/NOT RUN |
| FIN-IOS-OPS-001 | P0 | Добавить expense/income с выбранной датой | Операция сохранена с date-only semantics | BLOCKED/NOT RUN |
| FIN-IOS-OPS-002 | P1 | Поиск категории по части слова | Вертикальный список фильтруется, выбор сохраняется | BLOCKED/NOT RUN |
| FIN-IOS-OPS-003 | P0 | Создать transfer в investment account | Баланс актива и инвестиции выбранного месяца обновлены после sync | BLOCKED/NOT RUN |
| FIN-IOS-OPS-004 | P1 | Открыть операции/главную | Операции отсортированы от новых к старым | BLOCKED/NOT RUN |
| FIN-IOS-AN-001 | P1 | Переключить месяц в аналитике | Факт/план/отклонения и инвестиции соответствуют выбранному месяцу | BLOCKED/NOT RUN |
| FIN-IOS-OFF-001 | P0 | Offline create/edit/delete, relaunch | Локальные данные и pending queue сохранены | BLOCKED/NOT RUN |
| FIN-IOS-OFF-002 | P0 | Вернуть сеть, нажать sync | Push/pull сходится с сервером без дублей | BLOCKED/NOT RUN |
| FIN-IOS-OCR-002 | P0 | Без сети выбрать screenshot OCR | Понятная online-only ошибка, изображение не ставится в очередь | BLOCKED/NOT RUN |
| FIN-IOS-OCR-003 | P0 | С сетью пройти OCR confirm/edit | Сумма/дата редактируются до подтверждения; raw OCR не сохраняется | BLOCKED/NOT RUN |

## Production account locator

Для production smoke использовать только существующий persistent QA account из
[[QA_Результаты#Production QA persistent account (2026-07-11)]]. Учетную запись
помечать `NEVER DELETE`. Для текущей reusable production учётки использовать
[[QA_Учетная_Запись_Production_20260822]]; не копировать credentials в project
repo, release evidence, логи, screenshots или чат.

## Release boundary

Обычный public Release требует trusted HTTPS endpoint. Запрещён произвольный ATS
exception. Для owner/family physical install утверждён отдельный
`FinanceAppPersonalHTTP`/`PersonalSideloadHTTP` с точным production HTTP URL,
отдельной identity, no archive/export и waiver до 2026-11-22.

1. собственный домен/subdomain с публично доверенным TLS и автопродлением;
2. публично доверенный short-lived Let's Encrypt IP certificate с IP в SAN,
   контролем продления и мониторингом срока.

Plain HTTP production IP не является допустимым ordinary/public Release
endpoint, но разрешён в узком personal sideload scope выше с принятым риском.

## Финальный review closure

Оба reviewer-цикла закрыты: 72-hour restore cap, refresh/logout race,
offline edit/delete analytics, отдельные access/refresh expiry, partial
edit -> delete rebase и `uncategorized` breakdown имеют regression coverage.
Final reviewer: **APPROVE for code/CI**.

Production deploy: **PASS**, run `32604838031`; DB migrated to
`20260822_0019`; backup/smoke PASS. Final independent review exact
`db7ebdd...`: **APPROVE**, no P0-P3. Physical iPhone remains NOT RUN.
