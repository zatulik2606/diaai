import type { BjeMedal, LeaderboardTableRow } from "@/lib/types/leaderboard";

export const MEDAL_EMOJI: Record<BjeMedal, string> = {
  gold: "🥇",
  silver: "🥈",
  bronze: "🥉",
  fourth: "4️⃣",
  fifth: "5️⃣",
};

export const MEDAL_LABEL: Record<BjeMedal, string> = {
  gold: "1 место",
  silver: "2 место",
  bronze: "3 место",
  fourth: "4 место",
  fifth: "5 место",
};

const MEDAL_RANK: Record<BjeMedal, number> = {
  gold: 1,
  silver: 2,
  bronze: 3,
  fourth: 4,
  fifth: 5,
};

export type TopBjeProduct = {
  name: string;
  total_bje: number;
  bje_medal: BjeMedal;
};

export function aggregateTop5Bje(table: LeaderboardTableRow[]): TopBjeProduct[] {
  const totals = new Map<
    string,
    { name: string; total_bje: number; bje_medal: BjeMedal | null }
  >();

  for (const row of table) {
    for (const product of row.products) {
      const key = product.name.trim().toLowerCase();
      const current = totals.get(key);
      if (!current) {
        totals.set(key, {
          name: product.name,
          total_bje: product.bje,
          bje_medal: product.bje_medal,
        });
      } else {
        current.total_bje += product.bje;
        if (product.bje_medal) {
          current.bje_medal = product.bje_medal;
        }
      }
    }
  }

  return [...totals.values()]
    .filter((item): item is TopBjeProduct => item.bje_medal != null)
    .sort((a, b) => MEDAL_RANK[a.bje_medal] - MEDAL_RANK[b.bje_medal]);
}
