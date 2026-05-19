from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class RoomModeEnum(str, Enum):
    """Room operation modes"""

    COLLABORATIVE = "collaborative"
    INTERVIEW = "interview"
    PRACTICE = "practice"


class RoomStatusEnum(str, Enum):
    """Room status"""

    ACTIVE = "active"
    ENDED = "ended"
    ARCHIVED = "archived"


class RoomCreate(BaseModel):
    """Schema for creating a room"""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    problem_id: Optional[int] = None
    mode: RoomModeEnum = RoomModeEnum.COLLABORATIVE
    max_participants: int = Field(default=10, ge=2, le=50)
    settings: Dict[str, Any] = Field(default_factory=dict)


class RoomUpdate(BaseModel):
    """Schema for updating a room"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[RoomStatusEnum] = None
    settings: Optional[Dict[str, Any]] = None


class RoomResponse(BaseModel):
    """Schema for room response"""

    id: int
    room_code: str
    title: str
    description: Optional[str] = None
    host_user_id: int
    problem_id: Optional[int] = None
    mode: str
    status: str
    max_participants: int
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    # Additional computed fields
    participant_count: int = 0

    class Config:
        from_attributes = True


class RoomDetailResponse(RoomResponse):
    """Detailed room response with participants"""

    participants: List[Dict[str, Any]] = []
    current_code: Optional[str] = None
    current_language: Optional[str] = None

    class Config:
        from_attributes = True


class RoomJoinRequest(BaseModel):
    """Schema for joining a room"""

    display_name: Optional[str] = None


class RoomJoinResponse(BaseModel):
    """Response after joining a room"""

    room: RoomDetailResponse
    participant_id: int
    cursor_color: str
    role: str
