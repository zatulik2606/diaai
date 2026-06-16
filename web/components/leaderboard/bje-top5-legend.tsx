import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  aggregateTop5Bje,
  MEDAL_EMOJI,
  MEDAL_LABEL,
} from "@/lib/leaderboard-utils";
import type { LeaderboardTableRow } from "@/lib/types/leaderboard";
import { cn } from "@/lib/utils";

const MEDAL_STYLES = {
  gold: "border-[#FFD700]/60 bg-[#FFD700]/10",
  silver: "border-[#C0C0C0]/60 bg-[#C0C0C0]/10",
  bronze: "border-[#CD7F32]/60 bg-[#CD7F32]/10",
  fourth: "border-[#9CA3AF]/60 bg-[#9CA3AF]/10",
  fifth: "border-[#78716F]/60 bg-[#78716F]/10",
} as const;

export function BjeTop5Legend({ rows }: { rows: LeaderboardTableRow[] }) {
  const top5 = aggregateTop5Bje(rows);

  if (top5.length === 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Топ-5 продуктов когорты по БЖЕ</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
          {top5.map((item) => (
            <li
              key={item.name}
              className={cn(
                "flex items-center gap-2 rounded-md border px-3 py-2 text-sm",
                MEDAL_STYLES[item.bje_medal],
              )}
            >
              <span className="text-xl" aria-hidden>
                {MEDAL_EMOJI[item.bje_medal]}
              </span>
              <div className="min-w-0">
                <p className="truncate font-medium">{item.name}</p>
                <p className="font-mono text-xs text-muted-foreground">
                  {item.total_bje.toFixed(1)} БЖЕ · {MEDAL_LABEL[item.bje_medal]}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
