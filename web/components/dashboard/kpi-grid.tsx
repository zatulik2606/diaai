import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { PatientDashboardKpi } from "@/lib/types/patient-dashboard";

function trendClass(trend: PatientDashboardKpi["trend"]): string {
  if (trend === "up") {
    return "text-primary";
  }
  if (trend === "down") {
    return "text-destructive";
  }
  return "text-muted-foreground";
}

function formatDelta(delta: number, deltaPct: number): string {
  const sign = delta > 0 ? "+" : "";
  return `${sign}${delta} (${sign}${deltaPct}%)`;
}

export function KpiGrid({ kpis }: { kpis: PatientDashboardKpi[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {kpis.map((kpi) => (
        <Card key={kpi.id}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {kpi.label}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="font-mono text-3xl font-semibold">{kpi.value}</div>
            <p className={cn("mt-1 text-sm", trendClass(kpi.trend))}>
              {formatDelta(kpi.delta, kpi.delta_pct)} vs prev
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
