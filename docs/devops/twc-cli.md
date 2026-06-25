# Timeweb Cloud CLI (twc)

Подготовка к post-MVP deploy diaai на [Timeweb Cloud](https://timeweb.cloud). **Сейчас:** только настройка CLI; автодеплой в репозитории не реализован.

Связь: образы в GHCR — [ghcr-stack.md](ghcr-stack.md) · CI — [devops/ci/README.md](../../devops/ci/README.md).

---

## Зачем

| Этап | twc |
|------|-----|
| iter 0–1 (✅) | не требуется |
| post-MVP deploy | VPS / Apps / K8s в Timeweb Cloud |

Типичный сценарий: сервер → `docker login ghcr.io` → `docker compose` с registry profile (см. [ghcr-stack.md](ghcr-stack.md)).

---

## Установка

```bash
# macOS (если tap доступен)
brew install timeweb-cloud/tap/twc

# или pip
pip install twc-cli
# часто: ~/.local/bin/twc — добавьте в PATH
```

Проверка:

```bash
twc --version
```

---

## Настройка

### 1. API-токен

1. [timeweb.cloud](https://timeweb.cloud) → профиль → **API и Terraform**
2. Создать токен (права на серверы, apps, сеть — по задаче)

### 2. Конфиг

```bash
twc config init
# или вручную:
twc config set token YOUR_API_TOKEN
```

Файл: `~/.twcrc` (TOML):

```toml
token = "YOUR_API_TOKEN"
```

Путь к файлу: `twc config file`

Профили: `twc config profiles` · переключение: `twc -p PROFILE_NAME ...`

### 3. Проверка

```bash
twc whoami
twc account status
twc server list
```

Ожидание: `whoami` — login аккаунта, команды без `401` / `Unauthorized`.

---

## Полезные команды (справка)

| Команда | Назначение |
|---------|------------|
| `twc server list` | VPS |
| `twc apps list` | Cloud Apps |
| `twc ssh-key list` | SSH-ключи для серверов |
| `twc ip list` | floating IP |
| `twc config dump` | текущий конфиг (⚠️ содержит token) |
| `twc config edit` | открыть `~/.twcrc` в редакторе |

Документация: `twc --help` · [Timeweb Cloud docs](https://timeweb.cloud/docs).

---

## Безопасность

| Правило | Почему |
|---------|--------|
| **Не коммитить** `~/.twcrc` | API token = полный доступ к облаку |
| Не логировать `twc config dump` | token в plaintext |
| CI/CD | secret `TWC_TOKEN` / `TWC_API_TOKEN`, не в коде |
| Ротация | при утечке — отозвать ключ в панели Timeweb |

Как `.env` для приложения — только локально или в secrets manager.

---

## Post-MVP (не в scope iter 0–1)

- Provision VPS через `twc server create`
- Pull `ghcr.io/zatulik2606/diaai-*` на сервере
- `docker compose` + `.env` production
- CD workflow (GitHub Actions + twc / SSH)

См. [tasklist-devops.md](../tasks/tasklist-devops.md) § Post-MVP.
