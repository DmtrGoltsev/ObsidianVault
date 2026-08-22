---
id: "release-finance-android-production-20260822"
тип: "доказательство"
статус: "завершено"
проект: "Finance"
создано: "2026-08-22"
обновлено: "2026-08-22"
уверенность: "высокая"
теги: ["finance", "release", "android", "apk", "production", "cicd"]
ссылки:
  - "[[Finance]]"
  - "[[QA_Результаты]]"
  - "[[QA_Фиксы]]"
  - "[[QA_ТестКейсы_Android_Production_20260822]]"
---

# Finance Android Production Release - 2026-08-22

## Source

- Branch: `prod/finance-personal-android-backend-20260822`.
- Secure session/sync: `af22cce6417012e2adedb2fe0689c0670e322cf1`.
- Functional Android fixes: `12a1b91f20c2ce3f48bcae6919b76eb976b12c3f`.
- Final source/month selector: `43f4b1780e3bdcf6891b877fe03ee53971f74500`.

## APK

- Path: `C:\Users\style\Documents\Codex\Финансы\artifacts\apk\finance-android-prod-20260822-035412-personal-FINAL-manual-install.apk`.
- SHA-256: `b7244a339eb71bcb91dc8a02066e93bc219707691a350488315255a57f5cb1c4`.
- Size: `8119142` bytes.
- Package/version: `com.finance.mvp`, `0.1.0`, code `1`.
- Certificate SHA-256: `b5675864b9cb8a046d889f54e58f5b0256d6937ecd448e69d7faa955e587aca0`.
- API: `http://45.10.110.42/finance-api`.
- Gates: non-debuggable, production URL only, ZIP/EOCD/CD integrity, zero
  trailing bytes and abnormal gaps, zipalign, v2/v3 signature, certificate
  continuity: PASS.

## QA

- Android unit `167/167`; lint `0` errors.
- Install and production login on `emulator-5554`: PASS.
- Targeted E2E: session persistence, selected-month investment transfer,
  newest-first operations/transfers, payment-account refresh, searchable category
  dialog and manual expense: PASS.
- Raw screenshots/XML stay local in `C:\Temp\finance-absolute-final-*` and
  `C:\Temp\finance-final-e2e-*`; not committed.

## Backend Production

- Actions: https://github.com/DmtrGoltsev/finance/actions/runs/32540824773
- Workflow source: `12a1b91f20c2ce3f48bcae6919b76eb976b12c3f`.
- Release: `/opt/finance/releases/finance-personal-backend-20260822-12a1b91f`.
- Backend PASS; frontend skipped; health/OpenAPI/login/refresh PASS.
- Migrations and backup skipped; DB unchanged; revision `20260618_0017`.
- Rollback: `/opt/finance/releases/20260726T220603Z-55f4ac53`.

## Residual Coverage And Risk

- Full UI offline create/reconnect/sync not rerun on final APK.
- OCR real-image upload not run; OCR stays online-only.
- Android 17 Espresso framework incompatibility occurs before assertions.
- Production plain HTTP remains an unresolved TLS risk.

Credentials are intentionally absent. Use
[[QA_Учетная_Запись_Production_20260822]].
