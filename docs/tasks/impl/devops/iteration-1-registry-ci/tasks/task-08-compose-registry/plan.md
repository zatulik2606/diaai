# Task 08: Compose registry mode

## Цель

Запуск stack из GHCR через profiles/env в **корневом** `docker-compose.yml`.

## Файлы

- `docker-compose.yml` — profiles `build` / `registry`
- `Makefile` — `stack-up-registry`, `stack-pull-registry`, bot variants
- `docs/devops/docker-compose-local.md` § Registry

## Решения

- `COMPOSE_PROFILES=build` — default `make stack-up`
- `COMPOSE_PROFILES=registry` + `DIAAI_*_IMAGE` — pull/up без build
- Bot: profile `bot`; registry+bot через `COMPOSE_PROFILES=registry,bot`
- `--pull missing` — локальные теги без GHCR login (smoke)

## DoD

`make stack-up-registry` поднимает stack без `docker build`.
