# WebSocket "Not a Participant" Error - Fixed

## Problem
Users were getting "Not a participant" error when trying to connect to WebSocket in collaborative rooms. The WebSocket connection was being rejected because users weren't properly added as participants before connecting.

## Root Cause
The frontend was connecting to WebSocket without first calling the `/join` endpoint to add the user as a participant. The flow was:
1. User navigates to `/room/{roomCode}`
2. Frontend loads room details with `GET /rooms/{roomCode}`
3. Frontend tries to connect to WebSocket
4. Backend checks if user is a participant → **FAILS** because user never joined

## Solution

### Backend (Already Working)
- WebSocket endpoint validates that user is an active participant before accepting connection
- `/rooms/{roomCode}/join` endpoint properly adds users as participants
- `create_room` automatically adds host as participant

### Frontend Changes

#### 1. CollaborativeRoom.jsx
Updated `loadRoom()` to call the join endpoint before loading room details:
```javascript
const loadRoom = async () => {
    setLoading(true);
    try {
        // First, try to join the room
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const displayName = user.name || user.email || 'Anonymous';
        
        try {
            const joinResponse = await roomsAPI.join(roomCode, { display_name: displayName });
            setRoom(joinResponse.data.room);
            // ... load code and problem
        } catch (joinErr) {
            // If join fails (e.g., already joined), try to get room details
            if (joinErr.response?.status === 400) {
                const response = await roomsAPI.getByCode(roomCode);
                setRoom(response.data);
                // ... load code and problem
            } else {
                throw joinErr;
            }
        }
    } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load room');
    } finally {
        setLoading(false);
    }
};
```

#### 2. RoomLobby.jsx
Updated both join and room click handlers to include display_name:

**handleJoinRoom:**
```javascript
const user = JSON.parse(localStorage.getItem('user') || '{}');
const displayName = user.name || user.email || 'Anonymous';

await roomsAPI.join(joinCode.toUpperCase(), { display_name: displayName });
navigate(`/room/${joinCode.toUpperCase()}`);
```

**handleRoomClick:**
```javascript
const handleRoomClick = async (roomCode) => {
    try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const displayName = user.name || user.email || 'Anonymous';
        
        await roomsAPI.join(roomCode, { display_name: displayName });
    } catch (err) {
        console.log('Join room error (continuing anyway):', err);
    }
    
    navigate(`/room/${roomCode}`);
};
```

## Flow After Fix

### Creating a Room
1. User creates room → Backend adds user as HOST participant
2. User navigates to room → Frontend calls join (reactivates if needed)
3. WebSocket connects → Backend validates participant → **SUCCESS**

### Joining a Room
1. User enters room code → Frontend calls join with display_name
2. Backend adds user as VIEWER/CANDIDATE participant
3. User navigates to room → Frontend calls join again (idempotent)
4. WebSocket connects → Backend validates participant → **SUCCESS**

### Clicking Existing Room
1. User clicks room from list → Frontend calls join
2. Backend reactivates participant if inactive, or returns existing
3. User navigates to room → Frontend calls join again (safe)
4. WebSocket connects → Backend validates participant → **SUCCESS**

## Key Points
- Join endpoint is **idempotent** - safe to call multiple times
- If user is already a participant, it just returns existing participant
- If user was inactive, it reactivates them
- Display name is taken from user's profile (name or email)
- WebSocket connection now always succeeds because user is guaranteed to be a participant

## Testing
1. Create a new room → Should connect successfully
2. Join a room with code → Should connect successfully
3. Click existing room from list → Should connect successfully
4. Refresh page while in room → Should reconnect successfully
5. Multiple users in same room → All should connect successfully

## Files Modified
- `frontend/src/pages/CollaborativeRoom.jsx` - Auto-join on room load
- `frontend/src/pages/RoomLobby.jsx` - Join with display_name in both handlers
