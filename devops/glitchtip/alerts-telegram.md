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

**Prerequisite:** task 02 — `make monitoring-up` на VPS, bridge `:8080` healthy, ufw `8080/tcp`.

**Prod URL (Telegram через bridge):**

```
http://201.51.4.34:8080/webhook
```

Env на VPS: `TELEGRAM_ALARM_BOT_TOKEN`, `TELEGRAM_ALARM_CHAT_ID`, `GLITCHTIP_BRIDGE_BIND=8080:8080`.

---

## 4.1 Task 03 — настройка в GlitchTip UI (eu.glitchtip.com)

Повторить для **обоих** проектов: `diaai-backend` и `diaai-web`.

### Шаг A — Alert rule

1. **Organization `diaai` → Projects →** выберите проект
2. **Settings** → **Project Alerts**
3. **Create New Alert** (или редактировать существующее)
4. Условие (hosted GlitchTip — **quantity + timespan**):
   - **Quantity:** `1` event
   - **Timespan:** `1` minute
5. Save

### Шаг B — Webhook recipient (Telegram)

1. **Add An Alert Recipient**
2. Type: **Webhook** / **General (Slack-compatible)**
3. URL: `http://201.51.4.34:8080/webhook`  
   С secret: `http://201.51.4.34:8080/webhook?secret=YOUR_SECRET`
4. Submit

### Шаг C — Email (опционально, второй recipient)

```
http://201.51.4.34:8000/webhooks/glitchtip/email
```

См. [alerts-email.md](alerts-email.md).

### Шаг D — Удалить старый Telegram URL

Если был `http://201.51.4.34:8000/webhooks/glitchtip` — **удалите** или замените на `:8080/webhook`.

### GlitchTip UI (task 03) — два webhook recipient в одном alert rule

| Канал | URL | Куда |
|-------|-----|------|
| Telegram | `http://201.51.4.34:8080/webhook` | bridge → `@diaaialarm_bot` |
| Email | `http://201.51.4.34:8000/webhooks/glitchtip/email` | backend → Mail.ru SMTP |

Настроить для **diaai-backend** и **diaai-web**. Rule: **1 event / 1 minute**.

### Smoke после UI

```bash
TOKEN=$(grep ^GLITCHTIP_DEBUG_TOKEN= /opt/diaai/.env | cut -d= -f2)
curl -sf -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/glitchtip-test
curl -sf -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  http://127.0.0.1:3000/api/debug/glitchtip-test
# ≤1–2 min → Telegram + email (без ручного curl)
docker logs diaai-glitchtip-telegram-bridge-1 --since 5m | tail -20
docker logs diaai-backend-1 --since 5m | grep "POST /webhooks/glitchtip"
```

Ожидание: `165.227.159.10` (GlitchTip EU) → `POST /webhook` и `POST /webhooks/glitchtip/email`.

---

## 4.2 Ручная проверка bridge

```bash
curl -sf http://127.0.0.1:8080/health
curl -X POST http://127.0.0.1:8080/webhook \
  -H 'Content-Type: application/json' \
  -d '{"attachments":[{"title":"Test","title_link":"https://eu.glitchtip.com","text":"manual"}]}'
```

**Альтернатива — backend :8000:** `http://201.51.4.34:8000/webhooks/glitchtip`

**Fallback:** backend poller — `GLITCHTIP_API_TOKEN`, `GLITCHTIP_ORG=diaai` в `.env`.

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
