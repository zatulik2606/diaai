# diaai Backend

FastAPI backend для MVP diaai: сценарий A (вопрос ассистенту) и сценарий B (события питания и инсулина). Контракт API — [api-contract.md](../docs/api/api-contract.md) (индекс: [`docs/api/`](../docs/api/)).

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker (для PostgreSQL)

## Quick start

Из корня репозитория:

```bash
cp .env.example .env
# Заполнить BACKEND_SERVICE_TOKEN и OPENROUTER_API_KEY (см. раздел «Конфигурация»)

make backend-install
make db-reset              # PostgreSQL :5433 + migrate + seed
make backend-run           # http://127.0.0.1:8000
```

Проверка данных: `make db-inspect`.

Проверка:

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok","version":"1.0.0"}
```

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Конфигурация

Переменные читаются из `.env` в корне репозитория (см. [`backend/config.py`](config.py)).

| Переменная | Обязательна | Описание |
|------------|-------------|----------|
| `BACKEND_SERVICE_TOKEN` | да | Bearer-токен для `/api/v1/*`. Значения с `:` — в кавычках: `"my:secret"` |
| `DATABASE_URL` | да | Async PG URL; default `postgresql+asyncpg://diaai:diaai@localhost:5433/diaai` |
| `OPENROUTER_API_KEY` | да для assistant | LLM через OpenRouter; без ключа `POST /assistant/messages` → 502 |
| `LLM_MODEL` | нет | default `openrouter/auto` |
| `LLM_MAX_HISTORY` | нет | сообщений в контексте диалога, default `10` |
| `LLM_TIMEOUT_SECONDS` | нет | таймаут LLM, default `30` |
| `BACKEND_HOST` / `BACKEND_PORT` | нет | bind uvicorn, default `127.0.0.1:8000` |
| `STT_MODEL` | нет | модель STT через OpenRouter, default `openai/whisper-large-v3` |
| `STT_TIMEOUT_SECONDS` | нет | таймаут транскрипции, default `60` |
| `ANALYTICS_QUERY_MODEL` | нет | LLM для Text-to-SQL, default `openrouter/auto` |
| `ANALYTICS_QUERY_TIMEOUT_SECONDS` | нет | таймаут SQL-запроса, default `5` |
| `ANALYTICS_QUERY_ROW_LIMIT` | нет | max строк результата, default `100` |
| `ANALYTICS_QUERY_LLM_TIMEOUT_SECONDS` | нет | таймаут генерации SQL, default `30` |
| `GLITCHTIP_DSN` | нет | GlitchTip (проект `diaai-backend`); пусто = выкл. · [devops/glitchtip/hosted.md](../devops/glitchtip/hosted.md) |
| `GLITCHTIP_ENVIRONMENT` | нет | default `development` |
| `GLITCHTIP_TRACES_SAMPLE_RATE` | нет | default `0.01` (1% transactions); GlitchTip: `auto_session_tracking=False` в коде |
| `GLITCHTIP_DEBUG_TOKEN` | нет | Bearer для `GET /debug/glitchtip-test`; пусто = маршрут **404** (не регистрируется) |

События питания/инсулина (`/api/v1/events/*`) работают без OpenRouter.

### GlitchTip smoke (debug endpoint)

Требует `GLITCHTIP_DSN` и непустой `GLITCHTIP_DEBUG_TOKEN`. Ответ не содержит DSN.

```bash
curl -sf -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" \
  http://127.0.0.1:8000/debug/glitchtip-test
# → {"ok":true,"project":"diaai-backend"}
```

Web (server route): `GET /api/debug/glitchtip-test` с тем же Bearer — [devops/monitoring/README.md](../devops/monitoring/README.md).

## Команды Makefile

| Команда | Назначение |
|---------|------------|
| `make backend-install` | `uv sync` — зависимости |
| `make backend-run` | uvicorn с reload |
| `make backend-migrate` | `alembic upgrade head` |
| `make backend-test` | pytest (**67** backend tests; full suite: `make test` → 84) |
| `make backend-lint` | ruff check |
| `make backend-format` | ruff format |
| `make backend-openapi-export` | dump `/openapi.json` для diff (не коммитить) |

### Локальная БД

| Команда | Назначение |
|---------|------------|
| `make db-up` | PostgreSQL в Docker + wait healthy |
| `make db-down` | остановка контейнера |
| `make db-reset` | чистая БД: down -v → up → migrate → seed |
| `make db-migrate` | alias `make backend-migrate` |
| `make db-seed` | загрузка [`data/progress-import.v1.json`](../data/progress-import.v1.json) |
| `make db-shell` | psql в контейнере |
| `make db-inspect` | counts и sample rows (без ПДн) |

## API и авторизация

- **`GET /health`** — без auth, health check.
- **`/api/v1/*`** — заголовок `Authorization: Bearer <BACKEND_SERVICE_TOKEN>`.
- Пользователь идентифицируется полем **`telegram_id`** в JSON body (POST) или query (GET).
- Опционально: `X-Request-Id` (UUID) для трассировки.

### Swagger Authorize

В `/docs` нажать **Authorize** и ввести **только значение** токена из `.env` (без префикса `Bearer`).

## Примеры curl

Подставьте свой токен:

```bash
export TOKEN="your-backend-service-token"
export BASE="http://127.0.0.1:8000"
```

**Assistant (сценарий A):**

```bash
curl -s -X POST "$BASE/api/v1/assistant/messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456789, "text": "Сколько ХЕ в борще?"}'
```

**Создать событие питания (сценарий B):**

```bash
curl -s -X POST "$BASE/api/v1/events/food" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456789, "description": "борщ", "xe": 3.5, "bje": 1.0, "source": "text"}'
```

**Список событий питания:**

```bash
curl -s "$BASE/api/v1/events/food?telegram_id=123456789" \
  -H "Authorization: Bearer $TOKEN"
```

**Web dashboard (demo doctor `@doctor_ivanov`, telegram_id `162684825`):**

```bash
curl -s "$BASE/api/v1/web/auth/resolve" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "doctor_ivanov"}'

curl -s "$BASE/api/v1/web/doctor/dashboard/summary?doctor_telegram_id=162684825" \
  -H "Authorization: Bearer $TOKEN"

curl -s "$BASE/api/v1/web/leaderboard?doctor_telegram_id=162684825" \
  -H "Authorization: Bearer $TOKEN"
```

**Patient dashboard (demo `@ivan_p`, telegram_id `900000001`):**

```bash
curl -s "$BASE/api/v1/web/patient/dashboard/summary?patient_telegram_id=900000001" \
  -H "Authorization: Bearer $TOKEN"
```

**Analytics NL query (doctor):**

```bash
curl -s -X POST "$BASE/api/v1/web/analytics/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"doctor_telegram_id": 162684825, "question": "Сколько событий питания за неделю?"}'
```

## Docker Compose

Корневой [`docker-compose.yml`](../docker-compose.yml) — **полный stack**: postgres, backend, web; bot — profile `bot`.

| Режим | Команда |
|-------|---------|
| Полный stack | `make stack-up` |
| Только PostgreSQL | `make db-up` |
| Bot + stack | `make stack-up-bot` |

- Host port **5433** → container 5432.
- Volume `diaai_pg_data`.
- Backend в контейнере: migrate on start, `DATABASE_URL=@postgres:5432`.

Guide: [docs/devops/docker-compose-local.md](../docs/devops/docker-compose-local.md).

```bash
make db-up           # только postgres
docker compose ps    # healthcheck: healthy
make stack-up        # postgres + backend + web
```

## Тесты

```bash
make backend-test
```

Smoke: `backend/tests/test_health.py`, `backend/tests/test_auth.py`.  
Тесты in-process (ASGI + sqlite in-memory, mock LLM), без running server.

## Troubleshooting

| Симптом | Причина | Решение |
|---------|---------|---------|
| Connection refused :5433 | PG не запущен | `make db-up` |
| 401 `UNAUTHORIZED` | неверный/отсутствует Bearer | проверить `BACKEND_SERVICE_TOKEN` в `.env` и заголовок |
| 502 `LLM_UNAVAILABLE` | OpenRouter | задать `OPENROUTER_API_KEY` |
| 503 на API | нет БД | `make backend-migrate`, проверить `DATABASE_URL` |
| Токен с `:` не работает | парсинг `.env` | обернуть значение в кавычки |

## Документация

- [API-контракт v1](../docs/api/api-contract.md) — endpoint'ы, схемы, ошибки
- [API conventions](../docs/api/conventions.md)
- [OpenAPI yaml](../docs/api/openapi.yaml) — machine-readable контракт
- [Сценарии](../docs/api/scenarios/)
- [Design review](../docs/tech/api-contracts.md)
- [Architecture](../docs/architecture.md)
- [Tasklist backend](../docs/tasks/tasklist-backend.md)

## Миграции и БД

PostgreSQL через SQLAlchemy 2 async + Alembic. Миграции: `001_initial_schema` → `002_full_data_layer` → `003_telegram_username` (9 таблиц + `users.telegram_username`). Архитектура — [ADR-003](../docs/adr/adr-003-data-access-layer.md). Guide — [database-access.md](../docs/tech/database-access.md).

Web routes: `backend/api/v1/web/` — auth, patient/doctor dashboard, leaderboard, assistant history, analytics query. STT: `backend/api/v1/media.py` → `POST /api/v1/media/transcribe`. Контракт — [frontend-contract.md](../docs/api/frontend-contract.md).

```bash
make db-reset              # 001 + 002 + seed
make backend-migrate       # alembic upgrade head
make backend-test
```

Новые таблицы `002`: `photo_analyses`, `progress_snapshots`, `recommendations`, `consultations`. Photo-запросы assistant persist → `photo_analyses` (structured fields — backend iter 11).
