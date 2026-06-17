"use client";

import { useEffect, useRef } from "react";

import { ChatMessage } from "@/components/assistant/chat-message";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { HistoryMessage } from "@/lib/types/assistant-chat";

type ChatMessageListProps = {
  messages: HistoryMessage[];
};

export function ChatMessageList({ messages }: ChatMessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
      <ScrollArea className="min-h-0 flex-1 pr-3">
      <div className="flex flex-col gap-4 pb-2">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
    </div>
  );
}
