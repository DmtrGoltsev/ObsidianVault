---
id: "proof-v21-scroll-priority-2026-08-22"
тип: "доказательство"
статус: "развёрнуто"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
источники: ["GitHub Actions run 32551808905", "docs/68-scroll-and-priority-retirement-delivery.md", "docs/33-current-state-summary.md", "android/README.md"]
доказательства: ["Док_Prod_Deploy_State", "Док_Backend_Verification", "Док_Web_Verification", "Док_Android_Verification", "ADR_V21_Release_Backup_Waiver"]
теги: ["доказательство", "v21", "android", "scroll", "compatibility"]
---

# Док: V21 Scroll и Task Priority Retirement

## Граница статуса

V21 развёрнут в production 2026-08-22 из exact source SHA `50a63270ae094fe08ee57b945be0930cb1115dfe` как release `sha-50a63270ae09`. [GitHub Actions run 32551808905](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32551808905) завершился `success`.

## Реализованный контракт

- Android Home/Planner сохраняет stable visible anchor id и pixel offset при expand/collapse, возврате из details, refresh, вставке элементов выше viewport и rotation.
- При удалении anchor используется ближайший сохранившийся parent, затем clamped absolute scroll; переход между верхними вкладками намеренно сбрасывает список к началу.
- Task priority отсутствует в UI и бизнес-логике. API/DB shadow временно сохранена для V20/old APK: create `5`, update сохраняет историческое значение.
- V21 migration меняет только defaults и не переписывает/не удаляет исторические данные.
- Детерминированная сортировка использует date/`createdAt`/`id`; UUID-порядок backend совпадает с PostgreSQL unsigned ordering.
- Четыре runtime-владельца короткоживущего SQLite store закрывают ресурс; lifecycle покрыт тестами.
- Landscape task edit использует compact full-screen `Dialog`, реальный `ScrollView` и IME/system-bar insets; portrait сохраняет прежний `AlertDialog`.

## Автоматические проверки

- Backend: `142/142` PASS.
- Web: `61/61` PASS, production build PASS, dependency audit PASS.
- Android: `testDebugUnitTest` `90/90` PASS; `assembleDebug` PASS; `lintDebug` PASS (`0` errors, `34` existing warnings); `assembleDebugAndroidTest` PASS.

## Visual evidence

- Scroll: `C:\Users\style\AppData\Local\Temp\RocketFlow-QA-V21-20260821-180623\android-ui-20260821-182719\terminal-report.md`.
- Priority compatibility/UI: `C:\Users\style\AppData\Local\Temp\RocketFlow-QA-V21-20260821-180623\followup-terminal-20260821-231308`.
- IME: `C:\Users\style\AppData\Local\Temp\RocketFlow-Visual-QA-20260822-005335\executor-ime-followup-20260822-005854\qa-run-20260822-010539`; portrait, landscape Title и landscape Details PASS при открытой клавиатуре.

Последний IME rerun не повторял anchor/logcat. Предыдущий отдельный anchor QA остаётся PASS; IME diff не менял anchor-код. Эти два набора evidence дополняют друг друга и не считаются одним полным rerun.

## Production rollout evidence

- Backend и web promoted совместно один раз; duplicate promotion отсутствует.
- Flyway перешёл `20 -> 21`.
- Backend health и web вернули HTTP `200`.
- Authenticated disposable API smoke PASS; cleanup PASS, HTTP `5xx` — `0`.
- Rollback не выполнялся.
- Fresh DB recovery point отсутствует: одноразовый exact-SHA waiver [[ADR_V21_Release_Backup_Waiver]] consumed при этом rollout и не является precedent.
- V20 application rollback artifact существовал, но не использовался; будущий permanent gate [[Задача_Production_Deploy_Backup_Rollback]] остаётся открытым.
- Personal Android delivery зафиксирована отдельно в [[Док_Android_Verification]].

## Связанные заметки

- [[ADR_Отказ_От_Приоритета_Задач]]
- [[Док_Android_Verification]]
- [[Док_Backend_Verification]]
- [[Док_Web_Verification]]
- [[Док_Prod_Deploy_State]]
- [[ADR_V21_Release_Backup_Waiver]]
- [[Задача_Production_Deploy_Backup_Rollback]]
