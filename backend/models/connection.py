"""
Platform connection model - stores OAuth tokens for each platform
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base


class PlatformConnection(Base):
    __tablename__ = "platform_connections"

    connection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.artist_id"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)  # 'spotify', 'instagram', 'tiktok', 'youtube'
    access_token = Column(String, nullable=True)  # encrypted
    refresh_token = Column(String, nullable=True)  # encrypted
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    last_sync = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    artist = relationship("Artist", back_populates="platform_connections")

    # Unique constraint: one active connection per artist per platform
    __table_args__ = (
        Index('idx_platform_connections_artist_platform', 'artist_id', 'platform', unique=True),
    )

