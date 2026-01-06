"""
Instagram/Facebook API integration service
"""
import httpx
from typing import Optional, Dict, Any
from backend.config import settings
from backend.utils.oauth import generate_oauth_url


class InstagramService:
    AUTH_URL = "https://api.instagram.com/oauth/authorize"
    TOKEN_URL = "https://api.instagram.com/oauth/access_token"
    API_BASE = "https://graph.instagram.com"
    
    SCOPES = [
        "user_profile",
        "user_media",
    ]
    
    @staticmethod
    def get_auth_url(artist_id: str, state: str) -> str:
        """Generate Instagram OAuth URL"""
        return generate_oauth_url(
            base_url=InstagramService.AUTH_URL,
            client_id=settings.INSTAGRAM_APP_ID,
            redirect_uri=settings.INSTAGRAM_REDIRECT_URI,
            scopes=InstagramService.SCOPES,
            state=state
        )
    
    @staticmethod
    async def exchange_code(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                InstagramService.TOKEN_URL,
                data={
                    "client_id": settings.INSTAGRAM_APP_ID,
                    "client_secret": settings.INSTAGRAM_APP_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
                    "code": code,
                },
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_user_insights(access_token: str) -> Dict[str, Any]:
        """Get Instagram user insights"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{InstagramService.API_BASE}/me",
                params={
                    "fields": "id,username,account_type,media_count",
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json()

