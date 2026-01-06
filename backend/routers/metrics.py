"""
Metrics and analytics routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.metric import DailyMetric
from backend.schemas.metric import MetricsOverviewResponse, PlatformMetricsResponse, DailyMetricResponse
from backend.utils.auth import get_current_artist
from datetime import date, datetime, timedelta
from typing import Optional

router = APIRouter()


@router.get("/overview", response_model=MetricsOverviewResponse)
async def get_metrics_overview(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get dashboard overview metrics"""
    # Get latest metrics
    latest_metrics = db.query(DailyMetric).filter(
        DailyMetric.artist_id == artist.artist_id
    ).order_by(DailyMetric.date.desc()).limit(100).all()
    
    # Calculate summary
    total_streams = None
    monthly_listeners = None
    followers = {}
    growth_rates = {}
    
    # Group by platform and metric
    platform_metrics = {}
    for metric in latest_metrics:
        key = f"{metric.platform}_{metric.metric_name}"
        if key not in platform_metrics:
            platform_metrics[key] = []
        platform_metrics[key].append(metric)
    
    # Extract key metrics
    for key, metrics in platform_metrics.items():
        if "spotify" in key and "streams" in key:
            total_streams = metrics[0].value if metrics else None
        elif "spotify" in key and "monthly_listeners" in key:
            monthly_listeners = metrics[0].value if metrics else None
        elif "followers" in key:
            platform = key.split("_")[0]
            followers[platform] = metrics[0].value if metrics else 0
    
    # Calculate growth rates (simplified - compare last 2 weeks)
    two_weeks_ago = date.today() - timedelta(days=14)
    week_ago = date.today() - timedelta(days=7)
    
    for key, metrics in platform_metrics.items():
        recent = [m for m in metrics if m.date >= week_ago]
        old = [m for m in metrics if two_weeks_ago <= m.date < week_ago]
        
        if recent and old:
            recent_val = recent[0].value or 0
            old_val = old[0].value or 0
            if old_val > 0:
                growth = ((recent_val - old_val) / old_val) * 100
                growth_rates[key] = round(growth, 2)
    
    return MetricsOverviewResponse(
        total_streams=total_streams,
        monthly_listeners=monthly_listeners,
        followers=followers,
        growth_rates=growth_rates,
        last_updated=datetime.utcnow() if latest_metrics else None
    )


@router.get("/platform/{platform}", response_model=PlatformMetricsResponse)
async def get_platform_metrics(
    platform: str,
    days: int = Query(30, ge=1, le=365),
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get platform-specific metrics"""
    start_date = date.today() - timedelta(days=days)
    
    metrics = db.query(DailyMetric).filter(
        DailyMetric.artist_id == artist.artist_id,
        DailyMetric.platform == platform.lower(),
        DailyMetric.date >= start_date
    ).order_by(DailyMetric.date.desc()).all()
    
    return PlatformMetricsResponse(
        platform=platform,
        metrics=metrics,
        summary={}
    )


@router.get("/growth")
async def get_growth_trends(
    days: int = Query(30, ge=1, le=365),
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get growth trends over time"""
    start_date = date.today() - timedelta(days=days)
    
    metrics = db.query(DailyMetric).filter(
        DailyMetric.artist_id == artist.artist_id,
        DailyMetric.date >= start_date
    ).order_by(DailyMetric.date.asc()).all()
    
    # Group by date and platform
    trends = {}
    for metric in metrics:
        date_str = str(metric.date)
        if date_str not in trends:
            trends[date_str] = {}
        if metric.platform not in trends[date_str]:
            trends[date_str][metric.platform] = {}
        trends[date_str][metric.platform][metric.metric_name] = metric.value
    
    return {"trends": trends}

