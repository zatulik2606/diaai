# Seed data — progress import

Эталонная анонимизированная выгрузка для локальной разработки ([database iter 4](../docs/tasks/tasklist-database.md)).

| Файл | Назначение |
|------|------------|
| [progress-import.v1.json](progress-import.v1.json) | users, food/insulin events |

**Не путать** с [docs/data/](../docs/data/) — продуктовые сценарии и требования.

## Формат v2 (`schema_version: 2`)

```json
{
  "schema_version": 2,
  "users": [...],
  "food_events": [...],
  "insulin_events": [...],
  "progress_snapshots": [...],
  "consultations": [...],
  "recommendations": [],
  "photo_analyses": []
}
```

- **Идемпотентность:** фиксированные UUID; `ON CONFLICT DO NOTHING` по `id`.
- **`progress_snapshots`, `consultations`:** seed после миграции `002_*` (database iter 5).
- **`photo_analyses`:** создаются через API assistant (photo), не через seed.

## Загрузка

```bash
make db-seed
# или
uv run python scripts/db/seed_from_progress.py --file data/progress-import.v1.json
```

Полный сброс: `make db-reset` (volumes down → up → migrate → seed).

## Обновление seed

1. Отредактировать JSON, сохраняя стабильные `id` для существующих записей.
2. Новые записи — новые UUID.
3. Проверить FK: `user_id`, `food_event_id` ссылаются на существующие id.
4. `make db-seed` или `make db-reset`.

См. [database-access.md](../docs/tech/database-access.md) — секция «Локальное окружение и seed».
