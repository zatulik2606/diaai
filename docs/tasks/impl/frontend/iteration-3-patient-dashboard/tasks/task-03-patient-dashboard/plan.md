# Task 03: Панель пациента с диабетом

Итерация: [iteration-3-patient-dashboard](../../plan.md)

**Статус:** 📋 Planned · [summary](summary.md)

---

## Цель

Реализовать `/dashboard` для роли `diabetic`: backend patient-scoped API + frontend UI (KPI, chart, questions, submissions, matrix) на live данных seed v3.

## Текущее состояние (baseline)

| Готово | Не готово |
|--------|-----------|
| App shell iter 2, session с `telegram_id` | Patient API `/patient/dashboard/*` |
| Placeholder `/dashboard` | KPI, chart, tables, matrix |
| shadcn Card, Table, Chart wrapper | Dashboard components |
| Doctor API iter 1 (reference impl) | Patient-scoped queries |
| Seed v3 с demo-пациентами | Contract section patient |

## Порядок выполнения

### 📋 Фаза 0: Plan + contract gap

- Зафиксировать patient endpoint'ы в [frontend-contract.md](../../../../../api/frontend-contract.md)
- KPI ids для patient:

| KPI id | Label | PG |
|--------|-------|-----|
| `total_xe` | Сумма ХЕ за 7д | `food_events.xe` |
| `questions_count` | Вопросов за 7д | `dialog_requests` |
| `food_events_count` | Событий питания | `food_events` |
| `insulin_total` | Инсулин за 7д | `insulin_events` |

### 📋 Фаза 1: Backend patient API

**Deps** — `backend/api/v1/web/deps.py`:

```python
async def require_diabetic(patient_telegram_id: int, db=Depends(get_db)) -> User:
    return await UserRepository(db).require_diabetic(patient_telegram_id)
```

**Service** — `WebPatientService` (аналог `WebDoctorService`, scope = `[user.id]`):

| Method | Логика |
|--------|--------|
| `get_summary` | 4 KPI + delta vs prev window |
| `get_activity` | daily requests + food_events 14d |
| `get_questions` | paginated, без поля `patient` |
| `get_submissions` | food + photo для user |
| `get_progress_matrix` | 1 patient row или metric rows |

**Router** — `backend/api/v1/web/patient_dashboard.py`, prefix `/patient/dashboard`.

**Tests** — `backend/tests/test_web_patient_api.py`: login patient fixture, 200 + schema.

### 📋 Фаза 2: Web lib

**`lib/types/patient-dashboard.ts`** — TypeScript DTO (mirror OpenAPI).

**`lib/backend-client.ts`** — helpers:

```typescript
fetchPatientSummary(telegramId: number): Promise<DashboardSummary>
fetchPatientActivity(telegramId: number): Promise<ActivityResponse>
// …questions, submissions, matrix
```

Все fetch: server-only, `Authorization: Bearer`, `cache: 'no-store'`.

### 📋 Фаза 3: KPI + activity chart

**`components/dashboard/kpi-grid.tsx`** — 4 Card, value mono 3xl, delta badge (green/red по trend).

**`components/dashboard/activity-chart.tsx`** — `"use client"`, recharts LineChart, series `--chart-1` / `--chart-2`.

### 📋 Фаза 4: Questions + submissions

**`components/dashboard/questions-table.tsx`** — shadcn Table: время, вопрос, ответ.

**`components/dashboard/submissions-list.tsx`** — list items, тип food/photo, `detail_url` link.

### 📋 Фаза 5: Progress matrix

**`components/dashboard/progress-matrix.tsx`** — heatmap/table по [frontend-requirements § Зона 4](../../../../../spec/frontend-requirements.md); period selector (week default).

### 📋 Фаза 6: Dashboard page

**`app/(app)/dashboard/page.tsx`** — server component:

1. `getSession()` → `telegram_id` (redirect if missing)
2. `Promise.all` fetch 5 blocks
3. Grid layout по wireframe (2×2 + KPI row)

**`loading.tsx`** — Skeleton для KPI + chart + tables.

**`error.tsx`** — сообщение + retry button.

### 📋 Фаза 7: Verify + summary

```bash
make backend-test
make web-lint && make web-build
make web-dev
# login ivan_p → dashboard filled
```

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `backend/api/v1/web/patient_dashboard.py` | create |
| `backend/services/web_patient_service.py` | create |
| `backend/schemas/web.py` | extend PatientKpiId |
| `backend/api/v1/web/deps.py` | require_diabetic |
| `backend/api/v1/web/router.py` | include patient router |
| `backend/tests/test_web_patient_api.py` | create |
| `web/lib/types/patient-dashboard.ts` | create |
| `web/lib/backend-client.ts` | extend |
| `web/components/dashboard/*` | create |
| `web/app/(app)/dashboard/page.tsx` | replace placeholder |
| `web/app/(app)/dashboard/loading.tsx` | create |
| `web/app/(app)/dashboard/error.tsx` | create |
| `docs/api/frontend-contract.md` | patient section |
| `web/README.md` | dashboard smoke |

## Проверки

```bash
# Backend
curl -s "$BASE/api/v1/web/patient/dashboard/summary?patient_telegram_id=<ID>" \
  -H "Authorization: Bearer $TOKEN"

# Web (после login ivan_p)
open http://localhost:3000/dashboard
```

## Demo credentials

| username | telegram_id (seed) | ожидание |
|----------|-------------------|----------|
| `ivan_p` | из seed v3 | KPI > 0, questions в таблице |
| `akozhin` | 162684825 | middleware → `/leaderboard` |

## Skills

| Skill | Checklist |
|-------|-----------|
| shadcn | semantic colors, Table sticky header, ChartContainer |
| vercel-react-best-practices | fetch в RSC, client chart isolated |
| nextjs-app-router-patterns | loading/error boundaries |

## Definition of Done

**Агент:** patient API tests green; dashboard без mock; build green.

**Пользователь:** login `ivan_p` → заполненный dashboard; KPI и график соответствуют seed.
