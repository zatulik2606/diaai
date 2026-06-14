"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Не удалось загрузить dashboard</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <p className="text-sm text-muted-foreground">
          {error.message || "Проверьте, что backend запущен (make backend-run)."}
        </p>
        <Button onClick={reset} variant="outline">
          Повторить
        </Button>
      </CardContent>
    </Card>
  );
}
