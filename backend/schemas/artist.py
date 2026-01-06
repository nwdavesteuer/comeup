"""
Artist schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ArtistBase(BaseModel):
    artist_name: str
    genre: Optional[str] = None
    subscription_tier: str = "free"


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    artist_name: Optional[str] = None
    genre: Optional[str] = None
    subscription_tier: Optional[str] = None
    onboarding_complete: Optional[bool] = None


class ArtistResponse(ArtistBase):
    artist_id: UUID
    user_id: UUID
    onboarding_complete: bool
    created_at: datetime

    class Config:
        from_attributes = True

