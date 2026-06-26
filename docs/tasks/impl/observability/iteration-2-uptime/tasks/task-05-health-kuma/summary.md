# Task 05 summary — `/health` + Uptime Kuma

## Сделано

### Backend `/health`

- [`backend/health.py`](../../../../../../../../backend/health.py) — `probe_database()` (`SELECT 1`), router `GET /health`
- 200: `{"status":"ok","version":"…","database":"ok"}`
- 503: `{"status":"unavailable","database":"down"}`
- [`backend/main.py`](../../../../../../../../backend/main.py) — inline handler заменён на router

### Тесты

- [`backend/tests/test_health.py`](../../../../../../../../backend/tests/test_health.py) — 200 + 503 без БД
- [`backend/tests/conftest.py`](../../../../../../../../backend/tests/conftest.py) — wire `AsyncSessionLocal` для integration; teardown globals

### Monitoring stack

- [`devops/monitoring/compose.yml`](../../../../../../../../devops/monitoring/compose.yml) — `uptime-kuma`, volume `uptime_kuma_data`, bind `127.0.0.1:3002:3001`
- [`devops/monitoring/Makefile`](../../../../../../../../devops/monitoring/Makefile) — `monitoring-up` включает kuma
- [`.env.example`](../../../../../../../../.env.example) — `UPTIME_KUMA_BIND`

### Docs

- [`devops/monitoring/uptime-kuma.md`](../../../../../../../../devops/monitoring/uptime-kuma.md) — compose, порты, URL мониторов (UI → task 06)
- [`devops/monitoring/README.md`](../../../../../../../../devops/monitoring/README.md) — таблица инструментов, quick start
- [`backend/README.md`](../../../../../../../../backend/README.md) — контракт `/health`

## Verify

```bash
make lint && uv run pytest backend/tests/test_health.py -q
# prod/local после monitoring-up:
curl -sf http://127.0.0.1:8000/health
curl -sf -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3002/
```

## Отклонения

- `health.py` импортирует `backend.database` модулем (не `from … import AsyncSessionLocal`) — иначе тесты и runtime расходятся при rebind globals.

## Следующая задача

Task 06 — мониторы + Telegram в Kuma UI; acceptance §9 п.4–5.
