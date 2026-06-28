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
| IPv4 | `201.51.4.34` (Timeweb Cloud, preset 4801: 2 vCPU / 4 GB / 50 GB) |
| OS | Ubuntu 24.04 |
| Web | http://201.51.4.34:3000 |
| API | http://201.51.4.34:8000/health |
| Доступ | по IP, **без custom domain** (`diaai.ai` отложен) |
| CD | push `main` → publish → deploy (`git reset --hard origin/main`) |
| Monitoring | **вариант 1:** app + Grafana/Prometheus/Loki/Kuma/Dozzle на том же VPS; GlitchTip — hosted EU + bridge `:8080` |
| RAM (snapshot 2026-06-28) | app ~680 MB · monitoring ~450 MB · host ~1.4/3.8 GB + **swap 2 GB** (`bootstrap.sh`) · disk ~18/48 GB |

**SSH:** [server/README.md § Проверка SSH](../../../devops/server/README.md#проверка-ssh)

## Чеклист приёмки ✅

- [x] VPS минимальной конфигурации + публичный IP (`8460897`, `201.51.4.34`)
- [x] SSH-ключи admin/deploy, инструкция и вход
- [x] Docker/Compose + `bootstrap.sh`
- [x] GHCR stack, health + web снаружи
- [x] GitHub Secrets `DEPLOY_*`
- [x] CD workflow green, контейнеры обновляются

## E2E CD

Последний успешный run: [Deploy #28167868567](https://github.com/zatulik2606/diaai/actions/runs/28167868567) (commit `18167f2`).

Fixes по пути: compose `ports: !override`; wait web + `set -e` в deploy script; CD `git fetch + reset --hard origin/main + clean -fd` (локальные правки на VPS блокировали `git pull --ff-only`).

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

HTTPS reverse proxy / custom domain, K8s, managed PostgreSQL, CI lint/test on PR — см. tasklist.
