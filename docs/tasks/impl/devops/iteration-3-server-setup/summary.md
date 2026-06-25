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

## Обязательная проверка (2026-06-07)

| Критерий | Результат |
|----------|-----------|
| Docker 29.6 + Compose v5.2 | ✅ |
| `make stack-pull-registry` | ✅ GHCR backend/web Pulled |
| `make stack-health` | ✅ postgres, backend, web |
| Public API | ✅ `http://201.51.4.34:8000/health` → `{"status":"ok",...}` |
| Public web | ✅ `http://201.51.4.34:3000` → HTTP 307 |

## Next

Iter 4: GitHub Secrets + deploy workflow ✅
