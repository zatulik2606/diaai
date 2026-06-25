# GlitchTip VPS inventory (example)

Отдельный VPS под error tracking. **Не** diaai-prod (`8460897` / `201.51.4.34`).

| Поле | Рекомендация | Пример |
|------|--------------|--------|
| Name | `diaai-glitchtip` | `diaai-glitchtip` |
| Server ID | `twc server list` | `________` |
| Region | `ru-3` | `ru-3` |
| Preset | **≥ 2 GB RAM** (лучше 4 GB) | preset `2451` / `4801` |
| OS | Ubuntu 24.04 | Ubuntu 24.04 |
| Public IPv4 | | `________` |
| UI + ingest | `:8000` | `http://IP:8000` |

## Связь с diaai-prod

| | |
|--|--|
| App VPS | `201.51.4.34` |
| ufw | allow `:8000` **from** `201.51.4.34` |

## Проекты GlitchTip

| Project | Platform | env на diaai-prod |
|---------|----------|-------------------|
| `diaai-backend` | Python / FastAPI | `GLITCHTIP_DSN` |
| `diaai-web` | JavaScript / Next.js | `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN` |

См. [timeweb-deploy.md](timeweb-deploy.md)
