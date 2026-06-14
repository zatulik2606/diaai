# Task 04: Лидерборд

Итерация: [iteration-4-leaderboard](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** 📋 Next

---

## Цель

Реализовать `/leaderboard`: backend DTO с продуктами и медалями топ-5 БЖЕ + UI (таблица / scatter).

## Состав работ

### Backend

- [ ] `LeaderboardProduct` + `BjeMedal` в `backend/schemas/web.py`
- [ ] `FoodEventRepository.products_by_user()` — group by `description`, sum xe/bje
- [ ] `WebLeaderboardService`: cohort top-5 BJE → `bje_medal`; убрать `medal` за rank
- [ ] Обновить `test_web_api.py::test_leaderboard_*`

### Frontend

- [ ] `web/lib/types/leaderboard.ts`
- [ ] `fetchLeaderboard()` в `backend-client.ts`
- [ ] `components/leaderboard/leaderboard-table.tsx` — rank, progress, product chips
- [ ] `components/leaderboard/product-chip.tsx` — icon + xe + bje medal overlay
- [ ] `components/leaderboard/leaderboard-scatter.tsx` — recharts scatter
- [ ] `components/leaderboard/leaderboard-tabs.tsx` — Table / Scatter
- [ ] `app/(app)/leaderboard/page.tsx` + `loading.tsx` + `error.tsx`

## Затронутые файлы

| Область | Файлы |
|---------|-------|
| Backend | `schemas/web.py`, `repositories/food_event.py`, `services/web_leaderboard_service.py`, `services/web_utils.py`, `tests/test_web_api.py` |
| Frontend | `lib/types/leaderboard.ts`, `lib/backend-client.ts`, `components/leaderboard/*`, `app/(app)/leaderboard/*` |
| Docs | `frontend-contract.md`, `api-contract.md`, `openapi.yaml`, summaries |

## UI (из spec)

- Period + metric selectors (query sync optional MVP)
- Table: `#` | Patient | Progress bar | Products (icon + XE + BJE medal)
- Scatter: axes from API, tooltip name + x/y
- Empty: «Нет пациентов»; error: retry

## Проверка

```bash
make backend-test   # test_web_api leaderboard
make web-dev        # doctor_ivanov → /leaderboard
curl -s "http://127.0.0.1:8000/api/v1/web/leaderboard?doctor_telegram_id=162684825&period=30d" \
  -H "Authorization: Bearer $TOKEN" | jq '.table[0].products'
```

## Definition of Done

- API возвращает `products[]` с `bje_medal` для топ-5 БЖЕ когорты
- UI отображает оба режима без remount bugs
- Legacy `metrics`/`medal` удалены из backend response
