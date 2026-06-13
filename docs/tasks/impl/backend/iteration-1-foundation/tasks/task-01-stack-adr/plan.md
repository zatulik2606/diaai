# Task 01: Стек, ADR, conventions

## Цель

Зафиксировать backend-стек и обновить соглашения проекта.

## Что делаем

1. ADR-002: FastAPI + PostgreSQL + SQLAlchemy/Alembic (KISS-структура `backend/`)
2. Обновить `conventions.mdc` — bot (MVP) + backend (целевой)
3. Актуализировать `vision.md`, `plan.md`, `adr/README.md`

## Затронутые файлы

- `docs/adr/adr-002-backend-stack.md` (новый)
- `.cursor/rules/conventions.mdc`
- `docs/vision.md`
- `docs/plan.md`
- `docs/adr/README.md`

## Архитектура backend (решение)

```
backend/
├── main.py           # FastAPI app
├── config.py         # pydantic-settings, env
├── api/              # routers (v1)
├── services/         # бизнес-логика, LLM
├── repositories/     # доступ к БД
└── models/           # SQLAlchemy models
```

Стек: Python 3.12+, uv, FastAPI, Uvicorn, SQLAlchemy 2, Alembic, ruff, pytest, httpx.

## Skills (рекомендация)

- `.agents/skills/fastapi-templates`
- `.agents/skills/api-design-principles`

## DoD

- ADR-002 принят; conventions и vision согласованы
