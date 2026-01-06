"""
YouTube API integration service
"""
import httpx
from typing import Optional, Dict, Any
from backend.config import settings
from backend.utils.oauth import generate_oauth_url


class YouTubeService:
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    API_BASE = "https://www.googleapis.com/youtube/v3"
    
    SCOPES = [
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/youtube.upload",
    ]
    
    @staticmethod
    def get_auth_url(artist_id: str, state: str) -> str:
        """Generate YouTube OAuth URL"""
        return generate_oauth_url(
            base_url=YouTubeService.AUTH_URL,
            client_id=settings.YOUTUBE_CLIENT_ID,
            redirect_uri=settings.YOUTUBE_REDIRECT_URI,
            scopes=YouTubeService.SCOPES,
            state=state
        )
    
    @staticmethod
    async def exchange_code(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                YouTubeService.TOKEN_URL,
                data={
                    "client_id": settings.YOUTUBE_CLIENT_ID,
                    "client_secret": settings.YOUTUBE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.YOUTUBE_REDIRECT_URI,
                },
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                YouTubeService.TOKEN_URL,
                data={
                    "client_id": settings.YOUTUBE_CLIENT_ID,
                    "client_secret": settings.YOUTUBE_CLIENT_SECRET,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_channel_stats(access_token: str) -> Dict[str, Any]:
        """Get YouTube channel statistics"""
        async with httpx.AsyncClient() as client:
            # First get channel ID
            response = await client.get(
                f"{YouTubeService.API_BASE}/channels",
                params={
                    "part": "snippet,statistics",
                    "mine": "true",
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json()

