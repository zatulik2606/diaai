from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ChartHint = Literal["scalar", "bar", "line", "table"]


class AnalyticsQueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AnalyticsQueryResponse(BaseModel):
    answer: str
    columns: list[str]
    rows: list[list[str | int | float | None]]
    chart_hint: ChartHint = "table"
