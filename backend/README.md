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
docker compose up -d          # PostgreSQL на localhost:5433
make backend-migrate
make backend-run              # http://127.0.0.1:8000
```

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
| `LOG_LEVEL` | нет | default `INFO` |

События питания/инсулина (`/api/v1/events/*`) работают без OpenRouter.

## Команды Makefile

| Команда | Назначение |
|---------|------------|
| `make backend-install` | `uv sync` — зависимости |
| `make backend-run` | uvicorn с reload |
| `make backend-migrate` | `alembic upgrade head` |
| `make backend-test` | pytest (30 тестов) |
| `make backend-lint` | ruff check |
| `make backend-format` | ruff format |
| `make backend-openapi-export` | dump `/openapi.json` для diff (не коммитить) |

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

## Docker Compose

В репозитории только **PostgreSQL** (backend запускается локально через `make backend-run`):

- Host port **5433** → container 5432 (если локальный 5432 занят другим PG).
- Volume `diaai_pg_data` для персистентности данных.

```bash
docker compose up -d
docker compose ps    # healthcheck: healthy
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
| Connection refused :5433 | PG не запущен | `docker compose up -d` |
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
- [Tasklist backend](../docs/tasks/tasklist-backend.md)
