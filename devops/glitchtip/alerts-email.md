# GlitchTip → Email alerts (SMTP bridge)

На **hosted GlitchTip EU** нельзя указать свой SMTP — встроенные email-алерты не работают. Bridge принимает Slack-compatible webhook от GlitchTip и шлёт письмо через **ваш SMTP**.

Связь: [alerts-telegram.md](alerts-telegram.md) · [hosted.md](hosted.md) · ADR: [adr-005-observability.md](../../docs/adr/adr-005-observability.md)

---

## 1. Переменные окружения

Корневой `.env` (не в git):

```bash
# Куда слать алерты
GLITCHTIP_ALERT_EMAIL_TO=you@example.com
# От кого (если пусто — SMTP_USER)
GLITCHTIP_ALERT_EMAIL_FROM=diaai-alerts@example.com

# SMTP (Gmail app password, Yandex, Mailgun, …)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=true
```

| Variable | Обязательна | Описание |
|----------|-------------|----------|
| `GLITCHTIP_ALERT_EMAIL_TO` | да | получатель алертов |
| `SMTP_HOST` | да | хост SMTP |
| `SMTP_PORT` | нет | по умолчанию `587` |
| `SMTP_USER` / `SMTP_PASSWORD` | обычно да | auth |
| `GLITCHTIP_ALERT_EMAIL_FROM` | нет | From; иначе `SMTP_USER` |
| `GLITCHTIP_WEBHOOK_SECRET` | нет | `?secret=` или header |

---

## 2. Prod (рекомендуется): backend :8000

Порт уже открыт на VPS. Отдельный webhook URL **только для email**:

```
http://201.51.4.34:8000/webhooks/glitchtip/email
```

Telegram остаётся на bridge `:8080/webhook` — в GlitchTip **два** webhook recipient в одном alert rule:

| Recipient | URL |
|-----------|-----|
| Telegram | `http://201.51.4.34:8080/webhook` |
| Email | `http://201.51.4.34:8000/webhooks/glitchtip/email` |

### GlitchTip UI

1. **Projects → Settings → Project Alerts** (правило с `1 event / 1 min`)
2. **+ Add An Alert Recipient → Webhook**
3. URL: `http://201.51.4.34:8000/webhooks/glitchtip/email`
4. **Submit** — для **diaai-backend** и **diaai-web**

### Smoke

```bash
curl -X POST http://201.51.4.34:8000/webhooks/glitchtip/email \
  -H 'Content-Type: application/json' \
  -d '{"attachments":[{"title":"Test email bridge","title_link":"https://eu.glitchtip.com","text":"manual check"}]}'
```

Ожидание: письмо на `GLITCHTIP_ALERT_EMAIL_TO`.

---

## 3. Локально: контейнер (profile monitoring)

```bash
make monitoring-up
curl -sf http://127.0.0.1:8081/health
```

Webhook URL для GlitchTip (если туннель/ngrok): `http://HOST:8081/webhook`

---

## 4. Gmail (пример)

1. Google Account → Security → 2FA → **App passwords**
2. `.env`:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
GLITCHTIP_ALERT_EMAIL_FROM=your@gmail.com
GLITCHTIP_ALERT_EMAIL_TO=your@gmail.com
```

---

## 5. Mail.ru (рекомендуется для РФ)

Официально: [help.mail.ru — вход из почтовой программы](https://help.mail.ru/mail/login/mailer/)

1. Ящик `@mail.ru` (или `@inbox.ru`, `@bk.ru` — тот же SMTP)
2. **Настройки → Все настройки → Безопасность → [Пароли для внешних приложений](https://help.mail.ru/mail/faq/password/external/)**
3. Создать → тип **«Только отправка писем»** / SMTP → скопировать пароль
4. К ящику должен быть **привязан телефон** (+7)

`.env`:

```bash
SMTP_HOST=smtp.mail.ru
SMTP_PORT=465
SMTP_USER=you@mail.ru
SMTP_PASSWORD=пароль_для_внешнего_приложения
SMTP_USE_TLS=false
GLITCHTIP_ALERT_EMAIL_FROM=you@mail.ru
GLITCHTIP_ALERT_EMAIL_TO=you@mail.ru
```

| Параметр | Значение |
|----------|----------|
| SMTP | `smtp.mail.ru:465` SSL |
| Логин | **полный** email (`user@mail.ru`) |
| Пароль | **не** от аккаунта — только «для внешнего приложения» |

Получать алерты можно на **другой** адрес: `GLITCHTIP_ALERT_EMAIL_TO=you@gmail.com`.

---

## 6. Yandex

1. [id.yandex.ru/security](https://id.yandex.ru/security) → **Пароли приложений**
2. IMAP/SMTP в [mail.yandex.ru](https://mail.yandex.ru) → **Почтовые программы**
3. `.env`: `smtp.yandex.ru`, порт `465` или `587` — см. таблицу ниже

| Порт | `.env` |
|------|--------|
| **465** | `SMTP_PORT=465`, `SMTP_USE_TLS=false` |
| **587** | `SMTP_PORT=587`, `SMTP_USE_TLS=true` |

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| `503 Not configured` | задайте `GLITCHTIP_ALERT_EMAIL_TO` + `SMTP_HOST` на VPS, перезапустите backend |
| `502 Email delivery failed` | проверьте SMTP creds, TLS, порт 587 |
| GlitchTip не шлёт POST | см. [alerts-telegram.md §4](alerts-telegram.md) — worker hosted; Test API или poller |
| Письмо в spam | SPF/DKIM у домена From; для Gmail — From = тот же аккаунт |

---

## Безопасность

- SMTP пароль только в `.env` / GitHub secrets, не в git
- Не логировать тело писем и webhook payload в prod
