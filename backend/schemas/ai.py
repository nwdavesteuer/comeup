"""
AI feature schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


class GenerateIdeasRequest(BaseModel):
    platform: str
    content_type: Optional[str] = None
    context: Optional[str] = None


class GenerateIdeasResponse(BaseModel):
    ideas: List[str]


class GenerateCaptionRequest(BaseModel):
    content_type: str
    platform: str
    context: Optional[str] = None
    tone: Optional[str] = "professional"


class GenerateCaptionResponse(BaseModel):
    captions: List[str]


class PredictPerformanceRequest(BaseModel):
    platform: str
    content_type: str
    caption: Optional[str] = None
    scheduled_for: Optional[str] = None


class PredictPerformanceResponse(BaseModel):
    predicted_engagement_rate: Optional[Decimal] = None
    predicted_streams_lift: Optional[int] = None
    confidence_score: Optional[Decimal] = None
    recommendation: Optional[str] = None


class WeeklyInsightsResponse(BaseModel):
    insights: str
    key_points: List[str]
    action_items: List[str]
    generated_at: str

