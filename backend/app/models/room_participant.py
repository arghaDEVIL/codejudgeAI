from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class ParticipantRole(str, enum.Enum):
    """Participant roles in a room"""

    HOST = "host"
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    VIEWER = "viewer"


class RoomParticipant(Base):
    """Room participant model"""

    __tablename__ = "room_participants"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Participant info
    role = Column(
        Enum(ParticipantRole, values_callable=lambda x: [e.value for e in x]),
        default=ParticipantRole.VIEWER,
        nullable=False,
    )
    display_name = Column(String(100), nullable=False)
    cursor_color = Column(String(7), nullable=False)  # Hex color code

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    room = relationship("Room", back_populates="participants")
    user = relationship("User")
