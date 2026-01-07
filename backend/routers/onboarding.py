"""
Onboarding routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.onboarding import OnboardingResponse
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
    "release_date",
    "song_name",
    "collaborations"
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
    # Release date/timeline - only count if they have upcoming music that needs it
    if onboarding.upcoming_music in ['soon', 'unreleased']:
        if onboarding.specific_release_date or onboarding.release_timeline:
            progress += 1
            # If they have a date, song_name is also required
            if onboarding.specific_release_date:
                if onboarding.song_name:
                    progress += 1
    if onboarding.collaboration_plans:
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
    # If they have upcoming music (soon/unreleased), check for release date first
    if onboarding.upcoming_music in ['soon', 'unreleased']:
        # First check if they have a date
        if not onboarding.specific_release_date:
            # If no date, check if they have timeline (they skipped date and provided timeline)
            if not onboarding.release_timeline:
                return "release_date"
        else:
            # They have a date, check if they provided song name
            if not onboarding.song_name:
                return "song_name"
    if not onboarding.collaboration_plans:
        return "collaborations"
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
    
    # Calculate total questions based on their answers
    # Base questions: 8 (content_time through whats_working, upcoming_music, collaborations)
    total_questions = 8
    # If they have upcoming music (soon/unreleased), add release date/timeline question
    if onboarding.upcoming_music in ['soon', 'unreleased']:
        total_questions += 1
        # If they have a specific date, add song_name question
        if onboarding.specific_release_date:
            total_questions += 1
    
    return OnboardingStatusResponse(
        is_complete=onboarding.is_complete,
        current_question=next_question,
        progress=progress,
        total_questions=total_questions
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
    elif question_key == "release_date":
        if answer is None or answer == "":
            # User skipped - show timeline question instead
            onboarding.specific_release_date = None
        elif isinstance(answer, str):
            # Parse date string (YYYY-MM-DD format)
            try:
                onboarding.specific_release_date = datetime.fromisoformat(answer)
            except ValueError:
                # If parsing fails, try with time component
                onboarding.specific_release_date = datetime.fromisoformat(answer + "T00:00:00")
        elif isinstance(answer, dict):
            if "date" in answer:
                onboarding.specific_release_date = datetime.fromisoformat(answer["date"])
            elif "timeline" in answer:
                # They provided timeline instead of date
                onboarding.release_timeline = answer["timeline"]
                onboarding.specific_release_date = None
    elif question_key == "song_name":
        onboarding.song_name = str(answer) if answer else None
    elif question_key == "collaborations":
        onboarding.collaboration_plans = str(answer) if isinstance(answer, str) else answer
    
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
    
    # Check if there are any remaining questions
    next_question = get_next_question(onboarding)
    if next_question:
        # Calculate expected total
        total_questions = 8
        if onboarding.upcoming_music in ['soon', 'unreleased']:
            total_questions += 1
            if onboarding.specific_release_date:
                total_questions += 1
        progress = calculate_progress(onboarding)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Onboarding incomplete. Please answer all questions first."
        )
    
    # Platform connections are optional - no validation needed
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

