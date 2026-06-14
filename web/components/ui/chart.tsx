"use client";

import * as React from "react";
import * as RechartsPrimitive from "recharts";

import { cn } from "@/lib/utils";

export type ChartConfig = Record<
  string,
  {
    label?: string;
    color?: string;
  }
>;

const ChartContext = React.createContext<{ config: ChartConfig } | null>(null);

function useChart() {
  const context = React.useContext(ChartContext);
  if (!context) {
    throw new Error("useChart must be used within ChartContainer");
  }
  return context;
}

function ChartContainer({
  id,
  className,
  children,
  config,
}: React.ComponentProps<"div"> & {
  config: ChartConfig;
  children: React.ComponentProps<
    typeof RechartsPrimitive.ResponsiveContainer
  >["children"];
}) {
  const uniqueId = React.useId();
  const chartId = `chart-${id ?? uniqueId.replace(/:/g, "")}`;

  return (
    <ChartContext.Provider value={{ config }}>
      <div
        data-chart={chartId}
        className={cn(
          "flex aspect-video justify-center text-xs [&_.recharts-cartesian-axis-tick_text]:fill-muted-foreground [&_.recharts-cartesian-grid_line[stroke='#ccc']]:stroke-border/50",
          className,
        )}
      >
        <RechartsPrimitive.ResponsiveContainer>
          {children}
        </RechartsPrimitive.ResponsiveContainer>
      </div>
    </ChartContext.Provider>
  );
}

export { ChartContainer, useChart };
