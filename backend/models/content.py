"""
Content models - posts and their performance tracking
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Numeric, func, Index
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID


class ContentPost(Base):
    __tablename__ = "content_posts"

    post_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)  # 'spotify', 'instagram', 'tiktok', 'youtube'
    content_type = Column(String(50), nullable=False)  # 'reel', 'story', 'tiktok', 'youtube_short', 'post'
    caption = Column(Text, nullable=True)
    media_url = Column(Text, nullable=True)
    external_url = Column(Text, nullable=True)  # link to actual post on platform
    posted_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="draft")  # 'draft', 'scheduled', 'published', 'failed'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="content_posts")
    performance = relationship("ContentPerformance", back_populates="post", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="post", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_content_posts_artist', 'artist_id', 'posted_at'),
    )


class ContentPerformance(Base):
    __tablename__ = "content_performance"

    performance_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    post_id = Column(GUID(), ForeignKey("content_posts.post_id"), nullable=False, index=True)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, index=True)
    measured_at = Column(DateTime(timezone=True), nullable=False)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagement_rate = Column(Numeric(5, 4), nullable=True)
    spotify_traffic_lift = Column(Integer, nullable=True)  # streams increase in 48hr window
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("ContentPost", back_populates="performance")
    artist = relationship("Artist")

