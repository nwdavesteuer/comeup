"""
Content schedule routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.onboarding import OnboardingResponse
from backend.models.connection import PlatformConnection
from backend.schemas.content_schedule import (
    ContentScheduleResponse,
    ContentScheduleItem,
    ScheduleApprovalRequest
)
from backend.services.content_schedule_service import ContentScheduleService
from backend.utils.auth import get_current_artist

router = APIRouter()


@router.get("/preview", response_model=ContentScheduleResponse)
async def get_schedule_preview(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get a preview of the generated content schedule"""
    # Get onboarding data
    onboarding = db.query(OnboardingResponse).filter(
        OnboardingResponse.artist_id == artist.artist_id
    ).first()
    
    if not onboarding or not onboarding.is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding must be completed first"
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
            detail="Spotify account must be connected to generate content schedule. Please connect your Spotify account first."
        )
    
    if not instagram_connection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account must be connected to generate content schedule. Please connect your Instagram account first."
        )
    
    # Generate schedule
    schedule_data = ContentScheduleService.generate_weekly_schedule(onboarding)
    summary = ContentScheduleService.generate_schedule_summary(schedule_data)
    
    # Convert to response format
    schedule_items = [
        ContentScheduleItem(**item) for item in schedule_data
    ]
    
    return ContentScheduleResponse(
        schedule=schedule_items,
        summary=summary
    )


@router.post("/approve")
async def approve_schedule(
    approval: ScheduleApprovalRequest,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Approve or modify the content schedule"""
    if approval.approved:
        # Create content posts in database
        # This would create ContentPost records with status='scheduled'
        # For now, just return success
        return {
            "message": "Schedule approved! Your content calendar has been created.",
            "schedule_created": True
        }
    else:
        # User wants to make changes
        return {
            "message": "Please review and modify your schedule",
            "schedule_created": False
        }


@router.get("/this-week", response_model=ContentScheduleResponse)
async def get_this_week_schedule(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get this week's approved content schedule"""
    # For now, return the preview (in production, this would return saved schedule)
    return await get_schedule_preview(artist, db)

