"use client";

import dynamic from "next/dynamic";
import { useState } from "react";

import { BjeTop5Legend } from "@/components/leaderboard/bje-top5-legend";
import { LeaderboardTable } from "@/components/leaderboard/leaderboard-table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { LeaderboardResponse } from "@/lib/types/leaderboard";

const LeaderboardScatter = dynamic(
  () =>
    import("@/components/leaderboard/leaderboard-scatter").then(
      (mod) => mod.LeaderboardScatter,
    ),
  {
    loading: () => <Skeleton className="aspect-auto h-[320px] w-full" />,
    ssr: false,
  },
);

const PERIOD_LABELS: Record<string, string> = {
  "7d": "7 дней",
  "30d": "30 дней",
  "90d": "90 дней",
};

const METRIC_LABELS: Record<string, string> = {
  xe: "ХЕ",
  bje: "БЖЕ",
  insulin_dose: "Инсулин",
  activity_score: "Активность",
};

export function LeaderboardTabs({
  data,
  metricX = "xe",
  metricY = "insulin_dose",
  currentUserId,
}: {
  data: LeaderboardResponse;
  metricX?: string;
  metricY?: string;
  currentUserId?: string;
}) {
  const [tab, setTab] = useState("table");

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-muted-foreground">
        Период: {PERIOD_LABELS[data.period] ?? data.period} · Метрика рейтинга:{" "}
        {METRIC_LABELS[data.metric] ?? data.metric} · медали 🥇–5️⃣ — топ-5 продуктов
        когорты по БЖЕ
      </p>
      <BjeTop5Legend rows={data.table} />
      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="table">Таблица</TabsTrigger>
          <TabsTrigger value="scatter">Карта</TabsTrigger>
        </TabsList>
        <TabsContent value="table">
          <Card>
            <CardHeader>
              <CardTitle>Рейтинг пациентов</CardTitle>
            </CardHeader>
            <CardContent>
              <LeaderboardTable rows={data.table} currentUserId={currentUserId} />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="scatter">
          {tab === "scatter" ? (
            <LeaderboardScatter
              points={data.scatter}
              metricX={metricX}
              metricY={metricY}
            />
          ) : null}
        </TabsContent>
      </Tabs>
    </div>
  );
}
