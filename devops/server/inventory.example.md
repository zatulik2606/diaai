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

## Проверка SSH (ручная)

Production IPv4: **`201.51.4.34`**.

**Admin:**

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a'
```

**Deploy:**

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'whoami'
```

Права: `chmod 600 ~/.ssh/diaai-admin ~/.ssh/diaai-deploy`

Полная инструкция и troubleshoot: [server/README.md](../server/README.md#проверка-ssh) · [twc-cli.md](../../docs/devops/twc-cli.md#3-проверка-ssh-ручная).

```bash
twc server get 8460897
```

## Ссылки

- [twc-cli.md](../../docs/devops/twc-cli.md)
- [tasklist-devops.md](../../docs/tasks/tasklist-devops.md) iter 2
