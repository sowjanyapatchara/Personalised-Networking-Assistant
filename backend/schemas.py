from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    name: Optional[str] = None
    bio: str = Field(..., min_length=3, description="User's short profile bio")
    event_description: str = Field(..., min_length=3, description="Description of the networking event")
    interests: Optional[str] = Field(None, description="Comma-separated interests, e.g. 'climate change, urban planning'")


class GenerateResponse(BaseModel):
    interaction_id: int
    themes: List[str]
    starters: List[str]
    created_at: datetime


class VerifyResponse(BaseModel):
    query: str
    found: bool
    summary: Optional[str] = None
    source_url: Optional[str] = None


class FeedbackRequest(BaseModel):
    interaction_id: int
    useful: bool


class HistoryItem(BaseModel):
    id: int
    event_description: str
    interests: Optional[str]
    themes: List[str]
    starters: List[str]
    created_at: datetime
    feedback: Optional[bool] = None

    class Config:
        from_attributes = True
