"use client";

import { Loader2, Mic, MicOff, Send } from "lucide-react";
import { type FormEvent, useState } from "react";

import { useVoiceInput } from "@/hooks/use-voice-input";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type ChatInputProps = {
  onSend: (text: string) => Promise<void>;
  disabled?: boolean;
  sending?: boolean;
};

export function ChatInput({ onSend, disabled, sending }: ChatInputProps) {
  const [text, setText] = useState("");
  const [voiceError, setVoiceError] = useState<string | null>(null);

  const { isSupported, isListening, isProcessing, startListening } = useVoiceInput({
    onTranscript: (transcript) => {
      setVoiceError(null);
      setText(transcript);
    },
    onError: (message) => setVoiceError(message),
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const value = text.trim();
    if (!value || disabled || sending) {
      return;
    }
    setText("");
    setVoiceError(null);
    await onSend(value);
  }

  const inputDisabled = disabled || sending || isListening || isProcessing;

  return (
    <div className="flex flex-col gap-2 border-t border-border pt-4">
      {voiceError ? (
        <p className="text-sm text-destructive" role="alert">
          {voiceError}
        </p>
      ) : null}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Сообщение ассистенту…"
          disabled={inputDisabled}
          autoComplete="off"
          className="flex-1"
        />
        {isSupported ? (
          <Button
            type="button"
            size="icon"
            variant={isListening ? "default" : "outline"}
            disabled={inputDisabled}
            aria-label={isListening ? "Остановить запись" : "Голосовой ввод"}
            aria-pressed={isListening}
            onClick={() => startListening()}
          >
            {isProcessing ? (
              <Loader2 className="size-4 animate-spin" />
            ) : isListening ? (
              <MicOff className="size-4" />
            ) : (
              <Mic className="size-4" />
            )}
          </Button>
        ) : null}
        <Button
          type="submit"
          size="icon"
          disabled={inputDisabled || !text.trim()}
          aria-label="Отправить"
        >
          {sending ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <Send className="size-4" />
          )}
        </Button>
      </form>
    </div>
  );
}
