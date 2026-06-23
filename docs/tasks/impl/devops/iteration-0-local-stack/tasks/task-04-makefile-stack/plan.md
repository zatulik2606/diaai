# Task 04: Makefile stack-*

## Цель

Targets: stack-up, stack-down, stack-ps, stack-logs, stack-health, stack-init.

## Совместимость

`db-up` → `docker compose up -d postgres` only.

## DoD

`make stack-up && make stack-health` green.
