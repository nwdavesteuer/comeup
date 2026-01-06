"""
TikTok API integration service
"""
import httpx
from typing import Optional, Dict, Any
from backend.config import settings
from backend.utils.oauth import generate_oauth_url


class TikTokService:
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize"
    TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
    API_BASE = "https://open.tiktokapis.com/v2"
    
    SCOPES = [
        "user.info.basic",
        "video.list",
        "video.upload",
    ]
    
    @staticmethod
    def get_auth_url(artist_id: str, state: str) -> str:
        """Generate TikTok OAuth URL"""
        return generate_oauth_url(
            base_url=TikTokService.AUTH_URL,
            client_id=settings.TIKTOK_CLIENT_KEY,
            redirect_uri=settings.TIKTOK_REDIRECT_URI,
            scopes=TikTokService.SCOPES,
            state=state
        )
    
    @staticmethod
    async def exchange_code(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TikTokService.TOKEN_URL,
                json={
                    "client_key": settings.TIKTOK_CLIENT_KEY,
                    "client_secret": settings.TIKTOK_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.TIKTOK_REDIRECT_URI,
                },
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TikTokService.TOKEN_URL,
                json={
                    "client_key": settings.TIKTOK_CLIENT_KEY,
                    "client_secret": settings.TIKTOK_CLIENT_SECRET,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_user_stats(access_token: str) -> Dict[str, Any]:
        """Get TikTok user statistics"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{TikTokService.API_BASE}/user/info/",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"fields": "display_name,avatar_url,follower_count,following_count"}
            )
            response.raise_for_status()
            return response.json()

