# Seed data — progress import

Эталонная анонимизированная выгрузка для локальной разработки ([database iter 4](../docs/tasks/tasklist-database.md)).

| Файл | Назначение |
|------|------------|
| [progress-import.v1.json](progress-import.v1.json) | users, food/insulin events |

**Не путать** с [docs/data/](../docs/data/) — продуктовые сценарии и требования.

## Формат v1

```json
{
  "schema_version": 1,
  "users": [...],
  "food_events": [...],
  "insulin_events": [...],
  "progress_snapshots": []
}
```

- **Идемпотентность:** фиксированные UUID в JSON; повторный `make db-seed` не создаёт дублей (`ON CONFLICT DO NOTHING` по `id`).
- **Анонимизация:** `telegram_id` из диапазона `900000xxx`; синтетические описания еды, без реальных ПДн.
- **`progress_snapshots`:** пустой массив — заполнение в database iter 5 после миграции `002_*`.

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
