"""
OAuth helper utilities
"""
from jose import jwt
from backend.config import settings
from datetime import datetime, timedelta
from typing import Optional


def encode_state(artist_id: str) -> str:
    """Encode artist_id into JWT state parameter for OAuth"""
    payload = {
        "artist_id": artist_id,
        "exp": datetime.utcnow() + timedelta(minutes=10)  # 10 minute expiry
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_state(state: str) -> Optional[str]:
    """Decode JWT state parameter to get artist_id"""
    try:
        payload = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("artist_id")
    except Exception:
        return None


def generate_oauth_url(
    base_url: str,
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    state: str
) -> str:
    """Generate OAuth authorization URL"""
    scope_string = " ".join(scopes)
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope_string,
        "state": state,
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{query_string}"

