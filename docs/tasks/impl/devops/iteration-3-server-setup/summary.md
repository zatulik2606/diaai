# Итерация 3 summary

## Ценность

Production stack из GHCR на VPS; smoke API + web login.

## Задачи

| # | Статус |
|---|--------|
| 13 Bootstrap | ✅ |
| 14 Layout + `.env` | ✅ |
| 15 Manual stack + smoke | ✅ |

## Production URLs

| | |
|--|--|
| Web | http://201.51.4.34:3000 |
| API | http://201.51.4.34:8000/health |
| Path | `/opt/diaai` (user `deploy`) |

## Отклонения

- `compose.override.yml`: `ports: !override` — fix double port bind
- Seed на VPS через `uv` (не в bootstrap)

## Next

Iter 4: GitHub Secrets + deploy workflow
