import type {
  PaginatedHistory,
  SendMessageResponse,
} from "@/lib/types/assistant-chat";
import type { AnalyticsQueryResponse } from "@/lib/types/analytics-query";
import type { SessionUser } from "@/lib/types/auth";
import type {
  LeaderboardQuery,
  LeaderboardResponse,
} from "@/lib/types/leaderboard";
import type {
  MatrixPeriod,
  PatientDashboardActivity,
  PatientDashboardData,
  PatientDashboardSummary,
  PatientProgressMatrix,
  PaginatedPatientQuestions,
  PaginatedPatientSubmissions,
} from "@/lib/types/patient-dashboard";

export class AuthError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "AuthError";
  }
}

function backendConfig() {
  const baseUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";
  const token = process.env.BACKEND_SERVICE_TOKEN;
  if (!token) {
    throw new AuthError("BACKEND_SERVICE_TOKEN не настроен", 500);
  }
  return { baseUrl, token };
}

export async function resolveUsername(username: string): Promise<SessionUser> {
  const { baseUrl, token } = backendConfig();
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/v1/web/auth/resolve`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username }),
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }

  if (response.status === 404 || response.status === 401) {
    throw new AuthError("Пользователь не найден", 404);
  }
  if (!response.ok) {
    throw new AuthError("Ошибка авторизации", response.status);
  }

  const data = (await response.json()) as SessionUser;
  return data;
}

export function normalizeUsername(raw: string): string {
  return raw.trim().replace(/^@/, "").toLowerCase();
}

async function patientFetch<T>(
  path: string,
  telegramId: number,
  params: Record<string, string> = {},
): Promise<T> {
  const { baseUrl, token } = backendConfig();
  const query = new URLSearchParams({
    patient_telegram_id: String(telegramId),
    ...params,
  });
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}?${query}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось загрузить данные dashboard", response.status);
  }
  return (await response.json()) as T;
}

export async function fetchPatientSummary(
  telegramId: number,
  periodDays = 7,
): Promise<PatientDashboardSummary> {
  return patientFetch<PatientDashboardSummary>(
    "/api/v1/web/patient/dashboard/summary",
    telegramId,
    { period_days: String(periodDays) },
  );
}

export async function fetchPatientActivity(
  telegramId: number,
  days = 14,
): Promise<PatientDashboardActivity> {
  return patientFetch<PatientDashboardActivity>(
    "/api/v1/web/patient/dashboard/activity",
    telegramId,
    { days: String(days) },
  );
}

export async function fetchPatientQuestions(
  telegramId: number,
  limit = 10,
  offset = 0,
): Promise<PaginatedPatientQuestions> {
  return patientFetch<PaginatedPatientQuestions>(
    "/api/v1/web/patient/dashboard/questions",
    telegramId,
    { limit: String(limit), offset: String(offset) },
  );
}

export async function fetchPatientSubmissions(
  telegramId: number,
  limit = 10,
  offset = 0,
): Promise<PaginatedPatientSubmissions> {
  return patientFetch<PaginatedPatientSubmissions>(
    "/api/v1/web/patient/dashboard/submissions",
    telegramId,
    { limit: String(limit), offset: String(offset) },
  );
}

export async function fetchPatientProgressMatrix(
  telegramId: number,
  period: MatrixPeriod = "week",
): Promise<PatientProgressMatrix> {
  return patientFetch<PatientProgressMatrix>(
    "/api/v1/web/patient/dashboard/progress-matrix",
    telegramId,
    { period },
  );
}

export async function fetchPatientDashboard(
  telegramId: number,
): Promise<PatientDashboardData> {
  const [summary, activity, questions, submissions, matrix] = await Promise.all([
    fetchPatientSummary(telegramId),
    fetchPatientActivity(telegramId),
    fetchPatientQuestions(telegramId),
    fetchPatientSubmissions(telegramId),
    fetchPatientProgressMatrix(telegramId),
  ]);
  return { summary, activity, questions, submissions, matrix };
}

async function doctorFetch<T>(
  path: string,
  telegramId: number,
  params: Record<string, string> = {},
): Promise<T> {
  const { baseUrl, token } = backendConfig();
  const query = new URLSearchParams({
    doctor_telegram_id: String(telegramId),
    ...params,
  });
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}?${query}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось загрузить данные leaderboard", response.status);
  }
  return (await response.json()) as T;
}

export async function fetchLeaderboard(
  telegramId: number,
  role: string,
  options: LeaderboardQuery = {},
): Promise<LeaderboardResponse> {
  const params: Record<string, string> = {
    period: options.period ?? "30d",
    metric: options.metric ?? "xe",
    metric_x: options.metric_x ?? "xe",
    metric_y: options.metric_y ?? "insulin_dose",
  };
  if (role === "doctor") {
    return doctorFetch<LeaderboardResponse>(
      "/api/v1/web/leaderboard",
      telegramId,
      params,
    );
  }
  return patientFetch<LeaderboardResponse>(
    "/api/v1/web/leaderboard",
    telegramId,
    params,
  );
}

export async function fetchAssistantHistory(
  telegramId: number,
  options: { limit?: number; offset?: number } = {},
): Promise<PaginatedHistory> {
  const { baseUrl, token } = backendConfig();
  const query = new URLSearchParams({
    telegram_id: String(telegramId),
    limit: String(options.limit ?? 50),
    offset: String(options.offset ?? 0),
  });
  let response: Response;
  try {
    response = await fetch(
      `${baseUrl}/api/v1/web/assistant/history?${query}`,
      {
        headers: { Authorization: `Bearer ${token}` },
        cache: "no-store",
      },
    );
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось загрузить историю чата", response.status);
  }
  return (await response.json()) as PaginatedHistory;
}

export async function sendAssistantMessage(
  telegramId: number,
  text: string,
): Promise<SendMessageResponse> {
  const { baseUrl, token } = backendConfig();
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/v1/assistant/messages`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ telegram_id: telegramId, text }),
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (response.status === 502 || response.status === 503) {
    throw new AuthError("Ассистент временно недоступен", response.status);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось отправить сообщение", response.status);
  }
  return (await response.json()) as SendMessageResponse;
}

export async function transcribeAudio(
  audioBase64: string,
  mediaType: string,
): Promise<{ text: string }> {
  const { baseUrl, token } = backendConfig();
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/v1/media/transcribe`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audio_base64: audioBase64,
        media_type: mediaType,
      }),
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (response.status === 422 || response.status === 400) {
    throw new AuthError("Не удалось распознать речь", response.status);
  }
  if (response.status === 502 || response.status === 503) {
    throw new AuthError("Распознавание временно недоступно", response.status);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось распознать речь", response.status);
  }
  return (await response.json()) as { text: string };
}

export async function queryAnalytics(
  telegramId: number,
  role: string,
  question: string,
): Promise<AnalyticsQueryResponse> {
  const { baseUrl, token } = backendConfig();
  const query = new URLSearchParams(
    role === "doctor"
      ? { doctor_telegram_id: String(telegramId) }
      : { patient_telegram_id: String(telegramId) },
  );
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/v1/web/analytics/query?${query}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
      cache: "no-store",
    });
  } catch {
    throw new AuthError("Сервис недоступен. Запустите backend.", 503);
  }
  if (response.status === 422 || response.status === 403) {
    throw new AuthError("Не удалось выполнить запрос по данным", response.status);
  }
  if (response.status === 502 || response.status === 503 || response.status === 504) {
    throw new AuthError("Аналитика временно недоступна", response.status);
  }
  if (!response.ok) {
    throw new AuthError("Не удалось выполнить запрос", response.status);
  }
  return (await response.json()) as AnalyticsQueryResponse;
}
