from pydantic import BaseModel
from typing import Optional


class TestcaseResultResponse(BaseModel):
    """Schema for testcase result"""

    id: int
    submission_id: int
    testcase_id: int
    status: str
    actual_output: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: Optional[int] = None  # ms
    memory_used: Optional[float] = None  # MB

    # Include testcase info
    testcase_is_sample: bool
    testcase_description: Optional[str] = None

    class Config:
        from_attributes = True
