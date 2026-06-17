"use client";

import { AssistantChatProvider } from "@/components/assistant/assistant-chat-provider";

export function AssistantChatRoot({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AssistantChatProvider>{children}</AssistantChatProvider>;
}
