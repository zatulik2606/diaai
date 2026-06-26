# Итерация 3 — логи и метрики

Опирается на [tasklist-observability.md](../../../tasklist-observability.md) · [ADR-005](../../../../adr/adr-005-observability.md)

## Цель и ценность

При инциденте — **логи всех контейнеров** в одном UI (Dozzle) и **метрики** RED/latency (Prometheus + Grafana).

## Baseline

| Компонент | Статус |
|-----------|--------|
| Dozzle в `monitoring` compose | ✅ task 02, prod `:8888` localhost |
| Prometheus + Grafana | 📋 task 08 |
| FastAPI `/metrics` | 📋 task 08 |
| Dashboards | 📋 task 09 |

## Задачи

| # | Задача | Результат |
|---|--------|-----------|
| 07 | Dozzle prod + SSH tunnel | acceptance §9 п.6 ✅ |
| 08 | Prometheus + Grafana | compose + scrape |
| 09 | Grafana dashboards | FastAPI RED + VPS |
| 10 | (iter 3.1) ключевые метрики | docs |

## Документы задач

| Task | Plan | Summary |
|------|------|---------|
| 07 | [task-07/plan.md](tasks/task-07-dozzle-prod/plan.md) | [summary.md](tasks/task-07-dozzle-prod/summary.md) |
| 08 | [task-08/plan.md](tasks/task-08-prometheus-grafana/plan.md) | [summary.md](tasks/task-08-prometheus-grafana/summary.md) |
| 09 | [task-09/plan.md](tasks/task-09-grafana-dashboards/plan.md) | [summary.md](tasks/task-09-grafana-dashboards/summary.md) |
