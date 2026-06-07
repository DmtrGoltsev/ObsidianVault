---
id: "reg-deploy-focus"
тип: "регламент"
статус: "активно"
проект: "Focus"
владелец: "DmtrGoltsev"
создано: "2026-06-07"
обновлено: "2026-06-07"
уверенность: "высокая"
источники: ["[[Focus]]"]
доказательства: ["[[QA_Результаты]]"]
теги: ["регламент", "деплой", "production"]
---

# Регламент Деплоя Focus

## Цель

Стандартизировать процедуру развёртывания Focus на production-сервер [[HexCore]].

## Целевой сервер

HexCore (`45.10.110.42`) — Ubuntu, 1.6 GB RAM, 20 GB disk.

## Компоненты

| Компонент | Размещение | Порт |
|---|---|---|
| Backend JAR | `/opt/focus/focus-backend.jar` | `127.0.0.1:8082` |
| systemd unit | `/etc/systemd/system/focus.service` | — |
| Конфиг .env | `/opt/focus/.env` (600, focus:focus) | — |
| Логи | `/var/log/focus/application.log` | — |
| Frontend статика | `/var/www/focus/` | nginx location `/focus/` |
| Nginx proxy API | location `/focus-api/` | → `127.0.0.1:8082/` |
| БД | `focus_db`, пользователь `focus_user` | PostgreSQL 18 |

## Процедура деплоя backend

### 1. Сборка (локально или CI)

```bash
cd backend && mvn clean package -DskipTests
# → target/focus-backend-0.0.1-SNAPSHOT.jar
```

### 2. Копирование на сервер

```bash
scp target/focus-backend-0.0.1-SNAPSHOT.jar root@45.10.110.42:/opt/focus/focus-backend.jar.new
ssh root@45.10.110.42
cd /opt/focus
systemctl stop focus
cp focus-backend.jar focus-backend.jar.bak
mv focus-backend.jar.new focus-backend.jar
systemctl start focus
```

### 3. Проверка

```bash
systemctl status focus
journalctl -u focus -f  # логи
curl -X POST http://localhost:8082/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"deploy_test@focus.local","password":"Test1234!"}'
```

## Процедура деплоя frontend

### 1. Сборка

```bash
cd frontend && npx vite build --base=/focus/
# VITE_API_BASE_URL=/focus-api задаётся через .env или CI
```

### 2. Копирование на сервер

```bash
scp -r dist/* root@45.10.110.42:/var/www/focus/
ssh root@45.10.110.42 "chown -R www-data:www-data /var/www/focus/"
```

### 3. Проверка

```bash
curl -s -o /dev/null -w "%{http_code}" http://45.10.110.42/focus/
```

## Откат

### Backend

```bash
systemctl stop focus
cp focus-backend.jar.bak focus-backend.jar
systemctl start focus
```

### Frontend

```bash
rm -rf /var/www/focus/*
cp -a /var/www/focus-backup/* /var/www/focus/
nginx -t && systemctl reload nginx
```

## Управление сервисом

```bash
systemctl status focus          # Статус
systemctl restart focus         # Перезапуск
systemctl stop focus            # Остановка
journalctl -u focus -f          # Логи real-time
journalctl -u focus --since today  # Логи за сегодня
```

## Бэкап БД

```bash
sudo -u postgres pg_dump focus_db | gzip > /opt/focus/backups/focus_$(date +%Y%m%d_%H%M%S).sql.gz
```

Восстановление:
```bash
gunzip -c backup.sql.gz | sudo -u postgres psql focus_db
```

## Связанные заметки

- [[Focus]] — карточка проекта
- [[HexCore]] — production-сервер
- [[MOC_Focus]] — навигация по проекту
