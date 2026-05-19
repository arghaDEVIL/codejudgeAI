# Hidden Testcase System Implementation

## Overview
Complete implementation of a LeetCode/Codeforces-style hidden testcase system with weighted scoring, sample/hidden testcase separation, and admin-only management.

## Features Implemented

### 1. Database Schema
- **Testcase Model** (`backend/app/models/testcase.py`):
  - `is_sample`: Boolean flag to distinguish sample vs hidden testcases
  - `weight`: Integer (1-100) for weighted scoring
  - `time_limit`: Per-testcase time limit in milliseconds
  - `memory_limit`: Per-testcase memory limit in MB
  - `description`: Optional description for testcases

- **Submission Model** (`backend/app/models/submission.py`):
  - `score`: Float (0-100) for weighted score calculation

- **User Model** (`backend/app/models/user.py`):
  - `is_admin`: Boolean flag for admin privileges

### 2. Migrations
Created two new migrations:
- `003_add_submission_score.py`: Adds score field to submissions table
- `004_add_user_admin_field.py`: Adds is_admin field to users table

**To apply migrations:**
```bash
cd backend
python migrate.py upgrade
```

### 3. Weighted Scoring System
**Logic** (`backend/app/api/v1/endpoints/submissions.py`):
- Each testcase has a weight (default: 1, range: 1-100)
- Score = (sum of weights for passed testcases / total weight) × 100
- Final score is rounded to 2 decimal places
- Score is stored in submission record

**Example:**
- Problem has 6 testcases:
  - 2 sample testcases: weight 10 each (20 total)
  - 4 hidden testcases: weight 20 each (80 total)
  - Total weight: 100
- If user passes all sample + 2 hidden: score = (20 + 40) / 100 × 100 = 60.0

### 4. API Endpoints

#### Public Endpoints (Authenticated Users)
- `GET /api/v1/testcases/problem/{problem_id}`: Get testcases for a problem
  - Returns full details for sample testcases
  - Returns only metadata (no stdin/output) for hidden testcases
  
- `POST /api/v1/submissions/`: Submit code
  - Runs against ALL testcases (sample + hidden)
  - Returns score, passed count, total count
  - Shows detailed results ONLY for sample testcases
  - Hidden testcase results shown as pass/fail only

- `GET /api/v1/submissions/`: Get user's submissions
  - Includes score field in response

- `GET /api/v1/submissions/{id}`: Get submission details
  - Includes score field
  - Shows full details for sample testcase results
  - Shows only pass/fail for hidden testcase results

#### Admin-Only Endpoints
- `POST /api/v1/testcases/`: Create testcase (admin only)
- `PUT /api/v1/testcases/{id}`: Update testcase (admin only)
- `DELETE /api/v1/testcases/{id}`: Delete testcase (admin only)
- `GET /api/v1/testcases/admin/problem/{problem_id}`: Get ALL testcases with full details (admin only)
- `GET /api/v1/testcases/{id}`: Get specific testcase with full details (admin only)

### 5. Security Features
- **Admin Authentication**: `get_admin_user()` function in `backend/app/core/security.py`
  - Verifies user is authenticated AND has `is_admin=True`
  - Returns 403 Forbidden if not admin
  
- **Hidden Testcase Protection**:
  - Hidden testcase stdin/expected_output never exposed in public API responses
  - Only testcase ID, status, and metadata shown for hidden tests
  - Admin endpoints required to view hidden testcase data

### 6. Frontend Updates

#### Judge Page (`frontend/src/Judge.jsx`)
- Added score display in results metrics (4-column grid)
- Score shown as "X.X/100" with yellow star icon
- Sample testcase results shown with full details
- Hidden testcases not shown in results

#### Submission History (`frontend/src/SubmissionHistory.jsx`)
- Added score badge with star icon in submission list
- Score displayed prominently alongside other metrics

#### Submission Detail (`frontend/src/SubmissionDetail.jsx`)
- Added score in metrics section (4-column grid)
- Shows score, testcases passed, execution time, memory
- Sample testcases show full details when failed
- Hidden testcases show only pass/fail status

### 7. Seed Data Script
**Updated** `backend/add_testcases.py`:
- Adds both sample and hidden testcases with proper weights
- Weights configured to total 100 for easy percentage calculation
- Different testcase sets for different problem types:
  - **Addition problems**: 2 sample (10 each) + 4 hidden (20 each)
  - **Factorial problems**: 2 sample (15 each) + 3 hidden (20, 20, 30)
  - **Fibonacci problems**: 2 sample (15 each) + 3 hidden (20, 20, 30)
  - **Hello World**: 1 sample (100)
  - **Generic**: 2 sample (20 each) + 2 hidden (30 each)

**To populate testcases:**
```bash
cd backend
python add_testcases.py
```

## Usage Guide

### For Regular Users
1. Browse problems on Judge page
2. View sample testcases (visible with input/output)
3. Submit code - runs against all testcases
4. See results:
   - Score out of 100
   - Number of testcases passed
   - Detailed results for sample testcases only
   - Hidden testcases shown as count only
5. View submission history with scores

### For Admins
1. Create admin user by setting `is_admin=True` in database:
   ```sql
   UPDATE users SET is_admin = true WHERE email = 'admin@example.com';
   ```

2. Use admin endpoints to manage testcases:
   - Create new testcases with custom weights
   - Update existing testcases
   - Delete testcases
   - View all testcases including hidden ones

3. Admin API example (create testcase):
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/testcases/ \
     -H "Authorization: Bearer <admin_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "problem_id": 1,
       "stdin": "5 10",
       "expected_output": "15",
       "is_sample": false,
       "weight": 25,
       "time_limit": 2000,
       "memory_limit": 256,
       "description": "Hidden: Large numbers"
     }'
   ```

## Testing the System

### 1. Apply Migrations
```bash
cd backend
python migrate.py upgrade
```

### 2. Create Admin User
```sql
-- Connect to PostgreSQL
UPDATE users SET is_admin = true WHERE id = 1;
```

### 3. Populate Testcases
```bash
cd backend
python add_testcases.py
```

### 4. Test Submission Flow
1. Login as regular user
2. Select a problem
3. Submit code
4. Verify:
   - Score is calculated correctly
   - Sample testcases show full details
   - Hidden testcases show only pass/fail
   - Score displayed in all views

### 5. Test Admin Endpoints
1. Login as admin user
2. Use admin endpoints to:
   - View all testcases with full details
   - Create new testcases
   - Update testcase weights
   - Delete testcases

## Architecture Decisions

### Why Weighted Scoring?
- Allows flexible point distribution
- Can assign more points to edge cases
- Can assign more points to performance tests
- Matches industry-standard platforms (LeetCode, Codeforces)

### Why Separate Sample/Hidden?
- Educational: Users learn from sample testcases
- Security: Prevents hardcoding solutions
- Fairness: Tests edge cases users might not consider
- Realistic: Matches real coding interview platforms

### Why Admin-Only Management?
- Prevents testcase tampering
- Maintains problem integrity
- Allows curated problem sets
- Enables quality control

## Backward Compatibility
- All existing features continue to work
- Existing submissions get score=0.0 by default
- Existing testcases can be updated with weights
- No breaking changes to existing API contracts

## Future Enhancements
Possible improvements:
1. Partial credit for partially correct solutions
2. Time-based scoring (faster = more points)
3. Memory-based scoring (less memory = more points)
4. Difficulty-based weight multipliers
5. Testcase categories (correctness, edge cases, performance)
6. Batch testcase creation via CSV/JSON import
7. Testcase versioning and history
8. A/B testing different testcase sets

## Files Modified/Created

### Backend
- `backend/app/models/user.py` - Added is_admin field
- `backend/app/models/submission.py` - Added score field
- `backend/app/schemas/submission.py` - Added score to schemas
- `backend/app/core/security.py` - Added get_admin_user() function
- `backend/app/api/v1/endpoints/testcases.py` - Admin-only routes
- `backend/app/api/v1/endpoints/submissions.py` - Weighted scoring logic
- `backend/alembic/versions/003_add_submission_score.py` - New migration
- `backend/alembic/versions/004_add_user_admin_field.py` - New migration
- `backend/add_testcases.py` - Updated with weights
- `backend/HIDDEN_TESTCASE_SYSTEM.md` - This documentation

### Frontend
- `frontend/src/Judge.jsx` - Added score display
- `frontend/src/SubmissionHistory.jsx` - Added score display
- `frontend/src/SubmissionDetail.jsx` - Added score display

## Summary
Complete hidden testcase system with:
✅ Sample and hidden testcase separation
✅ Weighted scoring (0-100)
✅ Admin-only testcase management
✅ Security: Hidden testcase data never exposed
✅ Frontend score display in all views
✅ Backward compatible with existing features
✅ Database migrations ready
✅ Seed data script with proper weights
✅ Comprehensive documentation
