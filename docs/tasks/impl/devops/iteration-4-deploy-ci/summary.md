# Итерация 4 summary

## Ценность

Push `main` → GHCR → автодеплой на VPS (SSH, без ручного вмешательства).

## Задачи

| # | Статус |
|---|--------|
| 16 GitHub Secrets | ✅ |
| 17 deploy.yml | ✅ |
| 18 E2E | ✅ |

## Pipeline

```
push main → Docker Publish → Deploy (workflow_run)
  → SSH deploy@201.51.4.34
  → git fetch + reset --hard origin/main + clean -fd + make stack-*-registry + health
```

## E2E

| Run | Commit | Result |
|-----|--------|--------|
| [28166137641](https://github.com/zatulik2606/diaai/actions/runs/28166137641) | `120710e` | FAIL — web cold start |
| [28166245576](https://github.com/zatulik2606/diaai/actions/runs/28166245576) | `d96ee48` | FAIL — `set -e` + curl |
| [28166334358](https://github.com/zatulik2606/diaai/actions/runs/28166334358) | `3e6e0da` | ✅ success |

## Артефакты

- `.github/workflows/deploy.yml`
- [devops/deploy/github-secrets.md](../../../devops/deploy/github-secrets.md)

## Область DevOps MVP

**18/18 задач ✅** — local stack → GHCR → VPS → CD.
