from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class ParticipantRoleEnum(str, Enum):
    """Participant roles"""

    HOST = "host"
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    VIEWER = "viewer"


class RoomParticipantCreate(BaseModel):
    """Schema for creating a participant"""

    room_id: int
    user_id: int
    role: ParticipantRoleEnum = ParticipantRoleEnum.VIEWER
    display_name: str = Field(..., min_length=1, max_length=100)
    cursor_color: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")


class RoomParticipantUpdate(BaseModel):
    """Schema for updating a participant"""

    role: Optional[ParticipantRoleEnum] = None
    is_active: Optional[bool] = None


class RoomParticipantResponse(BaseModel):
    """Schema for participant response"""

    id: int
    room_id: int
    user_id: int
    role: str
    display_name: str
    cursor_color: str
    is_active: bool
    joined_at: datetime
    left_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ParticipantPresence(BaseModel):
    """Schema for participant presence (WebSocket)"""

    user_id: int
    display_name: str
    cursor_color: str
    role: str
    is_active: bool
    cursor_position: Optional[dict] = None  # {line: int, column: int}
