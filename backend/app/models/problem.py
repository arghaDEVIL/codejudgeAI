from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Problem(Base):
    """Problem model for coding challenges"""

    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False, index=True)
    statement = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)  # Easy, Medium, Hard
    tags = Column(JSON, nullable=True, default=list)  # Array of topic tags

    # Deprecated: will be replaced by testcases table
    expected_output = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    submissions = relationship(
        "Submission", back_populates="problem", cascade="all, delete-orphan"
    )
    testcases = relationship(
        "Testcase", back_populates="problem", cascade="all, delete-orphan"
    )
