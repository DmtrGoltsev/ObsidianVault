---
id: "n8nagents-evidence-local-compose-render-20260829"
тип: "доказательство"
статус: "historical-local-evidence"
проект: "N8NAgents"
владелец: "style"
создано: "2026-08-29"
обновлено: "2026-08-29"
уверенность: "высокая"
источники:
  - "local/evidence/compose-render.txt"
  - "[[Лаборатория_Local_Docker_N8NAgents]]"
доказательства:
  - "raw SHA-256: 9d27c8c5b09f21fab60da5d2c588982c37d20cb6757acb208d2ea6390a5c663a"
теги: ["evidence", "compose", "local", "redacted", "n8n"]
source_path: "local/evidence/compose-render.txt"
source_repository_head_at_import: "dd9e10a9b9b51e33761971e517a61a6bd9fa899c"
source_repository_status: "LOCAL_ONLY / NO_ORIGIN / NOT_DEPLOYED"
source_tracking_status: "ignored local evidence; bytes are not part of the commit tree"
source_file_sha256: "9d27c8c5b09f21fab60da5d2c588982c37d20cb6757acb208d2ea6390a5c663a"
source_hash_semantics: "SHA-256 of exact 14922 raw source bytes; UTF-8 without BOM; 491 CRLF-terminated logical lines"
redaction_manifest_version: "n8nagents-evidence-redaction-v1"
redaction_status: "PASS"
redacted_payload_sha256: "8bf5819ac63c8d76a2e2acc3a025025d024891ca30400b56efd671748f2f2f4c"
redacted_payload_hash_semantics: "SHA-256 of UTF-8 bytes of LF-normalized fenced payload between markers, including one final LF and excluding markers/fence lines"
---

# Доказательство — local Compose render N8NAgents, 2026-08-29

Безопасное Markdown-представление локального docker compose config render. Оно сохраняет весь несекретный текст и порядок строк, но не доказывает current production digests/runtime.

Исходный ignored-файл оставлен без изменений вне Vault. Raw-копия не хранится в Vault из-за локальных путей, secret-bearing rendered fields и тестовых user/chat identifiers.

## Provenance и hash semantics

- source_file_sha256 — exact raw source bytes до преобразований.
- redacted_payload_sha256 — LF-normalized безопасный payload ниже.
- source repository HEAD фиксирует лишь контекст: ignored-файл не входит в commit tree.
- Преобразование одностороннее; raw redacted values не восстанавливаются.

## Redaction manifest v1

Правила по порядку: non-empty YAML secret-like values → <REDACTED_SECRET_VALUE>; *_CHAT_IDS/*_USER_IDS values → <REDACTED_IDENTIFIER_VALUE>; Windows и /home,/Users,/root host paths → <REDACTED_LOCAL_PATH>; email/non-loopback IPv4 → соответствующие markers. Container paths, names, pins, loopback, ports and non-sensitive config retained.

Срабатывания: secret values 2; identifiers 4; local paths 22; emails 0; non-loopback IPv4 0.

## Redacted payload

<!-- REDACTED_PAYLOAD_BEGIN n8nagents-evidence-redaction-v1 -->
```yaml
name: n8nagents-local
networks:
  app-internal:
    driver: bridge
    internal: true
    name: n8nagents-local_app-internal
  data-internal:
    driver: bridge
    internal: true
    name: n8nagents-local_data-internal
  mock-internal:
    driver: bridge
    internal: true
    name: n8nagents-local_mock-internal
  telegram-egress:
    driver: bridge
    name: n8nagents-local_telegram-egress
secrets:
  assistant_db_password:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_assistant_db_password
  memory_db_password:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_memory_db_password
  n8n_db_password:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_n8n_db_password
  n8n_encryption_key:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_n8n_encryption_key
  postgres_admin_password:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_postgres_admin_password
  telegram_allowed_chat_ids:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_telegram_allowed_chat_ids
  telegram_allowed_user_ids:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_telegram_allowed_user_ids
  telegram_bot_token:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_telegram_bot_token
  telegram_real_arm:
    file: <REDACTED_LOCAL_PATH>
    name: n8nagents-local_telegram_real_arm
services:
  mock-test:
    cap_drop:
      - ALL
    cpus: "0.25"
    entrypoint:
      - node
      - /opt/n8nagents/tests/docker-mock-test.mjs
    environment:
      BRIDGE_ADMIN_URL: http://telegram-bridge-mock:8082/__test__/reset
      BRIDGE_HEALTH_URL: http://telegram-bridge-mock:8082/health
      TELEGRAM_MOCK_URL: http://telegram-mock:8080
      WORKFLOW_MOCK_URL: http://workflow-mock:8081
    image: docker.n8n.io/n8nio/n8n:2.36.7
    init: true
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 128m
    networks:
      mock-internal: null
    pids_limit: 80
    profiles:
      - mock-test
    read_only: true
    restart: 'no'
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777
    volumes:
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /opt/n8nagents/tests
        type: bind
  n8n:
    cap_drop:
      - ALL
    cpus: "1.25"
    depends_on:
      postgres:
        condition: service_healthy
        required: true
    entrypoint:
      - /bin/sh
      - /local-entrypoints/n8n-secrets.sh
    environment:
      DB_POSTGRESDB_DATABASE: n8n_metadata
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: "5432"
      DB_POSTGRESDB_USER: n8n_runtime
      DB_TYPE: postgresdb
      EXECUTIONS_DATA_MAX_AGE: "168"
      EXECUTIONS_DATA_PRUNE: "true"
      EXECUTIONS_DATA_PRUNE_MAX_COUNT: "10000"
      EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS: "false"
      EXECUTIONS_DATA_SAVE_ON_ERROR: none
      EXECUTIONS_DATA_SAVE_ON_SUCCESS: none
      GENERIC_TIMEZONE: ${TIMEZONE:-Etc/UTC}
      N8N_BLOCK_ENV_ACCESS_IN_NODE: "true"
      N8N_COMMUNITY_PACKAGES_ENABLED: "false"
      N8N_DIAGNOSTICS_ENABLED: "false"
      N8N_EDITOR_BASE_URL: http://127.0.0.1:5678
      N8N_HOST: 127.0.0.1
      N8N_PORT: "5678"
      N8N_PROTOCOL: http
      N8N_PROXY_HOPS: "0"
      N8N_PUBLIC_API_DISABLED: "true"
      N8N_PUBLIC_API_SWAGGERUI_DISABLED: "true"
      N8N_RESTRICT_FILE_ACCESS_TO: <REDACTED_LOCAL_PATH>
      N8N_SECURE_COOKIE: "false"
      N8N_SSRF_PROTECTION_ENABLED: "true"
      N8N_TEMPLATES_ENABLED: "false"
      N8N_VERSION_NOTIFICATIONS_ENABLED: "false"
      N8N_WEBHOOK_URL: http://127.0.0.1:5678/
      NODE_OPTIONS: --max-old-space-size=512
      NODES_EXCLUDE: '["n8n-nodes-base.executeCommand","n8n-nodes-base.readWriteFile"]'
      TZ: ${TIMEZONE:-Etc/UTC}
    healthcheck:
      interval: 15s
      retries: 20
      start_period: 60s
      test:
        - CMD
        - node
        - -e
        - require('http').get('http://127.0.0.1:5678/healthz',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))
      timeout: 5s
    image: docker.n8n.io/n8nio/n8n:2.36.7
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 768m
    networks:
      app-internal: null
      data-internal: null
    pids_limit: 300
    ports:
      - host_ip: 127.0.0.1
        mode: ingress
        protocol: tcp
        published: "5678"
        target: 5678
    read_only: true
    restart: unless-stopped
    secrets:
      - source: n8n_db_password
        target: /run/secrets/n8n_db_password
      - source: n8n_encryption_key
        target: /run/secrets/n8n_encryption_key
    security_opt:
      - no-new-privileges:true
    stop_grace_period: 30s
    tmpfs:
      - /tmp:size=128m,mode=1777
    volumes:
      - source: local_n8n_data
        target: <REDACTED_LOCAL_PATH>
        type: volume
        volume: {}
      - source: local_n8n_files
        target: <REDACTED_LOCAL_PATH>
        type: volume
        volume: {}
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /local-entrypoints
        type: bind
  postgres:
    cpus: "0.75"
    entrypoint:
      - /bin/sh
      - /local-entrypoints/postgres-secrets.sh
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
    healthcheck:
      interval: 10s
      retries: 12
      start_period: 30s
      test:
        - CMD
        - /bin/sh
        - /healthcheck/check-foundation.sh
      timeout: 5s
    image: postgres:17.11-alpine3.24
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 512m
    networks:
      data-internal: null
    pids_limit: 200
    restart: unless-stopped
    secrets:
      - source: postgres_admin_password
        target: /run/secrets/postgres_admin_password
      - source: n8n_db_password
        target: /run/secrets/n8n_db_password
      - source: assistant_db_password
        target: /run/secrets/assistant_db_password
      - source: memory_db_password
        target: /run/secrets/memory_db_password
    security_opt:
      - no-new-privileges:true
    stop_grace_period: 30s
    volumes:
      - source: local_postgres_data
        target: /var/lib/postgresql/data
        type: volume
        volume: {}
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /local-entrypoints
        type: bind
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /docker-entrypoint-initdb.d/00-bootstrap.sh
        type: bind
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /migrations
        type: bind
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /healthcheck/check-foundation.sh
        type: bind
  telegram-bridge-mock:
    cap_drop:
      - ALL
    cpus: "0.25"
    depends_on:
      telegram-mock:
        condition: service_healthy
        required: true
      workflow-mock:
        condition: service_healthy
        required: true
    entrypoint:
      - node
      - /opt/n8nagents/bridge/bridge.mjs
    environment:
      ALLOWED_CHAT_IDS: <REDACTED_IDENTIFIER_VALUE>
      ALLOWED_USER_IDS: <REDACTED_IDENTIFIER_VALUE>
      BRIDGE_HEALTH_PORT: "8082"
      BRIDGE_MODE: mock
      BRIDGE_STATE_FILE: /state/bridge-state.json
      POLL_INTERVAL_MS: "100"
      SEND_CAP: "20"
      TELEGRAM_BASE_URL: http://telegram-mock:8080
      TELEGRAM_MOCK_TOKEN: <REDACTED_SECRET_VALUE>
      WORKFLOW_URL: http://workflow-mock:8081/process
    healthcheck:
      interval: 5s
      retries: 10
      start_period: 5s
      test:
        - CMD
        - node
        - -e
        - require('http').get('http://127.0.0.1:8082/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))
      timeout: 3s
    image: docker.n8n.io/n8nio/n8n:2.36.7
    init: true
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 128m
    networks:
      mock-internal: null
    pids_limit: 80
    profiles:
      - mock
    read_only: true
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777
    volumes:
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /opt/n8nagents/bridge
        type: bind
      - source: bridge_mock_state
        target: /state
        type: volume
        volume: {}
  telegram-bridge-real:
    cap_drop:
      - ALL
    cpus: "0.25"
    depends_on:
      n8n:
        condition: service_healthy
        required: true
    entrypoint:
      - node
      - /opt/n8nagents/bridge/bridge.mjs
    environment:
      ALLOWED_CHAT_IDS_FILE: <REDACTED_IDENTIFIER_VALUE>
      ALLOWED_USER_IDS_FILE: <REDACTED_IDENTIFIER_VALUE>
      BRIDGE_HEALTH_PORT: "8082"
      BRIDGE_MODE: real
      BRIDGE_STATE_FILE: /state/bridge-state.json
      POLL_INTERVAL_MS: "1000"
      SEND_CAP: "20"
      TELEGRAM_BASE_URL: https://api.telegram.org
      TELEGRAM_REAL_ARM_FILE: /run/secrets/telegram_real_arm
      TELEGRAM_TOKEN_FILE: <REDACTED_SECRET_VALUE>
      WORKFLOW_URL: http://n8n:5678/webhook/local-telegram-bridge
    healthcheck:
      interval: 10s
      retries: 10
      start_period: 5s
      test:
        - CMD
        - node
        - -e
        - require('http').get('http://127.0.0.1:8082/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))
      timeout: 3s
    image: docker.n8n.io/n8nio/n8n:2.36.7
    init: true
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 128m
    networks:
      app-internal: null
      telegram-egress: null
    pids_limit: 80
    profiles:
      - real
    read_only: true
    restart: 'no'
    secrets:
      - source: telegram_bot_token
        target: /run/secrets/telegram_bot_token
      - source: telegram_real_arm
        target: /run/secrets/telegram_real_arm
      - source: telegram_allowed_user_ids
        target: /run/secrets/telegram_allowed_user_ids
      - source: telegram_allowed_chat_ids
        target: /run/secrets/telegram_allowed_chat_ids
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777
    volumes:
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /opt/n8nagents/bridge
        type: bind
      - source: bridge_real_state
        target: /state
        type: volume
        volume: {}
  telegram-mock:
    cap_drop:
      - ALL
    cpus: "0.25"
    entrypoint:
      - node
      - /opt/n8nagents/mock/telegram-mock.mjs
    healthcheck:
      interval: 5s
      retries: 10
      start_period: 5s
      test:
        - CMD
        - node
        - -e
        - require('http').get('http://127.0.0.1:8080/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))
      timeout: 3s
    image: docker.n8n.io/n8nio/n8n:2.36.7
    init: true
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 128m
    networks:
      mock-internal: null
    pids_limit: 80
    profiles:
      - mock
    read_only: true
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777
    volumes:
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /opt/n8nagents/mock
        type: bind
  workflow-mock:
    cap_drop:
      - ALL
    cpus: "0.25"
    entrypoint:
      - node
      - /opt/n8nagents/mock/workflow-mock.mjs
    healthcheck:
      interval: 5s
      retries: 10
      start_period: 5s
      test:
        - CMD
        - node
        - -e
        - require('http').get('http://127.0.0.1:8081/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))
      timeout: 3s
    image: docker.n8n.io/n8nio/n8n:2.36.7
    init: true
    logging:
      driver: json-file
      options:
        max-file: "3"
        max-size: 10m
    mem_limit: 128m
    networks:
      mock-internal: null
    pids_limit: 80
    profiles:
      - mock
    read_only: true
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777
    volumes:
      - bind:
          create_host_path: true
        read_only: true
        source: <REDACTED_LOCAL_PATH>
        target: /opt/n8nagents/mock
        type: bind
volumes:
  bridge_mock_state:
    name: n8nagents-local_bridge_mock_state
  bridge_real_state:
    name: n8nagents-local_bridge_real_state
  local_n8n_data:
    name: n8nagents-local_local_n8n_data
  local_n8n_files:
    name: n8nagents-local_local_n8n_files
  local_postgres_data:
    name: n8nagents-local_local_postgres_data
x-json-logging:
  driver: json-file
  options:
    max-file: "3"
    max-size: 10m
LOCAL_COMPOSE_RENDER=PASS SECRET_VALUES=NOT_RENDERED
```
<!-- REDACTED_PAYLOAD_END n8nagents-evidence-redaction-v1 -->

## Ограничения

- Local/parity snapshot, не deployed production evidence.
- Production digests UNKNOWN без отдельной production verification.
- Redacted fields не являются deploy inputs.
