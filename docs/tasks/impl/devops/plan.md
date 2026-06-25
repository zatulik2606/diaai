# DevOps — план области

Опирается на [tasklist-devops.md](../../tasklist-devops.md) · [plan.md](../../../plan.md) · [architecture.md](../../../architecture.md)

## Цель области

Production deploy MVP: локальный stack → GHCR → VPS Timeweb Cloud → bootstrap → GHA CD.

**Статус:** ✅ **18 / 18 задач** · область DevOps MVP закрыта.

## Итерации

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Локальный полный стек | 01–06 | ✅ Done | [plan](iteration-0-local-stack/plan.md) · [summary](iteration-0-local-stack/summary.md) |
| 1 | Сборка образов и GHCR | 07–09 | ✅ Done | [plan](iteration-1-registry-ci/plan.md) · [summary](iteration-1-registry-ci/summary.md) |
| 2 | Облачный сервер Timeweb Cloud | 10–12 | ✅ Done | [plan](iteration-2-timeweb-server/plan.md) · [summary](iteration-2-timeweb-server/summary.md) |
| 3 | Настройка сервера и ручной deploy | 13–15 | ✅ Done | [plan](iteration-3-server-setup/plan.md) · [summary](iteration-3-server-setup/summary.md) |
| 4 | Автоматизация деплоя (GHA → VPS) | 16–18 | ✅ Done | [plan](iteration-4-deploy-ci/plan.md) · [summary](iteration-4-deploy-ci/summary.md) |

## Production VPS

| Поле | Значение |
|------|----------|
| Server ID | `8460897` |
| Name | `diaai-prod` |
| IPv4 | `201.51.4.34` |
| OS | Ubuntu 24.04 |
| Region / preset | `ru-3` / `4801` (≈2453) |
| Path | `/opt/diaai` (user `deploy`) |

**SSH (ручная проверка):**

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
```

Документация: [inventory.example.md](../../../devops/server/inventory.example.md) · [server/README.md § Проверка SSH](../../../devops/server/README.md#проверка-ssh) · [twc-cli.md](../../../devops/twc-cli.md)

## Правило

**Один корневой** [`docker-compose.yml`](../../../../docker-compose.yml) — build, registry, production VPS.

## Pipeline (iter 1 + 4)

```
push main → docker-publish.yml → GHCR
         → deploy.yml (workflow_run) → SSH deploy@VPS → make stack-*-registry
```

Workflows: [docker-publish.yml](../../../../.github/workflows/docker-publish.yml) · [deploy.yml](../../../../.github/workflows/deploy.yml)

## Ключевые артефакты

| Iter | Артефакты |
|------|-----------|
| 0–1 | `devops/docker/*`, `make stack-*`, GHCR |
| 2 | `devops/server/`, `twc-cli.md` |
| 3 | `bootstrap.sh`, `devops/deploy/`, `compose.server.override.yml` |
| 4 | `deploy.yml`, [github-secrets.md](../../../devops/deploy/github-secrets.md) |

## Секреты

Не в git: `.env` на сервере; GitHub Secrets `DEPLOY_*`. `docker login ghcr.io` — только пользователь.

## Post-MVP

K8s, managed DB, HTTPS, full CI on PR — [tasklist § Post-MVP](../../tasklist-devops.md#post-mvp-не-в-этом-tasklist)
