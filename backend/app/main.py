from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered code judge platform for competitive programming",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Test WebSocket endpoint - minimal version to debug
from fastapi import WebSocket


@app.websocket("/ws/test")
async def test_websocket(websocket: WebSocket):
    """Minimal test WebSocket"""
    await websocket.accept()
    await websocket.send_json({"message": "Connected!"})
    await websocket.close()


# Import and register WebSocket route directly (bypass potential middleware issues)
from app.api.v1.endpoints.websocket import websocket_endpoint

app.add_api_websocket_route("/ws/room/{room_code}", websocket_endpoint)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else "disabled in production",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("✅ Application started")
    print("⚠️  Note: Run 'python migrate.py upgrade' to apply database migrations")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("👋 Shutting down...")
