from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class SnapshotType(str, enum.Enum):
    """Snapshot types"""

    AUTO = "auto"  # Auto-saved periodically
    MANUAL = "manual"  # User-triggered save
    SUBMISSION = "submission"  # Code submitted to judge


class RoomCodeSnapshot(Base):
    """Room code snapshot model for version history"""

    __tablename__ = "room_code_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Snapshot content
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)
    snapshot_type = Column(
        Enum(SnapshotType, values_callable=lambda x: [e.value for e in x]),
        default=SnapshotType.AUTO,
        nullable=False,
    )

    # Creator info
    created_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    room = relationship("Room", back_populates="code_snapshots")
    creator = relationship("User")
