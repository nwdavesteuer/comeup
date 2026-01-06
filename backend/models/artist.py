"""
Artist model - represents a music artist account
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
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

