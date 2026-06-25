# Task 14 summary

## Сделано

- [`devops/deploy/README.md`](../../../../../../devops/deploy/README.md) — layout `/opt/diaai`, `.env`, ghcr login (manual), deploy SSH
- [`devops/deploy/compose.server.override.yml`](../../../../../../devops/deploy/compose.server.override.yml) — postgres `127.0.0.1:5433`
- [`docs/devops/ghcr-stack.md`](../../../../../../docs/devops/ghcr-stack.md) §11 Production VPS
- На VPS `201.51.4.34`:
  - git clone → `/opt/diaai`
  - `compose.override.yml` + `.env` (chmod 600, owner deploy)
  - deploy SSH + docker OK

## Verify

```text
docker pull ghcr.io/zatulik2606/diaai-backend:main → OK без login (public package)
ssh deploy@201.51.4.34 → docker compose version OK
/opt/diaai/.env exists, mode 600
```

## GHCR login

Packages **public** — login не потребовался. Инструкция для `denied` — deploy README §5 (пользователь выполняет сам).

## Отложено

- `make stack-up-registry` + smoke — task 15
- Seed БД (`uv` / `db-reset`) — task 15
