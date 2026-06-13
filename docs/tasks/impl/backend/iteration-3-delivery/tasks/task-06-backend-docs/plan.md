# Task 06: Документирование backend

Опирается на [iteration-3-delivery/plan.md](../../plan.md) · [ADR-002](../../../../../../adr/adr-002-backend-stack.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — Health and Monitoring, Documentation with OpenAPI

## Цель

Онбординг разработчика: README, docker-compose, единый Makefile, синхронизация OpenAPI.

## Состав работ

### 1. README backend

Файл: `backend/README.md` или секция в корневом [README.md](../../../../../../README.md)

- prerequisites: Python 3.12+, uv, Docker (optional)
- команды: `make backend-install`, `backend-run`, `backend-test`, `backend-migrate`, `backend-lint`, `backend-format`
- env из `.env.example`: `BACKEND_SERVICE_TOKEN`, `BACKEND_HOST`, `BACKEND_PORT`, `DATABASE_URL`, `OPENROUTER_*`

### 2. docker-compose.yml (KISS)

```yaml
# postgres + backend (uvicorn)
# healthcheck postgres; backend depends_on
# volumes для PG; порты 5432, 8000
```

### 3. OpenAPI sync

- FastAPI `/docs`, `/redoc` — title `diaai Backend API`, version `1.0.0`
- сверка с [openapi.yaml](../../../../../../api/openapi.yaml) и [api-contracts.md](../../../../../../tech/api-contracts.md)
- при расхождении: обновить yaml или задокументировать auto-gen как source of truth

### 4. Makefile

Дополнить если отсутствует:

- `backend-migrate` — `alembic upgrade head`
- `backend-test`, `backend-lint`, `backend-format`

### 5. Документы проекта

- [README.md](../../../../../../README.md) — статус backend, ссылка на backend README
- [plan.md](../../../../../../plan.md) — прогресс итераций 2–3

## Затронутые файлы

- `backend/README.md` (или корневой README)
- `docker-compose.yml`
- `Makefile`, `.env.example`
- `docs/plan.md`, `README.md`

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | `docker compose up` → `GET /health` 200; README воспроизводим |
| Пользователь | поднять stack только по README + `.env.example`; OpenAPI совпадает с реализацией |

## Вне scope

- Production deploy, CI/CD

## Следующий шаг

Task-07 — рефакторинг бота на backend API.
