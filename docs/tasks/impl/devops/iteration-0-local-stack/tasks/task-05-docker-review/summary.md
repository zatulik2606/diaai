# Task 05 summary — docker-expert audit

## Review scope

`devops/docker/*`, корневой `docker-compose.yml`, `.dockerignore`, Makefile stack/db targets.

## Findings — fixed

| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | Critical | Web `pnpm start` as `nextjs` → corepack EACCES on `$HOME/.cache` | CMD: `node node_modules/next/dist/bin/next start` |
| 2 | Critical | `make db-up` поднимал full stack после расширения compose | `docker compose up -d postgres` |
| 3 | High | `uv sync` без `src/`/`README.md` — build fail | Copy sources before sync |
| 4 | High | pnpm 11.6 + Node 20 → `ERR_UNKNOWN_BUILTIN_MODULE` | Web base: Node 24 bookworm-slim |
| 5 | Medium | Backend healthcheck без curl in slim | Install curl in backend image |

## Findings — deferred (post-MVP)

| # | Finding | Reason |
|---|---------|--------|
| 1 | Next.js `output: 'standalone'` | smaller image; current copy node_modules works |
| 2 | CPU/memory limits in compose | local dev; add in prod iter |
| 3 | read-only rootfs | complicates migrate entrypoint |
| 4 | distroless Python images | curl/alembic shell needs |

## Pass checklist

- [x] Build context + `.dockerignore`
- [x] Secrets via `.env` / env_file (not in image)
- [x] Non-root USER (backend `app`, web `nextjs`)
- [x] HEALTHCHECK (backend Dockerfile + compose; web Dockerfile)
- [x] Service DNS networking
- [x] Migrate in entrypoint; seed manual
- [x] Single root compose

## Verify

`make stack-up && make stack-health` ✅ · login API `@ivan_p` ✅

## Review 2026-06-23 (docker-expert)

| # | Severity | Finding | Action |
|---|----------|---------|--------|
| 1 | Critical | `uv:latest` — не воспроизводимо | **Fixed:** pin `ghcr.io/astral-sh/uv:0.11` |
| 2 | Critical | Bot `uv run` пересобирал пакет при старте | **Fixed:** `/app/.venv/bin/python` |
| 3 | High | Backend entrypoint через `uv run` — лишний overhead | **Fixed:** `.venv/bin/alembic` + `uvicorn` |
| 4 | Medium | Web runner: corepack без использования | **Fixed:** убран из runner stage |
| 5 | Medium | Web healthcheck только в Dockerfile | **Fixed:** явный healthcheck в compose |
| 6 | Low | `stack-logs -f` блокирует скрипты | **Fixed:** `make stack-logs-tail` |

Deferred: standalone Next.js, resource limits, bot HEALTHCHECK, pin image digests.
