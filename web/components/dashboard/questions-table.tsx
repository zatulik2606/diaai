import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PaginatedPatientQuestions } from "@/lib/types/patient-dashboard";

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function QuestionsTable({
  questions,
}: {
  questions: PaginatedPatientQuestions;
}) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Вопросы ассистенту</CardTitle>
      </CardHeader>
      <CardContent>
        {questions.items.length === 0 ? (
          <p className="text-sm text-muted-foreground">Нет вопросов за период</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[120px]">Время</TableHead>
                <TableHead>Вопрос</TableHead>
                <TableHead>Ответ</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {questions.items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="text-muted-foreground">
                    {formatTime(item.created_at)}
                  </TableCell>
                  <TableCell>{item.content ?? "—"}</TableCell>
                  <TableCell>{item.reply}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
