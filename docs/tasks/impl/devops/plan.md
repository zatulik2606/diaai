# DevOps — план области

Опирается на [tasklist-devops.md](../../tasklist-devops.md) · [plan.md](../../../plan.md) · [architecture.md](../../../architecture.md)

## Цель области

Production deploy MVP: **локальный stack** (iter 0 ✅) → **GHCR** (iter 1 ✅) → **VPS Timeweb Cloud** (iter 2) → **bootstrap + manual deploy** (iter 3) → **GHA CD** (iter 4).

## Итерации

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Локальный полный стек | 01–06 | ✅ Done | [plan](iteration-0-local-stack/plan.md) · [summary](iteration-0-local-stack/summary.md) |
| 1 | Сборка образов и GHCR | 07–09 | ✅ Done | [plan](iteration-1-registry-ci/plan.md) · [summary](iteration-1-registry-ci/summary.md) |
| 2 | Облачный сервер Timeweb Cloud | 10–12 | ✅ Done | [plan](iteration-2-timeweb-server/plan.md) · [summary](iteration-2-timeweb-server/summary.md) |
| 3 | Настройка сервера и ручной deploy | 13–15 | ✅ Done | [plan](iteration-3-server-setup/plan.md) · [summary](iteration-3-server-setup/summary.md) |
| 4 | Автоматизация деплоя (GHA → VPS) | 16–18 | 📋 Next | [plan](iteration-4-deploy-ci/plan.md) · [summary](iteration-4-deploy-ci/summary.md) |

**Прогресс:** 15 / 18 задач · **iter 0–3 ✅** · **iter 4 📋 Next**

## Правило

**Один корневой** [`docker-compose.yml`](../../../../docker-compose.yml) — orchestration полного стека (build, registry, production VPS). Dockerfile'ы в `devops/docker/*`.

## Iter 0–1 — итог

- `make stack-up` / `make stack-up-registry` — локально
- GHCR: `ghcr.io/zatulik2606/diaai-*` · workflow `docker-publish.yml`
- Guides: [docker-compose-local.md](../../../devops/docker-compose-local.md) · [ghcr-stack.md](../../../devops/ghcr-stack.md)

## Iter 2–4 — план

| Iter | Фокус | Ключевые артефакты |
|------|-------|-------------------|
| 2 | VPS `twc`, SSH admin + deploy | `devops/server/`, [twc-cli.md](../../../devops/twc-cli.md) |
| 3 | bootstrap, manual stack | `bootstrap.sh`, `devops/deploy/README.md` |
| 4 | GHA deploy | `.github/workflows/deploy.yml`, GitHub Secrets (manual) |

**Секреты:** не в git — `.env` на сервере, GitHub Secrets для CD. **`docker login ghcr.io`** — только пользователь.

## Связь с plan.md

Production deploy MVP: iter 2–4 в [tasklist-devops.md](../../tasklist-devops.md). Post-MVP: K8s, managed DB, observability.
