"use client";

import { cn } from "@/lib/utils";
import type { HistoryMessage } from "@/lib/types/assistant-chat";

function formatTime(iso: string): string {
  try {
    return new Intl.DateTimeFormat("ru-RU", {
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(iso));
  } catch {
    return "";
  }
}

type ChatMessageProps = {
  message: HistoryMessage;
};

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex flex-col gap-1",
        isUser ? "items-end" : "items-start",
      )}
    >
      <div
        className={cn(
          "max-w-[85%] rounded-lg px-3 py-2 text-sm",
          isUser ? "bg-muted text-foreground" : "bg-card text-card-foreground",
        )}
      >
        <p className="whitespace-pre-wrap break-words">{message.text}</p>
      </div>
      <time
        className="text-xs text-muted-foreground"
        dateTime={message.created_at}
      >
        {formatTime(message.created_at)}
      </time>
    </div>
  );
}
