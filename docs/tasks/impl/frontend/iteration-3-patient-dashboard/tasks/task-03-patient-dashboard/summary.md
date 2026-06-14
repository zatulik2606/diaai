# Task 03: Панель пациента с диабетом — Summary

> **Статус:** ✅ Done

Итерация: [iteration-3-patient-dashboard](../../plan.md) · [plan](plan.md)

---

## Сделано

### Backend patient API

- `PatientKpiId`, patient DTO в `backend/schemas/web.py`
- `WebPatientService` — scope одного patient
- `require_diabetic` + router `/api/v1/web/patient/dashboard/*` (5 endpoints)
- `backend/tests/test_web_patient_api.py` — 7 tests

### Frontend dashboard

- `web/lib/types/patient-dashboard.ts`, fetch helpers в `backend-client.ts`
- `web/components/dashboard/*` — KPI, chart, questions, submissions, matrix
- `web/app/(app)/dashboard/` — RSC page + loading + error

### Docs

- `docs/api/frontend-contract.md` — patient section
- `docs/api/api-contract.md` — patient endpoints
- `web/README.md` — dashboard smoke

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| Отдельные patient DTO | KPI ids и matrix rows ≠ doctor API |
| Submission detail link stub | out of scope iter 3 |

## Проверки

| Команда | Результат |
|---------|-----------|
| `pytest backend/tests/test_web_patient_api.py` | ✅ 7 passed |
| `make web-lint && make web-build` | ✅ |
| login `ivan_p` → `/dashboard` | ✅ live API |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ✅ Card, Table, ChartContainer |
| vercel-react-best-practices | ✅ RSC fetch, client chart only |
| nextjs-app-router-patterns | ✅ loading/error boundaries |
