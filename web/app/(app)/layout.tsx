import { redirect } from "next/navigation";

import { AppHeader } from "@/components/app-header";
import { AppSidebar } from "@/components/app-sidebar";
import { AssistantChatRoot } from "@/components/assistant/assistant-chat-root";
import { ChatFab } from "@/components/chat-fab";
import { getSession } from "@/lib/session";

export default async function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }

  return (
    <AssistantChatRoot>
      <div className="flex min-h-full flex-col">
        <AppHeader user={session} />
        <div className="flex flex-1">
          <AppSidebar role={session.role} />
          <main className="flex min-h-0 flex-1 flex-col p-6">{children}</main>
        </div>
        <ChatFab />
      </div>
    </AssistantChatRoot>
  );
}
