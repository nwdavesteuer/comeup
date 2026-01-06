"""
Platform connection routes (OAuth)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.artist import Artist
from backend.models.connection import PlatformConnection
from backend.schemas.connection import ConnectionResponse, ConnectionListResponse, OAuthURLResponse
from backend.utils.auth import get_current_artist
from backend.utils.oauth import encode_state
from backend.services.spotify_service import SpotifyService
from backend.services.instagram_service import InstagramService
from backend.services.tiktok_service import TikTokService
from backend.services.youtube_service import YouTubeService

router = APIRouter()


@router.get("/spotify", response_model=OAuthURLResponse)
async def connect_spotify(artist: Artist = Depends(get_current_artist)):
    """Generate Spotify OAuth URL"""
    state = encode_state(str(artist.artist_id))
    auth_url = SpotifyService.get_auth_url(str(artist.artist_id), state)
    return {"auth_url": auth_url, "state": state}


@router.get("/instagram", response_model=OAuthURLResponse)
async def connect_instagram(artist: Artist = Depends(get_current_artist)):
    """Generate Instagram OAuth URL"""
    state = encode_state(str(artist.artist_id))
    auth_url = InstagramService.get_auth_url(str(artist.artist_id), state)
    return {"auth_url": auth_url, "state": state}


@router.get("/tiktok", response_model=OAuthURLResponse)
async def connect_tiktok(artist: Artist = Depends(get_current_artist)):
    """Generate TikTok OAuth URL"""
    state = encode_state(str(artist.artist_id))
    auth_url = TikTokService.get_auth_url(str(artist.artist_id), state)
    return {"auth_url": auth_url, "state": state}


@router.get("/youtube", response_model=OAuthURLResponse)
async def connect_youtube(artist: Artist = Depends(get_current_artist)):
    """Generate YouTube OAuth URL"""
    state = encode_state(str(artist.artist_id))
    auth_url = YouTubeService.get_auth_url(str(artist.artist_id), state)
    return {"auth_url": auth_url, "state": state}


@router.get("", response_model=ConnectionListResponse)
async def list_connections(
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """List all platform connections for current artist"""
    connections = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist.artist_id,
        PlatformConnection.is_active == True
    ).all()
    
    return {"connections": connections}


@router.delete("/{platform}")
async def disconnect_platform(
    platform: str,
    artist: Artist = Depends(get_current_artist),
    db: Session = Depends(get_db)
):
    """Disconnect a platform"""
    connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist.artist_id,
        PlatformConnection.platform == platform.lower()
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    connection.is_active = False
    db.commit()
    return {"message": f"{platform} disconnected successfully"}

