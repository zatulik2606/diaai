# GlitchTip (Sentry-compatible)

Error tracking для **diaai-backend** и **diaai-web**. SDK — Sentry-compatible; env — `GLITCHTIP_*`.

| Документ | Назначение |
|----------|------------|
| **[hosted.md](hosted.md)** | **Облако EU/US** (без VPS) — проверено |
| **[alerts-telegram.md](alerts-telegram.md)** | **@diaaialarm_bot** — алерты GlitchTip |
| **[alerts-email.md](alerts-email.md)** | **SMTP bridge** — email-алерты GlitchTip |
| **[timeweb-deploy.md](timeweb-deploy.md)** | self-hosted на Timeweb |
| [inventory.example.md](inventory.example.md) | VPS inventory |
| [dsn.env.example](dsn.env.example) | DSN шаблон |
| [compose.yml](compose.yml) | production stack |

## Быстрый старт (локально)

```bash
cd devops/glitchtip
cp .env.example .env
# SECRET_KEY=$(openssl rand -hex 32), править GLITCHTIP_DOMAIN
make glitchtip-up
open http://127.0.0.1:8000
```

## diaai-prod

После DSN — в `/opt/diaai/.env` на `201.51.4.34`. SDK уже в backend/web.

Альтернатива (тяжелее): [../sentry/timeweb-deploy.md](../sentry/timeweb-deploy.md)
