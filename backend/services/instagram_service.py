"""
Instagram/Facebook API integration service
"""
import httpx
from typing import Optional, Dict, Any
from backend.config import settings
from backend.utils.oauth import generate_oauth_url


class InstagramService:
    # Instagram Graph API uses Facebook OAuth endpoints
    AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
    TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    API_BASE = "https://graph.instagram.com"
    
    # Instagram Graph API scopes
    SCOPES = [
        "instagram_basic",
        "instagram_content_publish",
        "pages_read_engagement",  # Required for Instagram Graph API
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
        """Exchange authorization code for access token using Facebook OAuth"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                InstagramService.TOKEN_URL,
                params={
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

