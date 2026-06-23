# Task 01: Структура devops/

## Цель

Layout DevOps-артефактов до Dockerfile'ов.

## Артефакты

- `devops/README.md`
- `devops/compose/.env.compose.example`
- `devops/docker/{backend,bot,web}/`
- `devops/ci/README.md` (заглушка iter 1)

## DoD

README связывает docker/* → корневой compose; второй compose-файл не создаётся.
