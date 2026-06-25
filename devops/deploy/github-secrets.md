# GitHub Secrets для CD (iter 4)

**Выполняет пользователь:** Settings → Secrets and variables → Actions → Repository secrets.

Связь: [deploy/README.md](README.md) · workflow [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml).

---

## Обязательные secrets

| Secret | Значение | Пример production |
|--------|----------|-------------------|
| `DEPLOY_HOST` | публичный IPv4 VPS | `201.51.4.34` |
| `DEPLOY_USER` | SSH user для deploy | `deploy` |
| `DEPLOY_SSH_KEY` | **private** key `diaai-deploy` (PEM) | содержимое `~/.ssh/diaai-deploy` |

**Не коммитить** private keys и `.env`.

---

## Как добавить (UI)

1. GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** для каждой строки таблицы
3. `DEPLOY_SSH_KEY`: скопировать **весь** файл `~/.ssh/diaai-deploy` (включая `-----BEGIN/END-----`)

---

## CLI (альтернатива)

```bash
gh secret set DEPLOY_HOST --body "201.51.4.34"
gh secret set DEPLOY_USER --body "deploy"
gh secret set DEPLOY_SSH_KEY < ~/.ssh/diaai-deploy
gh secret list
```

---

## Опционально

| Secret | Когда |
|--------|-------|
| `GHCR_PULL_TOKEN` | packages private; PAT `read:packages` для `docker login` на сервере |

Login на VPS (выполняет пользователь):

```bash
docker login ghcr.io -u GITHUB_USERNAME -p GITHUB_PAT
# или: echo "$GITHUB_PAT" | docker login ghcr.io -u GITHUB_USERNAME --password-stdin
```

Подробнее: [devops/ci/ghcr-login.md](../ci/ghcr-login.md).

---

## Проверка SSH (локально)

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'cd /opt/diaai && docker compose version'
```

Подробнее: [server/README.md § Проверка SSH](../server/README.md#проверка-ssh).

Public key `diaai-deploy` уже на сервере (bootstrap task 13).

---

## Проверка secrets (после добавления)

```bash
gh workflow run deploy.yml   # manual dispatch
gh run list --workflow=deploy.yml
```

Или push в `main` → **Docker Publish** green → **Deploy** автоматически.

---

## Troubleshoot

| Симптом | Решение |
|---------|---------|
| `ssh: handshake failed` | проверить `DEPLOY_SSH_KEY` (полный private key, без лишних пробелов) |
| `permission denied (publickey)` | public key в `/home/deploy/.ssh/authorized_keys` |
| deploy до publish | workflow ждёт `workflow_run` Docker Publish success |
