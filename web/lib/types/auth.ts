export type SessionUser = {
  user_id: string;
  telegram_id: number | null;
  role: string;
  display_name: string | null;
};

export type AuthRole = "doctor" | "diabetic" | string;

export function defaultPathForRole(role: AuthRole): string {
  return role === "doctor" ? "/leaderboard" : "/dashboard";
}
