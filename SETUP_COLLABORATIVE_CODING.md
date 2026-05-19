# Setup Collaborative Coding Feature - Quick Start

## Step 1: Run Migrations

### Option A: Automated Setup (Recommended)
```bash
cd backend
python setup_collaborative_coding.py
```

### Option B: Manual Migration
```bash
cd backend
python migrate.py upgrade
```

### Option C: Manual SQL (If migrations fail)
Open pgAdmin and run the SQL from `backend/RUN_MIGRATIONS.md`

## Step 2: Verify Setup

Check that tables were created:

```sql
-- In pgAdmin or psql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'room%'
ORDER BY table_name;
```

You should see:
- ✅ room_code_snapshots
- ✅ room_messages
- ✅ room_participants
- ✅ room_sessions
- ✅ rooms

## Step 3: Verify Models

```bash
cd backend
python -c "from app.models import Room, RoomParticipant, RoomSession, RoomMessage, RoomCodeSnapshot; print('✅ Success!')"
```

## What Was Created?

### Database Tables (5 new tables)
1. **rooms** - Main room entity with settings
2. **room_participants** - Tracks who's in each room
3. **room_sessions** - Stores current code state
4. **room_messages** - Chat and system messages
5. **room_code_snapshots** - Version history

### Models (5 new models)
- `backend/app/models/room.py`
- `backend/app/models/room_participant.py`
- `backend/app/models/room_session.py`
- `backend/app/models/room_message.py`
- `backend/app/models/room_code_snapshot.py`

### Migrations (5 new migrations)
- `005_create_rooms_table.py`
- `006_create_room_participants_table.py`
- `007_create_room_sessions_table.py`
- `008_create_room_messages_table.py`
- `009_create_room_code_snapshots_table.py`

## Troubleshooting

### "Migration failed"
- Check PostgreSQL is running
- Verify database credentials in `.env`
- Try manual SQL approach (see `RUN_MIGRATIONS.md`)

### "Table already exists"
```bash
python migrate.py stamp head
```

### "Cannot import models"
- Make sure you're in the backend directory
- Check that all model files exist
- Verify `app/models/__init__.py` includes new models

## Next Steps

Now that the database is ready, you can:

1. **Implement Backend Services**
   - WebSocket manager
   - Room manager
   - Code sync service

2. **Create API Endpoints**
   - Room CRUD operations
   - WebSocket endpoint
   - Participant management

3. **Build Frontend**
   - Room lobby page
   - Collaborative editor
   - WebSocket integration

See `COLLABORATIVE_CODING_PLAN.md` for the complete implementation roadmap.

## Quick Commands

```bash
# Run migrations
cd backend && python migrate.py upgrade

# Verify models
python -c "from app.models import Room; print('✅')"

# Check migration status
python migrate.py current

# Rollback if needed
python migrate.py downgrade 004
```

## Summary

✅ **Database schema ready**
✅ **Models created**
✅ **Migrations applied**

You're now ready to implement the collaborative coding features!
