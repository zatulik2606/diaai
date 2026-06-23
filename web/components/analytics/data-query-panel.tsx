"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer } from "@/components/ui/chart";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import type { AnalyticsQueryResponse } from "@/lib/types/analytics-query";

const chartConfig = {
  value: { label: "Значение", color: "hsl(var(--chart-1))" },
};

type DataQueryPanelProps = {
  role: string;
};

export function DataQueryPanel({ role }: DataQueryPanelProps) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyticsQueryResponse | null>(null);

  async function handleSubmit() {
    const trimmed = question.trim();
    if (!trimmed || loading) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/analytics/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
      });
      const body = (await response.json()) as AnalyticsQueryResponse & {
        error?: string;
      };
      if (!response.ok) {
        setError(body.error ?? "Не удалось выполнить запрос");
        setResult(null);
        return;
      }
      setResult(body);
    } catch {
      setError("Сервис недоступен. Запустите backend.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const chartData =
    result && result.chart_hint === "bar" && result.columns.length >= 2
      ? result.rows.map((row) => ({
          label: String(row[0] ?? ""),
          value: Number(row[1] ?? 0),
        }))
      : [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Вопрос по данным</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder={
            role === "doctor"
              ? "Например: сколько ХЕ за неделю у Иван П.?"
              : "Например: сколько ХЕ я съел за последние 7 дней?"
          }
          rows={2}
          disabled={loading}
        />
        <div className="flex items-center gap-3">
          <Button type="button" onClick={() => void handleSubmit()} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 size-4 animate-spin" />
                Запрос…
              </>
            ) : (
              "Спросить"
            )}
          </Button>
          {error ? (
            <p className="text-sm text-destructive" role="alert">
              {error}
            </p>
          ) : null}
        </div>

        {result ? (
          <div className="flex flex-col gap-4 border-t pt-4">
            <p className="whitespace-pre-wrap text-sm">{result.answer}</p>

            {result.chart_hint === "bar" && chartData.length > 0 ? (
              <ChartContainer config={chartConfig} className="aspect-auto h-[220px] w-full">
                <BarChart data={chartData} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-border/50" />
                  <XAxis dataKey="label" tickLine={false} axisLine={false} fontSize={12} />
                  <YAxis tickLine={false} axisLine={false} fontSize={12} width={32} />
                  <Bar dataKey="value" fill="hsl(var(--chart-1))" radius={4} />
                </BarChart>
              </ChartContainer>
            ) : null}

            {result.rows.length > 0 &&
            !(result.chart_hint === "scalar" && result.rows.length === 1) ? (
              <div className="overflow-x-auto rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      {result.columns.map((column) => (
                        <TableHead key={column}>{column}</TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {result.rows.map((row, rowIndex) => (
                      <TableRow key={`row-${rowIndex}`}>
                        {row.map((cell, cellIndex) => (
                          <TableCell key={`cell-${rowIndex}-${cellIndex}`}>
                            {cell ?? "—"}
                          </TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            ) : null}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
