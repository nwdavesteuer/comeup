"""
Prediction model - stores ML predictions
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, index=True)
    post_id = Column(GUID(), ForeignKey("content_posts.post_id"), nullable=True, index=True)
    prediction_type = Column(String(50), nullable=False)  # 'engagement_rate', 'streams_lift', 'viral_probability'
    predicted_value = Column(Numeric(10, 4), nullable=True)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="predictions")
    post = relationship("ContentPost", back_populates="predictions")

