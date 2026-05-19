from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class SubmissionCreate(BaseModel):
    """Schema for creating a submission"""

    problem_id: int
    code: str = Field(..., min_length=1)
    language: str = Field(..., pattern="^(python|cpp)$")


class SubmissionResponse(BaseModel):
    """Schema for submission response"""

    id: int
    user_id: int
    problem_id: int
    code: str
    language: str
    status: str
    execution_time: Optional[int] = None
    memory_used: Optional[float] = None
    created_at: datetime

    # Include testcase results summary
    passed_testcases: int = 0
    total_testcases: int = 0
    score: float = 0.0  # Weighted score

    class Config:
        from_attributes = True


class SubmissionResult(BaseModel):
    """Schema for submission execution result"""

    submission_id: int
    status: str
    passed_testcases: int
    total_testcases: int

    # Separate counts for sample and hidden tests
    sample_passed: int = 0
    sample_total: int = 0
    hidden_passed: int = 0
    hidden_total: int = 0

    score: float = 0.0  # Weighted score (0-100)
    max_score: float = 100.0  # Maximum possible score
    execution_time: Optional[int] = None
    memory_used: Optional[float] = None

    # Detailed results (only sample testcases shown)
    sample_results: List[dict] = []

    # Overall feedback
    message: Optional[str] = None


class SubmissionDetailResponse(BaseModel):
    """Detailed submission with testcase results"""

    id: int
    user_id: int
    problem_id: int
    code: str
    language: str
    status: str
    execution_time: Optional[int] = None
    memory_used: Optional[float] = None
    created_at: datetime
    score: float = 0.0  # Weighted score (0-100)

    # Testcase results
    testcase_results: List[dict] = []

    # AI feedback if available
    has_ai_feedback: bool = False

    class Config:
        from_attributes = True
