import { NextResponse } from "next/server";

import { AuthError, sendAssistantMessage } from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export async function POST(request: Request) {
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

  let body: { text?: string };
  try {
    body = (await request.json()) as { text?: string };
  } catch {
    return NextResponse.json({ error: "Неверный запрос" }, { status: 400 });
  }

  const text = body.text?.trim() ?? "";
  if (!text) {
    return NextResponse.json(
      { error: "Введите сообщение" },
      { status: 400 },
    );
  }

  try {
    const data = await sendAssistantMessage(session.telegram_id, text);
    return NextResponse.json(data);
  } catch (error) {
    if (error instanceof AuthError) {
      const message =
        error.status === 502 || error.status === 503
          ? "Ассистент временно недоступен"
          : error.message;
      return NextResponse.json({ error: message }, { status: error.status });
    }
    return NextResponse.json({ error: "Ошибка сервера" }, { status: 500 });
  }
}
