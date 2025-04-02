from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReviewCreate(BaseModel):
    entity_id: UUID
    rating: float
    comment: str | None = None

class ReviewResponse(BaseModel):
    id: UUID
    entity_id: UUID
    rating: float
    comment: str | None
    timestamp: datetime

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None