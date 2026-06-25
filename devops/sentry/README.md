# Sentry — diaai-backend + diaai-web

Error monitoring для **FastAPI** и **Next.js**. Два проекта, два DSN.

| Режим | Когда |
|-------|-------|
| **[Timeweb GlitchTip](../glitchtip/timeweb-deploy.md)** | **РФ, основной путь** — VPS ≥2 GB |
| [Timeweb Sentry](timeweb-deploy.md) | full self-hosted, ≥8 GB |
| **[Self-hosted локально](#self-hosted-on-premise)** | dev / staging на своей машине |
| [sentry.io](#sentryio-saas) | если облако доступно (не РФ) |

Связь: [devops/README.md](../README.md) · **деплой Timeweb:** [timeweb-deploy.md](timeweb-deploy.md) · DSN: [dsn.env.example](dsn.env.example).

SDK уже в backend и web — достаточно прописать DSN в `.env`.

---

## sentry.io (SaaS)

> Из РФ часто **403 / недоступен** — используйте [timeweb-deploy.md](timeweb-deploy.md).

### 1. Аккаунт и org

1. [sentry.io/signup](https://sentry.io/signup/)
2. Создайте organization (slug, например `diaai`) — или используйте существующую
3. **Settings → Auth Tokens** → [Create Token](https://sentry.io/settings/account/api/auth-tokens/)  
   Тип: **User Auth Token** (Personal Tokens), не Internal Integration.  
   Scopes: `org:read`, `project:read`, `project:write`  
   При **403**: добавить `org:write`, `team:write` или создать проекты в UI (см. § Troubleshooting).

### 2. Проекты и DSN (скрипт)

```bash
export SENTRY_AUTH_TOKEN=sntrys_...
export SENTRY_ORG=diaai          # slug вашей org на sentry.io

bash devops/sentry/scripts/create-projects-cloud.sh
# → devops/sentry/dsn.cloud.local.env
```

Создаст **`diaai-backend`** (python-fastapi) и **`diaai-web`** (javascript-nextjs).

Если org не найдена — скрипт выведет список доступных org slug.

### 3. UI (без скрипта)

1. [sentry.io](https://sentry.io) → **Create Project**
2. `diaai-backend` → FastAPI → скопировать DSN
3. `diaai-web` → Next.js → скопировать DSN

Шаблон: [dsn.cloud.env.example](dsn.cloud.env.example)

### 4. DSN в `.env`

```bash
# корневой .env
SENTRY_DSN=https://xxx@o....ingest.sentry.io/...          # backend
WEB_SENTRY_DSN=https://yyy@o....ingest.sentry.io/...      # web (docker)
NEXT_PUBLIC_SENTRY_DSN=https://yyy@o....ingest.sentry.io/...
SENTRY_URL=https://sentry.io
SENTRY_ORG=diaai
SENTRY_ENVIRONMENT=production

# web/.env.local (pnpm dev)
SENTRY_DSN=https://yyy@o....ingest.sentry.io/...
NEXT_PUBLIC_SENTRY_DSN=https://yyy@o....ingest.sentry.io/...
```

Пустой `SENTRY_DSN` — мониторинг **выключен**.

---

## Self-hosted (on-premise)

Production на Timeweb: **[timeweb-deploy.md](timeweb-deploy.md)** — полный чеклист.

Локальный dev — см. ниже. Production Timeweb — [timeweb-deploy.md](timeweb-deploy.md).

## Требования

| Ресурс | Минимум (dev) | Timeweb VPS |
|--------|---------------|-------------|
| RAM | 8 GB | 8 GB (+ swap) · лучше 16 GB |
| Docker | Engine + Compose v2 | то же |
| Диск | 20 GB | 50 GB+ |

> На prod VPS diaai (4 GB) **не** поднимайте Sentry на том же хосте — вынесите на отдельную машину или локальный dev-сервер.

---

## 1. Установка self-hosted Sentry

```bash
make sentry-install    # git clone getsentry/self-hosted
cd devops/sentry/self-hosted
./install.sh           # интерактивно: версия, создать admin user
docker compose up -d
```

UI: **http://127.0.0.1:9000** (или `http://YOUR_SENTRY_HOST:9000`).

При первом входе создайте организацию **`diaai`** (slug `diaai`).

---

## 2. Проекты и DSN

### Вариант A — скрипт (API)

1. Sentry → **Settings → Auth Tokens** → token с `project:write`, `org:read`
2. Запуск:

```bash
export SENTRY_URL=http://127.0.0.1:9000
export SENTRY_AUTH_TOKEN=sntrys_...
bash devops/sentry/scripts/create-projects.sh
```

Создаст проекты **`diaai-backend`** (python-fastapi) и **`diaai-web`** (javascript-nextjs), запишет DSN в `devops/sentry/dsn.local.env` (gitignored).

### Вариант B — UI

1. **Projects → Create Project**
2. `diaai-backend` — platform **FastAPI**
3. `diaai-web` — platform **Next.js**
4. В каждом: **Settings → Client Keys (DSN)** — скопировать DSN

Заполните [dsn.env.example](dsn.env.example) → сохраните как `dsn.local.env`.

---

## 3. DSN в приложениях

| Проект | Переменные | Куда |
|--------|------------|------|
| **diaai-backend** | `SENTRY_DSN` | корневой `.env` |
| **diaai-web** (server) | `SENTRY_DSN` | `web/.env.local`; в Docker: `WEB_SENTRY_DSN` → `SENTRY_DSN` |
| **diaai-web** (browser) | `NEXT_PUBLIC_SENTRY_DSN` | `.env`, `web/.env.local`; **build-time** для Docker |

Общие (опционально):

```bash
SENTRY_URL=http://127.0.0.1:9000
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1
```

Пример корневого `.env` (два проекта — два DSN):

```bash
# diaai-backend
SENTRY_DSN=http://KEY@127.0.0.1:9000/2

# diaai-web (docker-compose)
WEB_SENTRY_DSN=http://KEY@127.0.0.1:9000/3
NEXT_PUBLIC_SENTRY_DSN=http://KEY@127.0.0.1:9000/3
```

`web/.env.local` для `pnpm dev`:

```bash
SENTRY_DSN=http://KEY@127.0.0.1:9000/3
NEXT_PUBLIC_SENTRY_DSN=http://KEY@127.0.0.1:9000/3
```

Пустой `SENTRY_DSN` — Sentry **отключён** (локальная разработка без мониторинга).

---

## 4. Проверка

**Backend:**

```bash
# временно вызвать тестовую ошибку или curl несуществующий internal endpoint
# событие должно появиться в Sentry → diaai-backend
make backend-run
```

**Web:**

```bash
cd web && pnpm dev
# в браузере — ошибка в devtools console → diaai-web
```

**Docker stack:**

```bash
# .env с DSN перед build web (NEXT_PUBLIC_*)
make stack-up
```

---

## Make-команды

| Команда | Действие |
|---------|----------|
| `bash devops/sentry/scripts/create-projects-cloud.sh` | проекты + DSN на **sentry.io** |
| `bash devops/sentry/scripts/create-projects.sh` | проекты + DSN на **self-hosted** |
| `make sentry-install` | clone `getsentry/self-hosted` |
| `make sentry-up` | `docker compose up -d` в self-hosted |
| `make sentry-down` | остановить Sentry |
| `make sentry-ps` | статус контейнеров Sentry |

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| **403 Forbidden** (API / скрипт) | см. ниже |
| События не приходят | проверить DSN; self-hosted URL доступен из контейнера |
| Web client без событий | пересобрать образ после `NEXT_PUBLIC_SENTRY_DSN` |
| `install.sh` OOM | больше RAM или отдельный сервер |

### 403 Forbidden на sentry.io

Частые причины:

1. **Неверный тип токена** — нужен **User Auth Token**: [Personal Tokens](https://sentry.io/settings/account/api/auth-tokens/), не Internal Integration (если integration не привязана к org с Admin).
2. **Мало scopes** — минимум `org:read`, `project:write`; при создании team/project добавьте `org:write`, `team:write`.
3. **Org запретила создание проектов members** — Settings → General → **Allow Members to Create Projects** → включить, или попросить Owner создать проекты.
4. **Роль Member без прав** — Owner/Manager создаёт проекты в UI, вы копируете DSN.
5. **Неверный `SENTRY_ORG`** — slug org (Settings → General), не display name.

**Обход без API:** создайте проекты в UI → **Projects → Create** → скопируйте DSN в [dsn.cloud.env.example](dsn.cloud.env.example).

Проверка токена:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  https://sentry.io/api/0/organizations/
# 200 = token OK · 401 = неверный token · 403 = scopes/доступ
```

Self-hosted docs: https://develop.sentry.dev/self-hosted/
