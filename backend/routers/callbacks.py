"""
OAuth callback routes
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.connection import PlatformConnection
from backend.utils.oauth import decode_state
from backend.utils.encryption import encrypt_token
from backend.services.spotify_service import SpotifyService
from backend.services.instagram_service import InstagramService
from backend.services.tiktok_service import TikTokService
from backend.services.youtube_service import YouTubeService
from backend.config import settings
from datetime import datetime, timedelta
from urllib.parse import urlencode

router = APIRouter()


@router.get("/spotify")
async def callback_spotify(
    code: str = Query(...),
    state: str = Query(...),
    error: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle Spotify OAuth callback"""
    # Get frontend URL for redirect
    frontend_url = settings.FRONTEND_URL or "http://localhost:5173"
    
    # Handle OAuth errors
    if error:
        error_params = urlencode({"error": error, "platform": "spotify"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")
    
    artist_id = decode_state(state)
    if not artist_id:
        error_params = urlencode({"error": "invalid_state", "platform": "spotify"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")
    
    try:
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
        
        # Redirect to frontend with success message
        success_params = urlencode({"connected": "spotify", "message": "Spotify connected successfully"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{success_params}")
    except Exception as e:
        error_params = urlencode({"error": str(e), "platform": "spotify"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")


@router.get("/instagram")
async def callback_instagram(
    code: str = Query(...),
    state: str = Query(...),
    error: str = Query(None),
    error_reason: str = Query(None),
    db: Session = Depends(get_db)
):
    """Handle Instagram OAuth callback"""
    # Get frontend URL for redirect
    frontend_url = settings.FRONTEND_URL or "http://localhost:5173"
    
    # Handle OAuth errors
    if error:
        error_msg = error_reason or error
        error_params = urlencode({"error": error_msg, "platform": "instagram"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")
    
    artist_id = decode_state(state)
    if not artist_id:
        error_params = urlencode({"error": "invalid_state", "platform": "instagram"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")
    
    try:
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
        
        # Redirect to frontend with success message
        success_params = urlencode({"connected": "instagram", "message": "Instagram connected successfully"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{success_params}")
    except Exception as e:
        error_params = urlencode({"error": str(e), "platform": "instagram"})
        return RedirectResponse(url=f"{frontend_url}/dashboard?{error_params}")


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


@router.get("/instagram/webhook")
async def verify_instagram_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    """
    Facebook/Instagram webhook verification endpoint
    Facebook will send a GET request to verify the webhook
    Must return the challenge as plain text (not JSON)
    """
    from fastapi.responses import PlainTextResponse
    
    verify_token = settings.INSTAGRAM_WEBHOOK_VERIFY_TOKEN
    
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        # Return the challenge token as plain text to verify the webhook
        return PlainTextResponse(content=hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/instagram/webhook")
async def handle_instagram_webhook():
    """
    Handle Instagram webhook events (e.g., media updates, user updates)
    This endpoint receives POST requests from Facebook/Instagram
    """
    # For now, just acknowledge receipt
    # In the future, you can process webhook events here
    return {"status": "ok"}

