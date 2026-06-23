# DevOps — summary области

**Обновлено:** 2026-06-23

## Статус

| Итерация | Статус | Задачи |
|----------|--------|--------|
| 0 — локальный stack | ✅ Done | 01–06 |
| 1 — GHCR | ✅ Done | 07–09 |

**Прогресс:** 9 / 9 · **prep phase закрыта**

## Iter 0 ✅

Полный stack в одном [`docker-compose.yml`](../../../docker-compose.yml).

| Команда | Назначение |
|---------|------------|
| `make stack-init` | первый запуск (db-reset + stack) |
| `make stack-up` / `stack-health` | build mode |
| `make stack-up-bot` | + Telegram bot |
| `make db-up` | только PostgreSQL (host dev) |

Guide: [docs/devops/docker-compose-local.md](../../../devops/docker-compose-local.md)

## Iter 1 ✅

| Команда | Назначение |
|---------|------------|
| `make stack-up-registry` | stack из GHCR (без build) |
| `make stack-pull-registry` | pull образов из GHCR |
| `make stack-up-registry-bot` | registry + bot |

CI: [`.github/workflows/docker-publish.yml`](../../../.github/workflows/docker-publish.yml) · [devops/ci/README.md](../../../devops/ci/README.md)

Образы: `ghcr.io/zatulik2606/diaai-{backend,bot,web}`

Детали: [iteration-1-registry-ci/summary.md](iteration-1-registry-ci/summary.md)

## Post-MVP

Deploy в облако, CD, secrets management, full CI on PR — вне iter 0–1.
