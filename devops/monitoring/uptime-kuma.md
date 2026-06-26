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
ssh -L 3002:127.0.0.1:3002 deploy@201.51.4.34
# браузер → http://127.0.0.1:3002
```

---

## Первичная настройка (пользователь)

1. Открыть UI → создать admin user (один раз).
2. **Settings → Notifications → Telegram** — bot token + chat_id (добавляете сами; **не в git**).
3. Добавить мониторы (см. ниже).

---

## Monitors (task 06)

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

## Smoke

1. Kuma dashboard — оба monitor **Up** (green).
2. **Pause** monitor → Telegram alert → **Resume**.
3. (опционально) `docker stop diaai-postgres-1` → backend `/health` → 503 → alert.

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| Backend Down, curl с VPS OK | URL в Kuma: prod → `172.18.0.1:8000`, не `backend:8000` |
| Keyword failed | ответ без `"status":"ok"` — проверить `curl /health` |
| UI недоступен снаружи | ожидаемо — только SSH tunnel на prod |
| Ложные Down | увеличить interval / retries в Kuma |

---

## Альтернатива (не используется)

[uptimerobot.md](uptimerobot.md) — SaaS; в iter 2 заменён на Kuma по решению проекта.
