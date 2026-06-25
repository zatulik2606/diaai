# Sentry VPS inventory (example)

Шаблон **отдельного** VPS под self-hosted Sentry. **Не** diaai-prod (`8460897`).

Заполненную копию храните вне git (`inventory.local.md` / password manager).

## Timeweb Cloud

| Поле | Рекомендация | Пример |
|------|--------------|--------|
| Name | `diaai-sentry` | `diaai-sentry` |
| Server ID | из `twc server list` | `________` |
| Region | `ru-3` (если ru-1/2 заняты) | `ru-3` |
| Preset | **≥ 8 GB RAM**, 50+ GB disk | см. `twc server list-presets` |
| OS | Ubuntu 24.04 | Ubuntu 24.04 |

> Official self-hosted: [16 GB+ RAM](https://develop.sentry.dev/self-hosted/) для production load. MVP / малый трафик — **8 GB** + swap 4 GB.

## Network

| Поле | Значение |
|------|----------|
| Public IPv4 | `________` |
| Sentry UI + ingest | `:9000` |
| diaai-prod (app) | `201.51.4.34` |

## SSH

| Ключ | Файл | Назначение |
|------|------|------------|
| admin | `~/.ssh/diaai-admin` | bootstrap, install Sentry |

```bash
ssh -i ~/.ssh/diaai-admin root@SENTRY_IP
```

## Проекты Sentry (после install)

| Project | Platform | DSN env (diaai-prod `.env`) |
|---------|----------|----------------------------|
| `diaai-backend` | python-fastapi | `SENTRY_DSN` |
| `diaai-web` | javascript-nextjs | `WEB_SENTRY_DSN`, `NEXT_PUBLIC_SENTRY_DSN` |

## Ссылки

- [timeweb-deploy.md](timeweb-deploy.md) — чеклист деплоя
- [twc-cli.md](../../docs/devops/twc-cli.md)
- [deploy/README.md](../deploy/README.md) — diaai-prod
