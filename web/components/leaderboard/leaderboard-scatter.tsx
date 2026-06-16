"use client";

import {
  CartesianGrid,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer } from "@/components/ui/chart";
import type { LeaderboardScatterPoint } from "@/lib/types/leaderboard";

const chartConfig = {
  point: { label: "Пациент", color: "hsl(var(--chart-1))" },
};

type ScatterDatum = {
  name: string;
  x: number;
  y: number;
};

function ScatterTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: { payload: ScatterDatum }[];
}) {
  if (!active || !payload?.length) return null;
  const point = payload[0].payload;
  return (
    <div className="rounded-md border border-border bg-card px-3 py-2 text-xs shadow-md">
      <p className="font-medium">{point.name}</p>
      <p className="font-mono text-muted-foreground">
        X: {point.x.toFixed(1)} · Y: {point.y.toFixed(1)}
      </p>
    </div>
  );
}

export function LeaderboardScatter({
  points,
  metricX = "xe",
  metricY = "insulin_dose",
}: {
  points: LeaderboardScatterPoint[];
  metricX?: string;
  metricY?: string;
}) {
  const data: ScatterDatum[] = points.map((point) => ({
    name: point.display_name ?? point.patient_id.slice(0, 8),
    x: point.x,
    y: point.y,
  }));

  const hasData = data.length > 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          Scatter: {metricX} × {metricY}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {hasData ? (
          <ChartContainer config={chartConfig} className="aspect-auto h-[320px] w-full">
            <ScatterChart margin={{ left: 8, right: 8, top: 8, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-border/50" />
              <XAxis
                type="number"
                dataKey="x"
                name={metricX}
                tickLine={false}
                axisLine={false}
                fontSize={12}
              />
              <YAxis
                type="number"
                dataKey="y"
                name={metricY}
                tickLine={false}
                axisLine={false}
                fontSize={12}
                width={40}
              />
              <Tooltip content={<ScatterTooltip />} />
              <Scatter data={data} fill="hsl(var(--chart-1))" />
            </ScatterChart>
          </ChartContainer>
        ) : (
          <p className="py-8 text-center text-sm text-muted-foreground">
            Нет данных для scatter plot
          </p>
        )}
      </CardContent>
    </Card>
  );
}
