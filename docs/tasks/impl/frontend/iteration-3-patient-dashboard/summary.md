# Итерация frontend 3: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-03: Панель пациента с диабетом ✅

- Patient-scoped API: 5 endpoint'ов `/patient/dashboard/*`
- `/dashboard` — KPI, activity chart, questions, submissions, progress matrix
- Без mock; RSC + loading/error states
- Детали: [task-03 summary](tasks/task-03-patient-dashboard/summary.md)

| Компонент | Путь |
|-----------|------|
| Patient service | `backend/services/web_patient_service.py` |
| Patient router | `backend/api/v1/web/patient_dashboard.py` |
| Tests | `backend/tests/test_web_patient_api.py` |
| Web lib | `web/lib/types/patient-dashboard.ts`, `backend-client.ts` |
| UI | `web/components/dashboard/*` |
| Page | `web/app/(app)/dashboard/` |

## Ценность

Первый data-driven экран для пациента с диабетом — live данные из PostgreSQL через patient API.

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| Patient API tests | ✅ 7 passed |
| `make web-build` | ✅ |
| Dashboard без mock | ✅ |
| loading / error states | ✅ |

## User-check

```bash
make db-reset && make backend-run
make web-dev
# login ivan_p → /dashboard filled
```

## Следующий шаг

[iteration-4-leaderboard](../iteration-4-leaderboard/plan.md) — leaderboard для доктора.
