"""
User model for authentication
"""
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
import uuid
from backend.database import Base, GUID


class User(Base):
    __tablename__ = "users"

    user_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    artists = relationship("Artist", back_populates="user", cascade="all, delete-orphan")

