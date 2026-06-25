# Локальный stack из образов GHCR

Запуск **без `docker build`**: backend и web берутся из GitHub Container Registry. PostgreSQL — официальный образ `postgres:16-alpine` (как и в build-режиме).

> Build-режим (локальная сборка): [docker-compose-local.md](docker-compose-local.md)  
> CI и naming образов: [devops/ci/README.md](../../devops/ci/README.md)

---

## Что нужно

| Инструмент | Зачем |
|------------|--------|
| Docker Desktop / engine | compose, pull образов |
| `make`, `curl` | команды stack |
| Git + clone репозитория | `docker-compose.yml`, `.env.example`, Makefile |
| `uv` + Python 3.12 | **только для первого seed БД** (`make db-reset` / `make db-seed`) |

Python/Node для **работы** stack не нужны — только для однократной инициализации demo-данных с хоста.

---

## Образы

| Сервис | GHCR image (по умолчанию) |
|--------|---------------------------|
| backend | `ghcr.io/zatulik2606/diaai-backend:main` |
| web | `ghcr.io/zatulik2606/diaai-web:main` |
| bot (optional) | `ghcr.io/zatulik2606/diaai-bot:main` |

Архитектуры: **linux/amd64**, **linux/arm64** (Apple Silicon).

Переопределение:

```bash
IMAGE_TAG=sha-abc1234 GHCR_OWNER=zatulik2606 make stack-pull-registry
```

---

## 1. Клонировать репозиторий

```bash
git clone https://github.com/zatulik2606/diaai.git
cd diaai
```

Достаточно файлов orchestration; исходники backend/web для stack **не собираются**.

---

## 2. Настроить `.env`

```bash
cp .env.example .env
```

Обязательно в `.env`:

```bash
BACKEND_SERVICE_TOKEN=<secure-not-change-me>   # не "change-me"
OPENROUTER_API_KEY=<key>
# TELEGRAM_BOT_TOKEN=<token>                   # только для bot
```

Web читает `BACKEND_URL` и `BACKEND_SERVICE_TOKEN` из корневого `.env` через compose. Отдельный `web/.env.local` не нужен.

---

## 3. Login в GHCR (если `denied` при pull)

### Шаг 1 — pull без login

```bash
docker pull ghcr.io/zatulik2606/diaai-backend:main
```

Packages **public** — часто достаточно этого шага. При `Pull complete` / `Image is up to date` → §4.

### Шаг 2 — login (только если pull вернул `denied`)

PAT (classic), scope **`read:packages`**. Username: **`zatulik2606`** (не `$zatulik2606`, не пароль от GitHub).

```bash
read -s GITHUB_PAT
echo "$GITHUB_PAT" | docker login ghcr.io -u zatulik2606 --password-stdin
unset GITHUB_PAT
```

Подробнее: **[devops/ci/ghcr-login.md](../../devops/ci/ghcr-login.md)**.

### Шаг 3 — pull снова

```bash
docker pull ghcr.io/zatulik2606/diaai-backend:main
```

Затем stack:

```bash
make stack-pull-registry
make stack-up-registry
```

---

## 4. Первый запуск (БД + stack)

### 4a. Demo-данные (рекомендуется)

Нужен `uv` на хосте (см. [onboarding.md](../onboarding.md)):

```bash
make db-reset
# postgres :5433 + migrate + seed (@ivan_p, @doctor_ivanov)
```

### 4b. Поднять stack из GHCR

```bash
make stack-pull-registry
make stack-up-registry
make stack-health
```

| URL | Сервис |
|-----|--------|
| http://localhost:3000 | web |
| http://localhost:8000/health | backend |
| localhost:5433 | PostgreSQL |

Demo login: **`ivan_p`** → `/dashboard`, **`doctor_ivanov`** → `/leaderboard`.

### Одной цепочкой (после `db-reset`)

```bash
make stack-pull-registry && make stack-up-registry && make stack-health
```

---

## 5. Обновление образов (без пересборки)

После нового push в `main` и green CI:

```bash
make stack-pull-registry
make stack-up-registry
make stack-health
```

Конкретный commit:

```bash
IMAGE_TAG=sha-519e194 make stack-pull-registry
IMAGE_TAG=sha-519e194 make stack-up-registry
```

---

## 6. Bot (optional)

```bash
# TELEGRAM_BOT_TOKEN в .env
make stack-pull-registry-bot
make stack-up-registry-bot
```

---

## 7. Полезные команды

| Команда | Действие |
|---------|----------|
| `make stack-down` | остановить stack |
| `make stack-ps` | статус контейнеров |
| `make stack-logs` | логи (follow) |
| `make stack-logs SVC=backend` | логи одного сервиса |
| `make stack-health` | pg + backend + web |

---

## 8. Build vs Registry

| | Build (`make stack-up`) | Registry (`make stack-up-registry`) |
|--|-------------------------|-------------------------------------|
| Образы | локальная сборка | pull из GHCR |
| Profile compose | `build` | `registry` |
| Postgres | тот же compose | тот же compose |
| Файл | один `docker-compose.yml` | один `docker-compose.yml` |

---

## 9. Troubleshoot

| Симптом | Решение |
|---------|---------|
| `denied` при pull | [ghcr-login.md](../../devops/ci/ghcr-login.md); проверить visibility package |
| `no matching manifest for linux/arm64` | обновить образы (CI публикует amd64+arm64 с iter 1) |
| `FAIL: backend` | `make stack-logs SVC=backend`; проверить `.env` |
| Пустой dashboard / login 401 | `make db-reset` или `make db-seed` |
| Порт 5433/8000/3000 занят | `make stack-down` |
| CI ещё не публиковал образы | Actions → **Docker Publish** green на нужном commit |

Проверка CI: https://github.com/zatulik2606/diaai/actions — run **success** для commit, с которого тянете `IMAGE_TAG`.

---

## 10. Минимальный сценарий «только Docker»

Если на машине **нет** `uv`, но нужен быстрый smoke:

```bash
cp .env.example .env   # задать BACKEND_SERVICE_TOKEN, OPENROUTER_API_KEY
make stack-up-registry   # postgres + migrate (entrypoint backend)
# seed не будет — login demo не сработает без make db-seed с хоста
```

Для полноценного demo один раз установите `uv` и выполните `make db-reset`.

---

## 11. Production VPS (Timeweb Cloud)

Полная инструкция layout, `.env`, GHCR login (ручной шаг): **[devops/deploy/README.md](../../devops/deploy/README.md)**.

Кратко:

| | |
|--|--|
| Server | `diaai-prod` (ID `8460897`, Ubuntu 24.04, `ru-3`) |
| IPv4 | `201.51.4.34` |
| Path | `/opt/diaai` (user `deploy`) |
| Override | `compose.override.yml` — postgres на `127.0.0.1:5433` |
| Pull | `make stack-pull-registry` (packages public — login часто не нужен) |
| Up | `make stack-up-registry` |
| URLs | http://201.51.4.34:3000 · http://201.51.4.34:8000/health |
| SSH | `ssh -i ~/.ssh/diaai-admin root@201.51.4.34` — см. [server/README.md § Проверка SSH](../../devops/server/README.md#проверка-ssh) |

**`docker login ghcr.io`** — только если `denied` при pull; выполняет **пользователь** (PAT `read:packages`). См. deploy README §5.

Bootstrap VPS: [devops/server/README.md](../../devops/server/README.md).
