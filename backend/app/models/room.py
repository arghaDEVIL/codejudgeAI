from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class RoomMode(str, enum.Enum):
    """Room operation modes"""

    COLLABORATIVE = "collaborative"
    INTERVIEW = "interview"
    PRACTICE = "practice"


class RoomStatus(str, enum.Enum):
    """Room status"""

    ACTIVE = "active"
    ENDED = "ended"
    ARCHIVED = "archived"


class Room(Base):
    """Room model for collaborative coding sessions"""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String(8), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Host and problem
    host_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Room configuration
    mode = Column(
        Enum(RoomMode, values_callable=lambda x: [e.value for e in x]),
        default=RoomMode.COLLABORATIVE,
        nullable=False,
    )
    status = Column(
        Enum(RoomStatus, values_callable=lambda x: [e.value for e in x]),
        default=RoomStatus.ACTIVE,
        nullable=False,
    )
    max_participants = Column(Integer, default=10, nullable=False)

    # Settings stored as JSON
    # Example: {"allow_chat": true, "allow_code_execution": true, "interviewer_can_edit": false}
    settings = Column(JSON, default={}, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    host = relationship("User", foreign_keys=[host_user_id])
    problem = relationship("Problem", foreign_keys=[problem_id])
    participants = relationship(
        "RoomParticipant", back_populates="room", cascade="all, delete-orphan"
    )
    sessions = relationship(
        "RoomSession", back_populates="room", cascade="all, delete-orphan"
    )
    messages = relationship(
        "RoomMessage", back_populates="room", cascade="all, delete-orphan"
    )
    code_snapshots = relationship(
        "RoomCodeSnapshot", back_populates="room", cascade="all, delete-orphan"
    )
