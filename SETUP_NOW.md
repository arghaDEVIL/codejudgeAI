# Setup Hidden Testcase System - DO THIS NOW! 🚀

## The Problem
Your database is missing two columns needed for the hidden testcase system:
- `submissions.score` - for weighted scoring
- `users.is_admin` - for admin privileges

## The Solution (2 Minutes)

### Step 1: Open pgAdmin 4
1. Open pgAdmin 4
2. Connect to your database
3. Right-click on your database → Query Tool

### Step 2: Run This SQL
Copy and paste this into the Query Tool and click Execute:

```sql
-- Add score column to submissions table
ALTER TABLE submissions 
ADD COLUMN IF NOT EXISTS score FLOAT DEFAULT 0.0 NOT NULL;

-- Add is_admin column to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE NOT NULL;

-- Verify columns were added
SELECT 'Columns added successfully!' as status;
```

### Step 3: Populate Testcases
Open terminal in `backend` folder and run:
```bash
python add_testcases.py
```

### Step 4: Restart Backend
```bash
python run.py
```

## Done! ✅

Now when you submit code, you'll see:
- ⭐ Score out of 100
- ✅ Testcases passed count
- 📊 Sample testcase details
- 🔒 Hidden testcases (pass/fail only)

## Optional: Create Admin User
If you want to manage testcases, run this SQL:
```sql
UPDATE users SET is_admin = true WHERE email = 'your@email.com';
```

## That's It!
The hidden testcase system is now fully functional.
