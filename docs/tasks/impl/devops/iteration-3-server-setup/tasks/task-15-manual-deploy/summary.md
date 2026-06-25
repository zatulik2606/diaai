# Task 15 summary

## Сделано

- Stack registry на VPS `201.51.4.34`: postgres + backend + web
- Fix `compose.server.override.yml`: `ports: !override` (double bind 5433)
- Seed: `uv sync` + `make db-seed` на сервере
- Smoke external + login API
- Docs: smoke-test § Production VPS, onboarding, architecture

## Verify

```text
make stack-health on VPS → all passed ✅
curl http://201.51.4.34:8000/health → {"status":"ok","version":"1.0.0"}
curl http://201.51.4.34:3000/ → HTTP 307
POST /api/auth/login ivan_p → {"ok":true,"role":"diabetic"} HTTP 200
postgres 5433: localhost only, not in ufw
```

## Пользователь

Открыть в браузере: http://201.51.4.34:3000/login → `ivan_p`

## Отложено

- HTTPS / reverse proxy — post-MVP
- CD iter 4
