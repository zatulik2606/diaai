import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Панель пациента с диабетом</CardTitle>
        <CardDescription>
          KPI, график активности и матрица прогресса — iter 3.
        </CardDescription>
      </CardHeader>
    </Card>
  );
}
