"""
Platform connection schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ConnectionResponse(BaseModel):
    connection_id: UUID
    artist_id: UUID
    platform: str
    connected_at: datetime
    last_sync: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True


class ConnectionListResponse(BaseModel):
    connections: list[ConnectionResponse]


class OAuthURLResponse(BaseModel):
    auth_url: str
    state: str

