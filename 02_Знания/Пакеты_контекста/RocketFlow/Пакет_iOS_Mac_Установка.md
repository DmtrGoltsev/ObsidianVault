---
id: "pkg-ios-mac-install"
тип: "пакет_контекста"
статус: "активно"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-08-24"
обновлено: "2026-08-24"
уверенность: "высокая"
источники: ["docs/ios-native-mac-codex-install-prompt.md", "docs/72-native-ios-mac-device-handoff.md", "docs/71-native-ios-delivery.md", "ios/README.md", "ios/scripts/mac-preflight.sh", "ios/scripts/mac-verify.sh", "ios/scripts/mac-build-device.sh", "ios/scripts/mac-install-device.sh"]
доказательства: ["Док_iOS_Verification", "Док_Prod_Deploy_State"]
теги: ["пакет_контекста", "ios", "mac", "iphone", "handoff", "rocketflow"]
---

# Пакет контекста: iOS Mac установка

## Назначение

Практическая точка входа для переноса RocketFlow на другой Mac, локальной
подписанной сборки и установки на личный iPhone. Полный копируемый сценарий для
нового чата Codex находится в canonical
[`docs/ios-native-mac-codex-install-prompt.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/ios-native-mac-codex-install-prompt.md),
человеческий handoff — в
[`docs/72-native-ios-mac-device-handoff.md`](https://github.com/DmtrGoltsev/RocketFlow/blob/99172cd171e8cade0545fb442c9233961c7865d1/docs/72-native-ios-mac-device-handoff.md).

## Текущая identity

- Проектная ветка: `codex/native-ios-companion`.
- Финальный docs HEAD: `99172cd171e8cade0545fb442c9233961c7865d1`.
- Immutable tooling commit A:
  `a66b501f2a5ec8d8d25dc518a9fcd097e5ee1149`.
- Tooling evidence: [run 32669924719](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32669924719),
  job `97269056380`; Mac contracts `174/174` PASS, `0` skipped;
  XcodeGen `2.46.0`, project parity, packages и simulator build PASS;
  unit `540/0`, UI `2/0`, всего `542/0`.
- Tooling artifacts: `RocketFlow-xcresult`, ID `9501177125`, `1,317,064`
  bytes; `RocketFlow-xcodeproj-xcodegen-2.46.0`, ID `9501179599`,
  `25,070` bytes.
- Отдельное behavior/build evidence: SHA
  `35e98d965cf49a356e5a7a7ebdbc59afaa1f9fb3`,
  [run 32655691351](https://github.com/DmtrGoltsev/RocketFlow/actions/runs/32655691351),
  job `97233929959`, `540` unit + `2` UI PASS. Оно доказывает поведение
  приложения, но не подменяет tooling identity.

Exact таблицы доказательств и границы утверждений: [[Док_iOS_Verification]].

## Порядок на другом Mac

1. Clone/fetch repository и checkout/pull последнего состояния
   `codex/native-ios-companion`; не требовать, чтобы HEAD совпадал с tooling SHA.
2. Доказать, что tooling commit A является ancestor текущего checkout, а exact
   tooling paths из canonical prompt не менялись после A.
3. Открыть новый чат Codex на Mac и передать ему целиком canonical Mac prompt.
   Сначала выполняются чтение `AGENTS.md`, audit и сверка script `--help`; без
   доказанного blocker source не меняется.
4. Запустить simulator verification через `mac-verify.sh`. После green gate
   добавить Apple Account только в Xcode UI и создать локальный
   `ios/Config/Device.xcconfig` из example. Если файл уже существует, не
   перезаписывать: остановиться и переиспользовать только после осознанной
   проверки. Файл обязан оставаться ignored и untracked.
5. Пользователь локально выбирает только Team, уникальный owner-controlled
   bundle ID и подключённый iPhone. Затем выполняются documented
   `mac-preflight.sh`, `mac-build-device.sh`, `mac-install-device.sh` и smoke
   checklist.
6. Default режим — `no-push`: signed personal development `.app`, установка и
   launch через `devicectl`; при его сбое допустима установка того же готового
   `.app` через Xcode Devices and Simulators. Это не альтернативная сборка.
7. Режим `push` только optional и только после отдельного согласия и локальной
   настройки Firebase/APNs; отсутствие push prerequisites не блокирует
   успешный `no-push` handoff.

## Безопасность и границы

- Не переносить в чат, Git, vault или публичные logs пароли, 2FA, Team ID, UDID,
  certificates, profiles, private keys, Firebase/APNs credentials, токены и
  `GoogleService-Info.plist`.
- Не выполнять Archive/IPA/App Store release, backend deploy, Flyway migration
  или production DB verification в рамках Mac/iPhone handoff.
- Production backend остаётся на SHA
  `50a63270ae094fe08ee57b945be0930cb1115dfe`, Flyway V21. Candidate V22 для iOS
  device registrations существует только в candidate и не deployed; DB в этой
  актуализации не проверялась.
- На `origin/master` trigger fix действует с commit
  `c0682493c93ac2d8ff1d31bca9e1b1c2546b3c56` (2026-08-24): Android,
  Backend и Web success runs `32766368686`, `32766368744`, `32766368663`;
  iOS/deploy/publish не запускались. Candidate `99172cd` имеет эквивалентную
  политику через `0bbf4acb`; старые другие branches автоматически не исправлены.
- Physical iPhone build/install/launch ещё не доказаны. Статус изменяется только
  после redacted evidence с Mac; green CI доказывает tooling/simulator gate, а не
  physical device, push или App Store readiness.

## Связанные заметки

- [[Пакет_iOS]] — общий iOS-контекст
- [[MOC_iOS]] — карта native iOS
- [[Агент_iOS]] — роль исполнителя
- [[Док_iOS_Verification]] — immutable CI evidence
- [[Источник_Текущее_Состояние]] — общий current state
- [[Док_Prod_Deploy_State]] — production V21 boundary
