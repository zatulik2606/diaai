# Локальный запуск через Docker Compose

Полный stack diaai в одном корневом [`docker-compose.yml`](../../docker-compose.yml): PostgreSQL, backend, web. Bot — опционально (profile).

> **Альтернатива:** ручной multi-process dev — [onboarding.md](../onboarding.md) §2.

---

## Prerequisites

| Инструмент | Проверка |
|------------|----------|
| Docker Desktop / engine | `docker compose version` |
| make, curl | — |

Python/Node на хосте **не обязательны** для stack (нужны для `make test`, `make db-seed` с хоста).

---

## 1. Env

```bash
cp .env.example .env
# Обязательно до stack-up:
# BACKEND_SERVICE_TOKEN=<secure>   # не change-me
# OPENROUTER_API_KEY=<key>
# TELEGRAM_BOT_TOKEN=<token>       # только для profile bot
```

Web в контейнере читает `BACKEND_URL` и `BACKEND_SERVICE_TOKEN` из корневого `.env` (compose `env_file`). Отдельный `web/.env.local` для stack **не нужен**.

---

## 2. Первый запуск (demo data)

```bash
make stack-init
# = make db-reset && make stack-up
```

Или по шагам:

```bash
make db-reset      # PG + migrate + seed (@ivan_p, @doctor_ivanov)
make stack-up      # postgres + backend + web
make stack-health  # pg + /health + :3000
```

| URL | Сервис |
|-----|--------|
| http://localhost:3000 | web |
| http://localhost:8000/health | backend |
| localhost:5433 | PostgreSQL (host) |

Demo login: `ivan_p` → `/dashboard`, `doctor_ivanov` → `/leaderboard`.

---

## 3. Команды

| Команда | Действие |
|---------|----------|
| `make stack-up` | полный stack (build + up) |
| `make stack-up-bot` | stack + Telegram bot (profile `bot`) |
| `make stack-down` | остановить stack |
| `make stack-ps` | статус контейнеров |
| `make stack-logs` | логи всех сервисов (follow) |
| `make stack-logs-tail` | последние 100 строк (без follow) |
| `make stack-logs SVC=backend` | логи одного сервиса |
| `make stack-health` | pg + backend + web |
| `make stack-init` | db-reset + stack-up |

### Registry mode (GHCR)

После CI push образов в GHCR — без локальной сборки:

```bash
# login (private packages)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

make stack-pull-registry      # pull backend + web
make stack-up-registry        # up без build (--pull missing)
make stack-health
```

Переопределение tag/owner: `IMAGE_TAG=sha-abc1234 GHCR_OWNER=zatulik2606 make stack-up-registry`

Smoke без GHCR (локальные теги):

```bash
docker tag diaai-backend:local ghcr.io/zatulik2606/diaai-backend:main
docker tag diaai-web:local ghcr.io/zatulik2606/diaai-web:main
make stack-up-registry
```

Подробнее: [devops/ci/README.md](../../devops/ci/README.md)

### Только PostgreSQL (host dev)

```bash
make db-up       # docker compose up -d postgres
make db-reset    # migrate + seed с хоста
make backend-run # :8000 с reload
make web-dev     # :3000 hot reload
```

---

## 4. Bot (optional)

```bash
# TELEGRAM_BOT_TOKEN в .env
make stack-up-bot
# или
COMPOSE_PROFILES=bot make stack-up
```

Без token stack стартует без бота (profile не активен).

---

## 5. Архитектура stack

```
Host :5433 ── postgres (volume diaai_pg_data)
                └── backend :8000  (migrate on start)
                      ├── web :3000
                      └── bot (profile, polling)
```

Dockerfile'ы: [`devops/README.md`](../../devops/README.md).

---

## 6. Troubleshoot

| Симптом | Решение |
|---------|---------|
| `Set BACKEND_SERVICE_TOKEN...` | задать token в `.env`, не `change-me` |
| `FAIL: backend` | `make stack-logs SVC=backend`; проверить `OPENROUTER_API_KEY` |
| `FAIL: web` | `make stack-logs SVC=web`; пересобрать: `docker compose up -d --build web` |
| Порт 5433/8000/3000 занят | освободить или остановить: `make stack-down` |
| Пустой dashboard | `make db-seed` или `make db-reset` |
| Login 401/500 | seed + одинаковый `BACKEND_SERVICE_TOKEN` в `.env` |

Smoke: [smoke-test.md](../smoke-test.md) (web paths на stack).

---

## 7. Сборка образов вручную

```bash
docker build -f devops/docker/backend/Dockerfile -t diaai-backend:local .
docker build -f devops/docker/bot/Dockerfile -t diaai-bot:local .
docker build -f devops/docker/web/Dockerfile -t diaai-web:local web/
```

Iter 1: образы в GHCR — `make stack-up-registry` · [devops/ci/README.md](../../devops/ci/README.md)
