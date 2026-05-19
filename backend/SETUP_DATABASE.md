# 🗄️ Database Setup - Quick Guide

## ✅ Commands to Run

### 1. Install Alembic
```bash
pip install alembic
```

### 2. Run Migrations
```bash
python migrate.py upgrade
```

This will:
- Create all tables if they don't exist
- Add missing timestamp columns to existing tables
- Add new tables (testcases, testcase_results, ai_feedback)
- Fix all schema drift issues

### 3. Start Application
```bash
python run.py
```

## 🎯 What Gets Fixed

### Existing Tables Updated:
- **users**: Adds `created_at`, `updated_at`
- **problems**: Adds `created_at`, `updated_at`
- **submissions**: Adds `created_at`, `execution_time`, `memory_used`

### New Tables Created:
- **testcases**: For problem test cases
- **testcase_results**: Per-testcase execution results
- **ai_feedback**: AI-generated feedback storage

## 🔍 Verify Migration

```bash
# Check current migration version
python migrate.py current

# Should show: 002 (head)
```

## 🐛 Troubleshooting

### "alembic: command not found"
```bash
pip install alembic
```

### "Table already exists"
Migrations are safe - they won't fail if tables exist.

### "Column already exists"
Migration 002 handles this gracefully.

### Start Fresh
```bash
# Drop all tables (WARNING: deletes data!)
alembic downgrade base

# Recreate everything
python migrate.py upgrade
```

## 📊 Manual Verification

Connect to PostgreSQL and check:

```sql
-- Check users table
\d users

-- Should have: id, name, email, password, created_at, updated_at

-- Check submissions table
\d submissions

-- Should have: id, user_id, problem_id, code, language, status, 
--              execution_time, memory_used, created_at
```

---

**Status**: Migration system ready
**Next**: Run `python migrate.py upgrade`
