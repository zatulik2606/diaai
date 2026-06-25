# Task 10: SSH-ключи (admin + deploy) и twc CLI

## Цель

Инструкция по двум SSH-ключам и расширение `twc-cli.md` для iter 2.

## Файлы

- `docs/devops/twc-cli.md` — § SSH keys, presets, upload key
- `devops/server/README.md` — каркас iter 2–3

## Архитектура ключей

| Ключ | Файл (пример) | Назначение |
|------|---------------|------------|
| admin | `~/.ssh/diaai-admin` | вход человека на VPS |
| deploy | `~/.ssh/diaai-deploy` | GitHub Actions CD (iter 4) |

Private keys — только локально / GitHub Secrets; public — `twc ssh-key new`.

## DoD

- docs самодостаточны для генерации ключей и `twc whoami` / `list-presets`
- private keys не в git
