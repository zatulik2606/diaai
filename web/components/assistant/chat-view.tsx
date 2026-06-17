"use client";

import { AssistantChatPanel } from "@/components/assistant/assistant-chat-panel";

export function ChatView() {
  return (
    <div className="flex h-full flex-col gap-4">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Чат с ассистентом
        </h1>
        <p className="text-sm text-muted-foreground">
          Вопросы о питании, ХЕ и самоконтроле — та же история, что в FAB-виджете
        </p>
      </header>
      <AssistantChatPanel variant="page" active />
    </div>
  );
}
