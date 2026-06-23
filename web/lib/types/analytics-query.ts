export type ChartHint = "scalar" | "bar" | "line" | "table";

export type AnalyticsQueryResponse = {
  answer: string;
  columns: string[];
  rows: (string | number | null)[][];
  chart_hint: ChartHint;
};
