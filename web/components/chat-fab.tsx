"use client";

import { MessageCircle } from "lucide-react";
import { useState } from "react";

import { AssistantChatPanel } from "@/components/assistant/assistant-chat-panel";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

export function ChatFab() {
  const [open, setOpen] = useState(false);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button
          size="icon"
          className="fixed bottom-6 right-6 z-50 size-14 rounded-full shadow-lg"
          aria-label="Открыть чат"
        >
          <MessageCircle className="size-6" />
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="flex w-full flex-col sm:max-w-[380px]">
        <SheetHeader>
          <SheetTitle>Чат с ассистентом</SheetTitle>
          <SheetDescription>
            Вопросы о питании, ХЕ и самоконтроле
          </SheetDescription>
        </SheetHeader>
        <AssistantChatPanel active={open} />
      </SheetContent>
    </Sheet>
  );
}
