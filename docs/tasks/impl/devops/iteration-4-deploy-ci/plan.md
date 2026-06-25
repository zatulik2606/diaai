# Итерация 4 — автоматизация деплоя

Опирается на [tasklist-devops.md](../../../tasklist-devops.md) · [iter 3](../iteration-3-server-setup/plan.md)

## Цель

GitHub Actions: deploy на VPS по push в `main` (после green `docker-publish`).

## Задачи

| # | Задача | Статус |
|---|--------|--------|
| 16 | GitHub Secrets + deploy key | ✅ |
| 17 | Workflow `deploy.yml` | ✅ |
| 18 | E2E auto-deploy + docs | ✅ |

## Secrets (GitHub, не в git)

| Secret | Значение |
|--------|----------|
| `DEPLOY_HOST` | `201.51.4.34` |
| `DEPLOY_USER` | `deploy` |
| `DEPLOY_SSH_KEY` | private `diaai-deploy` |

Инструкция: [github-secrets.md](../../../../devops/deploy/github-secrets.md)

## DoD итерации

→ [summary.md](summary.md) ✅ · область DevOps MVP закрыта
