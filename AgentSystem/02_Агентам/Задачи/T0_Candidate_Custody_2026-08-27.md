---
id: "n8nagents-t0-candidate-custody-2026-08-27"
тип: "custody"
статус: "выполнено"
проект: "AgentSystem"
создано: "2026-08-27"
обновлено: "2026-08-27"
---

# T0.1 — custody production candidate

## Результат

- Source Git root: `C:/Users/style/Documents/ChatGPT/Агенты`
- Source project subtree: `N8NAgents/`
- Source branch: `codex/n8nagents-foundation`
- Source HEAD: `11974a33fa78bb72598059671cef9465402ab091`
- Candidate worktree: `C:/Users/style/Documents/ChatGPT/N8NAgents-production-candidate`
- Candidate branch: `codex/n8nagents-production-candidate`
- Candidate HEAD: `11974a33fa78bb72598059671cef9465402ab091`
- Candidate status: clean; никакие dirty-файлы ещё не переносились.
- Source project dirty inventory: `41` файлов (`12` tracked modified, `29` untracked).
- Canonical inventory SHA-256 до и после `git worktree add`: `9c52f3d299fd09c5d5492bd7b60c74cfde050f1d705b8d26ecb6afc77619e623` — совпадает.

Canonical aggregate вычислен по строкам в исходном porcelain-порядке:

```text
status<TAB>path<TAB>bytes<TAB>sha256<TAB>mode<TAB>tracked-lower<TAB>classification<LF>
```

Кодировка UTF-8, LF, ровно один финальный LF. Для tracked-файлов `mode` взят из Git index через `git ls-files -s`; для untracked — mode, который Git на этом Windows worktree с `core.filemode=false` определяет при добавлении нового обычного файла (`100644`). Инвентаризация получена через `git -c core.quotepath=false status --porcelain=v1 -z --untracked-files=all`.

## Правила disposition

- `IMPORT_PRODUCTION` — production/release/governance код и актуальные production-документы для интеграции в candidate после отдельного content review.
- `IMPORT_LOCAL_REGRESSION` — локальная Docker-лаборатория и её deterministic regression harness; это не production runtime.
- `REFERENCE_ONLY` — в этом снимке нет файлов, которым нужен этот disposition.
- `DEFER_K4R_HISTORY` — исторический local verification result; не переносить как актуальное доказательство exact candidate.
- `SECRET_OR_EVIDENCE_EXCLUDED` — placeholder runtime-evidence directory; не переносить. Реальные ignored secret leaves и runtime evidence также исключены.

Итоги: `IMPORT_PRODUCTION=20`, `IMPORT_LOCAL_REGRESSION=19`, `REFERENCE_ONLY=0`, `DEFER_K4R_HISTORY=1`, `SECRET_OR_EVIDENCE_EXCLUDED=1`.

## Exact inventory

| status | path | bytes | SHA-256 | mode | tracked | disposition |
|---|---|---:|---|---:|---|---|
| ` M` | `N8NAgents/docs/deploy-rollback-manifest.md` | 44027 | `e8a484571ec3b9c7700935b601929719081a2c82f52643c3bb44b734d7a4126b` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/docs/local-verification-result.md` | 2312 | `4d3289fe0adc2339eb78f631da787bab9af14c2451c5f5bf52968375d7b406bf` | 100644 | true | DEFER_K4R_HISTORY |
| ` M` | `N8NAgents/docs/verification-matrix.md` | 5934 | `2a284d545a77aad0e83b75c4fbb9a8590ba7426a74fae953ac4710de7897bee6` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/infra/phase-a-compose.sh` | 4564 | `81b70448223bdc2982cd6ad7cb63ffc95a014053e7520432b676fd224b61284d` | 100755 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/infra/phase-a-release-gate.sh` | 26412 | `f5ff1b66ade404fc744646cfc1d01e4f1b7d1e8ba2a39d5d789b7bb26a0cd352` | 100755 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/infra/verify-release-governance.sh` | 13551 | `5ddd4691550ca0e71b2363557a80fc4350a68d61c226a0e02d85fdf192a1f398` | 100755 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/package-reviewed-release.ps1` | 12372 | `4f15af8bb56e581cbc1329a111a43522f80d0e896418e283e436f048703e2c5a` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/test-package-reviewed-release.ps1` | 13251 | `d3c77eb6e6183f908a0c341e8f4f5093b6baff61c40ab6d3695fdce4dda27102` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/test-release-governance.sh` | 1515 | `49b8fe33ce2861b189d44e64912688c6d95d0d494aec6fe3283acfcaf80faca7` | 100755 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/test-remote-package-gate.sh` | 924 | `1d50effa82292a7dde0088c2c87172c61f30dc03626e8b472721a0850dfd58db` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/verify-static.ps1` | 15954 | `75d18062f6d495b90b7e03e333a24219cdcd929d11f1f2bc10ea9fa8c2cd0ace` | 100644 | true | IMPORT_PRODUCTION |
| ` M` | `N8NAgents/scripts/verify-static.sh` | 1074 | `3f908f1e0c4baccca114ba2d94ea7b07767f7faf43688e6fbec55e80c355a8d5` | 100755 | true | IMPORT_PRODUCTION |
| `??` | `N8NAgents/infra/phase-a-runner-bootstrap.sh` | 13763 | `462f708e55e8c7dac3a6b89e5b40e49052ba0940ab96de90a26726a0867f9947` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/local/.env.example` | 11 | `3a856f828e45a8c3e64cb17c9732a7fc68f307b48e793e657ccd3ba7ffb88113` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/.gitignore` | 71 | `9b56f68efc38ca6fee7ae55c12daf80b19705f27f5b2cdaf34463b5aaf669924` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/README.md` | 3337 | `5b8fd8ff8c9860a42c349499eb34b2d1eb6b8204ce3635490257931126d3e66f` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/bridge/bridge.mjs` | 6854 | `a88a51e9e9351f4dabb371a692a947aa6fb3ccb766bdb28243a71f4c491b670e` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/bridge/core.mjs` | 2767 | `3930ff4007666a8e59c4c7bdc8640ea0774eb91185fb12759e0d89aeff6eb675` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/compose.yaml` | 12304 | `522f4b2617b8a0cfa570283d67854ee385bad513682d3c7c973039ec135e8e4b` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/entrypoints/n8n-secrets.sh` | 604 | `48e1ea32a93612a619702f8d9f438134c03a12cb45df272fa4c5b29f6d1c109a` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/entrypoints/postgres-secrets.sh` | 665 | `16253654efaa3257d543505f9f8eea8780d1609e9d35f015365d1863ede48015` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/evidence/.gitkeep` | 1 | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | 100644 | false | SECRET_OR_EVIDENCE_EXCLUDED |
| `??` | `N8NAgents/local/mock/http-utils.mjs` | 565 | `b00a111a93e426abfc75dd1e6bb212b81bcbc2a5a25616a034ecbb059f22b237` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/mock/telegram-mock.mjs` | 1869 | `32f2a873cec9d4218f3e746ef9f0ea1d0828c6d6d8e98189b06fc327a2e9e8ed` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/mock/workflow-mock.mjs` | 1210 | `8aa7b7a21bb0a37519737617d39f00e4b0d1ae6893975d58309d1b2a2d5d8b30` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/n8nagents-local.ps1` | 6849 | `f665e0fce9190c3e18ba8d3773c8d66aae5c24681950683aa361657846484b7a` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/proxy/n8n-loopback-proxy.mjs` | 1599 | `1d96fbab5a4d45aaa9999cc3bd0e71791e4c9deb31972d9d9cc5a0728dc1c506` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/secrets/README.md` | 457 | `3b09e17ceeb90141fc0d9c826614721f304babfa0745dd8d73c04f20f723c8ff` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/tests/bridge-core.test.mjs` | 1896 | `b36af897929098b62dfaab87b7f1f409b6090ca7ff4bf90b20d2d6b4f98b8b3d` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/tests/docker-mock-test.mjs` | 2596 | `3ccf7dc3ced6dd0c0dbcf920b85467e12dc77d8cec95fc682a93bd1a14d8f61a` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/tests/run-static.ps1` | 846 | `b3d5550c0142462d55bf5af5cbcc0049a13bd5af604200d31dd0df8835c80074` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/tests/static-contract.test.py` | 2811 | `754227499fd1083e9edae712aea66fc9fc5ea44d8eda8d7a0b7de00176ea5547` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/local/workflows/telegram-local-reply.json` | 1895 | `a5e5b0b0be04cf48d176aa818c75f49eea562e43f5dae76a11d7d581d965e07d` | 100644 | false | IMPORT_LOCAL_REGRESSION |
| `??` | `N8NAgents/scripts/build-k4r-evidence.py` | 36086 | `918ceb8194dbbb643b1ea11f3bb29d41779d3a80ddb27c3491eb135265e6f2d0` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/build-reviewed-candidate.ps1` | 4900 | `a53d9540e256e8cd95ee3ff6c236ce41c030c55a13950579000143550dae9c0c` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/lib/GitTreeValidation.psm1` | 11076 | `967fb9fc0270a0f2c346136f363c7787d8e89744ed9b2cef7ef64fc52308ef83` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/requirements-k4r.lock` | 148 | `8e31f28c4eb60f44cf36e5d84556214feef3208fd3322d9ea8e9cc520c0b8e04` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/run-k4r-offline.ps1` | 7470 | `b8973ca114d1e0f44feae16736e020bc07d5adb8626b183ea4ff26d9eb8fed0c` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/test-k4r-evidence.py` | 7749 | `8ee2dcf6d9cb13ca05f817652c95cd814e16c6446521e6b9c5431f15f925287f` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/test-phase-a-release-gate-linux.sh` | 40454 | `d098c071c1cd06ba7e42ef788e3d60d1211260008424fcc0ffda62b03ecfb84a` | 100644 | false | IMPORT_PRODUCTION |
| `??` | `N8NAgents/scripts/test-runner-bootstrap-linux.sh` | 5448 | `98406f61f8bd42d4cf224693f2568143ebe2179f9617fa857643843612a0f22a` | 100644 | false | IMPORT_PRODUCTION |

## Secret/evidence exclusion proof

- Source local secret directory содержит `9` runtime secret leaves; все девять подтверждены как ignored и ни один не присутствует в porcelain inventory.
- Source local evidence directory содержит `2` runtime evidence files; оба ignored и не присутствуют в porcelain inventory.
- `local/secrets/README.md` не является secret leaf: это только инструкция без значения секрета; он классифицирован как local regression documentation.
- `local/evidence/.gitkeep` не содержит evidence, но исключён из candidate disposition, чтобы не переносить runtime-evidence subtree механически.
- Candidate остаётся точным clean checkout исходного HEAD: tracked `N8NAgents/local/**` в нём нет; path scan по secret/evidence leaf patterns дал `NONE`.
- Значения secret leaves не читались, не хешировались и не записывались в эту заметку.

## Source preservation after worktree creation

Повторный inventory только для исходного project subtree `N8NAgents/` дал те же `41` строки и тот же aggregate SHA-256 `9c52f3d299fd09c5d5492bd7b60c74cfde050f1d705b8d26ecb6afc77619e623`. Следовательно, все исходные dirty-файлы побайтно сохранены.

Первоначально worktree был создан по адресу `C:/Users/style/Documents/ChatGPT/Агенты/N8NAgents-production-candidate`, который после path-resolution оказался внутри source Git root. До исправления он был clean, находился на exact HEAD и воспроизводимо удалялся штатной командой `git worktree remove` без `--force`. Этот зарегистрированный clean worktree удалён и заново создан на той же ветке и том же HEAD по внешнему адресу `C:/Users/style/Documents/ChatGPT/N8NAgents-production-candidate`.

После исправления новый path не находится внутри source root, candidate clean, старый path отсутствует, а исходный raw `git status --porcelain=v1 -z --untracked-files=all` снова содержит ровно исходные `41` project paths без административной записи candidate worktree. Aggregate остался `9c52f3d299fd09c5d5492bd7b60c74cfde050f1d705b8d26ecb6afc77619e623`.

## Blockers / ограничения следующего шага

- Custody blocker отсутствует: ветка и worktree созданы от exact HEAD, candidate clean, source project aggregate сохранён.
- До content review перенос запрещён: эта операция только создала custody boundary и disposition register.
- `20` production-файлов и `19` local-regression файлов требуют отдельного controlled import; K4R historical evidence и runtime evidence/secrets импортировать нельзя.
- Исправленный candidate path расположен вне source Git root; nested-path caveat устранён. `.git/info/exclude` не менялся.

## Placement correction attestation

- Old registered path: `C:/Users/style/Documents/ChatGPT/Агенты/N8NAgents-production-candidate`.
- Old path inside source root: `true`.
- Old status before removal: clean; HEAD `11974a33fa78bb72598059671cef9465402ab091`.
- Removal: exact registered worktree, `git worktree remove`, no `--force`; старый path после удаления отсутствует.
- New registered path: `C:/Users/style/Documents/ChatGPT/N8NAgents-production-candidate`.
- New path inside source root: `false`.
- New branch/HEAD: `codex/n8nagents-production-candidate` / `11974a33fa78bb72598059671cef9465402ab091`.
- New status: clean.
- Source raw status after correction: `41` paths, `12` tracked modified + `29` untracked, candidate administrative records `0`, staged/index `0`.
- Source inventory aggregate after correction: `9c52f3d299fd09c5d5492bd7b60c74cfde050f1d705b8d26ecb6afc77619e623`, exact match.
