# Task 08: Голосовой режим чата

Итерация: [iteration-8-voice-chat](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Web voice UI + backend batch transcribe + bot voice handler. После STT — **тот же** chat API, что в iter 5.

---

## 1. Выбор реализации (web)

| # | Решение | Файлы |
|---|---------|-------|
| 1 | Primary STT: **Web Speech API** (`ru-RU`) | `web/hooks/use-voice-input.ts`, `web/lib/voice-support.ts` |
| 2 | Fallback: **MediaRecorder** (≤8 s) → BFF → backend | `use-voice-input.ts`, `web/app/api/assistant/transcribe/route.ts` |
| 3 | TTS: **speechSynthesis**, toggle | `web/hooks/use-speech-output.ts`, `assistant-chat-panel.tsx` |
| 4 | Preview transcript в input, send вручную | `chat-input.tsx` → `sendMessage(text)` |

Отклонённые варианты: только cloud STT в Chrome; streaming upload — см. [plan iter 8 §2](../../plan.md).

---

## 2. Ограничения браузеров

→ [voice-limitations.md](../../../../../spec/voice-limitations.md)

| Браузер | STT | TTS |
|---------|-----|-----|
| Chrome / Edge | Web Speech API | ✅ |
| Firefox / Safari | batch transcribe | частично |

Fallback UI: `role="alert"`, текст «Не удалось распознать — введите текст»; mic скрыт если `getVoiceInputMode() === "none"`.

---

## 3. Аудио на backend (batch, не streaming)

- [x] `POST /api/v1/media/transcribe` — `{ audio_base64, media_type }` → `{ text }`
- [x] Max 5 MB decoded; Whisper via OpenRouter (`STT_MODEL`)
- [x] **Не** streaming/chunked — см. обоснование в [plan §2](../../plan.md)

BFF proxy: `POST /api/assistant/transcribe` → `backend-client.transcribeAudio()`.

---

## 4. Согласование с API чата

| Endpoint | Роль в voice flow | Изменён? |
|----------|-------------------|----------|
| `GET /api/assistant/history` | история без audio | нет |
| `POST /api/assistant/messages` | send после STT (`text` only) | нет |
| `POST /api/assistant/transcribe` | STT до send | **новый BFF** |
| `POST /v1/media/transcribe` | STT backend | **новый** |

`AssistantChatProvider` / optimistic UI — без изменений; голос только заполняет `text`.

---

## 5. Telegram-бот

- [x] `@router.message(F.voice)` — download ogg → base64
- [x] `backend_client.transcribe_audio()` → `send_assistant_message(text=...)`
- [x] Fallback user message при ошибке STT
- [x] Tests `tests/test_backend_client.py`; [tasklist-bot.md](../../../../tasklist-bot.md) iter 4

Bot не меняет формат ответа пользователю — текст, как у `text_handler`.

---

## Состав работ (чеклист)

### A. Backend ✅

- [x] `TranscribeService`, `media.py`, schemas, tests
- [x] openapi, api-contracts, integrations

### B. Bot ✅

- [x] voice handler + transcribe client

### C. Web ✅

- [x] hooks, mic UI, BFF transcribe, TTS toggle

### D. Docs ✅

- [x] voice-limitations, frontend-requirements зона 3

## Затронутые файлы

| Область | Файлы |
|---------|-------|
| backend | `api/v1/media.py`, `services/transcribe_service.py`, `schemas/media.py` |
| bot | `handlers.py`, `backend_client.py` |
| web | `chat-input.tsx`, `hooks/use-voice-*.ts`, `app/api/assistant/transcribe/` |

## Проверка

```bash
make test && make web-lint && make web-build
# web: mic → preview → send → reply
# bot: voice → reply
```

## Definition of Done

- [x] Решения §1–§5 зафиксированы в plan + voice-limitations
- [x] Chat send/history без изменений контракта
- [x] Web + bot smoke
