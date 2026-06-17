"use client";

import { createContext, useCallback, useContext, useState, type ReactNode } from "react";

import type {
  HistoryMessage,
  PaginatedHistory,
  SendMessageResponse,
} from "@/lib/types/assistant-chat";

const PAGE_SIZE = 50;

async function fetchHistoryPage(offset: number): Promise<PaginatedHistory> {
  const params = new URLSearchParams({
    limit: String(PAGE_SIZE),
    offset: String(offset),
  });
  const response = await fetch(`/api/assistant/history?${params}`);
  const body = (await response.json()) as PaginatedHistory & { error?: string };
  if (!response.ok) {
    throw new Error(body.error ?? "Не удалось загрузить историю");
  }
  return body;
}

async function postMessage(text: string): Promise<SendMessageResponse> {
  const response = await fetch("/api/assistant/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const body = (await response.json()) as SendMessageResponse & {
    error?: string;
  };
  if (!response.ok) {
    throw new Error(body.error ?? "Не удалось отправить сообщение");
  }
  return body;
}

export type AssistantChatState = {
  messages: HistoryMessage[];
  total: number;
  loading: boolean;
  loadingMore: boolean;
  sending: boolean;
  error: string | null;
  loaded: boolean;
  hasMore: boolean;
  loadHistory: () => Promise<void>;
  retryHistory: () => Promise<void>;
  loadMore: () => Promise<void>;
  sendMessage: (text: string) => Promise<void>;
};

const AssistantChatContext = createContext<AssistantChatState | null>(null);

function useAssistantChatState(): AssistantChatState {
  const [messages, setMessages] = useState<HistoryMessage[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);

  const loadHistory = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchHistoryPage(0);
      setMessages(data.items);
      setTotal(data.total);
      setLoaded(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  }, []);

  const retryHistory = useCallback(async () => {
    setLoaded(false);
    await loadHistory();
  }, [loadHistory]);

  const loadMore = useCallback(async () => {
    if (loadingMore || messages.length >= total) {
      return;
    }
    setLoadingMore(true);
    setError(null);
    try {
      const data = await fetchHistoryPage(messages.length);
      setMessages((prev) => [...prev, ...data.items]);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка загрузки");
    } finally {
      setLoadingMore(false);
    }
  }, [loadingMore, messages.length, total]);

  const sendMessage = useCallback(async (text: string) => {
    const optimisticId = `optimistic-${Date.now()}`;
    const optimisticUser: HistoryMessage = {
      id: optimisticId,
      role: "user",
      text,
      created_at: new Date().toISOString(),
    };

    setSending(true);
    setError(null);
    setMessages((prev) => [...prev, optimisticUser]);
    setTotal((prev) => prev + 2);

    try {
      const data = await postMessage(text);
      const now = new Date().toISOString();
      setMessages((prev) => {
        const withoutOptimistic = prev.filter((m) => m.id !== optimisticId);
        return [
          ...withoutOptimistic,
          {
            id: data.request_id,
            role: "user",
            text,
            created_at: now,
          },
          {
            id: `${data.request_id}-reply`,
            role: "assistant",
            text: data.reply,
            created_at: now,
          },
        ];
      });
      setLoaded(true);
    } catch (err) {
      setMessages((prev) => prev.filter((m) => m.id !== optimisticId));
      setTotal((prev) => Math.max(0, prev - 2));
      setError(err instanceof Error ? err.message : "Ошибка отправки");
    } finally {
      setSending(false);
    }
  }, []);

  const hasMore = messages.length < total;

  return {
    messages,
    total,
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
  };
}

export function AssistantChatProvider({ children }: { children: ReactNode }) {
  const value = useAssistantChatState();
  return (
    <AssistantChatContext.Provider value={value}>
      {children}
    </AssistantChatContext.Provider>
  );
}

export function useAssistantChat(): AssistantChatState {
  const context = useContext(AssistantChatContext);
  if (!context) {
    throw new Error("useAssistantChat must be used within AssistantChatProvider");
  }
  return context;
}
