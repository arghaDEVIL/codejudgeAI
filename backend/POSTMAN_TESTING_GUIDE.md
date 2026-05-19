# Postman Testing Guide - Collaborative Coding API

## Prerequisites

1. Backend server running: `python run.py` (should be at http://127.0.0.1:8000)
2. PostgreSQL database running
3. At least one user account created
4. Postman installed

## Step 1: Authentication (Get JWT Token)

### Register a User (if needed)
```
POST http://127.0.0.1:8000/api/v1/auth/register

Headers:
Content-Type: application/json

Body (JSON):
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Login
```
POST http://127.0.0.1:8000/api/v1/auth/login

Headers:
Content-Type: application/json

Body (JSON):
{
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**IMPORTANT:** Copy the `access_token` value. You'll need it for all subsequent requests.

---

## Step 2: Room Management Tests

### Test 1: Create a Room
```
POST http://127.0.0.1:8000/api/v1/rooms/

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>
Content-Type: application/json

Body (JSON):
{
  "title": "My First Coding Room",
  "description": "Testing collaborative coding",
  "mode": "collaborative",
  "max_participants": 10
}

Expected Response (201 Created):
{
  "id": 1,
  "room_code": "ABC12XYZ",
  "title": "My First Coding Room",
  "description": "Testing collaborative coding",
  "host_user_id": 1,
  "problem_id": null,
  "mode": "collaborative",
  "status": "active",
  "max_participants": 10,
  "settings": {},
  "created_at": "2026-04-21T...",
  "updated_at": null,
  "ended_at": null,
  "participant_count": 1
}
```

**IMPORTANT:** Copy the `room_code` value (e.g., "ABC12XYZ"). You'll need it for other tests.

---

### Test 2: Get Room Details
```
GET http://127.0.0.1:8000/api/v1/rooms/{room_code}

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>

Example:
GET http://127.0.0.1:8000/api/v1/rooms/ABC12XYZ

Expected Response (200 OK):
{
  "id": 1,
  "room_code": "ABC12XYZ",
  "title": "My First Coding Room",
  "description": "Testing collaborative coding",
  "host_user_id": 1,
  "problem_id": null,
  "mode": "collaborative",
  "status": "active",
  "max_participants": 10,
  "settings": {},
  "created_at": "2026-04-21T...",
  "updated_at": null,
  "ended_at": null,
  "participant_count": 1,
  "participants": [
    {
      "id": 1,
      "user_id": 1,
      "display_name": "Test User",
      "role": "host",
      "cursor_color": "#FF6B6B",
      "is_active": true,
      "joined_at": "2026-04-21T..."
    }
  ],
  "current_code": "",
  "current_language": "python"
}
```

---

### Test 3: List User's Rooms
```
GET http://127.0.0.1:8000/api/v1/rooms/

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>

Expected Response (200 OK):
[
  {
    "id": 1,
    "room_code": "ABC12XYZ",
    "title": "My First Coding Room",
    "description": "Testing collaborative coding",
    "host_user_id": 1,
    "problem_id": null,
    "mode": "collaborative",
    "status": "active",
    "max_participants": 10,
    "settings": {},
    "created_at": "2026-04-21T...",
    "updated_at": null,
    "ended_at": null,
    "participant_count": 1
  }
]
```

---

### Test 4: Join a Room (with second user)
**Note:** You'll need a second user account and token for this test.

```
POST http://127.0.0.1:8000/api/v1/rooms/{room_code}/join

Headers:
Authorization: Bearer <SECOND_USER_TOKEN>
Content-Type: application/json

Body (JSON):
{
  "display_name": "Second User"
}

Expected Response (200 OK):
{
  "room": {
    "id": 1,
    "room_code": "ABC12XYZ",
    "title": "My First Coding Room",
    ...
    "participant_count": 2,
    "participants": [
      {
        "id": 1,
        "user_id": 1,
        "display_name": "Test User",
        "role": "host",
        ...
      },
      {
        "id": 2,
        "user_id": 2,
        "display_name": "Second User",
        "role": "viewer",
        ...
      }
    ],
    "current_code": "",
    "current_language": "python"
  },
  "participant_id": 2,
  "cursor_color": "#4ECDC4",
  "role": "viewer"
}
```

---

### Test 5: Get Room Participants
```
GET http://127.0.0.1:8000/api/v1/rooms/{room_code}/participants

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>

Expected Response (200 OK):
[
  {
    "id": 1,
    "user_id": 1,
    "display_name": "Test User",
    "role": "host",
    "cursor_color": "#FF6B6B",
    "is_active": true,
    "joined_at": "2026-04-21T...",
    "left_at": null
  },
  {
    "id": 2,
    "user_id": 2,
    "display_name": "Second User",
    "role": "viewer",
    "cursor_color": "#4ECDC4",
    "is_active": true,
    "joined_at": "2026-04-21T...",
    "left_at": null
  }
]
```

---

### Test 6: Send Chat Message
```
POST http://127.0.0.1:8000/api/v1/rooms/{room_code}/messages

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>
Content-Type: application/json

Body (JSON):
{
  "content": "Hello everyone! This is a test message."
}

Expected Response (201 Created):
{
  "id": 2,
  "user_id": 1,
  "message_type": "chat",
  "content": "Hello everyone! This is a test message.",
  "created_at": "2026-04-21T..."
}
```

---

### Test 7: Get Chat Messages
```
GET http://127.0.0.1:8000/api/v1/rooms/{room_code}/messages?limit=50

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>

Expected Response (200 OK):
[
  {
    "id": 1,
    "user_id": null,
    "message_type": "system",
    "content": "Room created by Test User",
    "message_data": {},
    "created_at": "2026-04-21T..."
  },
  {
    "id": 2,
    "user_id": 1,
    "message_type": "chat",
    "content": "Hello everyone! This is a test message.",
    "message_data": {},
    "created_at": "2026-04-21T..."
  }
]
```

---

### Test 8: Update Room (Host Only)
```
PUT http://127.0.0.1:8000/api/v1/rooms/{room_code}

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>
Content-Type: application/json

Body (JSON):
{
  "title": "Updated Room Title",
  "description": "Updated description"
}

Expected Response (200 OK):
{
  "id": 1,
  "room_code": "ABC12XYZ",
  "title": "Updated Room Title",
  "description": "Updated description",
  ...
}
```

---

### Test 9: Leave Room
```
POST http://127.0.0.1:8000/api/v1/rooms/{room_code}/leave

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>

Expected Response (204 No Content):
(Empty response body)
```

---

### Test 10: Create Interview Room
```
POST http://127.0.0.1:8000/api/v1/rooms/

Headers:
Authorization: Bearer <YOUR_TOKEN_HERE>
Content-Type: application/json

Body (JSON):
{
  "title": "Technical Interview - Software Engineer",
  "description": "Coding interview for backend position",
  "mode": "interview",
  "problem_id": 1,
  "max_participants": 5,
  "settings": {
    "allow_interviewer_edit": true,
    "show_timer": true,
    "duration_minutes": 60
  }
}

Expected Response (201 Created):
{
  "id": 2,
  "room_code": "XYZ98ABC",
  "title": "Technical Interview - Software Engineer",
  "description": "Coding interview for backend position",
  "mode": "interview",
  "problem_id": 1,
  ...
}
```

---

## Step 3: WebSocket Testing

### Using Postman WebSocket

1. **Create New WebSocket Request**
   - Click "New" → "WebSocket Request"

2. **Connect to Room**
   ```
   ws://127.0.0.1:8000/ws/room/{room_code}?token=<YOUR_TOKEN_HERE>
   
   Example:
   ws://127.0.0.1:8000/ws/room/ABC12XYZ?token=eyJhbGc...
   ```

3. **Click "Connect"**
   - You should see connection established
   - Server will send initial `room_state` message

4. **Test Messages**

   **Send Code Change:**
   ```json
   {
     "type": "code_change",
     "data": {
       "code": "def hello():\n    print('Hello World')",
       "language": "python",
       "changes": []
     }
   }
   ```

   **Send Cursor Move:**
   ```json
   {
     "type": "cursor_move",
     "data": {
       "position": {
         "line": 5,
         "column": 10
       }
     }
   }
   ```

   **Send Chat Message:**
   ```json
   {
     "type": "chat_message",
     "data": {
       "message": "Hello from WebSocket!"
     }
   }
   ```

   **Send Ping:**
   ```json
   {
     "type": "ping",
     "data": {}
   }
   ```

5. **Expected Server Messages**

   **On Connect:**
   ```json
   {
     "type": "room_state",
     "data": {
       "participants": [...],
       "room_code": "ABC12XYZ"
     },
     "timestamp": "2026-04-21T..."
   }
   ```

   **When Another User Joins:**
   ```json
   {
     "type": "user_joined",
     "data": {
       "user_id": 2,
       "display_name": "Second User",
       "cursor_color": "#4ECDC4",
       "role": "viewer",
       "is_active": true,
       "cursor_position": null,
       "connected_at": "2026-04-21T..."
     },
     "timestamp": "2026-04-21T..."
   }
   ```

   **Code Update from Another User:**
   ```json
   {
     "type": "code_update",
     "data": {
       "user_id": 2,
       "code": "def hello():\n    print('Hello World')",
       "language": "python",
       "changes": []
     },
     "timestamp": "2026-04-21T..."
   }
   ```

   **Cursor Update:**
   ```json
   {
     "type": "cursor_update",
     "data": {
       "user_id": 2,
       "position": {
         "line": 5,
         "column": 10
       }
     },
     "timestamp": "2026-04-21T..."
   }
   ```

   **Chat Message:**
   ```json
   {
     "type": "chat_message",
     "data": {
       "user_id": 2,
       "user_name": "Second User",
       "message": "Hello from WebSocket!"
     },
     "timestamp": "2026-04-21T..."
   }
   ```

---

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**Solution:** Check your JWT token is valid and included in Authorization header.

### 404 Not Found
```json
{
  "detail": "Room not found"
}
```
**Solution:** Verify the room_code is correct.

### 400 Bad Request
```json
{
  "detail": "Room is full"
}
```
**Solution:** Room has reached max_participants limit.

### 403 Forbidden
```json
{
  "detail": "Only host can update room"
}
```
**Solution:** Only the room host can update room settings.

---

## Testing Checklist

- [ ] Register/Login and get JWT token
- [ ] Create a room
- [ ] Get room details
- [ ] List user's rooms
- [ ] Join room with second user
- [ ] Get room participants
- [ ] Send chat message
- [ ] Get chat messages
- [ ] Update room (as host)
- [ ] Leave room
- [ ] Create interview room
- [ ] Connect via WebSocket
- [ ] Send code change via WebSocket
- [ ] Send cursor move via WebSocket
- [ ] Send chat via WebSocket
- [ ] Test with multiple WebSocket connections

---

## Tips for Testing

1. **Save Tokens:** Create Postman environment variables for tokens
   - Variable: `auth_token`
   - Use: `{{auth_token}}` in Authorization headers

2. **Save Room Code:** Create variable for room_code
   - Variable: `room_code`
   - Use: `{{room_code}}` in URLs

3. **Multiple Users:** Open multiple Postman windows or use different browsers to test real-time collaboration

4. **WebSocket Testing:** Keep WebSocket connection open in one window while making HTTP requests in another

5. **Check Backend Logs:** Watch the terminal where `python run.py` is running for any errors

---

## Next Steps After Testing

Once all tests pass:
1. ✅ Backend is fully functional
2. Move to frontend implementation
3. Build room lobby UI
4. Implement collaborative editor with Monaco
5. Integrate WebSocket for real-time sync

---

## Troubleshooting

**Server not starting?**
- Check PostgreSQL is running
- Verify `.env` file has correct database credentials
- Check for import errors in terminal

**WebSocket connection fails?**
- Ensure token is valid (not expired)
- Check room exists and user is a participant
- Verify WebSocket URL format is correct

**Database errors?**
- Run migrations: `alembic upgrade head`
- Check database tables exist
- Verify user has permissions

---

Happy Testing! 🚀
