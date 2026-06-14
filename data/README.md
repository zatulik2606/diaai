# Seed data — progress import

Эталонная анонимизированная выгрузка для локальной разработки ([database iter 4](../docs/tasks/tasklist-database.md), [frontend iter 1](../docs/tasks/tasklist-frontend.md)).

| Файл | Назначение |
|------|------------|
| [progress-import.v1.json](progress-import.v1.json) | users, dialogs, events, snapshots, photo_analyses |

**Не путать** с [docs/data/](../docs/data/) — продуктовые сценарии и требования.

## Формат v3 (`schema_version: 3`)

```json
{
  "schema_version": 3,
  "users": [...],
  "dialogs": [...],
  "dialog_requests": [...],
  "food_events": [...],
  "insulin_events": [...],
  "progress_snapshots": [...],
  "photo_analyses": [...],
  "consultations": [...],
  "recommendations": []
}
```

- **Demo doctor:** `@doctor_ivanov`, `display_name: Doctor Ivanov`, `telegram_id: 162684825`
- **Patients:** 6 diabetics с `telegram_username`, food/insulin за 14 дней
- **Dialogs/requests:** Q&A для dashboard questions и assistant history
- **Photo analyses:** 4 записи для submissions feed
- **Progress snapshots:** 3 недели × каждый patient

## Формат v2 (legacy)

v2 содержал только users + food/insulin без dialogs. Текущий файл — v3.

- **Идемпотентность:** фиксированные UUID; `ON CONFLICT DO NOTHING` по `id`.
- **`users.telegram_username`:** после миграции `003_*` (frontend iter 1).

## Загрузка

```bash
make db-seed
# или
uv run python scripts/db/seed_from_progress.py --file data/progress-import.v1.json
```

Полный сброс: `make db-reset` (volumes down → up → migrate → seed).

## Обновление seed

1. Редактировать `progress-import.v1.json` (фиксированные UUID).
2. `make db-seed` — idempotent, повторный запуск +0 строк.
3. `make db-inspect` — counts + users by role.
