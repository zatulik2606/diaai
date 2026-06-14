# Task 01: Frontend API + seed v3

Итерация: [iteration-1-frontend-api](../../plan.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Реализовать 8 endpoint'ов `/api/v1/web/*`, seed v3 и contract tests по [frontend-contract.md](../../../../../../api/frontend-contract.md).

## Порядок выполнения

1. Plan-артефакты iter 1 + task 01
2. Gap analysis → зафиксировать ниже
3. Миграция `003` + User model/repo
4. `backend/schemas/web.py`
5. Repos: aggregation queries + `web_submission`
6. Services (auth → doctor → leaderboard → chat)
7. API routers + register in v1 router + service DI
8. Seed v3 + db_inspect
9. `test_web_api.py`
10. Docs + skills review → summary

## Gap → действие

| Gap | Действие | Статус |
|-----|----------|--------|
| Нет `telegram_username` | миграция 003 | ✅ |
| Нет web routes | routers + services | ✅ |
| Seed: 1 patient, нет dialogs | seed v3 | ✅ |
| Invalid UUID prefixes `g`/`h` в seed JSON | заменены на `e7`/`f8` (hex) | ✅ |
| Cohort doctor→patient | MVP: все `role=diabetic` | ✅ |
| Load-all pagination | SQL UNION + request-window history | ✅ |

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `alembic/versions/003_telegram_username.py` | create |
| `backend/models/user.py` | `telegram_username` |
| `backend/repositories/user.py` | `get_by_username`, `list_diabetics`, `require_doctor` |
| `backend/repositories/*.py` | aggregation queries |
| `backend/repositories/web_submission.py` | create |
| `backend/schemas/web.py` | create |
| `backend/services/web_*.py` | create |
| `backend/api/v1/web/*.py` | create |
| `backend/api/v1/web/service_deps.py` | create |
| `backend/api/v1/router.py` | include web router |
| `data/progress-import.v1.json` | schema v3 |
| `scripts/db/seed_from_progress.py` | dialogs, requests, photos |
| `scripts/db/db_inspect.py` | counts by role |
| `backend/tests/test_web_api.py` | create |

## Проверки

```bash
make db-reset && make db-inspect
make lint && make test          # 60 passed
make backend-run                # curl smoke 8 endpoints
```

Demo: `username=doctor_ivanov`, `doctor_telegram_id=162684825`.
