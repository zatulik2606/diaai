export type LeaderboardPeriod = "7d" | "30d" | "90d";
export type MetricKey = "xe" | "bje" | "insulin_dose" | "activity_score";
export type BjeMedal = "gold" | "silver" | "bronze" | "fourth" | "fifth";

export type LeaderboardProduct = {
  name: string;
  xe: number;
  bje: number;
  bje_medal: BjeMedal | null;
};

export type LeaderboardPatient = {
  user_id: string;
  display_name: string | null;
};

export type LeaderboardTableRow = {
  rank: number;
  patient: LeaderboardPatient;
  progress_pct: number;
  products: LeaderboardProduct[];
};

export type LeaderboardScatterPoint = {
  patient_id: string;
  display_name: string | null;
  x: number;
  y: number;
};

export type LeaderboardResponse = {
  period: LeaderboardPeriod;
  metric: MetricKey;
  table: LeaderboardTableRow[];
  scatter: LeaderboardScatterPoint[];
};

export type LeaderboardQuery = {
  period?: LeaderboardPeriod;
  metric?: MetricKey;
  metric_x?: MetricKey;
  metric_y?: MetricKey;
};
