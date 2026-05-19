-- SQL script to add columns for Hidden Testcase System
-- Run this in pgAdmin if migrations fail

-- Add score column to submissions table
ALTER TABLE submissions 
ADD COLUMN IF NOT EXISTS score FLOAT DEFAULT 0.0 NOT NULL;

-- Add is_admin column to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE NOT NULL;

-- Verify columns were added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'submissions' AND column_name = 'score';

SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'is_admin';

-- Success message
SELECT 'Hidden Testcase System columns added successfully!' as status;
