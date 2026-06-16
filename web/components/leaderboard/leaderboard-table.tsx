import { ProductChip } from "@/components/leaderboard/product-chip";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { LeaderboardTableRow } from "@/lib/types/leaderboard";
import { cn } from "@/lib/utils";

export function LeaderboardTable({
  rows,
  currentUserId,
}: {
  rows: LeaderboardTableRow[];
  currentUserId?: string;
}) {
  if (rows.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-muted-foreground">
        Нет пациентов в когорте
      </p>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-12">#</TableHead>
          <TableHead className="min-w-[8rem]">Пациент</TableHead>
          <TableHead className="min-w-[10rem]">Прогресс</TableHead>
          <TableHead>Продукты</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((row) => {
          const isCurrentUser = currentUserId === row.patient.user_id;
          return (
          <TableRow
            key={row.patient.user_id}
            className={cn(isCurrentUser && "bg-primary/10 ring-1 ring-inset ring-primary/30")}
          >
            <TableCell className="font-mono">
              {row.rank}
              {isCurrentUser ? (
                <span className="ml-1 text-xs text-primary">(вы)</span>
              ) : null}
            </TableCell>
            <TableCell>{row.patient.display_name ?? "—"}</TableCell>
            <TableCell>
              <div className="flex min-w-[8rem] flex-col gap-1">
                <Progress value={row.progress_pct} />
                <span className="font-mono text-xs text-muted-foreground">
                  {row.progress_pct.toFixed(0)}%
                </span>
              </div>
            </TableCell>
            <TableCell>
              <div className="flex flex-wrap gap-2">
                {row.products.length === 0 ? (
                  <span className="text-xs text-muted-foreground">—</span>
                ) : (
                  row.products.map((product) => (
                    <ProductChip
                      key={`${row.patient.user_id}-${product.name}`}
                      product={product}
                    />
                  ))
                )}
              </div>
            </TableCell>
          </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}
