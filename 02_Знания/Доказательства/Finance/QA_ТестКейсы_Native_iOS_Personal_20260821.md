---
id: "finance-qa-native-ios-personal-20260821"
тип: "доказательство"
проект: "Finance"
название: "QA тест-кейсы — Native iOS Personal"
создано: "2026-08-21"
обновлено: "2026-08-21"
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

- Branch: `codex/ios-native-personal-parity-20260820`.
- Verified commit: `96aa58226ad8f80834ea333192ebace7885d69c2`.
- CI: `https://github.com/DmtrGoltsev/finance/actions/runs/32523201106`.
- Native automated baseline: Debug/Release PASS, XCTest 47/47, UI 1/1.
- Репозиторный handoff: `docs/ios-native-mac-handoff.md`.
- Evidence: `MVP_EVIDENCE/personal-native-ios-final-regression-20260821-234120/SUMMARY_SANITIZED.md`.

## Автоматические и статические кейсы

| ID | Приоритет | Кейс | Ожидаемый результат | Статус 2026-08-21 |
| --- | --- | --- | --- | --- |
| FIN-IOS-BLD-001 | P0 | `xcodegen generate` | Проект генерируется без ошибок | PASS CI |
| FIN-IOS-BLD-002 | P0 | Debug device build без signing | `BUILD SUCCEEDED` | PASS CI |
| FIN-IOS-BLD-003 | P0 | Release device build без signing с HTTPS URL | `BUILD SUCCEEDED` | PASS CI |
| FIN-IOS-BLD-004 | P0 | Release с пустым/plain HTTP/local API URL | Приложение блокирует небезопасную конфигурацию | PASS automated/static |
| FIN-IOS-TST-001 | P0 | Полный XCTest | 47/47, 0 failures | PASS CI |
| FIN-IOS-TST-002 | P0 | Launch UI personal-only | Вход/регистрация видимы; `Общее`/`Мой обзор` отсутствуют | PASS CI, 1/1 |
| FIN-IOS-PER-001 | P0 | Account/category/asset list API | Только personal scope, household rows отфильтрованы | PASS automated/static |
| FIN-IOS-PER-002 | P0 | Reports API | `reportMode=personal`, `householdId=nil` | PASS automated/static |
| FIN-IOS-CAT-001 | P1 | Категории | Заголовок `Категории расходов`, только expense active/archive | PASS automated/static |
| FIN-IOS-CAT-002 | P1 | Создание категории | Создаётся `expense` + `personal`, переключателей income/expense и mode нет | PASS automated/static |
| FIN-IOS-SYNC-001 | P0 | HTTP 401 | Сессия/CSRF/identity очищаются, требуется вход | PASS XCTest |
| FIN-IOS-SYNC-002 | P0 | HTTP 403 | Identity, session и pending queue сохраняются | PASS XCTest |
| FIN-IOS-SYNC-003 | P0 | Pending queue после cold start/network error | Очередь сохраняется и доступна для retry | PASS XCTest |
| FIN-IOS-OCR-001 | P0 | OCR boundary | Screenshot/OCR не попадает в local store/pending queue | PASS XCTest/static |

## Обязательные кейсы на Mac и физическом iPhone

| ID | Приоритет | Шаги | Ожидаемый результат | Текущий статус |
| --- | --- | --- | --- | --- |
| FIN-IOS-DEV-001 | P0 | Выбрать Team, уникальный bundle ID, подключить iPhone, Run | Приложение подписано и установлено без App Store | BLOCKED/NOT RUN |
| FIN-IOS-AUTH-001 | P0 | Войти, force quit, открыть снова | Сессия восстановлена, повторный ввод пароля не нужен | BLOCKED/NOT RUN |
| FIN-IOS-AUTH-002 | P0 | Logout, relaunch | Сессия, CSRF, local snapshot и pending queue очищены | BLOCKED/NOT RUN |
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
помечать `NEVER DELETE`. Пароль брать только из owner-managed secret store; не
копировать его в Vault, git, evidence, логи или screenshots.

## Release blocker

Native iOS code/CI ready, но actual production login заблокирован до выбора
trusted HTTPS endpoint. Запрещён произвольный ATS exception. Допустимы:

1. собственный домен/subdomain с публично доверенным TLS и автопродлением;
2. публично доверенный short-lived Let's Encrypt IP certificate с IP в SAN,
   контролем продления и мониторингом срока.

Plain HTTP production IP не является допустимым Release endpoint.

