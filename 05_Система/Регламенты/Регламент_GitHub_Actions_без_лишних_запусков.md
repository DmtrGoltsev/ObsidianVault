---
id: "rg-github-actions-trigger-policy"
тип: "регламент"
статус: "утверждено"
проект: ""
владелец: "knowledge-base"
создано: "2026-08-24"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["GitHub Actions: Triggering a workflow", "GitHub Actions: Workflow syntax", "GitHub Actions: Notifications for workflow runs", "GitHub Actions: Workflow concurrency", "GitHub Actions: Managing environments for deployment", "GitHub: About protected branches"]
доказательства: []
теги: ["регламент", "github-actions", "ci", "уведомления", "workflow"]
---

# Регламент: GitHub Actions без лишних запусков

Обязателен для новых проектов и при устранении повторяющихся GitHub Actions failure emails в существующих репозиториях. Цель — убрать ненужные запуски, сохранив полезные уведомления о настоящих сбоях CI.

## Канонические источники

- [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Notifications for workflow runs](https://docs.github.com/en/actions/concepts/workflows-and-actions/notifications-for-workflow-runs)
- [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [About protected branches and required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

## Корневая причина почтового потока

Запись `on: push` без `branches`/`tags` filters запускает workflow для push-событий branch и tag refs. Если одинаковое событие слушают несколько verify-workflows, один push создаёт несколько независимых runs и потенциально несколько failure notifications. Повторные push и дублирующие workflows дополнительно увеличивают поток.

Исправление workflow в candidate или feature branch не меняет действующую политику default branch до доставки изменения в default branch. Кроме того, старая существующая ветка может содержать собственную прежнюю ревизию workflow и продолжать запускать её при подходящем событии. Такие ветки нужно явно обновить исправлением или удалить/закрыть после подтверждения, что они больше не нужны.

## Сначала отличить лишний запуск от настоящего сбоя

Не считать каждое письмо шумом. Уведомление является ожидаемым, если run создан:

- вручную через `workflow_dispatch`;
- для pull request в default branch;
- после push/merge в default branch;
- утверждённым release/deploy событием;
- расписанием или другим явно документированным событием.

В таком случае нужно исправить тест, сборку, инфраструктуру или сам workflow. Отключение уведомлений не устраняет причину и не является CI-исправлением.

## Инвентаризация и диагностика

1. Определить default branch и текущую ветку:

```bash
gh repo view --json defaultBranchRef,nameWithOwner
git branch --show-current
git status --short
```

2. Найти все workflow и все триггеры, включая косвенные:

```bash
find .github/workflows -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) -print
rg -n '^on:|^\s+(push|pull_request|pull_request_target|merge_group|workflow_dispatch|workflow_run|schedule|repository_dispatch):' .github/workflows
```

3. Сопоставить runs с workflow, событием, веткой и SHA:

```bash
gh run list --limit 50 --json databaseId,name,event,headBranch,headSha,status,conclusion,createdAt,url
gh run view <run-id> --json name,event,headBranch,headSha,status,conclusion,url,jobs
```

4. Проверить все причины умножения runs:

- голый `push` или широкие branch/tag patterns;
- одновременно `push` и `pull_request` для feature branch;
- несколько файлов workflow с одинаковой полной матрицей проверок;
- `workflow_run`, `repository_dispatch`, PAT или GitHub App, создающие следующий run;
- ошибочный подсчёт matrix jobs как отдельных workflow runs: matrix разворачивает jobs внутри одного run и сама по себе не объясняет множество runs или писем; сравнивать нужно `run id`, `workflow name`, event и ref;
- включённая merge queue без инвентаризированного `merge_group` event;
- старые ветки с прежней копией `.github/workflows/`;
- повторные push при уже выполняющемся run без политики обработки устаревших вычислений.

## Рекомендуемый verify-контракт

Подставить реальное имя default branch: `main`, `master` или другое значение из настроек репозитория.

```yaml
on:
  workflow_dispatch:
  pull_request:
    branches:
      - <default-branch> # например main или master
  push:
    branches:
      - <default-branch> # например main или master
```

Контракт означает:

- обычный push в feature/codex branch не запускает полную verification;
- pull request, нацеленный в default branch, запускает обязательные проверки;
- merge/push в default branch запускает полную проверку итогового состояния;
- ручной диагностический запуск остаётся доступным.

`workflow_dispatch` получает события только когда соответствующий workflow существует в default branch. Поэтому новую ручную политику нельзя считать действующей до её доставки туда.

### Required-check baseline для merge queue

Если для default branch включена merge queue, каждый workflow, публикующий required check, обязан дополнительно слушать `merge_group`:

```yaml
on:
  workflow_dispatch:
  pull_request:
    branches:
      - <default-branch>
  merge_group:
    types:
      - checks_requested
  push:
    branches:
      - <default-branch>
```

Без merge queue событие `merge_group` не требуется. При включённой queue одного `pull_request` недостаточно: required checks должны публиковаться и для временного merge-group commit.

## Verify и deploy разделены

Verify-workflow не должен неявно выполнять production deployment. Deploy/package/publish workflow требует одновременно:

- ограниченный и документированный trigger, например `workflow_dispatch` или узко разрешённая release branch/tag;
- protected GitHub environment с подходящими deployment branch/tag rules;
- минимальные `permissions` для workflow/job;
- required reviewer/approval или другая environment protection rule, где функция доступна и применима к проекту.

Это совместные уровни защиты, а не взаимоисключающие альтернативы. Один `workflow_dispatch` или branch filter без environment/permissions review не считается достаточной production-защитой. Изменение verify-триггеров не должно менять deploy secrets, environments, permissions, миграции, rollback или production branch filters.

## Concurrency и отмена устаревших runs

Для verify допустимо отменять более старый run той же ветки или PR:

```yaml
concurrency:
  group: verify-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

Concurrency экономит runner time и прекращает устаревшие вычисления, но не гарантирует меньше уведомлений. Отменённый run сохраняет отдельный run/conclusion и в зависимости от пользовательских настроек тоже может уведомлять. Поэтому `concurrency` не считается исправлением email storm и не заменяет правильные triggers. Для production deploy `cancel-in-progress: true` нельзя добавлять автоматически: прерывание деплоя может быть опасным и требует отдельного проектного решения.

## Дублирующие workflows

Каждый workflow должен иметь уникальную ответственность. Если backend, web, Android и iOS требуют разных runners или команд, отдельные lanes допустимы. Если несколько файлов повторяют одну полную проверку на одном событии, объединить их либо вынести общую реализацию в reusable workflow. После изменения сверить имена checks с branch protection.

## Required checks и path filters

GitHub предупреждает: workflow, пропущенный из-за branch/path filter или commit message, может оставить связанный required check в состоянии `Pending` и заблокировать merge. Поэтому `paths`/`paths-ignore` для required PR checks добавляются только после проверки branch protection и доказательства, что check публикуется для каждого PR.

Безопасный базовый вариант — не ставить workflow-level path filters на обязательный PR workflow. Экономию можно реализовать внутри jobs с явным успешным агрегирующим check либо отдельным архитектурным решением и контрактными тестами.

## Политика доставки одного исправления

Чтобы само исправление не создало новый поток писем:

1. Собрать полную инвентаризацию до первого изменения.
2. Изменить triggers всех затронутых verify-workflows одним согласованным commit.
3. Не смешивать с feature-кодом, deploy, secrets, environments или переименованием checks.
4. Локально проверить YAML и статический trigger-контракт.
5. Один раз push candidate commit и проверить фактические runs.
6. Одним PR/merge доставить commit в default branch либо использовать direct fast-forward только когда он явно разрешён protection policy и владельцем репозитория.
7. Не делать повторные пустые push ради проверки.
8. После merge обновить или закрыть старые ветки с прежней ревизией workflow.

Пусть `N` — число verify-workflows, matching конкретное событие после исправления. Ожидаемая арифметика доставки:

- **PR path:** candidate push до открытия PR создаёт `0` Verify runs; открытие/синхронизация PR создаёт `N` pull-request runs; каждый новый commit в открытом PR создаёт ещё `N`; merge создаёт `N` default-branch push runs.
- **Merge queue:** при включённой queue каждый `merge_group/checks_requested` создаёт дополнительно `N` merge-group runs для required-check workflows.
- **Direct fast-forward:** только при явном разрешении создаёт `N` default-branch push runs один раз, без PR runs.

Это ожидаемые проверки, а не email count: количество и каналы уведомлений зависят от настроек GitHub и conclusions runs.

## Матрица проверки

| Сценарий | Ожидаемый результат |
|---|---|
| Push в новую feature/codex branch | `0` автоматических verify runs |
| Повторный push в ту же feature branch | `0` автоматических verify runs |
| Manual `workflow_dispatch` | Ровно один выбранный workflow run |
| Первый PR commit в default branch | `N` PR runs; все заявленные required checks публикуются |
| Каждый новый commit в открытом PR | Ещё `N` PR runs |
| Merge/push в default branch | `N` default-push runs; полная verification |
| Direct fast-forward в default branch | Только при явном разрешении; `N` default-push runs один раз |
| `merge_group/checks_requested` при включённой merge queue | `N` merge-group runs и все required checks для временного merge-group commit |
| Изменение только пути, исключённого фильтром | Нет вечного `Pending` required check |
| Два быстрых обновления одного PR | Новый набор `N` runs создан; устаревшие вычисления могут быть отменены concurrency, но снижение уведомлений не гарантируется |
| Verify-only изменение | Deploy/package/publish workflows не запущены |
| Старая активная ветка | Обновлена исправлением либо явно retired |

Финальное доказательство снимается через `gh run list` и `gh run view`: фиксируются event, ref, SHA, число runs, conclusions и отсутствие deploy/publish.

## Stop conditions

Остановиться и эскалировать, если:

- default branch не установлена точно;
- непонятно, какие checks обязательны в branch protection;
- включена или планируется merge queue, но required-check workflows не покрывают `merge_group/checks_requested`;
- workflow объединяет verification и production deploy;
- deploy trigger не дополнен review минимальных permissions и protected environment/approval, где они применимы;
- изменение затрагивает secrets, permissions, environments, migrations или rollback вне утверждённого deploy scope;
- path filters могут оставить required check в `Pending`;
- старые ветки продолжают создавать runs, но их нельзя обновить или удалить;
- один push создаёт runs через неинвентаризированный `workflow_run`, PAT, GitHub App или dispatch;
- нет способа доказать матрицу без production-операции.

## Bootstrap нового проекта

До первого рабочего push:

- [ ] Определена и записана default branch.
- [ ] Составлена таблица `workflow -> event -> branch/tag/merge-group -> назначение`.
- [ ] В verify отсутствует голый или недокументированный feature-branch `push`; специальные release/integration/stacked flows разрешены только через audited allowlist с владельцем, назначением и ожидаемым числом runs.
- [ ] Verify использует `workflow_dispatch`, PR в default и push в default.
- [ ] При merge queue required-check workflows также используют `merge_group/checks_requested`.
- [ ] Deploy/package/publish отделены и одновременно имеют ограниченные triggers, минимальные permissions и protected environment/approval, где применимо.
- [ ] Проверены дубли workflows и косвенные triggers.
- [ ] Решена политика concurrency отдельно для verify и deploy.
- [ ] Required checks согласованы с именами jobs/workflows.
- [ ] Path filters либо отсутствуют, либо покрыты успешным check-контрактом.
- [ ] Добавлена статическая или контрактная проверка trigger policy.
- [ ] Проверена матрица runs до включения почтовых уведомлений команды.

Минимальная статическая проверка должна отклонять голый `push`, неверное имя default branch, недокументированный автоматический feature-branch verify, отсутствие `merge_group` при включённой merge queue и случайное изменение deploy triggers. Разрешённые release/integration/stacked branch flows оформляются только как audited allowlist: точный pattern, владелец, цель, ожидаемые events/runs и срок пересмотра. Предпочтителен YAML parser, а не поиск строк. Контрактный тест должен анализировать все `.github/workflows/*.yml` и выдавать список нарушающих файлов.

## Уведомления

GitHub может отправлять уведомления о workflow runs через web и email в зависимости от пользовательских настроек. Эти настройки регулируют доставку, но не количество runs. Сначала исправляется trigger topology; отключение Actions notifications допустимо только как личное предпочтение после сохранения наблюдаемости настоящих PR/default/deploy failures.

## Связанные заметки

- [[Регламент_GitHub_для_Агентов]] — Git/GitHub preflight и рабочий цикл
- [[Регламент_Добавление_Проекта]] — применение правила при bootstrap проекта
- [[Старт_Агента]] — общая точка входа
