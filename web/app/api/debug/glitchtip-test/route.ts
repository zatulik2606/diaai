import * as Sentry from "@sentry/nextjs";
import { NextResponse } from "next/server";
import { notFound } from "next/navigation";

function verifyDebugToken(request: Request): NextResponse | null {
  const token = process.env.GLITCHTIP_DEBUG_TOKEN;
  if (!token) {
    notFound();
  }

  const authorization = request.headers.get("Authorization");
  if (
    !authorization?.startsWith("Bearer ") ||
    authorization.slice("Bearer ".length) !== token
  ) {
    return NextResponse.json({ detail: "Unauthorized" }, { status: 401 });
  }

  return null;
}

export async function GET(request: Request) {
  const authError = verifyDebugToken(request);
  if (authError) {
    return authError;
  }

  const dsn =
    process.env.GLITCHTIP_DSN ?? process.env.NEXT_PUBLIC_GLITCHTIP_DSN;
  if (!dsn) {
    return NextResponse.json(
      { detail: "GlitchTip is not configured" },
      { status: 503 },
    );
  }

  const eventId = Sentry.captureException(
    new Error("diaai glitchtip test: web api"),
  );
  await Sentry.flush(2000);
  return NextResponse.json({ ok: true, project: "diaai-web", eventId });
}
