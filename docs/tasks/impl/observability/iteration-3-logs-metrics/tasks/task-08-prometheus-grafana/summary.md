# Task 08 summary — Prometheus + Grafana

## Сделано

### Код и compose

- `backend/metrics.py` — `prometheus-fastapi-instrumentator`, `GET /metrics`
- `devops/monitoring/prometheus.yml` — scrape prometheus, cadvisor, backend (`host.docker.internal:8000`)
- `devops/monitoring/compose.yml` — prometheus, grafana, cadvisor
- Grafana provisioning: datasource Prometheus
- `make monitoring-up` поднимает весь monitoring stack
- `.env.example` — `GRAFANA_*`, `PROMETHEUS_BIND`, `CADVISOR_BIND`

### Prod (2026-06-26)

| Проверка | Результат |
|----------|-----------|
| Prometheus healthy | ✅ |
| Grafana login | ✅ `:3001` |
| Targets cadvisor, prometheus, diaai-backend | ✅ UP |
| `/metrics` | ✅ prometheus text |
| `/health` + `database: ok` | ✅ после rebuild backend |
| RAM (prometheus+grafana+cadvisor) | ~150 MiB |

`GRAFANA_ADMIN_PASSWORD` добавлен в `/opt/diaai/.env` на VPS (см. файл на сервере).

### Отклонения

- Volume paths в compose: `./devops/monitoring/...` от корня проекта (не от каталога compose-файла)
- Backend на prod пересобран локально (`diaai-backend:amd64`) — CI/GHCR `:main` обновится при push

## Smoke (пользователь)

```bash
ssh -i ~/.ssh/diaai-deploy -L 13001:127.0.0.1:3001 -L 19090:127.0.0.1:9090 deploy@201.51.4.34
# Grafana → http://127.0.0.1:13001  (admin / GRAFANA_ADMIN_PASSWORD из prod .env)
# Prometheus targets → http://127.0.0.1:19090/targets
# Explore → query: rate(http_requests_total[5m])
```

## Следующая задача

Task 09 — JSON dashboards (RED + VPS host).
