# Task 08 summary

## Сделано

- [`docker-compose.yml`](../../../../../../docker-compose.yml): profiles `build` + `registry` на backend/web; bot — profile `bot`
- [`Makefile`](../../../../../../Makefile):
  - `stack-up` → `COMPOSE_PROFILES=build`
  - `stack-up-registry` / `stack-up-registry-bot` — `--no-build --pull missing`
  - `stack-pull-registry` / `stack-pull-registry-bot` — явный pull из GHCR
  - `stack-ps/logs/down` — все profiles
- [`devops/ci/README.md`](../../../../../../devops/ci/README.md) — profiles table

## Review (docker-expert lite)

| Проверка | Build | Registry | Parity |
|----------|-------|----------|--------|
| env_file `.env` | ✅ | ✅ | ✅ |
| DATABASE_URL internal | ✅ | ✅ | ✅ |
| healthchecks | ✅ | ✅ | ✅ |
| postgres unchanged | ✅ | ✅ | — |

Bot в registry: образ через `DIAAI_BOT_IMAGE`; profile `bot` + `registry` в COMPOSE_PROFILES.

## Verify

- `make stack-up && make stack-health` ✅
- `make stack-up-registry && make stack-health` (local tags as GHCR) ✅
