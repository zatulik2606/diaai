"use client";

import { Loader2, Send } from "lucide-react";
import { type FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type ChatInputProps = {
  onSend: (text: string) => Promise<void>;
  disabled?: boolean;
  sending?: boolean;
};

export function ChatInput({ onSend, disabled, sending }: ChatInputProps) {
  const [text, setText] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const value = text.trim();
    if (!value || disabled || sending) {
      return;
    }
    setText("");
    await onSend(value);
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 border-t border-border pt-4">
      <Input
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Сообщение ассистенту…"
        disabled={disabled || sending}
        autoComplete="off"
        className="flex-1"
      />
      <Button
        type="submit"
        size="icon"
        disabled={disabled || sending || !text.trim()}
        aria-label="Отправить"
      >
        {sending ? (
          <Loader2 className="size-4 animate-spin" />
        ) : (
          <Send className="size-4" />
        )}
      </Button>
    </form>
  );
}
