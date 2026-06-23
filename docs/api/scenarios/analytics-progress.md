# Сценарий D3: снимок прогресса (analytics REST)

Полный контракт: [api-contract.md](../api-contract.md) · Продукт: [user-scenarios.md](../../spec/user-scenarios.md) (D3) · Сущности: ProgressSnapshot, FoodEvent, InsulinEvent · Соглашения: [conventions.md](../conventions.md)

Единый API для бота и клиентов вне web-dashboard. Web UI использует отдельные DTO — [frontend-contract.md](../frontend-contract.md).

## GET /api/v1/analytics/progress

Агрегат ХЕ, БЖЕ, инсулина (и опционально БЖУ) за период + сравнение с предыдущим окном.

### Query

| Параметр | Тип | Обязательный | Default | Описание |
|----------|-----|--------------|---------|----------|
| `telegram_id` | integer | да | — | Владелец данных (роль `diabetic`) |
| `period` | enum | нет | `week` | `day` · `week` · `month` |

### Response 200

```json
{
  "telegram_id": 900000001,
  "period": "week",
  "period_start": "2026-06-01",
  "period_end": "2026-06-07",
  "sums": {
    "xe": 42.5,
    "bje": 12.0,
    "insulin": 28.0,
    "proteins": 180.0,
    "fats": 65.0,
    "carbs": 210.0
  },
  "previous_period": {
    "period_start": "2026-05-25",
    "period_end": "2026-05-31",
    "sums": {
      "xe": 38.0,
      "bje": 11.5,
      "insulin": 26.5,
      "proteins": null,
      "fats": null,
      "carbs": null
    }
  },
  "delta_pct": {
    "xe": 11.8,
    "bje": 4.3,
    "insulin": 5.7
  },
  "trend": "stable",
  "comment": null,
  "source": "computed"
}
```

| Поле | Описание |
|------|----------|
| `period_start` / `period_end` | inclusive calendar dates (UTC) |
| `sums` | агрегаты текущего окна |
| `previous_period` | то же для предшествующего окна той же длины |
| `delta_pct` | `(current - previous) / previous * 100`; при `previous=0` → `100` если current>0, иначе `0` |
| `trend` | `improving` · `stable` · `worsening` — по знаку delta ХE (см. task 10) |
| `source` | `computed` — из событий; `snapshot` — материализованная строка `progress_snapshots` |

### Errors

| HTTP | code | Когда |
|------|------|-------|
| 401 | `UNAUTHORIZED` | нет/неверный Bearer |
| 403 | `FORBIDDEN` | user не `diabetic` |
| 404 | `NOT_FOUND` | `telegram_id` не найден |
| 422 | — | неверный `period` |

### Пример

```bash
curl -s "$BASE/api/v1/analytics/progress?telegram_id=900000001&period=week" \
  -H "Authorization: Bearer $TOKEN"
```

Demo user после `make db-reset`: `@ivan_p` → `900000001`.
