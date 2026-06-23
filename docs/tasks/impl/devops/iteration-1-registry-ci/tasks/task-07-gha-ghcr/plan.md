# Task 07: GitHub Actions → GHCR

## Цель

Workflow сборки и push трёх образов в GHCR на push `main`, tags `v*`, `workflow_dispatch`.

## Файлы

- `.github/workflows/docker-publish.yml`
- `devops/ci/README.md`

## Архитектура

- Matrix: backend, bot (context `.`), web (context `web`)
- Login: `GITHUB_TOKEN`, `packages: write`
- Tags: `main`, `sha-*`, branch, semver
- Cache: GHA (`type=gha`, scope per service)
- Images: `ghcr.io/<owner>/diaai-{backend,bot,web}`

## DoD

Workflow в репозитории; README с naming, pull, permissions.
