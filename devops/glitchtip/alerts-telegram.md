# GlitchTip → Telegram alerts (@diaaialarm_bot)

Бот **только для алертов** GlitchTip. Отдельный от основного diaai-бота (`TELEGRAM_BOT_TOKEN`).

| | Основной bot | Alarm bot |
|--|--------------|-----------|
| Username | ваш diaai bot | `@diaaialarm_bot` |
| Env | `TELEGRAM_BOT_TOKEN` | `TELEGRAM_ALARM_BOT_TOKEN` |
| Назначение | диалог с пациентом | уведомления об ошибках |

Связь: [hosted.md](hosted.md) · [how-to-get-tokens.md](../../docs/how-to-get-tokens.md)

---

## 1. Переменные окружения

Корневой `.env` (не в git):

```bash
# @diaaialarm_bot — GlitchTip alerts only
TELEGRAM_ALARM_BOT_TOKEN=
# chat_id получателя (личка или группа) — после /start бота
TELEGRAM_ALARM_CHAT_ID=
```

| Variable | Обязательна | Описание |
|----------|-------------|----------|
| `TELEGRAM_ALARM_BOT_TOKEN` | да | токен от [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_ALARM_CHAT_ID` | для send | numeric id чата (см. §2) |

> **Не путать** с `TELEGRAM_BOT_TOKEN` — это другой бот для `make run`.

---

## 2. Первый запуск — получить `chat_id`

1. В Telegram откройте [@diaaialarm_bot](https://t.me/diaaialarm_bot)
2. Нажмите **Start** (`/start`)
3. Локально:

```bash
export TELEGRAM_ALARM_BOT_TOKEN='...'
bash devops/glitchtip/scripts/test-alarm-bot.sh
```

Скрипт выведет `chat_id` из `getUpdates` и отправит тестовое сообщение, если id задан в env.

Или вручную:

```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_ALARM_BOT_TOKEN}/getUpdates" | python3 -m json.tool
# message.chat.id → TELEGRAM_ALARM_CHAT_ID
```

---

## 3. Проверка отправки

```bash
export TELEGRAM_ALARM_BOT_TOKEN='...'
export TELEGRAM_ALARM_CHAT_ID='123456789'
bash devops/glitchtip/scripts/test-alarm-bot.sh
```

Ожидание: в Telegram сообщение *«diaai GlitchTip alarm bot: test OK»*.

---

## 4. Подключение GlitchTip (webhook)

GlitchTip шлёт **Slack-compatible JSON**; Telegram API — другой формат. Прямой URL `api.telegram.org` **не подходит**.

**MVP (рекомендуется):** контейнер [`glitchtip-telegram-bridge`](../monitoring/glitchtip-telegram-bridge/) в profile `monitoring`:

```bash
make monitoring-up
```

1. GlitchTip → Project → **Alerts → Alert recipients → Webhook**
2. URL: `http://201.51.4.34:8080/webhook` (или `?secret=` если задан `GLITCHTIP_WEBHOOK_SECRET`)
3. Проверка:

```bash
curl -X POST http://127.0.0.1:8080/webhook \
  -H 'Content-Type: application/json' \
  -d '{"attachments":[{"title":"Test","title_link":"https://eu.glitchtip.com","text":"manual"}]}'
```

Подробно: [../monitoring/README.md](../monitoring/README.md) · ADR: [adr-005-observability.md](../../docs/adr/adr-005-observability.md)

Альтернативы (post-MVP):

| Вариант | Сложность |
|---------|-----------|
| [glitchtip-alert-telegram-bot](https://github.com/it-projects-llc/glitchtip-alert-telegram-bot) | готовый bridge |
| n8n / webhook relay | no-code |
| FastAPI endpoint в backend | полный контроль |

---

## 5. Безопасность

- Токен **только** в `.env` / secrets, не в git
- При утечке — `/revoke` в BotFather, новый token
- Бот не нужен в Docker image diaai-bot profile

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| `getUpdates` пустой | написать `/start` боту в Telegram |
| `403 chat not found` | неверный `TELEGRAM_ALARM_CHAT_ID` |
| `401 Unauthorized` | неверный token |
| GlitchTip webhook 4xx | нужен transform, не прямой Telegram URL |
