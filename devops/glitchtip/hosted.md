# GlitchTip hosted (SaaS)

Облачный GlitchTip без своего VPS. SDK — `sentry-sdk` / `@sentry/nextjs`, env — `GLITCHTIP_*`.

Связь: [README.md](README.md) · self-hosted Timeweb: [timeweb-deploy.md](timeweb-deploy.md)

---

## US vs EU

| Instance | URL | Регион | Для diaai (РФ) |
|----------|-----|--------|----------------|
| **EU** | [eu.glitchtip.com](https://eu.glitchtip.com) | Frankfurt, DE | **рекомендуется** |
| US | [app.glitchtip.com](https://app.glitchtip.com) | NYC, US | может быть медленнее / нестабильнее |

Данные US и EU **не синхронизируются** — отдельная регистрация на каждый instance.

Pricing: [glitchtip.com/pricing](https://glitchtip.com/pricing) — Free 1000 events/mo, unlimited projects.

---

## Проверка доступности (2026-06)

С dev-машины (curl, timeout 15s):

| URL | HTTP | Примечание |
|-----|------|------------|
| `https://eu.glitchtip.com/` | **200** | ~0.4 s |
| `https://app.glitchtip.com/` | 200 / timeout | US instance нестабилен из некоторых сетей |
| `https://glitchtip.com/` | **200** | маркeting site |

**Вывод:** внешний GlitchTip **можно использовать**; для РФ/ЕС — **eu.glitchtip.com**.

---

## Быстрый старт

1. [eu.glitchtip.com](https://eu.glitchtip.com) → **Sign Up**
2. Create organization **`diaai`**
3. **Projects → Create**
   - `diaai-backend` — Python / FastAPI
   - `diaai-web` — JavaScript / Next.js
4. **Client Keys (DSN)** — скопировать оба

---

## DSN в diaai

```bash
# /opt/diaai/.env на prod (DSN с eu.glitchtip.com)
GLITCHTIP_DSN=https://xxx@o....eu.glitchtip.com/...
GLITCHTIP_WEB_DSN=https://yyy@o....eu.glitchtip.com/...
NEXT_PUBLIC_GLITCHTIP_DSN=https://yyy@o....eu.glitchtip.com/...
GLITCHTIP_ENVIRONMENT=production
GLITCHTIP_TRACES_SAMPLE_RATE=0.1
GLITCHTIP_URL=https://eu.glitchtip.com
```

`web/.env.local` — те же DSN для `pnpm dev`.

После `NEXT_PUBLIC_*` — **rebuild web** (Docker/CD).

Пустой DSN — мониторинг выключен.

---

## Hosted vs self-hosted Timeweb

| | Hosted EU | Self-hosted VPS |
|--|-----------|---------------|
| VPS | не нужен | ≥ 2 GB Timeweb |
| Оплата | Free / $15+ | только VPS |
| Доступ из РФ | ✅ eu.glitchtip.com | ✅ свой IP |
| Данные | Frankfurt (GlitchTip) | ваш сервер |

Для MVP без железа — **hosted EU**. Для полного контроля данных — [timeweb-deploy.md](timeweb-deploy.md).

---

## Проверка ingest

После DSN в backend:

```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_DSN")
sentry_sdk.capture_message("diaai hosted glitchtip test")
```

Issue должен появиться в UI eu.glitchtip.com в течение минуты.
