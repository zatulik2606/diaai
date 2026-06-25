# VPS server (Timeweb Cloud)

Артефакты iter 2–3: SSH, bootstrap, layout деплоя на одном VPS.

## Документация

| Документ | Содержание |
|----------|------------|
| [docs/devops/twc-cli.md](../../docs/devops/twc-cli.md) | `twc`, SSH keys, presets, `server create` |
| [docs/devops/ghcr-stack.md](../../docs/devops/ghcr-stack.md) | stack из GHCR на сервере |
| [docs/tasks/tasklist-devops.md](../../docs/tasks/tasklist-devops.md) | iter 2–4, задачи 10–18 |

## SSH-ключи (task 10)

| Ключ | Файл | Роль |
|------|------|------|
| admin | `~/.ssh/diaai-admin` | ваш вход на VPS |
| deploy | `~/.ssh/diaai-deploy` | GitHub Actions (iter 4) |

Генерация и загрузка в Timeweb — см. [twc-cli.md § SSH-ключи](../../docs/devops/twc-cli.md#ssh-ключи-admin--deploy).

## Структура (по мере iter 2–3)

```
devops/server/
├── README.md                 # этот файл
├── bootstrap.sh              # task 13 — Docker, ufw, …
└── inventory.example.md      # task 12 — шаблон без секретов
```

Заполненный inventory (IP, server id) — **вне git** или redacted копия у владельца infra.

## Preset

Рекомендуемый: **2453** (2 vCPU, 4 GB, 50 GB, `ru-1`). Минимум: **2451** (2 GB, без bot).

## Production VPS (iter 2 ✅)

| | |
|--|--|
| Server | `diaai-prod` (ID `8460897`) |
| IPv4 | `201.51.4.34` |
| Region | `ru-3`, preset `4801`, Ubuntu 24.04 |
| SSH | `ssh -i ~/.ssh/diaai-admin root@201.51.4.34` |

Inventory: [inventory.example.md](inventory.example.md)

## Bootstrap (task 13 ✅)

Idempotent скрипт: Docker, compose, ufw, user `deploy`, каталог `/opt/diaai`.

```bash
# с локальной машины (admin key)
scp devops/server/bootstrap.sh ~/.ssh/diaai-deploy.pub root@201.51.4.34:/tmp/
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'bash /tmp/bootstrap.sh'
```

Проверка:

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'docker compose version'
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'docker compose version'
```

**ufw:** 22 (SSH), 3000 (web), 8000 (backend). PostgreSQL наружу не открывается (5433 только в compose, не в ufw).

| User | SSH | Docker |
|------|-----|--------|
| `root` | `diaai-admin` | да |
| `deploy` | `diaai-deploy` | да (group docker) |

Deploy layout: `/opt/diaai` (task 14 ✅) · stack live (task 15 ✅).

URLs: http://201.51.4.34:3000 · http://201.51.4.34:8000/health

**Next:** iter 4 — GHA deploy workflow.
