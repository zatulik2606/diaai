# DevOps — план области

Опирается на [tasklist-devops.md](../../tasklist-devops.md) · [plan.md](../../../plan.md) · [architecture.md](../../../architecture.md)

## Цель области

Подготовка к production deploy: **локальный stack в Docker** (iter 0 ✅) → **образы в GHCR** (iter 1 ✅).

## Итерации

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Локальный полный стек | 01–06 | ✅ Done | [plan](iteration-0-local-stack/plan.md) · [summary](iteration-0-local-stack/summary.md) |
| 1 | Сборка образов и GHCR | 07–09 | ✅ Done | [plan](iteration-1-registry-ci/plan.md) · [summary](iteration-1-registry-ci/summary.md) |

**Прогресс:** 9 / 9 задач

## Правило

**Один корневой** [`docker-compose.yml`](../../../../docker-compose.yml) — orchestration полного стека. Dockerfile'ы в `devops/docker/*`.

## Iter 0 — итог

- `make stack-up` → postgres :5433, backend :8000, web :3000
- Bot: `make stack-up-bot` (profile)
- Guide: [docs/devops/docker-compose-local.md](../../../devops/docker-compose-local.md)
- Host dev без изменений: `make db-reset`, `backend-run`, `make test`

## Iter 1 — итог

- `.github/workflows/docker-publish.yml` → `ghcr.io/zatulik2606/diaai-*`
- `make stack-up-registry` / `stack-pull-registry` — тот же compose
- Guide: § Registry в [docker-compose-local.md](../../../devops/docker-compose-local.md)

## Связь с plan.md

Post-MVP «Production deploy»: iter 0 ✅ stack · iter 1 ✅ registry · deploy/CD — post-MVP.
