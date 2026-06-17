import { NextResponse } from "next/server";

import {
  AuthError,
  fetchAssistantHistory,
} from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export async function GET(request: Request) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: "Не авторизован" }, { status: 401 });
  }
  if (session.telegram_id == null) {
    return NextResponse.json(
      { error: "У пользователя нет telegram_id" },
      { status: 400 },
    );
  }

  const { searchParams } = new URL(request.url);
  const limit = Number(searchParams.get("limit") ?? "50");
  const offset = Number(searchParams.get("offset") ?? "0");

  try {
    const data = await fetchAssistantHistory(session.telegram_id, {
      limit: Number.isFinite(limit) ? limit : 50,
      offset: Number.isFinite(offset) ? offset : 0,
    });
    return NextResponse.json(data);
  } catch (error) {
    if (error instanceof AuthError) {
      const message =
        error.status === 503
          ? "Сервис недоступен. Запустите backend."
          : error.message;
      return NextResponse.json({ error: message }, { status: error.status });
    }
    return NextResponse.json({ error: "Ошибка сервера" }, { status: 500 });
  }
}
