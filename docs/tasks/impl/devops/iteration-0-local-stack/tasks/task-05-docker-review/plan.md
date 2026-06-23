# Task 05: Ревью docker-expert

## Цель

Audit Dockerfile'ов и compose; fix critical findings.

## Чеклист

- build context / .dockerignore
- non-root USER (where feasible)
- HEALTHCHECK
- secrets via env only
- networking, restart policy

## DoD

Findings в summary; `make stack-up` после правок.
