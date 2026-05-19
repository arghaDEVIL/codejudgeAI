# 🗄️ Database Migration Guide

## Setup

### 1. Install Alembic
```bash
pip install alembic
```

### 2. Initialize (Already Done)
The migration system is already set up with:
- `alembic.ini` - Configuration
- `alembic/env.py` - Environment setup
- `alembic/versions/` - Migration files

## Quick Commands

### Run Migrations
```bash
# Option 1: Using helper script
python migrate.py upgrade

# Option 2: Using alembic directly
alembic upgrade head
```

### Create New Migration
```bash
# Auto-generate from model changes
python migrate.py create "add new column"

# Or with alembic
alembic revision --autogenerate -m "add new column"
```

### Check Current Version
```bash
python migrate.py current
# or
alembic current
```

### View History
```bash
python migrate.py history
# or
alembic history
```

### Rollback
```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade 001

# Rollback all
alembic downgrade base
```

## Migration Workflow

### 1. Fix Existing Database
If you have an existing database with missing columns:

```bash
# Run the timestamp migration
python migrate.py upgrade
```

This will add:
- `created_at` and `updated_at` to users
- `created_at` and `updated_at` to problems
- `created_at`, `execution_time`, `memory_used` to submissions
- All new tables (testcases, testcase_results, ai_feedback)

### 2. Making Model Changes

When you modify models:

```bash
# 1. Edit your model in app/models/
# 2. Create migration
python migrate.py create "describe your change"

# 3. Review the generated migration in alembic/versions/
# 4. Run migration
python migrate.py upgrade
```

### 3. Fresh Database Setup

For a new database:

```bash
# Run all migrations
python migrate.py upgrade
```

## Current Migrations

### 001_initial_schema.py
- Creates all tables with proper structure
- Adds indexes and foreign keys
- Safe to run on existing databases (uses postgresql_ignore_tables)

### 002_add_missing_timestamps.py
- Adds missing timestamp columns to existing tables
- Safe to run multiple times (uses try/except)
- Fixes schema drift issues

## Troubleshooting

### "Table already exists" Error
The migrations are designed to be safe. They won't fail if tables exist.

### "Column already exists" Error
Migration 002 handles this gracefully with try/except blocks.

### Reset Everything
```bash
# Drop all tables
alembic downgrade base

# Recreate from scratch
alembic upgrade head
```

### Manual Column Addition
If migrations fail, you can manually add columns:

```sql
-- Add timestamps to users
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;

-- Add timestamps to problems
ALTER TABLE problems ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE problems ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;

-- Add columns to submissions
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS execution_time INTEGER;
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS memory_used FLOAT;
```

## Best Practices

1. **Always review auto-generated migrations** before running them
2. **Test migrations on a copy of production data** first
3. **Never edit migration files after they've been committed**
4. **Create a new migration** if you need to change something
5. **Keep migrations small and focused** on one change
6. **Add comments** to complex migrations

## Integration with Application

The app no longer uses `Base.metadata.create_all()` for schema changes.

### Old Way (Removed)
```python
# Don't do this anymore
Base.metadata.create_all(bind=engine)
```

### New Way
```python
# Run migrations before starting app
# python migrate.py upgrade
# python run.py
```

## Production Deployment

### Deployment Checklist
1. Backup database
2. Run migrations: `python migrate.py upgrade`
3. Verify migration success
4. Start application
5. Monitor for errors

### Automated Deployment
Add to your deployment script:

```bash
#!/bin/bash
# deploy.sh

# Backup database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Run migrations
python migrate.py upgrade

# Start application
python run.py
```

## FAQ

**Q: Do I need to run migrations every time?**
A: Only when there are new migrations. Check with `python migrate.py current`

**Q: Can I skip migrations?**
A: No, migrations must be run in order. Use `alembic upgrade head` to run all pending.

**Q: What if migration fails halfway?**
A: Alembic uses transactions. Failed migrations are rolled back automatically.

**Q: How do I see what changed?**
A: Check the migration file in `alembic/versions/` or use `alembic history -v`

---

**Status**: Migration system ready
**Next**: Run `python migrate.py upgrade` to fix schema drift
