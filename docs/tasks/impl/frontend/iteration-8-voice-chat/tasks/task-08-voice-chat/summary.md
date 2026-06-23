# Task 08: Summary

> **Статус:** ✅ Done

Итерация: [iteration-8-voice-chat](../../plan.md)

---

## Сделано

- Backend `POST /api/v1/media/transcribe` — OpenRouter JSON STT (`input_audio`)
- Bot `F.voice` → `transcribe_audio` → assistant
- Web: mic hook, TTS toggle, BFF transcribe fallback
- Docs: voice-limitations, integrations, api-contracts, openapi

## Затронутые файлы

| Область | Файлы |
|---------|-------|
| backend | `api/v1/media.py`, `services/transcribe_service.py`, `schemas/media.py`, `config.py` |
| bot | `handlers.py`, `backend_client.py` |
| web | `chat-input.tsx`, `assistant-chat-panel.tsx`, `hooks/use-voice-input.ts`, `hooks/use-speech-output.ts`, `app/api/assistant/transcribe/` |
| tests | `backend/tests/test_media_transcribe.py`, `tests/test_backend_client.py` |

## Отклонения

- STT через OpenRouter JSON API, не OpenAI multipart (см. [iteration summary](../../summary.md#отклонения-от-плана))

## Проблемы

- **502 на transcribe** при первом smoke — OpenRouter отклонял `multipart/form-data`; исправлено в `transcribe_service.py`, live smoke → 200.

## Проверки

```bash
make test && make lint && make web-lint && make web-build  # ✅
curl POST /api/v1/media/transcribe  # ✅ 200 (после фикса)
```
