import { redirect } from "next/navigation";

import { ActivityChart } from "@/components/dashboard/activity-chart";
import { KpiGrid } from "@/components/dashboard/kpi-grid";
import { ProgressMatrix } from "@/components/dashboard/progress-matrix";
import { QuestionsTable } from "@/components/dashboard/questions-table";
import { SubmissionsList } from "@/components/dashboard/submissions-list";
import { fetchPatientDashboard } from "@/lib/backend-client";
import { getSession } from "@/lib/session";

export default async function DashboardPage() {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }
  if (session.telegram_id == null) {
    throw new Error("Telegram ID не найден в сессии");
  }

  const data = await fetchPatientDashboard(session.telegram_id);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Панель пациента с диабетом
        </h1>
        <p className="text-sm text-muted-foreground">
          {session.display_name ?? session.user_id}
        </p>
      </div>

      <KpiGrid kpis={data.summary.kpis} />

      <div className="grid gap-6 lg:grid-cols-2">
        <ActivityChart activity={data.activity} />
        <QuestionsTable questions={data.questions} />
        <SubmissionsList submissions={data.submissions} />
        <ProgressMatrix matrix={data.matrix} />
      </div>
    </div>
  );
}
