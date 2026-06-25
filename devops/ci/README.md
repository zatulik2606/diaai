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

Образы: **linux/amd64** + **linux/arm64** (Apple Silicon).

## Login

Полная инструкция: **[ghcr-login.md](ghcr-login.md)**.

**PAT (classic):** scope `read:packages` (pull), `write:packages` (push с машины). Username: GitHub login (`zatulik2606`).

```bash
# Способ 1 — -u + -p (работает; Docker warn про insecure CLI)
docker login ghcr.io -u "$GITHUB_USERNAME" -p "$GITHUB_PAT"

# Способ 2 — предпочтительно
echo "$GITHUB_PAT" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
```

Packages public — login часто не нужен. См. [ghcr-login.md § Быстрая проверка](ghcr-login.md#быстрая-проверка-pull).

## Локальный pull + stack (registry mode)

```bash
# 1. проверка pull (без login, если public)
docker pull ghcr.io/zatulik2606/diaai-backend:main

# 2. при denied — login (см. ghcr-login.md), затем pull снова

# 3. stack
make stack-up-registry              # IMAGE_TAG=main по умолчанию
make stack-up-registry IMAGE_TAG=sha-abc1234

make stack-pull-registry
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

Guide: [docs/devops/docker-compose-local.md](../../docs/devops/docker-compose-local.md) · **GHCR:** [docs/devops/ghcr-stack.md](../../docs/devops/ghcr-stack.md) · **login:** [ghcr-login.md](ghcr-login.md)
