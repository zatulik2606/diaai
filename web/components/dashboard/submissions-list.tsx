import Link from "next/link";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { PaginatedPatientSubmissions } from "@/lib/types/patient-dashboard";

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function typeLabel(type: string): string {
  return type === "food_event" ? "Питание" : "Фото";
}

export function SubmissionsList({
  submissions,
}: {
  submissions: PaginatedPatientSubmissions;
}) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Фиксации</CardTitle>
      </CardHeader>
      <CardContent>
        {submissions.items.length === 0 ? (
          <p className="text-sm text-muted-foreground">Нет фиксаций за период</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {submissions.items.map((item) => (
              <li
                key={item.id}
                className="flex items-start justify-between gap-3 rounded-md border border-border p-3"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{typeLabel(item.type)}</span>
                    <span>{formatTime(item.recorded_at)}</span>
                  </div>
                  <p className="mt-1 truncate font-medium">{item.title}</p>
                  {item.xe != null ? (
                    <p className="font-mono text-sm text-muted-foreground">
                      ХЕ {item.xe}
                      {item.bje != null ? ` · БЖЕ ${item.bje}` : ""}
                    </p>
                  ) : null}
                </div>
                <Link
                  href={item.detail_url}
                  className="shrink-0 text-sm text-primary hover:underline"
                >
                  Детали
                </Link>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
