# Task 09 summary — Grafana dashboards

## Сделано

- `grafana/dashboards/diaai-backend-red.json` — RPS, 5xx %, p50/p95, by handler/status
- `grafana/dashboards/diaai-vps-host.json` — host CPU/RAM/disk + top cgroup CPU/RAM
- Provisioning: `grafana/provisioning/dashboards/default.yml`, datasource uid `prometheus`
- `compose.yml` — mount dashboards; cAdvisor `--docker_only`
- `README.md` — folder **diaai**, tunnel `:13001`

## Prod verify (2026-06-26)

| Проверка | Результат |
|----------|-----------|
| Grafana provisioning | ✅ `finished to provision dashboards` |
| API search | ✅ `diaai Backend RED`, `diaai VPS Host` in folder `diaai` |
| Host panels (CPU/RAM/disk) | ✅ data from `id="/"` |

### Отклонение

cAdvisor на VPS не отдаёт docker `name` labels — container panels используют **cgroup `id`** (topk по slice), не имена контейнеров.

## Smoke (пользователь)

```bash
ssh -i ~/.ssh/diaai-deploy -L 13001:127.0.0.1:3001 deploy@201.51.4.34
# http://127.0.0.1:13001 → Dashboards → diaai
# Подождать ≥15 min трафика для RED graphs
```

## Следующая задача

Task 10 — `key-metrics.md` (iter 3.1).
