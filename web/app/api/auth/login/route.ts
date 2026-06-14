import { NextResponse } from "next/server";

import {
  AuthError,
  normalizeUsername,
  resolveUsername,
} from "@/lib/backend-client";
import { setSession } from "@/lib/session";

export async function POST(request: Request) {
  let body: { username?: string };
  try {
    body = (await request.json()) as { username?: string };
  } catch {
    return NextResponse.json({ error: "Неверный запрос" }, { status: 400 });
  }

  const username = normalizeUsername(body.username ?? "");
  if (!username) {
    return NextResponse.json({ error: "Введите username" }, { status: 400 });
  }

  try {
    const user = await resolveUsername(username);
    await setSession(user);
    return NextResponse.json({ ok: true, role: user.role });
  } catch (error) {
    if (error instanceof AuthError) {
      return NextResponse.json({ error: error.message }, { status: error.status });
    }
    return NextResponse.json({ error: "Ошибка сервера" }, { status: 500 });
  }
}
