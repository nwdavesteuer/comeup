"""
Content schedule schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import date


class ContentScheduleItem(BaseModel):
    """A single content item in the schedule"""
    day: str
    date: str
    platform: str
    content_type: str
    idea: str
    time_suggestion: str
    estimated_time: str


class ContentScheduleResponse(BaseModel):
    """Full content schedule response"""
    schedule: List[ContentScheduleItem]
    summary: Dict[str, Any]


class ScheduleApprovalRequest(BaseModel):
    """Request to approve or modify schedule"""
    approved: bool
    modifications: List[Dict[str, Any]] = Field(default_factory=list, description="Any modifications to specific items")

