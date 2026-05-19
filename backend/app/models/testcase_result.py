from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base


class TestcaseResult(Base):
    """Individual testcase result for a submission"""

    __tablename__ = "testcase_results"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(
        Integer,
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    testcase_id = Column(
        Integer,
        ForeignKey("testcases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Result
    status = Column(String(50), nullable=False)  # Passed, Failed, TLE, RTE, etc.
    actual_output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)

    # Metrics
    execution_time = Column(Integer, nullable=True)  # milliseconds
    memory_used = Column(Float, nullable=True)  # MB

    # Relationships
    submission = relationship("Submission", back_populates="testcase_results")
    testcase = relationship("Testcase", back_populates="testcase_results")
