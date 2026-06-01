---
id: "rg-github-agents"
тип: "регламент"
статус: "утверждено"
проект: ""
владелец: "rocketflow-team"
создано: "2026-06-01"
обновлено: "2026-06-01"
уверенность: "высокая"
источники: []
доказательства: []
теги: ["регламент", "github", "git", "агент", "ssh"]
---

# Регламент: Работа с GitHub для агентов

Обязателен к исполнению всеми агентами при работе с любым Git-репозиторием.

---

## 1. Аутентификация

Протокол: **SSH**. Ключ: `~/.ssh/id_ed25519.pub`.

### Проверка доступа
```bash
ssh -T git@github.com
# Ожидается: Hi <username>! You've successfully authenticated...
```

### Если доступ не работает
1. Сгенерировать ключ: `ssh-keygen -t ed25519 -C "agent@rocketflow"`
2. Добавить в GitHub: https://github.com/settings/keys → New SSH Key
3. Проверить: `ssh -T git@github.com`

### gh CLI
Установлен: `winget install GitHub.cli`  
Авторизация: `gh auth login` → GitHub.com → SSH → выбрать `~/.ssh/id_ed25519.pub`  

---

## 2. Именование веток

Формат: `agent/<среда>/<задача>`

| Компонент | Значение | Пример |
|-----------|----------|--------|
| `<среда>` | opencode / deepseek / codex / claude | `opencode` |
| `<задача>` | краткий slug задачи (kebab-case) | `obsidian-memory-rules` |

Примеры:
- `agent/opencode/obsidian-vault-init`
- `agent/deepseek/android-task-steps`
- `agent/codex/backend-api-fix`

---

## 3. Preflight (перед началом работы)

```bash
git status                        # репозиторий?
git branch --show-current         # какая ветка?
git status --short                # чужие незакоммиченные изменения?
```

**Стоп-правила:**
- Если `main`/`master`/`develop`/`release/*` → создать новую ветку
- Если чужие незакоммиченные изменения → остановиться, спросить
- Если не Git-репозиторий → инициализировать по [[Регламент_Добавление_Проекта]]

---

## 4. Рабочий цикл

```bash
# 1. Создать ветку
git checkout -b agent/opencode/my-task

# 2. Работать — изменять только файлы задачи

# 3. Проверить изменения
git diff --stat

# 4. Закоммитить
git add <файлы>
git commit -m "<тип>: краткое описание"

# 5. Запушить
git push -u origin agent/opencode/my-task
```

### Формат коммитов
```
<тип>: <описание>

<детали если нужно>
```

Типы: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`

---

## 5. Запрещено без явного разрешения

- ❌ `git merge`
- ❌ `git rebase`
- ❌ `git push --force`
- ❌ `git reset --hard`
- ❌ Коммиты в `main`/`master`
- ❌ `git push` в основную ветку
- ❌ Изменение файлов другого агента (если задача не про интеграцию)

---

## 6. Работа с Obsidian vault как Git-репозиторием

Vault — это обычный Git-репозиторий. После инициализации доступен по SSH.

### Клонирование
```bash
git clone git@github.com:<user>/<repo>.git
```

### Синхронизация перед работой
```bash
cd ObsidianVault
git checkout main
git pull origin main
git checkout -b agent/opencode/my-task
```

### Фиксация изменений в vault
```bash
git add -A
git commit -m "docs: обновление структуры vault, добавление ADR"
git push -u origin agent/opencode/my-task
```

### Создание нового Git-репозитория для проекта
```bash
cd <папка-проекта>
git init
git config user.name "Codex"
git config user.email "codex@local"
echo -e "# Secrets\n.env\n*.pem" > .gitignore
git add -A
git commit -m "Initial commit"
gh repo create <имя-репо> --public --source=. --remote=origin --push
```

---

## 7. Параллельная работа нескольких агентов

- Каждый агент — в своей ветке
- При конфликте файлов — использовать `git worktree`:
  ```bash
  git worktree add ../obsidian-agent2 agent/opencode/task-2
  ```
- Не редактировать файлы, изменяемые другим агентом
- Интеграцию выполняет оркестратор или назначенный интегратор

---

## 8. Завершение задачи — отчёт агента

Вернуть оркестратору:
```markdown
## Git-отчёт
- **Ветка:** agent/opencode/my-task
- **Коммиты:** <sha1> <sha2>
- **Изменённые файлы:** <список>
- **Команды проверки:** <список>
- **Результат:** пройдено / ошибки
- **Конфликты:** есть / нет
- **Оставшаяся работа:** <описание>
```

---

## Связанные заметки
- [[Регламент работы агента]] — общие правила работы агента
- [[Регламент Git-изоляции агентов]] — правила изоляции веток
- [[Регламент_Добавление_Проекта]] — добавление нового проекта в vault
