# Сценарии D3/D4: сигналы и рекомендации (analytics REST)

Полный контракт: [api-contract.md](../api-contract.md) · Продукт: [user-scenarios.md](../../spec/user-scenarios.md) (D3, D4) · Сущность: Recommendation · Соглашения: [conventions.md](../conventions.md)

> **Ограничение:** рекомендации и сигналы **справочные**. Тексты не содержат назначения доз инсулина.

## GET /api/v1/analytics/signals

Эвристики изменений рациона и инсулина за период (rule-based, без LLM в v1).

### Query

| Параметр | Тип | Обязательный | Default |
|----------|-----|--------------|---------|
| `telegram_id` | integer | да | — |
| `period` | enum | нет | `week` — `week` · `month` |

### Response 200

```json
{
  "telegram_id": 900000001,
  "period": "week",
  "signals": [
    {
      "code": "xe_up",
      "severity": "info",
      "metric": "xe",
      "direction": "up",
      "message": "Сумма ХЕ за неделю выросла на 12% относительно прошлой недели",
      "delta_pct": 11.8
    },
    {
      "code": "insulin_stable",
      "severity": "info",
      "metric": "insulin",
      "direction": "flat",
      "message": "Общий инсулин за период без существенных изменений",
      "delta_pct": 0.0
    }
  ]
}
```

| Поле | Описание |
|------|----------|
| `code` | стабильный идентификатор правила (`xe_up`, `xe_down`, `insulin_up`, …) |
| `severity` | `info` · `warning` |
| `metric` | `xe` · `bje` · `insulin` |
| `direction` | `up` · `down` · `flat` |
| `message` | человекочитаемый текст на русском |
| `delta_pct` | изменение метрики vs предыдущий период |

Пустой массив `signals` — допустим (нет значимых отклонений).

### Errors

Те же, что у [analytics-progress.md](analytics-progress.md) (`401`, `403`, `404`, `422`).

---

## GET /api/v1/analytics/recommendations

Справочные рекомендации пользователю: persist из `recommendations` + rule-based (task 11).

### Query

| Параметр | Тип | Default | Max |
|----------|-----|---------|-----|
| `telegram_id` | integer | обязательный | — |
| `limit` | integer | 10 | 50 |
| `offset` | integer | 0 | — |

### Response 200

```json
{
  "telegram_id": 900000001,
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "type": "nutrition",
      "text": "За неделю сумма ХЕ выше среднего — имеет смысл сверить перекусы с дневником.",
      "created_at": "2026-06-07T10:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440011",
      "type": "dynamics",
      "text": "Динамика БЖЕ стабильна — продолжайте фиксировать приёмы пищи.",
      "created_at": "2026-06-06T18:30:00Z"
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}
```

| `type` | Смысл |
|--------|--------|
| `nutrition` | питание, ХE/БЖE |
| `insulin` | контекст инсулина **без доз** |
| `dynamics` | общая динамика периода |

### Errors

| HTTP | code | Когда |
|------|------|-------|
| 401 | `UNAUTHORIZED` | Bearer |
| 403 | `FORBIDDEN` | не `diabetic` |
| 404 | `NOT_FOUND` | user |
| 422 | — | `limit`/`offset` |

### Пример

```bash
curl -s "$BASE/api/v1/analytics/recommendations?telegram_id=900000001&limit=5" \
  -H "Authorization: Bearer $TOKEN"
```
