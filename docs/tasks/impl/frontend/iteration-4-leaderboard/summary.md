# Итерация frontend 4: Summary

> **Статус:** 📋 Next (планирование ✅ · реализация — не начата)

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано (подготовка)

### Спецификация и контракты

Обновлена модель лидерборда (зона 2) по новым требованиям: продукты + ХЕ, медали топ-5 БЖЕ на продукты (не топ-3 за место пациента).

| Артефакт | Изменение |
|----------|-----------|
| `docs/spec/frontend-requirements.md` | wireframe, колонки таблицы, медали топ-5 БЖЕ |
| `docs/spec/frontend-design-system.md` | S7 топ-5 БЖЕ, Badge → product chips |
| `docs/api/frontend-contract.md` | `table[].products[]`, `bje_medal`; legacy `metrics`/`medal` — миграция iter 4 |
| `docs/api/api-contract.md` | leaderboard response, demo `doctor_ivanov` |
| `docs/api/openapi.yaml` | `LeaderboardProduct`, deprecated legacy fields |
| `docs/tasks/tasklist-frontend.md` | iter 4 DoD, критерии области |

### Планирование

| Артефакт | Путь |
|----------|------|
| План итерации | [plan.md](plan.md) |
| План task 04 | [tasks/task-04-leaderboard/plan.md](tasks/task-04-leaderboard/plan.md) |
| Сводный plan области | [../plan.md](../plan.md) |

### Синхронизация demo

- `akozhin` → `doctor_ivanov` во всех актуальных smoke/curl и планах
- Placeholder `/leaderboard` — описание обновлено под новый scope

## Не сделано (реализация task 04)

| Блок | Статус |
|------|--------|
| Backend `products[]` + `bje_medal` | ❌ legacy `metrics` + `medal` топ-3 |
| `WebLeaderboardService` / repo | ❌ |
| Frontend `/leaderboard` UI | ❌ placeholder |
| `test_web_api.py` leaderboard | ❌ старые assertions |
| Task-04 summary | ❌ после реализации |

## Gap (iter 1 → iter 4)

| Legacy (сейчас) | Целевое |
|-----------------|---------|
| `table[].medal` за rank 1–3 | убрать |
| `table[].metrics` (xe/bje/insulin) | `table[].products[]` |
| — | `bje_medal`: топ-5 продуктов когорты по БЖЕ |

## Решения

| Решение | Обоснование |
|---------|-------------|
| Продукт = `food_events.description` | нет отдельной таблицы продуктов на MVP |
| Медали на продукты, не на rank | новое ТЗ экрана 2 |
| Legacy DTO помечен deprecated в openapi | iter 4 UI + backend в одном PR |
| Scatter без изменений | оси `metric_x` / `metric_y` из API |

## Проблемы

Нет блокеров. Код не менялся — `make lint` / `make web-build` не перезапускались.

## Следующий шаг

Реализация [task-04-leaderboard/plan.md](tasks/task-04-leaderboard/plan.md):

1. Backend DTO + `products_by_user()` + cohort top-5 BJE
2. Frontend table/scatter + product chips
3. Summary task 04 + закрытие итерации

## User-check (после реализации)

```bash
make db-reset && make backend-run
make web-dev
# login doctor_ivanov → /leaderboard: продукты, ХЕ, медали БЖЕ, scatter
```
