"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { getVoiceInputMode, type VoiceInputMode } from "@/lib/voice-support";

type UseVoiceInputOptions = {
  onTranscript: (text: string) => void;
  onError?: (message: string) => void;
  lang?: string;
};

type VoiceInputState = "idle" | "listening" | "processing";

async function transcribeBlob(blob: Blob): Promise<string> {
  const buffer = await blob.arrayBuffer();
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 1) {
    binary += String.fromCharCode(bytes[i] ?? 0);
  }
  const audioBase64 = btoa(binary);
  const response = await fetch("/api/assistant/transcribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      audio_base64: audioBase64,
      media_type: blob.type || "audio/webm",
    }),
  });
  const body = (await response.json()) as { text?: string; error?: string };
  if (!response.ok) {
    throw new Error(body.error ?? "Не удалось распознать речь");
  }
  const text = body.text?.trim();
  if (!text) {
    throw new Error("Не удалось распознать речь");
  }
  return text;
}

export function useVoiceInput({
  onTranscript,
  onError,
  lang = "ru-RU",
}: UseVoiceInputOptions) {
  const [state, setState] = useState<VoiceInputState>("idle");
  const [mode] = useState<VoiceInputMode>(() => getVoiceInputMode());
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  const stopMediaStream = useCallback(() => {
    mediaStreamRef.current?.getTracks().forEach((track) => track.stop());
    mediaStreamRef.current = null;
  }, []);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    stopMediaStream();
    setState("idle");
  }, [stopMediaStream]);

  const startRecorder = useCallback(async () => {
    setState("listening");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      const chunks: Blob[] = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      recorder.onstop = () => {
        stopMediaStream();
        void (async () => {
          setState("processing");
          try {
            const blob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
            const text = await transcribeBlob(blob);
            onTranscript(text);
          } catch (err) {
            onError?.(err instanceof Error ? err.message : "Ошибка распознавания");
          } finally {
            setState("idle");
          }
        })();
      };

      recorder.start();
      window.setTimeout(() => {
        if (recorder.state === "recording") {
          recorder.stop();
        }
      }, 8000);
    } catch {
      stopMediaStream();
      setState("idle");
      onError?.("Нет доступа к микрофону");
    }
  }, [onError, onTranscript, stopMediaStream]);

  const startWebSpeech = useCallback(() => {
    const SpeechRecognitionCtor =
      window.SpeechRecognition ??
      (window as Window & { webkitSpeechRecognition?: typeof window.SpeechRecognition })
        .webkitSpeechRecognition;

    if (!SpeechRecognitionCtor) {
      onError?.("Распознавание речи не поддерживается");
      return;
    }

    const recognition = new SpeechRecognitionCtor();
    recognition.lang = lang;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognitionRef.current = recognition;

    recognition.onstart = () => setState("listening");
    recognition.onend = () => setState("idle");
    recognition.onerror = () => {
      setState("idle");
      onError?.("Не удалось распознать — введите текст");
    };
    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0]?.[0]?.transcript?.trim();
      if (transcript) {
        onTranscript(transcript);
      } else {
        onError?.("Не удалось распознать — введите текст");
      }
    };

    recognition.start();
  }, [lang, onError, onTranscript]);

  const startListening = useCallback(() => {
    if (state !== "idle") {
      stopListening();
      return;
    }
    if (mode === "webspeech") {
      startWebSpeech();
      return;
    }
    if (mode === "recorder") {
      void startRecorder();
      return;
    }
    onError?.("Голосовой ввод недоступен в этом браузере");
  }, [mode, onError, startRecorder, startWebSpeech, state, stopListening]);

  useEffect(() => {
    return () => {
      recognitionRef.current?.stop();
      stopMediaStream();
    };
  }, [stopMediaStream]);

  return {
    mode,
    state,
    isSupported: mode !== "none",
    isListening: state === "listening",
    isProcessing: state === "processing",
    startListening,
    stopListening,
  };
}
