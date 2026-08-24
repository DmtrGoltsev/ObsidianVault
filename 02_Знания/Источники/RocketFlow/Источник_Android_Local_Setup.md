---
id: "src-android-local-setup-2026-06-07"
тип: "источник"
статус: "актуально"
проект: "RocketFlow"
владелец: "rocketflow-team"
создано: "2026-06-07"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["android/local.properties", "local Android SDK"]
доказательства: ["Док_Android_Verification"]
теги: ["источник", "android", "local-setup", "sdk"]
---

# Источник: Android Local Setup

## Текущая локальная конфигурация

- Android SDK: `C:\Users\style\AppData\Local\Android\Sdk`
- `android/local.properties`: `sdk.dir=C:/Users/style/AppData/Local/Android/Sdk`
- `android/local.properties` должен оставаться ignored by git
- emulator `emulator-5554` видим локально

## Граница секрета

`local.properties` хранит локальный путь SDK, не должен попадать в git и не должен использоваться как portable project source.

## Связанные заметки

- [[Док_Android_Verification]]
- [[Док_Android_Build]]
- [[MOC_Android]]
