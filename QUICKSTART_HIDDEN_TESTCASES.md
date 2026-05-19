# Hidden Testcase System - Quick Start ⚡

## 3-Step Setup (Manual SQL Approach)

### Step 1: Add Database Columns
Run this SQL in **pgAdmin** or **psql**:

```sql
-- Add score column to submissions
ALTER TABLE submissions 
ADD COLUMN IF NOT EXISTS score FLOAT DEFAULT 0.0 NOT NULL;

-- Add is_admin column to users
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE NOT NULL;
```

**OR** run the SQL file:
```bash
cd backend
# Then execute add_hidden_testcase_columns.sql in pgAdmin
```

### Step 2: Populate Testcases
```bash
cd backend
python add_testcases.py
```

### Step 3: Restart Backend
```bash
python run.py
```

**That's it!** The hidden testcase system is now active.

## What You Get

✅ **Weighted Scoring (0-100)** - Each testcase has a weight, score calculated automatically
✅ **Sample Testcases** - Visible to users with full input/output details
✅ **Hidden Testcases** - Only pass/fail shown, input/output hidden
✅ **Score Display** - Shown in Judge page, History, and Submission Detail
✅ **Admin Management** - Create/update/delete testcases (admin only)

## Quick Test

1. Login to the app
2. Select any problem
3. Submit code
4. See your score! (e.g., "75.0/100")

## Create Admin User (Optional)

```sql
-- Connect to PostgreSQL
UPDATE users SET is_admin = true WHERE email = 'your@email.com';
```

## Testcase Weights

Each problem now has weighted testcases:
- **Sample testcases**: Lower weight (visible to users)
- **Hidden testcases**: Higher weight (only pass/fail shown)
- **Total**: Always adds up to 100 for easy percentage

## Example Score Calculation

Problem with 4 testcases:
- Sample 1: weight 20 ✅ Passed
- Sample 2: weight 20 ✅ Passed  
- Hidden 1: weight 30 ❌ Failed
- Hidden 2: weight 30 ✅ Passed

**Score = (20 + 20 + 30) / 100 × 100 = 70.0**

## Need More Details?

See `HIDDEN_TESTCASE_IMPLEMENTATION.md` for complete documentation.

## Troubleshooting

**Migrations fail?**
- Check PostgreSQL is running
- Verify `.env` database credentials

**No testcases?**
- Run `python add_testcases.py`
- Check problems exist in database

**Score not showing?**
- Clear browser cache
- Restart backend server
- Check migrations applied

## Files to Know

- `backend/add_testcases.py` - Populate testcases with weights
- `backend/setup_hidden_testcases.py` - Automated setup script
- `backend/HIDDEN_TESTCASE_SYSTEM.md` - Full documentation
- `HIDDEN_TESTCASE_IMPLEMENTATION.md` - Implementation summary
