# Итерация 1 — summary

## Сделано

- GHA workflow → GHCR (3 образа, matrix, cache, tags)
- Registry mode в корневом compose (profiles + `DIAAI_*_IMAGE`)
- Makefile: `stack-up-registry`, `stack-pull-registry`, bot variants
- Docs: `devops/ci/README.md`, § Registry в docker-compose-local

## Verify

| Проверка | Результат |
|----------|-----------|
| `make stack-up && make stack-health` | ✅ |
| `make stack-up-registry && make stack-health` | ✅ (local tags) |
| `make test` | 84 passed |

## Решения

- `--pull missing` в `stack-up-registry` — smoke без GHCR login
- Явный pull: `make stack-pull-registry`
- GHCR owner: `zatulik2606` (`GHCR_OWNER` в Makefile)

## CI

Workflow green на GitHub — после merge в `main`. Локально не прогонялся.

## Tasks

- [07](tasks/task-07-gha-ghcr/summary.md)
- [08](tasks/task-08-compose-registry/summary.md)
- [09](tasks/task-09-registry-verify/summary.md)
