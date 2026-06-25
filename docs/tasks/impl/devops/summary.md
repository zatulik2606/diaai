# DevOps — итог области (iter 0–4)

Опирается на [tasklist-devops.md](../../tasklist-devops.md)

## Прогресс

**18 / 18 задач ✅**

| Iter | Результат |
|------|-----------|
| 0 | Локальный docker-compose stack |
| 1 | GHCR + `docker-publish.yml` |
| 2 | VPS Timeweb `201.51.4.34` |
| 3 | Bootstrap + manual registry deploy |
| 4 | GHA CD `deploy.yml` |

## Production

- http://201.51.4.34:3000
- http://201.51.4.34:8000/health
- CD: push `main` → publish → deploy

## Post-MVP

K8s, managed DB, HTTPS reverse proxy, full CI on PR — см. tasklist § Post-MVP
