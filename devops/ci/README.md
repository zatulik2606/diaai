# CI / GHCR

Сборка и публикация Docker-образов diaai в GitHub Container Registry.

## Workflow

[`.github/workflows/docker-publish.yml`](../../.github/workflows/docker-publish.yml)

| Trigger | Действие |
|---------|----------|
| push → `main` | build + push 3 образа |
| push tag `v*` | semver tags |
| `workflow_dispatch` | ручной запуск |

## Образы

| Сервис | GHCR image |
|--------|------------|
| backend | `ghcr.io/<owner>/diaai-backend` |
| bot | `ghcr.io/<owner>/diaai-bot` |
| web | `ghcr.io/<owner>/diaai-web` |

Owner по умолчанию: **`zatulik2606`** (см. `git remote`). Переопределение: `GHCR_OWNER` в Makefile.

## Tags

| Tag | Когда |
|-----|-------|
| `main` | push в default branch |
| `sha-<commit>` | каждый push |
| `<branch>` | имя ветки (sanitized) |
| semver | git tag `v1.2.3` |

## Permissions

Repo → Settings → Actions → General → **Read and write permissions** для `GITHUB_TOKEN` (packages: write).

Первый push: package visibility **public** или `docker login ghcr.io` для private pull.

## Локальный pull + stack (registry mode)

```bash
# login (private packages)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# из корня repo
make stack-up-registry              # IMAGE_TAG=main по умолчанию
make stack-up-registry IMAGE_TAG=sha-abc1234

# явный pull из GHCR (после login)
make stack-pull-registry

# с bot
make stack-up-registry-bot
```

Без GHCR (smoke с локальными тегами):

```bash
docker tag diaai-backend:local ghcr.io/zatulik2606/diaai-backend:main
docker tag diaai-web:local ghcr.io/zatulik2606/diaai-web:main
make stack-up-registry
```

## Compose profiles

| Profile | Режим |
|---------|-------|
| `build` | `make stack-up` — local build |
| `registry` | `make stack-up-registry` — pull GHCR, `--no-build` |
| `bot` | + Telegram bot (`stack-up-bot`, `stack-up-registry-bot`) |

Один файл: [`docker-compose.yml`](../../docker-compose.yml).

Guide: [docs/devops/docker-compose-local.md](../../docs/devops/docker-compose-local.md)
