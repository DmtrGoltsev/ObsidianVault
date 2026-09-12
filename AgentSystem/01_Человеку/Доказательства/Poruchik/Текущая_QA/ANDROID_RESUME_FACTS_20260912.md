# Android: факты для возобновления QA

Этот файл — краткая база знаний для нового чата. Канонические матрицы и файл продолжения обновляет назначенный единственный исполнитель документации.

## Подписанный артефакт

- Проверенный final16: `C:/BackUp/Poruchik-Signing/Poruchik-MVP0-final16-release-signed-20260911.apk`.
- SHA-256: `6218012f6751d088a210c27a1e7898c522fbd1ca28ff92eea25990e29eecd142`.
- Старый совместимый release: `C:/BackUp/Poruchik-Signing/Poruchik-MVP0-network-phase-release-signed-2026-09-09.apk`, SHA-256 `d1257d142ad6fa56ac6c6e91048a721b6a3206aa5a5857e9a30a8d9035e5e820`.
- Оба: `com.poruchik.app`, versionCode 2, minSdk 26, сертификат `4ca92be4b6682276bae07820b7c725aed5f7ab9af48c9df7c1627b7ecc63224f`.
- Final16 не пересобирать и не подписывать повторно. Продуктовый код этой адресной Android-пачкой не менялся.

## Принятые Android-доказательства

- **ENV01 PASS:** final16 запущен на изолированном API26 AVD.
- **ENV02 PASS:** normal same-cert update old release → final16 на API26 сохранил install identity, PIN-lock и private baseline task.
- **EX018 NOT_RUN:** pending CREATE/UPDATE не заявлять. На API26 три штатных offline-control способа не дали фактического отключения сети: `svc wifi disable` завершился `Killed`; `wifi_on=0` сохранил Wi-Fi CONNECTED; airplane broadcast отклонён ACL. Четвёртую попытку не делать.
- **EX010 PASS:** controlled enrollment recreation с валидной fixture identity/invite, ожиданием bootstrap и safe failure. Два bootstrap после recreation допустимы; нет double redeem, частичной session или secret persistence.
- **EX024 PASS:** уникальный AndroidKeyStore P-256 alias: `privateKey.encoded==null`, подпись/verify, destroy; штатные aliases сохранены.
- **PUSH02 PASS:** одна actual Firebase SDK rotation на QA_Stable35, новая регистрация enabled и `pending=false`; другие registrations неизменны. Обновление bearer/refresh/expiry является штатным refresh, не продуктовым FAIL.
- **E2E06 PASS:** изолированный OWNER официально отозвал MEMBER device (204); server отключил target session/SSH/push, а final16 sync и reopen показали durable re-enrollment recovery без stale cached task и silent wipe. Это намеренно отозванная fixture, не дефект.
- **VOI01/08 NOT_RUN:** требуется настоящая русская речь/акустика; не подменять UI или text tests.

## Лимиты и последнее состояние

- Release35 network failure: три попытки (netd отсутствует/нет IPv4 route, Wi-Fi reconnect, reboot). Четвёртую не выполнять.
- API26 offline control: три попытки выше. Не ремонтировать или обходить повторно.
- Последнее подтверждённое состояние: `QA_API26_ISO20260911` (`emulator-5570`) и `QA_Stable35` (`emulator-5554`) штатно остановлены; дисковые данные сохранены. Это не свежая текущая проверка.
- `QA_Auth35` (`emulator-5562`) не затрагивался последним cleanup.
- Телефон `b2257b46`, owner0 и QA10: при возобновлении сначала только ADB read-only verification; не переключать без предупреждения, PIN не запрашивать, пользовательский профиль восстанавливать.

## Артефакты и порядок возобновления

- Scoped checkpoint: `C:/Users/style/Documents/ChatGPT/Агенты/.e2e/runs/MVP0-QA-20260910-TOOLS-1ebebe44/mobile-20260910/QA_ANDROID_TARGETED_CHECKPOINT_20260911_v2.zip`, 25 файлов, SHA-256 `92a8bf56afbe156ee7be2f61728e3139b43fe45de1e39b54a5f9ca79d6383b23`.
- Ключевые proofs: `API26-fixture-provenance.md`, `API26-ENV02-normal-samecert-proof.md`, `API26-E2E06-live-owner-member-revoke-proof.md`, `EX024-actual-keystore-proof.md`, `EX010-final-controlled-recreation-proof.md`, `PUSH02-local-recovery-proof.md` в том же `mobile-20260910`.
- Секреты, QA PIN и содержимое ключей в evidence/этом файле не приводить.
- Новый чат начинает с узкой оценки трёх оставшихся сценариев; без broad regression, повторов уже принятых проверок или нового build.
