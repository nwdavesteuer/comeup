"""
Artist model - represents a music artist account
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.user_id"), nullable=False, index=True)
    artist_name = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=True)
    subscription_tier = Column(String(50), default="free")  # 'free', 'pro', 'premium'
    onboarding_complete = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="artists")
    platform_connections = relationship("PlatformConnection", back_populates="artist", cascade="all, delete-orphan")
    daily_metrics = relationship("DailyMetric", back_populates="artist", cascade="all, delete-orphan")
    content_posts = relationship("ContentPost", back_populates="artist", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="artist", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="artist", cascade="all, delete-orphan")
    onboarding_response = relationship("OnboardingResponse", back_populates="artist", uselist=False, cascade="all, delete-orphan")

