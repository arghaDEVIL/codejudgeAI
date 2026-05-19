from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AIFeedbackResponse(BaseModel):
    """Schema for AI feedback response"""

    id: int
    submission_id: int
    overall_feedback: str
    error_analysis: Optional[str] = None
    optimization_hints: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    code_quality_score: Optional[int] = Field(None, ge=0, le=100)
    model_used: str
    generated_at: datetime

    class Config:
        from_attributes = True


class AIFeedbackRequest(BaseModel):
    """Schema for requesting AI feedback"""

    submission_id: int
