"""
Onboarding model - stores artist persona data from onboarding interview
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID, JSONType


class OnboardingResponse(Base):
    __tablename__ = "onboarding_responses"

    response_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    artist_id = Column(GUID(), ForeignKey("artists.artist_id"), nullable=False, unique=True, index=True)
    
    # Question 1: Content creation time
    content_hours_per_week = Column(String(50), nullable=True)  # 'less_than_2', '2_5', '5_10', '10_15', 'more_than_15'
    
    # Question 2: Live performances
    performs_live = Column(String(50), nullable=True)  # 'regularly', 'occasionally', 'planning', 'no'
    
    # Question 3: Content types (stored as JSON array)
    preferred_content_types = Column(JSONType(), nullable=True)  # ['behind_scenes', 'music_snippets', etc.]
    
    # Question 4: Music inspiration
    inspiring_artists = Column(Text, nullable=True)  # Comma-separated list or JSON
    genre_fallback = Column(String(100), nullable=True)  # If they said "not sure"
    
    # Question 5: Visual style (stored as JSON array)
    visual_styles = Column(JSONType(), nullable=True)  # ['natural', 'vintage', etc.]
    visual_style_followup = Column(JSONType(), nullable=True)  # For narrowing down
    
    # Question 6: Top challenges (stored as JSON array)
    top_challenges = Column(JSONType(), nullable=True)  # ['ideas', 'time', 'consistency', etc.]
    
    # Question 7: What's working (stored as JSON array)
    whats_working = Column(JSONType(), nullable=True)  # ['behind_scenes', 'music_snippets', etc.]
    
    # Question 8: Upcoming music
    upcoming_music = Column(String(50), nullable=True)  # 'soon', 'unreleased', 'working', 'existing', 'not_yet'
    release_timeline = Column(String(50), nullable=True)  # 'within_month', '1_3_months', '3_6_months', '6_plus_months', 'flexible'
    specific_release_date = Column(DateTime(timezone=True), nullable=True)  # If they provided exact date
    
    # Question 9: Collaborations
    collaboration_plans = Column(String(50), nullable=True)  # 'coming_up', 'open', 'maybe', 'no'
    
    # Question 10: Upcoming content
    upcoming_content = Column(Text, nullable=True)  # Free text about content they plan to post soon
    
    # Metadata
    current_question = Column(String(50), nullable=True)  # Track progress: 'content_time', 'live_performances', etc.
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    artist = relationship("Artist", back_populates="onboarding_response")

