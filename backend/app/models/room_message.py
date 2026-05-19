from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class MessageType(str, enum.Enum):
    """Message types in a room"""

    CHAT = "chat"
    SYSTEM = "system"
    CODE_RUN = "code_run"


class RoomMessage(Base):
    """Room message model for chat and system messages"""

    __tablename__ = "room_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Message content
    message_type = Column(
        Enum(MessageType, values_callable=lambda x: [e.value for e in x]),
        default=MessageType.CHAT,
        nullable=False,
    )
    content = Column(Text, nullable=False)

    # Additional data (JSON) - renamed from 'metadata' to avoid SQLAlchemy conflict
    # Example: {"code_snippet": "...", "execution_result": {...}}
    message_data = Column(JSON, default={}, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    room = relationship("Room", back_populates="messages")
    user = relationship("User")
