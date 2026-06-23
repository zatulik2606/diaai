# Task 09: Verify registry + docs

## Цель

E2E registry mode локально; закрыть iter 1 и область devops (prep).

## Сценарий

1. Tag local images → `ghcr.io/zatulik2606/diaai-*:main` (smoke без GHCR)
2. `make stack-up-registry && make stack-health`
3. `make test` — unit tests green

## Docs

- `docker-compose-local.md`, `devops/README.md`, `onboarding.md`, `architecture.md`
- `impl/devops/summary.md`, iter 1 summary, tasklist

## DoD

Verification log в summary; iter 1 ✅.
