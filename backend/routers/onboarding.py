"""
Onboarding routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.onboarding import OnboardingResponse
from backend.models.connection import PlatformConnection
from backend.schemas.onboarding import (
    OnboardingAnswerRequest,
    OnboardingStatusResponse,
    OnboardingResponseModel
)
from backend.utils.auth import get_current_artist
from datetime import datetime
import json

router = APIRouter()

# Question order mapping
QUESTION_ORDER = [
    "content_time",
    "live_performances",
    "content_types",
    "music_inspiration",
    "visual_style",
    "challenges",
    "whats_working",
    "upcoming_music",
    "collaborations",
    "upcoming_content"
]


def get_or_create_onboarding(db: Session, artist_id) -> OnboardingResponse:
    """Get existing onboarding or create new one"""
    onboarding = db.query(OnboardingResponse).filter(
        OnboardingResponse.artist_id == artist_id
    ).first()
    
    if not onboarding:
        onboarding = OnboardingResponse(artist_id=artist_id)
        db.add(onboarding)
        db.commit()
        db.refresh(onboarding)
    
    return onboarding


def calculate_progress(onboarding: OnboardingResponse) -> int:
    """Calculate how many questions have been answered"""
    progress = 0
    if onboarding.content_hours_per_week:
        progress += 1
    if onboarding.performs_live:
        progress += 1
    if onboarding.preferred_content_types:
        progress += 1
    if onboarding.inspiring_artists or onboarding.genre_fallback:
        progress += 1
    if onboarding.visual_styles:
        progress += 1
    if onboarding.top_challenges:
        progress += 1
    if onboarding.whats_working:
        progress += 1
    if onboarding.upcoming_music:
        progress += 1
    if onboarding.collaboration_plans:
        progress += 1
    if onboarding.upcoming_content:
        progress += 1
    return progress


def get_next_question(onboarding: OnboardingResponse) -> Optional[str]:
    """Determine the next unanswered question"""
    if not onboarding.content_hours_per_week:
        return "content_time"
    if not onboarding.performs_live:
        return "live_performances"
    if not onboarding.preferred_content_types:
        return "content_types"
    if not onboarding.inspiring_artists and not onboarding.genre_fallback:
        return "music_inspiration"
    if not onboarding.visual_styles:
        return "visual_style"
    if not onboarding.top_challenges:
        return "challenges"
    if not onboarding.whats_working:
        return "whats_working"
    if not onboarding.upcoming_music:
        return "upcoming_music"
    if not onboarding.collaboration_plans:
        return "collaborations"
    if not onboarding.upcoming_content:
        return "upcoming_content"
    return None


@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get onboarding status and progress"""
    onboarding = get_or_create_onboarding(db, artist.artist_id)
    progress = calculate_progress(onboarding)
    next_question = get_next_question(onboarding)
    
    return OnboardingStatusResponse(
        is_complete=onboarding.is_complete,
        current_question=next_question,
        progress=progress,
        total_questions=10
    )


@router.post("/answer")
async def save_onboarding_answer(
    answer_data: OnboardingAnswerRequest,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Save an onboarding answer"""
    onboarding = get_or_create_onboarding(db, artist.artist_id)
    
    # Map question keys to model fields
    question_key = answer_data.question_key
    answer = answer_data.answer
    
    if question_key == "content_time":
        onboarding.content_hours_per_week = str(answer) if isinstance(answer, str) else answer
    elif question_key == "live_performances":
        onboarding.performs_live = str(answer) if isinstance(answer, str) else answer
    elif question_key == "content_types":
        onboarding.preferred_content_types = answer if isinstance(answer, list) else [answer]
    elif question_key == "music_inspiration":
        if isinstance(answer, str):
            onboarding.inspiring_artists = answer
        elif isinstance(answer, dict) and "genre" in answer:
            onboarding.genre_fallback = answer["genre"]
    elif question_key == "visual_style":
        if isinstance(answer, list):
            onboarding.visual_styles = answer
        elif isinstance(answer, dict):
            onboarding.visual_style_followup = answer
    elif question_key == "challenges":
        onboarding.top_challenges = answer if isinstance(answer, list) else [answer]
    elif question_key == "whats_working":
        onboarding.whats_working = answer if isinstance(answer, list) else [answer]
    elif question_key == "upcoming_music":
        if isinstance(answer, dict):
            onboarding.upcoming_music = answer.get("type")
            onboarding.release_timeline = answer.get("timeline")
            if answer.get("specific_date"):
                onboarding.specific_release_date = datetime.fromisoformat(answer["specific_date"])
        else:
            onboarding.upcoming_music = str(answer)
    elif question_key == "collaborations":
        onboarding.collaboration_plans = str(answer) if isinstance(answer, str) else answer
    elif question_key == "upcoming_content":
        onboarding.upcoming_content = str(answer) if isinstance(answer, str) else answer
    
    # Update current question
    onboarding.current_question = get_next_question(onboarding)
    onboarding.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(onboarding)
    
    return {"message": "Answer saved", "next_question": onboarding.current_question}


@router.post("/complete")
async def complete_onboarding(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Mark onboarding as complete"""
    onboarding = get_or_create_onboarding(db, artist.artist_id)
    
    # Verify all questions are answered
    progress = calculate_progress(onboarding)
    if progress < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Onboarding incomplete. {progress}/10 questions answered."
        )
    
    # Check for required platform connections
    spotify_connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist.artist_id,
        PlatformConnection.platform == "spotify",
        PlatformConnection.is_active == True
    ).first()
    
    instagram_connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist.artist_id,
        PlatformConnection.platform == "instagram",
        PlatformConnection.is_active == True
    ).first()
    
    if not spotify_connection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spotify account must be connected to complete onboarding. Please connect your Spotify account first."
        )
    
    if not instagram_connection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account must be connected to complete onboarding. Please connect your Instagram account first."
        )
    
    onboarding.is_complete = True
    artist.onboarding_complete = True
    onboarding.current_question = None
    
    db.commit()
    
    return {"message": "Onboarding completed successfully"}


@router.get("/data", response_model=OnboardingResponseModel)
async def get_onboarding_data(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get full onboarding data"""
    onboarding = get_or_create_onboarding(db, artist.artist_id)
    return onboarding

