# Task 02 summary

## Сделано

- `devops/docker/backend/Dockerfile` + `entrypoint.sh` — uv, migrate, non-root `app`, HEALTHCHECK
- `devops/docker/bot/Dockerfile` — shared uv pattern, non-root
- `devops/docker/web/Dockerfile` — multi-stage, Node 24 bookworm, pnpm 11.6, production `next start`
- Root `.dockerignore`, `web/.dockerignore`, reference lists in `devops/docker/*/.dockerignore`

## Решения

- `uv sync` после copy `src/`, `backend/`, `README.md` (setuptools egg_base)
- Web: Node **24** (pnpm 11.6 падает на Node 20 в Docker с `ERR_UNKNOWN_BUILTIN_MODULE`)
- Web context: `web/`; Python context: repo root

## docker-expert (draft review)

| Finding | Action |
|---------|--------|
| Multi-stage web | ✅ deps → builder → runner |
| Non-root USER | ✅ app/nextjs |
| HEALTHCHECK | ✅ backend curl, web node http |
| .dockerignore | ✅ root + web |
| Bake prompts | ✅ in backend image |

## Verify

```bash
docker build -f devops/docker/backend/Dockerfile -t diaai-backend:local .
docker build -f devops/docker/bot/Dockerfile -t diaai-bot:local .
docker build -f devops/docker/web/Dockerfile -t diaai-web:local web/
```

All three builds ✅
