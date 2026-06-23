"use client";

export type VoiceInputMode = "webspeech" | "recorder" | "none";

export function getVoiceInputMode(): VoiceInputMode {
  if (typeof window === "undefined") {
    return "none";
  }
  const SpeechRecognition =
    window.SpeechRecognition ??
    (window as Window & { webkitSpeechRecognition?: typeof window.SpeechRecognition })
      .webkitSpeechRecognition;
  if (SpeechRecognition) {
    return "webspeech";
  }
  if (
    typeof MediaRecorder !== "undefined" &&
    typeof navigator.mediaDevices?.getUserMedia === "function"
  ) {
    return "recorder";
  }
  return "none";
}

export function isSpeechOutputSupported(): boolean {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}
