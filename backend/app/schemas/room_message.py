from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class MessageTypeEnum(str, Enum):
    """Message types"""

    CHAT = "chat"
    SYSTEM = "system"
    CODE_RUN = "code_run"


class RoomMessageCreate(BaseModel):
    """Schema for creating a message"""

    room_id: int
    message_type: MessageTypeEnum = MessageTypeEnum.CHAT
    content: str = Field(..., min_length=1)
    message_data: Dict[str, Any] = Field(default_factory=dict)


class RoomMessageResponse(BaseModel):
    """Schema for message response"""

    id: int
    room_id: int
    user_id: Optional[int] = None
    message_type: str
    content: str
    message_data: Dict[str, Any]
    created_at: datetime

    # Additional fields
    user_name: Optional[str] = None

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Schema for chat message (WebSocket)"""

    message: str = Field(..., min_length=1, max_length=1000)


class SystemMessage(BaseModel):
    """Schema for system message"""

    event: str  # 'user_joined', 'user_left', 'code_executed', etc.
    data: Dict[str, Any]
