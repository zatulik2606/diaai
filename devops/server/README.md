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

**4 GB preset:** app + monitoring stack на одном хосте; `bootstrap.sh` создаёт **swap 2 GB** (защита от OOM при Loki/Prometheus).

## Production VPS (iter 2 ✅)

| | |
|--|--|
| Server | `diaai-prod` (ID `8460897`) |
| IPv4 | `201.51.4.34` |
| Region | `ru-3`, preset `4801`, Ubuntu 24.04 |
| SSH | см. [§ Проверка SSH](#проверка-ssh) |

Inventory: [inventory.example.md](inventory.example.md)

## Проверка SSH

Production: **`201.51.4.34`**. Вход только по ключу (пароль отключён).

### Admin — ваш вход на сервер

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34
```

При первом подключении подтвердите fingerprint (`yes`). Должна открыться shell **без пароля**.

Быстрая проверка:

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a'
```

### Deploy — ключ для CI/CD

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
```

Проверка docker и stack:

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'docker compose version'
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'cd /opt/diaai && docker compose ps'
```

### Сводка

| Ключ | User | Команда |
|------|------|---------|
| `~/.ssh/diaai-admin` | `root` | `ssh -i ~/.ssh/diaai-admin root@201.51.4.34` |
| `~/.ssh/diaai-deploy` | `deploy` | `ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34` |

Права на private keys:

```bash
chmod 600 ~/.ssh/diaai-admin ~/.ssh/diaai-deploy
```

### Если не работает

| Симптом | Что проверить |
|---------|----------------|
| `Permission denied (publickey)` | ключ существует; указан `-i`; `chmod 600` на private key |
| `No such file or directory` | ключи на этой машине — см. [twc-cli.md § SSH](../../docs/devops/twc-cli.md#ssh-ключи-admin--deploy) |
| `Connection timed out` | IP `201.51.4.34`; сервер `on` в Timeweb |
| запрос пароля | используйте `-i` с правильным ключом |

Генерация и загрузка ключей в Timeweb — [twc-cli.md § SSH-ключи](../../docs/devops/twc-cli.md#ssh-ключи-admin--deploy).

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

CD: [deploy/README.md](../deploy/README.md) · [github-secrets.md](../deploy/github-secrets.md).
