# 🚀 Phase 1 Implementation - Complete Guide

## ✅ What We've Built So Far

### 1. Database Models (Complete)
- ✅ `Testcase` model - stdin/stdout with sample/hidden flag
- ✅ `TestcaseResult` model - per-testcase execution results
- ✅ `AIFeedback` model - AI-generated feedback storage
- ✅ Updated relationships in existing models

### 2. Schemas (Complete)
- ✅ Testcase schemas (create, response, public)
- ✅ TestcaseResult schema
- ✅ AIFeedback schema
- ✅ Enhanced Submission schemas with testcase support

### 3. Services (Complete)
- ✅ `CodeExecutor` - Docker + subprocess execution
- ✅ `AIFeedbackService` - GPT-4 powered feedback

## 📋 Next Steps to Complete Phase 1

### Step 1: Update requirements.txt
Add these dependencies:
```txt
# AI & Code Execution
openai==1.12.0
docker==7.0.0

# Code Analysis (optional for Phase 2)
radon==6.0.1
bandit==1.7.7
```

### Step 2: Update .env
Add OpenAI API key:
```env
# AI Feedback
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 3: Create Enhanced Endpoints

#### A. Testcase Management Endpoints
File: `backend/app/api/v1/endpoints/testcases.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.testcase import Testcase
from app.models.problem import Problem
from app.models.user import User
from app.schemas.testcase import TestcaseCreate, TestcaseResponse, TestcasePublic
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=TestcaseResponse, status_code=status.HTTP_201_CREATED)
def create_testcase(
    testcase_data: TestcaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new testcase for a problem (protected)"""
    
    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == testcase_data.problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    # Create testcase
    testcase = Testcase(**testcase_data.dict())
    db.add(testcase)
    db.commit()
    db.refresh(testcase)
    
    return testcase


@router.get("/problem/{problem_id}", response_model=List[TestcasePublic])
def get_problem_testcases(
    problem_id: int,
    db: Session = Depends(get_db)
):
    """Get testcases for a problem (only sample testcases shown)"""
    
    testcases = db.query(Testcase).filter(
        Testcase.problem_id == problem_id
    ).all()
    
    # Return public view (hide expected output for hidden testcases)
    public_testcases = []
    for tc in testcases:
        public_tc = {
            "id": tc.id,
            "is_sample": tc.is_sample,
            "description": tc.description,
            "stdin": tc.stdin if tc.is_sample else None,
            "expected_output": tc.expected_output if tc.is_sample else None
        }
        public_testcases.append(public_tc)
    
    return public_testcases
```

#### B. Enhanced Submissions Endpoint
File: `backend/app/api/v1/endpoints/submissions.py` (replace existing)

Key changes:
1. Run code against all testcases
2. Store individual testcase results
3. Calculate overall verdict
4. Track execution metrics
5. Generate AI feedback (async)

#### C. AI Feedback Endpoint
File: `backend/app/api/v1/endpoints/ai_feedback.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.submission import Submission
from app.models.ai_feedback import AIFeedback
from app.models.user import User
from app.schemas.ai_feedback import AIFeedbackResponse
from app.core.security import get_current_user
from app.services.ai_feedback_service import ai_feedback_service

router = APIRouter()


@router.get("/submission/{submission_id}", response_model=AIFeedbackResponse)
def get_ai_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI feedback for a submission"""
    
    # Verify submission belongs to user
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Check if feedback already exists
    feedback = db.query(AIFeedback).filter(
        AIFeedback.submission_id == submission_id
    ).first()
    
    if feedback:
        return feedback
    
    # Generate new feedback
    # ... (implementation in full code)
    
    return feedback
```

### Step 4: Update Router
File: `backend/app/api/v1/router.py`

```python
from app.api.v1.endpoints import auth, problems, submissions, testcases, ai_feedback

api_router.include_router(testcases.router, prefix="/testcases", tags=["Testcases"])
api_router.include_router(ai_feedback.router, prefix="/ai-feedback", tags=["AI Feedback"])
```

### Step 5: Frontend Updates

#### A. Update API Client
File: `frontend/src/utils/api.js`

Add:
```javascript
// Testcases API
export const testcasesAPI = {
  getByProblem: (problemId) => api.get(`/testcases/problem/${problemId}`),
  create: (data) => api.post("/testcases", data),
};

// AI Feedback API
export const aiFeedbackAPI = {
  getBySubmission: (submissionId) => api.get(`/ai-feedback/submission/${submissionId}`),
};
```

#### B. Enhanced Judge Component
File: `frontend/src/Judge.jsx`

Add:
1. Display sample testcases
2. Show testcase results after submission
3. AI feedback button
4. Execution metrics display

#### C. Submission History Page
File: `frontend/src/SubmissionHistory.jsx` (new)

Features:
- List all user submissions
- Filter by problem/status
- View detailed results
- Access AI feedback

### Step 6: Docker Setup (Optional but Recommended)

#### A. Create Dockerfile for Execution
File: `backend/Dockerfile.executor`

```dockerfile
FROM python:3.11-slim

# Install g++ for C++ support
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy and run user code
CMD ["python", "main.py"]
```

#### B. Docker Compose for Development
File: `docker-compose.yml`

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: codejudge
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+psycopg://postgres:postgres@postgres:5432/codejudge
    depends_on:
      - postgres
    volumes:
      - ./backend:/app

volumes:
  postgres_data:
```

## 🎯 Testing Checklist

### Backend Tests
- [ ] Create testcase via API
- [ ] Submit code with multiple testcases
- [ ] Verify testcase results stored correctly
- [ ] Check AI feedback generation
- [ ] Test Docker execution (if enabled)
- [ ] Test subprocess fallback

### Frontend Tests
- [ ] View sample testcases
- [ ] Submit code and see results
- [ ] View testcase-by-testcase results
- [ ] Request AI feedback
- [ ] View submission history

## 📊 Database Migration

Run this to create new tables:
```bash
cd backend
python -c "from app.db.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

Or simply restart the backend (tables auto-create).

## 🚀 Quick Start After Implementation

1. **Install dependencies:**
```bash
cd backend
pip install openai docker radon bandit
```

2. **Update .env:**
```env
OPENAI_API_KEY=sk-...
```

3. **Restart backend:**
```bash
python run.py
```

4. **Test via Swagger:**
- Go to http://localhost:8000/docs
- Create testcases for a problem
- Submit code
- Check AI feedback

## 📈 Resume Impact

After Phase 1, you can claim:

✅ "Built AI-powered code judge with GPT-4 integration for intelligent feedback"
✅ "Implemented Docker-based code execution sandbox for security"
✅ "Designed testcase management system with hidden/sample testcases"
✅ "Developed real-time execution metrics tracking (time/memory)"
✅ "Created comprehensive submission analytics dashboard"

## 🔄 What's Next (Phase 2)

After Phase 1 is complete and tested:
- Real-time collaborative coding (WebSockets)
- Interview rooms
- Shared code editor
- Live presence indicators

---

**Status**: Implementation guide complete
**Next**: Implement endpoints and test
**Estimated Time**: 4-6 hours for full Phase 1
