"""
Authentication service
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.user import User
from backend.models.artist import Artist
from backend.schemas.auth import UserSignup, UserLogin
from backend.utils.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from backend.config import settings


class AuthService:
    @staticmethod
    def signup(db: Session, user_data: UserSignup) -> tuple[User, Artist]:
        """Create a new user and artist account"""
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password)
        )
        db.add(user)
        db.flush()  # Get user_id
        
        # Create artist
        artist = Artist(
            user_id=user.user_id,
            artist_name=user_data.artist_name,
            genre=user_data.genre,
            subscription_tier="free"
        )
        db.add(artist)
        db.commit()
        db.refresh(user)
        db.refresh(artist)
        
        return user, artist
    
    @staticmethod
    def login(db: Session, login_data: UserLogin) -> str:
        """Authenticate user and return JWT token"""
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Update last login
        from datetime import datetime
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.user_id)},
            expires_delta=access_token_expires
        )
        
        return access_token

