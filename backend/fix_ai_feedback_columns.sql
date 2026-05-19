-- Fix ai_feedback table column sizes to accommodate longer AI responses

ALTER TABLE ai_feedback 
    ALTER COLUMN time_complexity TYPE VARCHAR(500),
    ALTER COLUMN space_complexity TYPE VARCHAR(500);

-- Verify the changes
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'ai_feedback' 
AND column_name IN ('time_complexity', 'space_complexity');
