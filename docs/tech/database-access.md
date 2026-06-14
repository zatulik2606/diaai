# Доступ к PostgreSQL в backend

Практический guide для разработчиков. Архитектурное решение — [ADR-003](../adr/adr-003-data-access-layer.md). Физическая схема — [schema-er.md](../spec/schema-er.md).

## Карта файлов

| Путь | Назначение |
|------|------------|
| [`backend/database.py`](../../backend/database.py) | `Base`, engine, `get_db`, init/dispose |
| [`alembic/`](../../alembic/) + [`alembic.ini`](../../alembic.ini) | миграции |
| [`alembic/env.py`](../../alembic/env.py) | async runner, `target_metadata`, import моделей |
| [`backend/models/`](../../backend/models/) | ORM — **один файл на таблицу** |
| [`backend/repositories/`](../../backend/repositories/) | SQLAlchemy queries |
| [`backend/services/`](../../backend/services/) | доменная логика, orchestration |
| [`backend/api/v1/`](../../backend/api/v1/) | routers — **без SQL** |
| [`docs/spec/schema-er.md`](../spec/schema-er.md) | DDL; `002_full_data_layer` ✅ |
| [`scripts/db/`](../../scripts/db/) | seed, inspect (iter 4) |
| [`data/progress-import.v1.json`](../../data/progress-import.v1.json) | эталонный seed |

## Поток данных

```
HTTP handler  →  Service  →  Repository  →  AsyncSession  →  PostgreSQL
                     ↑
              Depends(get_db) — commit/rollback на конец запроса
```

Пример: [`events.py`](../../backend/api/v1/events.py) → [`events_service.py`](../../backend/services/events_service.py) → [`food_event.py`](../../backend/repositories/food_event.py).

## Workflow: новая таблица (5 шагов)

### 1. Схема

Колонки, FK, индексы — в [schema-er.md](../spec/schema-er.md). Для таблиц из draft `002` спецификация уже есть (iter 2 ✅).

### 2. Alembic revision

```bash
uv run alembic revision -m "add_photo_analyses"
```

Отредактировать `alembic/versions/00N_*.py`: `upgrade()` / `downgrade()` по DDL из [schema-er §6](../spec/schema-er.md#6-appendix-draft-migration-002).

Применить:

```bash
make backend-migrate
```

### 3. SQLAlchemy model

Создать `backend/models/<entity>.py`:

```python
class PhotoAnalysis(Base):
    __tablename__ = "photo_analyses"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # ... колонки по schema-er
```

Образец: [`backend/models/food_event.py`](../../backend/models/food_event.py).

### 4. Register model

Добавить import и `__all__` в:

- [`backend/models/__init__.py`](../../backend/models/__init__.py)
- [`alembic/env.py`](../../alembic/env.py) — **обязательно**, иначе autogenerate не увидит таблицу

### 5. Repository + Service + Handler

1. `backend/repositories/<entity>.py` — `select`, `add`, `flush`; без `AppError`
2. `backend/services/<domain>_service.py` — бизнес-правила, ownership, вызов repos
3. Router — `db: AsyncSession = Depends(get_db)`, передать session в service

```python
@router.post("/events/food")
async def create_food(
    body: FoodEventCreate,
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> EventCreated:
    service = EventsService(db)
    return await service.create_food(body)
```

## Make-команды

### Backend

| Команда | Действие |
|---------|------------|
| `make backend-migrate` | `alembic upgrade head` |
| `make backend-test` | pytest backend (sqlite in-memory) |
| `make backend-run` | uvicorn с reload |
| `uv run alembic revision -m "..."` | новая revision |
| `uv run alembic downgrade -1` | откат одной revision *(осторожно, dev only)* |
| `uv run alembic current` | текущая revision |
| `uv run alembic history` | список revisions |

### Локальная БД (`db-*`)

| Команда | Действие |
|---------|------------|
| `make db-up` | `docker compose up -d` + wait healthy |
| `make db-down` | остановка PostgreSQL |
| `make db-reset` | volumes down → up → migrate → seed |
| `make db-migrate` | alias `make backend-migrate` |
| `make db-seed` | загрузка [`data/progress-import.v1.json`](../../data/progress-import.v1.json) |
| `make db-shell` | `psql` в контейнере postgres |
| `make db-inspect` | counts + sample rows (без ПДн по умолчанию) |

## Локальное окружение и seed

**Быстрый старт (чистая seeded БД):**

```bash
cp .env.example .env
make db-reset
make db-inspect
```

`make db-reset` выполняет: `docker compose down -v` → `db-up` → `db-migrate` → `db-seed`.

**Идемпотентность seed:** [`scripts/db/seed_from_progress.py`](../../scripts/db/seed_from_progress.py) использует `INSERT ... ON CONFLICT (id) DO NOTHING` по первичному ключу. Повторный `make db-seed` не создаёт дубликаты — counts в `make db-inspect` не растут.

**Формат данных:** [`data/progress-import.v1.json`](../../data/progress-import.v1.json) — users, food_events, insulin_events; `progress_snapshots` — пустой массив до iter 5. См. [`data/README.md`](../../data/README.md).

**Inspect без ПДн:** по умолчанию не показывает `telegram_id` и тексты описаний; `--verbose` — усечённые description/comment:

```bash
uv run python scripts/db/db_inspect.py --verbose
```

## Конфигурация

| Переменная | Default | Описание |
|------------|---------|----------|
| `DATABASE_URL` | `postgresql+asyncpg://diaai:diaai@localhost:5433/diaai` | async PG URL |

См. также [`backend/README.md`](../../backend/README.md) и [`.env.example`](../../.env.example).

## Тестирование

**Unit/contract (CI, локально):**

- [`backend/tests/conftest.py`](../../backend/tests/conftest.py) — sqlite `:memory:`, override `get_db`
- `make backend-test` — без running PostgreSQL

**Integration (ручная):**

```bash
make db-reset
make backend-run
# curl к /api/v1/...
```

Не логировать промпты, тексты сообщений, токены — [conventions.mdc](../../.cursor/rules/conventions.mdc).

## Troubleshooting

| Симптом | Причина | Решение |
|---------|---------|---------|
| `Database is not available` (503) | `DATABASE_URL` пуст или PG down | `make db-up`, проверить `.env` |
| Connection refused :5433 | PostgreSQL не запущен | `make db-up` |
| `Can't locate revision` | рассинхрон alembic | `uv run alembic current`; применить `make backend-migrate` |
| Autogenerate не видит таблицу | модель не в `env.py` | добавить import в `alembic/env.py` |
| Тест падает на PG-специфике | sqlite ≠ PG | проверить на docker PG или упростить тест |
| Duplicate revision | две head | `alembic heads`, merge или fix down_revision |
| Seed дублирует записи | изменены id в JSON | использовать стабильные UUID; `make db-reset` для чистой БД |

## Соглашения (кратко)

| Делай | Не делай |
|-------|----------|
| SQLAlchemy queries в repository | Raw SQL в handler |
| Бизнес-логику в service | HTTP/AppError в repository |
| Один файл модели на таблицу | Generic BaseRepository на MVP |
| `snake_case` имён = schema-er | VARCHAR(n) — используй TEXT |
| `flush()` когда нужен id до commit | `session.commit()` в service |

## Связанные документы

- [ADR-003](../adr/adr-003-data-access-layer.md)
- [backend-structure.md](backend-structure.md)
- [schema-er.md](../spec/schema-er.md)
- [tasklist-database.md](../tasks/tasklist-database.md)
- [data/README.md](../../data/README.md)
