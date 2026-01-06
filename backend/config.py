"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    # Default to SQLite for local development (no setup needed)
    # For production, use PostgreSQL: postgresql://user:password@host:5432/dbname
    DATABASE_URL: str = "sqlite:///./fanbase_builder.db"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8000"
    ]
    FRONTEND_URL: str = ""  # Production frontend URL (set in production)
    
    # Spotify API
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8000/api/callback/spotify"
    
    # Instagram/Facebook API
    INSTAGRAM_APP_ID: str = ""
    INSTAGRAM_APP_SECRET: str = ""
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:8000/api/callback/instagram"
    INSTAGRAM_WEBHOOK_VERIFY_TOKEN: str = "comeup_instagram_webhook_verify_token_2024"
    
    # TikTok API
    TIKTOK_CLIENT_KEY: str = ""
    TIKTOK_CLIENT_SECRET: str = ""
    TIKTOK_REDIRECT_URI: str = "http://localhost:8000/api/callback/tiktok"
    
    # YouTube API
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""
    YOUTUBE_REDIRECT_URI: str = "http://localhost:8000/api/callback/youtube"
    
    # Claude API
    ANTHROPIC_API_KEY: str = ""
    
    # AWS S3 (optional for MVP)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""
    
    # Redis (optional for MVP)
    REDIS_URL: str = "redis://localhost:6379"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


settings = Settings()

