# Task 11: Создание VPS Timeweb

## Цель

VPS preset 2453 (или эквивалент), Ubuntu 24.04, public IPv4, SSH key admin.

## Команда

```bash
twc server create \
  --name diaai-prod \
  --image ubuntu-24.04 \
  --preset-id PRESET_ID \
  --ssh-key diaai-admin \
  --region REGION \
  --disable-ssh-password-auth
```

## DoD

Сервер `on`, public IP, SSH по `diaai-admin`.
