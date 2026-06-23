"use client";

import { useCallback, useEffect, useState } from "react";

import { isSpeechOutputSupported } from "@/lib/voice-support";

export function useSpeechOutput() {
  const [enabled, setEnabled] = useState(false);
  const supported = isSpeechOutputSupported();

  const speak = useCallback(
    (text: string) => {
      if (!enabled || !supported || !text.trim()) {
        return;
      }
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "ru-RU";
      const voices = window.speechSynthesis.getVoices();
      const ruVoice = voices.find((voice) => voice.lang.toLowerCase().startsWith("ru"));
      if (ruVoice) {
        utterance.voice = ruVoice;
      }
      window.speechSynthesis.speak(utterance);
    },
    [enabled, supported],
  );

  useEffect(() => {
    if (!supported) {
      return;
    }
    const loadVoices = () => {
      window.speechSynthesis.getVoices();
    };
    loadVoices();
    window.speechSynthesis.addEventListener("voiceschanged", loadVoices);
    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", loadVoices);
      window.speechSynthesis.cancel();
    };
  }, [supported]);

  return {
    enabled,
    setEnabled,
    supported,
    speak,
  };
}
