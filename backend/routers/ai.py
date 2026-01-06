"""
AI features routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.artist import Artist
from backend.schemas.ai import (
    GenerateIdeasRequest, GenerateIdeasResponse,
    GenerateCaptionRequest, GenerateCaptionResponse,
    PredictPerformanceRequest, PredictPerformanceResponse,
    WeeklyInsightsResponse
)
from backend.utils.auth import get_current_artist
from backend.services.insights_service import InsightsService
from backend.services.prediction_service import PredictionService
from datetime import datetime

router = APIRouter()
insights_service = InsightsService()
prediction_service = PredictionService()


@router.post("/generate-ideas", response_model=GenerateIdeasResponse)
async def generate_content_ideas(
    request: GenerateIdeasRequest,
    artist: Artist = Depends(get_current_artist)
):
    """Generate content ideas using AI"""
    # Placeholder - would use Claude API to generate ideas
    ideas = [
        f"Create a {request.content_type} showcasing your latest track",
        f"Share behind-the-scenes content from your recording session",
        f"Post a {request.content_type} with a snippet of your new song"
    ]
    return GenerateIdeasResponse(ideas=ideas)


@router.post("/generate-caption", response_model=GenerateCaptionResponse)
async def generate_caption(
    request: GenerateCaptionRequest,
    artist: Artist = Depends(get_current_artist)
):
    """Generate caption variations using AI"""
    # Placeholder - would use Claude API to generate captions
    captions = [
        f"New {request.content_type} dropping soon! 🎵",
        f"Check out my latest {request.content_type} - what do you think?",
        f"Excited to share this {request.content_type} with you all!"
    ]
    return GenerateCaptionResponse(captions=captions)


@router.post("/predict-performance", response_model=PredictPerformanceResponse)
async def predict_performance(
    request: PredictPerformanceRequest,
    artist: Artist = Depends(get_current_artist)
):
    """Predict post performance using ML"""
    post_data = {
        "platform": request.platform,
        "content_type": request.content_type,
        "caption": request.caption,
        "scheduled_for": request.scheduled_for
    }
    
    prediction = prediction_service.predict_engagement(post_data)
    streams_lift = prediction_service.predict_streams_lift(post_data)
    
    return PredictPerformanceResponse(
        predicted_engagement_rate=prediction["predicted_engagement_rate"],
        predicted_streams_lift=streams_lift,
        confidence_score=prediction["confidence"],
        recommendation=prediction["recommendation"]
    )


@router.post("/weekly-insights", response_model=WeeklyInsightsResponse)
async def get_weekly_insights(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Generate weekly strategic insights"""
    insights_text = await insights_service.generate_weekly_insights(db, str(artist.artist_id))
    
    # Parse insights (simplified)
    key_points = []
    action_items = []
    
    # Simple parsing - in production would use better parsing
    lines = insights_text.split("\n")
    for line in lines:
        if "insight" in line.lower() or "key" in line.lower():
            key_points.append(line.strip())
        elif "action" in line.lower() or "try" in line.lower():
            action_items.append(line.strip())
    
    return WeeklyInsightsResponse(
        insights=insights_text,
        key_points=key_points[:3] if key_points else ["Analyze your content performance", "Engage with your audience", "Post consistently"],
        action_items=action_items[:2] if action_items else ["Post 3 times this week", "Engage with comments"],
        generated_at=datetime.utcnow().isoformat()
    )

