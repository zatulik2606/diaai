# Task 03 — GlitchTip Alert receivers → webhook

## Цель

Новый issue в GlitchTip автоматически шлёт webhook на bridge → Telegram.

## Scope

**Только пользователь + docs.** Код репозитория не меняется (кроме уточнения checklist в docs при необходимости).

## Подготовка (пользователь)

Prerequisite: task 02 — bridge `:8080` доступен с интернета.

## Шаги (eu.glitchtip.com)

### Проект `diaai-backend`

1. **Projects** → `diaai-backend` → **Alerts** (или Project Settings → Alerts)
2. **Add Alert Recipient** → type **Webhook** (General / Slack-compatible)
3. URL:
   - без secret: `http://201.51.4.34:8080/webhook`
   - с secret: `http://201.51.4.34:8080/webhook?secret=YOUR_GLITCHTIP_WEBHOOK_SECRET`
4. Triggers: **New issue** (минимум); опционально regression
5. Save

### Проект `diaai-web`

Повторить с тем же webhook URL (один bridge на оба проекта) **или** отдельный recipient — на усмотрение.

## Smoke

1. Task 01: `curl` `/debug/glitchtip-test` (backend)
2. В GlitchTip — новый issue
3. Telegram — сообщение от `@diaaialarm_bot` без ручного `curl /webhook`

## Файлы (агент — docs only)

| Файл | Действие |
|------|----------|
| [`devops/glitchtip/alerts-telegram.md`](../../../../../../../devops/glitchtip/alerts-telegram.md) | уточнить шаги UI + ссылка на task 03 |
| [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) | §9 пункт 3 checklist |

## Definition of Done

**Пользователь:** issue из debug endpoint → Telegram alert.

## Skill

—
