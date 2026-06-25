# Timeweb Cloud CLI (twc)

Управление VPS diaai на [Timeweb Cloud](https://timeweb.cloud). **Iter 2:** SSH-ключи и подготовка сервера; создание VPS — task 11 (с согласования).

Связь: [devops/server/README.md](../../devops/server/README.md) · GHCR — [ghcr-stack.md](ghcr-stack.md) · CI — [devops/ci/README.md](../../devops/ci/README.md) · [tasklist-devops.md](../tasks/tasklist-devops.md).

Официальная документация CLI: [timeweb-cloud/twc docs/ru](https://github.com/timeweb-cloud/twc/blob/master/docs/ru/README.md).

---

## Зачем

| Этап | twc |
|------|-----|
| iter 0–1 (✅) | не требуется |
| iter 2 (📋) | presets, SSH keys, `server create` |
| iter 3–4 | тот же сервер; CD через SSH + GHCR |

---

## Установка

```bash
# macOS
brew install timeweb-cloud/tap/twc

# или pip
pip install twc-cli
# часто: ~/.local/bin/twc — добавьте в PATH
```

```bash
twc --version
```

---

## Настройка API

### 1. Токен

1. [timeweb.cloud](https://timeweb.cloud) → профиль → **API и Terraform**
2. Создать токен (права на серверы и SSH-ключи)

### 2. Конфиг

```bash
twc config init
# или:
twc config set token YOUR_API_TOKEN
```

Файл `~/.twcrc` (TOML):

```toml
token = "YOUR_API_TOKEN"
```

Профили: `twc config profiles` · `twc -p PROFILE_NAME ...`

### 3. Проверка

```bash
twc whoami
twc account status
twc server list
```

Ожидание: `whoami` — login аккаунта, без `401`.

**Verify (2025-06):** `twc whoami` → `wj602148`; `twc server list-presets --region ru-1` — presets 2451, 2453, …

---

## SSH-ключи (admin + deploy)

Два ключа — **разные роли**. Private keys **не коммитить** и не класть в репозиторий.

| Ключ | Файлы (пример) | Кто использует |
|------|----------------|----------------|
| **admin** | `~/.ssh/diaai-admin`, `~/.ssh/diaai-admin.pub` | вы — вход на VPS, bootstrap |
| **deploy** | `~/.ssh/diaai-deploy`, `~/.ssh/diaai-deploy.pub` | GitHub Actions (iter 4); public key на сервере |

### 1. Генерация (выполняет пользователь)

```bash
# admin — ed25519, без passphrase или с passphrase (на ваш выбор)
ssh-keygen -t ed25519 -C "diaai-admin" -f ~/.ssh/diaai-admin

# deploy — отдельный ключ; passphrase не нужен (ключ уйдёт в GitHub Secret)
ssh-keygen -t ed25519 -C "diaai-deploy" -f ~/.ssh/diaai-deploy -N ""
```

Права:

```bash
chmod 600 ~/.ssh/diaai-admin ~/.ssh/diaai-deploy
chmod 644 ~/.ssh/diaai-admin.pub ~/.ssh/diaai-deploy.pub
```

### 2. Загрузка public key в Timeweb Cloud

```bash
# admin — default для новых серверов (task 11)
twc ssh-key new ~/.ssh/diaai-admin.pub --name diaai-admin --default

# deploy — без default (добавим на сервер в iter 3/4)
twc ssh-key new ~/.ssh/diaai-deploy.pub --name diaai-deploy

twc ssh-key list
```

На существующий сервер (после create):

```bash
twc ssh-key add SERVER_ID SSH_KEY_ID
```

### 3. Проверка SSH (ручная)

Production VPS: IPv4 **`201.51.4.34`**. Пароль отключён — только ключ.

**Admin** (ваш вход, user `root`):

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34
```

Без интерактивной сессии:

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a'
```

Ожидание: prompt shell или вывод `Linux ... Ubuntu 24.04` **без запроса пароля**.

**Deploy** (CI/CD, user `deploy`):

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34
```

Проверка доступа к stack:

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'cd /opt/diaai && docker compose ps'
```

| Ключ | User | Файл |
|------|------|------|
| admin | `root` | `~/.ssh/diaai-admin` |
| deploy | `deploy` | `~/.ssh/diaai-deploy` |

**Troubleshoot**

| Симптом | Решение |
|---------|---------|
| `Permission denied (publickey)` | проверить путь к ключу; `chmod 600 ~/.ssh/diaai-admin` |
| `No such file or directory` (ключ) | сгенерировать ключи (§1) или скопировать с машины, где создавали |
| `Connection timed out` | IP и статус сервера в панели Timeweb |
| запрос пароля | на сервере только ключи; проверить `-i ~/.ssh/diaai-admin` |

Подробнее: [devops/server/README.md § Проверка SSH](../../devops/server/README.md#проверка-ssh).

---

## Presets VPS (ru-1)

Минимально **достаточный** под full stack (postgres + backend + web + bot):

```bash
twc server list-presets --region ru-1
```

| Preset | CPU | RAM | Disk | ~₽/мес | Рекомендация |
|--------|-----|-----|------|--------|--------------|
| **2453** | 2 | 4 GB | 50 GB NVMe | 1000 | **production MVP** |
| 2451 | 2 | 2 GB | 40 GB NVMe | 800 | staging без bot |

Публичный IPv4 обязателен — при `server create` **не** использовать `--no-public-ip`.

Черновик create (task 11 ✅ — production в **ru-3**):

```bash
# ru-1/ru-2 могут вернуть no_free_node — см. inventory.example.md
twc server create \
  --name diaai-prod \
  --image ubuntu-24.04 \
  --preset-id 4801 \
  --region ru-3 \
  --ssh-key diaai-admin \
  --disable-ssh-password-auth
```

Production: ID `8460897`, IPv4 `201.51.4.34`.

---

## Полезные команды

| Команда | Назначение |
|---------|------------|
| `twc whoami` | login аккаунта |
| `twc server list-presets --region ru-1` | тарифы VPS |
| `twc server list` | список серверов |
| `twc server get ID` | детали (IP, status) |
| `twc ssh-key list` | ключи в облаке |
| `twc ssh-key new FILE --name NAME` | загрузить public key |
| `twc config dump` | ⚠️ содержит token |

Справка: `twc --help` · `twc server create --help`

---

## Безопасность

| Правило | Почему |
|---------|--------|
| **Не коммитить** `~/.twcrc`, `~/.ssh/diaai-*` (private) | полный доступ к облаку / серверу |
| Не логировать `twc config dump` | token в plaintext |
| `diaai-deploy` private key → только **GitHub Secret** `DEPLOY_SSH_KEY` (iter 4) | CI/CD |
| Ротация | при утечке — удалить ключ в Timeweb + GitHub + `authorized_keys` |

Как `.env` приложения — только локально или secrets manager.

---

## Дальше (iter 2–4)

| Task | Действие |
|------|----------|
| 11 | `twc server create` (с согласования) |
| 12 | inventory сервера в docs |
| 13–15 | bootstrap, `docker login ghcr.io` (**вручную**), stack на VPS |
| 16–18 | GitHub Secrets + deploy workflow |

См. [devops/server/README.md](../../devops/server/README.md).
