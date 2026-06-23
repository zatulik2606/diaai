import { NextResponse } from "next/server";

import { AuthError, transcribeAudio } from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export async function POST(request: Request) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: "Не авторизован" }, { status: 401 });
  }

  let body: { audio_base64?: string; media_type?: string };
  try {
    body = (await request.json()) as { audio_base64?: string; media_type?: string };
  } catch {
    return NextResponse.json({ error: "Неверный запрос" }, { status: 400 });
  }

  const audioBase64 = body.audio_base64?.trim() ?? "";
  if (!audioBase64) {
    return NextResponse.json({ error: "Пустое аудио" }, { status: 400 });
  }

  try {
    const data = await transcribeAudio(
      audioBase64,
      body.media_type?.trim() || "audio/webm",
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
