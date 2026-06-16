import { redirect } from "next/navigation";

import { LeaderboardTabs } from "@/components/leaderboard/leaderboard-tabs";
import { fetchLeaderboard } from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export default async function LeaderboardPage() {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }
  if (session.telegram_id == null) {
    throw new Error("Telegram ID не найден в сессии");
  }

  const data = await fetchLeaderboard(session.telegram_id, session.role);
  const myRow =
    session.role === "diabetic"
      ? data.table.find((row) => row.patient.user_id === session.user_id)
      : undefined;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Лидерборд</h1>
        <p className="text-sm text-muted-foreground">
          {session.display_name ?? session.user_id}
          {myRow ? ` · ваше место: #${myRow.rank}` : ""}
        </p>
      </div>

      <LeaderboardTabs
        data={data}
        metricX="xe"
        metricY="insulin_dose"
        currentUserId={session.user_id}
      />
    </div>
  );
}
