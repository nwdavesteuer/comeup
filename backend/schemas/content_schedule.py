"""
Content schedule schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import date


class ShotListItem(BaseModel):
    """A single shot in the shot list"""
    shot: str
    time_range: str
    description: str


class VisualDirection(BaseModel):
    """Visual direction for content"""
    color_palette: str
    style_description: str


class ContentScheduleItem(BaseModel):
    """A single content item in the schedule"""
    content_name: str
    date: str
    activity_type: str  # 'filming', 'editing', or 'posting'
    platform: str
    format: str  # 'reel', 'post', 'carousel', 'tiktok_video', 'story'
    
    # Filming-specific fields
    visual_direction: Optional[Dict[str, str]] = None
    content_description: Optional[str] = None
    shot_list: Optional[List[Dict[str, str]]] = None
    setup_time: Optional[str] = None
    filming_duration: Optional[str] = None
    
    # Editing-specific fields
    editing_duration: Optional[str] = None
    
    # Posting-specific fields
    posting_time: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None


class ContentScheduleResponse(BaseModel):
    """Full content schedule response"""
    schedule: List[ContentScheduleItem]
    summary: Dict[str, Any]


class ScheduleApprovalRequest(BaseModel):
    """Request to approve or modify schedule"""
    approved: bool
    modifications: List[Dict[str, Any]] = Field(default_factory=list, description="Any modifications to specific items")

