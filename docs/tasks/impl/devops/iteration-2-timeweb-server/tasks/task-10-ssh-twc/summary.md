# Task 10 summary

## Сделано

- [`docs/devops/twc-cli.md`](../../../../../../devops/twc-cli.md) — iter 2 scope:
  - § SSH keys (admin + deploy): `ssh-keygen`, naming, `twc ssh-key new/list/add`
  - § Presets ru-1 (2453 / 2451), черновик `server create`
  - verify: `twc whoami`, `list-presets`
- [`devops/server/README.md`](../../../../../../devops/server/README.md) — каркас iter 2–3

## Verify (агент)

```text
twc whoami → wj602148
twc server list-presets --region ru-1 → 2451, 2453, …
twc ssh-key list → пусто (ключи ещё не загружены пользователем)
```

## Пользователь (DoD)

- [ ] `ssh-keygen` → `~/.ssh/diaai-admin`, `~/.ssh/diaai-deploy`
- [ ] `twc ssh-key new …` для обоих public keys
- [ ] `twc whoami` — OK

## Отложено

- Реальные ключи и VPS — task 11–12 (после согласования create)
