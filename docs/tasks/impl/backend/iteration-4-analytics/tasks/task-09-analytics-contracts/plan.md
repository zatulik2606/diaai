# Task 09: Контракты analytics REST

Опирается на [iteration-4 plan](../../plan.md) · [plan.md](../../../../../../plan.md#итерация-4--аналитика-и-динамика-backend-rest) · [user-scenarios.md](../../../../../../spec/user-scenarios.md) (D3, D4)

## Цель

Зафиксировать contract-first API `/api/v1/analytics/*` для бота и будущих клиентов — до реализации (task 10–11).

## Контекст репозитория

| Уже есть | Не дублировать |
|----------|----------------|
| `/api/v1/web/patient|doctor/dashboard/*` ✅ | другие DTO, doctor cohort |
| `/api/v1/web/analytics/query` ✅ (Text-to-SQL) | NL → SQL, doctor-only |
| Таблицы `progress_snapshots`, `recommendations` ✅ | seed + ORM |
| `web_utils.compute_trend`, repos агрегации ✅ | переиспользовать в task 10 |

## Endpoint'ы (контракт)

| Method | Path | Сценарий | Query |
|--------|------|----------|-------|
| GET | `/api/v1/analytics/progress` | D3 | `telegram_id`, `period=day\|week\|month` |
| GET | `/api/v1/analytics/signals` | D3 | `telegram_id`, `period=week\|month` |
| GET | `/api/v1/analytics/recommendations` | D4 | `telegram_id`, `limit`, `offset` |

Auth: Bearer (как bot). User: `telegram_id` в query. Role: только `diabetic` (403 иначе).

## Решения контракта

| Тема | Решение |
|------|---------|
| Агрегация progress | on-the-fly из `food_events` + `insulin_events` (task 10); поле `source`: `computed` \| `snapshot` |
| Период `day` | rolling 24h UTC; `week`/`month` — rolling 7/30 days |
| `trend` | `improving` \| `stable` \| `worsening` — по delta суммы ХE vs предыдущий период |
| Signals | rule-based список; severity `info` \| `warning`; без LLM в v1 |
| Recommendations | read из `recommendations` + rule-based append (task 11); **без доз инсулина** |
| Ошибки | 404 user, 403 role, 422 period — [conventions.md](../../../../../../api/conventions.md) |

## Артефакты

| Файл | Действие |
|------|----------|
| `docs/api/scenarios/analytics-progress.md` | создать |
| `docs/api/scenarios/analytics-signals-recommendations.md` | создать |
| `docs/api/api-contract.md` | секция analytics 📋 impl |
| `docs/api/openapi.yaml` | paths + schemas, tag `analytics` |
| `docs/tech/api-contracts.md` | карта endpoint'ов |
| `docs/data-model.md` | cross-ref analytics REST (если нужно) |

## Definition of Done

**Агент:** контракты согласованы; openapi валиден; task-09 `summary.md`; tasklist 09 → ✅.

**Пользователь:** по scenarios понятно, чем `/analytics/*` отличается от `/web/*`.

## Следующая задача

[task-10-progress-snapshots](../task-10-progress-snapshots/plan.md) — impl `GET /analytics/progress`.
