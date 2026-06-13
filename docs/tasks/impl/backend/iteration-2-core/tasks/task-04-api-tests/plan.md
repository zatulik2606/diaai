# Task 04: API-тесты сценариев бота

Опирается на [task-03-scaffold/plan.md](../task-03-scaffold/plan.md) · [openapi.yaml](../../../../../../api/openapi.yaml)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — AsyncClient, conftest fixtures, pytest-asyncio

## Цель

Contract-тесты API для сценариев A и B на каркасе task-03: auth, validation, routes.

## Состав работ

### 1. Расширить `backend/tests/conftest.py`

```python
@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers(settings):
    return {"Authorization": f"Bearer {settings.backend_service_token}"}
```

- fixture `app` / override settings для тестов
- опционально: override `get_db` (sqlite memory) — задел под task-05

### 2. Тесты auth и validation

- `test_health.py` — GET `/health` 200, без auth
- без Bearer → 401 на `/api/v1/assistant/messages`
- невалидное тело → 422

### 3. Тесты сценария A

- POST assistant/messages: текст (mock LLM или expect 501 до task-05)
- POST с `image_base64` — schema validation
- 400: пустой text и нет image

### 4. Тесты сценария B

- POST `/events/food`, `/events/insulin` — schema, auth
- 403/404 cases по [event-record.md](../../../../../../api/scenarios/event-record.md)

### 5. Makefile

- `make backend-test` → `pytest backend/tests`

## Затронутые файлы

- `backend/tests/conftest.py`
- `backend/tests/test_health.py`, `test_auth.py`, `test_assistant.py`, `test_events.py`
- `Makefile`

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | тесты падают на stub 501 до task-05; проходят после impl; auth/422 покрыты |
| Пользователь | `make backend-test` зелёный после task-05 |

## Следующий шаг

Task-05 — реализация endpoint'ов и PostgreSQL.
