"""
Encryption utilities for storing OAuth tokens securely
"""
from cryptography.fernet import Fernet
from backend.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """
    Generate encryption key from SECRET_KEY.
    In production, use a dedicated encryption key.
    """
    # Use first 32 bytes of SHA256 hash of SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_token(token: str) -> str:
    """Encrypt a token for storage"""
    if not token:
        return ""
    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(token.encode())
    return encrypted.decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a stored token"""
    if not encrypted_token:
        return ""
    try:
        f = Fernet(get_encryption_key())
        decrypted = f.decrypt(encrypted_token.encode())
        return decrypted.decode()
    except Exception:
        return ""

