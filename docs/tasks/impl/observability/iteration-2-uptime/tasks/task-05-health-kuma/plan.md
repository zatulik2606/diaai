# Task 05 — `/health` с проверкой БД + Uptime Kuma в compose

## Цель

1. **`GET /health`** — readiness: `SELECT 1` в PostgreSQL → **200** или **503**.
2. **Uptime Kuma** — сервис в profile `monitoring`, порт **3002** (без конфликта с app stack).

Мониторы и Telegram в UI Kuma — **task 06** (пользователь).

## Подготовка (пользователь)

- [ ] После деплоя task 05: `make monitoring-up` на VPS
- [ ] SSH tunnel для UI: `ssh -L 3002:127.0.0.1:3002 deploy@201.51.4.34` → `http://127.0.0.1:3002`
- [ ] Первичная настройка Kuma (admin user) — один раз

## Архитектура `/health`

```
GET /health
  → probe_database(): AsyncSession execute text("SELECT 1")
  → OK:  200 {"status":"ok","version":…,"database":"ok"}
  → FAIL: 503 {"status":"unavailable","database":"down"}
```

Если `AsyncSessionLocal is None` (нет `DATABASE_URL`) → 503.

## Файлы (агент)

| Файл | Действие |
|------|----------|
| [`backend/health.py`](../../../../../../../../backend/health.py) | **новый** — `probe_database()`, router `GET /health` |
| [`backend/main.py`](../../../../../../../../backend/main.py) | убрать inline `/health`; `include_router(health_router)` |
| [`backend/tests/test_health.py`](../../../../../../../../backend/tests/test_health.py) | 200 + DB ok; 503 при недоступной БД |
| [`backend/README.md`](../../../../../../../../backend/README.md) | контракт `/health` |
| [`devops/monitoring/compose.yml`](../../../../../../../../devops/monitoring/compose.yml) | сервис `uptime-kuma`, volume `uptime_kuma_data` |
| [`devops/monitoring/Makefile`](../../../../../../../../devops/monitoring/Makefile) | `monitoring-up` включает `uptime-kuma` |
| [`.env.example`](../../../../../../../../.env.example) | `UPTIME_KUMA_BIND=127.0.0.1:3002:3001` |
| [`devops/monitoring/uptime-kuma.md`](../../../../../../../../devops/monitoring/uptime-kuma.md) | **новый** — compose + порты + URL мониторов (настройка UI → task 06) |
| [`devops/monitoring/README.md`](../../../../../../../../devops/monitoring/README.md) | ссылка на Kuma, строка в таблице инструментов |

**Не менять:** [`docker-compose.yml`](../../../../../../../../docker-compose.yml) healthcheck backend — уже `curl -f /health`; начнёт реагировать на 503 при DB down.

## Compose: `uptime-kuma`

```yaml
uptime-kuma:
  profiles: [monitoring]
  image: louislam/uptime-kuma:1
  volumes:
    - uptime_kuma_data:/app/data
  ports:
    - "${UPTIME_KUMA_BIND:-127.0.0.1:3002:3001}"
  restart: unless-stopped
```

- Образ pin `:1` (major), обновление — осознанно.
- **Не** публиковать UI на `0.0.0.0` на prod (как Dozzle).
- RAM ~150 MB — учитывать на 4 GB VPS (рядом с Dozzle + bridge).

## Тесты

| Кейс | Ожидание |
|------|----------|
| DB up (`@pytest.mark.integration`) | 200, `"status":"ok"`, `"database":"ok"` |
| DB down / wrong URL | 503, `"database":"down"` |
| Auth | не требуется (`test_auth.py` без изменений) |

Использовать существующий `client` + `db_engine` из [`conftest.py`](../../../../../../../../backend/tests/conftest.py).

## Smoke (агент, локально)

```bash
make stack-up
make monitoring-up
curl -sf http://127.0.0.1:8000/health | jq .
curl -sf -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3002/
docker compose -f docker-compose.yml -f devops/monitoring/compose.yml --profile monitoring ps uptime-kuma
```

## Definition of Done

- [ ] `/health` с SELECT 1; 503 при fail
- [ ] pytest `test_health.py` green
- [ ] `uptime-kuma` в compose; порт 3002; volume для persistence
- [ ] `make lint` / `make format`
- [ ] `uptime-kuma.md` + monitoring README
- [ ] `summary.md`

## Skill

`docker-expert` · `sharp-edges` (не коммитить Kuma admin password / Telegram token)
