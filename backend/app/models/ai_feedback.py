from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class AIFeedback(Base):
    """AI-generated feedback for submissions"""

    __tablename__ = "ai_feedback"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(
        Integer,
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Feedback content
    overall_feedback = Column(Text, nullable=False)
    error_analysis = Column(Text, nullable=True)
    optimization_hints = Column(Text, nullable=True)
    time_complexity = Column(String(50), nullable=True)  # e.g., "O(n^2)"
    space_complexity = Column(String(50), nullable=True)  # e.g., "O(n)"
    code_quality_score = Column(Integer, nullable=True)  # 0-100

    # Metadata
    model_used = Column(String(50), default="gpt-4")
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    submission = relationship("Submission", back_populates="ai_feedback")
