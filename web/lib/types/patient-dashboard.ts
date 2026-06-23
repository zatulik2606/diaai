export type Trend = "up" | "down" | "flat";

export type PatientKpiId =
  | "total_xe"
  | "questions_count"
  | "food_events_count"
  | "insulin_total";

export type PatientMetricId = "xe" | "bje" | "insulin";

export type MatrixPeriod = "week" | "month";

export type PatientDashboardKpi = {
  id: PatientKpiId;
  label: string;
  value: number;
  delta: number;
  delta_pct: number;
  trend: Trend;
};

export type PatientDashboardSummary = {
  period_days: number;
  kpis: PatientDashboardKpi[];
};

export type ActivityDayPoint = {
  date: string;
  requests_count: number;
  food_events_count: number;
};

export type PatientDashboardActivity = {
  days: number;
  series: ActivityDayPoint[];
};

export type PatientQuestionItem = {
  id: string;
  content: string | null;
  reply: string;
  created_at: string;
};

export type PaginatedPatientQuestions = {
  items: PatientQuestionItem[];
  total: number;
  limit: number;
  offset: number;
};

export type PatientSubmissionItem = {
  id: string;
  type: "food_event" | "photo_analysis";
  title: string;
  xe: number | null;
  bje: number | null;
  confidence: number | null;
  recorded_at: string;
  detail_url: string;
};

export type PaginatedPatientSubmissions = {
  items: PatientSubmissionItem[];
  total: number;
  limit: number;
  offset: number;
};

export type MatrixColumn = {
  id: string;
  label: string;
};

export type PatientMetricCell = {
  column_id: string;
  value: number;
  completion_pct: number;
  snapshot_date: string | null;
};

export type PatientMetricRow = {
  metric_id: PatientMetricId;
  label: string;
  cells: PatientMetricCell[];
};

export type PatientProgressMatrix = {
  period: MatrixPeriod;
  columns: MatrixColumn[];
  rows: PatientMetricRow[];
};

export type PatientDashboardData = {
  summary: PatientDashboardSummary;
  activity: PatientDashboardActivity;
  questions: PaginatedPatientQuestions;
  submissions: PaginatedPatientSubmissions;
  matrix: PatientProgressMatrix;
};
