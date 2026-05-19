from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Testcase(Base):
    """Testcase model for problems"""
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Input/Output
    stdin = Column(Text, nullable=False)  # Input for the program
    expected_output = Column(Text, nullable=False)  # Expected output
    
    # Testcase metadata
    is_sample = Column(Boolean, default=False)  # Sample (visible) vs Hidden
    weight = Column(Integer, default=1)  # Points for this testcase
    time_limit = Column(Integer, default=2000)  # Time limit in milliseconds
    memory_limit = Column(Integer, default=256)  # Memory limit in MB
    
    # Description (for sample testcases)
    description = Column(String(500), nullable=True)  # e.g., "Basic test case"
    
    # Relationships
    problem = relationship("Problem", back_populates="testcases")
    testcase_results = relationship("TestcaseResult", back_populates="testcase", cascade="all, delete-orphan")
