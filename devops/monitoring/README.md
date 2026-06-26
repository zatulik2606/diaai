# Monitoring (observability MVP)

Стек сопровождения prod: [ADR-005](../../docs/adr/adr-005-observability.md).

| Категория | Инструмент | Где |
|-----------|------------|-----|
| Ошибки | GlitchTip EU | SaaS |
| Алерты об ошибках | glitchtip-telegram-bridge / email-bridge | compose profile `monitoring` |
| Uptime | Uptime Kuma | compose `monitoring` · [uptime-kuma.md](uptime-kuma.md) |
| Логи | Dozzle | compose profile `monitoring` |

---

## Быстрый старт (локально)

```bash
# из корня репо — app stack уже running
make monitoring-up
open http://127.0.0.1:8888   # Dozzle
open http://127.0.0.1:3002   # Uptime Kuma
curl -sf http://127.0.0.1:8080/health
curl -sf http://127.0.0.1:8081/health
curl -sf http://127.0.0.1:8000/health
```

---

## GlitchTip smoke (task 01 — ingest)

Защищённые debug-маршруты шлют тестовое событие в GlitchTip EU. DSN — в `.env`; token **не коммитить**.

| Маршрут | Проект GlitchTip |
|---------|------------------|
| `GET /debug/glitchtip-test` (:8000) | `diaai-backend` |
| `GET /api/debug/glitchtip-test` (:3000) | `diaai-web` |

Если `GLITCHTIP_DEBUG_TOKEN` пуст → маршруты **404**.

```bash
# Backend
curl -sf -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" \
  http://127.0.0.1:8000/debug/glitchtip-test

# Web (server-only route)
curl -sf -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" \
  -H "Accept: application/json" \
  http://127.0.0.1:3000/api/debug/glitchtip-test
```

Ожидание: HTTP 200, JSON `{ "ok": true, "project": "diaai-backend|diaai-web" }`; issue в [eu.glitchtip.com](https://eu.glitchtip.com) ≤1 min.

**Backend `/health`:** `SELECT 1` → 200 `{"status":"ok","database":"ok",…}` или 503 при недоступной БД. Keyword для Kuma: `"status":"ok"`.

Подробнее: [../glitchtip/hosted.md](../glitchtip/hosted.md) · tasklist observability task 01.

---

## Prod sequence (task 02 — monitoring stack)

После app stack на VPS:

```bash
ssh deploy@201.51.4.34
cd /opt/diaai
git pull --ff-only origin main
cp devops/deploy/compose.server.override.yml compose.override.yml
make stack-up-registry
make monitoring-up
make monitoring-ps
```

**`.env` на prod:** `TELEGRAM_ALARM_*`, `DOZZLE_BIND=127.0.0.1:8888`, `GLITCHTIP_BRIDGE_BIND=8080:8080`, опционально `GLITCHTIP_WEBHOOK_SECRET`.

**ufw (пользователь):** `sudo ufw allow 8080/tcp` — GlitchTip EU → bridge webhook. Порт **8888 не открывать**.

Smoke:

```bash
curl -sf http://127.0.0.1:8080/health
curl -X POST http://127.0.0.1:8080/webhook \
  -H 'Content-Type: application/json' \
  -d '{"attachments":[{"title":"bridge prod test","title_link":"https://eu.glitchtip.com","text":"task-02"}]}'
curl -sf -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8888/
```

Ожидание: Telegram от `@diaaialarm_bot`; Dozzle HTTP 200 на localhost.

**Два пути Telegram-алертов на prod:**

| Путь | URL | Когда |
|------|-----|-------|
| **Bridge (task 02/03)** | `http://IP:8080/webhook` | GlitchTip alert recipient → task 03 |
| Backend (legacy) | `http://IP:8000/webhooks/glitchtip` | встроено в FastAPI; email — `/webhooks/glitchtip/email` |

---

## Dozzle — логи контейнеров

- UI: `http://127.0.0.1:8888` (по умолчанию только localhost)
- Читает `/var/run/docker.sock` — видит все контейнеры проекта

**Prod (VPS):** порт не открывать в ufw. Доступ через SSH tunnel:

```bash
ssh -L 8888:127.0.0.1:8888 deploy@201.51.4.34
# браузер → http://127.0.0.1:8888
```

Переменная `DOZZLE_BIND=127.0.0.1:8888` в `.env` (см. `.env.example`).

---

## GlitchTip → Telegram bridge

GlitchTip шлёт Slack-compatible JSON; Telegram API — другой формат. Bridge принимает webhook и вызывает `sendMessage`.

### Env

| Variable | Описание |
|----------|----------|
| `TELEGRAM_ALARM_BOT_TOKEN` | `@diaaialarm_bot` |
| `TELEGRAM_ALARM_CHAT_ID` | после `/start` |
| `GLITCHTIP_BRIDGE_BIND` | default `8080:8080` |
| `GLITCHTIP_WEBHOOK_SECRET` | опционально — query `?secret=` или header `X-Webhook-Secret` |

### GlitchTip UI (eu.glitchtip.com) — task 03

1. Project → **Alerts** → **Alert recipients** → **Add**
2. Type: **Webhook** (General / Slack-compatible)
3. URL (prod, порт **8080** — `make monitoring-up` + ufw):
   - `http://201.51.4.34:8080/webhook`
   - с secret: `http://201.51.4.34:8080/webhook?secret=YOUR_SECRET`
4. Trigger: new issue / regression (по необходимости)

**Альтернатива:** backend `:8000/webhooks/glitchtip` — без отдельного bridge; см. [alerts-telegram.md](../glitchtip/alerts-telegram.md).

**ufw:** порт **8080** для bridge; Dozzle **8888** только localhost.

### Проверка

```bash
curl -sf http://127.0.0.1:8080/health

curl -X POST http://127.0.0.1:8080/webhook \
  -H 'Content-Type: application/json' \
  -d '{"text":"test","attachments":[{"title":"Test error","title_link":"https://eu.glitchtip.com","text":"manual test"}]}'
```

Ожидание: сообщение в Telegram.

Подробнее: [../glitchtip/alerts-telegram.md](../glitchtip/alerts-telegram.md)

---

## GlitchTip → Email bridge

Hosted GlitchTip не шлёт email без своего SMTP. Bridge / backend endpoint принимает webhook и отправляет письмо через **ваш SMTP**.

**Prod:** `http://201.51.4.34:8000/webhooks/glitchtip/email` (второй webhook recipient в alert rule).

**Локально:** `:8081/webhook` — `make monitoring-up`.

Подробнее: [../glitchtip/alerts-email.md](../glitchtip/alerts-email.md)

---

## E2E iter 1 (task 04 — ingest → alert)

Полная проверка цепочки observability iter 1 на **VPS** (после tasks 01–03). Секреты — только из `/opt/diaai/.env`, не в git.

| # | Шаг | Ожидание |
|---|-----|----------|
| 1 | Debug backend | HTTP 200, issue в GlitchTip `diaai-backend` |
| 2 | Debug web | HTTP 200, issue в GlitchTip `diaai-web` |
| 3 | GlitchTip alert rule | auto POST на bridge + email endpoint |
| 4 | (опционально) | Telegram + письмо на новый issue |

```bash
ssh deploy@201.51.4.34
cd /opt/diaai

# 1–2: ingest (Bearer из .env)
TOKEN=$(grep ^GLITCHTIP_DEBUG_TOKEN= /opt/diaai/.env | cut -d= -f2)
curl -sf -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/glitchtip-test
curl -sf -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  http://127.0.0.1:3000/api/debug/glitchtip-test

# 3: auto webhook от GlitchTip EU (≤1–2 min, rule «1 event / 1 min»)
docker logs diaai-glitchtip-telegram-bridge-1 --since 5m 2>&1 | grep -a "POST /webhook"
docker logs diaai-backend-1 --since 5m 2>&1 | grep -a "POST /webhooks/glitchtip/email"

# Bridge health (task 02)
curl -sf http://127.0.0.1:8080/health
```

**Ожидание шага 3:** в логах bridge — `165.227.159.10 - "POST /webhook HTTP/1.1" 200`; в backend — `POST /webhooks/glitchtip/email HTTP/1.1" 200`. IP — worker GlitchTip EU.

**Telegram:** сообщение от `@diaaialarm_bot` с ссылкой на issue в [eu.glitchtip.com](https://eu.glitchtip.com).

**Если webhook не пришёл:** alert rule throttling (1/min), issue уже существует (не «new»), ufw `:8080`, recipients в UI — см. [alerts-telegram.md](../glitchtip/alerts-telegram.md) §4.1.

Acceptance §9 пункты 1–3: [deploy/README.md §9](../deploy/README.md#9-observability-mvp).

---

## Uptime Kuma

Self-hosted мониторинг доступности — см. [uptime-kuma.md](uptime-kuma.md). UI: `127.0.0.1:3002` (`UPTIME_KUMA_BIND`).

---

## UptimeRobot (альтернатива, не iter 2)

SaaS — см. [uptimerobot.md](uptimerobot.md).

---

## Prod checklist

- [x] `make stack-up-registry && make stack-health` (iter 1)
- [x] `make monitoring-up` — Dozzle + bridge (task 02)
- [x] `uptime-kuma` в monitoring stack (task 05) — `:3002` localhost
- [x] debug curl backend + web → GlitchTip (task 01)
- [x] GlitchTip alert recipient → `:8080/webhook` + `:8000/.../email` (task 03)
- [x] E2E iter 1 — [§ E2E iter 1](#e2e-iter-1-task-04--ingest--alert) (task 04)
- [ ] Uptime Kuma monitors green (iter 2, task 06)
- [ ] Dozzle через SSH tunnel (iter 3)

Acceptance: [../deploy/README.md](../deploy/README.md#9-observability-mvp)

---

## Makefile

| Target | Действие |
|--------|----------|
| `make monitoring-up` | Dozzle + bridge |
| `make monitoring-down` | остановить monitoring |
| `make monitoring-ps` | статус |
| `make monitoring-logs` | логи (`SVC=...`) |

---

## Отложено (post-MVP)

Prometheus + Grafana, Loki, endpoint алертов в backend — см. ADR-005.
