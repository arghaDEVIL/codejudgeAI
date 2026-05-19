"""
Room Manager Service
Handles room creation, joining, leaving, and management
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
import random
import string
from datetime import datetime

from app.models.room import Room, RoomMode, RoomStatus
from app.models.room_participant import RoomParticipant, ParticipantRole
from app.models.room_session import RoomSession
from app.models.room_message import RoomMessage, MessageType
from app.models.user import User
from app.schemas.room import RoomCreate, RoomUpdate


class RoomManager:
    """Manages collaborative coding rooms"""

    @staticmethod
    def generate_room_code(length: int = 8) -> str:
        """Generate a unique room code"""
        # Use uppercase letters and numbers, excluding similar-looking characters
        chars = string.ascii_uppercase + string.digits
        chars = (
            chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "")
        )
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def generate_cursor_color() -> str:
        """Generate a random cursor color"""
        colors = [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#FFA07A",
            "#98D8C8",
            "#F7DC6F",
            "#BB8FCE",
            "#85C1E2",
            "#F8B739",
            "#52B788",
            "#FF8FA3",
            "#6C5CE7",
            "#00B894",
            "#FDCB6E",
            "#E17055",
        ]
        return random.choice(colors)

    def create_room(
        self, db: Session, room_data: RoomCreate, host_user_id: int
    ) -> Room:
        """Create a new room"""
        # Generate unique room code
        room_code = self.generate_room_code()
        while db.query(Room).filter(Room.room_code == room_code).first():
            room_code = self.generate_room_code()

        # Create room
        room = Room(
            room_code=room_code,
            title=room_data.title,
            description=room_data.description,
            host_user_id=host_user_id,
            problem_id=room_data.problem_id,
            mode=room_data.mode,
            max_participants=room_data.max_participants,
            settings=room_data.settings or {},
            status=RoomStatus.ACTIVE,
        )

        db.add(room)
        db.flush()  # Get room.id

        # Create room session
        session = RoomSession(
            room_id=room.id,
            code="",
            language="python",
            version=0,
        )
        db.add(session)

        # Add host as participant
        host_user = db.query(User).filter(User.id == host_user_id).first()
        host_participant = RoomParticipant(
            room_id=room.id,
            user_id=host_user_id,
            role=ParticipantRole.HOST,
            display_name=host_user.name if host_user else f"User {host_user_id}",
            cursor_color=self.generate_cursor_color(),
            is_active=True,
        )
        db.add(host_participant)

        # Add system message
        system_message = RoomMessage(
            room_id=room.id,
            user_id=None,
            message_type=MessageType.SYSTEM,
            content=f"Room created by {host_participant.display_name}",
            message_data={},
        )
        db.add(system_message)

        db.commit()
        db.refresh(room)

        return room

    def get_room_by_code(self, db: Session, room_code: str) -> Optional[Room]:
        """Get room by code"""
        return db.query(Room).filter(Room.room_code == room_code).first()

    def get_room_by_id(self, db: Session, room_id: int) -> Optional[Room]:
        """Get room by ID"""
        return db.query(Room).filter(Room.id == room_id).first()

    def get_user_rooms(self, db: Session, user_id: int) -> List[Room]:
        """Get all rooms where user is a participant"""
        participant_room_ids = (
            db.query(RoomParticipant.room_id)
            .filter(RoomParticipant.user_id == user_id)
            .all()
        )
        room_ids = [r[0] for r in participant_room_ids]

        return (
            db.query(Room)
            .filter(Room.id.in_(room_ids))
            .order_by(Room.created_at.desc())
            .all()
        )

    def join_room(
        self,
        db: Session,
        room_code: str,
        user_id: int,
        display_name: Optional[str] = None,
    ) -> tuple[Room, RoomParticipant]:
        """Join a room"""
        # Get room
        room = self.get_room_by_code(db, room_code)
        if not room:
            raise ValueError("Room not found")

        if room.status != RoomStatus.ACTIVE:
            raise ValueError("Room is not active")

        # Check if already a participant
        existing = (
            db.query(RoomParticipant)
            .filter(
                and_(
                    RoomParticipant.room_id == room.id,
                    RoomParticipant.user_id == user_id,
                )
            )
            .first()
        )

        if existing:
            # Reactivate if was inactive
            if not existing.is_active:
                existing.is_active = True
                existing.left_at = None
                db.commit()
                db.refresh(existing)
            return room, existing

        # Check participant limit
        active_count = (
            db.query(RoomParticipant)
            .filter(
                and_(
                    RoomParticipant.room_id == room.id,
                    RoomParticipant.is_active == True,
                )
            )
            .count()
        )

        if active_count >= room.max_participants:
            raise ValueError("Room is full")

        # Get user info
        user = db.query(User).filter(User.id == user_id).first()
        if not display_name:
            display_name = user.name if user else f"User {user_id}"

        # Determine role based on room mode
        if room.mode == RoomMode.INTERVIEW:
            # In interview mode, non-host joins as candidate
            role = ParticipantRole.CANDIDATE
        else:
            # In collaborative mode, join as viewer
            role = ParticipantRole.VIEWER

        # Create participant
        participant = RoomParticipant(
            room_id=room.id,
            user_id=user_id,
            role=role,
            display_name=display_name,
            cursor_color=self.generate_cursor_color(),
            is_active=True,
        )
        db.add(participant)

        # Add system message
        system_message = RoomMessage(
            room_id=room.id,
            user_id=None,
            message_type=MessageType.SYSTEM,
            content=f"{display_name} joined the room",
            message_data={"user_id": user_id},
        )
        db.add(system_message)

        db.commit()
        db.refresh(participant)

        return room, participant

    def leave_room(self, db: Session, room_code: str, user_id: int):
        """Leave a room"""
        room = self.get_room_by_code(db, room_code)
        if not room:
            raise ValueError("Room not found")

        participant = (
            db.query(RoomParticipant)
            .filter(
                and_(
                    RoomParticipant.room_id == room.id,
                    RoomParticipant.user_id == user_id,
                )
            )
            .first()
        )

        if not participant:
            raise ValueError("Not a participant")

        # Mark as inactive
        participant.is_active = False
        participant.left_at = datetime.utcnow()

        # Add system message
        system_message = RoomMessage(
            room_id=room.id,
            user_id=None,
            message_type=MessageType.SYSTEM,
            content=f"{participant.display_name} left the room",
            message_data={"user_id": user_id},
        )
        db.add(system_message)

        db.commit()

    def update_room(
        self, db: Session, room_code: str, room_data: RoomUpdate, user_id: int
    ) -> Room:
        """Update room (host only)"""
        room = self.get_room_by_code(db, room_code)
        if not room:
            raise ValueError("Room not found")

        if room.host_user_id != user_id:
            raise ValueError("Only host can update room")

        # Update fields
        if room_data.title is not None:
            room.title = room_data.title
        if room_data.description is not None:
            room.description = room_data.description
        if room_data.status is not None:
            room.status = room_data.status
            if room_data.status == RoomStatus.ENDED:
                room.ended_at = datetime.utcnow()
        if room_data.settings is not None:
            room.settings = room_data.settings

        room.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(room)

        return room

    def get_room_participants(self, db: Session, room_id: int) -> List[RoomParticipant]:
        """Get all participants in a room"""
        return (
            db.query(RoomParticipant)
            .filter(RoomParticipant.room_id == room_id)
            .order_by(RoomParticipant.joined_at)
            .all()
        )

    def get_room_session(self, db: Session, room_id: int) -> Optional[RoomSession]:
        """Get room session"""
        return db.query(RoomSession).filter(RoomSession.room_id == room_id).first()

    def update_room_code(
        self, db: Session, room_id: int, code: str, language: str, user_id: int
    ) -> RoomSession:
        """Update room code"""
        session = self.get_room_session(db, room_id)
        if not session:
            raise ValueError("Room session not found")

        session.code = code
        session.language = language
        session.version += 1
        session.last_edited_by = user_id
        session.last_edited_at = datetime.utcnow()

        db.commit()
        db.refresh(session)

        return session

    def get_room_messages(
        self, db: Session, room_id: int, limit: int = 50
    ) -> List[RoomMessage]:
        """Get room messages"""
        return (
            db.query(RoomMessage)
            .filter(RoomMessage.room_id == room_id)
            .order_by(RoomMessage.created_at.desc())
            .limit(limit)
            .all()
        )

    def add_chat_message(
        self, db: Session, room_id: int, user_id: int, content: str
    ) -> RoomMessage:
        """Add a chat message"""
        message = RoomMessage(
            room_id=room_id,
            user_id=user_id,
            message_type=MessageType.CHAT,
            content=content,
            message_data={},
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        return message


# Global room manager instance
room_manager = RoomManager()
