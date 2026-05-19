"""
WebSocket Endpoint for Real-Time Collaboration
Handles WebSocket connections for collaborative coding rooms
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
from datetime import datetime
from urllib.parse import parse_qs

from app.db.database import get_db
from app.services.websocket_manager import connection_manager
from app.services.room_manager import room_manager
from app.core.security import verify_token

router = APIRouter()


async def get_current_user_ws(token: str, db: Session):
    """Authenticate WebSocket connection"""
    try:
        print(f"[WS Auth] Verifying token: {token[:20]}...")
        payload = verify_token(token)
        print(f"[WS Auth] Payload: {payload}")
        user_id = payload.get("sub")
        print(f"[WS Auth] User ID: {user_id}")
        if user_id is None:
            print(f"[WS Auth] No user_id in payload")
            return None
        return int(user_id)
    except Exception as e:
        print(f"[WS Auth] Exception: {e}")
        return None


@router.websocket("/ws/room/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    """WebSocket endpoint for real-time collaboration"""

    # IMPORTANT: Accept connection FIRST
    await websocket.accept()

    # Get database session
    db_gen = get_db()
    db = next(db_gen)

    try:
        # Extract token from query string manually
        query_string = websocket.scope.get("query_string", b"").decode()
        print(f"[WS] Query string: {query_string}")
        query_params = parse_qs(query_string)
        print(f"[WS] Query params: {query_params}")
        token = query_params.get("token", [None])[0]
        print(f"[WS] Extracted token: {token[:20] if token else 'None'}...")

        if not token:
            await websocket.send_json(
                {"type": "error", "data": {"message": "No token provided"}}
            )
            await websocket.close(code=1008)
            return

        # Authenticate user
        user_id = await get_current_user_ws(token, db)
        print(f"[WS] Authenticated user_id: {user_id}")

        if not user_id:
            await websocket.send_json(
                {"type": "error", "data": {"message": "Authentication failed"}}
            )
            await websocket.close(code=1008)
            return

        # Verify room exists
        room = room_manager.get_room_by_code(db, room_code)
        if not room:
            await websocket.send_json(
                {"type": "error", "data": {"message": "Room not found"}}
            )
            await websocket.close(code=1008)
            return

        # Get participant info
        participant = None
        participants = room_manager.get_room_participants(db, room.id)

        for p in participants:
            if p.user_id == user_id and p.is_active:
                participant = p
                break

        if not participant:
            await websocket.send_json(
                {"type": "error", "data": {"message": "Not a participant"}}
            )
            await websocket.close(code=1008)
            return

        # Register connection
        if room_code not in connection_manager.active_connections:
            connection_manager.active_connections[room_code] = {}
            connection_manager.user_presence[room_code] = {}

        connection_manager.active_connections[room_code][user_id] = websocket
        connection_manager.user_rooms[user_id] = room_code

        # Store presence data
        connection_manager.user_presence[room_code][user_id] = {
            "user_id": user_id,
            "display_name": participant.display_name,
            "cursor_color": participant.cursor_color,
            "role": participant.role.value,
            "is_active": True,
            "cursor_position": None,
            "connected_at": datetime.utcnow().isoformat(),
        }

        # Notify others that user joined
        await connection_manager.broadcast_to_room(
            room_code,
            {
                "type": "user_joined",
                "data": connection_manager.user_presence[room_code][user_id],
                "timestamp": datetime.utcnow().isoformat(),
            },
            exclude_user=user_id,
        )

        # Send current room state to new user
        await connection_manager.send_room_state(websocket, room_code, user_id)

        # Message loop
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)

                message_type = message.get("type")
                message_data = message.get("data", {})

                if message_type == "code_change":
                    code = message_data.get("code", "")
                    language = message_data.get("language", "python")

                    try:
                        room_manager.update_room_code(
                            db, room.id, code, language, user_id
                        )
                        await connection_manager.broadcast_code_change(
                            room_code,
                            user_id,
                            {
                                "code": code,
                                "language": language,
                                "changes": message_data.get("changes", []),
                            },
                        )
                    except Exception as e:
                        await websocket.send_json(
                            {"type": "error", "data": {"message": str(e)}}
                        )

                elif message_type == "cursor_move":
                    position = message_data.get("position", {})
                    await connection_manager.update_cursor_position(
                        room_code, user_id, position
                    )

                elif message_type == "chat_message":
                    content = message_data.get("message", "").strip()
                    if content:
                        try:
                            room_manager.add_chat_message(db, room.id, user_id, content)
                            await connection_manager.broadcast_chat_message(
                                room_code, user_id, content, participant.display_name
                            )
                        except Exception as e:
                            await websocket.send_json(
                                {"type": "error", "data": {"message": str(e)}}
                            )

                elif message_type == "ping":
                    await websocket.send_json({"type": "pong", "data": {}})

        except WebSocketDisconnect:
            await connection_manager.disconnect(room_code, user_id)
        except Exception as e:
            print(f"WebSocket error: {e}")
            await connection_manager.disconnect(room_code, user_id)
    finally:
        try:
            db.close()
        except:
            pass
