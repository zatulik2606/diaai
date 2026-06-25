# DevOps — итог области (iter 0–4)

Опирается на [tasklist-devops.md](../../tasklist-devops.md) · [plan.md](plan.md)

## Прогресс

**18 / 18 задач ✅** — область DevOps MVP закрыта.

## Итерации

| Iter | Результат |
|------|-----------|
| 0 | Локальный `docker-compose` stack, `make stack-*` |
| 1 | GHCR `ghcr.io/zatulik2606/diaai-*`, `docker-publish.yml` |
| 2 | VPS Timeweb: SSH admin + deploy, inventory |
| 3 | Bootstrap, `/opt/diaai`, ручной registry deploy, smoke |
| 4 | `deploy.yml`, GitHub Secrets, E2E CD |

## Production

| | |
|--|--|
| IPv4 | `201.51.4.34` |
| OS | Ubuntu 24.04 |
| Web | http://201.51.4.34:3000 |
| API | http://201.51.4.34:8000/health |
| CD | push `main` → publish → deploy |

**SSH:** [server/README.md § Проверка SSH](../../../devops/server/README.md#проверка-ssh)

## E2E CD

Успешный run: [Deploy #28166334358](https://github.com/zatulik2606/diaai/actions/runs/28166334358) (commit `3e6e0da`).

Fixes по пути: compose `ports: !override`; wait web + `set -e` в deploy script.

## Отклонения

| Тема | Решение |
|------|---------|
| Регион VPS | `ru-3` вместо `ru-1` (`no_free_node`) |
| Preset | `4801` (эквивалент 2453 в ru-3) |
| Seed на VPS | `uv` на хосте, не в bootstrap |

## Документация (карта)

| Документ | Назначение |
|----------|------------|
| [inventory.example.md](../../../devops/server/inventory.example.md) | IP, OS, server id |
| [twc-cli.md](../../../devops/twc-cli.md) | twc, SSH keys |
| [ghcr-stack.md](../../../devops/ghcr-stack.md) | registry stack |
| [deploy/README.md](../../../devops/deploy/README.md) | layout + CD |
| [github-secrets.md](../../../devops/deploy/github-secrets.md) | `DEPLOY_*` |

## Post-MVP

HTTPS reverse proxy, K8s, managed PostgreSQL, CI lint/test on PR — см. tasklist.
