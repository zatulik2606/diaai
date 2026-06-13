# Task 03: Каркас backend + API-скелет

Опирается на [ADR-002](../../../../../adr/adr-002-backend-stack.md) · [openapi.yaml](../../../../../api/openapi.yaml)

Skills: [api-design-principles](.agents/skills/api-design-principles/SKILL.md) · [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md)

## Цель

Async FastAPI-каркас с REST-скелетом v1: готов к contract-тестам (task-04) и реализации (task-05).

## Чеклист

### 1. Структура каталогов

```
backend/
├── __init__.py
├── main.py              # FastAPI app, lifespan, middleware
├── config.py            # Settings (pydantic-settings)
├── api/
│   ├── deps.py          # verify_service_token, get_settings
│   └── v1/
│       ├── router.py
│       ├── assistant.py # async POST /assistant/messages (stub 501)
│       └── events.py    # async POST/GET events (stub 501)
├── schemas/
│   ├── assistant.py
│   ├── events.py
│   └── errors.py
├── exceptions.py
└── tests/
    └── conftest.py      # AsyncClient, app fixture (задел task-04)
```

Design review: [backend-structure.md](../../../../../tech/backend-structure.md) (fastapi-templates).

### 2. Инфраструктура

- [ ] `pyproject.toml`: пакет `backend` (`where = ["src", "."]`, include `backend*`); deps: fastapi, uvicorn, pydantic-settings
- [ ] dev-deps: **httpx**, pytest, pytest-asyncio
- [ ] Запуск: `uv run uvicorn backend.main:app --host … --port …` → `make backend-run`
- [ ] `GET /health` → `{ "status": "ok" }`, без auth
- [ ] Makefile: `backend-install`, `backend-run`, `backend-lint`, `backend-format`
- [ ] `.env.example`: `BACKEND_SERVICE_TOKEN`, `BACKEND_HOST`, `BACKEND_PORT`

### 3. FastAPI patterns (fastapi-templates)

- [ ] **Async:** все route handlers `async def`; middleware async-compatible
- [ ] **Lifespan** (`@asynccontextmanager`): placeholder startup/shutdown (DB pool — task-05)
- [ ] **DI:** `Depends(verify_service_token)`, `Depends(get_settings)` в `api/deps.py`
- [ ] **App factory:** `app = create_app()` в `main.py` для переиспользования в tests

### 4. API design (api-design-principles)

- [ ] Prefix `/api/v1` на APIRouter
- [ ] Paths как в openapi.yaml
- [ ] Bearer missing/invalid → **401** `UNAUTHORIZED`
- [ ] `AppError` handlers → `{ error: { code, message, details } }`
- [ ] Middleware `X-Request-Id`
- [ ] OpenAPI: title `diaai Backend API`, version `1.0.0`, tags

### 5. Pydantic-схемы (task-02)

- `AssistantMessageRequest`, `AssistantMessageResponse`
- `FoodEventCreate`, `InsulinEventCreate`, `EventCreated`

### 6. Tests scaffold (task-04)

```python
# backend/tests/conftest.py — минимум
@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
```

- [ ] Fixture `auth_headers` с `BACKEND_SERVICE_TOKEN`
- [ ] Пустой `test_health.py` — smoke `GET /health`

### 7. Stub (до task-05)

- Endpoints принимают body по схемам → **501** `NOT_IMPLEMENTED` единообразно

## Затронутые файлы

- `backend/**`, `pyproject.toml`, `Makefile`, `.env.example`

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | `make backend-run`; `/health` 200; no Bearer → 401; `pytest backend/tests/test_health.py` OK |
| Пользователь | `/docs` paths v1; `uvicorn backend.main:app` из Makefile |

## Вне scope

- PostgreSQL, OpenRouter, `database.py`, `services/`, `repositories/`, `models/` (task-05)
- `alembic/` (task-05, корень репо)
- CORS middleware (defer до web)
- Полные contract tests (task-04)

## Следующий шаг

Task-04 — расширить tests на auth, validation, scenarios A/B.
