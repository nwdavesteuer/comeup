"""
Metrics schemas
"""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import date, datetime
from uuid import UUID


class DailyMetricBase(BaseModel):
    date: date
    platform: str
    metric_name: str
    value: Optional[int] = None


class DailyMetricResponse(DailyMetricBase):
    metric_id: UUID
    artist_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MetricsOverviewResponse(BaseModel):
    total_streams: Optional[int] = None
    monthly_listeners: Optional[int] = None
    followers: dict[str, int] = {}  # platform -> count
    growth_rates: dict[str, float] = {}  # metric -> percentage
    last_updated: Optional[datetime] = None


class PlatformMetricsResponse(BaseModel):
    platform: str
    metrics: list[DailyMetricResponse]
    summary: dict[str, Any] = {}

