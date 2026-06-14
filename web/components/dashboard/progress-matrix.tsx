import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import type { PatientProgressMatrix } from "@/lib/types/patient-dashboard";

function cellColor(pct: number): string {
  if (pct <= 0) {
    return "bg-muted/30";
  }
  if (pct >= 80) {
    return "bg-primary/40";
  }
  if (pct >= 50) {
    return "bg-primary/25";
  }
  return "bg-primary/10";
}

export function ProgressMatrix({ matrix }: { matrix: PatientProgressMatrix }) {
  const hasData = matrix.columns.length > 0;

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Матрица прогресса</CardTitle>
      </CardHeader>
      <CardContent>
        {!hasData ? (
          <p className="text-sm text-muted-foreground">Нет snapshots за период</p>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="sticky left-0 bg-card">Метрика</TableHead>
                  {matrix.columns.map((col) => (
                    <TableHead key={col.id} className="text-center">
                      {col.label}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {matrix.rows.map((row) => (
                  <TableRow key={row.metric_id}>
                    <TableCell className="sticky left-0 bg-card font-medium">
                      {row.label}
                    </TableCell>
                    {row.cells.map((cell) => (
                      <TableCell key={`${row.metric_id}-${cell.column_id}`}>
                        <div
                          className={cn(
                            "rounded px-2 py-1 text-center font-mono text-sm",
                            cellColor(cell.completion_pct),
                          )}
                          title={
                            cell.snapshot_date
                              ? `${cell.value} · ${Math.round(cell.completion_pct)}%`
                              : undefined
                          }
                        >
                          {cell.value > 0 ? cell.value : "—"}
                        </div>
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
