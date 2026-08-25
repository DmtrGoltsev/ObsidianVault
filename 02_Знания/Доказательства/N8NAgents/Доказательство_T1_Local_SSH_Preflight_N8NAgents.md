---
id: "evidence-n8nagents-t1-local-ssh-preflight-20260825"
тип: "доказательство"
статус: "утверждено"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-25"
обновлено: "2026-08-25"
уверенность: "высокая"
источники:
  - "[[Источник_Мастер_Промпт_N8NAgents]]"
  - "[[Промпт_N8NAgents_v1_2026-08-25]]"
доказательства: []
теги: ["n8n", "ssh", "preflight", "acl", "fingerprint", "безопасность"]
---

# T1 — local SSH-preflight N8NAgents

## Что доказывается

Локальные SSH key-файлы из мастер-промпта существуют, имеют ожидаемый тип, распознаются локальным OpenSSH, соответствуют друг другу по SHA-256 fingerprint и не имеют небезопасного ACL на приватном ключе.

## Границы проверки

- Проверка выполнена только локально на Windows.
- Сеть, DNS, VPS и provider API не использовались.
- Значения private key, derived public key, fingerprint, passphrase, SSH host и SSH user не выводились и не сохранялись.
- SSH key-файлы и их ACL не изменялись.

## Метод проверки

Команды выполнялись с логическими placeholders вместо сохранения чувствительных значений:

- `Test-Path -PathType Leaf <private-candidate>` и `Test-Path -PathType Leaf <public-key>`;
- `Get-Item <key-file>` для размера, типа и признака reparse point;
- `Get-Acl <key-file>` с классификацией owner и ACE без сохранения account name/SID;
- `ssh-keygen -E sha256 -lf <private-candidate>`;
- `ssh-keygen -E sha256 -lf <public-key>`;
- сравнение SHA-256 fingerprint в памяти без вывода его значения;
- `ssh-keygen -y -P '' -f <private-candidate>` без сохранения stdout — только для различения private key и public key; пустая passphrase не подошла, что классифицировано OpenSSH как passphrase-protected key;
- `git status --short --branch` перед записью evidence.

## Результат

| Проверка | Redacted result | Статус |
|---|---|---|
| Файлы существуют и являются обычными файлами | Private: 444 bytes; public: 90 bytes; reparse point отсутствует | PASS |
| Формат private candidate | OpenSSH fingerprint parse exit code `0`; ED25519, 256 bits | PASS |
| Формат public key | OpenSSH fingerprint parse exit code `0`; ED25519, 256 bits | PASS |
| Соответствие пары | SHA-256 fingerprints совпали; сами значения не сохранены | PASS |
| Private-key distinction | `ssh-keygen -y` распознал passphrase-protected private key; empty-passphrase derivation ожидаемо отклонена | PASS |
| Owner private key | Текущий локальный пользователь | PASS |
| ACL private key | Inheritance отключён; explicit allow только текущему пользователю, `SYSTEM` и `Administrators`; широких или посторонних allow ACE нет | PASS |
| ACL public key | Inheritance отключён; публичное чтение допустимо для `.pub` | PASS |
| Отсутствие сетевой активности | SSH/SCP/SFTP, port probe, DNS и provider API не запускались | PASS |

## Итог T1

**PASS** — локальные SSH-предпосылки подтверждены без раскрытия key material и без изменения ключей или ACL.

Passphrase-protected private key потребует локального интерактивного unlock либо заранее настроенного `ssh-agent` после прохождения следующего gate. Passphrase нельзя запрашивать или передавать в чате.

## Незакрытый gate G1

T1 `PASS` **не разрешает SSH-подключение**. До любого обращения к VPS должны быть независимо подтверждены:

1. фактический SSH port;
2. ожидаемый SSH host fingerprint;
3. доступность provider console.

Пока эти три условия не подтверждены, следующий статус — `BLOCKED-EXTERNAL`, а SSH запрещён.

## Верификатор

- Кто проверял: ограниченный SSH Security Engineer subagent
- Роль: local SSH-preflight, read-only

## Известные ограничения

- Passphrase не вводилась; фактический интерактивный unlock не проверялся.
- SSH port, SSH host fingerprint и provider console не проверялись и остаются внешним gate G1.
- Доступ к VPS и read-only discovery не выполнялись.

## Связанные заметки

- [[Задача_Развертывание_N8NAgents]]
- [[Пакет_N8NAgents_Стартовый]]
- [[N8NAgents]]
- [[MOC_N8NAgents]]
