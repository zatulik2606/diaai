# UptimeRobot — внешний uptime для diaai

GlitchTip видит **ошибки в коде**; UptimeRobot проверяет, что **сервис отвечает с интернета**. Внутренний `make stack-health` этого не заменяет.

Связь: [README.md](README.md) · [ADR-005](../../docs/adr/adr-005-observability.md)

---

## 1. Регистрация

1. [uptimerobot.com](https://uptimerobot.com/) → Sign Up (free: 50 monitors)
2. **My Settings** → **Alert Contacts** → Add
   - **Telegram:** Follow bot instructions или webhook URL
   - **Email:** резервный канал

---

## 2. Monitors для diaai-prod

Замените IP на ваш (`201.51.4.34`).

### Backend health

| Field | Value |
|-------|-------|
| Monitor Type | HTTP(s) |
| Friendly Name | `diaai-backend-health` |
| URL | `http://201.51.4.34:8000/health` |
| Monitoring Interval | 5 minutes |
| Monitor Timeout | 30 seconds |
| Keyword monitoring | Enabled |
| Keyword | `"status":"ok"` |
| Alert Contacts | ваш Telegram / email |

### Web

| Field | Value |
|-------|-------|
| Monitor Type | HTTP(s) |
| Friendly Name | `diaai-web` |
| URL | `http://201.51.4.34:3000/` |
| Monitoring Interval | 5 minutes |
| Monitor Timeout | 30 seconds |
| Alert Contacts | ваш Telegram / email |

Ожидание: HTTP **200** или **307** (redirect на `/login`).

> **Не** мониторить PostgreSQL `:5433` снаружи — порт привязан к `127.0.0.1` на prod.

---

## 3. Telegram через UptimeRobot

**Вариант A — встроенный Telegram contact**

UptimeRobot → Alert Contacts → Telegram → следовать инструкциям бота.

**Вариант B — webhook на свой relay**

URL формата `https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<ID>&text=***` **не рекомендуется** (токен в URL).

Лучше: email-to-Telegram или отдельный `@diaaialarm_bot` через GlitchTip bridge только для ошибок; uptime — через встроенный Telegram contact UptimeRobot.

---

## 4. Проверка

1. Monitors → Status **Up** (зелёный)
2. **Pause monitor** → должен прийти alert → **Resume**
3. Response time виден в dashboard (грубая метрика latency)

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| Down, но `curl` с VPS OK | ufw / провайдер блокирует :8000/:3000 снаружи |
| Keyword failed | backend вернул не JSON или не `"status":"ok"` |
| Ложные срабатывания | увеличить interval; проверить timeout |

---

## Альтернатива (self-hosted)

Uptime Kuma в compose profile `monitoring` — см. ADR-005. Для MVP предпочтён UptimeRobot (0 RAM на VPS).
