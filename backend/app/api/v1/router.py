from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    problems,
    submissions,
    testcases,
    ai_feedback,
    rooms,
    websocket,
    dashboard,
    admin,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(problems.router, prefix="/problems", tags=["Problems"])
api_router.include_router(
    submissions.router, prefix="/submissions", tags=["Submissions"]
)
api_router.include_router(testcases.router, prefix="/testcases", tags=["Testcases"])
api_router.include_router(
    ai_feedback.router, prefix="/ai-feedback", tags=["AI Feedback"]
)
api_router.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

# WebSocket endpoint (no prefix needed, path is in the endpoint)
api_router.include_router(websocket.router, tags=["WebSocket"])
