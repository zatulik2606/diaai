# GlitchTip на Timeweb Cloud

**Основной** error tracking для diaai (РФ, без sentry.io). Sentry-compatible SDK — меняется только DSN.

Связь: [README.md](README.md) · diaai-prod [deploy/README.md](../deploy/README.md) · [twc-cli.md](../../docs/devops/twc-cli.md).

**Не поднимайте GlitchTip на diaai-prod** (4 GB) — отдельная VM **≥ 2 GB RAM**.

Docs: [glitchtip.com/documentation/install](https://glitchtip.com/documentation/install)

---

## Архитектура

```mermaid
flowchart LR
  User["Браузер"]
  App["diaai-prod\n201.51.4.34"]
  GT["diaai-glitchtip\n:8000"]

  App -->|"GLITCHTIP_DSN"| GT
  App -->|"WEB_* DSN"| GT
  User -->|"NEXT_PUBLIC_DSN\nесли UI :8000 доступен"| GT
```

| VPS | Роль | Порт |
|-----|------|------|
| `diaai-prod` | stack | 3000, 8000 |
| `diaai-glitchtip` | GlitchTip UI + ingest | **8000** |

---

## Фаза 0 — Подготовка

- [ ] `twc whoami` OK
- [ ] SSH: `~/.ssh/diaai-admin`
- [ ] Решение: **browser errors** — открыть `:8000` для вашего IP **или** только server-side web (без `NEXT_PUBLIC_GLITCHTIP_DSN`)

---

## Фаза 1 — VPS Timeweb

### 1.1 Preset

```bash
twc server list-presets --region ru-3
```

| | Минимум | Рекомендуется |
|--|---------|---------------|
| RAM | 2 GB | 4 GB |
| Disk | 20 GB | 40 GB+ |

GlitchTip ~512 MB–1 GB RAM (web + worker + postgres + valkey).

### 1.2 Создание

```bash
twc server create \
  --name diaai-glitchtip \
  --image ubuntu-24.04 \
  --preset-id PRESET_ID \
  --region ru-3 \
  --ssh-key diaai-admin \
  --disable-ssh-password-auth
```

- [ ] Сервер `on`, IPv4 записан → [inventory.example.md](inventory.example.md)

```bash
export GLITCHTIP_IP=YOUR.IP.HERE
ssh -i ~/.ssh/diaai-admin root@${GLITCHTIP_IP} 'uname -a'
```

---

## Фаза 2 — Bootstrap

```bash
scp devops/glitchtip/bootstrap-timeweb.sh root@${GLITCHTIP_IP}:/tmp/

ssh -i ~/.ssh/diaai-admin root@${GLITCHTIP_IP} \
  'DIAAPP_IP=201.51.4.34 ADMIN_IP=YOUR_HOME_IP bash /tmp/bootstrap-timeweb.sh'
```

- [ ] Docker + Compose
- [ ] ufw: 22; `:8000` from `201.51.4.34` + ваш IP

---

## Фаза 3 — Репозиторий и `.env`

### 3.1 Клон (monorepo)

```bash
ssh root@${GLITCHTIP_IP}

apt-get install -y git
git clone https://github.com/zatulik2606/diaai.git /opt/diaai
cd /opt/diaai/devops/glitchtip
```

### 3.2 Секреты

```bash
cp .env.example .env
chmod 600 .env

SECRET_KEY=$(openssl rand -hex 32)
PG_PASS=$(openssl rand -hex 16)
# отредактировать .env:
#   SECRET_KEY=...
#   POSTGRES_PASSWORD=...
#   DATABASE_URL=postgres://glitchtip:${PG_PASS}@postgres:5432/glitchtip
#   GLITCHTIP_DOMAIN=http://${GLITCHTIP_IP}:8000
```

- [ ] `GLITCHTIP_DOMAIN` = `http://IP:8000` (позже HTTPS + домен)
- [ ] `EMAIL_URL=consolemail://` для MVP (алерты в логах)

### 3.3 Запуск

```bash
cd /opt/diaai/devops/glitchtip
docker compose up -d
docker compose ps
```

- [ ] `web`, `worker` — Up (healthy)
- [ ] `migrate` — Exited 0

UI: **http://${GLITCHTIP_IP}:8000**

---

## Фаза 4 — Org, проекты, DSN

### 4.1 Первый вход

1. **Sign Up** — admin account
2. **Create organization** — `diaai`
3. **Settings** → `ENABLE_USER_REGISTRATION=false` в `.env` → `docker compose up -d`

### 4.2 Проекты

| Project | Platform в UI | DSN → |
|---------|---------------|-------|
| `diaai-backend` | Python | `GLITCHTIP_DSN` |
| `diaai-web` | JavaScript / Next.js | `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN` |

**Projects → Create → Client Keys (DSN)** — скопировать оба.

Шаблон: [dsn.env.example](dsn.env.example) → `dsn.local.env` (gitignored)

Пример:

```bash
GLITCHTIP_DSN=http://PUBLIC_KEY@${GLITCHTIP_IP}:8000/1
GLITCHTIP_WEB_DSN=http://PUBLIC_KEY@${GLITCHTIP_IP}:8000/2
NEXT_PUBLIC_GLITCHTIP_DSN=http://PUBLIC_KEY@${GLITCHTIP_IP}:8000/2
```

- [ ] Два проекта созданы
- [ ] DSN сохранены вне git

---

## Фаза 5 — diaai-prod

На **201.51.4.34**, `/opt/diaai/.env`:

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
nano /opt/diaai/.env
```

```bash
GLITCHTIP_DSN=http://...@GLITCHTIP_IP:8000/...
GLITCHTIP_WEB_DSN=http://...@GLITCHTIP_IP:8000/...
NEXT_PUBLIC_GLITCHTIP_DSN=http://...@GLITCHTIP_IP:8000/...
GLITCHTIP_ENVIRONMENT=production
GLITCHTIP_TRACES_SAMPLE_RATE=0.1
```

- [ ] DSN host = **GlitchTip IP**, не `127.0.0.1`
- [ ] Пересборка **web** если задан `NEXT_PUBLIC_GLITCHTIP_DSN` (CD или `make stack-up` build)

Проверка с prod:

```bash
ssh deploy@201.51.4.34 "curl -sf -o /dev/null -w '%{http_code}\n' http://${GLITCHTIP_IP}:8000/"
```

- [ ] HTTP 200/302 с diaai-prod (ufw)

---

## Фаза 6 — Приёмка

| # | Проверка | Ожидание |
|---|----------|----------|
| 1 | `docker compose ps` | web + worker healthy |
| 2 | UI | login, org `diaai`, 2 projects |
| 3 | Backend event | test message / 500 → issue `diaai-backend` |
| 4 | Web event | server error → `diaai-web` |
| 5 | diaai stack | `curl :8000/health` OK |

Тест backend (Python REPL на prod или dev с DSN):

```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_BACKEND_DSN")
sentry_sdk.capture_message("diaai glitchtip test")
```

---

## DoD (обязательный чеклист)

- [ ] VPS **≥ 2 GB**, отдельный от diaai-prod
- [ ] Bootstrap + compose green
- [ ] Org + **diaai-backend** + **diaai-web** + DSN
- [ ] diaai-prod `.env` + web rebuild при client DSN
- [ ] События видны в GlitchTip UI
- [ ] `ENABLE_USER_REGISTRATION=false` после onboarding

---

## Post-MVP

| Задача | Как |
|--------|-----|
| HTTPS | nginx + Let's Encrypt; `GLITCHTIP_DOMAIN=https://...`; `CSRF_TRUSTED_ORIGINS` |
| SMTP | `EMAIL_URL=smtp://...` в `.env` |
| Backup | `pg_dump` + volume `glitchtip_uploads` |
| Обновление | `docker compose pull && docker compose up -d` |

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| События не приходят | DSN URL; ufw from `201.51.4.34`; `docker compose logs worker` |
| 403 CSRF в UI | `CSRF_TRUSTED_ORIGINS` при reverse proxy |
| OOM | preset 4 GB; swap; `GLITCHTIP_MAX_EVENT_LIFE_DAYS=30` |
| Web client silent | rebuild с `NEXT_PUBLIC_*`; или только server DSN |
| migrate fails | `docker compose logs migrate`; postgres healthy |

---

## Make (локально / на VPS)

```bash
cd devops/glitchtip
cp .env.example .env   # edit
make glitchtip-up
make glitchtip-ps
make glitchtip-logs
```

См. [Makefile](Makefile)
