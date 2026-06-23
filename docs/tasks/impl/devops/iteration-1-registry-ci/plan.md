# Итерация 1 — сборка образов и GHCR

Опирается на [tasklist-devops.md](../../../tasklist-devops.md) · [iter 0 plan](../iteration-0-local-stack/plan.md)

## Цель

GitHub Actions публикует образы в GHCR; локальный stack из registry через **тот же** `docker-compose.yml` (profiles `build` / `registry`).

## Задачи

| # | Задача | Статус |
|---|--------|--------|
| 07 | GHA → GHCR | ✅ |
| 08 | Compose registry mode | ✅ |
| 09 | Verify + docs | ✅ |

## Образы

`ghcr.io/zatulik2606/diaai-{backend,bot,web}` · tags: `main`, `sha-*`, branch, semver

## Критерии

- [x] workflow `.github/workflows/docker-publish.yml`
- [x] `make stack-up-registry` без local build
- [x] `make stack-health` в registry mode
- [x] summary iter 1 ✅
