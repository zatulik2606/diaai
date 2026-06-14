import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function LeaderboardPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Leaderboard</CardTitle>
        <CardDescription>
          Таблица (продукты, ХЕ, топ-5 БЖЕ) и scatter plot — iter 4.
        </CardDescription>
      </CardHeader>
    </Card>
  );
}
