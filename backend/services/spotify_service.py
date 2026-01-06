"""
Spotify API integration service
"""
import httpx
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from backend.config import settings
from backend.utils.encryption import encrypt_token, decrypt_token
from backend.utils.oauth import generate_oauth_url


class SpotifyService:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_BASE = "https://api.spotify.com/v1"
    
    SCOPES = [
        "user-read-email",
        "user-read-private",
        "user-read-recently-played",
        "user-top-read",
        "user-read-playback-state",
        "user-read-currently-playing",
        "playlist-read-private",
        "playlist-read-collaborative",
    ]
    
    @staticmethod
    def get_auth_url(artist_id: str, state: str) -> str:
        """Generate Spotify OAuth URL"""
        return generate_oauth_url(
            base_url=SpotifyService.AUTH_URL,
            client_id=settings.SPOTIFY_CLIENT_ID,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scopes=SpotifyService.SCOPES,
            state=state
        )
    
    @staticmethod
    async def exchange_code(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SpotifyService.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
                    "client_id": settings.SPOTIFY_CLIENT_ID,
                    "client_secret": settings.SPOTIFY_CLIENT_SECRET,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SpotifyService.TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": settings.SPOTIFY_CLIENT_ID,
                    "client_secret": settings.SPOTIFY_CLIENT_SECRET,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_artist_stats(access_token: str) -> Dict[str, Any]:
        """Get artist statistics from Spotify"""
        # Note: Spotify API doesn't directly provide artist stats
        # This would need to use Spotify for Artists API or track streams differently
        # For now, return a placeholder structure
        async with httpx.AsyncClient() as client:
            # Get user profile
            response = await client.get(
                f"{SpotifyService.API_BASE}/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()

