# Task 01: Frontend API + seed v3 — Summary

> **Статус:** ✅ Done

Итерация: [iteration-1-frontend-api](../../plan.md) · [plan](plan.md)

---

## Сделано

- Миграция `003_telegram_username` + `User.telegram_username`
- 8 web endpoints `/api/v1/web/*` (auth, dashboard ×5, leaderboard, history)
- Services: `web_auth`, `web_doctor`, `web_leaderboard`, `web_chat` + `web_utils`
- Repos: cohort aggregations, `WebSubmissionRepository` (SQL UNION pagination)
- DI: `backend/api/v1/web/service_deps.py` (`get_web_*_service`)
- Seed v3: doctor `@doctor_ivanov`, 6 patients, dialogs, photo_analyses, snapshots
- Contract tests: `backend/tests/test_web_api.py` (8 cases)
- Docs: `frontend-contract.md`, `api-contract.md`, `backend/README.md`, `data/README.md`

## Отклонения от плана

| Отклонение | Комментарий |
|------------|-------------|
| `columns=metric` в progress-matrix | query param принят; MVP — period-колонки |
| Cohort doctor→patient | все `role=diabetic`, без consultations filter |
| Seed UUID `g*`/`h*` | invalid hex → заменены на `e7`/`f8` при проверке `db-reset` |

## Решения

| Решение | Обоснование |
|---------|-------------|
| Миграция 003 | lookup по `telegram_username` для auth resolve |
| SQL UNION submissions | pagination в PG, не load-all в RAM |
| History pagination | окно по requests + expand user/assistant messages |
| Service DI через `Depends` | fastapi-templates pattern |
| `require_doctor` → `User` | явная проверка role в dependency |

## Проблемы

| Проблема | Решение |
|----------|---------|
| Seed validation error (UUID `g`/`h`) | hex-only prefixes в `progress-import.v1.json` |
| `ruff format` drift | `assistant_history.py` отформатирован |

## Проверки

| Команда | Результат |
|---------|-----------|
| `make db-reset && make db-inspect` | users:7, requests:24, photos:4 |
| `make db-seed` (повтор) | +0 rows |
| `make lint` | green |
| `make test` | 60 passed |
| curl 8 web endpoints | HTTP 200 |
| curl 401/403/404 | expected codes |

## User-check

```bash
make db-reset && make db-inspect
make backend-run
curl -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN" \
  "http://127.0.0.1:8000/api/v1/web/doctor/dashboard/summary?doctor_telegram_id=162684825"
```
