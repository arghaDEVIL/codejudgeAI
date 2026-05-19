# Frontend Implementation Guide - Collaborative Coding

## Overview
Build the React frontend for real-time collaborative coding with WebSocket integration.

## Step 1: Install Dependencies ✅

```bash
cd frontend
npm install socket.io-client @monaco-editor/react
```

## Step 2: File Structure

```
frontend/src/
├── pages/
│   ├── RoomLobby.jsx          # Create/join rooms UI
│   └── CollaborativeRoom.jsx  # Main collaborative editor page
├── hooks/
│   └── useWebSocket.js        # WebSocket connection management
├── components/
│   └── room/
│       ├── ParticipantsList.jsx  # Show active participants
│       ├── ChatPanel.jsx          # Chat interface
│       └── CodeEditor.jsx         # Monaco editor wrapper
└── utils/
    └── api.js                 # Add room API functions

```

## Step 3: Implementation Order

### 3.1 Update API Utils
Add room-related API functions to `utils/api.js`:
- `createRoom()`
- `getRoomDetails()`
- `joinRoom()`
- `leaveRoom()`
- `getUserRooms()`

### 3.2 Create WebSocket Hook
`hooks/useWebSocket.js` - Manages WebSocket connection:
- Connect/disconnect
- Send/receive messages
- Handle reconnection
- Manage connection state

### 3.3 Create Room Lobby
`pages/RoomLobby.jsx` - Entry point:
- Create new room form
- Join existing room with code
- List user's active rooms
- Navigate to collaborative room

### 3.4 Create Collaborative Room
`pages/CollaborativeRoom.jsx` - Main page:
- Monaco code editor
- Participants list
- Chat panel
- Real-time sync
- Leave room button

### 3.5 Create Components
- `ParticipantsList.jsx` - Show users with colors
- `ChatPanel.jsx` - Send/receive messages
- `CodeEditor.jsx` - Monaco editor with sync

### 3.6 Update App Routing
Add routes in `App.jsx`:
- `/rooms` - Room lobby
- `/room/:roomCode` - Collaborative room

## Step 4: Key Features

### WebSocket Integration
```javascript
// Connect
ws = new WebSocket(`ws://localhost:8000/ws/room/${roomCode}?token=${token}`)

// Send code change
ws.send(JSON.stringify({
  type: 'code_change',
  data: { code, language }
}))

// Receive updates
ws.onmessage = (event) => {
  const message = JSON.parse(event.data)
  // Handle: code_update, chat_message, user_joined, user_left
}
```

### Real-Time Code Sync
- Debounce code changes (500ms)
- Send changes via WebSocket
- Apply remote changes to editor
- Prevent infinite loops

### Participant Tracking
- Show online users
- Display cursor colors
- Show roles (host, viewer, etc.)
- Join/leave notifications

### Chat System
- Send messages
- Receive broadcasts
- Show user names
- Scroll to bottom

## Step 5: UI Design

### Room Lobby Layout
```
┌─────────────────────────────────────┐
│  CodeJudge AI - Collaborative Rooms │
├─────────────────────────────────────┤
│  Create New Room                    │
│  ┌─────────────────────────────┐   │
│  │ Title: [____________]        │   │
│  │ Mode: [Collaborative ▼]     │   │
│  │ [Create Room]               │   │
│  └─────────────────────────────┘   │
│                                     │
│  Join Room                          │
│  ┌─────────────────────────────┐   │
│  │ Room Code: [________]        │   │
│  │ [Join]                       │   │
│  └─────────────────────────────┘   │
│                                     │
│  Your Rooms                         │
│  ┌─────────────────────────────┐   │
│  │ • Room ABC123 (2 users)     │   │
│  │ • Room XYZ789 (1 user)      │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Collaborative Room Layout
```
┌──────────────────────────────────────────────────────┐
│  Room: ABC123  |  2 participants  |  [Leave Room]   │
├────────────────────────────────┬─────────────────────┤
│                                │  Participants       │
│                                │  ┌───────────────┐ │
│                                │  │ 🟢 You (Host) │ │
│                                │  │ 🟢 User2      │ │
│      Monaco Code Editor        │  └───────────────┘ │
│                                │                     │
│                                │  Chat               │
│                                │  ┌───────────────┐ │
│                                │  │ User2: Hi!    │ │
│                                │  │ You: Hello    │ │
│                                │  └───────────────┘ │
│                                │  [Type message__] │
└────────────────────────────────┴─────────────────────┘
```

## Step 6: State Management

### Room State
```javascript
{
  roomCode: 'ABC123',
  title: 'My Room',
  participants: [
    { userId: 1, displayName: 'User1', role: 'host', cursorColor: '#FF6B6B' }
  ],
  code: 'print("Hello")',
  language: 'python'
}
```

### WebSocket State
```javascript
{
  connected: false,
  connecting: false,
  error: null,
  messages: []
}
```

## Step 7: Error Handling

- Connection failures
- Authentication errors
- Room not found
- Network issues
- Reconnection logic

## Step 8: Testing Checklist

- [ ] Create room
- [ ] Join room with code
- [ ] See other participants
- [ ] Type code and see it sync
- [ ] Send chat messages
- [ ] Leave room
- [ ] Reconnect after disconnect
- [ ] Multiple users editing simultaneously

## Step 9: Styling

Use existing CSS patterns from:
- `Judge.jsx` - For layout
- `Login.jsx` - For forms
- `SubmissionHistory.jsx` - For lists

Keep consistent with current design.

## Step 10: Integration with Existing Features

### Navigation
Add "Rooms" link to navigation bar

### Authentication
Use existing `localStorage.getItem('token')`

### API Base URL
Use existing `API_BASE_URL` from `api.js`

## Quick Start Commands

```bash
# Install dependencies
cd frontend
npm install socket.io-client @monaco-editor/react

# Start development server
npm run dev

# Backend should be running
cd backend
python run.py
```

## API Endpoints Reference

```
POST   /api/v1/rooms/                    # Create room
GET    /api/v1/rooms/{code}              # Get room details
POST   /api/v1/rooms/{code}/join         # Join room
POST   /api/v1/rooms/{code}/leave        # Leave room
GET    /api/v1/rooms/                    # List user's rooms
WS     /ws/room/{code}?token=<jwt>       # WebSocket connection
```

## WebSocket Message Types

### Client → Server
- `code_change` - Code edited
- `cursor_move` - Cursor moved
- `chat_message` - Chat sent
- `ping` - Keep-alive

### Server → Client
- `room_state` - Initial state
- `code_update` - Code changed
- `cursor_update` - Cursor moved
- `chat_message` - Chat received
- `user_joined` - User joined
- `user_left` - User left
- `pong` - Ping response

## Next Steps

1. Install dependencies
2. Create WebSocket hook
3. Update API utils
4. Build Room Lobby
5. Build Collaborative Room
6. Test with multiple users

Ready to start building!
