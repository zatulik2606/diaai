# Task 09 — Grafana dashboards (FastAPI RED + VPS)

## Цель

Два provisioned dashboard в Grafana: **backend RED** и **VPS/host** (cAdvisor).

## Файлы

| Файл | Действие |
|------|----------|
| `grafana/dashboards/diaai-backend-red.json` | RPS, 5xx, p50/p95 по handler |
| `grafana/dashboards/diaai-vps-host.json` | CPU, RAM, disk, containers |
| `grafana/provisioning/dashboards/default.yml` | file provider |
| `grafana/provisioning/datasources/prometheus.yml` | uid `prometheus` |
| `compose.yml` | mount dashboards, cadvisor `--docker_only` |
| `README.md` | Grafana tunnel + default dashboards |

## PromQL (instrumentator v8)

- RPS: `sum(rate(http_requests_total{job="diaai-backend"}[5m]))`
- 5xx: `status="5xx"`
- Latency: `http_request_duration_seconds_bucket`

## Definition of Done

- Dashboards в Grafana folder `diaai` после `monitoring-up`
- Prod: live data на panels
