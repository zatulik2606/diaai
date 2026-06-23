# DevOps artifacts (diaai)

Единая база Docker/CI-артефактов monorepo. **Orchestration — только корневой [`docker-compose.yml`](../docker-compose.yml).**

## Структура

```
devops/
├── README.md                 # этот файл
├── docker/
│   ├── backend/              # FastAPI + Alembic + prompts
│   ├── bot/                  # Telegram bot (src/diaai)
│   └── web/                  # Next.js production image
├── compose/
│   └── .env.compose.example  # stack env overrides (справка)
└── ci/
    └── README.md             # GHCR / GHA (iter 1)
```

## Почему не `backend/Dockerfile`?

| Причина | Детали |
|---------|--------|
| Monorepo build context | backend нужны `alembic/`, `prompts/`, `pyproject.toml` в корне |
| Shared Python deps | bot и backend — один `uv.lock` |
| Web isolation | context `web/`, Dockerfile в `devops/docker/web/` |

## Локальные образы (iter 0)

| Образ | Dockerfile | Context |
|-------|------------|---------|
| `diaai-backend:local` | `devops/docker/backend/Dockerfile` | `.` (repo root) |
| `diaai-bot:local` | `devops/docker/bot/Dockerfile` | `.` |
| `diaai-web:local` | `devops/docker/web/Dockerfile` | `web/` |

Сборка вручную:

```bash
docker build -f devops/docker/backend/Dockerfile -t diaai-backend:local .
docker build -f devops/docker/bot/Dockerfile -t diaai-bot:local .
docker build -f devops/docker/web/Dockerfile -t diaai-web:local web/
```

Полный stack: `make stack-up` (см. [docs/devops/docker-compose-local.md](../docs/devops/docker-compose-local.md)).

## GHCR (iter 1 ✅)

| Образ | GHCR |
|-------|------|
| backend | `ghcr.io/zatulik2606/diaai-backend` |
| bot | `ghcr.io/zatulik2606/diaai-bot` |
| web | `ghcr.io/zatulik2606/diaai-web` |

CI: [devops/ci/README.md](ci/README.md) · `make stack-up-registry`

## Compose

- **Один файл:** `docker-compose.yml` в корне
- **Build mode:** `make stack-up` (`COMPOSE_PROFILES=build`)
- **Registry mode:** `make stack-up-registry` (`COMPOSE_PROFILES=registry`)
- **Только PG (dev):** `make db-up` → `docker compose up -d postgres`
- **Bot optional:** `make stack-up-bot` / `make stack-up-registry-bot`

## Связанные docs

- [tasklist-devops.md](../docs/tasks/tasklist-devops.md)
- [docker-compose-local.md](../docs/devops/docker-compose-local.md)
