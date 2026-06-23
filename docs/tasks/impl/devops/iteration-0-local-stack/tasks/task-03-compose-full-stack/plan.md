# Task 03: Корневой docker-compose.yml

## Цель

Расширить postgres-only compose сервисами backend, web, bot (profile).

## Сервисы

| Service | Port | depends_on |
|---------|------|------------|
| postgres | 5433 | — |
| backend | 8000 | postgres healthy |
| web | 3000 | backend healthy |
| bot | — | backend (profile bot) |

## Env overrides

- backend: `DATABASE_URL=@postgres:5432`, `BACKEND_HOST=0.0.0.0`
- web/bot: `BACKEND_URL=http://backend:8000`

## DoD

`docker compose config`; stack postgres+backend+web up.
