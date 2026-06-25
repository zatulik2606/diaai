# Итерация 4 summary

## Ценность

Push `main` → GHCR → автодеплой на VPS без ручного SSH.

## Задачи

| # | Статус |
|---|--------|
| 16 GitHub Secrets | ✅ |
| 17 deploy.yml | ✅ |
| 18 E2E | → после push |

## Pipeline

`docker-publish.yml` → `deploy.yml` → `/opt/diaai` → `make stack-up-registry`

## Secrets

`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY` — см. [github-secrets.md](../../../../devops/deploy/github-secrets.md)
