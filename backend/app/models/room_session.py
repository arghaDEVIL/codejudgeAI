from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class RoomSession(Base):
    """Room session model for storing current code state"""

    __tablename__ = "room_sessions"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Current code state
    code = Column(Text, default="", nullable=False)
    language = Column(String(20), default="python", nullable=False)

    # Version control
    version = Column(Integer, default=0, nullable=False)  # For conflict resolution

    # Last edit info
    last_edited_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    last_edited_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    room = relationship("Room", back_populates="sessions")
    last_editor = relationship("User", foreign_keys=[last_edited_by])
