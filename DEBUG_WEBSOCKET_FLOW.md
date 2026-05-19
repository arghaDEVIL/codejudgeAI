# WebSocket Connection Flow - Debug Guide

## Updated Flow (After Fix)

### 1. User Navigates to Room
```
User clicks "Join Room" or navigates to /room/{roomCode}
↓
CollaborativeRoom component mounts
↓
isJoined = false (WebSocket does NOT connect yet)
↓
loadRoom() is called
```

### 2. Join Room API Call
```
loadRoom() executes:
↓
Call: POST /api/v1/rooms/{roomCode}/join
Body: { display_name: "User Name" }
↓
Backend adds user as participant (or reactivates if inactive)
↓
Response: { room: {...}, participant_id: X, cursor_color: "#...", role: "..." }
↓
setIsJoined(true) ← This triggers WebSocket connection
```

### 3. WebSocket Connection
```
isJoined changes from false → true
↓
useWebSocket hook detects change
↓
connect() is called
↓
WebSocket connects to: ws://127.0.0.1:8000/ws/room/{roomCode}?token={JWT}
↓
Backend validates:
  - Token is valid ✓
  - Room exists ✓
  - User is an active participant ✓ (because we just joined!)
↓
Connection accepted!
```

## Key Changes Made

### frontend/src/pages/CollaborativeRoom.jsx
1. Added `isJoined` state variable (default: false)
2. Pass `isJoined` to `useWebSocket` as the `enabled` parameter
3. Set `isJoined = true` AFTER successful join API call

### frontend/src/hooks/useWebSocket.js
- Already supports `enabled` parameter
- Only connects when `enabled === true`

## Testing Steps

### Test 1: Create New Room
1. Login as User A
2. Click "Create Room"
3. Fill in details and create
4. **Expected**: Automatically joins and connects to WebSocket
5. **Check**: No "Not a participant" error
6. **Check**: Can see yourself in participants list

### Test 2: Join Existing Room
1. Login as User B
2. Enter room code from Test 1
3. Click "Join Room"
4. **Expected**: Joins room and connects to WebSocket
5. **Check**: No "Not a participant" error
6. **Check**: Both users see each other in participants list

### Test 3: Rejoin Room
1. User A refreshes the page
2. **Expected**: Automatically rejoins and reconnects
3. **Check**: No "Not a participant" error
4. **Check**: Connection is restored

### Test 4: Multiple Users
1. Login as User C
2. Join the same room
3. **Expected**: All 3 users connected
4. **Check**: All users see each other
5. **Check**: Code changes sync across all users

## Debug Checklist

If you still see "Not a participant" error:

### 1. Check Browser Console
Look for these logs in order:
```
[WebSocket] Connecting to: ws://127.0.0.1:8000/ws/room/XXXXX?token=...
[WebSocket] Connected
[WebSocket] Received: room_state
```

If you see:
```
[WebSocket] Received: error
[WebSocket] Error: Not a participant
[WebSocket] Closed: 1008
```
Then the join API call didn't complete before WebSocket connected.

### 2. Check Network Tab
Look for API calls in this order:
1. `POST /api/v1/rooms/{roomCode}/join` → Status 200
2. WebSocket connection to `/ws/room/{roomCode}` → Status 101 (Switching Protocols)

If WebSocket connects BEFORE the join API call completes, that's the issue.

### 3. Check Backend Logs
Look for:
```
[WS] Query string: token=...
[WS] Authenticated user_id: X
[WS Auth] User ID: X
```

If you see:
```
Not a participant
```
Then the user is not in the `room_participants` table with `is_active = true`.

### 4. Check Database
```sql
-- Check if user is a participant
SELECT * FROM room_participants 
WHERE room_id = (SELECT id FROM rooms WHERE room_code = 'XXXXX')
AND user_id = YOUR_USER_ID;

-- Should show:
-- is_active = true
-- left_at = NULL
```

### 5. Hard Refresh Browser
After code changes:
- Press `Ctrl + Shift + R` (Windows)
- Or `Cmd + Shift + R` (Mac)
- This clears cached JavaScript

### 6. Restart Backend
```bash
cd backend
# Kill existing process
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
# Start fresh
python run.py
```

## Common Issues

### Issue: WebSocket connects before join completes
**Symptom**: "Not a participant" error
**Cause**: Race condition - WebSocket hook connects too early
**Fix**: Ensure `isJoined` is only set to `true` AFTER join API succeeds

### Issue: User already joined but still gets error
**Symptom**: Error on page refresh
**Cause**: `is_active` is false in database
**Fix**: Join endpoint should reactivate inactive participants (already implemented)

### Issue: Token expired
**Symptom**: "Authentication failed" error
**Cause**: JWT token expired
**Fix**: Login again to get fresh token

### Issue: Room doesn't exist
**Symptom**: "Room not found" error
**Cause**: Invalid room code or room was deleted
**Fix**: Create a new room or use valid room code

## Success Indicators

When everything works correctly, you should see:

1. **Browser Console**:
   ```
   [WebSocket] Connecting to: ws://...
   [WebSocket] Connected
   [WebSocket] Received: room_state
   ```

2. **Network Tab**:
   - Join API: Status 200
   - WebSocket: Status 101 (green)

3. **UI**:
   - "Connected" indicator (green dot)
   - Participants list shows all users
   - Code changes sync in real-time
   - Chat messages appear for all users

4. **Backend Logs**:
   ```
   [WS] Authenticated user_id: X
   [WS] Connected
   ```

## Additional Notes

- The join endpoint is **idempotent** - safe to call multiple times
- If user is already a participant, it returns existing participant data
- If user was inactive, it reactivates them
- WebSocket will auto-reconnect on connection loss (up to 5 attempts)
- Ping/pong keeps connection alive (every 30 seconds)
