# Pydantic schemas for request/response validation
from backend.schemas.auth import UserSignup, UserLogin, Token, UserResponse
from backend.schemas.artist import ArtistBase, ArtistCreate, ArtistUpdate, ArtistResponse
from backend.schemas.connection import ConnectionResponse, ConnectionListResponse, OAuthURLResponse
from backend.schemas.metric import DailyMetricResponse, MetricsOverviewResponse, PlatformMetricsResponse
from backend.schemas.content import (
    ContentPostBase, ContentPostCreate, ContentPostUpdate, ContentPostResponse,
    ContentPerformanceResponse
)
from backend.schemas.ai import (
    GenerateIdeasRequest, GenerateIdeasResponse,
    GenerateCaptionRequest, GenerateCaptionResponse,
    PredictPerformanceRequest, PredictPerformanceResponse,
    WeeklyInsightsResponse
)

__all__ = [
    "UserSignup", "UserLogin", "Token", "UserResponse",
    "ArtistBase", "ArtistCreate", "ArtistUpdate", "ArtistResponse",
    "ConnectionResponse", "ConnectionListResponse", "OAuthURLResponse",
    "DailyMetricResponse", "MetricsOverviewResponse", "PlatformMetricsResponse",
    "ContentPostBase", "ContentPostCreate", "ContentPostUpdate", "ContentPostResponse",
    "ContentPerformanceResponse",
    "GenerateIdeasRequest", "GenerateIdeasResponse",
    "GenerateCaptionRequest", "GenerateCaptionResponse",
    "PredictPerformanceRequest", "PredictPerformanceResponse",
    "WeeklyInsightsResponse",
]
