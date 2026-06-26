# Task 07 summary — Dozzle на prod + SSH tunnel

## Сделано

### Prod verify (2026-06-26)

| Проверка | Результат |
|----------|-----------|
| `diaai-dozzle-1` | ✅ Up, `127.0.0.1:8888->8080` |
| `curl :8888` | ✅ 200 |
| `DOZZLE_BIND=127.0.0.1:8888` | ✅ в `/opt/diaai/.env` |

Dozzle поднят в task 02 (`make monitoring-up`); отдельный deploy не требовался.

### Документация

- [`devops/monitoring/README.md`](../../../../../../../../devops/monitoring/README.md) — tunnel **18888** (конфликт с local `:8888`)
- [`devops/deploy/README.md`](../../../../../../../../devops/deploy/README.md) §9 п.6 — tunnel команда

## Smoke (пользователь)

```bash
ssh -i ~/.ssh/diaai-deploy -L 18888:127.0.0.1:8888 deploy@201.51.4.34
# http://127.0.0.1:18888 — логи backend, web, postgres, kuma, bridge
```

## Acceptance §9 п.6

📋 после smoke пользователя → ✅ в deploy README.

## Следующая задача

Task 08 — Prometheus + Grafana в compose `monitoring`.
