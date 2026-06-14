"use client";

import { MessageCircle } from "lucide-react";

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
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          size="icon"
          className="fixed bottom-6 right-6 z-50 size-14 rounded-full shadow-lg"
          aria-label="Открыть чат"
        >
          <MessageCircle className="size-6" />
        </Button>
      </SheetTrigger>
      <SheetContent side="right">
        <SheetHeader>
          <SheetTitle>Чат с ассистентом</SheetTitle>
          <SheetDescription>
            Полноценный чат — iter 5. История и отправка сообщений появятся позже.
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  );
}
