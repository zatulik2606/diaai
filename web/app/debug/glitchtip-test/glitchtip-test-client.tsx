"use client";

import * as Sentry from "@sentry/nextjs";
import { useState, useTransition } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { sendServerGlitchTipTest } from "./actions";

export function GlitchTipTestClient() {
  const [message, setMessage] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();
  const [clientPending, setClientPending] = useState(false);

  async function sendClientTest() {
    setMessage(null);
    setClientPending(true);
    try {
      const eventId = Sentry.captureException(
        new Error("diaai glitchtip test: web client"),
      );
      await Sentry.flush(2000);
      setMessage(
        eventId
          ? `Клиент: event ${eventId} → проект diaai-web`
          : "Клиент: событие отправлено, но event id не получен",
      );
    } finally {
      setClientPending(false);
    }
  }

  function sendServerTest() {
    setMessage(null);
    startTransition(async () => {
      const result = await sendServerGlitchTipTest();
      if (result.ok) {
        setMessage(
          result.eventId
            ? `Сервер: event ${result.eventId} → проект diaai-web`
            : "Сервер: событие отправлено, но event id не получен",
        );
        return;
      }
      setMessage(result.error ?? "Не удалось отправить событие.");
    });
  }

  return (
    <div className="flex min-h-full items-center justify-center p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>GlitchTip smoke test</CardTitle>
          <CardDescription>
            Dev-only. Ищите issues в проекте{" "}
            <code className="font-mono">diaai-web</code> на eu.glitchtip.com
            (фильтр environment: development).
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <Button
            type="button"
            onClick={sendClientTest}
            disabled={pending || clientPending}
          >
            {clientPending ? "Отправка…" : "Клиентская ошибка"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={sendServerTest}
            disabled={pending || clientPending}
          >
            {pending ? "Отправка…" : "Серверная ошибка"}
          </Button>
          {message ? (
            <p className="text-sm text-muted-foreground">{message}</p>
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}
