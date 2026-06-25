"use server";

import * as Sentry from "@sentry/nextjs";

export async function sendServerGlitchTipTest(): Promise<{
  ok: boolean;
  eventId?: string;
  error?: string;
}> {
  if (!process.env.GLITCHTIP_DEBUG_TOKEN) {
    return { ok: false, error: "Debug route is disabled" };
  }

  const dsn =
    process.env.GLITCHTIP_DSN ?? process.env.NEXT_PUBLIC_GLITCHTIP_DSN;
  if (!dsn) {
    return { ok: false, error: "GlitchTip is not configured" };
  }

  const eventId = Sentry.captureException(
    new Error("diaai glitchtip test: web server"),
  );
  await Sentry.flush(2000);
  return { ok: true, eventId: eventId ?? undefined };
}
