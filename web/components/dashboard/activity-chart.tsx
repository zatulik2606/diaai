"use client";

import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer } from "@/components/ui/chart";
import type { PatientDashboardActivity } from "@/lib/types/patient-dashboard";

const chartConfig = {
  requests: { label: "Вопросы", color: "hsl(var(--chart-1))" },
  food: { label: "Питание", color: "hsl(var(--chart-2))" },
};

function formatDay(date: string): string {
  return new Date(date).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
  });
}

export function ActivityChart({ activity }: { activity: PatientDashboardActivity }) {
  const data = activity.series.map((point) => ({
    date: formatDay(point.date),
    requests: point.requests_count,
    food: point.food_events_count,
  }));

  const hasData = data.some((point) => point.requests > 0 || point.food > 0);

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Активность ({activity.days} дней)</CardTitle>
      </CardHeader>
      <CardContent>
        {hasData ? (
          <ChartContainer config={chartConfig} className="aspect-auto h-[240px] w-full">
            <LineChart data={data} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-border/50" />
              <XAxis dataKey="date" tickLine={false} axisLine={false} fontSize={12} />
              <YAxis tickLine={false} axisLine={false} fontSize={12} width={28} />
              <Line
                type="monotone"
                dataKey="requests"
                stroke="hsl(var(--chart-1))"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="food"
                stroke="hsl(var(--chart-2))"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ChartContainer>
        ) : (
          <p className="text-sm text-muted-foreground">Нет данных за период</p>
        )}
      </CardContent>
    </Card>
  );
}
