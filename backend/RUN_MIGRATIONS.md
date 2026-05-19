# How to Run Database Migrations

## What Are Migrations?
Migrations are version-controlled database schema changes. They allow you to update your database structure (add tables, columns, etc.) in a safe, reversible way.

## Migration Files Created
We've created 5 new migration files for the collaborative coding feature:
- `005_create_rooms_table.py` - Main rooms table
- `006_create_room_participants_table.py` - Participants tracking
- `007_create_room_sessions_table.py` - Current code state
- `008_create_room_messages_table.py` - Chat messages
- `009_create_room_code_snapshots_table.py` - Version history

## How to Run Migrations

### Method 1: Using Alembic (Recommended)

```bash
cd backend

# Check current migration status
python migrate.py current

# Run all pending migrations
python migrate.py upgrade

# Or use alembic directly
alembic upgrade head
```

### Method 2: Mark Migrations as Complete (If Already Applied)

If you've already applied schema changes manually:

```bash
cd backend
python migrate.py stamp head
```

### Method 3: Manual SQL (If Migrations Fail)

If migrations fail, you can run the SQL manually in pgAdmin:

```sql
-- 1. Create enum types
CREATE TYPE room_mode AS ENUM ('collaborative', 'interview', 'practice');
CREATE TYPE room_status AS ENUM ('active', 'ended', 'archived');
CREATE TYPE participant_role AS ENUM ('host', 'interviewer', 'candidate', 'viewer');
CREATE TYPE message_type AS ENUM ('chat', 'system', 'code_run');
CREATE TYPE snapshot_type AS ENUM ('auto', 'manual', 'submission');

-- 2. Create rooms table
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    room_code VARCHAR(8) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    host_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id INTEGER REFERENCES problems(id) ON DELETE SET NULL,
    mode room_mode NOT NULL DEFAULT 'collaborative',
    status room_status NOT NULL DEFAULT 'active',
    max_participants INTEGER NOT NULL DEFAULT 10,
    settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_rooms_id ON rooms(id);
CREATE INDEX ix_rooms_room_code ON rooms(room_code);
CREATE INDEX ix_rooms_host_user_id ON rooms(host_user_id);
CREATE INDEX ix_rooms_problem_id ON rooms(problem_id);

-- 3. Create room_participants table
CREATE TABLE room_participants (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role participant_role NOT NULL DEFAULT 'viewer',
    display_name VARCHAR(100) NOT NULL,
    cursor_color VARCHAR(7) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    left_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_room_participants_id ON room_participants(id);
CREATE INDEX ix_room_participants_room_id ON room_participants(room_id);
CREATE INDEX ix_room_participants_user_id ON room_participants(user_id);

-- 4. Create room_sessions table
CREATE TABLE room_sessions (
    id SERIAL PRIMARY KEY,
    room_id INTEGER UNIQUE NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    code TEXT NOT NULL DEFAULT '',
    language VARCHAR(20) NOT NULL DEFAULT 'python',
    version INTEGER NOT NULL DEFAULT 0,
    last_edited_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    last_edited_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_room_sessions_id ON room_sessions(id);
CREATE INDEX ix_room_sessions_room_id ON room_sessions(room_id);

-- 5. Create room_messages table
CREATE TABLE room_messages (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    message_type message_type NOT NULL DEFAULT 'chat',
    content TEXT NOT NULL,
    message_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ix_room_messages_id ON room_messages(id);
CREATE INDEX ix_room_messages_room_id ON room_messages(room_id);

-- 6. Create room_code_snapshots table
CREATE TABLE room_code_snapshots (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language VARCHAR(20) NOT NULL,
    snapshot_type snapshot_type NOT NULL DEFAULT 'auto',
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ix_room_code_snapshots_id ON room_code_snapshots(id);
CREATE INDEX ix_room_code_snapshots_room_id ON room_code_snapshots(room_id);

-- Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'room%'
ORDER BY table_name;
```

## Verify Migrations

After running migrations, verify they worked:

```bash
cd backend
python -c "from app.models import Room, RoomParticipant, RoomSession, RoomMessage, RoomCodeSnapshot; print('✅ All models imported successfully!')"
```

Or check in PostgreSQL:

```sql
-- List all tables
\dt

-- Check rooms table structure
\d rooms

-- Check if enum types exist
\dT
```

## Troubleshooting

### Error: "column already exists"
The migration is trying to add a column that already exists. Either:
1. Skip that migration: `python migrate.py stamp 009`
2. Or drop the column first in pgAdmin

### Error: "relation already exists"
The table already exists. Mark migrations as complete:
```bash
python migrate.py stamp head
```

### Error: "enum type already exists"
The enum type already exists. You can either:
1. Drop it first: `DROP TYPE room_mode CASCADE;`
2. Or skip the migration

## Next Steps

After migrations are complete:
1. ✅ Database schema is ready
2. ⏭️ Implement WebSocket manager
3. ⏭️ Create room endpoints
4. ⏭️ Build frontend components

## Rollback (If Needed)

To undo migrations:

```bash
cd backend

# Rollback one migration
python migrate.py downgrade -1

# Rollback to specific version
python migrate.py downgrade 004

# Rollback all collaborative coding migrations
python migrate.py downgrade 004
```

## Summary

**Quick Start:**
```bash
cd backend
python migrate.py upgrade
```

That's it! Your database is now ready for collaborative coding features.
