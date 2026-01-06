"""
Onboarding schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Dict, Any
from datetime import datetime
from uuid import UUID


class OnboardingAnswerRequest(BaseModel):
    """Request to save an onboarding answer"""
    question_key: str = Field(..., description="Key identifying the question (e.g., 'content_time', 'live_performances')")
    answer: Union[str, List[str], Dict[str, Any]] = Field(..., description="Answer value(s) - can be string, list, or dict depending on question")


class OnboardingStatusResponse(BaseModel):
    """Response showing onboarding status and progress"""
    is_complete: bool
    current_question: Optional[str] = None
    progress: int = Field(..., description="Number of questions completed (0-10)")
    total_questions: int = 10


class OnboardingResponseModel(BaseModel):
    """Full onboarding response data"""
    response_id: UUID
    artist_id: UUID
    content_hours_per_week: Optional[str] = None
    performs_live: Optional[str] = None
    preferred_content_types: Optional[List[str]] = None
    inspiring_artists: Optional[str] = None
    genre_fallback: Optional[str] = None
    visual_styles: Optional[List[str]] = None
    visual_style_followup: Optional[dict] = None
    top_challenges: Optional[List[str]] = None
    whats_working: Optional[List[str]] = None
    upcoming_music: Optional[str] = None
    release_timeline: Optional[str] = None
    specific_release_date: Optional[datetime] = None
    collaboration_plans: Optional[str] = None
    upcoming_content: Optional[str] = None
    current_question: Optional[str] = None
    is_complete: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

