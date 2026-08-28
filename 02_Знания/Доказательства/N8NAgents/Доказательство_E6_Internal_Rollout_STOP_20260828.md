---
id: "evidence-n8nagents-e6-internal-rollout-stop-20260828"
тип: "доказательство"
статус: "STOP"
проект: "N8NAgents"
создано: "2026-08-28"
обновлено: "2026-08-28"
уверенность: "высокая"
источники:
  - "[[N8NAgents]]"
доказательства: []
теги: ["n8nagents", "vps", "internal-rollout", "stop", "docker-compose"]
---

# E6 internal rollout — STOP на bind-source boundary

## Итог

Internal rollout остановлен до миграций и запуска n8n. Exact preflight исправленного reviewed commit прошёл, однако `deploy.sh --bootstrap` завершился с ошибкой при старте PostgreSQL: Compose разрешил относительные bind sources от release root, а файлы находятся под `infra/`. Automatic activation recovery вернула durable tuple в `OLD=NONE`; activation journal очищен. Retry, patch release, cleanup и public-edge действия не выполнялись.

## Exact authority и package

| Поле | Значение |
|---|---|
| Commit | `653f0e36014ba824057f2a23fefac99d0618255d` |
| Tree | `701f109a00206070eb7435324d29477f6c4da891` |
| Canonical archive SHA-256 | `0ed33963694a6568eb6e51f34fa54d9d9349bafe9421669d3d51c2e339fccf8b` |
| Archive size/files | `156907` bytes / `141` files |
| Remote archive | `/srv/.incoming-n8nagents-20260828T060500Z-653f0e36014ba824057f2a23fefac99d0618255d.tar.gz` |
| Remote release | `/opt/n8n-stack/releases/20260828T060500Z-653f0e36014ba824057f2a23fefac99d0618255d` |
| Candidate manifest SHA-256 | `7952b0637487dcb80fac665feb1b2af06ed0c212cb93b834f2a1cb533dd0eb49` |

До deploy server-side gates имели `PASS`: archive policy `171` members / `141` regular files, manifest bytes/modes, secret-like scan, восемь inactive workflows и fail-closed bindings. Исправленный preflight выдал:

```text
resource-plan steady=1275068416 reserve=402653184 required=1677721600
PASS: production preflight
```

## Legacy adoption evidence

Legacy release не объявлялся trusted rollback tuple. Исходный symlink физически сохранён:

- `/opt/n8n-stack/shared/state/legacy-current-20260828T061000Z.symlink` → `/opt/n8n-stack/releases/20260826T115345Z-f6e0c745ab889c11df1ab83ccf7957534be600cd`;
- immutable record `/opt/n8n-stack/shared/state/legacy-adoption-20260828T061000Z.record`, SHA-256 `0085d99f832af0978520bf4c26296b72c41a8251655e044c642a81e552bf3d29`;
- immutable evidence `/opt/n8n-stack/shared/evidence/20260828T061000Z-legacy-adoption-653f0e3`, index SHA-256 `cf52493571ff189cf706fe9233d6bca4adb2cb6e1b237dbbc6b6f9f5067e0628`;
- исходные legacy releases и `/opt/n8n-stack/shared/.env` не удалялись и не перезаписывались.

До adoption также сохранён immutable redacted snapshot `/opt/n8n-stack/shared/evidence/20260828T045641Z-predeploy-00e521f`, index SHA-256 `4fe867ac7e5bd79beb23fce4131eb4354ac0be7316360196139739293ca2cfbd`.

## Точная причина STOP

`infra/operations/lib.sh` запускает Compose с `--project-directory "$compose_release"`, то есть release root. При этом `infra/compose.yaml` использует `./postgres/...`, `./entrypoints` и `./Caddyfile`. Фактические bind sources стали:

```text
<release>/entrypoints -> /production-entrypoints
<release>/postgres/init/00-bootstrap.sh -> /docker-entrypoint-initdb.d/00-bootstrap.sh
<release>/postgres/migrations -> /migrations
<release>/postgres/healthcheck/check-foundation.sh -> /healthcheck/check-foundation.sh
```

Ожидаемые файлы находятся соответственно под `<release>/infra/...`. Docker создал отсутствующие sources как пустые каталоги внутри release. PostgreSQL завершился с `EXIT=2`, `OOM=false`, `RestartCount=6`, `health=unhealthy`; bounded log повторял только:

```text
/bin/sh: can't open '/production-entrypoints/postgres-secrets.sh': No such file or directory
```

Из-за автоматически созданных unmanifested каталогов release `653f0e3` теперь является сохранённым failure artifact и не может повторно считаться exact manifest tree.

## Recovery и фактическое состояние

- `/opt/n8n-stack/current` отсутствует; legacy symlink сохранён по versioned path выше.
- `activation-transaction`, `current-mode`, `previous-release`, `previous-mode` отсутствуют.
- PostgreSQL container остановлен: `Exited (2)`; n8n и Caddy containers не создавались.
- Слушает только SSH; `80`, `443`, `5432`, `5678`, `2375`, `2376` закрыты.
- Host OOM counter остался `0`.
- Миграции `001–008`, sentinels, workflow import и owner gate не выполнялись.
- Immutable config snapshot сохранён в `/opt/n8n-stack/shared/release-config/26a27ddfaa1101714aaeb1746dfcb56729b6bf524f23c715f2ed9944e77d91fd/`; `config.env` SHA-256 `9373e8e7902382b064dce14eae210f388b0aec4f3b4cf23fbe9413cc24d7dbe5`, `images.tsv` SHA-256 `170d658f315b17a60f137aeb2cd77ca17247dffc440b2f29f2e73bda213f98e9`.

Созданный volume `n8nagents_postgres_data` сохранён. Его `_data` имеет `0` entries, `0` files, `0` directories и не содержит `PG_VERSION`, `base`, `global` или `pgdata`: database initialization не начиналась. Несмотря на доказанную пустоту, volume не следует автоматически переиспользовать. До нового reviewed runbook admission он считается quarantined failure artifact; удаление запрещено без отдельного разрешения.

## Требуемое corrective closure

Новый exact candidate должен одновременно:

1. согласовать Compose project directory и все bind-source пути, сохранив проверяемую runtime binding identity;
2. preflight-проверять существование, тип, ownership и expected file/directory shape каждого bind source до любого `compose up`;
3. доказывать, что Docker не может создать unmanifested paths внутри release;
4. иметь fresh-host regression с реальным Compose render/create для PostgreSQL, db-migrate, n8n и Caddy bind sources;
5. явно решить судьбу quarantined empty volume и legacy-pointer reversal без удаления evidence.

До нового exact commit/archive, полного gate suite и независимого GO E6 остаётся `STOP`. Public edge, DNS, firewall/SSH hardening, Telegram, DeepSeek, owner creation и workflow activation не разрешены этим evidence.

## Связи

- [[N8NAgents]]
- [[MOC_N8NAgents]]

