# Real-Time Collaborative Coding + Interview Mode - Implementation Plan

## Overview
Add real-time collaborative coding rooms with WebSocket support, allowing multiple users to code together with live cursor tracking, interview mode, and integrated judge system.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
├─────────────────────────────────────────────────────────────┤
│  • Room Lobby          • Collaborative Editor                │
│  • Participants List   • Live Cursors                        │
│  • Chat Panel          • Interview Controls                  │
└─────────────────────────────────────────────────────────────┘
                            ↕ WebSocket + HTTP
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│  • WebSocket Manager   • Room Manager                        │
│  • Session Handler     • Auth Middleware                     │
│  • Code Sync Engine    • Judge Integration                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
├─────────────────────────────────────────────────────────────┤
│  • rooms               • room_participants                   │
│  • room_sessions       • room_messages                       │
│  • room_code_snapshots                                       │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Database Schema & Models

### New Tables

#### 1. `rooms` table
```sql
- id (PK)
- room_code (unique, 8-char)
- title
- description
- host_user_id (FK -> users)
- problem_id (FK -> problems, nullable)
- mode (enum: 'collaborative', 'interview', 'practice')
- status (enum: 'active', 'ended', 'archived')
- max_participants (default: 10)
- settings (JSONB: permissions, features)
- created_at
- updated_at
- ended_at
```

#### 2. `room_participants` table
```sql
- id (PK)
- room_id (FK -> rooms)
- user_id (FK -> users)
- role (enum: 'host', 'interviewer', 'candidate', 'viewer')
- display_name
- cursor_color
- joined_at
- left_at
- is_active (boolean)
```

#### 3. `room_sessions` table
```sql
- id (PK)
- room_id (FK -> rooms)
- code (TEXT)
- language
- last_edited_by (FK -> users)
- last_edited_at
- version (integer, for conflict resolution)
```

#### 4. `room_messages` table
```sql
- id (PK)
- room_id (FK -> rooms)
- user_id (FK -> users)
- message_type (enum: 'chat', 'system', 'code_run')
- content (TEXT)
- metadata (JSONB)
- created_at
```

#### 5. `room_code_snapshots` table
```sql
- id (PK)
- room_id (FK -> rooms)
- code (TEXT)
- language
- snapshot_type (enum: 'auto', 'manual', 'submission')
- created_by (FK -> users)
- created_at
```

## Phase 2: Backend Implementation

### File Structure
```
backend/app/
├── models/
│   ├── room.py
│   ├── room_participant.py
│   ├── room_session.py
│   ├── room_message.py
│   └── room_code_snapshot.py
├── schemas/
│   ├── room.py
│   ├── room_participant.py
│   ├── room_session.py
│   └── room_message.py
├── api/v1/endpoints/
│   ├── rooms.py
│   └── websocket.py
├── services/
│   ├── websocket_manager.py
│   ├── room_manager.py
│   └── code_sync_service.py
└── core/
    └── websocket_auth.py
```

### Key Components

#### 1. WebSocket Manager (`services/websocket_manager.py`)
- Manage active connections
- Handle connect/disconnect
- Broadcast messages to room
- Track user presence
- Handle reconnection logic

#### 2. Room Manager (`services/room_manager.py`)
- Create/join/leave rooms
- Manage participants
- Handle permissions
- Auto-save code state
- Session management

#### 3. Code Sync Service (`services/code_sync_service.py`)
- Operational Transformation (OT) or CRDT
- Conflict resolution
- Version tracking
- Delta compression

#### 4. WebSocket Endpoints (`api/v1/endpoints/websocket.py`)
```python
@router.websocket("/ws/room/{room_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_code: str,
    token: str
)
```

#### 5. HTTP Endpoints (`api/v1/endpoints/rooms.py`)
```python
POST   /api/v1/rooms/                    # Create room
GET    /api/v1/rooms/{room_code}         # Get room details
POST   /api/v1/rooms/{room_code}/join    # Join room
POST   /api/v1/rooms/{room_code}/leave   # Leave room
GET    /api/v1/rooms/{room_code}/participants
POST   /api/v1/rooms/{room_code}/messages
GET    /api/v1/rooms/{room_code}/history
POST   /api/v1/rooms/{room_code}/submit  # Submit code from room
```

## Phase 3: Frontend Implementation

### File Structure
```
frontend/src/
├── pages/
│   ├── RoomLobby.jsx
│   ├── CollaborativeEditor.jsx
│   └── InterviewRoom.jsx
├── components/
│   ├── room/
│   │   ├── RoomHeader.jsx
│   │   ├── ParticipantsList.jsx
│   │   ├── ChatPanel.jsx
│   │   ├── CodeEditor.jsx
│   │   ├── LiveCursor.jsx
│   │   └── InterviewControls.jsx
│   └── modals/
│       ├── CreateRoomModal.jsx
│       └── JoinRoomModal.jsx
├── hooks/
│   ├── useWebSocket.js
│   ├── useRoom.js
│   └── useCollaborativeEditor.js
└── utils/
    ├── websocket.js
    └── roomApi.js
```

### Key Components

#### 1. Room Lobby (`pages/RoomLobby.jsx`)
- Create room form
- Join room with code
- Active rooms list
- Room settings

#### 2. Collaborative Editor (`pages/CollaborativeEditor.jsx`)
- Monaco editor integration
- Live cursor tracking
- Participants sidebar
- Chat panel
- Code execution
- Interview controls

#### 3. WebSocket Hook (`hooks/useWebSocket.js`)
```javascript
const useWebSocket = (roomCode, token) => {
  // Connect to WebSocket
  // Handle messages
  // Auto-reconnect
  // Send messages
}
```

#### 4. Collaborative Editor Hook (`hooks/useCollaborativeEditor.js`)
```javascript
const useCollaborativeEditor = (roomCode) => {
  // Sync code changes
  // Handle remote updates
  // Track cursors
  // Manage conflicts
}
```

## Phase 4: WebSocket Message Protocol

### Message Types

#### Client → Server
```javascript
{
  type: 'join_room',
  data: { room_code, user_info }
}

{
  type: 'code_change',
  data: { 
    changes: [{ range, text }],
    version: 123,
    cursor_position: { line, column }
  }
}

{
  type: 'cursor_move',
  data: { line, column }
}

{
  type: 'chat_message',
  data: { message }
}

{
  type: 'run_code',
  data: { code, language, problem_id }
}
```

#### Server → Client
```javascript
{
  type: 'user_joined',
  data: { user_id, display_name, role, color }
}

{
  type: 'user_left',
  data: { user_id }
}

{
  type: 'code_update',
  data: { 
    changes: [{ range, text }],
    version: 124,
    user_id
  }
}

{
  type: 'cursor_update',
  data: { user_id, line, column }
}

{
  type: 'chat_message',
  data: { user_id, message, timestamp }
}

{
  type: 'code_result',
  data: { status, output, execution_time }
}

{
  type: 'room_state',
  data: { code, language, participants, version }
}
```

## Phase 5: Features Implementation

### 1. Room Creation & Management
- Generate unique 8-character room codes
- Set room mode (collaborative/interview/practice)
- Configure permissions
- Set problem for interview mode
- Invite participants

### 2. Real-Time Code Sync
- Use Operational Transformation (OT) for conflict resolution
- Track document version
- Apply changes atomically
- Handle concurrent edits
- Auto-save every 5 seconds

### 3. Live Cursors & Presence
- Assign unique color to each user
- Show cursor position with name tag
- Show selection ranges
- Typing indicators
- Online/offline status

### 4. Interview Mode
- Host creates interview room
- Assign candidate role
- Interviewer can watch live
- Optional interviewer edit permission
- Timer for interview duration
- Submit code to judge system
- View results together

### 5. Chat System
- Real-time messaging
- System notifications
- Code snippet sharing
- Emoji support

### 6. Code Execution
- Run code from collaborative editor
- Show results to all participants
- Submit to judge system
- View submission history

## Phase 6: Security & Performance

### Security
- JWT authentication for WebSocket
- Room access control
- Role-based permissions
- Rate limiting
- Input sanitization
- XSS prevention

### Performance
- Delta compression for code changes
- Message batching
- Connection pooling
- Redis for session state (optional)
- Horizontal scaling support

## Phase 7: Database Migrations

### Migration Files
```
005_create_rooms_table.py
006_create_room_participants_table.py
007_create_room_sessions_table.py
008_create_room_messages_table.py
009_create_room_code_snapshots_table.py
```

## Phase 8: Dependencies

### Backend
```
fastapi-websockets (included in FastAPI)
python-socketio (alternative)
redis (optional, for scaling)
```

### Frontend
```
npm install socket.io-client
npm install @monaco-editor/react
npm install yjs y-websocket (for CRDT, optional)
```

## Phase 9: Implementation Steps

### Step 1: Database Setup (Day 1)
1. Create migration files
2. Define models
3. Define schemas
4. Run migrations

### Step 2: Backend Core (Day 2-3)
1. WebSocket manager
2. Room manager
3. Code sync service
4. HTTP endpoints
5. WebSocket endpoints

### Step 3: Frontend Core (Day 4-5)
1. WebSocket hook
2. Room lobby page
3. Collaborative editor page
4. Basic UI components

### Step 4: Real-Time Features (Day 6-7)
1. Code synchronization
2. Live cursors
3. Presence tracking
4. Chat system

### Step 5: Interview Mode (Day 8-9)
1. Interview room creation
2. Role management
3. Interview controls
4. Judge integration

### Step 6: Polish & Testing (Day 10)
1. Error handling
2. Reconnection logic
3. UI/UX improvements
4. Testing

## Phase 10: Backward Compatibility

### Ensure Existing Features Work
- ✅ Current judge system
- ✅ Authentication
- ✅ Submissions
- ✅ AI feedback
- ✅ Problem management
- ✅ User management

### Integration Points
- Rooms can use existing problems
- Code execution uses existing judge
- Submissions from rooms saved normally
- AI feedback works in rooms

## Phase 11: Future Enhancements

### Phase 2 Features
- Voice/video integration (WebRTC)
- Whiteboard panel
- Screen sharing
- Recording sessions
- Analytics dashboard
- Room templates
- Scheduled interviews

## Summary

This implementation provides:
✅ Real-time collaborative coding
✅ WebSocket-based communication
✅ Live cursor tracking
✅ Interview mode
✅ Role-based permissions
✅ Chat system
✅ Judge integration
✅ Session history
✅ Scalable architecture
✅ Backward compatible

**Estimated Timeline**: 10 days for MVP
**Complexity**: High
**Impact**: Major feature addition
