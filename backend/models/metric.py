"""
Daily metrics model - time-series data for each platform
"""
from sqlalchemy import Column, String, Date, BigInteger, DateTime, ForeignKey, func, Index, UniqueConstraint
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID


class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    metric_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    platform = Column(String(50), nullable=False)  # 'spotify', 'instagram', 'tiktok', 'youtube'
    metric_name = Column(String(100), nullable=False)  # 'monthly_listeners', 'followers', 'streams', etc.
    value = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="daily_metrics")

    # Unique constraint: one metric per artist per date per platform per metric_name
    __table_args__ = (
        UniqueConstraint('artist_id', 'date', 'platform', 'metric_name', name='uq_daily_metrics'),
        Index('idx_daily_metrics_artist_date', 'artist_id', 'date'),
    )

