from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProblemCreate(BaseModel):
    """Schema for creating a problem"""

    title: str = Field(..., min_length=3, max_length=200)
    statement: str = Field(..., min_length=10)
    difficulty: str = Field(..., pattern="^(Easy|Medium|Hard)$")
    tags: Optional[List[str]] = Field(
        default=[], description="Topic tags for the problem"
    )
    expected_output: Optional[str] = None


class ProblemResponse(BaseModel):
    """Schema for problem response"""

    id: int
    title: str
    statement: str
    difficulty: str
    tags: Optional[List[str]] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
