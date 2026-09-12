# QA-лид 2: эмуляторный каталог

## Границы и доказательства
Независимый каталог по Android-коду, contracts и OpenClaw/n8n. Физический телефон, подпись, профили и production-данные вне scope. Каждая fixture: отдельные workspace/principal и префикс E2E_<group>_<UTC>_<random>; cleanup только по префиксу. Для каждого case обязательны: UI hierarchy + Room/WorkManager либо HTTP/audit/idempotency backend. P=positive, N=negative, B=boundary, S=stateful/race.

## Read-only готовность и параллелизм
- Доступны, но не запущены: OpenCode, OpenCodeSmall, Small_Phone. Последние два: Play Store, x86_64, 4 CPU, 1GB RAM, 6GB data.
- SDK: Emulator 36.5.11, adb 37.0.0, installed Android 37 Google APIs/Play Store x86_64. Gradle Managed Devices отсутствуют.
- Поэтому FCM/GMS и biometric не hardware-only: в принципе они возможны на Play Store AVD. Текущие boot, Play login/token и biometric success/cancel не доказаны.
- P0 локальные tests/contracts; P1 AVD owner-A; P2 AVD member-B/ACL; P3 Play Store AVD/FCM; P4 isolated n8n/OpenClaw. P0 параллелен всем. P1,P2,P3 параллельны на независимых fixtures. S1 одновременно P1+P2 только для shared concurrency. S2 один AVD/snapshot для process-death/upgrade. Общие Room schema, RepositoryPorts, SyncCoordinator, API contract и APK packaging интегрирует один writer.

## Cases

| ID тип группа | Preconditions/steps | Expected/oracle | Fixture/dependency |
|---|---|---|---|
| AUTH-01 P P1 | Valid invite, bootstrap/redeem, PIN | one identity/device/session; invite once | fresh invite; backend audit |
| AUTH-02 N P1 | malformed base64/UTF-8 invite | stable error, no credential/session | invalid artifact |
| AUTH-03 B P1 | plus, URI max, max+1 | plus not space; strict bound/no partial write | generated invite |
| AUTH-04 N P1 | consumed/expired invite | terminal error/no new device | two invites |
| AUTH-05 S P1 | same bootstrap requestId, then different body | same result; REQUEST_ID_REUSE; no duplicate audit | request-id fixture |
| AUTH-06 S P1 | lock/recreate/correct PIN | Room retained, authenticated | owner-A |
| AUTH-07 N P1 | wrong PIN then correct | no wrong unlock/no secret log; queue retained | no backend mutation |
| AUTH-08 P/N P1 | biometric success/cancel/unavailable | only success unlocks, PIN fallback | Play AVD capability |
| AUTH-09 S P1 | expired access + valid refresh + one call | one challenge/signature/rotation, original call once | backend marker |
| AUTH-10 N/S P1 | expired refresh, revoke, replay, timeout separately | different UX/retention; timeout never clears silently | backend status oracle |
| AUTH-11 N P1 | logout with pending queue | no authenticated call after logout | policy/audit |
| AUTH-12 N/S2 | malformed/warm deep link then recreation | no crash/foreign route; target once | UI Automator |
| AUTH-13 S2 | rotation/background at enrollment/PIN | no secret saved state | emulator only |
| SYNC-01 S P1 | offline CREATE, inspect Room, process death/reopen | placeholder + pending create atomic/persistent | one marker |
| SYNC-02 P P1 | restore network, exactly one sync | canonical one-to-one remap, one audit/key | before/after backend |
| SYNC-03 N/S2 | loss during CREATE, scheduler resume | same op/payload retained; no duplicate | AVD network |
| SYNC-04 B P1 | 100 then 101 allowed mutations | batch bound/order/no loss | bulk workspace |
| SYNC-05 S P1 | create then status/result/update/focus local references | all dependencies remap once | local graph |
| SYNC-06 N/S P1 | same key same/different payload | original result or IDEMPOTENCY_KEY_REUSE | key oracle |
| SYNC-07 P/N P1 | initial/repeated/foreign cursor | monotonic after apply/no foreign row or skip | cursor fixture |
| SYNC-08 S S2 | worker sync interrupted/Doze/process death | durable unique work resumes eligible once | WorkManager |
| SYNC-09 S S1 | two clients same vs different task/version | one conflict only for shared target; no leakage | owner/member |
| SYNC-10 N P1 | forbidden offline approval/ACL/delegation/document/tool | no forbidden outbox row | policy contract |
| SYNC-11 B/S2 | valid/invalid task transitions and delayed old envelope | state machine only/no regression | version fixture |
| SYNC-12 P/N P1 | focus 20, duplicate, 21, stale | order valid; reject/conflict no partial list | focus fixture |
| SYNC-13 S S2 | same-cert upgrade pending CREATE/UPDATE/CONFLICT | schema/payload semantics retained | signed APK pair |
| TASK-01 P P1 | create/list filters/detail | one task/status/version in UI+Room+backend | unique marker |
| TASK-02 B P1 | blank/300/301/Cyrillic/emoji/combining title | validation; accepted Unicode byte-preserved | marker |
| TASK-03 B P1 | Moscow midnight/offset/overdue/invalid RFC3339 | display/order exact; invalid Save blocked | fixed clock |
| TASK-04 S S2 | navigation/detail/back/rotation/missing detail | no duplicate nav/stale detail | UI hierarchy |
| TASK-05 S S1 | local title vs server description change | dirty title only, description survives | held fixture post-fix |
| TASK-06 N S2 | legacy conflict no changedFields | Save blocked until compare; no heuristic merge | regression fixture |
| TASK-07 S S2 | recorded title/description/due/visibility conflict, compare/reopen/repeat | typed draft survives overlay/reopen; untouched vN fields survive | known current blocker |
| TASK-08 N P1 | wrong-task conflict op ID | no supersede/enqueue | Room oracle |
| TASK-09 P/N P1 | status/result terminal, stale/forbidden action | only allowed transitions; stable deny/conflict | task+ACL fixture |
| TASK-10 S P1 | rapid double create/save/status; editor rotate unsaved | one durable op/no accidental write | idempotency/UI |
| CAL-01 P/B P1 | exact calendar range/empty/reversed/inaccessible | inclusion/order/local route; no leak | owner/member |
| FOCUS-01 N/S1 | concurrent focus replace | one apply/one conflict, never mixed order | shared focus |
| INBOX-01 P/S P1 | filters, offline mark-read, sync/reorder | correct event only, one outbox/audit | unique event |
| INBOX-02 P/N P2 | assignment accept/decline online/offline | one terminal online, offline no request | member assignment |
| INBOX-03 P/N P1 | approval decision/repeat/double tap | one terminal effect/audit | durable approval |
| INBOX-04 N P2 | no grant/revoked assignment | hidden/denied/no leaked text | ACL fixture |
| AGENT-01 P/S P4 | text command, queued/running/recreate | one TaskRun/history, no resubmit | agent-D |
| AGENT-02 N P4 | empty/20k/overlength/offline command | validation/no run | no model effect |
| AGENT-03 P/N P4 | agent create/update/assign intent | durable proposal/approval before effect | signed service |
| AGENT-04 S P4 | same dispatch retry, old rejection then tool | one mutation budget, old run blocked | guard oracle |
| AGENT-05 S P4 | opposite proposal decisions, waiting run retry | one terminal decision; retry new attempt | concurrency fixture |
| AGENT-06 N P4 | HMAC/timestamp/nonce/identity/direct-effect invalid | reject before effect | test identity |
| AGENT-07 P/N P4 | approval durable/non-durable n8n resource | effect once or APPROVAL_NOT_DURABLE | isolated workflow |
| DOC-01 P P1 | root/child/second root known SHA refresh | depth-first accessible tree | document fixture |
| DOC-02 S S2 | open Markdown online, offline reopen | verified cache + offline state | restore network |
| DOC-03 N P1 | bad checksum/media/Markdown | reject new, retain verified cache | fault fixture |
| DOC-04 N P2 | selected branch/sibling/ancestor/revoke | exact allowed branch only | ACL fixture |
| DOC-05 N P1 | orphan/cycle/cross-task parent | terminate/no leak/no hang | read-only malformed fixture |
| PUSH-01 P P3 | fresh token, granted permission, register | one enabled registration/no token log | Play services/backend |
| PUSH-02 S P3 | register fail then success/natural token rotation | pending clears only on success | no GMS clear |
| PUSH-03 N P3 | deny notification then TASK | refresh, no shade notification | event fixture |
| PUSH-04 P P3 | grant then TASK/INBOX/APPROVAL sequential background tap | neutral copy/exact route/no content leak | distinct IDs |
| PUSH-05 S/N P3 | duplicate ID, stale version, invalid envelope | correct dedupe/discard/no crash | push-store oracle |
| PUSH-06 N P3 | unregister + same-key replay + post-disabled event | disabled/replay-safe/no delivery | cleanup |
| OS-01 S S2 | rotation all routes/dialog/conflict | no accidental write/state coherent | AVD |
| OS-02 N/S2 | airplane DNS/connect/write/read; refused/no-route/timeout | queue/error distinction; telemetry phase/category/host only | restore baseline |
| OS-03 P/N S2 | direct HTTP allowlist vs other cleartext hosts | approved origin only/no adb reverse dependency | test endpoint |
| OS-04 P/N S2 | ECDSA P-256 enrollment/revoked/expired/rotated; wrong fingerprint/key/oversize/forwarding | non-exportable lifecycle/restricted bootstrap/no partial state | test invite |
| OS-05 S S2 | WorkManager constraint/Doze/reboot-equivalent | unique work once when eligible | later restart approval |
| OS-06 S/N S2 | upgrade/downgrade/signature mismatch | same-cert data retains; refusal/safe failure; no clear workaround | AVD snapshot |
| OS-07 B S2 | RU/EN, 24/12h, Moscow/UTC, low storage/battery/accessibility | correct copy/date/labels and safe degraded behavior | OS settings |

## Gates and blockers
1. Contract gate: contracts verifier plus Android/server/workflow tests.
2. AVD gate: visual state alone insufficient; capture UI plus Room/WorkManager/backend oracle.
3. S1 concurrency mandatory for shared version, idempotency and ACL.
4. Upgrade gate: pending CREATE/UPDATE/CONFLICT, verified cache, locked session, push registration.
5. Security gate: diagnostics never contain passwords, tokens, keys, URL query, headers, bodies, document content or IDs.
6. Defects aggregate by file/contract; one integration package and build, then rerun affected cases.

Dependencies: AVD boot/Play login/biometric simulation unproven; P3 needs one-event FCM publisher; repo n8n workflows are active:false so P4 needs isolated activation; DOC-05 needs safe fixture. Known WIP blocker: recorded-intent 409 draft can be overwritten after compare; TASK-05..08 remain unpassed until fixed/reviewed.

## Инфраструктурный preflight 2026-09-09

- Запущен только изолированный Play Store AVD OpenCodeSmall, serial emulator-5554. Физический serial не адресовался.
- Boot completed=1; модель sdk_gphone16k_x86_64; API 37; com.google.android.gms установлен.
- Connectivity validated: Wi-Fi network имеет INTERNET, VALIDATED, NOT_VPN. Read-only HTTP GET из AVD на production gateway /health/ready и /health/live вернул HTTP 200. Запросы без auth и без мутаций.
- Biometric capability: feature android.hardware.fingerprint и emulator console finger command доступны. Успешная/отменённая app-biometric проверка не доказана: для неё нужен отдельный разрешённый тест с enrolled fingerprint и открытым biometric prompt.
- UI automation blocker: после boot на launcher два uiautomator dump дали ERROR null root node returned by UiTestAutomationBridge; XML не создан. Это не connectivity/boot blocker. До новой гипотезы третий blind retry не выполнять; следующий вариант — instrumentation/UIAutomator smoke на отдельном test APK после согласования.
- UI automation alternative: existing NavigationSmokeTest was built and targeted to a new isolated QA_Emu37, serial emulator-5556. Debug app and androidTest APK installed, but UTP reported `Instrumentation run failed due to Process crashed`; tests=0. UTP then removed only those temporary packages. No product data or existing AVD data was wiped. This is the third meaningful UI-automation attempt after two root-null dumps; no further blind retry is scheduled. Next work needs retained process-crash evidence or an API-35/36 stable image hypothesis, not another identical command.
- Stable compatibility: official Android 35 Google Play image installed and QA_Stable35 booted as emulator-5558; API35, GMS and Play Store confirmed. Existing NavigationSmokeTest executed through Compose instrumentation (3 tests), proving the instrumentation path. All three fail because a fresh install is at auth/onboarding gate while the smoke assumes authenticated primary tabs. This is a missing isolated authenticated-fixture precondition, not yet a product defect. No rerun until fixture exists.
- Cross-review correction: cleanup must use exact UUID ledger plus before/after global baseline, not prefix alone. n8n readiness must be checked against concrete workflow ID/export; no global active-state inference.
