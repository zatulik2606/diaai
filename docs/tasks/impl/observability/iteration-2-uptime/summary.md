# Iteration 2 summary — мониторинг доступности

## Результат

**Uptime Kuma** на prod (`127.0.0.1:3002`); 3 monitor'а; Telegram через **glitchtip-telegram-bridge**. Acceptance §9 п.4–5 ✅.

| Компонент | Prod |
|-----------|------|
| `/health` + SELECT 1 | ✅ |
| Uptime Kuma | ✅ `uptime_kuma_data` |
| Monitors backend / frontend / postgres | ✅ Up |
| Telegram alerts | ✅ webhook → bridge |

## Задачи

| Task | Summary |
|------|---------|
| 05 | [summary](tasks/task-05-health-kuma/summary.md) |
| 06 | [summary](tasks/task-06-uptime-verify/summary.md) |

## Ключевые решения

- Kuma вместо UptimeRobot; порт **3002** (Grafana **3001** — iter 3).
- Backend `network_mode: host` → monitor `172.18.0.1:8000`.
- Tunnel prod UI: **13002** (конфликт с local Kuma на `:3002`).
- Алерты: **не** native Telegram Kuma → **bridge webhook** (`make kuma-notifications`).

## Runbook

[devops/monitoring/uptime-kuma.md](../../../../devops/monitoring/uptime-kuma.md)
