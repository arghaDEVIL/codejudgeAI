from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Submission(Base):
    """Submission model for code submissions"""

    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)  # python, cpp
    status = Column(String(50), default="Pending")  # Accepted, Wrong Answer, etc.

    # Execution details
    execution_time = Column(Integer, nullable=True)  # in milliseconds
    memory_used = Column(Integer, nullable=True)  # in KB
    score = Column(Float, default=0.0, nullable=False)  # Weighted score (0-100)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
    testcase_results = relationship(
        "TestcaseResult", back_populates="submission", cascade="all, delete-orphan"
    )
    ai_feedback = relationship(
        "AIFeedback",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )
