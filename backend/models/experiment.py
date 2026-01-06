"""
Experiment model - A/B tests
"""
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID, JSONType


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), default="active")  # 'active', 'completed', 'cancelled'
    results = Column(JSONType(), nullable=True)  # store statistical results
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="experiments")

