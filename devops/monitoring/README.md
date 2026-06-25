# Monitoring (observability MVP)

Стек сопровождения prod: [ADR-005](../../docs/adr/adr-005-observability.md).

| Категория | Инструмент | Где |
|-----------|------------|-----|
| Ошибки | GlitchTip EU | SaaS |
| Алерты об ошибках | glitchtip-telegram-bridge | compose profile `monitoring` |
| Uptime | UptimeRobot | SaaS · [uptimerobot.md](uptimerobot.md) |
| Логи | Dozzle | compose profile `monitoring` |

---

## Быстрый старт (локально)

```bash
# из корня репо — app stack уже running
make monitoring-up
open http://127.0.0.1:8888   # Dozzle
curl -sf http://127.0.0.1:8080/health
```

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
| `GLITCHTIP_WEBHOOK_SECRET` | опционально — query `?secret=` или header `X-Webhook-Secret` |

### GlitchTip UI (eu.glitchtip.com)

1. Project → **Alerts** → **Alert recipients** → **Add**
2. Type: **Webhook** (General / Slack-compatible)
3. URL:
   - без secret: `http://201.51.4.34:8080/webhook`
   - с secret: `http://201.51.4.34:8080/webhook?secret=YOUR_SECRET`
4. Trigger: new issue / regression (по необходимости)

**ufw:** порт **8080** должен быть открыт для ingest GlitchTip (или reverse proxy на 443 позже).

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

## UptimeRobot

Внешние HTTP checks — см. [uptimerobot.md](uptimerobot.md).

---

## Prod checklist

- [ ] `make stack-up-registry && make stack-health`
- [ ] `make monitoring-up`
- [ ] UptimeRobot monitors green
- [ ] GlitchTip test event → Telegram
- [ ] Dozzle через SSH tunnel

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
