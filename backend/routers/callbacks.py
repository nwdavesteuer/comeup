"""
OAuth callback routes
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.connection import PlatformConnection
from backend.utils.oauth import decode_state
from backend.utils.encryption import encrypt_token
from backend.services.spotify_service import SpotifyService
from backend.services.instagram_service import InstagramService
from backend.services.tiktok_service import TikTokService
from backend.services.youtube_service import YouTubeService
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/spotify")
async def callback_spotify(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle Spotify OAuth callback"""
    artist_id = decode_state(state)
    if not artist_id:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Exchange code for tokens
    tokens = await SpotifyService.exchange_code(code)
    
    # Store connection
    expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    
    connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist_id,
        PlatformConnection.platform == "spotify"
    ).first()
    
    if connection:
        connection.access_token = encrypt_token(tokens["access_token"])
        connection.refresh_token = encrypt_token(tokens.get("refresh_token", ""))
        connection.token_expires_at = expires_at
        connection.is_active = True
    else:
        connection = PlatformConnection(
            artist_id=artist_id,
            platform="spotify",
            access_token=encrypt_token(tokens["access_token"]),
            refresh_token=encrypt_token(tokens.get("refresh_token", "")),
            token_expires_at=expires_at,
            is_active=True
        )
        db.add(connection)
    
    db.commit()
    return {"message": "Spotify connected successfully"}


@router.get("/instagram")
async def callback_instagram(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle Instagram OAuth callback"""
    artist_id = decode_state(state)
    if not artist_id:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    tokens = await InstagramService.exchange_code(code)
    expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    
    connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist_id,
        PlatformConnection.platform == "instagram"
    ).first()
    
    if connection:
        connection.access_token = encrypt_token(tokens["access_token"])
        connection.token_expires_at = expires_at
        connection.is_active = True
    else:
        connection = PlatformConnection(
            artist_id=artist_id,
            platform="instagram",
            access_token=encrypt_token(tokens["access_token"]),
            token_expires_at=expires_at,
            is_active=True
        )
        db.add(connection)
    
    db.commit()
    return {"message": "Instagram connected successfully"}


@router.get("/tiktok")
async def callback_tiktok(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle TikTok OAuth callback"""
    artist_id = decode_state(state)
    if not artist_id:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    tokens = await TikTokService.exchange_code(code)
    expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    
    connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist_id,
        PlatformConnection.platform == "tiktok"
    ).first()
    
    if connection:
        connection.access_token = encrypt_token(tokens["access_token"])
        connection.refresh_token = encrypt_token(tokens.get("refresh_token", ""))
        connection.token_expires_at = expires_at
        connection.is_active = True
    else:
        connection = PlatformConnection(
            artist_id=artist_id,
            platform="tiktok",
            access_token=encrypt_token(tokens["access_token"]),
            refresh_token=encrypt_token(tokens.get("refresh_token", "")),
            token_expires_at=expires_at,
            is_active=True
        )
        db.add(connection)
    
    db.commit()
    return {"message": "TikTok connected successfully"}


@router.get("/youtube")
async def callback_youtube(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle YouTube OAuth callback"""
    artist_id = decode_state(state)
    if not artist_id:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    tokens = await YouTubeService.exchange_code(code)
    expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    
    connection = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist_id,
        PlatformConnection.platform == "youtube"
    ).first()
    
    if connection:
        connection.access_token = encrypt_token(tokens["access_token"])
        connection.refresh_token = encrypt_token(tokens.get("refresh_token", ""))
        connection.token_expires_at = expires_at
        connection.is_active = True
    else:
        connection = PlatformConnection(
            artist_id=artist_id,
            platform="youtube",
            access_token=encrypt_token(tokens["access_token"]),
            refresh_token=encrypt_token(tokens.get("refresh_token", "")),
            token_expires_at=expires_at,
            is_active=True
        )
        db.add(connection)
    
    db.commit()
    return {"message": "YouTube connected successfully"}

