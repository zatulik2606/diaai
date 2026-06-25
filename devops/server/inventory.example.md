# Server inventory (example)

Шаблон инвентаря VPS diaai. **Заполненную копию** храните вне git (например `inventory.local.md` в `.gitignore`) или в password manager.

## Timeweb Cloud

| Поле | Пример | Production (2025-06) |
|------|--------|----------------------|
| Server ID | `1234567` | `8460897` |
| Name | `diaai-prod` | `diaai-prod` |
| Region | `ru-1` | `ru-3` |
| Availability zone | `msk-1` | `msk-1` |
| Preset ID | `2453` | `4801` (≈2453 в ru-3) |
| vCPU / RAM / Disk | 2 / 4 GB / 50 GB NVMe | 2 / 4 GB / 50 GB NVMe |
| OS | Ubuntu 24.04 | Ubuntu 24.04 |

## Network

| Поле | Пример |
|------|--------|
| Public IPv4 | `203.0.113.10` |
| Public IPv6 | optional |
| PTR | `*.twc1.net` |

## SSH

| Ключ | Timeweb ID | Файл | Назначение |
|------|------------|------|------------|
| diaai-admin | `708193` | `~/.ssh/diaai-admin` | вход человека |
| diaai-deploy | `708195` | `~/.ssh/diaai-deploy` | GitHub Actions (iter 4) |

| Поле | Значение |
|------|----------|
| SSH user | `root` (Ubuntu cloud image Timeweb) |
| Password auth | disabled (`--disable-ssh-password-auth`) |

## Проверка

```bash
ssh -i ~/.ssh/diaai-admin root@PUBLIC_IPV4 'uname -a'
twc server get SERVER_ID
```

## Ссылки

- [twc-cli.md](../../docs/devops/twc-cli.md)
- [tasklist-devops.md](../../docs/tasks/tasklist-devops.md) iter 2
