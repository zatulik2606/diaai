# Итерация 4 — автоматизация деплоя

Опирается на [tasklist-devops.md](../../../tasklist-devops.md) · [iter 3](../iteration-3-server-setup/plan.md)

## Цель

GitHub Actions: deploy на VPS по push в `main` (после green `docker-publish`).

## Задачи

| # | Задача | Статус |
|---|--------|--------|
| 16 | GitHub Secrets + deploy SSH key (manual guide) | 📋 |
| 17 | Workflow `.github/workflows/deploy.yml` | 📋 |
| 18 | E2E auto-deploy + docs | 📋 |

## Secrets (GitHub, не в git)

| Secret | Назначение |
|--------|------------|
| `DEPLOY_HOST` | публичный IP VPS |
| `DEPLOY_USER` | пользователь SSH (deploy) |
| `DEPLOY_SSH_KEY` | private key **deploy** (не admin) |
| `GHCR_PULL_TOKEN` | optional; pull private packages (если не public) |

## Критерии

- [ ] push в `main` → deploy workflow → stack обновлён на сервере
- [ ] smoke после auto-deploy (health + web)
- [ ] skill `github-actions-templates` для workflow

## DoD итерации

→ tasks 16–18 summary ✅ · область deploy MVP закрыта
