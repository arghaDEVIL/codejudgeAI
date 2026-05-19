"""
WebSocket Manager for real-time collaborative coding
Handles connections, broadcasting, and presence tracking
"""

from fastapi import WebSocket
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """Manages WebSocket connections for collaborative rooms"""

    def __init__(self):
        # room_code -> {user_id -> WebSocket}
        self.active_connections: Dict[str, Dict[int, WebSocket]] = {}

        # room_code -> {user_id -> presence_data}
        self.user_presence: Dict[str, Dict[int, dict]] = {}

        # user_id -> room_code (for quick lookup)
        self.user_rooms: Dict[int, str] = {}

    async def connect(
        self, websocket: WebSocket, room_code: str, user_id: int, user_data: dict
    ):
        """Connect a user to a room"""
        await websocket.accept()

        # Initialize room if doesn't exist
        if room_code not in self.active_connections:
            self.active_connections[room_code] = {}
            self.user_presence[room_code] = {}

        # Add connection
        self.active_connections[room_code][user_id] = websocket
        self.user_rooms[user_id] = room_code

        # Store presence data
        self.user_presence[room_code][user_id] = {
            "user_id": user_id,
            "display_name": user_data.get("display_name"),
            "cursor_color": user_data.get("cursor_color"),
            "role": user_data.get("role"),
            "is_active": True,
            "cursor_position": None,
            "connected_at": datetime.utcnow().isoformat(),
        }

        # Notify others that user joined
        await self.broadcast_to_room(
            room_code,
            {
                "type": "user_joined",
                "data": self.user_presence[room_code][user_id],
                "timestamp": datetime.utcnow().isoformat(),
            },
            exclude_user=user_id,
        )

        # Send current room state to new user
        await self.send_room_state(websocket, room_code, user_id)

    async def disconnect(self, room_code: str, user_id: int):
        """Disconnect a user from a room"""
        if room_code in self.active_connections:
            if user_id in self.active_connections[room_code]:
                del self.active_connections[room_code][user_id]

            if user_id in self.user_presence.get(room_code, {}):
                user_data = self.user_presence[room_code][user_id]
                user_data["is_active"] = False

                # Notify others that user left
                await self.broadcast_to_room(
                    room_code,
                    {
                        "type": "user_left",
                        "data": {
                            "user_id": user_id,
                            "display_name": user_data.get("display_name"),
                        },
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )

                # Remove presence after notification
                del self.user_presence[room_code][user_id]

            # Clean up empty rooms
            if not self.active_connections[room_code]:
                del self.active_connections[room_code]
                if room_code in self.user_presence:
                    del self.user_presence[room_code]

        # Remove from user_rooms mapping
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")

    async def broadcast_to_room(
        self, room_code: str, message: dict, exclude_user: int = None
    ):
        """Broadcast message to all users in a room"""
        if room_code not in self.active_connections:
            return

        disconnected_users = []

        for user_id, websocket in self.active_connections[room_code].items():
            if exclude_user and user_id == exclude_user:
                continue

            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to user {user_id}: {e}")
                disconnected_users.append(user_id)

        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.disconnect(room_code, user_id)

    async def send_room_state(self, websocket: WebSocket, room_code: str, user_id: int):
        """Send current room state to a user"""
        if room_code not in self.user_presence:
            return

        # Get all active participants
        participants = [
            data
            for uid, data in self.user_presence[room_code].items()
            if uid != user_id  # Exclude self
        ]

        await self.send_personal_message(
            {
                "type": "room_state",
                "data": {
                    "participants": participants,
                    "room_code": room_code,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

    async def update_cursor_position(
        self, room_code: str, user_id: int, position: dict
    ):
        """Update and broadcast cursor position"""
        if room_code in self.user_presence and user_id in self.user_presence[room_code]:
            user_data = self.user_presence[room_code][user_id]
            user_data["cursor_position"] = position

            await self.broadcast_to_room(
                room_code,
                {
                    "type": "cursor_update",
                    "data": {
                        "user_id": user_id,
                        "user_name": user_data.get("display_name"),
                        "cursor_color": user_data.get("cursor_color"),
                        "position": position,
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                },
                exclude_user=user_id,
            )

    async def broadcast_code_change(
        self, room_code: str, user_id: int, code_data: dict
    ):
        """Broadcast code changes to all users in room"""
        await self.broadcast_to_room(
            room_code,
            {
                "type": "code_update",
                "data": {
                    "user_id": user_id,
                    **code_data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
            exclude_user=user_id,
        )

    async def broadcast_chat_message(
        self, room_code: str, user_id: int, message: str, user_name: str
    ):
        """Broadcast chat message to room"""
        await self.broadcast_to_room(
            room_code,
            {
                "type": "chat_message",
                "data": {
                    "user_id": user_id,
                    "user_name": user_name,
                    "message": message,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def get_room_participants(self, room_code: str) -> List[dict]:
        """Get list of active participants in a room"""
        if room_code not in self.user_presence:
            return []
        return list(self.user_presence[room_code].values())

    def get_active_rooms(self) -> List[str]:
        """Get list of active room codes"""
        return list(self.active_connections.keys())

    def is_user_in_room(self, room_code: str, user_id: int) -> bool:
        """Check if user is in a room"""
        return (
            room_code in self.active_connections
            and user_id in self.active_connections[room_code]
        )


# Global connection manager instance
connection_manager = ConnectionManager()
