import { ChatView } from "@/components/assistant/chat-view";
import { getSession } from "@/lib/session";

export default async function ChatPage() {
  const session = await getSession();
  if (session?.telegram_id == null) {
    throw new Error("У пользователя нет telegram_id");
  }

  return <ChatView />;
}
