"""
Room Management Endpoints
HTTP endpoints for creating, joining, and managing collaborative coding rooms
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
    RoomDetailResponse,
    RoomJoinRequest,
    RoomJoinResponse,
)
from app.services.room_manager import room_manager

router = APIRouter()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new collaborative coding room
    """
    try:
        room = room_manager.create_room(db, room_data, current_user.id)

        # Get participant count
        participants = room_manager.get_room_participants(db, room.id)

        return RoomResponse(
            id=room.id,
            room_code=room.room_code,
            title=room.title,
            description=room.description,
            host_user_id=room.host_user_id,
            problem_id=room.problem_id,
            mode=room.mode.value,
            status=room.status.value,
            max_participants=room.max_participants,
            settings=room.settings,
            created_at=room.created_at,
            updated_at=room.updated_at,
            ended_at=room.ended_at,
            participant_count=len(participants),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create room: {str(e)}",
        )


@router.get("/{room_code}", response_model=RoomDetailResponse)
def get_room(
    room_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get room details by room code
    """
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    # Get participants
    participants = room_manager.get_room_participants(db, room.id)
    participant_list = [
        {
            "id": p.id,
            "user_id": p.user_id,
            "display_name": p.display_name,
            "role": p.role.value,
            "cursor_color": p.cursor_color,
            "is_active": p.is_active,
            "joined_at": p.joined_at.isoformat(),
        }
        for p in participants
    ]

    # Get current code
    session = room_manager.get_room_session(db, room.id)

    # Build response manually
    return RoomDetailResponse(
        id=room.id,
        room_code=room.room_code,
        title=room.title,
        description=room.description,
        host_user_id=room.host_user_id,
        problem_id=room.problem_id,
        mode=room.mode.value,
        status=room.status.value,
        max_participants=room.max_participants,
        settings=room.settings,
        created_at=room.created_at,
        updated_at=room.updated_at,
        ended_at=room.ended_at,
        participant_count=len([p for p in participants if p.is_active]),
        participants=participant_list,
        current_code=session.code if session else "",
        current_language=session.language if session else "python",
    )


@router.post("/{room_code}/join", response_model=RoomJoinResponse)
def join_room(
    room_code: str,
    join_data: RoomJoinRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Join a room
    """
    try:
        room, participant = room_manager.join_room(
            db, room_code, current_user.id, join_data.display_name
        )

        # Get full room details
        participants = room_manager.get_room_participants(db, room.id)
        participant_list = [
            {
                "id": p.id,
                "user_id": p.user_id,
                "display_name": p.display_name,
                "role": p.role.value,
                "cursor_color": p.cursor_color,
                "is_active": p.is_active,
                "joined_at": p.joined_at.isoformat(),
            }
            for p in participants
        ]

        session = room_manager.get_room_session(db, room.id)

        room_detail = RoomDetailResponse(
            id=room.id,
            room_code=room.room_code,
            title=room.title,
            description=room.description,
            host_user_id=room.host_user_id,
            problem_id=room.problem_id,
            mode=room.mode.value,
            status=room.status.value,
            max_participants=room.max_participants,
            settings=room.settings,
            created_at=room.created_at,
            updated_at=room.updated_at,
            ended_at=room.ended_at,
            participant_count=len([p for p in participants if p.is_active]),
            participants=participant_list,
            current_code=session.code if session else "",
            current_language=session.language if session else "python",
        )

        return RoomJoinResponse(
            room=room_detail,
            participant_id=participant.id,
            cursor_color=participant.cursor_color,
            role=participant.role.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to join room: {str(e)}",
        )


@router.post("/{room_code}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_room(
    room_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Leave a room
    """
    try:
        room_manager.leave_room(db, room_code, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to leave room: {str(e)}",
        )


@router.get("/", response_model=List[RoomResponse])
def get_user_rooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all rooms where current user is a participant
    """
    rooms = room_manager.get_user_rooms(db, current_user.id)

    response_list = []
    for room in rooms:
        participants = room_manager.get_room_participants(db, room.id)
        room_response = RoomResponse(
            id=room.id,
            room_code=room.room_code,
            title=room.title,
            description=room.description,
            host_user_id=room.host_user_id,
            problem_id=room.problem_id,
            mode=room.mode.value,
            status=room.status.value,
            max_participants=room.max_participants,
            settings=room.settings,
            created_at=room.created_at,
            updated_at=room.updated_at,
            ended_at=room.ended_at,
            participant_count=len([p for p in participants if p.is_active]),
        )
        response_list.append(room_response)

    return response_list


@router.put("/{room_code}", response_model=RoomResponse)
def update_room(
    room_code: str,
    room_data: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update room settings (host only)
    """
    try:
        room = room_manager.update_room(db, room_code, room_data, current_user.id)

        participants = room_manager.get_room_participants(db, room.id)

        return RoomResponse(
            id=room.id,
            room_code=room.room_code,
            title=room.title,
            description=room.description,
            host_user_id=room.host_user_id,
            problem_id=room.problem_id,
            mode=room.mode.value,
            status=room.status.value,
            max_participants=room.max_participants,
            settings=room.settings,
            created_at=room.created_at,
            updated_at=room.updated_at,
            ended_at=room.ended_at,
            participant_count=len([p for p in participants if p.is_active]),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update room: {str(e)}",
        )


@router.get("/{room_code}/participants")
def get_room_participants(
    room_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all participants in a room
    """
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    participants = room_manager.get_room_participants(db, room.id)

    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "display_name": p.display_name,
            "role": p.role.value,
            "cursor_color": p.cursor_color,
            "is_active": p.is_active,
            "joined_at": p.joined_at.isoformat(),
            "left_at": p.left_at.isoformat() if p.left_at else None,
        }
        for p in participants
    ]


@router.get("/{room_code}/messages")
def get_room_messages(
    room_code: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get chat messages from a room
    """
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    messages = room_manager.get_room_messages(db, room.id, limit)

    return [
        {
            "id": m.id,
            "user_id": m.user_id,
            "message_type": m.message_type.value,
            "content": m.content,
            "message_data": m.message_data,
            "created_at": m.created_at.isoformat(),
        }
        for m in reversed(messages)  # Reverse to get chronological order
    ]


@router.post("/{room_code}/messages", status_code=status.HTTP_201_CREATED)
def send_chat_message(
    room_code: str,
    message: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a chat message to a room
    """
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    content = message.get("content", "").strip()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required",
        )

    try:
        chat_message = room_manager.add_chat_message(
            db, room.id, current_user.id, content
        )

        return {
            "id": chat_message.id,
            "user_id": chat_message.user_id,
            "message_type": chat_message.message_type.value,
            "content": chat_message.content,
            "created_at": chat_message.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}",
        )


@router.post("/{room_code}/execute")
async def execute_code_in_room(
    room_code: str,
    code_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute code in a collaborative room and broadcast results
    """
    from app.services.docker_executor import DockerExecutor
    from app.services.websocket_manager import connection_manager
    from datetime import datetime

    # Verify room exists
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Verify user is a participant
    participants = room_manager.get_room_participants(db, room.id)
    is_participant = any(
        p.user_id == current_user.id and p.is_active for p in participants
    )

    if not is_participant:
        raise HTTPException(status_code=403, detail="Not a participant in this room")

    # Execute code
    code = code_data.get("code", "")
    language = code_data.get("language", "python")

    try:
        executor = DockerExecutor()
        result = executor.execute(code, language)

        # Broadcast execution results to all users in the room
        await connection_manager.broadcast_to_room(
            room_code,
            {
                "type": "code_execution",
                "data": {
                    "user_id": current_user.id,
                    "user_name": current_user.name,
                    "result": result,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@router.post("/{room_code}/run-tests")
async def run_tests_in_room(
    room_code: str,
    code_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Run code against test cases in a collaborative room
    """
    from app.services.docker_executor import DockerExecutor
    from app.services.websocket_manager import connection_manager
    from app.models.testcase import Testcase
    from datetime import datetime

    # Verify room exists
    room = room_manager.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Verify user is a participant
    participants = room_manager.get_room_participants(db, room.id)
    is_participant = any(
        p.user_id == current_user.id and p.is_active for p in participants
    )

    if not is_participant:
        raise HTTPException(status_code=403, detail="Not a participant in this room")

    # Check if room has a problem
    if not room.problem_id:
        raise HTTPException(status_code=400, detail="Room has no problem assigned")

    # Get test cases
    testcases = (
        db.query(Testcase)
        .filter(Testcase.problem_id == room.problem_id)
        .order_by(Testcase.is_sample.desc(), Testcase.id)
        .all()
    )

    if not testcases:
        raise HTTPException(
            status_code=404, detail="No test cases found for this problem"
        )

    code = code_data.get("code", "")
    language = code_data.get("language", "python")

    try:
        executor = DockerExecutor()
        test_results = []
        passed_count = 0

        # Run code against each test case
        for idx, testcase in enumerate(testcases):
            # Execute with test input
            result = executor.execute(code, language, stdin=testcase.stdin)

            # Compare output (strip whitespace for comparison)
            actual_output = result.get("output", "").strip()
            expected_output = testcase.expected_output.strip()

            is_passed = actual_output == expected_output

            if is_passed:
                passed_count += 1

            test_results.append(
                {
                    "test_number": idx + 1,
                    "is_sample": testcase.is_sample,
                    "passed": is_passed,
                    "input": testcase.stdin
                    if testcase.is_sample
                    else None,  # Hide hidden test inputs
                    "expected": expected_output
                    if testcase.is_sample
                    else None,  # Hide hidden test outputs
                    "actual": actual_output
                    if testcase.is_sample or not is_passed
                    else None,  # Show actual only for samples or failures
                    "error": result.get("error"),
                    "execution_time": result.get("execution_time", 0),
                }
            )

        response_data = {
            "passed": passed_count,
            "total": len(testcases),
            "results": test_results,
            "all_passed": passed_count == len(testcases),
        }

        # Broadcast test results to all users in the room
        await connection_manager.broadcast_to_room(
            room_code,
            {
                "type": "test_results",
                "data": {
                    "user_id": current_user.id,
                    "user_name": current_user.name,
                    "results": response_data,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")
