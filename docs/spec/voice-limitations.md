# Voice mode — ограничения и API

Опирается на [frontend-requirements.md](frontend-requirements.md) · [integrations.md](../integrations.md) · [api-contracts.md](../tech/api-contracts.md) · [frontend-contract.md](../api/frontend-contract.md) · [iteration-8 plan](../tasks/impl/frontend/iteration-8-voice-chat/plan.md)

---

## Выбор реализации (web)

| Режим | Когда | Технология |
|-------|-------|------------|
| **Primary** | Chrome, Edge (desktop) | Web Speech API (`SpeechRecognition`, `lang=ru-RU`) |
| **Fallback** | Firefox, Safari, iOS | `MediaRecorder` (до ~8 с) → batch POST transcribe |
| **TTS** | опционально, toggle | `speechSynthesis` (client-only) |

Mic скрыт, если ни Web Speech, ни MediaRecorder недоступны.

---

## Ограничения браузеров

| Браузер | STT (ввод) | TTS (озвучивание) | Примечание |
|---------|------------|-------------------|------------|
| Chrome / Edge (desktop) | Web Speech API | `speechSynthesis` | рекомендуемый smoke |
| Firefox | batch transcribe | частично | нет `SpeechRecognition` |
| Safari (desktop / iOS) | batch transcribe | частично | нужен HTTPS |
| Mobile Chrome | Web Speech (varies) | varies | проверять на устройстве |

**Требования:** HTTPS или `localhost`; разрешение микрофона.

**Fallback UX:** ошибка STT → `role="alert"`; текстовый input остаётся доступен.

**Язык:** `ru-RU` (Web Speech + Whisper backend).

---

## Передача аудио на backend

| Параметр | Значение iter 8 |
|----------|-----------------|
| Модель | **Batch** (не streaming) |
| Формат запроса | JSON `{ audio_base64, media_type }` |
| Max size | 5 MB decoded |
| Web запись | до ~8 с (`MediaRecorder`) |
| Telegram | полный voice file (ogg/opus) |

Streaming STT/TTS — **out of scope** (см. plan iter 8 §2).

---

## Согласование с API чата

Голос **не** меняет контракт history/send. После STT — обычный текстовый message.

| Действие | Web BFF | Backend | Body / query |
|----------|---------|---------|--------------|
| История | `GET /api/assistant/history` | `GET /v1/web/assistant/history` | `telegram_id`, pagination |
| Отправка | `POST /api/assistant/messages` | `POST /v1/assistant/messages` | `{ text }` (+ session→telegram_id) |
| STT (до send) | `POST /api/assistant/transcribe` | `POST /v1/media/transcribe` | `{ audio_base64, media_type }` |

В PostgreSQL: `request_type=text`, `content`=transcript. История FAB ↔ `/chat` без изменений (iter 5–6).

---

## Telegram bot

| Шаг | Действие |
|-----|----------|
| 1 | `F.voice` → `bot.get_file` → bytes |
| 2 | `POST /v1/media/transcribe` (`audio/ogg`) |
| 3 | `POST /v1/assistant/messages` с `text`=transcript |
| 4 | `message.answer(reply)` |

**Fallback:** «Не удалось распознать. Отправьте текстом.»

Bot не хранит audio; не вызывает OpenRouter напрямую.

---

## Backend STT

| Параметр | Значение |
|----------|----------|
| Endpoint | `POST /api/v1/media/transcribe` |
| Auth | Bearer `BACKEND_SERVICE_TOKEN` |
| Provider | OpenRouter Whisper (`STT_MODEL`, default `openai/whisper-large-v3`; JSON `input_audio`, не multipart) |
| Env | `OPENROUTER_API_KEY`, `STT_TIMEOUT_SECONDS` |

---

## Out of scope

- Streaming/chunked audio upload
- Streaming TTS от LLM
- Сохранение audio в БД / history
- Offline STT
