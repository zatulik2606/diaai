# Итерация frontend 8: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md) · [voice-limitations.md](../../../../spec/voice-limitations.md)

---

## Сделано

### Task-08: Голосовой режим ✅

**Backend**
- `POST /api/v1/media/transcribe` — OpenRouter Whisper (JSON audio API)
- `TranscribeService` (`httpx`), schemas, tests (`test_media_transcribe.py`)
- Env: `STT_MODEL` (default `openai/whisper-large-v3`), `STT_TIMEOUT_SECONDS`

**Bot**
- `F.voice` handler → download OGG → transcribe → `send_assistant_message`
- `backend_client.transcribe_audio`

**Web**
- `use-voice-input` — Web Speech API (primary) + MediaRecorder → BFF (fallback)
- `use-speech-output` — TTS toggle (`speechSynthesis`)
- `ChatInput` mic button; BFF `POST /api/assistant/transcribe`

**Docs**
- [voice-limitations.md](../../../../spec/voice-limitations.md)
- integrations, api-contracts, openapi, tasklist-bot iter 4

| Компонент | Путь |
|-----------|------|
| STT API | `backend/api/v1/media.py` |
| STT service | `backend/services/transcribe_service.py` |
| Voice hook | `web/hooks/use-voice-input.ts` |
| Mic UI | `web/components/assistant/chat-input.tsx` |
| Bot voice | `src/diaai/handlers.py` |

## Ценность

Голос как канал ввода D2 без изменения assistant send/history API; единый STT на backend для bot и web fallback.

## Отклонения от плана

| План | Факт |
|------|------|
| Whisper via OpenRouter (детали протокола не зафиксированы) | OpenRouter **не** принимает OpenAI multipart STT; реализован JSON endpoint `POST …/audio/transcriptions` с `input_audio: { data, format }` |
| Streaming STT | Сознательно out of scope — batch достаточен для MVP ([plan §2](plan.md)) |

**Post-review fix:** первоначальная реализация через `openai` client → 502 `invalid content-type: multipart/form-data`; исправлено в `TranscribeService` до закрытия итерации.

## Проблемы и решения

| Проблема | Решение |
|----------|---------|
| Bot voice → 502 на `/media/transcribe` | Переход на OpenRouter JSON STT API; модель `openai/whisper-large-v3` |
| Web Speech в Safari нестабилен | Документировано в voice-limitations; fallback — MediaRecorder → backend |

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| `make test` (74) | ✅ |
| `make lint` | ✅ |
| `make web-lint && make web-build` | ✅ |
| `POST /api/v1/media/transcribe` (live) | ✅ 200 |
| BFF `/api/assistant/transcribe` | ✅ (proxy) |

## User-check

```bash
make db-reset && make backend-run && make web-dev
# ivan_p → /chat → mic → текст в поле → send
make run  # Telegram voice → transcribe → ответ ассистента
```

После фикса STT: повторная отправка voice в Telegram — ожидается roundtrip без 502 (backend с актуальным кодом).

## Следующий шаг

[iteration-9-text-to-sql](../iteration-9-text-to-sql/plan.md)
