"""
Content schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ContentPostBase(BaseModel):
    platform: str
    content_type: str
    caption: Optional[str] = None
    media_url: Optional[str] = None
    scheduled_for: Optional[datetime] = None


class ContentPostCreate(ContentPostBase):
    pass


class ContentPostUpdate(BaseModel):
    caption: Optional[str] = None
    media_url: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    status: Optional[str] = None


class ContentPostResponse(ContentPostBase):
    post_id: UUID
    artist_id: UUID
    external_url: Optional[str] = None
    posted_at: Optional[datetime] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContentPerformanceResponse(BaseModel):
    performance_id: UUID
    post_id: UUID
    artist_id: UUID
    measured_at: datetime
    likes: int
    comments: int
    shares: int
    saves: int
    impressions: int
    reach: int
    engagement_rate: Optional[Decimal] = None
    spotify_traffic_lift: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

