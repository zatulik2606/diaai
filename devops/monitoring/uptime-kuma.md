# Uptime Kuma — мониторинг доступности diaai

Self-hosted uptime в compose profile `monitoring`. GlitchTip ловит **ошибки в коде**; Kuma — **недоступность** backend/web (в т.ч. 503 при мёртвой БД).

Связь: [README.md](README.md) · [iteration-2 plan](../../docs/tasks/impl/observability/iteration-2-uptime/plan.md)

---

## Compose

Сервис `uptime-kuma` в [`compose.yml`](compose.yml):

| Variable | Default | Назначение |
|----------|---------|------------|
| `UPTIME_KUMA_BIND` | `127.0.0.1:3002:3001` | UI; **3002** на host → **3001** в контейнере (не конфликтует с web `:3000`, Grafana `:3001` iter 3) |

```bash
make monitoring-up
curl -sf -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3002/
```

Volume `uptime_kuma_data` — настройки и история мониторов.

**Prod:** не открывать `:3002` в ufw; доступ через SSH tunnel (как Dozzle):

```bash
ssh -i ~/.ssh/diaai-deploy -L 13002:127.0.0.1:3002 deploy@201.51.4.34
# браузер → http://127.0.0.1:13002
```

> **Конфликт портов:** если локально `make monitoring-up`, Kuma тоже на `127.0.0.1:3002` — браузер откроет **пустой local**, не prod. Либо tunnel на **13002** (как выше), либо `make monitoring-down` на Mac.

---

## 1. Первичная настройка UI (один раз)

1. Tunnel с Mac → **http://127.0.0.1:13002** (см. § Compose)
2. Создать **admin** user + password (только в Kuma, не в git)
3. Dashboard → **Add New Monitor** (см. §2)

---

## 2. Telegram notifications (через bridge)

Native Telegram из Kuma-контейнera на prod **ненадёжен**. Используем webhook → `glitchtip-telegram-bridge` (тот же `@diaaialarm_bot`).

**Автоматизация на VPS:**

```bash
cd /opt/diaai && make -C devops/monitoring kuma-notifications
```

Создаёт `diaai-telegram-bridge` → `http://glitchtip-telegram-bridge:8080/webhook`, привязывает ко всем monitor'ам, шлёт test.

Credentials: `TELEGRAM_ALARM_*` в `/opt/diaai/.env` (настраивает bridge, не Kuma UI).

---

## 2b. Email (SMTP)

Источник: `SMTP_*`, `GLITCHTIP_ALERT_EMAIL_TO` / `FROM` в `.env`.

**Ограничение prod VPS:** Kuma в Docker-bridge **не достигает** `smtp.mail.ru:465` (`Network is unreachable` — та же проблема, из‑за которой backend в `network_mode: host`). **Email из Kuma на этом VPS, скорее всего, не заработает.**

Рекомендация: uptime-алерты — **Telegram**; email-алерты об ошибках — GlitchTip → `:8000/webhooks/glitchtip/email`.

Если всё же нужен email из Kuma — отдельный relay на host (out of scope MVP).

---

## 3. Monitor: backend health

**Add New Monitor:**

| Field | Prod VPS |
|-------|----------|
| Monitor Type | HTTP(s) |
| Friendly Name | `diaai-backend` |
| URL | `http://172.18.0.1:8000/health` |
| Heartbeat Interval | 60 s (или 300 s) |
| Retries | 3 |
| Keyword monitoring | **On** |
| Keyword | `"status":"ok"` |
| Notifications | ваш Telegram contact |

**Save** → статус **Up** (зелёный) ≤1 min.

Проверка с VPS:

```bash
curl -sf http://127.0.0.1:8000/health
# {"status":"ok","version":"…","database":"ok"}
```

---

## 4. Monitor: web

**Add New Monitor:**

| Field | Prod VPS |
|-------|----------|
| Monitor Type | HTTP(s) |
| Friendly Name | `diaai-frontend` |
| URL | `http://web:3000/` |
| Heartbeat Interval | 60–300 s |
| Accepted Status Codes | `200-299,300-399` (или явно 200, 307) |
| Notifications | ваш Telegram contact |

Альтернатива URL: `http://172.18.0.1:3000/`

---

## 5. Smoke (acceptance)

1. Dashboard — **оба** monitor **Up**
2. Monitor → **Pause** → через 1–2 интервала alert в Telegram → **Resume**
3. (опционально) `docker stop diaai-postgres-1` → backend `/health` → **503** → alert → `docker start diaai-postgres-1`

### Monitor: postgres

**Add New Monitor:**

| Field | Prod VPS (compose network) |
|-------|----------------------------|
| Monitor Type | PostgreSQL |
| Friendly Name | `diaai-postgres` |
| Hostname | `postgres` |
| Port | `5432` |
| Database | `diaai` |
| Username | `diaai` |
| Password | из `POSTGRES_PASSWORD` / compose |
| Heartbeat Interval | 60–300 s |

Из Kuma-контейнера доступен сервис `postgres:5432` (общая docker-сеть). **Не** мониторить `127.0.0.1:5433` — это bind на host.

**Автоматизация:** `make kuma-bootstrap` (после `KUMA_PASSWORD` в `.env`) — создаёт monitor'ы:

| Name | Type | Target |
|------|------|--------|
| `diaai-backend` | HTTP | `http://172.18.0.1:8000/health`, keyword `"status":"ok"` |
| `diaai-frontend` | HTTP | `http://web:3000/`, codes 200–399 |
| `diaai-postgres` | PostgreSQL | `postgres://diaai:***@postgres:5432/diaai`, query `SELECT 1` |

Первый запуск также создаёт admin (`KUMA_USERNAME` / `KUMA_PASSWORD` в `.env`).

---

## Monitors — справочник (local vs prod)

### Backend health

| Field | Local compose | Prod VPS |
|-------|---------------|----------|
| Type | HTTP(s) | HTTP(s) |
| Name | `diaai-backend-health` | `diaai-backend-health` |
| URL | `http://backend:8000/health` | `http://172.18.0.1:8000/health` |
| Keyword | `"status":"ok"` | `"status":"ok"` |
| Interval | 60–300 s | 60–300 s |

> Prod: backend в `network_mode: host` — из контейнера Kuma только **`172.18.0.1:8000`**, не `backend:8000`.

Ожидание: **200** и JSON с `"database":"ok"`. При недоступной БД backend вернёт **503** → monitor Down.

### Web

| Field | Local compose | Prod VPS |
|-------|---------------|----------|
| Name | `diaai-web` | `diaai-web` |
| URL | `http://web:3000/` | `http://web:3000/` или `http://172.18.0.1:3000/` |
| Accepted status | 200 / 307 | 200 / 307 |

---

## 6. Troubleshooting

| Симптом | Решение |
|---------|---------|
| Backend Down, curl с VPS OK | URL в Kuma: prod → `172.18.0.1:8000`, не `backend:8000` |
| Keyword failed | ответ без `"status":"ok"` — проверить `curl /health` |
| UI недоступен снаружи | ожидаемо — только SSH tunnel на prod |
| Ложные Down | увеличить interval / retries в Kuma |

---

## Альтернатива (не используется)

[uptimerobot.md](uptimerobot.md) — SaaS; в iter 2 заменён на Kuma по решению проекта.
