# Task 04: API-тесты сценариев бота

Опирается на [task-03-scaffold/plan.md](../task-03-scaffold/plan.md) · [openapi.yaml](../../../../../../api/openapi.yaml)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — AsyncClient, conftest fixtures, pytest-asyncio

## Цель

Contract-тесты API для сценариев A и B: auth, validation, stub 501. Happy-path 200/201 — task-05.

## Стратегия stub vs impl

| Тип | task-04 | task-05 |
|-----|---------|---------|
| 401/422/400 | финальные коды | без изменений |
| Happy-path | 501 NOT_IMPLEMENTED | 200/201 + body |
| 403/404 | не пишем | с БД |

## Матрица тестов

### conftest.py

- `auth_headers`, `invalid_auth_headers`
- `assistant_text_payload`, `assistant_photo_payload`, `food_event_payload`, `insulin_event_payload`

### test_auth.py

- без Bearer → 401
- неверный Bearer → 401 (assistant, food)
- GET /health без auth → 200

### test_validation.py

- assistant: missing telegram_id → 422
- food: missing fields, negative xe → 422
- insulin: dose=0 → 422
- GET food: missing telegram_id → 422

### test_assistant.py

- text/photo valid body → 501
- empty content → 400
- X-Request-Id echo

### test_events.py

- POST food/insulin → 501
- GET food list → 501

## Проверка

```bash
make backend-test    # 17 passed
make backend-lint
uv run --with pytest-cov pytest backend/tests --cov=backend --cov-report=term-missing
```

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | `make backend-test` зелёный; 17 тестов |
| Пользователь | список тестов понятен до impl |

## Следующий шаг

Task-05 — impl + обновить happy-path assertions (501 → 200/201).
