# Task 07 summary

## Сделано

- [`.github/workflows/docker-publish.yml`](../../../../../../.github/workflows/docker-publish.yml)
  - triggers: push `main`, tags `v*`, `workflow_dispatch`
  - matrix backend/bot/web; build-push-action v6 + metadata-action v5
  - GHCR login via `GITHUB_TOKEN`; GHA cache per service
  - web: Dockerfile вне context — `github.workspace/devops/docker/web/Dockerfile`
- [`devops/ci/README.md`](../../../../../../devops/ci/README.md) — naming, tags, pull, permissions

## Skill

[`.agents/skills/github-actions-templates/SKILL.md`](../../../../../../.agents/skills/github-actions-templates/SKILL.md) — Pattern 2 (Build and Push) + matrix для backend/bot/web.

## Verify

- Workflow синтаксически валиден ✅
- CI green на GitHub — **после merge в main** (локально не прогонялся)

## Отложено

- `act` dry-run — optional, не требовалось для DoD
