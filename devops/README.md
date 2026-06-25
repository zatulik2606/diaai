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
├── ci/
│   ├── README.md             # GHCR / GHA (iter 1)
│   └── ghcr-login.md         # docker login ghcr.io
├── server/                   # VPS iter 2–3
│   ├── bootstrap.sh
│   ├── inventory.example.md
│   └── README.md
├── deploy/                   # VPS layout iter 3–4
│   ├── README.md
│   └── compose.server.override.yml
├── glitchtip/                # error tracking (основной, Timeweb)
│   ├── timeweb-deploy.md
│   ├── compose.yml
│   └── bootstrap-timeweb.sh
├── monitoring/               # Dozzle + GlitchTip→Telegram bridge (ADR-005)
│   ├── README.md
│   ├── uptimerobot.md
│   └── compose.yml
└── sentry/                   # альтернатива: full self-hosted Sentry
    ├── timeweb-deploy.md
    └── scripts/create-projects.sh
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

Guide GHCR: [docs/devops/ghcr-stack.md](../docs/devops/ghcr-stack.md) · login: [ci/ghcr-login.md](ci/ghcr-login.md)

## Error tracking (GlitchTip)

**Hosted EU (без VPS):** [glitchtip/hosted.md](glitchtip/hosted.md) · [eu.glitchtip.com](https://eu.glitchtip.com)

**Self-hosted Timeweb:** [glitchtip/timeweb-deploy.md](glitchtip/timeweb-deploy.md)

Альтернатива (16 GB+ RAM): [sentry/timeweb-deploy.md](sentry/timeweb-deploy.md)

## Monitoring (ADR-005)

| Компонент | Назначение |
|-----------|------------|
| [monitoring/README.md](monitoring/README.md) | Dozzle, GlitchTip→Telegram bridge |
| [monitoring/uptimerobot.md](monitoring/uptimerobot.md) | внешний uptime (SaaS) |

```bash
make monitoring-up    # Dozzle :8888 + bridge :8080
make monitoring-ps
```

ADR: [docs/adr/adr-005-observability.md](../docs/adr/adr-005-observability.md)

## Timeweb Cloud (iter 2 ✅)

Production VPS: `201.51.4.34` · [server/README.md](server/README.md) · [deploy/README.md](deploy/README.md).

## Compose

- **Один файл:** `docker-compose.yml` в корне
- **Build mode:** `make stack-up` (`COMPOSE_PROFILES=build`)
- **Registry mode:** `make stack-up-registry` (`COMPOSE_PROFILES=registry`)
- **Только PG (dev):** `make db-up` → `docker compose up -d postgres`
- **Bot optional:** `make stack-up-bot` / `make stack-up-registry-bot`

## Связанные docs

- [tasklist-devops.md](../docs/tasks/tasklist-devops.md)
- [docker-compose-local.md](../docs/devops/docker-compose-local.md)
- [twc-cli.md](../docs/devops/twc-cli.md) — Timeweb Cloud CLI (iter 2)
- [server/README.md](server/README.md) — VPS bootstrap (iter 2–3)
