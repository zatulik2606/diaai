# GHCR login (docker)

Когда нужен login к `ghcr.io`, как создать PAT и две рабочие команды.

Связь: [README.md](README.md) · [ghcr-stack.md](../../docs/devops/ghcr-stack.md) · [deploy/README.md](../deploy/README.md)

---

## Быстрая проверка (pull)

Сначала попробуйте **без login** — packages diaai **public**:

```bash
docker pull ghcr.io/zatulik2606/diaai-backend:main
```

| Результат | Действие |
|-----------|----------|
| `Pull complete` / `Image is up to date` | login **не нужен** → `make stack-pull-registry` |
| `denied` / `unauthorized` | login ниже → снова `docker pull ...` |

После успешного login — **та же команда**:

```bash
docker pull ghcr.io/zatulik2606/diaai-backend:main
```

Другие образы: `diaai-web:main`, `diaai-bot:main` (тот же owner/tag).

---

## PAT (Personal Access Token)

1. GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. **Generate new token (classic)**
3. Scopes:
   - **`read:packages`** — pull образов
   - **`write:packages`** — только если push с машины (CI использует `GITHUB_TOKEN`)

**Username:** GitHub **username** — `zatulik2606` (литерал в `-u`, **не** `$zatulik2606`).

PAT **не коммитить** — только env / prompt / GitHub Secret.

---

## Когда login нужен

| Ситуация | Login |
|----------|-------|
| `docker pull ghcr.io/zatulik2606/diaai-backend:main` OK | **не нужен** |
| `denied` / `unauthorized` при pull | **нужен** PAT |
| Push образов с локальной машины | **нужен** + `write:packages` |

## Способ 1: `-u` + `-p` (работает)

```bash
export GITHUB_USERNAME=zatulik2606
read -s GITHUB_PAT   # вставить PAT, Enter

docker login ghcr.io -u "$GITHUB_USERNAME" -p "$GITHUB_PAT"

unset GITHUB_PAT
```

Docker выведет предупреждение `Using --password via the CLI is insecure` — это нормально; команда **валидна**.

Одной строкой (не рекомендуется — PAT в history):

```bash
docker login ghcr.io -u GITHUB_USERNAME -p GITHUB_PAT
```

---

## Способ 2: `--password-stdin` (предпочтительно)

Токен не попадает в argv / `ps`:

```bash
export GITHUB_USERNAME=zatulik2606
read -s GITHUB_PAT

echo "$GITHUB_PAT" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
# или: docker login ghcr.io -u zatulik2606 -p "$GITHUB_PAT"

unset GITHUB_PAT

docker pull ghcr.io/zatulik2606/diaai-backend:main
```

---

## Проверка

```bash
docker pull ghcr.io/zatulik2606/diaai-backend:main
# Login Succeeded — при первом login
# Status: Image is up to date ... — pull OK
```

Credentials сохраняются в `~/.docker/config.json` (user `deploy` на VPS: `/home/deploy/.docker/config.json`).

Logout:

```bash
docker logout ghcr.io
```

---

## VPS (production)

На сервере под `deploy` — **выполняет пользователь** (агент не логинится):

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
# далее способ 1 или 2
```

Опционально GitHub Secret `GHCR_PULL_TOKEN` — см. [github-secrets.md](../deploy/github-secrets.md).

---

## Troubleshoot

| Симптом | Решение |
|---------|---------|
| `denied: denied` | PAT + login; scope `read:packages` |
| `unauthorized` | username = GitHub login, не org |
| WARNING insecure `-p` | использовать `--password-stdin` |
| pull OK без login | packages public — login не обязателен |
