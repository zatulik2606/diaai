"use client";

import { Loader2, Volume2 } from "lucide-react";
import { useEffect, useRef } from "react";

import { useAssistantChat } from "@/components/assistant/assistant-chat-provider";
import { ChatInput } from "@/components/assistant/chat-input";
import { ChatMessageList } from "@/components/assistant/chat-message-list";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useSpeechOutput } from "@/hooks/use-speech-output";
import { cn } from "@/lib/utils";

type AssistantChatPanelProps = {
  active?: boolean;
  variant?: "fab" | "page";
};

export function AssistantChatPanel({
  active = true,
  variant = "fab",
}: AssistantChatPanelProps) {
  const {
    messages,
    loading,
    loadingMore,
    sending,
    error,
    loaded,
    hasMore,
    loadHistory,
    retryHistory,
    loadMore,
    sendMessage,
  } = useAssistantChat();
  const { enabled: ttsEnabled, setEnabled: setTtsEnabled, supported: ttsSupported, speak } =
    useSpeechOutput();
  const wasSendingRef = useRef(false);

  useEffect(() => {
    if (active && !loaded && !loading) {
      void loadHistory();
    }
  }, [active, loaded, loading, loadHistory]);

  useEffect(() => {
    if (wasSendingRef.current && !sending && ttsEnabled) {
      const last = messages[messages.length - 1];
      if (last?.role === "assistant") {
        speak(last.text);
      }
    }
    wasSendingRef.current = sending;
  }, [messages, sending, speak, ttsEnabled]);

  const historyFailed = Boolean(error && !loaded && !loading);

  return (
    <div
      className={cn(
        "flex min-h-0 flex-col gap-4",
        variant === "page"
          ? "h-[calc(100vh-11rem)] min-h-[400px] flex-1"
          : "h-[calc(100vh-8rem)] min-h-[320px]",
      )}
    >
      {loading ? (
        <div className="flex flex-1 flex-col gap-3" aria-busy="true">
          <Skeleton className="h-12 w-3/4" />
          <Skeleton className="h-12 w-2/3 self-end" />
          <Skeleton className="h-12 w-4/5" />
        </div>
      ) : historyFailed ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-3 text-center">
          <p className="text-sm text-destructive" role="alert">
            {error}
          </p>
          <Button type="button" variant="outline" size="sm" onClick={() => void retryHistory()}>
            Повторить
          </Button>
        </div>
      ) : messages.length === 0 ? (
        <p className="flex flex-1 items-center justify-center text-sm text-muted-foreground">
          Напишите ассистенту — он поможет с вопросами о питании и диабете.
        </p>
      ) : (
        <ChatMessageList messages={messages} />
      )}

      {hasMore && !loading && !historyFailed ? (
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="shrink-0"
          onClick={() => void loadMore()}
          disabled={loadingMore}
        >
          {loadingMore ? (
            <>
              <Loader2 className="mr-2 size-4 animate-spin" />
              Загрузка…
            </>
          ) : (
            "Загрузить ещё"
          )}
        </Button>
      ) : null}

      {error && loaded && !sending ? (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      ) : null}

      {ttsSupported ? (
        <Button
          type="button"
          variant={ttsEnabled ? "outline" : "ghost"}
          size="sm"
          className="self-start"
          aria-pressed={ttsEnabled}
          onClick={() => setTtsEnabled((value) => !value)}
        >
          <Volume2 className="mr-2 size-4" />
          {ttsEnabled ? "Озвучивание включено" : "Озвучивать ответы"}
        </Button>
      ) : null}

      <ChatInput
        onSend={sendMessage}
        disabled={loading || historyFailed}
        sending={sending}
      />
    </div>
  );
}
