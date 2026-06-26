# Task 07 — Dozzle на prod + SSH tunnel

## Цель

Dozzle на prod (`127.0.0.1:8888`); доступ с Mac через SSH tunnel; acceptance [deploy/README.md §9](../../../../../devops/deploy/README.md#9-observability-mvp) пункт **6** ✅.

## Baseline

Dozzle уже в `make monitoring-up` (task 02). `DOZZLE_BIND=127.0.0.1:8888` на prod.

## Файлы (агент)

| Файл | Действие |
|------|----------|
| [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) | § Dozzle: tunnel `:18888`, конфликт с local |
| [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 п.6 | ✅ |
| task-07 `summary.md` | smoke prod |

## Smoke (пользователь)

```bash
ssh -i ~/.ssh/diaai-deploy -L 18888:127.0.0.1:8888 deploy@201.51.4.34
# http://127.0.0.1:18888 — логи backend, web, postgres, kuma, bridge
```

> Локально `make monitoring-up` тоже занимает `:8888` — tunnel на **18888** (как Kuma `:13002`).

## Definition of Done

- [ ] Dozzle Up на VPS, bind localhost
- [ ] ufw: **8888 не открыт**
- [ ] Tunnel → UI, логи `diaai-backend-1` видны
- [ ] deploy §9 п.6 ✅
