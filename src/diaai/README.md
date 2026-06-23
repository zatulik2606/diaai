# Telegram bot (`src/diaai`)

Тонкий клиент backend API ([vision.md](../../docs/vision.md)). Не вызывает OpenRouter напрямую — только `POST /api/v1/*` через [backend_client.py](backend_client.py).

## Структура

| Файл | Назначение |
|------|------------|
| `main.py` | entrypoint (`make run`) |
| `bot.py` | aiogram 3, polling |
| `handlers.py` | text, photo, voice → backend |
| `backend_client.py` | httpx → backend v1 |
| `config.py` | env: `TELEGRAM_BOT_TOKEN`, `BACKEND_URL`, `BACKEND_SERVICE_TOKEN` |

## Быстрый старт

```bash
# из корня репозитория
cp .env.example .env
# TELEGRAM_BOT_TOKEN, BACKEND_URL, BACKEND_SERVICE_TOKEN

make db-reset && make backend-run   # терминал 1
make install && make run            # терминал 2
```

Токены: [how-to-get-tokens.md](../../docs/how-to-get-tokens.md)

## Handlers

| Тип | Pipeline |
|-----|----------|
| Text | `POST /assistant/messages` |
| Photo | `POST /assistant/messages` + image_base64 |
| Voice | `POST /media/transcribe` → text → assistant |

## Тесты

```bash
make test    # includes tests/test_backend_client.py
```

## Документация

- [tasklist-bot.md](../../docs/tasks/tasklist-bot.md)
- [api-contract.md](../../docs/api/api-contract.md)
- [smoke-test.md](../../docs/smoke-test.md) §5
