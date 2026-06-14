# Итерация frontend 1: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-01: Frontend API + seed v3 ✅

- Backend `/api/v1/web/*` (8 endpoint'ов) по [frontend-contract.md](../../../../api/frontend-contract.md)
- Миграция `003_telegram_username`, seed v3, contract tests
- Детали: [task-01 summary](tasks/task-01-frontend-api/summary.md)

| Компонент | Путь |
|-----------|------|
| Migration 003 | `alembic/versions/003_telegram_username.py` |
| Web schemas | `backend/schemas/web.py` |
| Web services | `backend/services/web_*.py` |
| Web routers + DI | `backend/api/v1/web/`, `service_deps.py` |
| Submissions repo | `backend/repositories/web_submission.py` |
| Tests | `backend/tests/test_web_api.py` (8 cases) |
| Seed | `data/progress-import.v1.json` v3, `scripts/db/seed_from_progress.py` |
| Docs | `frontend-contract.md`, `api-contract.md`, `backend/README.md`, `api-contracts.md`, `data/README.md` |

## API (live)

| # | Method | Path |
|---|--------|------|
| 1 | POST | `/api/v1/web/auth/resolve` |
| 2–6 | GET | `/api/v1/web/doctor/dashboard/{summary,activity,questions,submissions,progress-matrix}` |
| 7 | GET | `/api/v1/web/leaderboard` |
| 8 | GET | `/api/v1/web/assistant/history` |

Demo doctor: `username=akozhin`, `doctor_telegram_id=162684825`.

## Seed v3 (demo counts)

| Таблица | Count |
|---------|-------|
| users | 7 (doctor: 1, diabetic: 6) |
| food_events | 167 |
| dialog_requests | 24 |
| photo_analyses | 4 |
| progress_snapshots | 18 |

## Ценность

После `make db-reset` Next.js iter 2+ может работать на live API без mock.

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| `columns=metric` в progress-matrix | query принят; MVP — period-колонки |
| Cohort doctor→patient | MVP: все `role=diabetic`, без consultations |
| UUID prefixes `g`/`h` в seed | исправлены на `e7`/`f8` (invalid hex) при user-check |
| Post-review: SQL UNION submissions, service DI | fastapi-templates / modern-python review |

## Skills review

| Skill | Verdict |
|-------|---------|
| api-design-principles | ✅ impl ↔ iter 0 contract |
| fastapi-templates | ✅ layers, DI, async |
| modern-python | ✅ ruff, typing |
| postgresql-table-design | ✅ `003` partial UNIQUE on `telegram_username` |
| sharp-edges | ✅ Bearer required; ORM queries |

Dual 422 format — unchanged (post-MVP).

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| `make db-reset` + migrate `003` | ✅ |
| Seed idempotent | ✅ 2-й `db-seed` → +0 |
| `make lint` / `make format` | ✅ |
| `make test` | ✅ **60 passed** |
| curl smoke 8 endpoints + 401/403/404 | ✅ |
| Doctor akozhin в PG | ✅ |

## User-check

```bash
make db-reset && make db-inspect
make backend-run

export TOKEN="$BACKEND_SERVICE_TOKEN"
export BASE="http://127.0.0.1:8000"
export DOC=162684825

curl -s -X POST "$BASE/api/v1/web/auth/resolve" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"username":"akozhin"}'

curl -s "$BASE/api/v1/web/doctor/dashboard/summary?doctor_telegram_id=$DOC" \
  -H "Authorization: Bearer $TOKEN"

curl -s "$BASE/api/v1/web/leaderboard?doctor_telegram_id=$DOC" \
  -H "Authorization: Bearer $TOKEN"
```

## Следующий шаг

[iteration-2-scaffold](../iteration-2-scaffold/plan.md) — каркас Next.js в `web/`.
