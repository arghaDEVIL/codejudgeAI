from pydantic import BaseModel, Field
from typing import Optional


class TestcaseCreate(BaseModel):
    """Schema for creating a testcase"""

    problem_id: int
    stdin: str
    expected_output: str
    is_sample: bool = False
    weight: int = Field(default=1, ge=1, le=100)
    time_limit: int = Field(default=2000, ge=100, le=10000)  # ms
    memory_limit: int = Field(default=256, ge=16, le=1024)  # MB
    description: Optional[str] = None


class TestcaseResponse(BaseModel):
    """Schema for testcase response"""

    id: int
    problem_id: int
    stdin: str
    expected_output: str
    is_sample: bool
    weight: int
    time_limit: int
    memory_limit: int
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TestcasePublic(BaseModel):
    """Public testcase (hides expected output for hidden testcases)"""

    id: int
    is_sample: bool
    description: Optional[str] = None
    stdin: Optional[str] = None  # Only for sample testcases
    expected_output: Optional[str] = None  # Only for sample testcases

    class Config:
        from_attributes = True
