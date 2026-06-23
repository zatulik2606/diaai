# Task 03 summary

## Сделано

- Расширен корневой [`docker-compose.yml`](../../../../../../docker-compose.yml): `postgres`, `backend`, `web`, `bot` (profile)
- Env overrides: `DATABASE_URL=@postgres:5432`, `BACKEND_URL=http://backend:8000`
- Healthchecks + `depends_on` chain
- `restart: unless-stopped`

## Verify

- `docker compose config` ✅
- `make stack-up` → backend `/health`, web :3000 ✅
