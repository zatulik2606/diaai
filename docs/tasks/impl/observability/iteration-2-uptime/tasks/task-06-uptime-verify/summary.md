# Task 06 summary — Kuma monitors + acceptance §9

## Сделано

### Мониторы (prod)

| Monitor | Type | Target |
|---------|------|--------|
| `diaai-backend` | HTTP | `172.18.0.1:8000/health`, keyword `"status":"ok"` |
| `diaai-frontend` | HTTP | `http://web:3000/` |
| `diaai-postgres` | PostgreSQL | `postgres:5432/diaai`, `SELECT 1` |

Автоматизация: `make kuma-bootstrap` · [`kuma-bootstrap.py`](../../../../../../../../devops/monitoring/kuma-bootstrap.py)

### Уведомления Telegram ✅

Native Telegram/SMTP из Kuma-контейнera на VPS **не работают** (socket hang up / SMTP timeout).

**Решение:** webhook → `glitchtip-telegram-bridge` (`diaai-telegram-bridge`):

```bash
make kuma-notifications   # на VPS
```

Smoke: `[Uptime Kuma] diaai-frontend: test DOWN via bridge` — пользователь подтвердил ✅

### Документация

- [`uptime-kuma.md`](../../../../../../../../devops/monitoring/uptime-kuma.md)
- [`kuma-notifications.py`](../../../../../../../../devops/monitoring/kuma-notifications.py)
- deploy §9 п.4–5 ✅

## Acceptance §9

| # | Статус |
|---|--------|
| 4 Kuma backend monitor Up | ✅ |
| 5 Kuma frontend (+ postgres) Up | ✅ |
| Telegram Down alert | ✅ через bridge |

Email из Kuma — out of scope (GlitchTip email для ошибок).

## Следующая задача

Task 07 — Dozzle SSH tunnel, §9 п.6.
