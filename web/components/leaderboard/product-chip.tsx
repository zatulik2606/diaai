import type { LeaderboardProduct } from "@/lib/types/leaderboard";
import { MEDAL_EMOJI, MEDAL_LABEL } from "@/lib/leaderboard-utils";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

const MEDAL_RING: Record<NonNullable<LeaderboardProduct["bje_medal"]>, string> = {
  gold: "border-[#FFD700] bg-[#FFD700]/15 shadow-[0_0_0_1px_#FFD70066]",
  silver: "border-[#C0C0C0] bg-[#C0C0C0]/15 shadow-[0_0_0_1px_#C0C0C066]",
  bronze: "border-[#CD7F32] bg-[#CD7F32]/15 shadow-[0_0_0_1px_#CD7F3266]",
  fourth: "border-[#9CA3AF] bg-[#9CA3AF]/15 shadow-[0_0_0_1px_#9CA3AF66]",
  fifth: "border-[#78716F] bg-[#78716F]/15 shadow-[0_0_0_1px_#78716F66]",
};

function productEmoji(name: string): string {
  const n = name.toLowerCase();
  if (n.includes("овсян")) return "🥣";
  if (n.includes("паста") || n.includes("макарон")) return "🍝";
  if (n.includes("хлеб")) return "🍞";
  if (n.includes("яблок")) return "🍎";
  if (n.includes("творог") || n.includes("молок")) return "🥛";
  if (n.includes("куриц") || n.includes("мяс")) return "🍗";
  return "🍽️";
}

export function ProductChip({ product }: { product: LeaderboardProduct }) {
  const medal = product.bje_medal;

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <span
            className={cn(
              "inline-flex items-center gap-1.5 rounded-md border border-border bg-muted/50 px-2 py-1 text-xs",
              medal && MEDAL_RING[medal],
            )}
          >
            {medal ? (
              <span
                className="text-base leading-none"
                title={MEDAL_LABEL[medal]}
                aria-label={`Топ-5 БЖЕ: ${MEDAL_LABEL[medal]}`}
              >
                {MEDAL_EMOJI[medal]}
              </span>
            ) : null}
            <span aria-hidden>{productEmoji(product.name)}</span>
            <span className="max-w-[6rem] truncate">{product.name}</span>
            <span className="font-mono text-muted-foreground">
              {product.xe.toFixed(1)} ХЕ
            </span>
          </span>
        </TooltipTrigger>
        <TooltipContent>
          <p className="font-medium">{product.name}</p>
          <p className="text-muted-foreground">
            ХЕ: {product.xe.toFixed(1)} · БЖЕ: {product.bje.toFixed(1)}
            {medal ? ` · ${MEDAL_LABEL[medal]} по БЖЕ когорты` : ""}
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
