# Task 02: Dockerfile + .dockerignore

## Цель

Образы backend, bot, web — reproducible build.

## Backend

- `python:3.12-slim`, uv, `uv sync --frozen --no-dev`
- Copy: `backend/`, `alembic/`, `prompts/`, `pyproject.toml`, `uv.lock`
- Entrypoint: migrate + uvicorn

## Bot

- Shared uv pattern; copy `src/`; `python -m diaai.main`

## Web

- Multi-stage node:20-alpine, pnpm 11.6, `next build` + `next start`
- Context: `web/`

## DoD

`docker build` для трёх образов без ошибок.
