from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoomSessionCreate(BaseModel):
    """Schema for creating a room session"""

    room_id: int
    code: str = ""
    language: str = Field(default="python", pattern="^(python|cpp)$")


class RoomSessionUpdate(BaseModel):
    """Schema for updating a room session"""

    code: Optional[str] = None
    language: Optional[str] = Field(None, pattern="^(python|cpp)$")
    version: Optional[int] = None


class RoomSessionResponse(BaseModel):
    """Schema for room session response"""

    id: int
    room_id: int
    code: str
    language: str
    version: int
    last_edited_by: Optional[int] = None
    last_edited_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CodeChange(BaseModel):
    """Schema for code change (WebSocket)"""

    changes: list  # Array of {range, text} objects
    version: int
    cursor_position: Optional[dict] = None  # {line: int, column: int}


class CodeSyncMessage(BaseModel):
    """Schema for code synchronization message"""

    type: str  # 'code_update', 'cursor_move', etc.
    user_id: int
    data: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
