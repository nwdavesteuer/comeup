"""
Content management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.content import ContentPost, ContentPerformance
from backend.schemas.content import (
    ContentPostCreate, ContentPostUpdate, ContentPostResponse,
    ContentPerformanceResponse
)
from backend.utils.auth import get_current_artist
from datetime import datetime
from uuid import UUID

router = APIRouter()


@router.get("", response_model=list[ContentPostResponse])
async def list_content(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """List all content posts"""
    posts = db.query(ContentPost).filter(
        ContentPost.artist_id == artist.artist_id
    ).order_by(ContentPost.created_at.desc()).offset(offset).limit(limit).all()
    
    return posts


@router.post("", response_model=ContentPostResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    post_data: ContentPostCreate,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Create or schedule a new post"""
    post = ContentPost(
        artist_id=artist.artist_id,
        platform=post_data.platform,
        content_type=post_data.content_type,
        caption=post_data.caption,
        media_url=post_data.media_url,
        scheduled_for=post_data.scheduled_for,
        status="scheduled" if post_data.scheduled_for else "draft"
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{post_id}", response_model=ContentPostResponse)
async def get_content(
    post_id: UUID,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get post details"""
    post = db.query(ContentPost).filter(
        ContentPost.post_id == post_id,
        ContentPost.artist_id == artist.artist_id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post


@router.put("/{post_id}", response_model=ContentPostResponse)
async def update_content(
    post_id: UUID,
    post_data: ContentPostUpdate,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Update a post"""
    post = db.query(ContentPost).filter(
        ContentPost.post_id == post_id,
        ContentPost.artist_id == artist.artist_id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_data.caption is not None:
        post.caption = post_data.caption
    if post_data.media_url is not None:
        post.media_url = post_data.media_url
    if post_data.scheduled_for is not None:
        post.scheduled_for = post_data.scheduled_for
    if post_data.status is not None:
        post.status = post_data.status
    
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    post_id: UUID,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Delete a post"""
    post = db.query(ContentPost).filter(
        ContentPost.post_id == post_id,
        ContentPost.artist_id == artist.artist_id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return None


@router.get("/calendar")
async def get_content_calendar(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None
):
    """Get calendar view of scheduled content"""
    query = db.query(ContentPost).filter(
        ContentPost.artist_id == artist.artist_id,
        ContentPost.scheduled_for.isnot(None)
    )
    
    if start_date:
        query = query.filter(ContentPost.scheduled_for >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(ContentPost.scheduled_for <= datetime.fromisoformat(end_date))
    
    posts = query.order_by(ContentPost.scheduled_for.asc()).all()
    return {"posts": posts}


@router.get("/{post_id}/performance", response_model=list[ContentPerformanceResponse])
async def get_content_performance(
    post_id: UUID,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Get performance data for a post"""
    # Verify post belongs to artist
    post = db.query(ContentPost).filter(
        ContentPost.post_id == post_id,
        ContentPost.artist_id == artist.artist_id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    performance = db.query(ContentPerformance).filter(
        ContentPerformance.post_id == post_id
    ).order_by(ContentPerformance.measured_at.desc()).all()
    
    return performance

