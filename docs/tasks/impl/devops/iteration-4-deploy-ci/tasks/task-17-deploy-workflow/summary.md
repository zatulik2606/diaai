# Task 17 summary

## Сделано

- [`.github/workflows/deploy.yml`](../../../../../../.github/workflows/deploy.yml)
  - trigger: `workflow_run` Docker Publish + `workflow_dispatch`
  - `appleboy/ssh-action`: `git fetch` + `reset --hard origin/main` + `clean -fd`, override, `make stack-*-registry`, health
  - smoke curl :8000/:3000
- [`devops/deploy/README.md`](../../../../../../devops/deploy/README.md) § CD

## Verify

→ task 18 после push / workflow_dispatch
