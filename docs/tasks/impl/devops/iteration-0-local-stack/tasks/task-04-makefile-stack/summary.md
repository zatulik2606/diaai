# Task 04 summary

## Сделано

- `stack-up`, `stack-up-bot`, `stack-down`, `stack-ps`, `stack-logs`, `stack-logs-tail`, `stack-health`, `stack-init`
- **`db-up` исправлен:** `docker compose up -d postgres` (не full stack)

## Verify

- `make stack-health` ✅
- `make db-up` → только `postgres` ✅
