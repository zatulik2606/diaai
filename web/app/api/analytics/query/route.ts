import { NextResponse } from "next/server";

import { AuthError, queryAnalytics } from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export async function POST(request: Request) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: "Не авторизован" }, { status: 401 });
  }
  if (session.telegram_id == null) {
    return NextResponse.json({ error: "Telegram ID не найден" }, { status: 400 });
  }

  let body: { question?: string };
  try {
    body = (await request.json()) as { question?: string };
  } catch {
    return NextResponse.json({ error: "Неверный запрос" }, { status: 400 });
  }

  const question = body.question?.trim() ?? "";
  if (!question) {
    return NextResponse.json({ error: "Введите вопрос" }, { status: 400 });
  }

  try {
    const data = await queryAnalytics(
      session.telegram_id,
      session.role,
      question,
    );
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
