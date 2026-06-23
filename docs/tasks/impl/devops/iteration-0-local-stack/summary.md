# Итерация 0 — summary

**Статус:** ✅ Done · **Задачи:** 01–06 · **Дата закрытия:** 2026-06-23

## Сделано

| Task | Результат |
|------|-----------|
| 01 | `devops/` layout, README, `.env.compose.example`, `ci/` stub |
| 02 | Dockerfile backend/bot/web; root + `web/.dockerignore` |
| 03 | Корневой `docker-compose.yml` — postgres, backend, web, bot (profile) |
| 04 | `make stack-*`, `stack-init`, `stack-logs-tail`; `db-up` → postgres only |
| 05 | docker-expert audit (2 раунда) — см. ниже |
| 06 | [docker-compose-local.md](../../../devops/docker-compose-local.md); sync onboarding, architecture, README, plan |

## Артефакты

```
devops/docker/{backend,bot,web}/
docker-compose.yml
.dockerignore, web/.dockerignore
Makefile — stack-* targets
docs/devops/docker-compose-local.md
docs/tasks/impl/devops/iteration-0-local-stack/
```

## Решения и отклонения от первоначального плана

| Тема | План | Факт |
|------|------|------|
| Web base | Node 20 alpine | **Node 24 bookworm-slim** (pnpm 11.6) |
| Web CMD | `pnpm start` | **`node node_modules/next/dist/bin/next start`** |
| Bot/backend runtime | `uv run` | **`.venv/bin/*`** — без пересборки при старте |
| uv image | `latest` | **pin `ghcr.io/astral-sh/uv:0.11`** |
| Web runner | corepack | **без corepack** в runner stage |
| ADR devops layout | опционально | раздел в `devops/README.md` (KISS) |

## docker-expert — ключевые fixes

**Раунд 1:** web CMD, Node 24, `db-up` postgres-only, curl в backend, `uv sync` + `src/`.

**Раунд 2 (2026-06-23):** pin uv 0.11; `.venv/bin` entrypoint; web healthcheck в compose; `stack-logs-tail`.

Deferred: Next standalone, resource limits, bot HEALTHCHECK, image digests.

Полный список: [task-05 summary](tasks/task-05-docker-review/summary.md).

## Verify

| Проверка | Результат |
|----------|-----------|
| `make stack-up && make stack-health` | ✅ |
| `POST /api/auth/login` `@ivan_p` | ✅ `{"ok":true,"role":"diabetic"}` |
| `/dashboard` с cookie | ✅ 200 |
| `make stack-up-bot` | ✅ polling, без `Building diaai` |
| `make db-up` | ✅ только postgres |
| `make test` | ✅ 84 passed |

## Проблемы

| Проблема | Решение |
|----------|---------|
| pnpm/corepack EACCES под `nextjs` | direct `node …/next start` |
| `uv run` rebuild bot at start | `.venv/bin/python` |
| `make db-up` поднимал full stack | `docker compose up -d postgres` |

## Следующий шаг

Итерация 1 — [tasklist-devops.md](../../../tasklist-devops.md) tasks 07–09 (GHCR + GHA).
