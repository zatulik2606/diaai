export type MessageRole = "user" | "assistant";

export type HistoryMessage = {
  id: string;
  role: MessageRole;
  text: string;
  created_at: string;
};

export type PaginatedHistory = {
  items: HistoryMessage[];
  total: number;
  limit: number;
  offset: number;
};

export type SendMessageResponse = {
  dialog_id: string;
  request_id: string;
  reply: string;
};
