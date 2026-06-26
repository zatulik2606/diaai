# Task 08 — Prometheus + Grafana (compose monitoring)

## Цель

Profile `monitoring`: Prometheus + Grafana + cAdvisor; scrape FastAPI `/metrics`; UI Grafana через SSH tunnel на prod.

## Baseline

- Dozzle, Kuma, bridge — ✅ task 07
- Backend `health.py` с DB probe — ✅ task 05 (prod образ — отдельно)
- Grafana host port **3001** (Kuma **3002**, web **3000**)

## Файлы

| Файл | Действие |
|------|----------|
| `backend/metrics.py` | `prometheus-fastapi-instrumentator`, `/metrics` |
| `backend/main.py` | `setup_metrics(app)` |
| `backend/tests/test_metrics.py` | smoke `/metrics` |
| `pyproject.toml` | dependency |
| `devops/monitoring/prometheus.yml` | scrape prometheus, cadvisor, backend |
| `devops/monitoring/grafana/provisioning/datasources/prometheus.yml` | datasource |
| `devops/monitoring/compose.yml` | prometheus, grafana, cadvisor |
| `devops/monitoring/Makefile` | `monitoring-up` + новые сервисы |
| `.env.example` | `GRAFANA_*`, `PROMETHEUS_BIND`, `GRAFANA_BIND` |
| `devops/monitoring/README.md` | tunnel `:13001`, smoke |
| `devops/deploy/README.md` §9 | п.7 Grafana/Prometheus |

## Архитектура scrape

Backend на prod — `network_mode: host` → Prometheus из Docker сети бьёт в `host.docker.internal:8000/metrics` (`extra_hosts: host-gateway`).

cAdvisor — `cadvisor:8080` (container metrics).

Retention 7d, scrape 30s — экономия RAM на 4 GB VPS.

## Definition of Done

- [ ] Prometheus targets UP (backend, cadvisor, self)
- [ ] Grafana UI через tunnel `13001 → prod:3001`
- [ ] `/metrics` отдаёт prometheus text
- [ ] `make lint` / `make format`
