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

## GlitchTip EU — DSN (observability)

Public ingest keys org **diaai** на [eu.glitchtip.com](https://eu.glitchtip.com). Копия значений: [devops/glitchtip/dsn.env.example](../glitchtip/dsn.env.example).

| Secret | Проект | Значение |
|--------|--------|----------|
| `GLITCHTIP_DSN` | diaai-backend (240) | `https://0751c4291bce484985dbdeb657c1272d@eu.glitchtip.com/240` |
| `GLITCHTIP_WEB_DSN` | diaai-web server (241) | `https://6b6da490a88a431cb2265981efdb5a97@eu.glitchtip.com/241` |
| `NEXT_PUBLIC_GLITCHTIP_DSN` | diaai-web browser (241) | `https://6b6da490a88a431cb2265981efdb5a97@eu.glitchtip.com/241` |

**Где используются**

| Место | Переменные |
|-------|------------|
| VPS runtime | `/opt/diaai/.env` — `GLITCHTIP_DSN`, `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN`, `GLITCHTIP_URL`, `GLITCHTIP_ENVIRONMENT` |
| GitHub Actions | secrets для CI build web (`NEXT_PUBLIC_*` в Docker) и документации команды |

**Не класть в GitHub Secrets** (только VPS `.env`): `GLITCHTIP_DEBUG_TOKEN`, `TELEGRAM_ALARM_*`, `GLITCHTIP_WEBHOOK_SECRET`.

### CLI

```bash
gh secret set GLITCHTIP_DSN --body "https://0751c4291bce484985dbdeb657c1272d@eu.glitchtip.com/240"
gh secret set GLITCHTIP_WEB_DSN --body "https://6b6da490a88a431cb2265981efdb5a97@eu.glitchtip.com/241"
gh secret set NEXT_PUBLIC_GLITCHTIP_DSN --body "https://6b6da490a88a431cb2265981efdb5a97@eu.glitchtip.com/241"
gh secret list | grep GLITCHTIP
```

На VPS после добавления secrets в GitHub — всё равно пропишите те же строки в `/opt/diaai/.env` (deploy не синхронизирует secrets автоматически).

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
